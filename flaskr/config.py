from pathlib import Path

basedir = Path(__file__).resolve().parent.parent


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# config_dev.py (Development Configuration)
class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/instance/flaskr.dev.sqlite"


# config_test.py (Test Configuration)
class TestConfig(Config):
    SECRET_KEY = "test"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/instance/flaskr.test.sqlite"


# config_prod.py (Production Configuration)
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/instance/flaskr.prod.sqlite"
