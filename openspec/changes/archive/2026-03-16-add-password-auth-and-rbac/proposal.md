## Why

当前系统只支持 OIDC 单点登录，缺乏本地用户名/密码认证能力，导致无法脱离外部 OIDC 提供方独立管理用户及权限。为了实现细粒度的用户权限管理（RBAC），需要引入本地用户账户体系、密码认证，并建立用户权限组机制，使两种认证方式共存、权限统一管控。

## What Changes

- 新增 PostgreSQL 数据库集成（asyncpg + SQLAlchemy async），存储用户及权限数据
- 新增本地用户注册与密码登录接口（`POST /auth/register`、`POST /auth/login`），使用 bcrypt 哈希存储密码
- 新增 JWT access token 签发，本地登录成功后返回 Bearer token
- OIDC 登录成功后同步将外部用户写入本地 users 表（以 `sub` 为唯一标识），并签发 JWT
- 新增用户权限组（`groups`）与用户-组关联（`user_groups`）数据模型
- 新增权限组管理接口（CRUD）供管理员使用
- 新增统一的 `require_auth` 依赖，支持 Session（OIDC 流程）和 Bearer JWT（密码登录流程）双通道校验
- 现有 `require_auth` 依赖升级以兼容两种认证方式，**BREAKING**：依赖返回的 `UserInfo` 增加 `id`、`groups` 字段

## Capabilities

### New Capabilities

- `local-user-auth`: 本地用户注册、密码登录、JWT 签发及校验，使用 PostgreSQL 存储用户信息
- `user-groups-rbac`: 用户权限组数据模型与管理接口，支持为用户分配组、按组进行权限校验

### Modified Capabilities

- `oidc-auth`: OIDC 回调成功后额外将用户同步写入本地 users 表并签发 JWT；`require_auth` 依赖扩展为双通道（Session + Bearer JWT）校验

## Impact

- **新增依赖**：`asyncpg`、`sqlalchemy[asyncio]`、`alembic`、`passlib[bcrypt]`、`python-jose`（或 `pyjwt`）
- **数据库**：PostgreSQL（host: localhost, port: 5433, user: postgres, password: mysecretpassword）
- **新文件**：`app/db/`（engine、session）、`app/models/user.py`（ORM 模型）、`app/routers/users.py`、`app/services/user_auth.py`、`app/services/groups.py`、Alembic migrations
- **改动文件**：`app/dependencies/auth.py`、`app/routers/oidc.py`、`app/services/auth.py`、`app/config.py`、`app/models/auth.py`
- **配置新增**：`APP_DB_URL`（数据库连接串）、`APP_JWT_SECRET`、`APP_JWT_EXPIRE_MINUTES`
