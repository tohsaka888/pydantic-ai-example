# 导入OpenAI模型和提供者类
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# 导入环境变量相关库
import os
from dotenv import load_dotenv

# 从.env文件加载环境变量
load_dotenv()

# 获取必要的环境变量
MODEL_NAME = os.getenv("MODEL_NAME")  # 模型名称
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API密钥
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL")  # API基础URL

# 检查必需环境变量是否设置
if MODEL_NAME is None:
    raise ValueError("MODEL_NAME environment variable is not set")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# 初始化OpenAI提供者
provider = OpenAIProvider(
    base_url=OPENAI_API_BASE_URL,  # API基础URL
    api_key=OPENAI_API_KEY,  # API密钥
)

# 创建OpenAI模型实例
model = OpenAIModel(
    model_name=MODEL_NAME,  # 模型名称
    provider=provider  # 提供者实例
)
