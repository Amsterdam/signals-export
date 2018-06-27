import os

from signalsexport.settings_common import *  # noqa F403
from signalsexport.settings_common import DEBUG
from signalsexport.settings_databases import LocationKey,\
    get_docker_host,\
    get_database_key,\
    OVERRIDE_HOST_ENV_VAR,\
    OVERRIDE_PORT_ENV_VAR


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django_extensions',

    'django_filters',
    'django.contrib.gis',

    'datapunt_api',

    'rest_framework',
    'rest_framework_gis',
    'corsheaders',
    'drf_yasg',

    'datasets',
    'api',
    'health'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'authorization_django.authorization_middleware',
    'corsheaders.middleware.CorsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'signalsexport.urls'

WSGI_APPLICATION = 'signalsexport.wsgi.application'

HEALTH_MODEL = 'datasets.MessageLog'

DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'signalsexport'),
        'USER': os.getenv('DATABASE_USER', 'signalsexport'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'signalsexport'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'signalsexport'),
        'USER': os.getenv('DATABASE_USER', 'signalsexport'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5432'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'signalsexport'),
        'USER': os.getenv('DATABASE_USER', 'signalsexport'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432'),
    }
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}


# This is a JWKS used for testing only.
JWKS_TEST_KEY = """
{
    "keys": [
        {
            "kty": "EC",
            "key_ops": [
                "verify",
                "sign"
            ],
            "kid": "2aedafba-8170-4064-b704-ce92b7c89cc6",
            "crv": "P-256",
            "x": "6r8PYwqfZbq_QzoMA4tzJJsYUIIXdeyPA27qTgEJCDw=",
            "y": "Cf2clfAfFuuCB06NMfIat9ultkMyrMQO9Hd2H7O9ZVE=",
            "d": "N1vu0UQUp0vLfaNeM0EDbl4quvvL6m_ltjoAXXzkI3U="
        }
    ]
}
"""

DATAPUNT_AUTHZ = {
    'JWKS': os.getenv('PUB_JWKS', JWKS_TEST_KEY),
    'ALWAYS_OK': LOCAL,
    'MIN_SCOPE': 'SIG/ALL',
    'FORCED_ANONYMOUS_ROUTES': (
        '/status/',
        '/signals_export/static/',
    )
}

SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False,
   'SECURITY_DEFINITIONS': {
      'Signals Export API - Swagger': {
         'type': 'oauth2',
         'authorizationUrl': DATAPUNT_API_URL + "oauth2/authorize",
         'flow': 'implicit',
         'scopes': {
            'SIG/ALL': 'Signals alle authorizaties',
         }
      }
   },
   'OAUTH2_CONFIG': {
      'clientId': 'swagger-ui',
      #  'clientSecret': 'yourAppClientSecret',
      'appName': 'Signal Swagger UI',
   },
}

TEST_RUNNER = 'signalsexport.runner.PytestTestRunner'
FIXTURES_DIR = os.path.join(BASE_DIR, 'fixtures')
