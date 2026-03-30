"""
MBTI人格分析服务
"""
from app.services.ai_service import ai_service

# MBTI人格类型描述
MBTI_TYPES = {
    'ISTJ': '检查员型 - 实际而务实，注重事实和细节，可靠且有责任感',
    'ISFJ': '保护者型 - 温暖友善，尽责且忠诚，注重实际帮助他人',
    'INFJ': '咨询师型 - 富有洞察力和同情心，追求意义和深度联系',
    'INTJ': '战略家型 - 独立且具有战略思维，追求知识和能力',
    'ISTP': '巧匠型 - 冷静的观察者，擅长解决实际问题',
    'ISFP': '艺术家型 - 温和敏感，注重审美和当下体验',
    'INFP': '治愈者型 - 理想主义且充满同情心，追求真实和自我表达',
    'INTP': '建筑师型 - 逻辑性强，喜欢理论和抽象思考',
    'ESTP': '挑战者型 - 精力充沛，适应性强，注重实际行动',
    'ESFP': '表演者型 - 外向热情，喜欢与他人分享快乐',
    'ENFP': '倡导者型 - 充满热情和创造力，善于激励他人',
    'ENTP': '辩论家型 - 聪明且好奇，喜欢挑战和智力辩论',
    'ESTJ': '监督者型 - 实际且传统，注重效率和秩序',
    'ESFJ': '供给者型 - 温暖友善，喜欢帮助和照顾他人',
    'ENFJ': '教育家型 - 富有魅力且善于交际，喜欢指导和帮助他人成长',
    'ENTJ': '指挥官型 - 果断且自信，天生的领导者'
}

class PersonalityService:
    """人格分析服务"""
    
    def __init__(self):
        self.ai = ai_service
        self.system_prompt = """你是一个专业的MBTI人格分析专家。根据用户的对话内容，分析其人格特征并给出最匹配的MBTI类型。
请仔细分析对话中的以下特征：
1. 外向(E) vs 内向(I)：社交能量来源
2. 感觉(S) vs 直觉(N)：获取信息的方式
3. 思考(T) vs 情感(F)：决策方式
4. 判断(J) vs 感知(P)：生活方式

只输出一个四个字母的MBTI类型（如INTJ、ENFP等），不要有其他解释。"""
    
    def analyze_personality(self, conversation_history):
        """
        根据对话历史分析MBTI人格类型
        :param conversation_history: 对话历史列表
        :return: MBTI类型
        """
        # 构建分析提示
        analysis_prompt = self._build_analysis_prompt(conversation_history)
        
        # 调用AI进行分析
        result = self.ai.chat(
            messages=[{"role": "user", "content": analysis_prompt}],
            system_prompt=self.system_prompt
        )
        
        if result:
            # 提取MBTI类型
            mbti_type = self._extract_mbti_type(result)
            return mbti_type if mbti_type else 'INTJ'  # 默认返回INTJ
        return 'INTJ'
    
    def _build_analysis_prompt(self, conversation_history):
        """构建分析提示"""
        # 提取最近的对话内容进行分析
        recent_messages = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        conversation_text = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('content', '')}"
            for msg in recent_messages
        ])
        
        return f"""请根据以下对话内容，分析说话者的MBTI人格类型。
只输出一个四个字母的MBTI类型（如INTJ、ENFP等），不要有其他解释。

对话内容：
{conversation_text}

MBTI类型："""
    
    def _extract_mbti_type(self, result):
        """从结果中提取MBTI类型"""
        # 尝试匹配16种MBTI类型
        valid_types = list(MBTI_TYPES.keys())
        
        for mbti_type in valid_types:
            if mbti_type in result.upper():
                return mbti_type
        
        # 如果没有精确匹配，尝试提取第一个四个字母的组合
        import re
        match = re.search(r'\b([IENS][TFJP][IENS][TFJP])\b', result.upper())
        if match:
            return match.group(1)
        
        return None
    
    def get_personality_description(self, mbti_type):
        """获取人格类型描述"""
        return MBTI_TYPES.get(mbti_type, '未知人格类型')
    
    def should_analyze(self, message_count):
        """
        判断是否应该进行分析
        :param message_count: 消息数量
        :return: 是否应该分析
        """
        # 通常在对话进行到一定程度后进行分析
        return message_count >= 10

# 全局实例
personality_service = PersonalityService()