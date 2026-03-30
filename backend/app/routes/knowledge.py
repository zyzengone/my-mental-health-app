"""
知识图谱路由 - 从 node.json 读取数据
"""
import json
import os
from flask import Blueprint, jsonify

knowledge_bp = Blueprint('knowledge', __name__)

# 获取 node.json 文件路径（从 backend/app/routes/ 向上一级到 backend/）
NODE_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'node.json')
NODE_JSON_PATH = os.path.normpath(NODE_JSON_PATH)


@knowledge_bp.route('/getAll', methods=['GET'])
def get_all_disease():
    """
    获取知识图谱数据
    从 node.json 读取节点和关系数据
    """
    print(f"[DEBUG] 知识图谱文件路径: {NODE_JSON_PATH}")
    print(f"[DEBUG] 文件是否存在: {os.path.exists(NODE_JSON_PATH)}")
    
    try:
        with open(NODE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'code': 200,
            'data': data
        })
    except FileNotFoundError:
        return jsonify({
            'code': 404,
            'message': '知识图谱数据文件不存在'
        })
    except json.JSONDecodeError:
        return jsonify({
            'code': 500,
            'message': '知识图谱数据格式错误'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'读取知识图谱数据失败: {str(e)}'
        })