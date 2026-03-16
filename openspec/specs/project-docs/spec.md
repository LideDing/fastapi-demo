## ADDED Requirements

### Requirement: 中文 README 文档
项目根目录 SHALL 包含一个 `README.md` 文件，使用中文撰写，包含以下章节：项目简介、环境要求、快速开始、项目结构、常用命令、许可证。

#### Scenario: 新开发者阅读 README
- **WHEN** 开发者打开 `README.md`
- **THEN** 可以看到项目用途说明、环境依赖（Python 3.13+、uv）、从克隆到启动的完整步骤

#### Scenario: README 包含项目结构
- **WHEN** 开发者查看项目结构章节
- **THEN** 可以看到 `app/` 目录的分层说明（routers、services、models）

### Requirement: Makefile 开发命令封装
项目根目录 SHALL 包含一个 `Makefile`，提供以下 target：`install`（安装依赖）、`dev`（启动开发服务器）、`lint`（代码检查）、`format`（代码格式化）、`test`（运行测试）、`clean`（清理缓存文件）。

#### Scenario: 使用 make install 安装依赖
- **WHEN** 开发者运行 `make install`
- **THEN** 执行 `uv sync` 安装所有依赖到虚拟环境

#### Scenario: 使用 make dev 启动服务
- **WHEN** 开发者运行 `make dev`
- **THEN** 以 reload 模式启动 uvicorn 开发服务器

#### Scenario: 使用 make lint 检查代码
- **WHEN** 开发者运行 `make lint`
- **THEN** 执行 `uv run ruff check app/` 进行代码检查

#### Scenario: 使用 make format 格式化代码
- **WHEN** 开发者运行 `make format`
- **THEN** 执行 `uv run ruff format app/` 格式化代码

#### Scenario: 使用 make test 运行测试
- **WHEN** 开发者运行 `make test`
- **THEN** 执行 `uv run pytest` 运行测试套件

#### Scenario: 使用 make clean 清理缓存
- **WHEN** 开发者运行 `make clean`
- **THEN** 删除 `__pycache__`、`.pytest_cache`、`.ruff_cache` 等缓存目录
