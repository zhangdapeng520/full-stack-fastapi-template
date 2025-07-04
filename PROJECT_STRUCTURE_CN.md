# 项目结构说明

## 整体架构

这是一个基于 FastAPI + React 的全栈项目模板，采用前后端分离架构。

```
full-stack-fastapi-template/
├── backend/                 # 后端代码目录
├── frontend/               # 前端代码目录
├── scripts/                # 脚本文件
│   ├── start_postgres.ps1  # PostgreSQL启动脚本
│   ├── stop_postgres.ps1   # PostgreSQL停止脚本
│   └── clean_postgres.ps1  # PostgreSQL清理脚本
├── start-local.sh          # Linux/Mac 启动脚本
├── start-local.bat         # Windows 启动脚本
└── README_CN.md           # 中文说明文档
```

## 后端结构 (backend/)

### 核心模块

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── models.py            # 数据模型定义
│   ├── crud.py              # 数据库操作函数
│   ├── utils.py             # 工具函数
│   ├── core/                # 核心配置模块
│   │   ├── __init__.py
│   │   ├── config.py        # 应用配置
│   │   ├── db.py           # 数据库配置
│   │   └── security.py     # 安全相关函数
│   ├── api/                # API 路由模块
│   │   ├── __init__.py
│   │   ├── main.py         # API 路由器
│   │   ├── deps.py         # 依赖注入
│   │   └── routes/         # 具体路由
│   │       ├── __init__.py
│   │       ├── login.py    # 登录认证
│   │       ├── users.py    # 用户管理
│   │       ├── items.py    # 项目管理
│   │       ├── utils.py    # 工具接口
│   │       └── private.py  # 私有接口（仅开发环境）
│   ├── alembic/            # 数据库迁移
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/       # 迁移文件
│   ├── email-templates/    # 邮件模板
│   └── tests/              # 测试代码
├── Dockerfile              # 后端容器配置
├── requirements.txt        # Python 依赖
├── pyproject.toml         # 项目配置
└── alembic.ini           # Alembic 配置
```

### 核心文件说明

#### 1. 配置管理 (core/config.py)
- **Settings 类**: 管理所有环境变量和配置
- **数据库配置**: PostgreSQL 连接参数
- **安全配置**: JWT 密钥、令牌过期时间
- **邮件配置**: SMTP 服务器设置
- **CORS 配置**: 跨域访问控制

#### 2. 数据模型 (models.py)
- **User 相关模型**: 用户基础信息、创建、更新、公开信息
- **Item 相关模型**: 项目基础信息、创建、更新、公开信息
- **认证模型**: Token、TokenPayload、密码更新等

#### 3. 数据库操作 (crud.py)
- **用户操作**: 创建、更新、查询、认证
- **项目操作**: 创建项目
- **密码处理**: 哈希化、验证

#### 4. API 路由 (api/routes/)
- **login.py**: 登录认证、密码重置
- **users.py**: 用户管理 CRUD
- **items.py**: 项目管理 CRUD
- **utils.py**: 工具接口
- **private.py**: 私有接口（测试用）

#### 5. 依赖注入 (api/deps.py)
- **数据库会话**: 为每个请求提供数据库连接
- **用户认证**: JWT 令牌验证
- **权限控制**: 超级用户权限检查

## 前端结构 (frontend/)

### 技术栈
- **React 18**: 前端框架
- **TypeScript**: 类型安全
- **Vite**: 构建工具
- **Chakra UI**: 组件库
- **React Router**: 路由管理
- **TanStack Query**: 数据获取

### 目录结构

```
frontend/
├── src/
│   ├── main.tsx            # 应用入口
│   ├── client/             # API 客户端（自动生成）
│   ├── components/         # React 组件
│   │   ├── Admin/         # 管理员组件
│   │   ├── Common/        # 通用组件
│   │   ├── Items/         # 项目相关组件
│   │   ├── Pending/       # 待处理组件
│   │   ├── UserSettings/  # 用户设置组件
│   │   └── ui/            # UI 基础组件
│   ├── hooks/             # 自定义 Hooks
│   ├── routes/            # 页面路由
│   ├── theme/             # 主题配置
│   └── utils.ts           # 工具函数
├── public/                # 静态资源
├── tests/                 # 测试文件
├── Dockerfile             # 前端容器配置
├── package.json           # Node.js 依赖
└── vite.config.ts         # Vite 配置
```

### 组件说明

#### 1. 通用组件 (Common/)
- **Navbar.tsx**: 导航栏
- **Sidebar.tsx**: 侧边栏
- **UserMenu.tsx**: 用户菜单
- **NotFound.tsx**: 404 页面

#### 2. 管理员组件 (Admin/)
- **AddUser.tsx**: 添加用户
- **EditUser.tsx**: 编辑用户
- **DeleteUser.tsx**: 删除用户

#### 3. 项目管理 (Items/)
- **AddItem.tsx**: 添加项目
- **EditItem.tsx**: 编辑项目
- **DeleteItem.tsx**: 删除项目

#### 4. 用户设置 (UserSettings/)
- **UserInformation.tsx**: 用户信息
- **ChangePassword.tsx**: 修改密码
- **DeleteAccount.tsx**: 删除账户

## 数据库设计

### 用户表 (user)
```sql
CREATE TABLE user (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);
```

### 项目表 (item)
```sql
CREATE TABLE item (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    owner_id UUID NOT NULL REFERENCES user(id) ON DELETE CASCADE
);
```

## 部署配置

### Docker Compose
- **scripts/start_postgres.ps1**: PostgreSQL 启动脚本
- **scripts/stop_postgres.ps1**: PostgreSQL 停止脚本
- **scripts/clean_postgres.ps1**: PostgreSQL 清理脚本

### 环境变量
- **.env**: 环境变量配置
- **SECRET_KEY**: JWT 密钥
- **POSTGRES_***: 数据库配置
- **SMTP_***: 邮件服务配置

## 开发流程

### 1. 本地开发
```bash
# 启动所有服务
./start-local.sh

# 或使用 Windows 脚本
start-local.bat
```

### 2. API 开发
- 后端服务运行在 http://localhost:8000
- API 文档访问 http://localhost:8000/docs
- 数据库运行在 localhost:5432

### 3. 前端开发
- 前端服务运行在 http://localhost:5173
- 支持热重载
- 自动生成 API 客户端

### 4. 数据库迁移
```bash
# 创建迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head
```

## 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm test
```

### E2E 测试
```bash
cd frontend
npm run test:e2e
```

## 本地化优化

### 1. 镜像源配置
- 后端使用阿里云 PyPI 镜像
- 前端使用阿里云 npm 镜像
- 加速依赖下载

### 2. 简化配置
- 移除复杂的 Traefik 配置
- 专注于核心功能开发
- 提供简单的启动脚本

### 3. 依赖管理
- 使用 requirements.txt 替代 uv
- 补充所有必需依赖
- 修复启动命令

## 扩展建议

### 1. 功能扩展
- 添加手机号登录
- 集成短信验证码
- 支持第三方登录（微信、QQ等）
- 添加文件上传功能

### 2. 性能优化
- 添加 Redis 缓存
- 实现数据库连接池
- 前端代码分割
- 图片懒加载

### 3. 安全增强
- 添加请求频率限制
- 实现 CSRF 保护
- 添加 SQL 注入防护
- 实现审计日志

### 4. 监控运维
- 集成日志系统
- 添加性能监控
- 实现健康检查
- 配置告警机制 