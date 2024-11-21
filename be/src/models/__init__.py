from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

from .fridge import Fridge
from .camera import Camera
from .item import Item
from .notification import Notification
from .fridge_user import fridge_user
from .user import User