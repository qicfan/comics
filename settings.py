# -*- coding:utf-8 -*-
import os.path,logging
from os.path import join
settings_path = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('qicfan', 'qicfan@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'myweb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = '123'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = join(settings_path, 'static/media')

MEDIA_URL = 'http://www.manmanfan.com/media'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '2(i!g*m0%*9wi3$-3c11*q=ju!%is^5u^081h_qumic6%^hd8z'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'myweb.urls'

TEMPLATE_DIRS = (
    join(settings_path, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'myweb',
    'myweb.pet',
    'myweb.comic',
    'myweb.comic_new'
)

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'