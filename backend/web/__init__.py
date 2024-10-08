from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
# None, async_mode='eventlet', cors_allowed_origins="*", message_queue='redis://'

socketio = SocketIO(None, cors_allowed_origins="*",
                    async_mode='gevent', debug=False)
jwt = JWTManager()


def create_app():

    # Initialize flask app
    app = Flask(__name__, static_folder=None)
    CORS(app, supports_credentials=True)
    app.config['SECRET_KEY'] = 'secret!'
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "X-CSRF-TOKEN"
    app.config['JWT_CSRF_IN_COOKIES'] = True
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=90)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    # app.config['JWT_ACCESS_COOKIE_PATH'] = '/'

    socketio.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # from .areas import areas
        from .auth import auth
        from .alarm import alarm
        from .system import system
        # # from . import SocketIO_events
        # # Registering web Blueprints
        app.register_blueprint(auth)
        app.register_blueprint(alarm)
        app.register_blueprint(system)
    return app
