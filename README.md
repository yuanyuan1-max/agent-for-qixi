# 七夕约会指南RAG智能体

这是一个集成了LLaMA系统、LangChain和其他先进技术的智能约会指南系统，能够进行外网搜索和自主规划。

## 功能特性

- 🤖 基于LLaMA的本地大语言模型
- 🔍 实时外网搜索能力
- 📚 RAG检索增强生成
- 🎯 智能约会规划
- 🌐 多源信息整合
- 💡 个性化建议生成

## 系统架构

```
用户查询 → 意图识别 → 信息检索 → 知识整合 → 规划生成 → 建议输出
    ↓           ↓         ↓         ↓         ↓         ↓
  自然语言    LLM分析   向量搜索    RAG增强   智能规划   格式化输出
```

## 安装说明

1. 激活conda环境：
```bash
conda activate school
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，填入必要的API密钥
```

4. 运行系统：
```bash
python main.py
```

## 使用方法

1. 启动系统后，可以通过命令行或Web界面与智能体交互
2. 输入约会相关的问题，如"帮我规划一个浪漫的七夕约会"
3. 系统会自动搜索相关信息，生成个性化建议

## 技术栈

- **LLM**: LLaMA 2, Transformers
- **框架**: LangChain, LangChain Community
- **向量数据库**: ChromaDB, FAISS
- **搜索**: DuckDuckGo Search
- **Web框架**: FastAPI
- **向量嵌入**: Sentence Transformers

## 项目结构

```
├── main.py                 # 主程序入口
├── config/                 # 配置文件
├── core/                   # 核心功能模块
├── agents/                 # 智能体模块
├── tools/                  # 工具模块
├── data/                   # 数据存储
├── web/                    # Web界面
└── utils/                  # 工具函数
```
