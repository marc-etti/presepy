from flask import Blueprint, render_template, request, flash, redirect, url_for

from app.auth import login_required


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