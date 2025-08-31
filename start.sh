#!/bin/bash

# 七夕约会指南RAG智能体启动脚本



# 启动系统
echo "🎯 选择启动模式："
echo "1. Web模式 (推荐)"
echo "2. 命令行模式"
echo "3. 退出"
read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🌐 启动Web模式..."
        python main.py
        ;;
    2)
        echo "💻 启动命令行模式..."
        python main.py --cli
        ;;
    3)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选择，启动Web模式..."
        python main.py
        ;;
esac
