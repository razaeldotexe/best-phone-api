from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class DeviceCache(db.Model):
    __tablename__ = 'device_cache'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    data_json = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def data(self):
        return json.loads(self.data_json)
    
    @data.setter
    def data(self, value):
        self.data_json = json.dumps(value)

class CacheMetadata(db.Model):
    __tablename__ = 'cache_metadata'
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    device_count = db.Column(db.Integer, default=0)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
