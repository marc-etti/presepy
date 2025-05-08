from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if User.query.filter_by(username=username).first() is not None:
                error = f"User {username} is already registered."
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not user.check_password(password):
            error = 'Incorrect password.'

        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    return render_template('auth/admin.html', users=User.query.all())

@auth_bp.route('/delete', methods=('POST',))
@login_required
def delete():
    user = User.query.get(current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted.')
    else:
        flash('User not found.')
    return redirect(url_for('main.index'))

@auth_bp.route('/deactivate', methods=('POST',))
@login_required
def deactivate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = False
        db.session.commit()
        flash(f'User {user.username} has been deactivated.')
    else:
        flash('User not found.')
    return redirect(url_for('auth.admin'))

@auth_bp.route('/activate', methods=('POST',))
@login_required
def activate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = True
        db.session.commit()
        flash(f'User {user.username} has been activated.')
    else:
        flash('User not found.')
    return redirect(url_for('auth.admin'))