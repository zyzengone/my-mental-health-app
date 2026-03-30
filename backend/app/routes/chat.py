"""
聊天路由 - 使用简化版流式服务（支持 SSE 实时响应和数据库保存）
不再使用 LangChain，直接使用 requests 调用通义 API
"""
from flask import Blueprint, request, jsonify, Response, current_app
import json
import uuid
import threading
import queue
from datetime import datetime
from app.models import db
from app.models.user import User
from app.models.session import Conversation
from app.models.message import Message
from app.models.warning import Warning
from app.services.simple_streaming_service import simple_streaming_service
from app.services.chat_history_service import chat_history_service
from app.services.warning_service import warning_service

chat_bp = Blueprint('chat', __name__)

# 心理健康咨询师的系统提示
SYSTEM_PROMPT = """你是一个专业、温暖、有同理心的心理健康咨询师。请遵循以下原则：
1. 倾听并理解用户的情感和经历
2. 提供支持和鼓励，帮助用户找到积极的解决方案
3. 不评判、不批评，始终保持耐心和关怀
4. 在用户提到消极情绪或困难时，给予适当的安慰和建议
5. 如果发现用户有自杀倾向或严重心理问题，及时提醒并建议寻求专业帮助"""

# 全局队列用于存储待保存的消息
save_queue = queue.Queue()
save_thread = None
save_thread_running = True


def _process_save_queue(app_instance):
    """后台处理队列，持续保存消息到数据库"""
    global save_thread_running
    while save_thread_running:
        try:
            conversation_id, content = save_queue.get(timeout=1)
            with app_instance.app_context():
                ai_msg = Message(
                    conversation_id=conversation_id,
                    role='assistant',
                    content=content
                )
                db.session.add(ai_msg)
                db.session.commit()
                print(f"[DEBUG] _process_save_queue: AI回复已保存, conversation_id={conversation_id}")
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[ERROR] _process_save_queue: 保存失败 - {e}")


def start_save_thread(app_instance):
    """启动后台保存线程"""
    global save_thread
    if save_thread is None or not save_thread.is_alive():
        save_thread = threading.Thread(target=_process_save_queue, args=(app_instance,), daemon=True)
        save_thread.start()
        print("[DEBUG] 保存线程已启动")


@chat_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """获取用户的所有会话"""
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'})
    
    try:
        user_id = int(user_id)
        conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
        
        return jsonify({
            'code': 200,
            'data': [conv.to_dict() for conv in conversations]
        })
    except ValueError:
        return jsonify({'code': 400, 'message': '无效的用户ID'})


@chat_bp.route('/createSession', methods=['POST'])
def create_session():
    """创建新会话"""
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'})
    
    try:
        user_id = int(user_id)
        
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'})
        
        # 创建新会话
        session_id = str(uuid.uuid4())
        conversation = Conversation(
            session_id=session_id,
            user_id=user_id,
            title='新对话'
        )
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': conversation.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'创建会话失败: {str(e)}'})


@chat_bp.route('/deleteSession', methods=['POST'])
def delete_session():
    """删除会话"""
    session_id = request.args.get('sessionId')
    
    if not session_id:
        return jsonify({'code': 400, 'message': '缺少会话ID'})
    
    try:
        conversation = Conversation.query.filter_by(session_id=session_id).first()
        if conversation:
            db.session.delete(conversation)
            db.session.commit()
            return jsonify({'code': 200, 'data': 1})
        return jsonify({'code': 404, 'message': '会话不存在'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'删除会话失败: {str(e)}'})


@chat_bp.route('/conversationHistory', methods=['GET'])
def get_conversation_history():
    """获取会话历史消息"""
    session_id = request.args.get('sessionId')
    
    if not session_id:
        return jsonify({'code': 400, 'message': '缺少会话ID'})
    
    try:
        print(f"[DEBUG] conversationHistory: 收到请求, session_id={session_id}")
        conversation = Conversation.query.filter_by(session_id=session_id).first()
        if not conversation:
            print(f"[DEBUG] conversationHistory: 会话不存在, session_id={session_id}")
            return jsonify({'code': 404, 'message': '会话不存在'})
        
        print(f"[DEBUG] conversationHistory: conversation.id={conversation.id}")
        
        # 使用聊天历史服务获取消息
        messages = chat_history_service.get_conversation_messages(conversation.id)
        print(f"[DEBUG] conversationHistory: 找到 {len(messages)} 条消息")
        
        return jsonify({
            'code': 200,
            'data': [msg.to_dict() for msg in messages]
        })
    except Exception as e:
        print(f"[ERROR] conversationHistory: {e}")
        return jsonify({'code': 500, 'message': f'获取历史消息失败: {str(e)}'})


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """发送消息并获取AI回复（非流式）"""
    data = request.get_json()
    
    if not data:
        return jsonify({'code': 400, 'message': '请求参数错误'})
    
    session_id = data.get('sessionId')
    user_id = data.get('userId')
    message = data.get('message')
    
    if not session_id or not user_id or not message:
        return jsonify({'code': 400, 'message': '缺少必要参数'})
    
    try:
        user_id = int(user_id)
        conversation = Conversation.query.filter_by(session_id=session_id).first()
        
        if not conversation:
            return jsonify({'code': 404, 'message': '会话不存在'})
        
        # 保存用户消息（使用聊天历史服务）
        user_msg = chat_history_service.save_user_message(conversation.id, message)
        
        # 获取对话历史用于上下文
        history = chat_history_service.get_conversation_history(conversation.id)
        
        # 调用简化的流式服务获取回复（非流式模式）
        response = simple_streaming_service.chat(history, SYSTEM_PROMPT)
        
        # 保存 AI 回复
        ai_msg = chat_history_service.save_assistant_message(conversation.id, response)
        
        # 在后台进行预警分析（每3条消息分析一次）
        from app.config import WARNING_MESSAGE_COUNT
        if len(history) % WARNING_MESSAGE_COUNT == 0:
            warning_info = warning_service.analyze_conversation(history, user_id, session_id)
            if warning_info:
                # 保存预警
                warning = Warning(
                    user_id=warning_info['user_id'],
                    warning_type=warning_info.get('type', '综合'),
                    content=warning_info['content'],
                    session_id=warning_info['session_id']
                )
                db.session.add(warning)
                db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': {
                'response': response,
                'messageId': ai_msg.id
            }
        })
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] chat 非流式请求错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'发送消息失败: {str(e)}'})


@chat_bp.route('/chatStream', methods=['POST'])
def chat_stream():
    """
    发送消息并获取AI回复（真正的 SSE 流式响应）
    使用简化版流式服务（不使用 LangChain）
    响应完成后自动保存消息到数据库
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'code': 400, 'message': '请求参数错误'})
    
    session_id = data.get('sessionId')
    user_id = data.get('userId')
    message = data.get('message')
    
    if not session_id or not user_id or not message:
        return jsonify({'code': 400, 'message': '缺少必要参数'})
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'code': 400, 'message': '无效的用户ID'})
    
    # 查询会话
    conversation = Conversation.query.filter_by(session_id=session_id).first()
    if not conversation:
        return jsonify({'code': 404, 'message': '会话不存在'})
    
    conversation_id = conversation.id
    
    # 保存用户消息
    user_msg = Message(
        conversation_id=conversation_id,
        role='user',
        content=message
    )
    db.session.add(user_msg)
    
    # 更新会话时间
    conversation.updated_at = datetime.utcnow()
    db.session.commit()
    
    print(f"[DEBUG] chat_stream: 用户消息已保存, user_msg_id={user_msg.id}")
    
    # 获取对话历史（用于构建上下文）
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    history = [{'role': msg.role, 'content': msg.content} for msg in messages]
    
    # 启动保存线程
    start_save_thread(current_app._get_current_object())
    
    def generate():
        """SSE 生成器 - 实时流式响应"""
        full_response = []
        
        try:
            # 使用简化的流式服务
            for chunk_content, accumulated in simple_streaming_service.chat_stream(history, SYSTEM_PROMPT):
                if chunk_content:
                    full_response.append(chunk_content)
                    # 实时发送每个片段给前端（SSE 格式）
                    yield f"data: {chunk_content}\n\n"
            
            # 流式结束后，完整内容已在 full_response 中
            final_response = ''.join(full_response)
            print(f"[DEBUG] chat_stream: AI响应完成, 总长度={len(final_response)}")
            
            if final_response:
                # 将 AI 回复加入保存队列
                save_queue.put((conversation_id, final_response))
                print(f"[DEBUG] chat_stream: AI回复已加入保存队列")
            else:
                print(f"[WARN] chat_stream: AI响应为空，跳过保存")
            
        except Exception as e:
            print(f"[ERROR] chat_stream 流式输出错误: {e}")
            import traceback
            traceback.print_exc()
            yield f"data: 抱歉，服务出现错误。\n\n"
        
        # 发送结束标记
        yield f"data: [DONE]\n\n"
    
    # 返回流式响应（SSE 格式）
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # 禁用 nginx 缓冲
        }
    )


@chat_bp.route('/chatImage', methods=['POST'])
def chat_image():
    """处理图片消息并获取AI回复（流式）"""
    data = request.get_json()
    
    if not data:
        return jsonify({'code': 400, 'message': '请求参数错误'})
    
    session_id = data.get('sessionId')
    user_id = data.get('userId')
    image_url = data.get('message')  # 图片URL
    
    if not session_id or not user_id or not image_url:
        return jsonify({'code': 400, 'message': '缺少必要参数'})
    
    def generate():
        try:
            user_id = int(user_id)
            conversation = Conversation.query.filter_by(session_id=session_id).first()
            
            if not conversation:
                yield f"data: 会话不存在\n\n"
                return
            
            # 保存用户消息
            user_msg = Message(
                conversation_id=conversation.id,
                role='user',
                content=f"[图片] {image_url}"
            )
            db.session.add(user_msg)
            db.session.commit()
            
            # 图片分析提示
            prompt = f"请分析这张图片中的内容，并以心理健康咨询师的角度给出回应。"
            
            # 调用 AI 分析图片（模拟，实际需要多模态模型）
            yield f"data: 图片已收到，正在分析...\n\n"
            yield f"data: 根据图片内容，我建议您关注自己的心理健康。如果您有困扰，可以告诉我更多。\n\n"
            
        except Exception as e:
            yield f"data: 发生错误: {str(e)}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@chat_bp.route('/uploadImage', methods=['POST'])
def upload_image():
    """上传图片"""
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '没有文件'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'code': 400, 'message': '没有选择文件'})
    
    try:
        # 保存文件到 uploads 目录
        import os
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        return jsonify({
            'code': 200,
            'data': filename
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'上传失败: {str(e)}'})