import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_list(name, default=""):
    return [
        value.strip() for value in os.getenv(name, default).split(",") if value.strip()
    ]


DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY before running in production."
        )
    SECRET_KEY = "development-only-deo-core-do-not-use-in-production"
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001"
)
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_CREDENTIALS = False

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "studio",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "studio.middleware.RequestSizeMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=60,
        conn_health_checks=True,
    )
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский"), ("en", "English")]
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
PRIVATE_MEDIA_ROOT = BASE_DIR / "private_uploads"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 50
DATA_UPLOAD_MAX_NUMBER_FILES = 1
MAX_REQUEST_BYTES = 6 * 1024 * 1024
redis_url = os.getenv("REDIS_URL")
CACHES = {
    "default": (
        {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": redis_url,
        }
        if redis_url
        else {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": str(BASE_DIR / ".cache"),
        }
    )
}
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_THROTTLE_RATES": {"lead_burst": "5/minute", "lead_daily": "30/day"},
    "NUM_PROXIES": int(os.getenv("DJANGO_NUM_PROXIES", "0")),
    "EXCEPTION_HANDLER": "studio.exceptions.api_exception_handler",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "DEO CORE API",
    "VERSION": "1.0.0",
    "DESCRIPTION": "Публичный контент сайта и приём заявок. Редактирование — через Jazzmin /admin/.",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "COMPONENT_SPLIT_REQUEST": True,
}
JAZZMIN_SETTINGS = {
    "site_title": "DEO CORE CMS",
    "site_header": "DEO CORE",
    "site_brand": "DEO CORE",
    "site_logo": "branding/logo.svg",
    "site_icon": "branding/icon.svg",
    "welcome_sign": "Управление сайтом DEO CORE",
    "copyright": "DEO CORE",
    "search_model": ["studio.Project", "studio.Lead", "studio.Article"],
    "show_ui_builder": False,
    "custom_css": "branding/deo-admin.css",
    "use_google_fonts_cdn": False,
    "order_with_respect_to": [
        "studio",
        "studio.Lead",
        "studio.SiteSettings",
        "studio.Project",
        "studio.Service",
        "studio.Partner",
        "studio.Article",
        "studio.ProcessStep",
        "studio.TeamMember",
        "studio.Technology",
        "studio.Testimonial",
        "studio.Job",
        "studio.Statistic",
        "studio.LeadDelivery",
        "auth",
    ],
    "topmenu_links": [
        {
            "name": "Открыть сайт",
            "url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
            "new_window": True,
        },
        {"name": "API / документация", "url": "/api/docs/", "new_window": True},
    ],
    "icons": {
        "studio.Lead": "fas fa-inbox",
        "studio.SiteSettings": "fas fa-sliders-h",
        "studio.Project": "fas fa-layer-group",
        "studio.Service": "fas fa-code",
        "studio.Partner": "fas fa-handshake",
        "studio.Article": "fas fa-pen-nib",
        "studio.ProcessStep": "fas fa-route",
        "studio.TeamMember": "fas fa-users",
        "studio.Technology": "fas fa-cubes",
        "studio.Testimonial": "fas fa-quote-left",
        "studio.Job": "fas fa-briefcase",
        "studio.Statistic": "fas fa-chart-bar",
        "studio.LeadDelivery": "fas fa-exchange-alt",
    },
    "changeform_format": "horizontal_tabs",
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-orange",
}
CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL", "")
CRM_API_TOKEN = os.getenv("CRM_API_TOKEN", "")
CRM_INTEGRATION_MODE = os.getenv("CRM_INTEGRATION_MODE", "generic")
CRM_ALLOW_LOCAL_HTTP = os.getenv("CRM_ALLOW_LOCAL_HTTP", "false").lower() == "true"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
# Enable only behind a proxy that overwrites this header.
if os.getenv("DJANGO_TRUST_PROXY", "false").lower() == "true":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
