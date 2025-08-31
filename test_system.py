"""
系统测试文件
"""
import sys
import traceback
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试配置模块
        from config.settings import settings
        print("✅ 配置模块导入成功")
        
        # 测试日志模块
        from utils.logger import get_logger
        logger = get_logger(__name__)
        print("✅ 日志模块导入成功")
        
        # 测试向量存储模块
        from core.vector_store import VectorStore
        print("✅ 向量存储模块导入成功")
        
        # 测试网络搜索模块
        from tools.web_search import WebSearchTool
        print("✅ 网络搜索模块导入成功")
        
        # 测试智能体模块
        from agents.dating_agent import DatingAgent
        print("✅ 智能体模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        traceback.print_exc()
        return False

def test_config():
    """测试配置系统"""
    print("\n🔍 测试配置系统...")
    
    try:
        from config.settings import settings
        
        print(f"✅ 项目根目录: {settings.BASE_DIR}")
        print(f"✅ 数据目录: {settings.DATA_DIR}")
        print(f"✅ 向量数据库目录: {settings.VECTOR_DB_DIR}")
        print(f"✅ 模型缓存目录: {settings.MODEL_CACHE_DIR}")
        print(f"✅ 向量数据库类型: {settings.VECTOR_DB_TYPE}")
        print(f"✅ 嵌入模型: {settings.EMBEDDING_MODEL}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_directories():
    """测试目录结构"""
    print("\n🔍 测试目录结构...")
    
    try:
        from config.settings import settings
        
        required_dirs = [
            settings.DATA_DIR,
            settings.VECTOR_DB_DIR,
            settings.CACHE_DIR,
            settings.MODEL_CACHE_DIR
        ]
        
        for directory in required_dirs:
            directory.mkdir(parents=True, exist_ok=True)
            if directory.exists():
                print(f"✅ 目录就绪: {directory}")
            else:
                print(f"❌ 目录创建失败: {directory}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 目录结构测试失败: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔍 测试基本功能...")
    
    try:
        # 测试向量存储初始化
        print("测试向量存储初始化...")
        from core.vector_store import VectorStore
        vector_store = VectorStore()
        print("✅ 向量存储初始化成功")
        
        # 测试网络搜索工具
        print("测试网络搜索工具...")
        from tools.web_search import WebSearchTool
        search_tool = WebSearchTool()
        print("✅ 网络搜索工具初始化成功")
        
        # 测试日志功能
        print("测试日志功能...")
        from utils.logger import get_logger
        logger = get_logger("test")
        logger.info("这是一条测试日志")
        print("✅ 日志功能正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 七夕约会指南RAG智能体 - 系统测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("配置系统", test_config),
        ("目录结构", test_directories),
        ("基本功能", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪。")
        print("\n使用方法：")
        print("1. 运行 ./start.sh 启动系统")
        print("2. 或直接运行 python main.py")
    else:
        print("⚠️  部分测试失败，请检查错误信息。")
        print("建议：")
        print("1. 确保已安装所有依赖: pip install -r requirements.txt")
        print("2. 检查Python版本是否为3.8+")
        print("3. 确保有足够的磁盘空间")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
