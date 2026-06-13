FROM python:3.11-slim AS base

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# App code
COPY packages/ packages/
COPY apps/ apps/
COPY skills/ skills/
COPY hooks/ hooks/

# Env defaults (override with docker-compose / .env)
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    LOG_LEVEL=INFO \
    SKILL_DIR=./skills

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "apps.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
