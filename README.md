# FastAPI Demo

生产级别的 FastAPI 应用程序框架，采用路由与业务逻辑分层设计。

## 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — Python 包管理器

## 快速开始

```bash
# 克隆项目
git clone https://github.com/lideding/fastapi-demo.git
cd fastapi-demo

# 安装依赖（自动创建虚拟环境）
uv sync

# 启动开发服务器
uv run python -m app.main

# 访问健康检查接口
curl http://127.0.0.1:8000/health
# 返回: {"status": "ok"}
```

## 项目结构

```
app/
├── main.py          # 应用工厂 create_app()、生命周期管理、CORS 中间件
├── config.py        # 配置管理（pydantic-settings，环境变量前缀 APP_）
├── routers/         # 路由层 — 仅定义 HTTP 端点，不包含业务逻辑
│   └── health.py    # 健康检查路由 GET /health
├── services/        # 服务层 — 业务逻辑函数
│   └── health.py    # 健康检查服务
└── models/          # 数据模型 — Pydantic 请求/响应 schema
    └── health.py    # HealthResponse 模型
```

**分层原则**: 每个功能域在 `routers/`、`services/`、`models/` 下各有对应文件，路由层调用服务层，服务层处理业务逻辑。

## 常用命令

| 命令 | 说明 |
|------|------|
| `uv sync` | 安装/更新所有依赖 |
| `uv run python -m app.main` | 启动开发服务器 |
| `uv run ruff check app/` | 代码检查 |
| `uv run ruff format app/` | 代码格式化 |
| `uv run pytest` | 运行测试 |

也可以使用 Makefile 快捷命令：

```bash
make install   # 安装依赖
make dev       # 启动开发服务器（reload 模式）
make lint      # 代码检查
make format    # 代码格式化
make test      # 运行测试
make clean     # 清理缓存文件
```

## 配置

通过环境变量配置，前缀为 `APP_`：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `APP_DEBUG` | `false` | 调试模式（启用时 uvicorn 自动重载） |
| `APP_HOST` | `0.0.0.0` | 监听地址 |
| `APP_PORT` | `8000` | 监听端口 |
| `APP_CORS_ORIGINS` | `["*"]` | 允许的 CORS 来源 |

## 许可证

[MIT](LICENSE)
