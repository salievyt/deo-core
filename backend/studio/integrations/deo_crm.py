"""DEO CRM protocol v1: idempotent receipt + private 512 KiB attachment parts."""

import hashlib
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import UUID

from django.conf import settings

CHUNK_BYTES = 512 * 1024
MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024


class CRMDeliveryError(Exception):
    def __init__(self, message, *, permanent=False, remote_id=None):
        super().__init__(message)
        self.permanent = permanent
        self.remote_id = remote_id


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class DeoCRMClient:
    def __init__(self):
        self.endpoint = settings.CRM_WEBHOOK_URL.rstrip("/") + "/"
        self.token = settings.CRM_API_TOKEN
        parsed = urlsplit(self.endpoint)
        local_http = (
            settings.DEBUG
            and getattr(settings, "CRM_ALLOW_LOCAL_HTTP", False)
            and parsed.scheme == "http"
            and parsed.hostname in ["localhost", "127.0.0.1", "::1"]
        )
        if (
            not (parsed.scheme == "https" or local_http)
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise CRMDeliveryError(
                "CRM: требуется HTTPS endpoint без встроенных учётных данных.",
                permanent=True,
            )
        if not parsed.path.endswith("/api/v1/leads/website/"):
            raise CRMDeliveryError(
                "CRM: endpoint должен оканчиваться /api/v1/leads/website/.",
                permanent=True,
            )
        if len(self.token) < 32:
            raise CRMDeliveryError(
                "CRM: настройте общий ключ длиной не менее 32 символов.", permanent=True
            )

    def request(
        self, url, *, method="GET", body=None, key=None, content_type="application/json"
    ):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if body is not None:
            headers["Content-Type"] = content_type
        if key:
            headers["Idempotency-Key"] = str(key)
        try:
            with build_opener(NoRedirect()).open(
                Request(url, data=body, headers=headers, method=method), timeout=20
            ) as response:
                raw = response.read(65537)
                if not 200 <= response.status < 300:
                    raise CRMDeliveryError(
                        f"CRM HTTP {response.status}", permanent=response.status < 500
                    )
                if len(raw) > 65536:
                    raise CRMDeliveryError(
                        "CRM: слишком большой ответ.", permanent=True
                    )
                result = json.loads(raw)
                if not isinstance(result, dict):
                    raise ValueError("Not an object")
                return result
        except HTTPError as exc:
            raise CRMDeliveryError(
                f"CRM HTTP {exc.code}",
                permanent=exc.code not in [408, 425, 429] and exc.code < 500,
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise CRMDeliveryError(f"CRM transport: {type(exc).__name__}") from exc
        except (ValueError, UnicodeError) as exc:
            raise CRMDeliveryError(
                "CRM: некорректное подтверждение доставки.", permanent=True
            ) from exc

    def check(self):
        result = self.request(self.endpoint + "health/")
        if (
            result.get("service") != "deo-crm-website-ingest"
            or result.get("protocol_version") != 1
            or result.get("chunk_bytes") != CHUNK_BYTES
            or result.get("max_attachment_bytes") != MAX_ATTACHMENT_BYTES
        ):
            raise CRMDeliveryError(
                "CRM: несовместимый endpoint интеграции.", permanent=True
            )
        if not result.get("stage_ready"):
            raise CRMDeliveryError("CRM: не настроена воронка продаж.", permanent=True)
        return result

    @staticmethod
    def verify_receipt(result, lead, remote_id=None):
        try:
            received_id = UUID(str(result["lead_id"]))
            if (
                UUID(str(result["website_request_id"])) != lead.pk
                or type(result["attachment_complete"]) is not bool
                or (remote_id and received_id != remote_id)
            ):
                raise ValueError("Mismatched receipt")
        except (KeyError, TypeError, ValueError) as exc:
            raise CRMDeliveryError(
                "CRM: подтверждение не соответствует заявке.",
                permanent=True,
                remote_id=remote_id,
            ) from exc
        return received_id

    def deliver(self, lead):
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
                "kind",
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
            {
                "protocol_version": 1,
                "id": str(lead.pk),
                "created_at": lead.created_at.isoformat(),
            }
        )
        content = b""
        if lead.attachment:
            with lead.attachment.open("rb") as file:
                content = file.read(MAX_ATTACHMENT_BYTES + 1)
            if not content or len(content) > MAX_ATTACHMENT_BYTES:
                raise CRMDeliveryError(
                    "CRM: некорректный размер вложения.", permanent=True
                )
            payload["attachment"] = {
                "name": lead.attachment_name,
                "size": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "parts": (len(content) + CHUNK_BYTES - 1) // CHUNK_BYTES,
            }
        remote_id = None
        try:
            result = self.request(
                self.endpoint,
                method="POST",
                body=json.dumps(
                    payload, ensure_ascii=False, separators=(",", ":")
                ).encode(),
                key=lead.pk,
            )
            remote_id = self.verify_receipt(result, lead)
            if result["attachment_complete"]:
                return remote_id
            if not content:
                raise CRMDeliveryError(
                    "CRM: получатель ожидает отсутствующее вложение.", permanent=True
                )
            for index, start in enumerate(range(0, len(content), CHUNK_BYTES)):
                result = self.request(
                    f"{self.endpoint}{lead.pk}/attachment/{index}/",
                    method="POST",
                    body=content[start : start + CHUNK_BYTES],
                    key=lead.pk,
                    content_type="application/octet-stream",
                )
                self.verify_receipt(result, lead, remote_id)
            if not result["attachment_complete"]:
                raise CRMDeliveryError("CRM: загрузка вложения не подтверждена.")
            return remote_id
        except CRMDeliveryError as exc:
            exc.remote_id = exc.remote_id or remote_id
            raise
