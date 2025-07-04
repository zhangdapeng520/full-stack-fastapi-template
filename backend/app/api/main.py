from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings

# 创建主API路由器
api_router = APIRouter()

# 包含各个功能模块的路由器
api_router.include_router(login.router)  # 登录认证路由
api_router.include_router(users.router)  # 用户管理路由
api_router.include_router(utils.router)  # 工具功能路由
api_router.include_router(items.router)  # 项目管理路由

# 仅在本地开发环境包含私有路由（用于测试和调试）
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
