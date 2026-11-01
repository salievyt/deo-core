from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from studio.models import Project, Lead, LeadDelivery, Article, Partner


class ApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.temp = TemporaryDirectory()
        self.override = override_settings(
            MEDIA_ROOT=Path(self.temp.name) / "public",
            PRIVATE_MEDIA_ROOT=Path(self.temp.name) / "private",
        )
        self.override.enable()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.override.disable)

    def payload(self, **changes):
        return {
            "name": "Test User",
            "email": "demo@example.com",
            "description": "A website for a digital product studio.",
            "projectType": "Website",
            "consent": True,
            "locale": "ru",
            **changes,
        }

    def project(self, **changes):
        return Project.objects.create(
            name="Visible",
            slug="visible",
            product_type="Web app",
            category="Web",
            description_ru="Описание",
            description_en="Description",
            idea_ru="Идея",
            solution_ru="Решение",
            **changes,
        )

    def test_drafts_are_hidden_and_public_content_is_read_only(self):
        visible = self.project(is_published=True)
        Project.objects.create(
            name="Draft", slug="draft", product_type="App", category="Mobile"
        )
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([p["slug"] for p in response.data["results"]], ["visible"])
        self.assertEqual(self.client.get("/api/projects/draft/").status_code, 404)
        self.assertEqual(self.client.post("/api/projects/", {}).status_code, 405)
        self.assertEqual(
            self.client.delete(f"/api/projects/{visible.slug}/").status_code, 405
        )
        self.assertEqual(
            self.client.get("/api/projects/?category=Mobile").data["count"], 0
        )

    def test_snapshot_matches_frontend_and_excludes_future_articles(self):
        self.project(is_published=True)
        Article.objects.create(
            slug="future",
            title_ru="Later",
            title_en="Later",
            body_ru="Future body",
            is_published=True,
            published_at=timezone.localdate() + timedelta(days=1),
        )
        Partner.objects.create(name="Draft partner")
        data = self.client.get("/api/site/").data
        self.assertEqual(data["projects"][0]["description"], "Описание")
        self.assertEqual(data["projects"][0]["descriptionEn"], "Description")
        self.assertEqual(data["articles"], [])
        self.assertEqual(data["partners"], [])
        self.assertEqual(data["settings"]["site_name"], "DEO CORE")

    def test_lead_persists_utm_and_ignores_privileged_fields(self):
        response = self.client.post(
            "/api/project-request/",
            self.payload(
                utm_source="campaign", source="Forged", status="won", notes="Untrusted"
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        lead = Lead.objects.get()
        self.assertEqual(lead.utm_source, "campaign")
        self.assertEqual(lead.source, "Website")
        self.assertEqual(lead.status, "new")
        self.assertEqual(lead.notes, "")
        self.assertNotIn("email", response.data)
        self.assertEqual(self.client.get("/api/project-request/").status_code, 405)

    def test_consent_honeypot_and_short_description_are_rejected(self):
        for changes in [
            {"consent": False},
            {"website": "spam.example"},
            {"description": "short"},
            {"email": "not-email"},
        ]:
            cache.clear()
            response = self.client.post(
                "/api/project-request/", self.payload(**changes), format="json"
            )
            self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(Lead.objects.exists())

    def test_idempotency_does_not_create_duplicate_leads(self):
        data = self.payload(request_id=str(uuid4()))
        first = self.client.post("/api/project-request/", data, format="json")
        second = self.client.post("/api/project-request/", data, format="json")
        self.assertEqual(first.status_code, 201)
        self.assertEqual(first.data["id"], second.data["id"])
        self.assertEqual(Lead.objects.count(), 1)

    def test_disallowed_origin_and_throttling(self):
        response = self.client.post(
            "/api/project-request/",
            self.payload(),
            format="json",
            HTTP_ORIGIN="https://untrusted.example",
        )
        self.assertEqual(response.status_code, 403)
        for _ in range(5):
            self.assertEqual(
                self.client.post(
                    "/api/project-request/", self.payload(), format="json"
                ).status_code,
                201,
            )
        self.assertEqual(
            self.client.post(
                "/api/project-request/", self.payload(), format="json"
            ).status_code,
            429,
        )
        self.assertEqual(Lead.objects.count(), 5)

    def test_attachment_is_private_and_download_requires_model_permission(self):
        upload = SimpleUploadedFile(
            "brief.txt", b"Private project brief.", content_type="text/plain"
        )
        response = self.client.post(
            "/api/project-request/", self.payload(attachment=upload), format="multipart"
        )
        self.assertEqual(response.status_code, 201, response.data)
        lead = Lead.objects.get()
        self.assertTrue(
            str(lead.attachment.path).startswith(
                str((Path(self.temp.name) / "private").resolve())
            )
        )
        url = reverse("admin:studio_lead_attachment", args=[lead.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        user = get_user_model().objects.create_user("staff", is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get(url).status_code, 403)
        user.is_superuser = True
        user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b"".join(response.streaming_content), b"Private project brief."
        )
        response.close()
        self.assertEqual(
            self.client.get(f"/media/{lead.attachment.name}").status_code, 404
        )
        self.assertEqual(
            self.client.get(
                reverse("admin:studio_lead_change", args=[lead.pk])
            ).status_code,
            200,
        )

    def test_invalid_and_oversized_files_are_rejected(self):
        files = [
            SimpleUploadedFile("fake.pdf", b"not a pdf"),
            SimpleUploadedFile("evil.html", b"<script>bad</script>"),
            SimpleUploadedFile("large.txt", b"x" * (5 * 1024 * 1024 + 1)),
        ]
        for upload in files:
            cache.clear()
            response = self.client.post(
                "/api/project-request/",
                self.payload(attachment=upload),
                format="multipart",
            )
            self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(Lead.objects.exists())

    def test_request_size_limit(self):
        response = self.client.generic(
            "POST",
            "/api/project-request/",
            data=b"x",
            content_type="application/json",
            CONTENT_LENGTH=str(7 * 1024 * 1024),
        )
        self.assertEqual(response.status_code, 413)

    def test_contact_endpoint_saves_correct_kind(self):
        response = self.client.post("/api/contact/", self.payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.get().kind, "contact")

    def test_jazzmin_admin_and_api_schema(self):
        self.assertContains(self.client.get("/admin/login/"), "jazzmin")
        response = self.client.get("/api/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/api/project-request/", response.data["paths"])
        self.assertEqual(self.client.get("/api/health/").data, {"status": "ok"})

    def test_seed_is_repeatable_and_preserves_editor_changes(self):
        call_command("seed_content", verbosity=0)
        project = Project.objects.get(slug="deo-crm")
        project.name = "Edited name"
        project.save()
        call_command("seed_content", verbosity=0)
        self.assertEqual(Project.objects.count(), 4)
        self.assertEqual(Project.objects.get(pk=project.pk).name, "Edited name")

    @override_settings(
        CRM_WEBHOOK_URL="https://crm.example.test/leads", CRM_INTEGRATION_MODE="generic"
    )
    def test_delivery_queue_records_and_retries_without_losing_lead(self):
        self.client.post("/api/project-request/", self.payload(), format="json")
        delivery = LeadDelivery.objects.get()
        self.assertEqual(delivery.status, "pending")
        with patch(
            "studio.management.commands.process_crm_queue.build_opener"
        ) as opener:
            opener.return_value.open.side_effect = TimeoutError()
            call_command("process_crm_queue", verbosity=0)
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, "failed")
        self.assertEqual(delivery.attempts, 1)
        self.assertTrue(Lead.objects.exists())
        delivery.next_attempt_at = timezone.now() - timedelta(seconds=1)
        delivery.save()
        with patch(
            "studio.management.commands.process_crm_queue.build_opener"
        ) as opener:
            response = MagicMock()
            response.status = 200
            opener.return_value.open.return_value.__enter__.return_value = response
            call_command("process_crm_queue", verbosity=0)
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(
                request.get_header("Idempotency-key"), str(delivery.lead_id)
            )
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, "sent")

    def test_contact_accepts_message_without_project_type(self):
        response = self.client.post(
            "/api/contact/",
            {
                "name": "Test User",
                "email": "demo@example.com",
                "message": "Please discuss our next project.",
                "consent": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        lead = Lead.objects.get()
        self.assertEqual(lead.project_type, "Other")
        self.assertEqual(lead.description, "Please discuss our next project.")
