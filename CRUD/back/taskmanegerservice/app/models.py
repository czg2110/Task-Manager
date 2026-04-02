# app/models.py
from datetime import datetime
from .database import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def allowed_statuses(cls):
        return ['pending', 'in-progress', 'completed', 'on-review', 'blocked']