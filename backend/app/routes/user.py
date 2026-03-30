"""
用户路由 - 登录注册
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db
from app.models.user import User
import secrets

user_bp = Blueprint('user', __name__)

def make_token(user_id):
    """生成简单的token"""
    return f"token_{user_id}_{secrets.token_hex(16)}"

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data:
        return jsonify({'code': 400, 'message': '请求参数错误'})
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'})
    
    # 检查用户是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'code': 400, 'message': '用户名已存在'})
    
    # 创建新用户
    try:
        user = User(
            username=username,
            password=generate_password_hash(password),
            email=email
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': {
                'userId': user.id,
                'username': user.username
            },
            'message': '注册成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'注册失败: {str(e)}'})

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data:
        return jsonify({'code': 400, 'message': '请求参数错误'})
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'})
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'code': 401, 'message': '用户名或密码错误'})
    
    # 生成token
    token = make_token(user.id)
    
    return jsonify({
        'code': 200,
        'data': {
            'token': token,
            'userId': user.id,
            'username': user.username,
            'personalityType': user.personality_type
        },
        'message': '登录成功'
    })

@user_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    return jsonify({
        'code': 200,
        'message': '登出成功'
    })

@user_bp.route('/userinfo', methods=['GET'])
def get_userinfo():
    """获取用户信息"""
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'})
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    return jsonify({
        'code': 200,
        'data': user.to_dict()
    })

@user_bp.route('/updatePersonality', methods=['POST'])
def update_personality():
    """更新用户人格类型"""
    data = request.get_json()
    user_id = data.get('userId')
    personality = data.get('personality')
    
    if not user_id or not personality:
        return jsonify({'code': 400, 'message': '缺少参数'})
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    user.personality_type = personality
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'data': {'personalityType': personality},
        'message': '更新成功'
    })