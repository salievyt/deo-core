from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from . import models, serializers


def published_articles():
    return models.Article.objects.filter(is_published=True).filter(
        Q(published_at__isnull=True) | Q(published_at__lte=timezone.localdate())
    )


class PublishedViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    filter_backends = [SearchFilter]
    search_fields = []

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class ProjectViewSet(PublishedViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    lookup_field = "slug"
    search_fields = ["name", "description_ru", "description_en"]

    def get_queryset(self):
        qs = super().get_queryset()
        for field in ["category", "industry"]:
            value = self.request.query_params.get(field)
            if value:
                qs = qs.filter(**{field: value})
        return qs


class ServiceViewSet(PublishedViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class ArticleViewSet(PublishedViewSet):
    queryset = published_articles()
    serializer_class = serializers.ArticleSerializer
    lookup_field = "slug"
    search_fields = ["title_ru", "title_en", "body_ru"]

    def get_queryset(self):
        return published_articles()


class PartnerViewSet(PublishedViewSet):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer


class ProcessViewSet(PublishedViewSet):
    queryset = models.ProcessStep.objects.all()
    serializer_class = serializers.ProcessStepSerializer


class TeamViewSet(PublishedViewSet):
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamSerializer


class TechnologyViewSet(PublishedViewSet):
    queryset = models.Technology.objects.all()
    serializer_class = serializers.TechnologySerializer


class TestimonialViewSet(PublishedViewSet):
    queryset = models.Testimonial.objects.select_related("project")
    serializer_class = serializers.TestimonialSerializer


class JobViewSet(PublishedViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    lookup_field = "slug"


class StatisticViewSet(PublishedViewSet):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer


class SettingsView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = serializers.SiteSettingsSerializer

    def get_object(self):
        return models.SiteSettings.objects.first() or models.SiteSettings()


class SiteView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(responses=serializers.SiteSnapshotSerializer)
    def get(self, request):
        data = {
            "settings": models.SiteSettings.objects.first() or models.SiteSettings(),
            "projects": models.Project.objects.filter(is_published=True),
            "services": models.Service.objects.filter(is_published=True),
            "processSteps": models.ProcessStep.objects.filter(is_published=True),
            "partners": models.Partner.objects.filter(is_published=True),
            "articles": published_articles(),
            "technologies": models.Technology.objects.filter(is_published=True),
        }
        return Response(
            serializers.SiteSnapshotSerializer(data, context={"request": request}).data
        )


class LeadOriginPermission(BasePermission):
    message = "Этот источник запросов не разрешён."

    def has_permission(self, request, view):
        origin = request.headers.get("Origin")
        return not origin or origin.rstrip("/") in settings.CORS_ALLOWED_ORIGINS


class LeadBurstThrottle(AnonRateThrottle):
    scope = "lead_burst"


class LeadDailyThrottle(AnonRateThrottle):
    scope = "lead_daily"


class LeadCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny, LeadOriginPermission]
    authentication_classes = []
    throttle_classes = [LeadBurstThrottle, LeadDailyThrottle]
    serializer_class = serializers.LeadSerializer
    kind = "project"

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "kind": self.kind}

    @extend_schema(responses={201: serializers.LeadReceiptSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        return Response(
            {
                "id": str(lead.pk),
                "message": "Спасибо. Мы получили вашу заявку и свяжемся с вами.",
            },
            status=status.HTTP_201_CREATED,
        )


class ContactCreateView(LeadCreateView):
    kind = "contact"
    serializer_class = serializers.ContactSerializer


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(responses=serializers.HealthSerializer)
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            return Response({"status": "unavailable"}, status=503)
        return Response({"status": "ok"})
