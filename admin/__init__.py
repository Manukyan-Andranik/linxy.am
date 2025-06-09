from flask import Blueprint
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def before_request():
    if not current_user.is_admin():
        return "Unauthorized", 403

from . import views