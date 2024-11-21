from flask import Flask
from models import db, ma
from routes.user_routes import user_routes 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/expirypal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

# Registra el Blueprint
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(debug=True)
