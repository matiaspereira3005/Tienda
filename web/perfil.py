from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from web.auth import login_required
from web.db import get_db

bp = Blueprint('perfil', __name__)

@bp.route('/perfiles', methods=['GET'])
def perfiles():
    db, c = get_db()
    c.execute(
        'SELECT perfil FROM perfil'
        )
    perfiles =  [row[0] for row in c.fetchall()]
    return render_template('auth/register.html', perfiles=perfiles) 
