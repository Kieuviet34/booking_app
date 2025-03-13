from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models để đăng ký với SQLAlchemy
    from app.models import user, staff, patient, appointment, finance

    # Đăng ký blueprint
    from app.views.main import main_bp
    from app.views.auth import auth_bp
    from app.views.staff import staff_bp
    from app.views.patient import patient_bp
    from app.views.appointment import appointment_bp
    from app.views.finance import finance_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    app.register_blueprint(finance_bp, url_prefix='/finance')

    return app
