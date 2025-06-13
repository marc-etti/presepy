from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from app.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    users = db.session.query(User).all()
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/delete_account', methods=['POST'])
@login_required
@role_required('admin')
def delete_account():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.delete()
        flash(f"L'utente {user.username} è stato eliminato.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/deactivate', methods=('POST',))
@login_required
@role_required('admin')
def deactivate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = False
        user.update()
        flash(f"L'utente {user.username} è stato disattivato.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/activate', methods=('POST',))
@login_required
def activate():
    user_id = request.form['user_id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_active = True
        user.update()
        flash(f"L'utente {user.username} è stato attivato.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/change_role', methods=('POST',))
@login_required
@role_required('admin')
def change_role():
    user_id = request.form['user_id']
    new_role = request.form['new_role']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.role = new_role
        user.update()
        flash(f"Il ruolo di {user.username} è stato cambiato in {new_role}.", 'success')
    else:
        flash('Utente non trovato.', 'error')
    return redirect(url_for('admin.dashboard'))