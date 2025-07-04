# 使用 Docker 搭建 PostgreSQL 数据库

本指南介绍如何在本地通过 Docker 快速搭建 PostgreSQL 数据库环境，适用于开发和测试场景。

---

## 一、拉取 PostgreSQL 镜像

所有平台通用：
```bash
docker pull postgres:17
```

---

## 二、启动 PostgreSQL 容器

### 1. Linux/macOS（bash）
```bash
docker run -d \
  --name app-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=changethis \
  -e POSTGRES_DB=app \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v app-postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart always \
  postgres:17
```

### 2. Windows PowerShell（推荐，支持多行）
```powershell
docker run -d `
  --name app-postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=changethis `
  -e POSTGRES_DB=app `
  -e PGDATA=/var/lib/postgresql/data/pgdata `
  -v app-postgres-data:/var/lib/postgresql/data `
  -p 5432:5432 `
  --restart always `
  postgres:17
```

### 3. Windows CMD（多行用 ^，或直接一行）
```cmd
docker run -d ^
  --name app-postgres ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=changethis ^
  -e POSTGRES_DB=app ^
  -e PGDATA=/var/lib/postgresql/data/pgdata ^
  -v app-postgres-data:/var/lib/postgresql/data ^
  -p 5432:5432 ^
  --restart always ^
  postgres:17
```

### 4. 一行命令（适用于所有平台，最简单）
```powershell
docker run -d --name app-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=changethis -e POSTGRES_DB=app -e PGDATA=/var/lib/postgresql/data/pgdata -v app-postgres-data:/var/lib/postgresql/data -p 5432:5432 --restart always postgres:17
```

### 参数说明
- `--name app-postgres`：容器名称，可自定义
- `-e POSTGRES_USER=postgres`：数据库用户名
- `-e POSTGRES_PASSWORD=changethis`：数据库密码
- `-e POSTGRES_DB=app`：默认数据库名
- `-e PGDATA=...`：数据目录，便于持久化
- `-v app-postgres-data:/var/lib/postgresql/data`：挂载数据卷，持久化数据
- `-p 5432:5432`：映射端口，左侧为主机端口
- `--restart always`：容器异常退出自动重启
- `postgres:17`：镜像版本

### 如果需要自定义网络（可选）
如果多个容器需要通信，可以先创建网络：
```powershell
# 创建网络
docker network create app-network

# 然后在启动命令中添加 --network app-network 参数
```

---

## 三、连接信息
- 主机：localhost
- 端口：5432
- 用户名：postgres
- 密码：changethis
- 数据库名：app

可通过 DBeaver、DataGrip、psql 等工具连接。

---

## 四、常用操作

### 查看容器状态
```powershell
docker ps -a
```

### 查看日志
```powershell
docker logs app-postgres
```

### 进入数据库容器
#### Linux/macOS:
```bash
docker exec -it app-postgres bash
psql -U postgres -d app
```
#### Windows（推荐 PowerShell）：
```powershell
docker exec -it app-postgres powershell
# 进入后可用
psql -U postgres -d app
```
或
```powershell
docker exec -it app-postgres cmd
```

### 停止容器
```powershell
docker stop app-postgres
```

### 启动容器
```powershell
docker start app-postgres
```

### 删除容器（不删除数据）
```powershell
docker rm app-postgres
```

### 删除数据卷（会丢失所有数据！）
```powershell
docker volume rm app-postgres-data
```

---

## 五、常见问题

### 1. 端口被占用
如 5432 端口被占用，可修改 `-p 5432:5432` 为其他端口，如 `-p 15432:5432`，连接时主机端口用 15432。

### 2. 数据丢失
如未挂载数据卷（`-v` 参数），容器删除后数据会丢失。务必使用数据卷持久化。

### 3. 权限问题
如遇到权限报错，可尝试以管理员身份运行 Docker Desktop。

### 4. 网络不存在错误
如果遇到 "network xxx not found" 错误，说明指定的网络不存在。建议使用默认网络，或先创建网络：
```powershell
docker network create app-network
```

---

## 六、环境变量建议

建议将数据库配置写入 `.env` 文件，便于统一管理：

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app
POSTGRES_PORT=5432
```

---

如有更多问题，请查阅 [PostgreSQL 官方文档](https://hub.docker.com/_/postgres) 或联系开发维护者。 