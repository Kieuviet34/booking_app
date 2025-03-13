from flask_sqlalchemy import SQLAlchemy

class DBHandler:
    def __init__(self, db_instance):
        self.db = db_instance

    def init_app(self, app):
        self.db.init_app(app)

    def get_db(self):
        return self.db
