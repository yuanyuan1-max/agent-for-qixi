"""
测试ChatAnywhere API配置
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_api_config():
    """测试API配置"""
    print("🧪 测试ChatAnywhere API配置")
    print("=" * 50)
    
    try:
        # 测试配置加载
        print("1. 测试配置加载...")
        from config.settings import settings
        
        print(f"✅ OpenAI API Key: {settings.OPENAI_API_KEY[:20]}...")
        print(f"✅ OpenAI API Base: {settings.OPENAI_API_BASE}")
        
        # 测试LLM管理器
        print("\n2. 测试LLM管理器...")
        from core.llm_manager import LLMManager
        
        print("正在初始化LLM管理器...")
        llm_manager = LLMManager()
        
        print(f"✅ LLM类型: {'OpenAI API' if llm_manager.use_openai else '本地LLaMA'}")
        
        # 测试模型信息
        print("\n3. 获取模型信息...")
        model_info = llm_manager.get_model_info()
        print(f"✅ 模型信息: {model_info}")
        
        # 测试文本生成
        print("\n4. 测试文本生成...")
        test_prompt = "我想在七夕节为女朋友准备一个浪漫的约会，预算500元以内"
        
        print(f"测试提示: {test_prompt}")
        print("正在生成回答...")
        
        response = llm_manager.generate(test_prompt)
        print(f"✅ 生成成功！回答长度: {len(response)}")
        print("\n生成的回答:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        print("\n🎉 API配置测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_direct():
    """直接测试OpenAI API"""
    print("\n🔍 直接测试OpenAI API")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        # 创建OpenAI客户端
        client = OpenAI(
            api_key="sk-MqcocWJZKTeK25CIpsS3pmCHHEC6Al9Kj4PSQ0E54WsaF8Ng",
            base_url="https://api.chatanywhere.tech/v1"
        )
        
        print("正在发送测试请求...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的七夕约会规划师。"},
                {"role": "user", "content": "请简单介绍一下七夕节。"}
            ],
            max_tokens=100
        )
        
        print("✅ API请求成功！")
        print(f"回答: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ 直接API测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试ChatAnywhere API配置...")
    
    # 测试1: 配置加载
    success1 = test_api_config()
    
    # 测试2: 直接API调用
    success2 = test_openai_direct()
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"配置测试: {'✅ 成功' if success1 else '❌ 失败'}")
    print(f"API测试: {'✅ 成功' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 所有测试通过！你的API配置工作正常。")
        print("现在可以运行主程序了:")
        print("python main.py")
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接。")
