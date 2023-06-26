import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash
from web.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        correo      = request.form['correo']
        password    = request.form['password']
        nombre      = request.form['nombre']
        apellido    = request.form['apellido']
        db, c = get_db()
        error = None
        c.execute(
            'select id_user from user where correo = %s', (correo,)
        )
        if not correo:
            error = 'correo es requerido'
        if not password:
            error = 'Password requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(correo)
        
        if error is None:
            c.execute(
                'insert into user (correo, password,nombre, apellido,id_perfil) values (%s,%s,%s,%s,2)',
                (correo, generate_password_hash(password),nombre,apellido,)
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id_user, correo, password from user where correo = %s', (correo,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o password invalido'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o password invalido'
        
        if error is None:
            session.clear()
            session['id_user'] = user['id_user']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    id_user = session.get('id_user')

    if id_user is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM user WHERE id_user = %s', (id_user,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        
        return view(**kwargs)
    
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))