# syntax=docker/dockerfile:1

# Build stage - base Python image
FROM python:3.13-slim AS base

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set uv to use system Python
ENV UV_SYSTEM_PYTHON=1

# Copy dependency files
COPY pyproject.toml ./

# Development stage
FROM base AS development

# Install all dependencies including dev
RUN uv pip install -e ".[dev]"

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment
ENV APP_ENV=development
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=auto

# Run with hot-reload
CMD ["streamlit", "run", "app/main.py", "--server.runOnSave=true"]

# Production stage
FROM base AS production

# Install only production dependencies
RUN uv pip install .

# Copy only necessary application files
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/

# Create non-root user
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app

USER streamlit

# Expose both HTTP and HTTPS ports
EXPOSE 8501 443

# Set environment
ENV APP_ENV=production
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app/main.py"]
