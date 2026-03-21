FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY backend/ backend/
COPY frontend/ frontend/

ENV PORT=8080

EXPOSE 8080

# Run from backend/ directory since imports are relative
WORKDIR /app/backend
CMD ["uv", "run", "--project", "/app", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
