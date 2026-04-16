from .main import main_bp
from .auth import auth_bp
from .fortune import fortune_bp
from .history import history_bp
from .donation import donation_bp
from .share import share_bp

def register_blueprints(app):
    """
    註冊 App 內所有的 Blueprints。
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(fortune_bp, url_prefix='/fortune')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(donation_bp, url_prefix='/donation')
    app.register_blueprint(share_bp, url_prefix='/share')
