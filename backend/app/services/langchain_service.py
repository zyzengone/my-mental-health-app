"""
LangChain 服务 - 使用 LangChain 框架进行 AI 对话
支持流式输出、对话历史管理、心理健康咨询师角色设定
"""
import os
import json
import requests
from typing import Optional, Generator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.config import AI_BASE_URL, AI_API_KEY, AI_MODEL, AI_TIMEOUT, AI_MAX_TOKENS


class LangChainService:
    """LangChain AI 服务类 - 提供对话式 AI 能力"""
    
    def __init__(self):
        """初始化 LangChain 服务"""
        self.base_url = AI_BASE_URL
        self.api_key = AI_API_KEY
        self.model = AI_MODEL
        self.timeout = AI_TIMEOUT
        self.max_tokens = AI_MAX_TOKENS
        
        # 心理健康咨询师的系统提示
        self.system_prompt = """你是一个专业、温暖、有同理心的心理健康咨询师。请遵循以下原则：
1. 倾听并理解用户的情感和经历
2. 提供支持和鼓励，帮助用户找到积极的解决方案
3. 不评判、不批评，始终保持耐心和关怀
4. 在用户提到消极情绪或困难时，给予适当的安慰和建议
5. 如果发现用户有自杀倾向或严重心理问题，及时提醒并建议寻求专业帮助"""
    
    def _create_llm(self, streaming: bool = False):
        """创建 LLM 实例"""
        return ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            streaming=streaming,
        )
    
    def chat(self, messages: list, system_prompt: Optional[str] = None) -> str:
        """
        发送聊天请求（非流式）
        
        Args:
            messages: 消息列表 [{"role": "user/assistant", "content": "..."}]
            system_prompt: 系统提示（可选）
            
        Returns:
            AI 回复内容
        """
        try:
            llm = self._create_llm(streaming=False)
            
            # 构建消息
            langchain_messages = []
            
            # 添加系统提示
            prompt = system_prompt or self.system_prompt
            langchain_messages.append(SystemMessage(content=prompt))
            
            # 添加历史消息
            for msg in messages:
                if msg['role'] == 'user':
                    langchain_messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    langchain_messages.append(AIMessage(content=msg['content']))
            
            print(f"[DEBUG] LangChain: 调用非流式接口, 消息数={len(langchain_messages)}")
            
            # 调用 LLM
            response = llm.invoke(langchain_messages)
            print(f"[DEBUG] LangChain: 响应长度={len(response.content) if response.content else 0}")
            return response.content
            
        except Exception as e:
            print(f"[ERROR] LangChain chat 错误: {e}")
            import traceback
            traceback.print_exc()
            return "抱歉，我现在无法回答您的问题，请稍后再试。"
    
    def chat_with_streaming(self, messages: list, system_prompt: Optional[str] = None) -> Generator:
        """
        发送聊天请求并返回流式生成器（使用 requests 直接调用 SSE）
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示
            
        Yields:
            AI 回复的每个片段
        """
        try:
            url = f"{self.base_url}/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # 构建消息
            chat_messages = []
            
            # 添加系统提示
            prompt = system_prompt or self.system_prompt
            chat_messages.append({"role": "system", "content": prompt})
            
            # 添加历史消息
            for msg in messages:
                if msg['role'] == 'user':
                    chat_messages.append({"role": "user", "content": msg['content']})
                elif msg['role'] == 'assistant':
                    chat_messages.append({"role": "assistant", "content": msg['content']})
            
            payload = {
                "model": self.model,
                "messages": chat_messages,
                "max_tokens": self.max_tokens,
                "stream": True
            }
            
            print(f"[DEBUG] LangChain: 调用流式 SSE 接口, 消息数={len(chat_messages)}")
            print(f"[DEBUG] LangChain: url={url}, model={self.model}")
            
            # 使用 requests 直接调用 SSE 流式接口
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            full_response = []
            
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    
                    # 跳过 [DONE] 消息
                    if decoded_line.strip() == 'data: [DONE]':
                        break
                    
                    # 解析 SSE 数据
                    if decoded_line.startswith('data: '):
                        try:
                            data = json.loads(decoded_line[6:])
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    full_response.append(content)
                                    yield content, ''.join(full_response)
                        except json.JSONDecodeError:
                            continue
            
            print(f"[DEBUG] LangChain: 流式结束, 总长度={len(''.join(full_response))}")
            
        except Exception as e:
            print(f"[ERROR] LangChain chat_stream 错误: {e}")
            import traceback
            traceback.print_exc()
            yield "", "抱歉，我现在无法回答您的问题，请稍后再试。"
    
    def build_langchain_messages(self, db_messages: list) -> list:
        """
        将数据库消息转换为 LangChain 消息格式
        
        Args:
            db_messages: 数据库中的消息列表（Message 对象或字典）
            
        Returns:
            LangChain 格式的消息列表
        """
        result = []
        for msg in db_messages:
            if isinstance(msg, dict):
                role = msg.get('role', '')
                content = msg.get('content', '')
            else:
                role = msg.role
                content = msg.content
            
            if role == 'user':
                result.append({'role': 'user', 'content': content})
            elif role == 'assistant':
                result.append({'role': 'assistant', 'content': content})
        
        return result
    
    def check_health(self) -> bool:
        """检查 AI 服务是否可用"""
        try:
            llm = self._create_llm(streaming=False)
            # 发送一个简单的测试消息
            test_messages = [
                SystemMessage(content="请回复'OK'以确认服务正常。"),
                HumanMessage(content="test")
            ]
            response = llm.invoke(test_messages)
            return "OK" in response.content.upper() if response.content else False
        except Exception as e:
            print(f"健康检查失败: {e}")
            return False


# 全局实例
langchain_service = LangChainService()