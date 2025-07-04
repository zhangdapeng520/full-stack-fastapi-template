from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

# 创建数据库引擎
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# 确保在初始化数据库之前导入所有SQLModel模型（app.models）
# 否则，SQLModel可能无法正确初始化关系
# 更多详情：https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    """
    初始化数据库
    创建超级用户（如果不存在）
    """
    # 表应该通过Alembic迁移创建
    # 但如果您不想使用迁移，可以通过取消注释以下行来创建表
    # from sqlmodel import SQLModel

    # 这可以工作是因为模型已经从app.models导入并注册
    # SQLModel.metadata.create_all(engine)

    # 检查超级用户是否已存在
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    
    # 如果超级用户不存在，则创建
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
