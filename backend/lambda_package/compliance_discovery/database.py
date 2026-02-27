"""Database models and session persistence."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class SessionModel(db.Model):
    """Persistent session storage."""
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(100), primary_key=True)
    customer_name = db.Column(db.String(200))
    analyst_name = db.Column(db.String(200))
    frameworks = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), default='active')
    responses = db.Column(db.Text)  # JSON object
    evidence = db.Column(db.Text)  # JSON object
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'analyst_name': self.analyst_name,
            'frameworks': json.loads(self.frameworks) if self.frameworks else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'responses': json.loads(self.responses) if self.responses else {},
            'evidence': json.loads(self.evidence) if self.evidence else {}
        }
    
    @staticmethod
    def from_dict(data):
        """Create from dictionary."""
        return SessionModel(
            id=data['id'],
            customer_name=data.get('customer_name', ''),
            analyst_name=data.get('analyst_name', ''),
            frameworks=json.dumps(data.get('frameworks', [])),
            status=data.get('status', 'active'),
            responses=json.dumps(data.get('responses', {})),
            evidence=json.dumps(data.get('evidence', {}))
        )
