import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or b"\xb0\xb3\n\xe1\xeep'\xdc\x9a\x1bm\xa4\xce\x81\xd5\x9fW^\xd0h"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or b'\x1c\x7f~\xe6\xb5<P3,9\x80\x15nXQEvK\x11%\xabF\x17\x8fc\xdc@2\x91\xe6'
    JWT_ERROR_MESSAGE_KEY = "error"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"