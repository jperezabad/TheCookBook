from application.models.user import User
from flask import Blueprint, render_template, request, current_app, redirect,url_for
from flask_login import current_user, login_user, logout_user
from application.forms import LoginForm, RegisterForm
from werkzeug.urls import url_parse

# Blueprint Configuration
users = Blueprint('login', __name__, template_folder="templates", static_folder="static")

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    #POST requests
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.get(email, password)
        if user is None:
            form.password.errors.append('Incorrect password')
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)

    #GET requests
    return render_template('login.html', form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    #POST requests
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.create(username, email, password)
        login_user(user)
        return redirect(url_for("main.home"))

    #GET requests
    return render_template('register.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))