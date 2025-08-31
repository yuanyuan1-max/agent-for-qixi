"""
七夕约会指南RAG智能体

一个集成了LLaMA系统、LangChain和其他先进技术的智能约会指南系统，
能够进行外网搜索和自主规划，为用户提供个性化的约会建议。

主要功能：
- 基于LLaMA的本地大语言模型
- 实时外网搜索能力
- RAG检索增强生成
- 智能约会规划
- 多源信息整合
- 个性化建议生成

作者: AI Assistant
版本: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "七夕约会指南RAG智能体"

# 导入主要组件
try:
    from .config import settings
    from .core import VectorStore, LLMManager
    from .agents import DatingAgent
    from .tools import WebSearchTool
    from .utils import get_logger
    from .web import app
    
    __all__ = [
        "settings",
        "VectorStore", 
        "LLMManager",
        "DatingAgent",
        "WebSearchTool",
        "get_logger",
        "app"
    ]
    
except ImportError:
    # 如果某些模块还未安装，只提供基本信息
    __all__ = []
