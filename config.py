import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://%2Ftmp%2Fmongodb%2Fmongodb.sock/my-flask-app'
