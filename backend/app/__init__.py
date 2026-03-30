"""
心理健康对话系统 - Flask应用工厂
"""
from flask import Flask
from flask_cors import CORS
from app.models import db
from app.config import *
import pymysql

def create_app():
    app = Flask(__name__)
    
    # 加载配置
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # 初始化SQLAlchemy
    db.init_app(app)
    
    # 启用CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # 注册蓝图
    from app.routes.user import user_bp
    from app.routes.chat import chat_bp
    from app.routes.personality import personality_bp
    from app.routes.knowledge import knowledge_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(chat_bp, url_prefix='/model')
    app.register_blueprint(personality_bp, url_prefix='/model')
    app.register_blueprint(knowledge_bp, url_prefix='/node')
    
    return app

def init_database():
    """初始化数据库"""
    # 先创建数据库
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.close()
    
    # 导入并创建所有模型
    from app.models.user import User
    from app.models.session import Conversation
    from app.models.message import Message
    from app.models.warning import Warning
    
    # 创建应用上下文并创建表
    app = create_app()
    with app.app_context():
        db.create_all()
    print("数据库初始化完成！")