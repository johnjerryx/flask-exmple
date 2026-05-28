from flask import Flask, redirect, render_template, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_bcrypt import Bcrypt

from models import User
from forms import RegisterForm, LoginForm

from tasks import random_number
from celery.result import AsyncResult

from celery_app import celery


def register_routes(app: Flask, db: SQLAlchemy, bcrypt: Bcrypt):
     
    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')
    
    @app.get('/register')
    def register_get():
        form = RegisterForm()
        return render_template('register.html', form=form)
    
    @app.post('/register')
    def register_post():

        form = RegisterForm()

        if not form.validate_on_submit():
            return render_template('register.html', form=form)

        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = User(username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_login_get'))

    
    @app.get('/login')
    def user_login_get(form: LoginForm = None):
        form = form or LoginForm()
        return render_template('login.html', form=form)
        
    @app.post('/login')
    def user_login_post():
        form = LoginForm()
        if not form.validate_on_submit():
            return user_login_get(form=form)
        
        user = db.session.scalar(select(User).where(User.username == form.username.data))

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        
        form.username.errors.append('Invalid username or password')
        
        return user_login_get(form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/dashboard', methods=['GET'])
    @login_required
    def user_dashboard():
        return render_template('dashboard.html')




    @app.get("/task/generate-random")
    def generate_random_task():
        result = random_number.delay()

        return jsonify({
            "task_id": result.id,
            "state": result.state
        })

    @app.get("/task/result/<task_id>")
    def get_task(task_id):
        result = AsyncResult(task_id, app=celery)

        if result.ready():
            return jsonify({
                "state": result.state,
                "result": result.get()
            })

        return jsonify({
            "state": result.state
        })