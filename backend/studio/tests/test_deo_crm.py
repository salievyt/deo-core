import hashlib
import json
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError
from uuid import uuid4
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.core.management import call_command
from studio.models import Lead, LeadDelivery
from studio.integrations.deo_crm import DeoCRMClient, CRMDeliveryError, CHUNK_BYTES

TOKEN = "test-integration-key-more-than-32-characters"
ENDPOINT = "https://crm.backend.deo-core.codes/api/v1/leads/website/"


@override_settings(
    CRM_WEBHOOK_URL=ENDPOINT, CRM_API_TOKEN=TOKEN, CRM_INTEGRATION_MODE="deo_core"
)
class DeoCRMTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.override = override_settings(PRIVATE_MEDIA_ROOT=self.temp.name)
        self.override.enable()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.override.disable)
        self.lead = Lead.objects.create(
            name="Integration test",
            email="demo@example.com",
            project_type="Website",
            description="Test integration request from the website.",
            consent=True,
        )
        self.remote_id = uuid4()

    def receipt(self, complete=True):
        return {
            "lead_id": str(self.remote_id),
            "website_request_id": str(self.lead.pk),
            "attachment_complete": complete,
        }

    def test_health_checks_marker_without_creating_a_lead(self):
        with patch.object(
            DeoCRMClient,
            "request",
            return_value={
                "status": "ok",
                "service": "deo-crm-website-ingest",
                "protocol_version": 1,
                "chunk_bytes": CHUNK_BYTES,
                "max_attachment_bytes": 5 * 1024 * 1024,
                "stage_ready": True,
            },
        ) as request:
            DeoCRMClient().check()
            self.assertEqual(request.call_args.args[0], ENDPOINT + "health/")
        with patch.object(DeoCRMClient, "request", return_value={"status": "ok"}):
            with self.assertRaises(CRMDeliveryError):
                DeoCRMClient().check()

    def test_acknowledgement_is_required_and_request_is_idempotent(self):
        with patch.object(
            DeoCRMClient, "request", return_value=self.receipt()
        ) as request:
            self.assertEqual(DeoCRMClient().deliver(self.lead), self.remote_id)
            payload = json.loads(request.call_args.kwargs["body"])
            self.assertEqual(payload["protocol_version"], 1)
            self.assertEqual(payload["id"], str(self.lead.pk))
            self.assertEqual(request.call_args.kwargs["key"], self.lead.pk)
        for bad in [
            {},
            {
                "lead_id": str(self.remote_id),
                "website_request_id": str(uuid4()),
                "attachment_complete": True,
            },
        ]:
            with patch.object(DeoCRMClient, "request", return_value=bad):
                with self.assertRaises(CRMDeliveryError):
                    DeoCRMClient().deliver(self.lead)

    def test_attachment_is_split_and_final_receipt_is_verified(self):
        content = b"brief " * (CHUNK_BYTES // 6 + 1000)
        self.lead.attachment.save("brief.txt", ContentFile(content))
        self.lead.attachment_name = "brief.txt"
        self.lead.save()
        with patch.object(
            DeoCRMClient,
            "request",
            side_effect=[self.receipt(False), self.receipt(False), self.receipt(True)],
        ) as request:
            self.assertEqual(DeoCRMClient().deliver(self.lead), self.remote_id)
            calls = request.call_args_list
            payload = json.loads(calls[0].kwargs["body"])
            self.assertEqual(
                payload["attachment"]["sha256"], hashlib.sha256(content).hexdigest()
            )
            self.assertNotIn("contentBase64", payload["attachment"])
            self.assertEqual(calls[1].kwargs["body"], content[:CHUNK_BYTES])
            self.assertEqual(calls[2].kwargs["body"], content[CHUNK_BYTES:])
            self.assertTrue(
                all(len(c.kwargs["body"]) <= CHUNK_BYTES for c in calls[1:])
            )

    def test_partial_upload_keeps_remote_id_for_retry(self):
        self.lead.attachment.save("brief.txt", ContentFile(b"brief"))
        self.lead.attachment_name = "brief.txt"
        self.lead.save()
        with patch.object(
            DeoCRMClient,
            "request",
            side_effect=[self.receipt(False), CRMDeliveryError("CRM timeout")],
        ):
            with self.assertRaises(CRMDeliveryError) as result:
                DeoCRMClient().deliver(self.lead)
        self.assertEqual(result.exception.remote_id, self.remote_id)

    def test_queue_records_crm_id_and_permanent_failures_stop_retrying(self):
        delivery = LeadDelivery.objects.create(lead=self.lead)
        with patch.object(DeoCRMClient, "deliver", return_value=self.remote_id):
            call_command("process_crm_queue", verbosity=0)
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, "sent")
        self.assertEqual(delivery.crm_lead_id, self.remote_id)
        delivery.status = "pending"
        delivery.save()
        with patch.object(
            DeoCRMClient,
            "deliver",
            side_effect=CRMDeliveryError("CRM HTTP 401", permanent=True),
        ):
            call_command("process_crm_queue", verbosity=0)
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, "failed")
        self.assertEqual(delivery.attempts, 5)
        self.assertIsNone(delivery.next_attempt_at)

    def test_insecure_endpoint_is_disabled_outside_explicit_local_debug_mode(self):
        with override_settings(
            CRM_WEBHOOK_URL="http://crm.backend.deo-core.codes/api/v1/leads/website/",
            CRM_ALLOW_LOCAL_HTTP=True,
            DEBUG=True,
        ):
            with self.assertRaises(CRMDeliveryError):
                DeoCRMClient()
        with override_settings(
            CRM_WEBHOOK_URL="http://127.0.0.1:8001/api/v1/leads/website/",
            CRM_ALLOW_LOCAL_HTTP=True,
            DEBUG=True,
        ):
            self.assertTrue(DeoCRMClient().endpoint.startswith("http://127.0.0.1"))
        with override_settings(
            CRM_WEBHOOK_URL="http://127.0.0.1:8001/api/v1/leads/website/",
            CRM_ALLOW_LOCAL_HTTP=True,
            DEBUG=False,
        ):
            with self.assertRaises(CRMDeliveryError):
                DeoCRMClient()

    def test_http_errors_are_classified_without_leaking_response_or_credentials(self):
        for code, permanent in [(401, True), (409, True), (429, False), (500, False)]:
            with patch("studio.integrations.deo_crm.build_opener") as opener:
                opener.return_value.open.side_effect = HTTPError(
                    ENDPOINT,
                    code,
                    "Private response",
                    None,
                    BytesIO(b"secret response"),
                )
                with self.assertRaises(CRMDeliveryError) as error:
                    DeoCRMClient().request(ENDPOINT)
                self.assertEqual(error.exception.permanent, permanent)
                self.assertNotIn("secret", str(error.exception))
