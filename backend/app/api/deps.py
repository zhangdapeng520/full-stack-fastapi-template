from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import TokenPayload, User

# OAuth2密码承载者，用于处理访问令牌
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖
    为每个请求提供数据库会话
    
    Yields:
        数据库会话对象
    """
    with Session(engine) as session:
        yield session


# 类型注解别名，用于依赖注入
SessionDep = Annotated[Session, Depends(get_db)]  # 数据库会话依赖
TokenDep = Annotated[str, Depends(reusable_oauth2)]  # 令牌依赖


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    获取当前用户
    验证JWT令牌并返回当前用户对象
    
    Args:
        session: 数据库会话
        token: JWT访问令牌
        
    Returns:
        当前用户对象
        
    Raises:
        HTTPException: 当令牌无效、用户不存在或用户未激活时
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",  # 无法验证凭据
        )
    
    # 根据令牌中的用户ID获取用户
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # 用户未找到
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")  # 用户未激活
    return user


# 当前用户依赖
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """
    获取当前活跃的超级用户
    检查当前用户是否为超级用户
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        超级用户对象
        
    Raises:
        HTTPException: 当用户不是超级用户时
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"  # 用户权限不足
        )
    return current_user
