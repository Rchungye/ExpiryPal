import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_CONN") ##### DATABASE CONNECTION SETTING #####
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "envConfig": DevelopmentConfig,
}