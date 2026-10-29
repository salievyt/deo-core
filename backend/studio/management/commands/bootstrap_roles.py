from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группы редакторов и менеджеров заявок с минимальными правами."

    def handle(self, *args, **options):
        editor, _ = Group.objects.get_or_create(name="Редакторы сайта")
        editor.permissions.set(
            Permission.objects.filter(content_type__app_label="studio").exclude(
                content_type__model__in=["lead", "leaddelivery"]
            )
        )
        manager, _ = Group.objects.get_or_create(name="Менеджеры заявок")
        manager.permissions.set(
            Permission.objects.filter(
                content_type__app_label="studio",
                codename__in=["view_lead", "change_lead", "view_leaddelivery"],
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Группы готовы. Назначьте их сотрудникам через /admin/auth/user/."
            )
        )
