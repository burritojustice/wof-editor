from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from editor.config import config


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_host=1, x_proto=1)

    Bootstrap(app)
    login_manager.init_app(app)

    from .exportify import exportify_bp
    app.register_blueprint(exportify_bp)

    from .place import place_bp
    app.register_blueprint(place_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
