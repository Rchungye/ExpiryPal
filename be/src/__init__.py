import os
from flask import Flask
from src.config import config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
app = Flask(__name__)
enviroment = config["envConfig"]
app.config.from_object(enviroment)
db = SQLAlchemy(app)
Migrate(app, db)
CORS(app, supports_credentials=True)


from src.routes.camera_routes import *
from src.routes.fridge_routes import *
from src.routes.fridgeLog_routes import *
from src.routes.item_routes import *
from src.routes.notificationPreferences_routes import *
from src.routes.user_routes import *

