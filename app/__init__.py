from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Khởi tạo các extension
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Tạo đối tượng ứng dụng Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Khởi tạo các extension với app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import các model để đăng ký với SQLAlchemy
    from app import models
    
    
    from app.views.main import main_bp
    app.register_blueprint(main_bp)
    from app.views.auth import auth_bp
    from app.views.patient import patient_bp
    from app.views.doctor import doctor_bp
    from app.views.appointment import appointment_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    
    return app
