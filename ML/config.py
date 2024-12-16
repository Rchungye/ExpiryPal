import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    RESULT_FOLDER = 'results'
    SECRET_KEY = os.urandom(24)
