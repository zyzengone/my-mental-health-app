"""
用户模型
"""
from datetime import datetime
from app.models import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # 加密存储
    email = db.Column(db.String(120), unique=True, nullable=True)
    personality_type = db.Column(db.String(10), nullable=True)  # MBTI类型
    role = db.Column(db.String(20), default='user')  # user/admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    conversations = db.relationship('Conversation', back_populates='user', cascade='all, delete-orphan')
    warnings = db.relationship('Warning', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'personality_type': self.personality_type,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'