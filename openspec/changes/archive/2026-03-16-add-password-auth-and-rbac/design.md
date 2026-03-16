## Context

当前应用已通过 Authlib + httpx 实现了完整的 OIDC 授权码流程，用户信息存储在服务端 Session（由 `starlette-session` 提供）中。认证统一由 `app/dependencies/auth.py` 的 `require_auth` 处理。

本次变更在此基础上引入：
1. **本地用户账户体系** —— PostgreSQL 存储用户、密码哈希、权限组
2. **密码认证 + JWT** —— `POST /auth/login` 校验密码并签发短期 JWT
3. **RBAC 权限组** —— `groups` / `user_groups` 表，管理员通过 API 管理
4. **统一认证依赖** —— `require_auth` 同时支持 Session（OIDC）与 Bearer JWT（密码登录）

数据库连接：`postgresql+asyncpg://postgres:mysecretpassword@localhost:5433/fastapi_demo`

## Goals / Non-Goals

**Goals:**
- 密码登录与 OIDC 登录并存，共享同一套用户表和权限组
- JWT 无状态，密码登录后端无需额外 session
- 数据库模型通过 Alembic 管理迁移，可复现
- 权限组 CRUD API，支持将用户加入/移出组
- `require_auth` 依赖返回包含 `groups` 的增强 `UserInfo`

**Non-Goals:**
- 不实现前端页面（仅 REST JSON API）
- 不实现细粒度 permission/role（仅组级别），未来可扩展
- 不替换 OIDC 流程中的 Session 机制（保持向后兼容）
- 不实现 refresh token

## Decisions

### 1. ORM：SQLAlchemy 2.x async + asyncpg

**选择理由**：项目已是 async FastAPI；asyncpg 是 PostgreSQL 性能最佳的 async 驱动；SQLAlchemy 2 的 `async_sessionmaker` 与 FastAPI 依赖注入模式完美契合。

**备选**：`databases` + raw SQL —— 灵活但缺乏 ORM 抽象，维护成本高。

### 2. 密码哈希：passlib + bcrypt

**选择理由**：bcrypt 是密码存储的行业标准，passlib 提供简洁 API 且支持未来算法迁移。

**备选**：`hashlib` SHA-256 —— 不适合密码存储（无 salt stretch）。

### 3. JWT：python-jose（HS256）

**选择理由**：轻量，与 FastAPI 文档示例一致；HS256 适合单服务内部签发/验证场景。Payload 包含 `sub`（user_id）、`exp`。

**备选**：PyJWT —— 同等能力，两者均可，选 python-jose 保持与 FastAPI 生态一致。

### 4. 认证双通道：Session 优先，Bearer JWT 次之

`require_auth` 依赖检测顺序：
1. `Authorization: Bearer <token>` header → 解码 JWT → 查数据库用户+组
2. Session `user` key → 查数据库用户+组（OIDC 流程）
3. 均无 → 302 重定向（浏览器流程）或 401（API 流程，依据 `Accept` header 判断）

**理由**：保持现有 OIDC 浏览器流程完全不变；JWT 路径为 API 客户端提供无状态访问。

### 5. OIDC 回调同步本地用户

OIDC 回调成功后，以 `sub` 为 `external_id` 在 `users` 表中 upsert 用户（`INSERT ... ON CONFLICT DO UPDATE`），并将 `user_id` 写入 Session，同时可选签发 JWT（存入 Session 供后续 API 调用携带）。

**理由**：统一用户表，权限组管理不需要区分认证来源。

### 6. 数据库 Session 注入

使用 `async_sessionmaker` 工厂 + FastAPI `Depends(get_db)` 注入，每请求一个 session，请求结束自动 commit/rollback/close。

## Risks / Trade-offs

- **bcrypt 速度** → 登录接口响应约 100-300ms，属正常范围；可通过 `rounds` 参数调节
- **JWT 无法主动吊销** → 短期过期（默认 60 分钟）+未来可加 token 黑名单表缓解；本期不实现
- **数据库单点** → 本地开发场景可接受；生产应配置连接池上限和重试
- **Session + JWT 双轨并行复杂度** → 通过清晰的依赖层级（`require_auth` 单入口）封装，路由层无感知

## Migration Plan

1. `uv add sqlalchemy asyncpg alembic passlib[bcrypt] python-jose[cryptography]`
2. 配置 `app/db/engine.py`（async engine + sessionmaker）
3. 定义 ORM 模型：`users`、`groups`、`user_groups`
4. `alembic init alembic` + 编写初始 migration
5. `alembic upgrade head` 建表
6. 实现服务层、路由层、依赖更新
7. 更新 `.env.example` 添加 `APP_DB_URL`、`APP_JWT_SECRET`

**回滚**：直接 `alembic downgrade base`；新增路由不影响现有端点。

## Open Questions

- JWT 过期时间默认 60 分钟，是否需要可配置？（建议通过 `APP_JWT_EXPIRE_MINUTES` 环境变量）
- 是否需要邮箱验证？（本期不实现，字段预留 `email` 列）
- 管理员权限如何引导？（建议首个注册用户自动加入 `admin` 组，或通过环境变量指定）
