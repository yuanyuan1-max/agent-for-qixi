"""
系统配置文件
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """系统配置类"""
    
    # 项目根目录
    BASE_DIR: Path = Path(__file__).parent.parent
    
    # 数据目录
    DATA_DIR: Path = BASE_DIR / "data"
    VECTOR_DB_DIR: Path = DATA_DIR / "vector_db"
    CACHE_DIR: Path = BASE_DIR / "cache"
    
    # LLM模型配置
    MODEL_NAME: str = "meta-llama/Llama-2-7b-chat-hf"
    MODEL_CACHE_DIR: Path = BASE_DIR / "models"
    
    # 向量数据库配置
    VECTOR_DB_TYPE: str = "chroma"  # chroma 或 faiss
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # 搜索配置
    SEARCH_ENGINE: str = "duckduckgo"
    MAX_SEARCH_RESULTS: int = 10
    
    # RAG配置
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RETRIEVAL: int = 5
    
    # API配置
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = BASE_DIR / "logs" / "app.log"
    
    # Web服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 创建全局配置实例
settings = Settings()

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        settings.DATA_DIR,
        settings.VECTOR_DB_DIR,
        settings.CACHE_DIR,
        settings.MODEL_CACHE_DIR,
        settings.LOG_FILE.parent
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# 初始化时创建目录
ensure_directories()
