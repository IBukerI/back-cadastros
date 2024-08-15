from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config') 
    db.init_app(app)
    

    CORS(app, origins=['http://localhost:4200'])

    with app.app_context():
        # Import blueprints
        from app.routes.user_routes import user_routes
        from app.routes.auth_routes import auth_routes
        from app.routes.minha_empresa_routes import minha_empresa_routes
        from app.routes.clientes_routes import clientes_routes

        # Register blueprints
        app.register_blueprint(user_routes, url_prefix='/user')
        app.register_blueprint(auth_routes, url_prefix='/auth')
        app.register_blueprint(minha_empresa_routes, url_prefix='/empresa')
        app.register_blueprint(clientes_routes, url_prefix='/cliente')

    return app
