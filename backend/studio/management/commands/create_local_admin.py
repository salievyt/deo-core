import os
import secrets
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Создаёт локального администратора с случайным паролем в приватном файле. Только DEBUG=True."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Используйте createsuperuser для production.")
        user_model = get_user_model()
        if user_model.objects.filter(username="admin").exists():
            self.stdout.write("Локальный admin уже существует; пароль не изменён.")
            return
        target = Path(settings.BASE_DIR) / ".local-admin.txt"
        if target.exists():
            raise CommandError(
                "Файл доступа уже существует; проверьте его перед созданием пользователя."
            )
        password = secrets.token_urlsafe(24)
        user_model.objects.create_superuser(
            username="admin", email="", password=password
        )
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as file:
            file.write(
                f"Локальная админка DEO CORE\nURL: http://localhost:8000/admin/\nЛогин: admin\nПароль: {password}\n"
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Локальный администратор создан. Доступ сохранён в {target.name}."
            )
        )
