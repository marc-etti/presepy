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

        if error is None:
            login_user(user)
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

@auth_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Non hai i permessi per accedere a questa pagina.', 'error')
        return redirect(url_for('dmx.index'))
    return render_template('auth/admin.html', users=User.query.all())

@auth_bp.route('/delete_account', methods=('POST',))
@login_required
def delete_account():
    user = db.session.get(User, request.form['user_id'])
    if user:
        user.delete()
        logout_user()
        flash('Il tuo account è stato eliminato.', 'success')
    else:
        flash("Errore durante l'eliminazione dell'account.", 'error')
    return redirect(url_for('dmx.index'))

@auth_bp.route('/deactivate', methods=('POST',))
@login_required
def deactivate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = False
        user.update()
        flash(f"L'utente {user.username} è stato disattivato.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('auth.admin'))

@auth_bp.route('/activate', methods=('POST',))
@login_required
def activate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = True
        user.update()
        flash(f"L'utente {user.username} è stato riattivato.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('auth.admin'))