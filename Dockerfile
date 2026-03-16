# ── Build stage: install dependencies with uv ──
FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

COPY app/ app/

# ── Runtime stage ──
FROM python:3.13-slim

RUN groupadd --system appuser && \
    useradd --system --gid appuser --no-create-home appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
