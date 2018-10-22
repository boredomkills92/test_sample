"""
Django settings for dwitter project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP_LOG_DIRECTORY = 'logs'
APP_LOG_FILE_NAME= 'dwitter.log'
API_LOG_FILE_NAME = 'dwitter_api.log'

APP_LOG_DIR = os.path.join(BASE_DIR, APP_LOG_DIRECTORY)
APP_LOG_FILE = os.path.join(APP_LOG_DIR, APP_LOG_FILE_NAME)
API_LOG_FILE = os.path.join(APP_LOG_DIR, API_LOG_FILE_NAME)

LOGLEVEL_DEBUG = 'DEBUG'
LOGLEVEL_INFO = 'INFO'
LOGLEVEL_WARNING = 'WARNING'
LOGLEVEL_ERROR = 'ERROR'
LOGLEVEL_CRITICAL = 'CRITICAL'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p9q+f!ct+da0e+3b=p_kip+#&d6gv4vk)p@1ka=cv*&3(+v(69'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost']

#Persistent connection
CONN_MAX_AGE = 600

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'cacheops',
    'userprofile',
    'dweetfeed',
    'dweetfeed.dweets'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drflog.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'dwitter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dwitter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dwitter.sqlite3'),
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dwitter_prod',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


environment = os.environ.get('environment')

if environment.upper() == "prod".upper():
    
    static_file_path = os.environ.get('static_file_path')

    if os.path.exists(os.path.dirname(static_file_path)):
        STATIC_ROOT = os.path.join( static_file_path)
    else:
        STATIC_ROOT = os.path.join( BASE_DIR, "static_prod")

AUTH_USER_MODEL = 'userprofile.UserProfile'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamp': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': LOGLEVEL_INFO,
            'class': 'logging.FileHandler',
            'filename': APP_LOG_FILE,
            'formatter': 'timestamp',
        },
        'api_file': {
            'level': LOGLEVEL_INFO,
            'class': 'logging.FileHandler',
            'filename': API_LOG_FILE,
            'formatter': 'timestamp',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGLEVEL_INFO,
            'propagate': True,
        },
        'drflog': {
            'handlers': ['api_file'],
            'level': LOGLEVEL_INFO,
            'propagate': True,
        },        
    },

}

CACHEOPS_REDIS = "redis://localhost:6379/1"

CACHEOPS = {
    
    'userprofile.UserProfile': {'ops': 'get', 'timeout': 60*15},
    'userprofile.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60},
    'userprofile.permission': {'ops': 'all', 'timeout': 60*60},

    
    'dweetfeed.dweets.*': {'ops': 'get', 'timeout': 60*15},
    'dweetfeed.dweets.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60},
    'dweetfeed.dweets.permission': {'ops': 'all', 'timeout': 60*60},

    '*.*': {'ops': (), 'timeout': 60*60},

    # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*60},
}