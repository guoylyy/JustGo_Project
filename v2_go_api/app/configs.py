# -*- coding: utf-8 -*-

import datetime

class DefaultConfig(object):

    SESSION_COOKIE_PATH='/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = 'Ssession'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(31)

    DEBUG = True
    SECRET_KEY ='\xf1N\xf6\x94a\x0ez\x82\x08\x9aB\xebkh\xc0\x97\xe9\x90\xb3hy\xdb\xed%'
    MD5_RANDOM = 'FSDAFSDSAdasfsadfddDD'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/globit/git/JustGo_Project/v2_go_api/app.db'
    SQLALCHEMY_ECHO = False
    
    UPLOAD_FOLDER = 'uploads'
    START_YEAR = 2014
    START_MONTH = 4
    
    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'
    
    ACCEPT_LANGUAGES = ['en', 'zh']
    
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
    
    VERSION = 'V1'
    PREVIEW_SIZE = 5
    
    SESSION_EXPIRE_DAYS = 7
    
    IMAGE_UPLOAD_URL = '/Users/globit/git/JustGo_Project/go_api/userimages'
    IMAGE_URL = 'file:///Users/globit/git/JustGo_Project/go_api/userimages/'

class TestConfig(object):
    
    SESSION_COOKIE_PATH='/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = 'Ssession'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(31)

    DEBUG = True
    SECRET_KEY ='\xf1N\xf6\x94a\x0ez\x82\x08\x9aB\xebkh\xc0\x97\xe9\x90\xb3hy\xdb\xed%'
    MD5_RANDOM = 'FSDAFSDSAdasfsadfddDD'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/globit/git/JustGo_Project/v2_go_api/app_test.db'
    SQLALCHEMY_ECHO = False
    
    UPLOAD_FOLDER = 'uploads'
    START_YEAR = 2014
    START_MONTH = 4
    
    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'
    
    ACCEPT_LANGUAGES = ['en', 'zh']
    
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'
    
    VERSION = 'V1'
    PREVIEW_SIZE = 5
    
    SESSION_EXPIRE_DAYS = 7
    
    IMAGE_UPLOAD_URL = '/Users/globit/git/JustGo_Project/v2_go_api/userimages_test'
    IMAGE_URL = 'file:///Users/globit/git/JustGo_Project/v2_go_api/userimages_test/'

class ProductionConfig(object):
    SQLALCHEMY_ECHO = False
    DEBUG = False
