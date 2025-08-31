# 🚀 七夕约会指南RAG智能体 - 快速启动指南

## 📋 系统要求

- **操作系统**: Linux (WSL2), macOS, Windows
- **Python**: 3.8+
- **内存**: 建议8GB+
- **磁盘空间**: 至少5GB可用空间
- **网络**: 稳定的互联网连接（用于下载模型和搜索）

## ⚡ 快速启动

### 1. 激活conda环境
```bash
conda activate school
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动系统

#### 方式一：使用启动脚本（推荐）
```bash
./start.sh
```

#### 方式二：直接运行
```bash
# Web模式
python main.py

# 命令行模式
python main.py --cli
```

### 4. 访问系统
- **Web界面**: 打开浏览器访问 http://localhost:8000
- **命令行**: 直接在终端中与AI交互

## 🧪 系统测试

运行测试确保系统正常：
```bash
python test_system.py
```

## 📁 项目结构

```
├── main.py                 # 主程序入口
├── config/                 # 配置文件
├── core/                   # 核心功能模块
│   ├── vector_store.py    # 向量数据库管理
│   └── llm_manager.py     # LLM模型管理
├── agents/                 # 智能体模块
│   └── dating_agent.py    # 约会指南智能体
├── tools/                  # 工具模块
│   └── web_search.py      # 网络搜索工具
├── web/                    # Web界面
│   └── app.py             # FastAPI应用
├── utils/                  # 工具函数
│   └── logger.py          # 日志管理
├── data/                   # 数据存储
├── models/                 # 模型缓存
└── logs/                   # 日志文件
```

## 🔧 配置说明

### 环境变量
复制 `env_example.txt` 为 `.env` 并编辑：
```bash
cp env_example.txt .env
```

### 主要配置项
- `VECTOR_DB_TYPE`: 向量数据库类型 (chroma/faiss)
- `EMBEDDING_MODEL`: 文本嵌入模型
- `MODEL_NAME`: LLM模型名称
- `SEARCH_ENGINE`: 搜索引擎

## 💡 使用示例

### Web界面使用
1. 启动Web服务
2. 在浏览器中输入约会需求
3. 获得AI生成的约会规划建议

### 命令行使用
```bash
python main.py --cli

# 输入示例：
# "我想在七夕节为女朋友准备一个浪漫的约会，预算1000元以内，她喜欢看电影和美食"
```

## 🚨 常见问题

### Q: 首次启动很慢？
A: 系统需要下载模型文件，请耐心等待。建议使用稳定的网络连接。

### Q: 内存不足？
A: 可以调整配置中的模型大小，或使用更小的模型。

### Q: 搜索功能不工作？
A: 检查网络连接，确保可以访问外网。

### Q: 向量数据库错误？
A: 删除 `data/vector_db` 目录重新初始化。

## 📞 技术支持

如果遇到问题：
1. 查看日志文件 `logs/app.log`
2. 运行 `python test_system.py` 检查系统状态
3. 检查Python版本和依赖安装

## 🎯 下一步

- 自定义约会知识库
- 调整AI模型参数
- 集成更多数据源
- 优化搜索算法

---

💕 **祝您使用愉快！** 💕
