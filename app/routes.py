from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dmx_management')
def dmx_management():
    return render_template('dmx_management.html')

@main_bp.route('/audio_management')
def audio_management():
    return render_template('audio_management.html')

@main_bp.route('/test')
def test():
    return render_template('test.html')