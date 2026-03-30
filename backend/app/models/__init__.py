"""
数据库模型初始化
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.session import Conversation
from app.models.message import Message
from app.models.warning import Warning

__all__ = ['db', 'User', 'Conversation', 'Message', 'Warning']