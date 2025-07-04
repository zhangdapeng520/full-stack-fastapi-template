@echo off
chcp 65001 >nul

echo 🚀 启动本地开发环境...

echo 📦 清理现有容器...
docker-compose down -v

echo 🗄️  启动数据库...
docker-compose up -d db

echo ⏳ 等待数据库启动...
timeout /t 10 /nobreak >nul

echo 🔧 启动后端服务...
docker-compose up -d backend

echo ⏳ 等待后端服务启动...
timeout /t 15 /nobreak >nul

echo 🎨 启动前端服务...
docker-compose up -d frontend

echo ✅ 所有服务已启动！
echo 📱 前端地址: http://localhost:5173
echo 🔌 后端API: http://localhost:8000
echo 📊 API文档: http://localhost:8000/docs
echo 🗄️  数据库: localhost:5432

echo 📊 服务状态:
docker-compose ps

pause 