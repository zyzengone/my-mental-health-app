# 心理健康对话系统 - 后端 API

## 项目简介
这是一个心理健康对话系统的后端API，使用Python Flask框架构建，支持与OpenAI兼容API集成，提供MBTI人格分析和心理危机预警功能。

## 功能特性
- 用户认证（注册、登录）
- 聊天会话管理
- 实时对话（集成AI大模型）
- MBTI人格分析
- 心理危机预警（AI智能分析）

## 技术栈
- Python 3.9+
- Flask 2.x
- SQLAlchemy
- PyMySQL
- Flask-CORS

## 项目结构
```
backend/
├── app/
│   ├── __init__.py          # Flask应用工厂
│   ├── config.py            # 配置管理
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   ├── session.py       # 会话模型
│   │   ├── message.py       # 消息模型
│   │   └── warning.py       # 预警模型
│   ├── routes/              # 路由
│   │   ├── __init__.py
│   │   ├── user.py          # 用户相关路由
│   │   ├── chat.py          # 聊天相关路由
│   │   └── personality.py  # 人格分析路由
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── ai_service.py           # AI大模型服务（OpenAI兼容）
│   │   ├── personality_service.py  # 人格分析服务
│   │   └── warning_service.py      # 预警服务
│   └── utils/               # 工具函数
│       └── __init__.py
├── requirements.txt         # 依赖
├── run.py                   # 启动脚本
├── .env                     # 环境配置
└── README.md
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置AI服务
编辑 `.env` 或 `app/config.py` 中的AI配置：
```python
AI_BASE_URL = 'http://localhost:8000/v1'  # OpenAI兼容API地址
AI_API_KEY = 'your-api-key'
AI_MODEL = 'gpt-3.5-turbo'
```

### 3. 配置数据库
编辑 `app/config.py` 中的数据库配置：
```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'mental_health_db'
```

### 4. 初始化数据库
```bash
python run.py init-db
```

### 5. 启动服务
```bash
python run.py
```

服务将在 http://localhost:8080 上运行

## API接口文档

### 用户接口

#### 注册
- **URL**: POST /user/register
- **参数**: `{"username": "xxx", "password": "xxx", "email": "xxx"}`
- **返回**: `{"code": 200, "data": {"userId": 1}}`

#### 登录
- **URL**: POST /user/login
- **参数**: `{"username": "xxx", "password": "xxx"}`
- **返回**: `{"code": 200, "data": {"token": "xxx", "userId": 1}}`

### 聊天接口

#### 获取用户会话列表
- **URL**: GET /model/sessions?userId={userId}
- **返回**: `{"code": 200, "data": [...]}`

#### 创建新会话
- **URL**: POST /model/createSession?userId={userId}
- **返回**: `{"code": 200, "data": {"sessionId": "xxx"}}`

#### 获取会话历史
- **URL**: GET /model/conversationHistory?sessionId={sessionId}
- **返回**: `{"code": 200, "data": [...]}`

#### 发送消息
- **URL**: POST /model/chat
- **参数**: `{"sessionId": "xxx", "userId": 1, "message": "xxx"}`
- **返回**: `{"code": 200, "data": {"response": "xxx"}}`

#### 删除会话
- **URL**: POST /model/deleteSession?sessionId={sessionId}
- **返回**: `{"code": 200, "data": 1}`

### 人格分析接口

#### 获取用户人格类型
- **URL**: GET /model/personality?userId={userId}
- **返回**: `{"code": 200, "data": {"personalityType": "INTJ"}}`

#### 获取用户人格类型（别名）
- **URL**: GET /model/getPersonality?userId={userId}
- **返回**: `{"code": 200, "data": {"personalityType": "INTJ"}}`

#### 更新用户人格类型
- **URL**: GET /model/updatePersonality?userId={userId}
- **返回**: `{"code": 200, "data": {"personalityType": "INTJ"}}`

#### 保存人格分析结果
- **URL**: GET /model/savePersonality?userId={userId}&personality={type}
- **返回**: `{"code": 200, "data": "success"}`

### 预警接口

#### 获取预警列表
- **URL**: GET /model/getUserWarning
- **返回**: `{"code": 200, "data": [...]}`

#### 处理预警
- **URL**: POST /model/dealWarning
- **参数**: `{"warningId": 1, "dealtBy": 1}`
- **返回**: `{"code": 200, "data": "success"}`

## 预警说明

系统使用AI大模型对对话进行实时智能分析，评估用户心理状态：

### 分析维度
- 自杀风险评估
- 抑郁倾向检测
- 焦虑状态分析
- 其他心理危机信号

### 预警触发条件
- 风险分数 >= 0.6（可配置）
- 每3条消息触发一次分析（可配置）

### 预警响应格式
```json
{
    "risk_level": "high/medium/low",
    "risk_type": "自杀/抑郁/焦虑/综合",
    "risk_score": 0.0-1.0,
    "warning_message": "简要描述",
    "need_attention": true/false
}
```

## 配置说明

### AI服务配置
确保使用OpenAI兼容的API服务，可以是：
- 本地部署的LLM服务（如vLLM、Ollama with OpenAI兼容模式）
- 云端API代理服务
- 其他兼容API

### 预警阈值
可在 `app/config.py` 中调整预警敏感度：
- `WARNING_THRESHOLD_SCORE`: 风险分数阈值（默认0.6）
- `WARNING_MESSAGE_COUNT`: 分析间隔消息数（默认3）