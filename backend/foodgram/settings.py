import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

AUTH_USER_MODEL = "users.User"

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ["http://localhost:8888", "https://*"]

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "djoser",
    "rest_framework.authtoken",
    "corsheaders",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    "recipes.apps.RecipesConfig",
    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodgram.wsgi.application"
CORS_ORIGIN_ALLOW_ALL = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default=5432),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "EXCEPTION_HANDLER": "api.exception_handlers.custom_exception_handler",
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": False,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "SERIALIZERS": {
        "user_create": "api.serializers.users.CustomUserCreateSerializer",
        "user": "api.serializers.users.CustomUserSerializer",
        "current_user": "api.serializers.users.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user_list": ["rest_framework.permissions.AllowAny"],
        "user": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
    },
}


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_URLS_REGEX = r"^/(api|admin)/.*$"
