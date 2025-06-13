from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username è obbligatorio.'
        elif not password:
            error = 'Password è obbligatoria.'

        if error is None:
            if User.query.filter_by(username=username).first() is not None:
                error = f"Il nome {username} è già in uso."
            else:
                new_user = User(username=username, password=password)
                new_user.add()
                flash(f"Registrazione completata per {username}.", 'success')
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_page = request.args.get('next')
        error = None

        if not username:
            error = 'Username è obbligatorio.'
        elif not password:
            error = 'Password è obbligatoria.'

        if error is None:
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = 'Username non trovato.'
            elif not user.check_password(password):
                error = 'Password errata.'
            elif not user.is_active:
                error = 'Il tuo account è stato disattivato. Contatta l\'amministratore.'

        if error is None:
            login_user(user)
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dmx.index'))

        flash(error)

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dmx.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)