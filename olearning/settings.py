# Django settings for olearning project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# ---------- Automatically synchronize to the sae mysql database ---------
if not DEBUG:  
    #from sae._restful_mysql import monkey  
    #monkey.patch()  
    
    MYSQL_HOST_M = 'w.rdc.sae.sina.com.cn'  
    MYSQL_PORT = '3307'  
    MYSQL_USER = 'xjl22oll45'  
    MYSQL_PASS = '122h1h5zmk5xhkih20jww5j253mm0y30k44515ik'  
    MYSQL_DB   = 'app_olearning'  
else:
    MYSQL_HOST_M = '127.0.0.1'  
    MYSQL_PORT = '3306'  
    MYSQL_USER = 'root'  
    MYSQL_PASS = 'admin'  
    MYSQL_DB   = 'olearning'  

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST_M,
        'PORT':     MYSQL_PORT,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',                      # Or path to database file if using sqlite3.
#         'USER': '',                      # Not used with sqlite3.
#         'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# file upload max size
FILE_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024

# temporare file directory
FILE_UPLOAD_TEMP_DIR='/home/yiranyaoqiu/olearning/1'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

HERE=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
if DEBUG:
    MEDIA_ROOT = os.path.join(HERE,'media').replace('\\','/')+'/'
else:
    MEDIA_ROOT = 'http://olearning-resources.sinaapp.com/'


# message type
SYSMSG,TASKMSG,COURSEMSG,EXAMMSG,CONTACTMSG,LEARNMSG=(1,2,3,4,5,6)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
if DEBUG:
    MEDIA_URL='/media/'
else:
    MEDIA_URL='http://olearning-resources.stor.sinaapp.com/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if not DEBUG:
    SITE_ROOT=os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
    STATIC_ROOT = os.path.join(SITE_ROOT,'static')
else:
    STATIC_ROOT=''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/home/yiranyaoqiu/olearning/1/static',
)

if not DEBUG:
    STATICFILES_DIRS += (
        ("css", os.path.join(STATIC_ROOT,'css')),
        ("js", os.path.join(STATIC_ROOT,'js')),
        ("image", os.path.join(STATIC_ROOT,'image')),
        ("theme", os.path.join(STATIC_ROOT,'theme')),
        ("json", os.path.join(STATIC_ROOT,'json')),
        ("upload_xls", os.path.join(STATIC_ROOT,'upload_xls')),
    )
else:
    STATICFILES_DIRS += (
        '/home/yiranyaoqiu/olearning/1/static',
    )

# List of finder classes that know how to find static files in
# various locations.

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'giyw#erde7o841m70fi=^e0eo6-m)83jzu_y)q12skq+0@*etf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


LOGIN_URL=r'/index/'
LOGIN_EXEMPT_URLS = (
    r'^login/',
    r'^help/',
    r'^about/',
    r'^logout/',
    r'^findpwd/',
)

MAIN_URLS = (
    '/student/',
    '/teacher/',
    '/admin/',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'tools.MyLoginRequiredMiddle.LoginRequiredMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    # transaction
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'olearning.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'olearning.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'index',
    'admin',
    'contact',
    'course',
    'exam',
    'learn',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# email
EMAIL_HOST='smtp.qq.com'
EMAIL_HOST_USER='1491634755@qq.com'
EMAIL_HOST_PASSWORD='abcde123456'
