import os
from urllib.parse import urljoin, urlparse

import peewee
from admin import admin
from api.api import api
from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from models import User
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['ERROR_404_HELP'] = False
csrf = CSRFProtect(app)
login = LoginManager(app)
login.login_view = '/login'
app.config.from_pyfile('dev_config.py', silent=True)
admin.init_app(app)
# api.init_app(app)
app.register_blueprint(api)
csrf.exempt(api)


@login.user_loader
def load_user(id):
    return User.get_or_none(User.id == id)


@app.errorhandler(400)
def bad_request(e):
    return jsonify(message=str(e)), 400


@app.errorhandler(peewee.DataError)
def data_error(e):
    return jsonify(message=str(e)), 400


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(message="page not found"), 404


@app.errorhandler(peewee.DoesNotExist)
def record_does_not_exist(e):
    return page_not_found(e)


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(message=str(e)), 405


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(message=str(e)), 500


@app.errorhandler(peewee.IntegrityError)
def integrity_error(e):
    return jsonify(message=str(e)), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    class LoginForm(FlaskForm):
        username = StringField('username', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        remember_me = BooleanField('remember_me')

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalide username or password')
            return render_template('login.html', title='Sign in', form=form)
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully')
        next_page = request.args.get('next')

        def is_safe_url(target):
            ref_url = urlparse(request.host_url)
            test_url = urlparse(urljoin(request.host_url, target))
            return test_url.scheme in (
                'http', 'https') and ref_url.netloc == test_url.netloc

        if not is_safe_url(next_page):
            return abort(400)
        return redirect(next_page or url_for('index'))

    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return index()


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
