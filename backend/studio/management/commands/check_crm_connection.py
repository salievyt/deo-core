from django.core.management.base import BaseCommand, CommandError
from studio.integrations.deo_crm import DeoCRMClient, CRMDeliveryError


class Command(BaseCommand):
    help = "Проверяет ключ, версию endpoint и воронку DEO CRM без создания лидов."

    def handle(self, *args, **options):
        try:
            DeoCRMClient().check()
        except CRMDeliveryError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS("DEO CRM доступна. Ключ, протокол и воронка проверены.")
        )
