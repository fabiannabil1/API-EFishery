from routes import register_routes
from .extensions import jwt, cors, swagger
from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    register_routes(app)

    return app
