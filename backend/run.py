"""
心理健康对话系统 - 启动脚本
"""
import sys
from app import create_app, init_database
from app.models import db

app = create_app()

def init_db():
    """初始化数据库"""
    with app.app_context():
        init_database()

def run_server(port=8080):
    """启动服务器"""
    print(f"正在启动心理健康对话系统后端服务...")
    print(f"服务地址: http://localhost:{port}")
    print(f"API文档: http://localhost:{port}/")
    print("\n按 Ctrl+C 停止服务\n")
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init-db':
            init_db()
        elif sys.argv[1] == 'init':
            init_db()
            print("\n数据库初始化完成！现在可以启动服务了。")
        else:
            print(f"未知命令: {sys.argv[1]}")
            print("可用命令:")
            print("  python run.py          - 启动服务")
            print("  python run.py init-db  - 初始化数据库")
    else:
        run_server()