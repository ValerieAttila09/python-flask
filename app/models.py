from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import mongo

class User(UserMixin, object):
    def __init__(self, username, password_hash=None, password=None):
        self.id = username
        self.username = username
        if password_hash:
            self.password_hash = password_hash
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        mongo.db.users.update_one({'username': self.username}, {'$set': {'password_hash': self.password_hash}}, upsert=True)

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({'username': user_id})
        if user_data:
            return User(user_data['username'], password_hash=user_data['password_hash'])
        return None
