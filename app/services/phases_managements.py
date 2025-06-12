from config import Config

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required

from sqlalchemy.orm import joinedload
from app.models import Device, Channel, Phase, Keyframe
from app.decorators import role_required
from app import db

# Creazione del Blueprint
phases_bp = Blueprint('phases', __name__)

@phases_bp.route('/phases_management/', methods=['GET', 'POST'])
@login_required
def phases_management():
    """
    Restituisce la lista delle fasi.
    """
    phases = Phase.get_phases()
    
    return render_template('phases_management.html', phases=phases)

@phases_bp.route('/active_deactivate_phase/<int:phase_id>', methods=['GET'])
@login_required
def active_deactivate_phase(phase_id):
    """
    Attiva disattiva una fase.
    """
    try:
        phase = Phase.query.filter_by(id=phase_id).first()
        if phase:
            if phase.status == "active":
                phase.deactivate()
                flash(f"Fase {phase.name} attiva", 'success')
            elif phase.status == "deactivated":
                phase.activate()
                flash(f"Fase {phase.name} disattivata", 'success')
            else:
                flash(f"Stato della fase {phase.name} non valido", 'error')
                return redirect(url_for('phases.phases_management'))
        else:
            flash('Fase non trovata', 'error')
    except Exception as e:
        flash(f"Errore durante l'attivazione/disattivazione della fase: {str(e)}", 'error')
    
    return redirect(url_for('phases.phases_management'))

@phases_bp.route('/delete_phase', methods=['POST'])
@login_required
@role_required('admin','expert')
def delete_phase():
    """
    Elimina una fase.
    """
    phase_id = request.form.get('phase_id')
    phase = db.session.query(Phase).filter_by(id=phase_id).first()
    if phase:
        try:
            phase.delete()
            flash(f"Fase {phase.name} eliminata con successo", 'success')
        except Exception as e:
            flash(f"Errore durante l'eliminazione della fase: {str(e)}", 'error')
    else:
        flash('Fase non trovata', 'error')
    return redirect(url_for('phases.phases_management'))

@phases_bp.route('/add_edit_phase_form', methods=['GET', 'POST'])
@phases_bp.route('/add_edit_phase_form/<int:phase_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','expert')
def add_edit_phase_form(phase_id=None):
    """
    Mostra il form per aggiungere o modificare una fase.
    """
    phase = None
    if phase_id:
        phase = Phase.query.filter_by(id=phase_id).first()
        if not phase:
            flash('Fase non trovata', 'error')
            return redirect(url_for('phases.phases_management'))
    
    return render_template('phases_form.html', phase=phase)

@phases_bp.route('/add_edit_phase', methods=['POST'])
@phases_bp.route('/add_edit_phase/<int:phase_id>', methods=['POST'])
@login_required
@role_required('admin','expert')
def add_edit_phase(phase_id=None):
    """
    Aggiunge o modifica una fase.
    """
    try:
        name = request.form.get('name')
        duration = request.form.get('duration')

        if phase_id:
            phase = Phase.query.filter_by(id=phase_id).first()
            if not phase:
                flash('Fase non trovata', 'error')
                return redirect(url_for('phases.phases_management'))
            phase.name = name
            phase.duration = int(duration)
            phase.update()
            flash(f'Fase {name} aggiornata con successo', 'success')
        else:
            phase = Phase()
            phase.name = name
            phase.duration = int(duration)
            phase.status = 'deactivated'  # Default status for new phases
            phase.order = db.session.query(Phase).filter_by(status='active').count() + 1  # Set order based on active phases
            phase.add()
            flash(f'Fase {name} aggiunta con successo', 'success')

    except ValueError as ve:
        flash(f'Errore di validazione: {str(ve)}', 'error')
    except Exception as e:
        flash(f'Errore imprevisto: {str(e)}', 'error')

    return redirect(url_for('phases.phases_management'))

@phases_bp.route('/move_up_down_phase/<int:phase_id>/<direction>', methods=['GET','POST'])
@login_required
def move_up_down_phase(phase_id, direction):
    """
    Cambia l'ordine di una fase.
    """
    phase = Phase.query.filter_by(id=phase_id).first()
    if not phase:
        flash('Fase non trovata', 'error')
        return redirect(url_for('phases.phases_management'))

    try:
        phase.move_up_down(direction)
        flash(f'Fase {phase.name} spostata {"su" if direction == "up" else "giù"}', 'success')

    except ValueError as ve:
        flash(f'{str(ve)}', 'error')

    except Exception as e:
        flash(f'Errore durante l\'aggiornamento dell\'ordine della fase: {str(e)}', 'error')

    return redirect(url_for('phases.phases_management'))