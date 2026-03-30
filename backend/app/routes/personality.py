"""
人格分析路由
"""
from flask import Blueprint, request, jsonify
from app.models import db
from app.models.user import User
from app.models.session import Conversation
from app.models.message import Message
from app.services.personality_service import personality_service

personality_bp = Blueprint('personality', __name__)

@personality_bp.route('/personality', methods=['GET'])
def get_personality():
    """获取用户的人格类型"""
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'})
    
    try:
        user_id = int(user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'})
        
        return jsonify({
            'code': 200,
            'data': {
                'personalityType': user.personality_type or 'unknown',
                'description': personality_service.get_personality_description(user.personality_type) if user.personality_type else None
            }
        })
    except ValueError:
        return jsonify({'code': 400, 'message': '无效的用户ID'})

# 别名路由，兼容前端调用
@personality_bp.route('/getPersonality', methods=['GET'])
def get_personality_alias():
    """获取用户的人格类型（别名）"""
    return get_personality()

@personality_bp.route('/updatePersonality', methods=['GET'])
def update_personality():
    """更新用户的人格类型（基于对话分析）"""
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'})
    
    try:
        user_id = int(user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'})
        
        # 获取用户所有对话消息
        conversations = Conversation.query.filter_by(user_id=user_id).all()
        
        all_messages = []
        for conv in conversations:
            messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.created_at).all()
            all_messages.extend([{'role': msg.role, 'content': msg.content} for msg in messages])
        
        if len(all_messages) < 5:
            return jsonify({
                'code': 200,
                'data': {
                    'personalityType': user.personality_type or 'unknown',
                    'message': '对话数据不足，无法准确分析'
                }
            })
        
        # 分析人格
        personality_type = personality_service.analyze_personality(all_messages)
        
        # 更新用户人格类型
        user.personality_type = personality_type
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': {
                'personalityType': personality_type,
                'description': personality_service.get_personality_description(personality_type)
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'分析失败: {str(e)}'})

@personality_bp.route('/savePersonality', methods=['GET'])
def save_personality():
    """保存用户的人格类型"""
    user_id = request.args.get('userId')
    personality = request.args.get('personality')
    
    if not user_id or not personality:
        return jsonify({'code': 400, 'message': '缺少必要参数'})
    
    try:
        user_id = int(user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'})
        
        user.personality_type = personality
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': 'success'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'保存失败: {str(e)}'})

@personality_bp.route('/getUserWarning', methods=['GET'])
def get_user_warning():
    """获取所有预警记录"""
    from app.models.warning import Warning
    from app.models import db
    
    try:
        # 获取所有未处理的预警，按时间倒序
        warnings = Warning.query.filter_by(is_dealt=False).order_by(Warning.created_at.desc()).all()
        
        return jsonify({
            'code': 200,
            'data': [w.to_dict() for w in warnings]
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取预警失败: {str(e)}'})

@personality_bp.route('/dealWarning', methods=['POST'])
def deal_warning():
    """处理预警"""
    from app.models.warning import Warning
    from app.models import db
    
    data = request.get_json()
    warning_id = data.get('warningId')
    dealt_by = data.get('dealtBy')
    
    if not warning_id:
        return jsonify({'code': 400, 'message': '缺少预警ID'})
    
    try:
        warning = Warning.query.get(warning_id)
        
        if not warning:
            return jsonify({'code': 404, 'message': '预警不存在'})
        
        warning.is_dealt = True
        warning.dealt_by = dealt_by
        from datetime import datetime
        warning.dealt_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': 'success'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'处理失败: {str(e)}'})