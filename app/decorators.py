from functools import wraps
from flask import abort, flash, redirect, url_for, render_template, request
from flask_login import current_user

def role_required(*roles):
    """
    Decoratore per verificare se l'utente ha uno dei ruoli specificati.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in roles:
                return f(*args, **kwargs)
            else:
                if current_user.is_authenticated:
                    if request.referrer:
                        flash('Accesso negato: permessi insufficienti.', 'error')
                        return redirect(request.referrer)
                    else:
                        return abort(403)
                else:
                    flash('Accesso negato: devi effettuare il login.', 'error')
                    return redirect(url_for('auth.login', next=request.url))
        return decorated_function
    return decorator