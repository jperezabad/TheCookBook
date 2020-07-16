from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from application.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', description="Email", validators=[DataRequired(message='Introduce your email')])
    password = PasswordField('Password', description="Password", validators=[DataRequired(message='Introduce your password')])
    submit = SubmitField('Sign in')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is None:
            raise ValidationError('Email not registered')

class RegisterForm(FlaskForm):
    username = StringField('Username', description="Username *", validators=[DataRequired(message='Introduce a username')])
    email = StringField('Email', description="Email *", validators=[DataRequired(message='Introduce your email'), Email("This field requires a valid email address")])
    password = PasswordField('Password', description="Password *", validators=[DataRequired(message='Introduce your password')])
    password2 = PasswordField('Repeat Password', description="Repeat password *", 
            validators=[DataRequired(message='Introduce your password'), EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered')


class SearchForm(FlaskForm):
    search = StringField('Search', description="Search...")
    submit = SubmitField("Search")