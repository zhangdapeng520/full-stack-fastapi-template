import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    """
    解析CORS配置
    支持字符串和列表格式的CORS origins配置
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    应用配置类
    管理所有环境变量和配置设置
    """
    model_config = SettingsConfigDict(
        # 使用顶级.env文件（在./backend/上一级）
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    
    # API配置
    API_V1_STR: str = "/api/v1"  # API版本路径
    SECRET_KEY: str = secrets.token_urlsafe(32)  # JWT密钥
    # 60分钟 * 24小时 * 8天 = 8天
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 访问令牌过期时间
    FRONTEND_HOST: str = "http://localhost:5173"  # 前端主机地址
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"  # 运行环境

    # CORS配置
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []  # 允许跨域访问的源

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        """
        计算所有CORS origins，包括前端主机
        """
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # 项目信息
    PROJECT_NAME: str  # 项目名称
    SENTRY_DSN: HttpUrl | None = None  # Sentry错误追踪DSN
    
    # 数据库配置
    POSTGRES_SERVER: str  # PostgreSQL服务器地址
    POSTGRES_PORT: int = 5432  # PostgreSQL端口
    POSTGRES_USER: str  # PostgreSQL用户名
    POSTGRES_PASSWORD: str = ""  # PostgreSQL密码
    POSTGRES_DB: str = ""  # PostgreSQL数据库名

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        构建SQLAlchemy数据库连接URI
        """
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # 邮件配置
    SMTP_TLS: bool = True  # 启用TLS加密
    SMTP_SSL: bool = False  # 启用SSL加密
    SMTP_PORT: int = 587  # SMTP端口
    SMTP_HOST: str | None = None  # SMTP服务器地址
    SMTP_USER: str | None = None  # SMTP用户名
    SMTP_PASSWORD: str | None = None  # SMTP密码
    EMAILS_FROM_EMAIL: EmailStr | None = None  # 发件人邮箱
    EMAILS_FROM_NAME: EmailStr | None = None  # 发件人名称

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        """
        设置默认发件人名称
        """
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48  # 邮件重置令牌过期时间（小时）

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        """
        检查邮件功能是否启用
        """
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # 测试用户邮箱
    
    # 超级用户配置
    FIRST_SUPERUSER: EmailStr  # 第一个超级用户邮箱
    FIRST_SUPERUSER_PASSWORD: str  # 第一个超级用户密码

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """
        检查默认密钥，确保生产环境不使用默认值
        """
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        强制检查所有密钥配置，确保不使用默认值
        """
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


# 创建全局配置实例
settings = Settings()  # type: ignore
