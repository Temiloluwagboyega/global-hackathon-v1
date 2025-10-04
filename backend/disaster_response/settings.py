import os
from pathlib import Path
from decouple import config
import mongoengine

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security & Debug
# -----------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'cloudinary_storage',
    'cloudinary',
    'reports',
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL and Templates
# -----------------------------
ROOT_URLCONF = 'disaster_response.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'disaster_response.wsgi.application'

# -----------------------------
# MongoDB (MongoEngine)
# -----------------------------
# MongoDB connection with Atlas-specific SSL configuration
mongodb_connected = False
connection_errors = []

# Strategy 1: Simple connection (let MongoDB handle SSL automatically)
try:
    # Set SSL context for production
    import ssl
    import os
    if not os.environ.get('PYTHONHTTPSVERIFY', '1') == '0':
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    else:
        ssl_context = None
    
    mongoengine.connect(
        db=config('MONGODB_NAME'),
        host=config('MONGODB_URI'),
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        maxPoolSize=10,
        retryWrites=True,
    )
    print("✅ MongoDB connected successfully (simple connection)")
    mongodb_connected = True
except Exception as e:
    connection_errors.append(f"Simple connection failed: {e}")
    print(f"❌ MongoDB simple connection failed: {e}")

# Strategy 2: Direct PyMongo connection
if not mongodb_connected:
    try:
        from pymongo import MongoClient
        
        # Create direct PyMongo client
        client = MongoClient(
            config('MONGODB_URI'),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxPoolSize=10,
            retryWrites=True,
        )
        
        # Test connection
        client.admin.command('ping')
        
        # Connect MongoEngine to the existing client
        mongoengine.connect(
            db=config('MONGODB_NAME'),
            _connect=False,  # Don't create new connection
            mongo_client=client
        )
        
        print("✅ MongoDB connected successfully (direct PyMongo)")
        mongodb_connected = True
    except Exception as e:
        connection_errors.append(f"Direct PyMongo connection failed: {e}")
        print(f"❌ MongoDB direct PyMongo connection failed: {e}")

# Strategy 3: Atlas-specific TLS settings
if not mongodb_connected:
    try:
        mongoengine.connect(
            db=config('MONGODB_NAME'),
            host=config('MONGODB_URI'),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxPoolSize=10,
            retryWrites=True,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
        )
        print("✅ MongoDB connected successfully (Atlas TLS)")
        mongodb_connected = True
    except Exception as e:
        connection_errors.append(f"Atlas TLS connection failed: {e}")
        print(f"❌ MongoDB Atlas TLS connection failed: {e}")

# Strategy 4: Minimal settings
if not mongodb_connected:
    try:
        mongoengine.connect(
            db=config('MONGODB_NAME'),
            host=config('MONGODB_URI'),
            serverSelectionTimeoutMS=60000,
            connectTimeoutMS=60000,
            socketTimeoutMS=60000,
            maxPoolSize=5,
            retryWrites=False,
        )
        print("✅ MongoDB connected successfully (minimal settings)")
        mongodb_connected = True
    except Exception as e:
        connection_errors.append(f"Minimal connection failed: {e}")
        print(f"❌ MongoDB minimal connection failed: {e}")

if not mongodb_connected:
    print("❌ All MongoDB connection strategies failed!")
    print("Connection errors:", connection_errors)
    # Don't raise error in production to allow app to start
    # raise Exception("MongoDB connection failed")

# -----------------------------
# Default Django DB (for admin/auth)
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------
# Password validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static & Media files
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / config('MEDIA_ROOT', default='media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# -----------------------------
# CORS
# -----------------------------
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS').split(',')
    CORS_ALLOW_CREDENTIALS = True

# -----------------------------
# Django REST Framework
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# -----------------------------
# API Documentation
# -----------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Disaster Response API',
    'DESCRIPTION': 'API for reporting and managing disaster incidents',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
}

# -----------------------------
# Upload limits
# -----------------------------
FILE_UPLOAD_MAX_MEMORY_SIZE = config('MAX_UPLOAD_SIZE', default=10485760, cast=int)
DATA_UPLOAD_MAX_MEMORY_SIZE = config('MAX_UPLOAD_SIZE', default=10485760, cast=int)

# -----------------------------
# Production security
# -----------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# -----------------------------
# Default primary key
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
