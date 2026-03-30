"""
工具函数
"""
from functools import wraps
from flask import request, jsonify

def token_required(f):
    """Token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'code': 401, 'message': '缺少认证token'})
        # 简单的token验证，实际应用中可以使用JWT等更安全的方案
        if not token.startswith('token_'):
            return jsonify({'code': 401, 'message': '无效的token'})
        return f(*args, **kwargs)
    return decorated_function


def handle_errors(f):
    """错误处理装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'code': 500, 'message': str(e)})
    return decorated_function