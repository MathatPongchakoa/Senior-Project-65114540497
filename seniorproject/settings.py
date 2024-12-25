"""
Django settings for seniorproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z7+xcwcx#x=2oz(5n1gjo5mr7^ussz!lk-lhjwdmsiod#g#wgv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'tableapp',
    'django_browser_reload',
    'django_celery_beat',
    'django_dbml',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = "seniorproject.urls"

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

WSGI_APPLICATION = "seniorproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # ใช้ MySQL
        "NAME": "sn_project",          # ชื่อฐานข้อมูล
        "USER": "root",             # ชื่อผู้ใช้ MySQL
        "PASSWORD": "1234",     # รหัสผ่าน MySQL
        "HOST": "localhost",                   # หรือที่อยู่ของ MySQL Server
        "PORT": "3306",
        'OPTIONS': {
            'charset': 'utf8mb4',
        },                   # พอร์ตของ MySQL (ค่าเริ่มต้นคือ 3306)
    },
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

TIME_ZONE = 'Asia/Bangkok'

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# settings.py
PASSWORD_RESET_TIMEOUT = 86400  # 1 วัน


# เพิ่มการตั้งค่าสำหรับการเข้าสู่ระบบ
LOGIN_REDIRECT_URL = '/table-status/'  
LOGOUT_REDIRECT_URL = '/'  
AUTH_USER_MODEL = 'tableapp.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # หรือโฮสต์ SMTP ที่คุณใช้
EMAIL_PORT = 587  # ใช้ 587 สำหรับ TLS หรือ 465 สำหรับ SSL
EMAIL_USE_TLS = True  # ถ้าใช้ TLS
EMAIL_HOST_USER = 'mathat.po.65@ubu.ac.th'  # อีเมลผู้ส่ง
EMAIL_HOST_PASSWORD = 'hnos oqff kuep voar'  # รหัสผ่านของอีเมล
DEFAULT_FROM_EMAIL = 'mathat.po.65@ubu.ac.th'


# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'







