"""
AI大模型服务 - OpenAI兼容API
"""
import requests
import json
from app.config import AI_BASE_URL, AI_API_KEY, AI_MODEL, AI_TIMEOUT, AI_MAX_TOKENS

class AIService:
    """AI大模型服务类（OpenAI兼容API）"""
    
    def __init__(self):
        self.base_url = AI_BASE_URL
        self.api_key = AI_API_KEY
        self.model = AI_MODEL
        self.timeout = AI_TIMEOUT
        self.max_tokens = AI_MAX_TOKENS
    
    def chat(self, messages, system_prompt=None):
        """
        发送聊天请求到AI大模型
        :param messages: 消息列表 [{"role": "user", "content": "..."}]
        :param system_prompt: 系统提示
        :return: AI回复
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 构建请求
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        
        payload["messages"].extend(messages)
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            return "抱歉，我现在无法回答您的问题。"
        except requests.exceptions.RequestException as e:
            print(f"AI服务请求错误: {e}")
            return "抱歉，我现在无法回答您的问题，请稍后再试。"
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return "抱歉，响应格式错误。"
    
    def chat_stream(self, messages, system_prompt=None):
        """
        发送聊天请求到AI大模型（流式）
        :param messages: 消息列表 [{"role": "user", "content": "..."}]
        :param system_prompt: 系统提示
        :return: 生成器，yield AI回复的每个片段
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 构建请求
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": self.max_tokens,
            "stream": True
        }
        
        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        
        payload["messages"].extend(messages)
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    # 跳过 [DONE] 消息
                    if line.decode('utf-8').strip() == 'data: [DONE]':
                        break
                    
                    # 解析SSE数据
                    try:
                        data = json.loads(line.decode('utf-8').replace('data: ', ''))
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as e:
            print(f"AI服务流式请求错误: {e}")
            return
        except Exception as e:
            print(f"流式处理错误: {e}")
            return
    
    def generate(self, prompt, system_prompt=None):
        """
        生成文本
        :param prompt: 提示
        :param system_prompt: 系统提示
        :return: 生成的文本
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, system_prompt)
    
    def check_health(self):
        """检查AI服务是否可用"""
        try:
            url = f"{self.base_url}/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code == 200
        except:
            return False

# 全局实例
ai_service = AIService()