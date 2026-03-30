"""
聊天历史服务 - 管理聊天消息的数据库持久化
支持消息保存、历史加载、上下文构建
"""
from typing import List, Optional, Dict
from datetime import datetime
from app.models import db
from app.models.message import Message
from app.models.session import Conversation


class ChatHistoryService:
    """聊天历史管理服务 - 负责消息的数据库操作"""
    
    def save_user_message(self, conversation_id: int, content: str) -> Message:
        """
        保存用户消息到数据库
        
        Args:
            conversation_id: 会话 ID
            content: 消息内容
            
        Returns:
            保存的消息对象
        """
        try:
            user_msg = Message(
                conversation_id=conversation_id,
                role='user',
                content=content
            )
            db.session.add(user_msg)
            
            # 更新会话时间
            conversation = Conversation.query.get(conversation_id)
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            db.session.commit()
            return user_msg
        except Exception as e:
            db.session.rollback()
            print(f"保存用户消息失败: {e}")
            raise
    
    def save_assistant_message(self, conversation_id: int, content: str) -> Message:
        """
        保存 AI 回复消息到数据库
        
        Args:
            conversation_id: 会话 ID
            content: 消息内容
            
        Returns:
            保存的消息对象
        """
        try:
            ai_msg = Message(
                conversation_id=conversation_id,
                role='assistant',
                content=content
            )
            db.session.add(ai_msg)
            db.session.commit()
            return ai_msg
        except Exception as e:
            db.session.rollback()
            print(f"保存 AI 消息失败: {e}")
            raise
    
    def get_conversation_history(self, conversation_id: int) -> List[Dict]:
        """
        获取会话的所有历史消息
        
        Args:
            conversation_id: 会话 ID
            
        Returns:
            消息列表 [{"role": "user/assistant", "content": "..."}]
        """
        try:
            messages = Message.query.filter_by(
                conversation_id=conversation_id
            ).order_by(Message.created_at).all()
            
            return [
                {'role': msg.role, 'content': msg.content}
                for msg in messages
            ]
        except Exception as e:
            print(f"获取历史消息失败: {e}")
            return []
    
    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        """
        获取会话的所有消息对象
        
        Args:
            conversation_id: 会话 ID
            
        Returns:
            Message 对象列表
        """
        try:
            return Message.query.filter_by(
                conversation_id=conversation_id
            ).order_by(Message.created_at).all()
        except Exception as e:
            print(f"获取消息对象失败: {e}")
            return []
    
    def delete_conversation_messages(self, conversation_id: int) -> bool:
        """
        删除会话的所有消息
        
        Args:
            conversation_id: 会话 ID
            
        Returns:
            是否成功
        """
        try:
            Message.query.filter_by(conversation_id=conversation_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"删除消息失败: {e}")
            return False
    
    def get_message_count(self, conversation_id: int) -> int:
        """
        获取会话的消息数量
        
        Args:
            conversation_id: 会话 ID
            
        Returns:
            消息数量
        """
        try:
            return Message.query.filter_by(conversation_id=conversation_id).count()
        except Exception as e:
            print(f"获取消息数量失败: {e}")
            return 0
    
    def build_context_for_ai(self, conversation_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        构建发送给 AI 的上下文（从数据库加载）
        
        Args:
            conversation_id: 会话 ID
            limit: 限制返回的消息数量（最近的 N 条）
            
        Returns:
            消息列表
        """
        try:
            query = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at)
            
            if limit:
                query = query.limit(limit)
            
            messages = query.all()
            return [
                {'role': msg.role, 'content': msg.content}
                for msg in messages
            ]
        except Exception as e:
            print(f"构建 AI 上下文失败: {e}")
            return []
    
    def get_last_n_messages(self, conversation_id: int, n: int = 10) -> List[Dict]:
        """
        获取最近 N 条消息
        
        Args:
            conversation_id: 会话 ID
            n: 消息数量
            
        Returns:
            消息列表
        """
        try:
            messages = Message.query.filter_by(
                conversation_id=conversation_id
            ).order_by(Message.created_at.desc()).limit(n).all()
            
            # 反转以获得正确的顺序
            return [
                {'role': msg.role, 'content': msg.content}
                for msg in reversed(messages)
            ]
        except Exception as e:
            print(f"获取最近消息失败: {e}")
            return []


# 全局实例
chat_history_service = ChatHistoryService()