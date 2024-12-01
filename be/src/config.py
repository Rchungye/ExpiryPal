import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    # DEV
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_CONN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "envConfig": DevelopmentConfig,
}
