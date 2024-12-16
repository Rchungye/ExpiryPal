from flask import Flask
import os
from config import Config
from models import load_models
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

# Load models
model, clip_model, clip_processor = load_models()

# Register routes
register_routes(app, model, clip_model, clip_processor)

if __name__ == '__main__':
    app.run(debug=True)
