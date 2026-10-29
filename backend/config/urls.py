from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from studio import views

router = DefaultRouter()
for prefix, view in [
    ("projects", views.ProjectViewSet),
    ("services", views.ServiceViewSet),
    ("articles", views.ArticleViewSet),
    ("partners", views.PartnerViewSet),
    ("process", views.ProcessViewSet),
    ("team", views.TeamViewSet),
    ("technologies", views.TechnologyViewSet),
    ("testimonials", views.TestimonialViewSet),
    ("jobs", views.JobViewSet),
    ("statistics", views.StatisticViewSet),
]:
    router.register(prefix, view)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", views.HealthView.as_view(), name="health"),
    path("api/site/", views.SiteView.as_view(), name="site"),
    path("api/settings/", views.SettingsView.as_view(), name="settings"),
    path(
        "api/project-request/", views.LeadCreateView.as_view(), name="project-request"
    ),
    path("api/contact/", views.ContactCreateView.as_view(), name="contact"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/", include(router.urls)),
]
# Production public media is served by Nginx, never from PRIVATE_MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
