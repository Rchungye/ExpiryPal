import os
import cloudinary

class Config:
    UPLOAD_FOLDER = 'uploads'
    RESULT_FOLDER = 'results'
    SECRET_KEY = os.urandom(24)

    # Cloudinary configuration
    CLOUD_NAME = "dqwutjyjh"
    API_KEY = "132533594763411"
    API_SECRET = "cW4iHQs41fcqnnOFGSyDKVQJel8"

cloudinary.config( 
    cloud_name=Config.CLOUD_NAME,
    api_key=Config.API_KEY,
    api_secret=Config.API_SECRET,
    secure=True
)
