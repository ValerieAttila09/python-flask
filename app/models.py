import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app

def read_users():
    users_file = current_app.config['USERS_FILE']
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            json.dump({"users": []}, f)
        return {"users": []}
    with open(users_file, 'r') as f:
        return json.load(f)

def write_users(data):
    users_file = current_app.config['USERS_FILE']
    with open(users_file, 'w') as f:
        json.dump(data, f, indent=2)

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
        users_data = read_users()
        user_data = next((u for u in users_data['users'] if u['username'] == self.username), None)
        if user_data:
            user_data['password_hash'] = self.password_hash
        else:
            users_data['users'].append({'username': self.username, 'password_hash': self.password_hash})
        write_users(users_data)

    @staticmethod
    def get(user_id):
        users_data = read_users()
        user_data = next((u for u in users_data['users'] if u['username'] == user_id), None)
        if user_data:
            return User(user_data['username'], password_hash=user_data['password_hash'])
        return None
