#!/bin/bash

# 七夕约会指南RAG智能体安装脚本

echo "🎉 欢迎使用七夕约会指南RAG智能体！"
echo "=================================="

# 检查conda环境
if ! command -v conda &> /dev/null; then
    echo "❌ 未检测到conda，请先安装Anaconda或Miniconda"
    exit 1
fi

# 激活conda环境
echo "🔧 正在激活conda环境 'school'..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate school

if [ $? -ne 0 ]; then
    echo "❌ 无法激活conda环境 'school'，请检查环境名称"
    exit 1
fi

echo "✅ conda环境 'school' 激活成功"

# 检查Python版本
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 当前Python版本: $python_version"

if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ 需要Python 3.8+，当前版本过低"
    exit 1
fi

# 升级pip
echo "📦 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装Python依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接和requirements.txt文件"
    exit 1
fi

echo "✅ 依赖安装完成"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p data/vector_db data/cache models logs

# 复制环境变量文件
if [ ! -f .env ]; then
    echo "📝 创建环境变量文件..."
    cp env_example.txt .env
    echo "✅ 环境变量文件已创建，请根据需要编辑 .env 文件"
else
    echo "✅ 环境变量文件已存在"
fi

echo ""
echo "🎊 安装完成！"
echo "=================================="
echo "使用方法："
echo "1. Web模式: python main.py"
echo "2. 命令行模式: python main.py --cli"
echo "3. 访问 http://localhost:8000 使用Web界面"
echo ""
echo "注意事项："
echo "- 首次运行时会下载必要的模型文件，请耐心等待"
echo "- 确保有足够的磁盘空间（建议至少5GB）"
echo "- 如果使用GPU，确保已安装CUDA和PyTorch"
echo ""
echo "💕 祝您使用愉快！"
