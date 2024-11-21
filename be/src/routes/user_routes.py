from flask import Blueprint, request
from models import db, User
from models import ma

user_routes = Blueprint('user_routes', __name__)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'unusedItemsPreference', 'expiryDatePreference')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_routes.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    unusedItemsPreference = request.json['unusedItemsPreference']
    expiryDatePreference = request.json['expiryDatePreference']

    new_user = User(username, unusedItemsPreference, expiryDatePreference)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@user_routes.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return {"users": result}, 200
