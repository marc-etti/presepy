from flask import Blueprint, render_template, request

from app.auth import login_required

from sqlalchemy.orm import joinedload
from app.models import Device


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dmx_management')
@login_required
def dmx_management():
    return render_template('dmx_management.html')

@main_bp.route('/audio_management')
def audio_management():
    return render_template('audio_management.html')

@main_bp.route('/light_management')
def light_management():
    return render_template('light_management.html')

@main_bp.route('/devices_management/', methods=['GET', 'POST'])
def devices_management():
    devices = (
        Device.query
        .order_by(Device.id)
        .options(joinedload(Device.channels))
        .all()
    )
    return render_template('devices_management.html', devices=devices)