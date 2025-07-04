# 开发指南

## 快速开始

### 环境要求
- Docker 和 Docker Compose
- Node.js 18+ (前端开发)
- Python 3.11+ (后端开发)

### 启动项目
```bash
# 克隆项目
git clone <your-repo-url>
cd full-stack-fastapi-template

# 启动所有服务
./start-local.sh
```

## 后端开发

### 项目结构
```
backend/
├── app/
│   ├── core/           # 核心配置
│   ├── api/           # API 路由
│   ├── models.py      # 数据模型
│   ├── crud.py        # 数据库操作
│   └── utils.py       # 工具函数
├── requirements.txt   # 依赖管理
└── Dockerfile        # 容器配置
```

### 添加新的 API 端点

#### 1. 创建数据模型
在 `app/models.py` 中添加新的模型：

```python
class NewModel(SQLModel, table=True):
    """新模型"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### 2. 添加 CRUD 操作
在 `app/crud.py` 中添加数据库操作：

```python
def create_new_model(*, session: Session, model_in: NewModelCreate) -> NewModel:
    """创建新模型"""
    db_obj = NewModel.model_validate(model_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_new_model(*, session: Session, model_id: uuid.UUID) -> NewModel | None:
    """根据ID获取模型"""
    return session.get(NewModel, model_id)
```

#### 3. 创建路由
在 `app/api/routes/` 下创建新的路由文件：

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import SessionDep, CurrentUser
from app import crud
from app.models import NewModel, NewModelCreate, NewModelPublic

router = APIRouter(tags=["new-model"])

@router.post("/", response_model=NewModelPublic)
def create_new_model(
    *,
    session: SessionDep,
    model_in: NewModelCreate,
    current_user: CurrentUser,
) -> Any:
    """创建新模型"""
    model = crud.create_new_model(session=session, model_in=model_in)
    return model

@router.get("/{model_id}", response_model=NewModelPublic)
def get_new_model(
    *,
    session: SessionDep,
    model_id: uuid.UUID,
) -> Any:
    """获取模型详情"""
    model = crud.get_new_model(session=session, model_id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
```

#### 4. 注册路由
在 `app/api/main.py` 中注册新路由：

```python
from app.api.routes import new_model

api_router.include_router(new_model.router, prefix="/new-models")
```

### 数据库迁移

#### 1. 创建迁移
```bash
cd backend
alembic revision --autogenerate -m "添加新模型"
```

#### 2. 应用迁移
```bash
alembic upgrade head
```

#### 3. 回滚迁移
```bash
alembic downgrade -1
```

### 测试

#### 1. 运行测试
```bash
cd backend
pytest
```

#### 2. 运行特定测试
```bash
pytest tests/api/routes/test_new_model.py -v
```

#### 3. 生成覆盖率报告
```bash
pytest --cov=app tests/
```

## 前端开发

### 项目结构
```
frontend/
├── src/
│   ├── components/     # React 组件
│   ├── hooks/         # 自定义 Hooks
│   ├── routes/        # 页面路由
│   └── client/        # API 客户端
├── package.json       # 依赖管理
└── vite.config.ts     # 构建配置
```

### 添加新页面

#### 1. 创建组件
在 `src/components/` 下创建新组件：

```tsx
import React from 'react';
import { Box, Heading, Text } from '@chakra-ui/react';

interface NewComponentProps {
  title: string;
  description?: string;
}

export const NewComponent: React.FC<NewComponentProps> = ({ 
  title, 
  description 
}) => {
  return (
    <Box p={6}>
      <Heading size="lg" mb={4}>{title}</Heading>
      {description && <Text>{description}</Text>}
    </Box>
  );
};
```

#### 2. 创建页面
在 `src/routes/` 下创建新页面：

```tsx
import React from 'react';
import { NewComponent } from '../components/NewComponent';

export const NewPage: React.FC = () => {
  return (
    <NewComponent 
      title="新页面" 
      description="这是一个新页面的描述" 
    />
  );
};
```

#### 3. 添加路由
在 `src/routes/_layout.tsx` 中添加路由：

```tsx
import { NewPage } from './new-page';

// 在路由配置中添加
{
  path: '/new-page',
  element: <NewPage />
}
```

### API 集成

#### 1. 使用生成的客户端
```tsx
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '../client';

// 查询数据
const { data, isLoading } = useQuery({
  queryKey: ['new-models'],
  queryFn: () => api.getNewModels()
});

// 创建数据
const createMutation = useMutation({
  mutationFn: (data: NewModelCreate) => api.createNewModel(data),
  onSuccess: () => {
    // 刷新查询
    queryClient.invalidateQueries({ queryKey: ['new-models'] });
  }
});
```

#### 2. 自定义 Hook
在 `src/hooks/` 下创建自定义 Hook：

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../client';

export const useNewModels = () => {
  return useQuery({
    queryKey: ['new-models'],
    queryFn: () => api.getNewModels()
  });
};

export const useCreateNewModel = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: NewModelCreate) => api.createNewModel(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['new-models'] });
    }
  });
};
```

### 样式和主题

#### 1. 使用 Chakra UI 组件
```tsx
import { 
  Box, 
  Button, 
  Input, 
  FormControl, 
  FormLabel 
} from '@chakra-ui/react';

export const FormComponent: React.FC = () => {
  return (
    <Box as="form" p={6}>
      <FormControl mb={4}>
        <FormLabel>名称</FormLabel>
        <Input placeholder="请输入名称" />
      </FormControl>
      <Button type="submit" colorScheme="blue">
        提交
      </Button>
    </Box>
  );
};
```

#### 2. 自定义主题
在 `src/theme/` 下修改主题配置：

```tsx
import { extendTheme } from '@chakra-ui/react';

export const theme = extendTheme({
  colors: {
    brand: {
      50: '#e3f2fd',
      500: '#2196f3',
      900: '#0d47a1',
    },
  },
  components: {
    Button: {
      defaultProps: {
        colorScheme: 'brand',
      },
    },
  },
});
```

## 调试技巧

### 后端调试

#### 1. 日志输出
```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.info("这是一条信息日志")
    logger.error("这是一条错误日志")
```

#### 2. 断点调试
在代码中添加断点：
```python
import pdb; pdb.set_trace()
```

#### 3. 查看 API 文档
访问 http://localhost:8000/docs 查看交互式 API 文档。

### 前端调试

#### 1. React DevTools
安装 React DevTools 浏览器扩展进行组件调试。

#### 2. 网络请求调试
使用浏览器开发者工具的 Network 面板查看 API 请求。

#### 3. 状态调试
使用 Redux DevTools 或 React Query DevTools 调试状态管理。

## 性能优化

### 后端优化

#### 1. 数据库查询优化
```python
# 使用 select 优化查询
from sqlmodel import select

# 避免 N+1 查询
users = session.exec(
    select(User).options(selectinload(User.items))
).all()
```

#### 2. 缓存策略
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_data(key: str):
    return expensive_operation(key)
```

#### 3. 异步处理
```python
from fastapi import BackgroundTasks

def send_email_background(email: str):
    # 异步发送邮件
    pass

@router.post("/send-email")
def send_email(
    background_tasks: BackgroundTasks,
    email: str
):
    background_tasks.add_task(send_email_background, email)
    return {"message": "Email sent"}
```

### 前端优化

#### 1. 代码分割
```tsx
import { lazy, Suspense } from 'react';

const LazyComponent = lazy(() => import('./LazyComponent'));

export const App = () => (
  <Suspense fallback={<div>加载中...</div>}>
    <LazyComponent />
  </Suspense>
);
```

#### 2. 图片优化
```tsx
import { Image } from '@chakra-ui/react';

<Image 
  src="/image.jpg" 
  loading="lazy"
  alt="描述"
/>
```

#### 3. 虚拟滚动
对于长列表，使用虚拟滚动：
```tsx
import { FixedSizeList as List } from 'react-window';

const VirtualList = ({ items }) => (
  <List
    height={400}
    itemCount={items.length}
    itemSize={50}
  >
    {({ index, style }) => (
      <div style={style}>
        {items[index]}
      </div>
    )}
  </List>
);
```

## 部署

### 本地测试部署
```bash
# 构建生产镜像
docker-compose -f docker-compose.yml build

# 启动生产环境
docker-compose -f docker-compose.yml up -d
```

### 生产环境部署
1. 配置环境变量
2. 设置数据库
3. 配置反向代理
4. 设置 SSL 证书
5. 配置监控和日志

## 常见问题

### 1. 数据库连接失败
- 检查 PostgreSQL 服务是否启动
- 验证数据库连接参数
- 确认网络连接

### 2. 前端构建失败
- 检查 Node.js 版本
- 清理 node_modules 重新安装
- 检查 TypeScript 类型错误

### 3. API 请求失败
- 检查 CORS 配置
- 验证认证令牌
- 查看服务器日志

### 4. 性能问题
- 使用数据库索引
- 实现缓存策略
- 优化前端打包

## 最佳实践

### 代码规范
- 使用 TypeScript 类型注解
- 遵循 PEP 8 (Python) 和 ESLint (JavaScript) 规范
- 编写单元测试
- 使用有意义的变量和函数名

### 安全考虑
- 验证所有用户输入
- 使用参数化查询防止 SQL 注入
- 实现适当的权限控制
- 定期更新依赖包

### 版本控制
- 使用语义化版本号
- 编写清晰的提交信息
- 创建功能分支
- 进行代码审查

### 文档维护
- 更新 API 文档
- 编写用户指南
- 记录架构决策
- 维护变更日志 