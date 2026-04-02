import os
import torch

class Config:
    # === 基础路径 (自动检测) ===
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    # === 环境变量配置 (支持 .env 文件) ===
    # 如果存在 .env 文件，自动加载
    from pathlib import Path
    env_file = Path(BASE_DIR) / '.env'
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # === 模型配置 ===
    # 文本模型 - 支持环境变量覆盖
    TEXT_MODEL_ID = os.getenv('TEXT_MODEL_ID', 'Qwen/Qwen2.5-1.5B-Instruct')
    VISION_MODEL_ID = os.getenv('VISION_MODEL_ID', 'Qwen/Qwen2-VL-2B-Instruct')
    
    # 运行模式 - 支持环境变量覆盖
    USE_MOCK = os.getenv('USE_MOCK', 'false').lower() == 'true'
    
    # 设备 - 自动检测或环境变量覆盖
    _device_env = os.getenv('DEVICE', '').lower()
    if _device_env in ['cuda', 'cpu']:
        DEVICE = _device_env
    else:
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    # === 知识库路径 ===
    KNOWLEDGE_DB_PATH = os.path.join(BASE_DIR, 'data', 'medical_knowledge.json')

    @staticmethod
    def init_app():
        for path in [Config.UPLOAD_FOLDER, Config.LOG_DIR]:
            if not os.path.exists(path):
                os.makedirs(path)

# 确保初始化目录
Config.init_app()