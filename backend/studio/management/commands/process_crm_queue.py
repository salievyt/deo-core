import base64
import json
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.db.models import Q
from django.utils import timezone
from studio.models import LeadDelivery


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Command(BaseCommand):
    help = "Доставляет ожидающие заявки в настроенный CRM webhook; запускать по расписанию."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=20)

    def handle(self, *args, **options):
        endpoint = settings.CRM_WEBHOOK_URL
        if not endpoint:
            raise CommandError(
                "CRM_WEBHOOK_URL не настроен. Заявки сохранены в Django."
            )
        parsed = urlparse(endpoint)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            raise CommandError(
                "CRM_WEBHOOK_URL должен быть HTTPS URL без встроенных учётных данных."
            )
        if options["limit"] < 1 or options["limit"] > 500:
            raise CommandError("limit: от 1 до 500.")
        sent = 0
        for _ in range(options["limit"]):
            with transaction.atomic():
                qs = (
                    LeadDelivery.objects.filter(
                        status__in=["pending", "failed"], attempts__lt=5
                    )
                    .filter(
                        Q(next_attempt_at__isnull=True)
                        | Q(next_attempt_at__lte=timezone.now())
                    )
                    .order_by("created_at")
                )
                qs = (
                    qs.select_for_update(skip_locked=True)
                    if connection.features.has_select_for_update_skip_locked
                    else qs.select_for_update()
                )
                delivery = qs.first()
                if not delivery:
                    break
                lead = delivery.lead
                payload = {
                    field: getattr(lead, field)
                    for field in [
                        "name",
                        "company",
                        "email",
                        "contact",
                        "project_type",
                        "description",
                        "budget",
                        "timeline",
                        "locale",
                        "source",
                        "referrer",
                        "utm_source",
                        "utm_medium",
                        "utm_campaign",
                        "utm_term",
                        "utm_content",
                        "consent",
                        "consent_version",
                    ]
                }
                payload.update(
                    {"id": str(lead.pk), "created_at": lead.created_at.isoformat()}
                )
                delivery.attempts += 1
                try:
                    if lead.attachment:
                        with lead.attachment.open("rb") as file:
                            payload["attachment"] = {
                                "name": lead.attachment_name,
                                "contentBase64": base64.b64encode(file.read()).decode(
                                    "ascii"
                                ),
                            }
                    headers = {
                        "Content-Type": "application/json",
                        "Idempotency-Key": str(lead.pk),
                    }
                    if settings.CRM_API_TOKEN:
                        headers["Authorization"] = f"Bearer {settings.CRM_API_TOKEN}"
                    request = Request(
                        endpoint,
                        data=json.dumps(payload, ensure_ascii=False).encode(),
                        headers=headers,
                        method="POST",
                    )
                    with build_opener(NoRedirect()).open(
                        request, timeout=15
                    ) as response:
                        if not 200 <= response.status < 300:
                            raise HTTPError(
                                endpoint,
                                response.status,
                                "Unexpected status",
                                None,
                                None,
                            )
                    delivery.status = "sent"
                    delivery.delivered_at = timezone.now()
                    delivery.last_error = ""
                    delivery.next_attempt_at = None
                    sent += 1
                except (HTTPError, URLError, TimeoutError, OSError) as exc:
                    delivery.status = "failed"
                    delivery.last_error = (
                        f"HTTP {exc.code}"
                        if isinstance(exc, HTTPError)
                        else type(exc).__name__
                    )
                    delivery.next_attempt_at = timezone.now() + timedelta(
                        minutes=2**delivery.attempts
                    )
                delivery.save()
        self.stdout.write(
            self.style.SUCCESS(f"Доставлено: {sent}. Лимит попыток на заявку: 5.")
        )
