"""
预警模型
"""
from datetime import datetime
from app.models import db

class Warning(db.Model):
    """心理危机预警模型"""
    __tablename__ = 'warnings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    warning_type = db.Column(db.String(50), nullable=False)  # 自杀/抑郁/焦虑
    content = db.Column(db.Text, nullable=False)  # 触发预警的内容
    session_id = db.Column(db.String(64), nullable=True)
    is_dealt = db.Column(db.Boolean, default=False)  # 是否已处理
    dealt_by = db.Column(db.Integer, nullable=True)  # 处理人
    dealt_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', back_populates='warnings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'type': self.warning_type,
            'content': self.content,
            'sessionId': self.session_id,
            'isDealt': self.is_dealt,
            'warningTime': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Warning {self.id} - {self.warning_type}>'