# 全栈 FastAPI 模板

<a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3ATest" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test/badge.svg" alt="测试状态"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/full-stack-fastapi-template.svg" alt="代码覆盖率"></a>

## 技术栈和功能特性

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) - Python 后端 API 框架
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) - Python SQL 数据库交互（ORM）
    - 🔍 [Pydantic](https://docs.pydantic.dev) - 数据验证和配置管理
    - 💾 [PostgreSQL](https://www.postgresql.org) - SQL 数据库
- 🚀 [React](https://react.dev) - 前端框架
    - 💃 使用 TypeScript、Hooks、Vite 等现代前端技术栈
    - 🎨 [Chakra UI](https://chakra-ui.com) - 前端组件库
    - 🤖 自动生成的前端客户端
    - 🧪 [Playwright](https://playwright.dev) - 端到端测试
    - 🦇 暗色模式支持
- 🐋 [Docker](https://www.docker.com) - 容器化部署
- 🔒 默认安全的密码哈希
- 🔑 JWT（JSON Web Token）身份认证
- 📫 基于邮件的密码重置
- ✅ 使用 [Pytest](https://pytest.org) 进行测试
- 🏭 基于 GitHub Actions 的 CI（持续集成）和 CD（持续部署）

### 仪表板登录界面

[![API 文档](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 仪表板 - 管理员

[![API 文档](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 仪表板 - 创建用户

[![API 文档](img/dashboard-create.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 仪表板 - 项目管理

[![API 文档](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 仪表板 - 用户设置

[![API 文档](img/dashboard-user-settings.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 仪表板 - 暗色模式

[![API 文档](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)

### 交互式 API 文档

[![API 文档](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)

## 如何使用

您可以直接 **fork 或克隆** 这个仓库并直接使用。

✨ 开箱即用 ✨

### 本地开发快速启动

1. **克隆项目**
```bash
git clone <your-repo-url>
cd full-stack-fastapi-template
```

2. **启动 PostgreSQL 数据库**
```powershell
# Windows PowerShell
.\scripts\start_postgres.ps1

# 或者手动启动
docker run -d --name app-postgres --network app-network -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=changethis -e POSTGRES_DB=app -v app-postgres-data:/var/lib/postgresql/data --restart always postgres:17
```

3. **启动后端服务**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **启动前端服务**
```bash
cd frontend
npm install
npm run dev
```

5. **访问服务**
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 数据库: localhost:5432

### 如何使用私有仓库

如果您想要一个私有仓库，GitHub 不允许简单地 fork 它，因为它不允许更改 fork 的可见性。

但您可以执行以下操作：

- 创建一个新的 GitHub 仓库，例如 `my-full-stack`
- 手动克隆此仓库，使用您想要的项目名称，例如 `my-full-stack`：

```bash
git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
```

- 进入新目录：

```bash
cd my-full-stack
```

- 将新的 origin 设置为您的新仓库，从 GitHub 界面复制，例如：

```bash
git remote set-url origin git@github.com:octocat/my-full-stack.git
```

- 将此仓库添加为另一个 "remote"，以便稍后获取更新：

```bash
git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
```

- 将代码推送到您的新仓库：

```bash
git push -u origin master
```

### 从原始模板更新

克隆仓库并进行更改后，您可能希望从原始模板获取最新更改。

- 确保您已将原始仓库添加为 remote，您可以使用以下命令检查：

```bash
git remote -v

origin    git@github.com:octocat/my-full-stack.git (fetch)
origin    git@github.com:octocat/my-full-stack.git (push)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
```

- 拉取最新更改而不合并：

```bash
git pull --no-commit upstream master
```

这将从此模板下载最新更改而不提交它们，这样您可以在提交前检查一切是否正确。

- 如果有冲突，在编辑器中解决它们。

- 完成后，提交更改：

```bash
git merge --continue
```

### 配置

然后您可以更新 `.env` 文件中的配置来自定义您的配置。

在部署之前，请确保至少更改以下值：

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

您可以（并且应该）从密钥中将这些作为环境变量传递。

阅读 [deployment.md](./deployment.md) 文档了解更多详细信息。

### 生成密钥

`.env` 文件中的一些环境变量的默认值为 `changethis`。

您必须用密钥更改它们，要生成密钥，您可以运行以下命令：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

复制内容并将其用作密码/密钥。再次运行以生成另一个安全密钥。

## 如何使用 - 使用 Copier 的替代方案

此仓库还支持使用 [Copier](https://copier.readthedocs.io) 生成新项目。

它将复制所有文件，询问您配置问题，并使用您的答案更新 `.env` 文件。

### 安装 Copier

您可以使用以下命令安装 Copier：

```bash
pip install copier
```

或者更好的是，如果您有 [`pipx`](https://pipx.pypa.io/)，您可以使用以下命令运行：

```bash
pipx install copier
```

**注意**：如果您有 `pipx`，安装 copier 是可选的，您可以直接运行它。

### 使用 Copier 生成项目

决定新项目目录的名称，您将在下面使用它。例如，`my-awesome-project`。

转到将成为您项目父目录的目录，并使用您的项目名称运行命令：

```bash
copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

如果您有 `pipx` 并且没有安装 `copier`，您可以直接运行：

```bash
pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

**注意** `--trust` 选项是必需的，以便能够执行更新 `.env` 文件的 [post-creation script](https://github.com/fastapi/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py)。

### 输入变量

Copier 会询问您一些数据，您可能希望在生成项目之前准备好。

但不用担心，您可以在 `.env` 文件中稍后更新任何内容。

## 本地化优化

本项目已针对国内网络环境进行了优化：

### 🚀 国内镜像源配置
- 后端使用阿里云 PyPI 镜像源
- 前端使用阿里云 npm 镜像源
- 加速依赖下载和构建过程

### 📦 简化的部署配置
- 移除了复杂的 Docker Compose 配置
- 提供了独立的 PostgreSQL 启动脚本
- 专注于核心功能，简化部署流程

### 🔧 数据库管理脚本
- `scripts/start_postgres.ps1` - 启动 PostgreSQL 容器
- `scripts/stop_postgres.ps1` - 停止 PostgreSQL 容器
- `scripts/clean_postgres.ps1` - 清理容器和数据卷

### 🎯 快速开始
1. 运行 PostgreSQL 启动脚本
2. 启动后端和前端服务
3. 访问 http://localhost:8000/docs 查看API文档
4. 开始您的开发工作

## 项目结构

```
full-stack-fastapi-template/
├── backend/                 # 后端代码
│   ├── app/                # 应用代码
│   │   ├── api/           # API路由
│   │   ├── core/          # 核心配置
│   │   ├── models.py      # 数据模型
│   │   └── main.py        # 应用入口
│   ├── Dockerfile         # 后端Docker配置
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端代码
│   ├── src/              # 源代码
│   ├── Dockerfile        # 前端Docker配置
│   └── package.json      # Node.js依赖
├── scripts/               # 脚本文件
│   ├── start_postgres.ps1 # PostgreSQL启动脚本
│   ├── stop_postgres.ps1  # PostgreSQL停止脚本
│   └── clean_postgres.ps1 # PostgreSQL清理脚本
└── .env                   # 环境配置文件
```

## 贡献

欢迎提交 Issue 和 Pull Request！

根据配置文件，您可以使用以下默认账户登录：
邮箱: admin@example.com
密码: changethis

## 许可证

本项目采用 MIT 许可证。 