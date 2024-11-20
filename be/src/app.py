from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db, ma, User



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/expirypal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 
ma.init_app(app)


with app.app_context():
    db.create_all() 

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'unusedItemsPreference', 'expiryDatePreference')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    unusedItemsPreference = request.json['unusedItemsPreference']
    expiryDatePreference = request.json['expiryDatePreference']

    new_user = User(username, unusedItemsPreference, expiryDatePreference)

    db.session.add(new_user)
    db.session.commit()
    print("User added")
    return user_schema.jsonify(new_user)

if __name__ == "__main__":
    app.run(debug=True)