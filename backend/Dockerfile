# Newer uv image with Python 3.12 on Debian trixie-slim
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Prevent Python from writing .pyc files and enable cleaner logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV UV_LINK_MODE=copy
ENV UV_PYTHON=/usr/local/bin/python3

# Set working directory
WORKDIR /app

# Copy dependency metadata first for better build cache usage
COPY pyproject.toml uv.lock* ./

# Install only production dependencies
RUN uv sync --locked --no-dev --no-install-project

# Copy application code
COPY src ./src

# Install the project itself
RUN uv sync --locked --no-dev

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
