import json
from pathlib import Path
from datetime import date
from django.core.management import call_command
from django.core.management.base import BaseCommand
from studio.models import (
    SiteSettings,
    Project,
    Service,
    ProcessStep,
    Article,
    Partner,
    Technology,
)


class Command(BaseCommand):
    help = (
        "Переносит текущий демо-контент фронтенда в CMS, сохраняя существующие записи."
    )

    def handle(self, *args, **options):
        data = json.loads(
            (
                Path(__file__).resolve().parents[2] / "fixtures/site_content.json"
            ).read_text()
        )
        SiteSettings.objects.get_or_create(pk=1)
        for i, p in enumerate(data["projects"]):
            Project.objects.get_or_create(
                slug=p["slug"],
                defaults={
                    "name": p["name"],
                    "product_type": p["type"],
                    "category": p["category"],
                    "description_ru": p["description"],
                    "description_en": p["descriptionEn"],
                    "idea_ru": p["idea"],
                    "solution_ru": p["solution"],
                    "visual": p["visual"],
                    "tags": p["tags"],
                    "sort_order": i,
                    "is_published": True,
                    "is_concept": True,
                },
            )
        for i, s in enumerate(data["services"]):
            Service.objects.get_or_create(
                title=s["title"],
                defaults={
                    "description_ru": s["ru"],
                    "description_en": s["en"],
                    "tags": s["tags"],
                    "icon": s["icon"],
                    "sort_order": i,
                    "is_published": True,
                },
            )
        for i, s in enumerate(data["processSteps"]):
            ProcessStep.objects.get_or_create(
                label=s["label"],
                defaults={
                    "title_ru": s["title"],
                    "title_en": s["en"],
                    "text_ru": s["text"],
                    "text_en": s["textEn"],
                    "items_ru": s["items"],
                    "items_en": s["itemsEn"],
                    "sort_order": i,
                    "is_published": True,
                },
            )
        for i, a in enumerate(data["articles"]):
            Article.objects.get_or_create(
                slug=a["slug"],
                defaults={
                    "title_ru": a["title"],
                    "title_en": a["en"],
                    "category": a["category"],
                    "body_ru": "\n\n".join(a["body"]),
                    "reading_minutes": int(a["time"].split()[0]),
                    "published_at": date(2026, 10, 28),
                    "sort_order": i,
                    "is_published": True,
                },
            )
        for i in range(6):
            Partner.objects.get_or_create(
                name=f"Партнёр {i + 1:02d}",
                defaults={"sort_order": i, "is_published": True},
            )
        for i, (name, category) in enumerate(
            [
                ("Next.js", "Frontend"),
                ("React", "Frontend"),
                ("Flutter", "Mobile"),
                ("Python", "Backend"),
                ("Django", "Backend"),
                ("Figma", "Design"),
            ]
        ):
            Technology.objects.get_or_create(
                name=name,
                defaults={"category": category, "sort_order": i, "is_published": True},
            )
        call_command("bootstrap_roles")
        self.stdout.write(
            self.style.SUCCESS(
                "Контент готов. Существующие записи не перезаписывались."
            )
        )
