import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# 用户相关模型

# 用户基础属性
class UserBase(SQLModel):
    """用户基础模型，包含用户的基本信息"""
    email: EmailStr = Field(unique=True, index=True, max_length=255)  # 邮箱，唯一且建立索引
    is_active: bool = True  # 是否激活
    is_superuser: bool = False  # 是否为超级用户
    full_name: str | None = Field(default=None, max_length=255)  # 全名


# 创建用户时通过API接收的属性
class UserCreate(UserBase):
    """用户创建模型，包含密码字段"""
    password: str = Field(min_length=8, max_length=40)  # 密码，长度8-40位


class UserRegister(SQLModel):
    """用户注册模型"""
    email: EmailStr = Field(max_length=255)  # 邮箱
    password: str = Field(min_length=8, max_length=40)  # 密码
    full_name: str | None = Field(default=None, max_length=255)  # 全名


# 更新用户时通过API接收的属性，所有字段都是可选的
class UserUpdate(UserBase):
    """用户更新模型，所有字段可选"""
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    """用户自我更新模型"""
    full_name: str | None = Field(default=None, max_length=255)  # 全名
    email: EmailStr | None = Field(default=None, max_length=255)  # 邮箱


class UpdatePassword(SQLModel):
    """密码更新模型"""
    current_password: str = Field(min_length=8, max_length=40)  # 当前密码
    new_password: str = Field(min_length=8, max_length=40)  # 新密码


# 数据库模型，数据库表名从类名推断
class User(UserBase, table=True):
    """用户数据库模型"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # 用户ID，主键
    hashed_password: str  # 哈希密码
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)  # 用户拥有的项目，级联删除


# 通过API返回的属性，id始终必需
class UserPublic(UserBase):
    """用户公开信息模型"""
    id: uuid.UUID  # 用户ID


class UsersPublic(SQLModel):
    """用户列表公开信息模型"""
    data: list[UserPublic]  # 用户列表
    count: int  # 用户总数


# 项目相关模型

# 项目基础属性
class ItemBase(SQLModel):
    """项目基础模型"""
    title: str = Field(min_length=1, max_length=255)  # 标题，长度1-255位
    description: str | None = Field(default=None, max_length=255)  # 描述，可选


# 创建项目时接收的属性
class ItemCreate(ItemBase):
    """项目创建模型"""
    pass


# 更新项目时接收的属性
class ItemUpdate(ItemBase):
    """项目更新模型"""
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# 数据库模型，数据库表名从类名推断
class Item(ItemBase, table=True):
    """项目数据库模型"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # 项目ID，主键
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )  # 所有者ID，外键关联用户表
    owner: User | None = Relationship(back_populates="items")  # 所有者关系


# 通过API返回的属性，id始终必需
class ItemPublic(ItemBase):
    """项目公开信息模型"""
    id: uuid.UUID  # 项目ID
    owner_id: uuid.UUID  # 所有者ID


class ItemsPublic(SQLModel):
    """项目列表公开信息模型"""
    data: list[ItemPublic]  # 项目列表
    count: int  # 项目总数


# 通用消息模型
class Message(SQLModel):
    """通用消息模型"""
    message: str  # 消息内容


# 包含访问令牌的JSON载荷
class Token(SQLModel):
    """令牌模型"""
    access_token: str  # 访问令牌
    token_type: str = "bearer"  # 令牌类型


# JWT令牌内容
class TokenPayload(SQLModel):
    """令牌载荷模型"""
    sub: str | None = None  # 主题（通常是用户ID）


class NewPassword(SQLModel):
    """新密码模型"""
    token: str  # 重置令牌
    new_password: str = Field(min_length=8, max_length=40)  # 新密码
