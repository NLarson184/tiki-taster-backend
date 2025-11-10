from dotenv import load_dotenv
import os
from pathlib import Path
import dj_database_url

# Load any environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['api.tikitaster.com']
if DEBUG:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django.contrib.sites',
    
    'rest_framework',
    
    'oauth2_provider', # Required by DRFSO2
    'social_django',  # Required by DRFSO2
    'drf_social_oauth2',
    'accounts',
    'ratings',
]

SITE_ID = 1

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': None,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Use OAuth2Authentication for standard token validation
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # Use SocialAuthentication for handling token conversion flow
        # 'drf_social_oauth2.authentication.SocialAuthentication',
        # Keep for DRF browsable API and standard session access
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# This is required for email/password login via /auth/token.
DRFSO2_PASSWORD = 'django.contrib.auth.backends.ModelBackend'


# Without this, the /auth/token endpoint rejects the request globally.
OAUTH2_PROVIDER = {
    'ALLOWED_GRANT_TYPES': [
        'password',
        'client_credentials',
        'authorization_code',
        'refresh_token',
    ],
    # You can adjust token expiration here if needed (default is 1 hour)
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600, 
}

# Social_django backends
AUTHENTICATION_BACKENDS = (
    # NEW: Add the social_core password backend here as the primary login mechanism
    'social_core.backends.email.EmailAuth',
    
    # 1. Standard Django login backend (required for DRFSO2_PASSWORD setting)
    'django.contrib.auth.backends.ModelBackend',
    
    # 2. Google OpenID Connect backend (Confirmed working for ID Token flow)
    'drf_social_oauth2.backends.GoogleIdentityBackend',
    
    # 3. DRFSO2 token conversion backend (required for /auth/convert-token)
    'drf_social_oauth2.backends.DjangoOAuth2',
)
    
# --- GOOGLE OAUTH2 SETTINGS (Used by GoogleIdentityBackend) ---
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_SOCIAL_LOGIN_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SOCIAL_LOGIN_SECRET')

# Define the scopes you need
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'openid',
    'email',
    'profile'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_ACCESS_TOKEN_METHOD = 'POST'

ROOT_URLCONF = 'tikitaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'tikitaster.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("POSTGRES_DATABASE_URL"),
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set up CORS
if DEBUG:
    # Dev
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:4200'
    ]
else:
    # Prod
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://\w+\.tikitaster\.com$",
    ]
DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # NEW: CRITICAL to debug token flow issues
        'oauth2_provider': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Existing loggers (keep these)
        'social_core': { 
            'handlers': ['console'],
            'level': 'DEBUG', 
            'propagate': True,
        },
        'drf_social_oauth2': {
            'handlers': ['console'],
            'level': 'DEBUG', 
            'propagate': True,
        },
        # Add the Django request/response logger for general visibility
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}
