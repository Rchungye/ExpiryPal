from src import db
from src.models.User import User
from src.models.Item import Item


class Notification(db.Model):
    __tablename__ = "notification"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = True)
    date = db.Column(db.Date(), nullable = True)
    message = db.Column(db.String(500), nullable = True)

    def as_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "code": self.code,
            "date": self.date,
            "message": self.message
        }