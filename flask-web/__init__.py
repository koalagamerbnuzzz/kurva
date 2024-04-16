from .config import app_config
from .models import db
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_caching import Cache


app = Flask(__name__, static_folder='static')
jwt = JWTManager(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

socketio = SocketIO(engineio_logger=True, logger=True,
                    cors_allowed_origins="*",
                    cors_credentials=True)

def create_app(config_name):
    '''CONFIGS'''
    app.config.from_object(app_config[config_name])
    
    '''FLASK_SECURITY'''
    from models import User, Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    '''DB'''
    db.init_app(app)

    '''ROTAS'''
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    '''INICIALIZADOR'''
    socketio.init_app(app)
    return app
