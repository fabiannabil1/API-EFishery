from .auth_routes import auth_bp
from .barang_routes import barang_bp
from .penawaran_routes import penawaran_bp
from .welcome import welcome_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(barang_bp)
    app.register_blueprint(penawaran_bp)
    app.register_blueprint(welcome_bp)
