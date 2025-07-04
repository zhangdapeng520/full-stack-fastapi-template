import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """
    创建新用户
    
    Args:
        session: 数据库会话
        user_create: 用户创建数据
        
    Returns:
        创建的用户对象
    """
    # 创建用户对象，将密码哈希化
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    """
    更新用户信息
    
    Args:
        session: 数据库会话
        db_user: 数据库中的用户对象
        user_in: 更新的用户数据
        
    Returns:
        更新后的用户对象
    """
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    # 如果包含密码字段，需要哈希化
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    根据邮箱获取用户
    
    Args:
        session: 数据库会话
        email: 用户邮箱
        
    Returns:
        用户对象，如果不存在则返回None
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """
    用户身份验证
    
    Args:
        session: 数据库会话
        email: 用户邮箱
        password: 用户密码
        
    Returns:
        验证成功的用户对象，验证失败返回None
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    """
    创建新项目
    
    Args:
        session: 数据库会话
        item_in: 项目创建数据
        owner_id: 所有者ID
        
    Returns:
        创建的项目对象
    """
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
