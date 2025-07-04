import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    自定义生成唯一ID函数
    用于OpenAPI文档中的操作ID
    
    Args:
        route: API路由对象
        
    Returns:
        唯一的操作ID
    """
    return f"{route.tags[0]}-{route.name}"


# 初始化Sentry错误追踪（仅在非本地环境且配置了DSN时）
if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,  # 应用标题
    openapi_url=f"{settings.API_V1_STR}/openapi.json",  # OpenAPI文档URL
    generate_unique_id_function=custom_generate_unique_id,  # 自定义ID生成函数
)

# 配置CORS中间件
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,  # 允许的源
        allow_credentials=True,  # 允许凭据
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有请求头
    )

# 包含API路由器
app.include_router(api_router, prefix=settings.API_V1_STR)
