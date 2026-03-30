"""
服务层初始化
"""
from app.services.ai_service import AIService, ai_service
from app.services.personality_service import PersonalityService, personality_service
from app.services.warning_service import WarningService, warning_service

__all__ = [
    'AIService', 'ai_service',
    'PersonalityService', 'personality_service',
    'WarningService', 'warning_service'
]