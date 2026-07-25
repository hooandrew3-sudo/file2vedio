from flask import render_template, Blueprint

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET'])
def index():
    """
    Serve the main web interface
    """
    return render_template('index.html')