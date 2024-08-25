# config.py

import os

class Config:
    UPLOAD_FOLDER = 'uploads/'
    SECRET_KEY = os.urandom(24)
