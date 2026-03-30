"""
心理危机预警服务 - AI大模型分析
"""
import json
from datetime import datetime
from app.config import WARNING_THRESHOLD_SCORE

class WarningService:
    """基于AI的预警服务"""
    
    def __init__(self):
        self.threshold = WARNING_THRESHOLD_SCORE
        self.system_prompt = """你是一个专业的心理健康预警系统。请分析用户对话内容，评估其心理状态风险。

评估维度：
1. 自杀风险：包括自杀念头、想死、结束生命等
2. 抑郁倾向：包括绝望、无助、持续情绪低落等
3. 焦虑状态：包括过度担忧、恐惧、失眠等
4. 其他心理危机信号

请以JSON格式返回分析结果：
{
    "risk_level": "high/medium/low",  // 风险等级：高/中/低
    "risk_type": "自杀/抑郁/焦虑/综合",  // 主要风险类型
    "risk_score": 0.0-1.0,  // 风险分数
    "warning_message": "简要描述预警原因",
    "need_attention": true/false  // 是否需要关注
}

注意：如果用户没有明显的心理危机信号，请返回低风险。"""
    
    def analyze_conversation(self, messages, user_id, session_id=None):
        """
        使用AI分析对话内容，判断是否触发预警
        :param messages: 消息列表 [{"role": "user/assistant", "content": "..."}]
        :param user_id: 用户ID
        :param session_id: 会话ID
        :return: 预警信息dict或None
        """
        from app.services.ai_service import ai_service
        
        # 构建分析提示
        conversation_text = self._build_conversation_text(messages)
        
        analysis_prompt = f"""请分析以下对话内容，评估用户的心理状态：

{conversation_text}

请返回JSON格式的分析结果。"""
        
        try:
            result = ai_service.chat(
                messages=[{"role": "user", "content": analysis_prompt}],
                system_prompt=self.system_prompt
            )
            
            # 尝试解析JSON结果
            warning_info = self._parse_analysis_result(result, user_id, session_id)
            return warning_info
            
        except Exception as e:
            print(f"预警分析错误: {e}")
            return None
    
    def analyze_message(self, message, user_id, session_id=None):
        """
        分析单条消息（结合上下文）
        :param message: 消息内容
        :param user_id: 用户ID
        :param session_id: 会话ID
        :return: 预警信息dict或None
        """
        # 单条消息分析较少触发预警，主要是上下文分析
        return None
    
    def _build_conversation_text(self, messages):
        """构建对话文本用于分析"""
        lines = []
        for msg in messages[-10:]:  # 取最近10条消息
            role = "用户" if msg.get('role') == 'user' else "AI助手"
            content = msg.get('content', '')
            lines.append(f"{role}: {content}")
        return "\n".join(lines)
    
    def _parse_analysis_result(self, result, user_id, session_id):
        """解析AI分析结果"""
        try:
            # 尝试提取JSON
            import re
            json_match = re.search(r'\{[^{}]*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(result)
            
            risk_score = data.get('risk_score', 0)
            need_attention = data.get('need_attention', False)
            
            if risk_score >= self.threshold or need_attention:
                return {
                    'type': data.get('risk_type', '综合'),
                    'content': data.get('warning_message', result[:200]),
                    'user_id': user_id,
                    'session_id': session_id,
                    'risk_level': data.get('risk_level', 'medium'),
                    'risk_score': risk_score,
                    'created_at': datetime.utcnow()
                }
            return None
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"解析预警结果失败: {e}")
            # 如果解析失败，使用简单规则作为后备
            return self._simple_fallback_check(result, user_id, session_id)
    
    def _simple_fallback_check(self, result, user_id, session_id):
        """简单后备检查"""
        high_risk_keywords = ['自杀', '想死', '结束生命', '严重', '极高风险']
        
        for keyword in high_risk_keywords:
            if keyword in result:
                return {
                    'type': '综合',
                    'content': f'AI分析检测到高风险信号：{result[:100]}',
                    'user_id': user_id,
                    'session_id': session_id,
                    'risk_level': 'high',
                    'risk_score': 0.8,
                    'created_at': datetime.utcnow()
                }
        return None
    
    def get_risk_level(self, risk_level):
        """
        获取风险等级描述
        :param risk_level: 风险等级
        :return: 描述文本
        """
        levels = {
            'high': '极高风险',
            'medium': '中等风险',
            'low': '低风险'
        }
        return levels.get(risk_level, '未知')

# 全局实例
warning_service = WarningService()