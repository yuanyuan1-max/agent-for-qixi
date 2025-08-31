# 🚀 七夕约会指南RAG智能体 - 部署说明

## 🎯 项目概述

这是一个集成了LLaMA系统、LangChain和其他先进技术的智能约会指南系统，具备以下核心功能：

- 🤖 **本地LLM**: 基于LLaMA 2的大语言模型
- 🔍 **实时搜索**: 外网搜索约会创意和地点
- 📚 **RAG系统**: 检索增强生成，提供精准建议
- 🎨 **智能规划**: 个性化约会方案生成
- 🌐 **Web界面**: 美观易用的用户界面
- 💻 **命令行**: 快速交互模式

## 🏗️ 技术架构

```
用户界面层 (Web/CLI)
        ↓
   智能体层 (DatingAgent)
        ↓
   核心服务层 (LLM + VectorDB + Search)
        ↓
   数据存储层 (ChromaDB/FAISS + 模型缓存)
```

### 核心技术栈
- **LLM框架**: Transformers, LangChain
- **向量数据库**: ChromaDB, FAISS
- **Web框架**: FastAPI
- **搜索工具**: DuckDuckGo Search
- **向量嵌入**: Sentence Transformers
- **日志系统**: Loguru

## 📦 安装部署

### 1. 环境准备
```bash
# 激活conda环境
conda activate school

# 检查Python版本 (需要3.8+)
python --version
```

### 2. 一键安装
```bash
# 给脚本执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh
```

### 3. 手动安装（可选）
```bash
# 安装依赖
pip install -r requirements.txt

# 创建必要目录
mkdir -p data/vector_db data/cache models logs

# 配置环境变量
cp env_example.txt .env
# 编辑 .env 文件
```

## 🚀 启动运行

### 方式一：启动脚本（推荐）
```bash
./start.sh
```

### 方式二：直接运行
```bash
# Web模式
python main.py

# 命令行模式
python main.py --cli
```

### 方式三：模块化启动
```bash
# 启动Web服务
python -m web.app

# 运行测试
python test_system.py
```

## 🔧 配置调优

### 环境变量配置
```bash
# 复制配置模板
cp env_example.txt .env

# 编辑配置文件
nano .env
```

### 主要配置项
```bash
# 向量数据库类型
VECTOR_DB_TYPE=chroma  # 或 faiss

# 嵌入模型
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# LLM模型
MODEL_NAME=meta-llama/Llama-2-7b-chat-hf

# 搜索配置
SEARCH_ENGINE=duckduckgo
MAX_SEARCH_RESULTS=10

# RAG参数
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
```

## 📊 性能优化

### 内存优化
- 使用4bit量化模型（GPU环境）
- 调整chunk_size和overlap参数
- 限制搜索结果数量

### 速度优化
- 使用SSD存储
- 启用GPU加速（如果可用）
- 调整向量数据库参数

### 准确性优化
- 增加知识库内容
- 调整检索参数
- 优化提示词模板

## 🧪 测试验证

### 系统测试
```bash
python test_system.py
```

### 功能测试
```bash
# 测试向量存储
python -c "from core.vector_store import VectorStore; vs = VectorStore(); print('✅ 向量存储正常')"

# 测试搜索功能
python -c "from tools.web_search import WebSearchTool; ws = WebSearchTool(); print('✅ 搜索功能正常')"

# 测试智能体
python -c "from agents.dating_agent import DatingAgent; da = DatingAgent(); print('✅ 智能体正常')"
```

## 📈 监控运维

### 日志监控
- 日志文件位置: `logs/app.log`
- 日志级别: INFO/DEBUG/ERROR
- 日志轮转: 10MB/7天

### 性能监控
- 向量数据库统计
- 模型响应时间
- 搜索成功率

### 健康检查
```bash
# API健康检查
curl http://localhost:8000/api/status

# 系统状态
curl http://localhost:8000/api/health
```

## 🚨 故障排除

### 常见问题

#### 1. 模型下载失败
```bash
# 清理缓存
rm -rf models/*
# 重新安装
pip install --force-reinstall transformers
```

#### 2. 向量数据库错误
```bash
# 重新初始化
rm -rf data/vector_db/*
# 重启系统
```

#### 3. 内存不足
```bash
# 使用更小的模型
# 调整配置参数
# 增加swap空间
```

#### 4. 搜索功能异常
```bash
# 检查网络连接
# 验证API配置
# 查看错误日志
```

### 调试模式
```bash
# 启用调试日志
export LOG_LEVEL=DEBUG

# 启动调试模式
python main.py --debug
```

## 🔒 安全考虑

### 网络安全
- 限制访问IP
- 启用HTTPS
- 配置防火墙

### 数据安全
- 加密敏感配置
- 定期备份数据
- 访问权限控制

## 📚 扩展开发

### 添加新功能
1. 在相应模块中添加功能
2. 更新配置文件
3. 添加测试用例
4. 更新文档

### 集成新模型
1. 在`core/llm_manager.py`中添加支持
2. 更新模型配置
3. 测试兼容性

### 自定义知识库
1. 准备数据文件
2. 使用`vector_store.add_documents()`添加
3. 验证检索效果

## 🎉 部署完成

恭喜！您的七夕约会指南RAG智能体已经部署完成。

### 下一步建议
1. 运行系统测试确保一切正常
2. 尝试一些约会规划查询
3. 根据使用情况调整配置
4. 考虑添加更多约会知识

### 获取帮助
- 查看日志文件了解详细错误信息
- 运行测试脚本诊断系统状态
- 参考技术文档和示例代码

---

💕 **祝您使用愉快，创造美好回忆！** 💕
