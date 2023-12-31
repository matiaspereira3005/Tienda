import os
from flask import Flask, render_template,Config



APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    app.config.from_mapping(
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )

    from . import db

    db.init_app(app)
    
    from . import main
    from . import auth
    from . import perfil


    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(perfil.bp)



    @app.route('/')
    def index():
        return render_template('public/index.html')

    return app


