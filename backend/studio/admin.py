from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import path, reverse
from django.utils.html import format_html
from . import models


class PublicationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "sort_order", "is_published", "updated_at"]
    list_editable = ["sort_order", "is_published"]
    list_filter = ["is_published"]
    readonly_fields = ["created_at", "updated_at"]
    save_on_top = True
    actions = ["publish", "unpublish"]

    @admin.action(description="Опубликовать выбранные")
    def publish(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации")
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ["updated_at"]
    fieldsets = [
        ("Основное", {"fields": ["site_name"]}),
        ("Первый экран RU", {"fields": ["hero_title_ru", "hero_description_ru"]}),
        ("Первый экран EN", {"fields": ["hero_title_en", "hero_description_en"]}),
        (
            "Контакты",
            {
                "fields": [
                    "email",
                    "telegram_url",
                    "whatsapp_url",
                    "instagram_url",
                    "linkedin_url",
                    "github_url",
                    "address_ru",
                    "address_en",
                ]
            },
        ),
        (
            "SEO",
            {
                "fields": [
                    "seo_title_ru",
                    "seo_title_en",
                    "seo_description_ru",
                    "seo_description_en",
                    "updated_at",
                ]
            },
        ),
    ]

    def has_add_permission(self, request):
        return not models.SiteSettings.objects.exists() and super().has_add_permission(
            request
        )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Project)
class ProjectAdmin(PublicationAdmin):
    search_fields = ["name", "description_ru", "description_en", "slug"]
    list_filter = ["is_published", "status", "category", "industry"]
    prepopulated_fields = {"slug": ["name"]}
    fieldsets = [
        (
            "Проект",
            {
                "fields": [
                    "name",
                    "slug",
                    "product_type",
                    "category",
                    "industry",
                    "year",
                    "status",
                    "is_concept",
                    "sort_order",
                    "is_published",
                ]
            },
        ),
        ("RU", {"fields": ["description_ru", "idea_ru", "solution_ru", "result_ru"]}),
        ("EN", {"fields": ["description_en", "idea_en", "solution_en", "result_en"]}),
        ("Визуал", {"fields": ["cover", "visual", "tags"]}),
        (
            "SEO и даты",
            {"fields": ["seo_title", "seo_description", "created_at", "updated_at"]},
        ),
    ]


@admin.register(models.Service)
class ServiceAdmin(PublicationAdmin):
    search_fields = ["title", "description_ru"]


@admin.register(models.Partner)
class PartnerAdmin(PublicationAdmin):
    search_fields = ["name"]


@admin.register(models.ProcessStep)
class ProcessStepAdmin(PublicationAdmin):
    search_fields = ["title_ru", "title_en", "label"]


@admin.register(models.Article)
class ArticleAdmin(PublicationAdmin):
    search_fields = ["title_ru", "title_en", "body_ru"]
    list_filter = ["is_published", "category", "published_at"]
    prepopulated_fields = {"slug": ["title_en"]}
    fieldsets = [
        (
            "Публикация",
            {
                "fields": [
                    "slug",
                    "category",
                    "author",
                    "reading_minutes",
                    "published_at",
                    "cover",
                    "sort_order",
                    "is_published",
                ]
            },
        ),
        ("RU", {"fields": ["title_ru", "body_ru"]}),
        ("EN", {"fields": ["title_en", "body_en"]}),
        (
            "SEO и даты",
            {"fields": ["seo_title", "seo_description", "created_at", "updated_at"]},
        ),
    ]


@admin.register(models.TeamMember)
class TeamAdmin(PublicationAdmin):
    search_fields = ["name", "role_ru", "role_en"]


@admin.register(models.Technology)
class TechnologyAdmin(PublicationAdmin):
    search_fields = ["name"]
    list_filter = ["is_published", "category"]


@admin.register(models.Testimonial)
class TestimonialAdmin(PublicationAdmin):
    search_fields = ["name", "company", "text_ru"]
    autocomplete_fields = ["project"]


@admin.register(models.Job)
class JobAdmin(PublicationAdmin):
    search_fields = ["title_ru", "title_en", "description_ru"]
    prepopulated_fields = {"slug": ["title_en"]}


@admin.register(models.Statistic)
class StatisticAdmin(PublicationAdmin):
    search_fields = ["label_ru", "label_en"]


@admin.register(models.Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "company",
        "project_type",
        "status",
        "assigned_to",
        "created_at",
    ]
    list_filter = ["status", "project_type", "kind", "locale", "created_at"]
    search_fields = ["name", "email", "company", "contact", "description"]
    date_hierarchy = "created_at"
    list_select_related = ["assigned_to"]
    readonly_fields = [
        "id",
        "source",
        "kind",
        "name",
        "company",
        "email",
        "contact",
        "project_type",
        "description",
        "budget",
        "timeline",
        "locale",
        "consent",
        "consent_version",
        "referrer",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "attachment_download",
        "attachment_name",
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Работа с заявкой",
            {
                "fields": [
                    "id",
                    "status",
                    "assigned_to",
                    "notes",
                    "created_at",
                    "updated_at",
                ]
            },
        ),
        ("Контакт", {"fields": ["name", "company", "email", "contact"]}),
        (
            "Проект",
            {
                "fields": [
                    "project_type",
                    "description",
                    "budget",
                    "timeline",
                    "attachment_name",
                    "attachment_download",
                ]
            },
        ),
        (
            "Источник и согласие",
            {
                "fields": [
                    "source",
                    "kind",
                    "locale",
                    "consent",
                    "consent_version",
                    "referrer",
                    "utm_source",
                    "utm_medium",
                    "utm_campaign",
                    "utm_term",
                    "utm_content",
                ]
            },
        ),
    ]
    actions = ["queue_crm_delivery"]

    @admin.action(
        description="Поставить выбранные заявки в очередь CRM", permissions=["change"]
    )
    def queue_crm_delivery(self, request, queryset):
        if not settings.CRM_WEBHOOK_URL:
            self.message_user(
                request,
                "Сначала настройте CRM_WEBHOOK_URL. Заявки сохранены в Django.",
                level=messages.WARNING,
            )
            return
        count = 0
        for lead in queryset:
            delivery, created = models.LeadDelivery.objects.get_or_create(lead=lead)
            if created:
                count += 1
            elif delivery.status != "sent":
                delivery.status = "pending"
                delivery.attempts = 0
                delivery.next_attempt_at = None
                delivery.save()
                count += 1
        self.message_user(
            request,
            f"В очереди: {count}. Доставка выполняется командой process_crm_queue.",
        )

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        return [
            path(
                "<uuid:object_id>/attachment/",
                self.admin_site.admin_view(self.download_attachment),
                name="studio_lead_attachment",
            )
        ] + super().get_urls()

    @admin.display(description="Скачать вложение")
    def attachment_download(self, obj):
        if not obj or not obj.attachment:
            return "Нет вложения"
        return format_html(
            '<a href="{}">Скачать файл</a>',
            reverse("admin:studio_lead_attachment", args=[obj.pk]),
        )

    def download_attachment(self, request, object_id):
        obj = self.get_object(request, str(object_id))
        if obj is None:
            raise Http404
        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied
        if not obj.attachment:
            raise Http404
        try:
            file = obj.attachment.open("rb")
        except FileNotFoundError as exc:
            raise Http404 from exc
        response = FileResponse(
            file,
            as_attachment=True,
            filename=obj.attachment_name or "attachment",
            content_type="application/octet-stream",
        )
        response["Cache-Control"] = "private, no-store"
        return response


@admin.register(models.LeadDelivery)
class LeadDeliveryAdmin(admin.ModelAdmin):
    list_display = ["lead", "status", "attempts", "last_error", "delivered_at"]
    list_filter = ["status"]
    readonly_fields = [field.name for field in models.LeadDelivery._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "DEO CORE"
admin.site.site_title = "DEO CORE CMS"
admin.site.index_title = "Контент сайта и заявки"
