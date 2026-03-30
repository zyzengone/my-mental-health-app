# Flask应用配置

# 数据库配置
MYSQL_HOST = '192.168.51.131'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'mental_health_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask配置
SECRET_KEY = 'mental-health-secret-key-2024'
DEBUG = True

# AI大模型配置（OpenAI兼容API）
AI_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'  # OpenAI兼容API地址
AI_API_KEY = ''  # API密钥
AI_MODEL = 'qwen3.5-flash'  # 使用的模型
AI_TIMEOUT = 60  # 超时时间（秒）
AI_MAX_TOKENS = 2000  # 最大生成token数

# 预警配置
WARNING_THRESHOLD_SCORE = 0.6  # 触发预警的风险分数阈值（0-1）
WARNING_MESSAGE_COUNT = 3  # 连续多少条消息触发分析