#!/bin/bash

# 本地开发启动脚本
echo "🚀 启动本地开发环境..."

# 停止并清理现有容器
echo "📦 清理现有容器..."
docker-compose down -v

# 启动数据库
echo "🗄️  启动数据库..."
docker-compose up -d db

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 10

# 启动后端
echo "🔧 启动后端服务..."
docker-compose up -d backend

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 15

# 启动前端
echo "🎨 启动前端服务..."
docker-compose up -d frontend

echo "✅ 所有服务已启动！"
echo "📱 前端地址: http://localhost:5173"
echo "🔌 后端API: http://localhost:8000"
echo "📊 API文档: http://localhost:8000/docs"
echo "🗄️  数据库: localhost:5432"

# 显示服务状态
echo "📊 服务状态:"
docker-compose ps 