"""
消息模型
"""
from datetime import datetime
from app.models import db

class Message(db.Model):
    """聊天消息模型"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user/assistant/system
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    conversation = db.relationship('Conversation', back_populates='messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversationId': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Message {self.id} - {self.role}>'