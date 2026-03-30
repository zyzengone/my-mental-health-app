"""
路由层初始化
"""
from app.routes.user import user_bp
from app.routes.chat import chat_bp
from app.routes.personality import personality_bp

__all__ = ['user_bp', 'chat_bp', 'personality_bp']