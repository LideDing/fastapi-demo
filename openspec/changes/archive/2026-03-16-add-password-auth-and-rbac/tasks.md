## 1. 依赖与配置

- [x] 1.1 添加依赖：`uv add sqlalchemy[asyncio] asyncpg alembic "passlib[bcrypt]" "python-jose[cryptography]"`
- [x] 1.2 在 `app/config.py` 中新增 `APP_DB_URL`、`APP_JWT_SECRET`、`APP_JWT_EXPIRE_MINUTES`（默认 60）配置项
- [x] 1.3 更新 `.env.example`（若存在）或在 README 中记录新增环境变量

## 2. 数据库引擎与 Session 工厂

- [x] 2.1 创建 `app/db/__init__.py`（空）
- [x] 2.2 创建 `app/db/engine.py`：使用 `create_async_engine` + `async_sessionmaker`，读取 `APP_DB_URL`
- [x] 2.3 创建 `app/db/deps.py`：提供 `get_db` FastAPI 依赖（`AsyncSession` 生成器）

## 3. ORM 模型

- [x] 3.1 创建 `app/db/models.py`：定义 `Base = DeclarativeBase()`
- [x] 3.2 在 `app/db/models.py` 中定义 `User` 模型（`id` UUID PK、`username`、`email`、`hashed_password`、`external_id`、`is_active`、`created_at`）
- [x] 3.3 在 `app/db/models.py` 中定义 `Group` 模型（`id` UUID PK、`name` unique、`description`、`created_at`）
- [x] 3.4 在 `app/db/models.py` 中定义 `UserGroup` 关联模型（`user_id` FK、`group_id` FK，复合 PK）

## 4. Alembic 迁移

- [x] 4.1 运行 `alembic init alembic` 初始化迁移目录，配置 `alembic.ini` 使用 `APP_DB_URL`（或 env_db_url 方式）
- [x] 4.2 编写初始 migration（`alembic revision --autogenerate -m "init users groups"`）并检查生成内容
- [x] 4.3 运行 `alembic upgrade head` 建表，验证表结构

## 5. Pydantic 请求/响应模型

- [x] 5.1 在 `app/models/auth.py` 中新增 `RegisterRequest`（`username`, `password` ≥ 8 chars, `email` optional）、`RegisterResponse`（`user_id`, `username`）
- [x] 5.2 在 `app/models/auth.py` 中新增 `LoginRequest`（`username`, `password`）、`TokenResponse`（`access_token`, `token_type`）
- [x] 5.3 更新 `app/models/auth.py` 中的 `UserInfo`：新增 `id`（UUID str）、`groups`（`list[str]`，默认 `[]`）字段

## 6. 本地用户认证服务

- [x] 6.1 创建 `app/services/user_auth.py`：实现 `create_user(db, username, password, email)` — bcrypt 哈希 + INSERT，首个用户自动加入 `admin` 组
- [x] 6.2 在 `app/services/user_auth.py` 中实现 `authenticate_user(db, username, password)` — 查用户 + bcrypt verify，返回 `User` 或 `None`
- [x] 6.3 在 `app/services/user_auth.py` 中实现 `create_access_token(user_id)` — HS256 JWT，payload 含 `sub` 和 `exp`
- [x] 6.4 在 `app/services/user_auth.py` 中实现 `get_user_with_groups(db, user_id)` — 查 User + join UserGroup + Group，返回 `(User, list[str])`
- [x] 6.5 在 `app/services/user_auth.py` 中实现 `upsert_oidc_user(db, sub, name)` — `INSERT ... ON CONFLICT(external_id) DO UPDATE`，返回 `User`

## 7. 权限组服务

- [x] 7.1 创建 `app/services/groups.py`：实现 `list_groups(db)`、`create_group(db, name, description)`、`get_group(db, group_id)`、`delete_group(db, group_id)`
- [x] 7.2 在 `app/services/groups.py` 中实现 `add_member(db, group_id, user_id)` 和 `remove_member(db, group_id, user_id)`
- [x] 7.3 在 `app/services/groups.py` 中实现 `ensure_admin_group(db)` — 若 `admin` 组不存在则创建

## 8. 认证依赖更新

- [x] 8.1 更新 `app/dependencies/auth.py`：`require_auth` 先检查 `Authorization: Bearer` header（解码 JWT → 查 DB），再检查 Session `user_id`（查 DB），均无则按请求类型返回 302/401
- [x] 8.2 新增 `require_admin` 依赖：调用 `require_auth` 后校验 `"admin" in user.groups`，否则返回 HTTP 403

## 9. 本地认证路由

- [x] 9.1 在 `app/routers/oidc.py`（或新建 `app/routers/local_auth.py`）中添加 `POST /auth/register` 路由，调用 `create_user`，返回 201
- [x] 9.2 在同文件中添加 `POST /auth/login` 路由，调用 `authenticate_user` + `create_access_token`，返回 `TokenResponse`

## 10. OIDC 回调更新

- [x] 10.1 更新 `app/routers/oidc.py` 的 `callback` 路由：成功后调用 `upsert_oidc_user`，将 `user_id` 写入 Session（替换原 `sub`/`name` 存储方式）

## 11. 权限组路由

- [x] 11.1 创建 `app/routers/groups.py`：`GET /groups`、`POST /groups`，使用 `require_admin` 依赖
- [x] 11.2 在 `app/routers/groups.py` 中添加 `GET /groups/{group_id}`、`DELETE /groups/{group_id}`
- [x] 11.3 在 `app/routers/groups.py` 中添加 `POST /groups/{group_id}/members`、`DELETE /groups/{group_id}/members/{user_id}`
- [x] 11.4 创建 `app/models/groups.py`：定义 `GroupCreate`、`GroupResponse`、`MemberAdd` 等 Pydantic 模型

## 12. 应用启动集成

- [x] 12.1 在 `app/main.py` 的 lifespan 中调用 `ensure_admin_group(db)` 确保 admin 组存在
- [x] 12.2 在 `app/main.py` 中注册 `groups` router

## 13. 测试

- [x] 13.1 为 `POST /auth/register` 编写测试：成功注册、重复用户名、密码过短
- [x] 13.2 为 `POST /auth/login` 编写测试：成功登录返回 token、错误密码返回 401
- [x] 13.3 为 JWT 认证依赖编写测试：有效 token、过期 token、无效签名
- [x] 13.4 为权限组 API 编写测试：admin 可操作、非 admin 返回 403
