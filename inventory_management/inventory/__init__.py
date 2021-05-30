from flask import Blueprint

inventory = Blueprint('inventory_bp', __name__, template_folder='templates')

from . import views
