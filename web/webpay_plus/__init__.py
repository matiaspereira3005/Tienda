from flask import Flask, Blueprint,Config

bp = Blueprint('webpay_plus', __name__)

from webpay_plus import routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from webpay_plus import bp as webpay_plus_bp

    app.register_blueprint(webpay_plus_bp, url_prefix="/webpay-plus")

