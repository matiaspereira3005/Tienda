import mysql.connector
import click#ejecutar comandos en terminal, para crear tablas y relaciones
from flask import current_app,g
#mantiene la aplicacion en ejecucion, (g) le podemos asignar distintas variables para 
#acceder a ellas en otras partes de la app, se usara para almacenar el usuario
from flask.cli import with_appcontext #para ejecutar el script de la bd
#se puede acceder a las variables de la aplicacion como el host, entre otros
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
        #ejecuta funciones entregadas como argumentos
        #cuando estemos terminando la ejecucion del aglun metodo llamado
        # o de algun endpoint creado, se devuelven los datos y se ejecuta close_db
    app.cli.add_command(init_db_command)