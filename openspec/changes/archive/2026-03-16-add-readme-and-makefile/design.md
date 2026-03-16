## Context

项目已有完整的 FastAPI 应用框架（app/ 目录、pyproject.toml、uv 管理依赖），但缺少面向开发者的入口文档和命令快捷方式。

## Goals / Non-Goals

**Goals:**
- 提供中文 README，让新开发者 5 分钟内可以启动项目
- 通过 Makefile 统一常用命令，避免记忆 `uv run ...` 前缀

**Non-Goals:**
- 英文文档（后续需要时再加）
- CI/CD 相关的 Makefile target
- Docker 构建命令

## Decisions

### 1. README 用中文撰写
用户明确要求中文文档。README 包含：项目简介、环境要求、快速开始、项目结构、常用命令。

### 2. Makefile 封装 uv 命令
Makefile target 直接调用 `uv run ...`，保持与 pyproject.toml 定义的工具链一致。target 包括：`install`、`dev`、`lint`、`format`、`test`、`clean`。

## Risks / Trade-offs

- **[Makefile 跨平台]** → Windows 用户可能没有 make。Mitigation: README 中同时列出原始命令。
