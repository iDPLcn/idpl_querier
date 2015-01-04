'''
Created on 2014.10.26

@author: Jarvis Zhang

Django productive settings for idpl_querier project.

'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from idpl_querier.settings import *

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'NAME': 'idpl',
        'ENGINE': 'mysql.connector.django',
        'USER': 'idpl',
        'PASSWORD': 'idpl@jsi',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

TIME_ZONE = 'Asia/Shanghai'
