"""
简化版流式聊天服务 - 直接使用 requests 调用通义 API（不使用 LangChain）
支持 SSE 流式响应，同时在响应完成后保存消息到数据库
"""
import json
import requests
from typing import Generator, List, Dict, Any
from app.config import AI_BASE_URL, AI_API_KEY, AI_MODEL, AI_TIMEOUT, AI_MAX_TOKENS


class SimpleStreamingService:
    """简化版流式聊天服务 - 直接调用通义 API"""
    
    def __init__(self):
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
    
    def build_messages(self, history: List[Dict], system_prompt: str = None) -> List[Dict]:
        """构建消息列表，包含系统提示和历史消息"""
        messages = []
        
        # 添加系统提示
        prompt = system_prompt or self.system_prompt
        messages.append({"role": "system", "content": prompt})
        
        # 添加历史消息
        for msg in history:
            if msg.get('role') == 'user':
                messages.append({"role": "user", "content": msg['content']})
            elif msg.get('role') == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
        
        return messages
    
    def chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        """非流式聊天请求"""
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        all_messages = self.build_messages(messages, system_prompt)
        
        payload = {
            "model": self.model,
            "messages": all_messages,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        try:
            print(f"[DEBUG] SimpleStreaming: 发送非流式请求, 消息数={len(all_messages)}")
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            return "抱歉，我现在无法回答您的问题。"
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] SimpleStreaming 非流式请求错误: {e}")
            return "抱歉，AI服务暂时不可用，请稍后再试。"
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON解析错误: {e}")
            return "抱歉，响应格式错误。"
        except Exception as e:
            print(f"[ERROR] 未知错误: {e}")
            return "抱歉，发生未知错误。"
    
    def chat_stream(self, messages: List[Dict], system_prompt: str = None) -> Generator[str, None, str]:
        """
        流式聊天请求 - 生成器，每次 yield 一个内容片段
        最后一个 yield 返回完整响应字符串
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        all_messages = self.build_messages(messages, system_prompt)
        
        payload = {
            "model": self.model,
            "messages": all_messages,
            "max_tokens": self.max_tokens,
            "stream": True
        }
        
        print(f"[DEBUG] SimpleStreaming: 发送流式请求, url={url}, model={self.model}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            full_response = []
            
            # 逐行处理 SSE 响应
            for line in response.iter_lines():
                if line:
                    try:
                        decoded_line = line.decode('utf-8')
                        
                        # 跳过空行
                        if not decoded_line.strip():
                            continue
                        
                        # 跳过 [DONE] 消息
                        if decoded_line.strip() == 'data: [DONE]':
                            break
                        
                        # 解析 SSE 数据行
                        if decoded_line.startswith('data: '):
                            data_str = decoded_line[6:]  # 去掉 "data: " 前缀
                            
                            try:
                                data = json.loads(data_str)
                                
                                # 检查是否有错误
                                if 'error' in data:
                                    print(f"[ERROR] API返回错误: {data['error']}")
                                    yield "", "抱歉，AI服务遇到问题。"
                                    return
                                
                                # 提取内容片段
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    
                                    if content:
                                        full_response.append(content)
                                        # 每次 yield 返回 (片段, 累计内容)
                                        yield content, ''.join(full_response)
                                        
                            except json.JSONDecodeError:
                                # 某些行可能不是有效的 JSON，跳过
                                continue
                                
                    except UnicodeDecodeError:
                        continue
            
            print(f"[DEBUG] SimpleStreaming: 流式结束, 总长度={len(''.join(full_response))}")
            
            # 流结束后返回完整内容（最后一个 yield）
            yield "", ''.join(full_response)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] SimpleStreaming 流式请求错误: {e}")
            yield "", "抱歉，AI服务暂时不可用，请稍后再试。"
        except Exception as e:
            print(f"[ERROR] SimpleStreaming 流式处理错误: {e}")
            import traceback
            traceback.print_exc()
            yield "", "抱歉，发生未知错误。"
    
    def check_health(self) -> bool:
        """检查服务健康状态"""
        try:
            url = f"{self.base_url}/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code == 200
        except:
            return False


# 全局实例
simple_streaming_service = SimpleStreamingService()