from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *
from flask_login import UserMixin
from application import login

@login.user_loader
def load_user(id):
    return User.objects(id=id).first()

class User(UserMixin, Document):
    username = StringField()
    email = EmailField()
    password_hash = StringField()
    verified = BooleanField()

    @staticmethod
    def create(username, email, password):
        user = User()
        user.username = username
        user.email = email
        user.password_hash = generate_password_hash(password)
        user.verified = False
        user.save()
        return user

    @staticmethod
    def get(email, password):
        user = User.objects(email=email).first()
        if check_password_hash(user.password_hash, password):
            return user
        else: return None