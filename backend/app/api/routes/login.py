from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import Message, NewPassword, Token, UserPublic
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

# 创建登录路由器
router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2兼容的令牌登录
    获取访问令牌用于后续请求
    
    Args:
        session: 数据库会话
        form_data: OAuth2密码请求表单
        
    Returns:
        包含访问令牌的Token对象
        
    Raises:
        HTTPException: 当邮箱或密码错误，或用户未激活时
    """
    # 验证用户凭据
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")  # 邮箱或密码错误
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")  # 用户未激活
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    测试访问令牌
    验证当前用户的令牌是否有效
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        当前用户信息
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    密码恢复
    发送密码重置邮件
    
    Args:
        email: 用户邮箱
        session: 数据库会话
        
    Returns:
        成功消息
        
    Raises:
        HTTPException: 当用户不存在时
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",  # 该邮箱的用户不存在
        )
    
    # 生成密码重置令牌和邮件
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")  # 密码恢复邮件已发送


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    重置密码
    使用重置令牌更新用户密码
    
    Args:
        session: 数据库会话
        body: 新密码请求体
        
    Returns:
        成功消息
        
    Raises:
        HTTPException: 当令牌无效、用户不存在或用户未激活时
    """
    # 验证重置令牌
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")  # 无效令牌
    
    # 获取用户并更新密码
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",  # 该邮箱的用户不存在
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")  # 用户未激活
    
    # 更新密码
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")  # 密码更新成功


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    密码恢复HTML内容
    仅超级用户可访问，用于预览密码重置邮件内容
    
    Args:
        email: 用户邮箱
        session: 数据库会话
        
    Returns:
        HTML格式的邮件内容
        
    Raises:
        HTTPException: 当用户不存在时
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",  # 该用户名的用户不存在
        )
    
    # 生成密码重置令牌和邮件内容
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
