"""
七夕约会指南RAG智能体 - 主程序
"""
import asyncio
import sys
from pathlib import Path

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """主函数"""
    try:
        logger.info("=" * 50)
        logger.info("🎉 七夕约会指南RAG智能体启动中...")
        logger.info("=" * 50)
        
        # 检查系统环境
        check_environment()
        
        # 启动Web服务
        start_web_service()
        
    except KeyboardInterrupt:
        logger.info("用户中断，正在退出...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"系统启动失败: {e}")
        sys.exit(1)

def check_environment():
    """检查系统环境"""
    logger.info("🔍 检查系统环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        raise RuntimeError(f"需要Python 3.8+，当前版本: {python_version.major}.{python_version.minor}")
    
    logger.info(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的目录
    required_dirs = [
        settings.DATA_DIR,
        settings.VECTOR_DB_DIR,
        settings.CACHE_DIR,
        settings.MODEL_CACHE_DIR
    ]
    
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ 目录就绪: {directory}")
    
    logger.info("✅ 系统环境检查完成")

def start_web_service():
    """启动Web服务"""
    logger.info("🚀 启动Web服务...")
    
    try:
        import uvicorn
        from web.app import app
        
        logger.info(f"Web服务将在 http://{settings.HOST}:{settings.PORT} 启动")
        logger.info("按 Ctrl+C 停止服务")
        
        # 启动服务
        uvicorn.run(
            app,
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower()
        )
        
    except ImportError as e:
        logger.error(f"导入Web模块失败: {e}")
        logger.info("请确保已安装所有依赖: pip install -r requirements.txt")
        raise
    except Exception as e:
        logger.error(f"启动Web服务失败: {e}")
        raise

def start_cli_mode():
    """启动命令行模式"""
    logger.info("💻 启动命令行模式...")
    
    try:
        from agents.dating_agent import DatingAgent
        
        # 初始化智能体
        logger.info("正在初始化智能体...")
        agent = DatingAgent()
        
        logger.info("智能体初始化完成！")
        logger.info("输入 'quit' 或 'exit' 退出")
        logger.info("-" * 50)
        
        # 交互循环
        while True:
            try:
                user_input = input("\n💕 请描述你的约会需求: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    logger.info("再见！💕")
                    break
                
                if not user_input:
                    continue
                
                logger.info("🤖 AI正在为你规划约会...")
                
                # 调用智能体
                result = agent.plan_dating(user_input)
                
                print("\n" + "=" * 50)
                print("💡 约会规划建议:")
                print("=" * 50)
                print(result["answer"])
                
                if result.get("source_documents"):
                    print("\n📚 参考信息:")
                    for i, doc in enumerate(result["source_documents"][:2]):
                        print(f"来源 {i+1}: {doc['content'][:100]}...")
                
                if result.get("search_results"):
                    print("\n🌐 网络搜索结果:")
                    for i, result_item in enumerate(result["search_results"][:2]):
                        print(f"结果 {i+1}: {result_item['title']}")
                        print(f"       {result_item['snippet'][:100]}...")
                
                print("=" * 50)
                
            except KeyboardInterrupt:
                logger.info("\n用户中断，正在退出...")
                break
            except Exception as e:
                logger.error(f"处理用户输入失败: {e}")
                print(f"❌ 抱歉，处理你的请求时出现错误: {e}")
    
    except Exception as e:
        logger.error(f"启动命令行模式失败: {e}")
        raise

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # 命令行模式
        start_cli_mode()
    else:
        # Web模式（默认）
        main()
