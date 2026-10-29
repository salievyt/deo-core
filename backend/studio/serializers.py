import re
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers
from . import models
from .validators import validate_attachment


class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="product_type")
    description = serializers.CharField(source="description_ru")
    descriptionEn = serializers.CharField(source="description_en")
    idea = serializers.CharField(source="idea_ru")
    ideaEn = serializers.CharField(source="idea_en")
    solution = serializers.CharField(source="solution_ru")
    solutionEn = serializers.CharField(source="solution_en")
    result = serializers.CharField(source="result_ru")
    resultEn = serializers.CharField(source="result_en")
    isConcept = serializers.BooleanField(source="is_concept")

    class Meta:
        model = models.Project
        fields = [
            "slug",
            "name",
            "type",
            "category",
            "industry",
            "description",
            "descriptionEn",
            "idea",
            "ideaEn",
            "solution",
            "solutionEn",
            "result",
            "resultEn",
            "visual",
            "cover",
            "tags",
            "year",
            "status",
            "isConcept",
            "seo_title",
            "seo_description",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    ru = serializers.CharField(source="description_ru")
    en = serializers.CharField(source="description_en")

    class Meta:
        model = models.Service
        fields = ["id", "title", "ru", "en", "tags", "icon"]


class ProcessStepSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="title_ru")
    en = serializers.CharField(source="title_en")
    text = serializers.CharField(source="text_ru")
    textEn = serializers.CharField(source="text_en")
    items = serializers.JSONField(source="items_ru")
    itemsEn = serializers.JSONField(source="items_en")

    class Meta:
        model = models.ProcessStep
        fields = ["id", "title", "en", "label", "text", "textEn", "items", "itemsEn"]


class PartnerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj) -> str:
        return str(obj.pk)

    class Meta:
        model = models.Partner
        fields = ["id", "name", "logo"]


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="title_ru")
    en = serializers.CharField(source="title_en")
    time = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    bodyEn = serializers.SerializerMethodField()

    def get_time(self, obj) -> str:
        return f"{obj.reading_minutes} min"

    def get_body(self, obj) -> list[str]:
        return [p.strip() for p in obj.body_ru.split("\n\n") if p.strip()]

    def get_bodyEn(self, obj) -> list[str]:
        return [p.strip() for p in obj.body_en.split("\n\n") if p.strip()]

    class Meta:
        model = models.Article
        fields = [
            "slug",
            "title",
            "en",
            "category",
            "body",
            "bodyEn",
            "time",
            "author",
            "cover",
            "published_at",
            "seo_title",
            "seo_description",
        ]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteSettings
        exclude = ["id", "updated_at"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeamMember
        fields = [
            "id",
            "name",
            "role_ru",
            "role_en",
            "bio_ru",
            "bio_en",
            "photo",
            "linkedin_url",
            "github_url",
        ]


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technology
        fields = ["id", "name", "category"]


class TestimonialSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    def get_project(self, obj) -> str | None:
        return obj.project.slug if obj.project and obj.project.is_published else None

    class Meta:
        model = models.Testimonial
        fields = [
            "id",
            "name",
            "company",
            "role",
            "text_ru",
            "text_en",
            "photo",
            "project",
        ]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = [
            "slug",
            "title_ru",
            "title_en",
            "work_format",
            "description_ru",
            "description_en",
            "requirements_ru",
            "requirements_en",
        ]


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistic
        fields = ["id", "label_ru", "label_en", "value"]


class SiteSnapshotSerializer(serializers.Serializer):
    settings = SiteSettingsSerializer(allow_null=True)
    projects = ProjectSerializer(many=True)
    services = ServiceSerializer(many=True)
    processSteps = ProcessStepSerializer(many=True)
    partners = PartnerSerializer(many=True)
    articles = ArticleSerializer(many=True)
    technologies = TechnologySerializer(many=True)


class LeadSerializer(serializers.ModelSerializer):
    projectType = serializers.ChoiceField(
        source="project_type",
        choices=models.Lead._meta.get_field("project_type").choices,
    )
    consent = serializers.BooleanField(required=True)
    website = serializers.CharField(
        write_only=True, required=False, allow_blank=True, max_length=200
    )
    request_id = serializers.UUIDField(
        source="idempotency_key", write_only=True, required=False
    )
    description = serializers.CharField(min_length=10, max_length=5000)
    attachment = serializers.FileField(
        required=False, write_only=True, allow_empty_file=False
    )

    class Meta:
        model = models.Lead
        fields = [
            "name",
            "company",
            "email",
            "contact",
            "projectType",
            "description",
            "budget",
            "timeline",
            "locale",
            "consent",
            "referrer",
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "attachment",
            "website",
            "request_id",
        ]

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError(
                "Необходимо согласие на обработку данных."
            )
        return value

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Не удалось принять заявку.")
        return value

    def validate_attachment(self, value):
        try:
            validate_attachment(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        attachment = validated_data.get("attachment")
        if attachment:
            validated_data["attachment_name"] = (
                re.sub(r"[\x00-\x1f\x7f]", "", attachment.name)[:255] or "attachment"
            )
        validated_data["kind"] = self.context.get("kind", "project")
        # Status, source and assignment are deliberately absent from input fields.
        key = validated_data.pop("idempotency_key", None)
        with transaction.atomic():
            if key:
                lead, created = models.Lead.objects.get_or_create(
                    idempotency_key=key, defaults=validated_data
                )
            else:
                lead = models.Lead.objects.create(**validated_data)
                created = True
            if created and settings.CRM_WEBHOOK_URL:
                models.LeadDelivery.objects.create(lead=lead)
        return lead


class LeadReceiptSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    message = serializers.CharField()


class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()


class ContactSerializer(LeadSerializer):
    projectType = serializers.ChoiceField(
        source="project_type",
        choices=models.Lead._meta.get_field("project_type").choices,
        default="Other",
    )
    description = serializers.CharField(required=False, min_length=10, max_length=5000)
    message = serializers.CharField(
        write_only=True, required=False, min_length=10, max_length=5000
    )

    class Meta(LeadSerializer.Meta):
        fields = LeadSerializer.Meta.fields + ["message"]

    def validate(self, attrs):
        message = attrs.pop("message", None)
        if not attrs.get("description"):
            if not message:
                raise serializers.ValidationError(
                    {"description": "Добавьте описание или сообщение."}
                )
            attrs["description"] = message
        return attrs
