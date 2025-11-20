# Docker Streamlit Scaffold Implementation Plan

---
date: 2025-11-20T22:33:00+0000
author: Glenn Cueto
git_commit: not-initialized
branch: not-initialized
repository: gc-streamlit
topic: "Docker-based Python Streamlit scaffold with multi-page routing"
tags: [docker, streamlit, python, devops, scaffold, multi-page]
status: ready
last_updated: 2025-11-20T22:54:54+0000
last_updated_by: Glenn Cueto
last_updated_note: "Added multi-page routing with About page to demonstrate Streamlit navigation"
---

## Overview

Create a production-ready Docker-based scaffold for a Python Streamlit application with:
- Python 3.13
- uv for fast dependency management
- Multi-page routing (home page + about page)
- Multi-stage Docker builds for optimal image sizes
- Development environment with hot-reload
- Production environment with SSL/HTTPS support
- Code quality tools (linting, formatting, testing)
- Helper scripts for common Docker operations

## Current State Analysis

The `/Users/glenn/htdocs/gc-streamlit` directory is currently empty. This is a greenfield project with no existing code, dependencies, or configuration.

**Key Constraints:**
- Not yet a git repository
- No existing Python environment
- No Docker configuration

## Desired End State

A fully functional Docker-based Streamlit development environment where:

1. **Development workflow:**
   - Run `./dock dev` to start development environment with hot-reload
   - Code changes automatically reflect in running container
   - Access Streamlit app at http://localhost:8501

2. **Production deployment:**
   - Run `./dock prod` to start production environment
   - SSL/HTTPS configured on port 443
   - Optimized, minimal Docker image size

3. **Code quality:**
   - Run `./dock test` to execute pytest test suite
   - Run `./dock lint` to check code quality
   - Pre-configured with ruff for fast linting/formatting

4. **Developer experience:**
   - Clear documentation in README.md
   - Environment variables managed via .env files
   - Simple helper scripts for all common tasks

### Verification:
- `./dock dev` starts app accessible at http://localhost:8501
- Home page and About page both accessible via sidebar navigation
- `./dock test` passes with tests for both pages (6 tests total)
- `./dock lint` passes with no errors
- `./dock prod` starts production build
- Code changes in dev mode trigger hot-reload for all pages

## What We're NOT Doing

- Database integration (can be added later)
- CI/CD pipeline configuration
- Kubernetes/orchestration configs
- User authentication
- Complex multi-page applications (we include 2 pages to demonstrate routing)
- Monitoring/observability setup
- Production SSL certificate generation (documented only)

## Implementation Approach

Use multi-stage Docker builds to separate development and production environments. Development uses volume mounts for hot-reload, while production creates an optimized standalone image. Helper scripts (`dock`) provide a simple CLI for all operations.

---

## Phase 1: Project Foundation & Structure

### Overview
Set up the basic project structure with directories, configuration files, and git initialization.

### Changes Required:

#### 1. Project Directory Structure
Create the following structure:

```
gc-streamlit/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── pages/
│       └── about.py
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_about.py
├── .streamlit/
│   └── config.toml
├── .gitignore
├── .env.example
├── README.md
└── pyproject.toml
```

#### 2. Initialize Git Repository
**Command**: Initialize git and create initial structure

```bash
git init
git add .
git commit -m "Initial commit: project structure"
```

#### 3. Create .gitignore
**File**: `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# uv
.uv/
uv.lock

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
*.log
docker-compose.override.yml

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Streamlit
.streamlit/secrets.toml
```

### Success Criteria:

#### Automated Verification:
- [ ] Directory structure exists: `ls -la app/ tests/ .streamlit/`
- [ ] Git repository initialized: `git status`
- [ ] .gitignore file present: `test -f .gitignore`

#### Manual Verification:
- [ ] Directory structure matches the planned layout
- [ ] All directories are properly created

---

## Phase 2: Python Dependencies & uv Setup

### Overview
Configure Python dependencies using uv with pyproject.toml, including Streamlit and development tools.

### Changes Required:

#### 1. Create pyproject.toml
**File**: `pyproject.toml`

```toml
[project]
name = "gc-streamlit"
version = "0.1.0"
description = "Docker-based Streamlit application"
requires-python = ">=3.13"
dependencies = [
    "streamlit>=1.39.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.7.0",
    "httpx>=0.27.0",  # for testing Streamlit app
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --cov=app --cov-report=term-missing"
```

#### 2. Lock Dependencies
**Command**: Generate uv.lock file (will be done in Docker build)

Note: This will be handled automatically when building the Docker image.

### Success Criteria:

#### Automated Verification:
- [ ] pyproject.toml exists: `test -f pyproject.toml`
- [ ] pyproject.toml is valid TOML: `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"`

#### Manual Verification:
- [ ] Dependencies are appropriate for project needs
- [ ] Version constraints are reasonable

---

## Phase 3: Environment Variable Management

### Overview
Set up environment variable configuration for development and production environments.

### Changes Required:

#### 1. Create .env.example
**File**: `.env.example`

```bash
# Application Settings
APP_NAME=gc-streamlit
APP_ENV=development

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Production Settings (for SSL/HTTPS)
ENABLE_SSL=false
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem
```

#### 2. Create .streamlit/config.toml
**File**: `.streamlit/config.toml`

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Success Criteria:

#### Automated Verification:
- [ ] .env.example exists: `test -f .env.example`
- [ ] .streamlit/config.toml exists: `test -f .streamlit/config.toml`
- [ ] Config file is valid TOML: `python -c "import tomllib; tomllib.load(open('.streamlit/config.toml', 'rb'))"`

#### Manual Verification:
- [ ] Environment variables are sensibly configured
- [ ] Streamlit config provides good defaults

---

## Phase 4: Multi-Page Streamlit Application

### Overview
Create a multi-page Streamlit application with a home page and an about page to demonstrate Streamlit's routing capabilities.

### Changes Required:

#### 1. Create app/__init__.py
**File**: `app/__init__.py`

```python
"""Streamlit application package."""

__version__ = "0.1.0"
```

#### 2. Create app/main.py (Home Page)
**File**: `app/main.py`

```python
"""Main Streamlit application - Home page."""

import streamlit as st


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="GC Streamlit",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🚀 Welcome to GC Streamlit")
    st.write("This is a multi-page Streamlit application running in Docker.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Info")
        st.info("Built with Python 3.13 and Streamlit")
        st.code("docker run -p 8501:8501 gc-streamlit")

    with col2:
        st.subheader("Getting Started")
        st.success("Edit app/main.py to customize this page")
        st.write("Changes will hot-reload automatically in dev mode!")

    st.divider()

    # Navigation hint
    st.subheader("📑 Multiple Pages")
    st.write("Check out the **About** page in the sidebar to learn more about this application!")

    # Simple interaction
    name = st.text_input("What's your name?", placeholder="Enter your name")
    if name:
        st.balloons()
        st.write(f"Hello, {name}! 👋")


if __name__ == "__main__":
    main()
```

#### 3. Create app/pages directory
**Command**: `mkdir -p app/pages`

#### 4. Create app/pages/about.py (About Page)
**File**: `app/pages/about.py`

```python
"""About page for GC Streamlit application."""

import streamlit as st


def main():
    """About page content."""
    st.set_page_config(
        page_title="About - GC Streamlit",
        page_icon="ℹ️",
        layout="wide",
    )

    st.title("ℹ️ About GC Streamlit")

    st.markdown("""
    ## Overview

    This is a production-ready Docker scaffold for Python Streamlit applications,
    demonstrating multi-page routing and modern development practices.

    ## Features

    - 🐍 **Python 3.13** - Latest stable Python version
    - ⚡ **uv** - Blazing fast Python package installer
    - 🚀 **Streamlit** - Modern web app framework
    - 🐳 **Multi-stage Docker** - Optimized builds for dev and prod
    - 🔥 **Hot-reload** - Automatic reload on code changes in dev mode
    - 🔒 **SSL/HTTPS support** - Production-ready with nginx reverse proxy
    - ✅ **Testing** - pytest with coverage reporting
    - 🎨 **Code quality** - ruff for fast linting and formatting
    - 📄 **Multi-page routing** - Demonstrated with this About page!

    ## Technology Stack

    | Component | Version | Purpose |
    |-----------|---------|---------|
    | Python | 3.13 | Programming language |
    | Streamlit | Latest | Web framework |
    | uv | Latest | Package management |
    | Docker | Latest | Containerization |
    | pytest | Latest | Testing framework |
    | ruff | Latest | Linting and formatting |

    ## Multi-Page Routing

    Streamlit automatically creates navigation from files in the `pages/` directory.
    Each Python file becomes a page in the sidebar navigation. The file name
    determines the page name in the sidebar.

    ### How it works:
    - `app/main.py` → Home page (always first)
    - `app/pages/about.py` → About page (you are here!)
    - `app/pages/xyz.py` → Would create an "Xyz" page

    """)

    st.divider()

    # Project metadata
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Python Version", "3.13")

    with col2:
        st.metric("Docker", "Multi-stage")

    with col3:
        st.metric("Hot Reload", "Enabled")

    st.divider()

    # Additional info
    with st.expander("📚 Learn More"):
        st.markdown("""
        ### Resources
        - [Streamlit Documentation](https://docs.streamlit.io/)
        - [Python 3.13 Docs](https://docs.python.org/3.13/)
        - [uv Package Manager](https://github.com/astral-sh/uv)
        - [Docker Documentation](https://docs.docker.com/)

        ### Author
        Glenn Cueto

        ### License
        MIT
        """)


if __name__ == "__main__":
    main()
```

### Success Criteria:

#### Automated Verification:
- [ ] app/__init__.py exists: `test -f app/__init__.py`
- [ ] app/main.py exists: `test -f app/main.py`
- [ ] app/pages/ directory exists: `test -d app/pages`
- [ ] app/pages/about.py exists: `test -f app/pages/about.py`
- [ ] Python syntax is valid: `python -m py_compile app/main.py app/pages/about.py`

#### Manual Verification:
- [ ] Code is readable and well-structured
- [ ] Application serves as a good starting template
- [ ] Multi-page navigation is clear

---

## Phase 5: Testing Setup with pytest

### Overview
Set up pytest with tests for both the home page and about page to verify the Streamlit app works correctly.

### Changes Required:

#### 1. Create tests/__init__.py
**File**: `tests/__init__.py`

```python
"""Test suite for gc-streamlit application."""
```

#### 2. Create tests/test_app.py
**File**: `tests/test_app.py`

```python
"""Tests for the main Streamlit application (home page)."""

import pytest
from unittest.mock import patch, MagicMock


def test_main_page_title():
    """Test that the main page sets the correct title."""
    with patch("streamlit.set_page_config") as mock_config, \
         patch("streamlit.title") as mock_title, \
         patch("streamlit.write"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.text_input"):

        # Mock columns to return context managers
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main
        from app.main import main
        main()

        # Verify page config was set
        mock_config.assert_called_once_with(
            page_title="GC Streamlit",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # Verify title was set
        mock_title.assert_called_once_with("🚀 Welcome to GC Streamlit")


def test_main_page_renders_without_errors():
    """Test that the main page renders without raising exceptions."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.write"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.info"), \
         patch("streamlit.code"), \
         patch("streamlit.success"), \
         patch("streamlit.text_input", return_value=""):

        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main - should not raise
        from app.main import main
        main()


def test_main_page_name_input():
    """Test that entering a name triggers the greeting."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.write") as mock_write, \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.info"), \
         patch("streamlit.code"), \
         patch("streamlit.success"), \
         patch("streamlit.text_input", return_value="Alice"), \
         patch("streamlit.balloons"):

        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main
        from app.main import main
        main()

        # Check that greeting was written
        calls = [str(call) for call in mock_write.call_args_list]
        assert any("Alice" in call for call in calls), "Expected greeting with name 'Alice'"
```

#### 3. Create tests/test_about.py
**File**: `tests/test_about.py`

```python
"""Tests for the About page."""

import pytest
from unittest.mock import patch, MagicMock


def test_about_page_title():
    """Test that the about page sets the correct title."""
    with patch("streamlit.set_page_config") as mock_config, \
         patch("streamlit.title") as mock_title, \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric"), \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main
        from app.pages.about import main
        main()

        # Verify page config was set
        mock_config.assert_called_once_with(
            page_title="About - GC Streamlit",
            page_icon="ℹ️",
            layout="wide",
        )

        # Verify title was set
        mock_title.assert_called_once_with("ℹ️ About GC Streamlit")


def test_about_page_renders_without_errors():
    """Test that the about page renders without raising exceptions."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric"), \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main - should not raise
        from app.pages.about import main
        main()


def test_about_page_displays_metrics():
    """Test that the about page displays project metrics."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric") as mock_metric, \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main
        from app.pages.about import main
        main()

        # Verify metrics were created
        assert mock_metric.call_count == 3
        calls = [call[0] for call in mock_metric.call_args_list]
        labels = [call[0] for call in calls]
        assert "Python Version" in labels
        assert "Docker" in labels
        assert "Hot Reload" in labels
```

### Success Criteria:

#### Automated Verification:
- [ ] tests/__init__.py exists: `test -f tests/__init__.py`
- [ ] tests/test_app.py exists: `test -f tests/test_app.py`
- [ ] tests/test_about.py exists: `test -f tests/test_about.py`
- [ ] Python syntax is valid: `python -m py_compile tests/test_app.py tests/test_about.py`
- [ ] Tests can be discovered: `python -m pytest --collect-only tests/`

#### Manual Verification:
- [ ] Tests cover both home page and about page functionality
- [ ] Test descriptions are clear
- [ ] All tests cover essential functionality

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the tests are running correctly before proceeding to the next phase.

---

## Phase 6: Docker Multi-Stage Build

### Overview
Create a Dockerfile with multi-stage builds: development (with hot-reload) and production (optimized).

### Changes Required:

#### 1. Create Dockerfile
**File**: `Dockerfile`

```dockerfile
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
```

#### 2. Create .dockerignore
**File**: `.dockerignore`

```dockerignore
# Git
.git/
.gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/
env/
.venv
.uv/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
tests/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
.dockerignore
docker-compose*.yml

# Docs
README.md
thoughts/
*.md

# Environment
.env
.env.*
!.env.example

# Logs
*.log
```

### Success Criteria:

#### Automated Verification:
- [ ] Dockerfile exists: `test -f Dockerfile`
- [ ] .dockerignore exists: `test -f .dockerignore`
- [ ] Dockerfile syntax is valid: `docker build --check -f Dockerfile .`

#### Manual Verification:
- [ ] Multi-stage build structure is clear
- [ ] Development and production stages are properly separated
- [ ] Security best practices followed (non-root user in prod)

---

## Phase 7: Docker Compose Configuration

### Overview
Create docker-compose.yml for development with hot-reload and docker-compose.prod.yml for production.

### Changes Required:

#### 1. Create docker-compose.yml (Development)
**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: gc-streamlit-dev
    ports:
      - "8501:8501"
    volumes:
      - ./app:/app/app:ro
      - ./app/pages:/app/app/pages:ro
      - ./tests:/app/tests:ro
      - ./.streamlit:/app/.streamlit:ro
    env_file:
      - .env
    environment:
      - APP_ENV=development
      - STREAMLIT_SERVER_FILE_WATCHER_TYPE=auto
    restart: unless-stopped
    command: streamlit run app/main.py --server.runOnSave=true
```

#### 2. Create docker-compose.prod.yml (Production)
**File**: `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: gc-streamlit-prod
    ports:
      - "80:8501"
      - "443:443"
    env_file:
      - .env
    environment:
      - APP_ENV=production
      - STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s

  # Nginx reverse proxy for SSL/HTTPS (optional, commented out by default)
  # nginx:
  #   image: nginx:alpine
  #   container_name: gc-streamlit-nginx
  #   ports:
  #     - "443:443"
  #   volumes:
  #     - ./nginx.conf:/etc/nginx/nginx.conf:ro
  #     - ./ssl/cert.pem:/etc/ssl/certs/cert.pem:ro
  #     - ./ssl/key.pem:/etc/ssl/private/key.pem:ro
  #   depends_on:
  #     - streamlit
  #   restart: always
```

#### 3. Create nginx.conf (for SSL/HTTPS)
**File**: `nginx.conf`

```nginx
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server streamlit:8501;
    }

    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/ssl/certs/cert.pem;
        ssl_certificate_key /etc/ssl/private/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://streamlit;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }

        location /_stcore/stream {
            proxy_pass http://streamlit/_stcore/stream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_read_timeout 86400;
        }
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name localhost;
        return 301 https://$host$request_uri;
    }
}
```

### Success Criteria:

#### Automated Verification:
- [ ] docker-compose.yml exists: `test -f docker-compose.yml`
- [ ] docker-compose.prod.yml exists: `test -f docker-compose.prod.yml`
- [ ] nginx.conf exists: `test -f nginx.conf`
- [ ] Compose files are valid: `docker-compose config`

#### Manual Verification:
- [ ] Development compose includes volume mounts for hot-reload
- [ ] Production compose has health checks configured
- [ ] Nginx config properly handles WebSocket connections

---

## Phase 8: Docker Helper Scripts

### Overview
Create `dock` script with subcommands for common Docker operations (dev, stop, prod, rebuild, test, lint, logs, shell).

### Changes Required:

#### 1. Create dock script
**File**: `dock`

```bash
#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Ensure .env exists
ensure_env() {
    if [ ! -f .env ]; then
        warn ".env not found, copying from .env.example"
        cp .env.example .env
    fi
}

# Commands
cmd_dev() {
    info "Starting development environment..."
    ensure_env
    docker-compose up --build -d
    info "Development server running at http://localhost:8501"
    info "Logs: ./dock logs"
}

cmd_stop() {
    info "Stopping all containers..."
    docker-compose down
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    info "Containers stopped"
}

cmd_prod() {
    info "Starting production environment..."
    ensure_env
    docker-compose -f docker-compose.prod.yml up --build -d
    info "Production server running at http://localhost:80"
    info "For HTTPS, uncomment nginx service in docker-compose.prod.yml and add SSL certs"
}

cmd_rebuild() {
    local target="${1:-dev}"
    info "Rebuilding $target environment..."

    if [ "$target" = "dev" ]; then
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
    elif [ "$target" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml down
        docker-compose -f docker-compose.prod.yml build --no-cache
        docker-compose -f docker-compose.prod.yml up -d
    else
        error "Unknown target: $target. Use 'dev' or 'prod'"
    fi

    info "Rebuild complete"
}

cmd_test() {
    info "Running tests..."
    docker-compose exec streamlit pytest "$@"
}

cmd_lint() {
    info "Running linter..."
    docker-compose exec streamlit ruff check app/ tests/
}

cmd_format() {
    info "Formatting code..."
    docker-compose exec streamlit ruff format app/ tests/
    info "Code formatted"
}

cmd_logs() {
    docker-compose logs -f "${1:-streamlit}"
}

cmd_shell() {
    info "Opening shell in container..."
    docker-compose exec streamlit /bin/bash
}

cmd_clean() {
    warn "This will remove all containers, volumes, and images. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        info "Cleaning up..."
        docker-compose down -v
        docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true
        docker system prune -af --volumes
        info "Cleanup complete"
    else
        info "Cancelled"
    fi
}

cmd_help() {
    cat << EOF
Docker Helper Script for GC Streamlit

Usage: ./dock <command> [options]

Commands:
  dev              Start development environment with hot-reload
  stop             Stop all running containers
  prod             Start production environment
  rebuild [target] Rebuild containers (target: dev|prod, default: dev)
  test [args]      Run pytest tests (pass additional args to pytest)
  lint             Run ruff linter
  format           Format code with ruff
  logs [service]   Show logs (default: streamlit)
  shell            Open bash shell in container
  clean            Remove all containers, volumes, and images
  help             Show this help message

Examples:
  ./dock dev                    # Start development server
  ./dock test                   # Run all tests
  ./dock test tests/test_app.py # Run specific test file
  ./dock logs                   # Follow logs
  ./dock rebuild prod           # Rebuild production image
  ./dock shell                  # Open shell in container

EOF
}

# Main command router
main() {
    local command="${1:-help}"
    shift || true

    case "$command" in
        dev)
            cmd_dev
            ;;
        stop)
            cmd_stop
            ;;
        prod)
            cmd_prod
            ;;
        rebuild)
            cmd_rebuild "$@"
            ;;
        test)
            cmd_test "$@"
            ;;
        lint)
            cmd_lint
            ;;
        format)
            cmd_format
            ;;
        logs)
            cmd_logs "$@"
            ;;
        shell)
            cmd_shell
            ;;
        clean)
            cmd_clean
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            error "Unknown command: $command. Use './dock help' for usage."
            ;;
    esac
}

main "$@"
```

#### 2. Make script executable
**Command**: `chmod +x dock`

### Success Criteria:

#### Automated Verification:
- [ ] dock script exists: `test -f dock`
- [ ] dock script is executable: `test -x dock`
- [ ] Script syntax is valid: `bash -n dock`

#### Manual Verification:
- [ ] Help message is clear and informative
- [ ] All commands are documented

---

## Phase 9: Documentation

### Overview
Create comprehensive README.md with setup instructions, usage examples, and deployment notes.

### Changes Required:

#### 1. Create README.md
**File**: `README.md`

```markdown
# GC Streamlit Docker Scaffold

A production-ready Docker scaffold for Python Streamlit applications with development and production environments.

## Features

- 🐍 **Python 3.13** - Latest stable Python version
- ⚡ **uv** - Blazing fast Python package installer
- 🚀 **Streamlit** - Modern web app framework for ML and data science
- 📄 **Multi-page routing** - Automatic navigation from pages/ directory
- 🐳 **Multi-stage Docker** - Optimized builds for dev and prod
- 🔥 **Hot-reload** - Automatic reload on code changes in dev mode
- 🔒 **SSL/HTTPS support** - Production-ready with nginx reverse proxy
- ✅ **Testing** - pytest with coverage reporting
- 🎨 **Code quality** - ruff for fast linting and formatting
- 🛠️ **Helper scripts** - Simple `dock` CLI for common tasks

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git (optional)

### Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd gc-streamlit
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start development server:**
   ```bash
   ./dock dev
   ```

4. **Open your browser:**
   ```
   http://localhost:8501
   ```

That's it! The app is now running with hot-reload enabled.

## Usage

### Development

Start the development environment:
```bash
./dock dev
```

The development environment includes:
- Hot-reload on code changes
- Volume mounts for real-time updates
- Development dependencies (pytest, ruff, etc.)
- Access at http://localhost:8501

### Testing

Run all tests:
```bash
./dock test
```

Run specific test file:
```bash
./dock test tests/test_app.py
```

Run with coverage:
```bash
./dock test --cov-report=html
```

### Code Quality

Check code with linter:
```bash
./dock lint
```

Format code:
```bash
./dock format
```

### Production

Start production environment:
```bash
./dock prod
```

Production environment features:
- Optimized Docker image (smaller size)
- No development dependencies
- Health checks enabled
- Runs as non-root user
- Access at http://localhost:80

### Other Commands

View logs:
```bash
./dock logs
```

Open shell in container:
```bash
./dock shell
```

Rebuild containers:
```bash
./dock rebuild dev   # Rebuild dev
./dock rebuild prod  # Rebuild prod
```

Stop all containers:
```bash
./dock stop
```

Clean everything:
```bash
./dock clean
```

## Project Structure

```
gc-streamlit/
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py            # Main Streamlit app (home page)
│   └── pages/             # Additional pages (auto-routed)
│       └── about.py       # About page
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_app.py        # Tests for home page
│   └── test_about.py      # Tests for about page
├── .streamlit/            # Streamlit config
│   └── config.toml
├── thoughts/              # Documentation and plans
│   └── shared/
│       └── plans/
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Development config
├── docker-compose.prod.yml # Production config
├── nginx.conf             # Nginx reverse proxy for SSL
├── pyproject.toml         # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore
├── dock                   # Helper script
└── README.md
```

## SSL/HTTPS Setup (Production)

For production deployment with SSL/HTTPS:

1. **Generate SSL certificates:**
   ```bash
   mkdir -p ssl
   # Use Let's Encrypt, self-signed, or your certificate provider
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout ssl/key.pem -out ssl/cert.pem
   ```

2. **Uncomment nginx service** in `docker-compose.prod.yml`

3. **Start production with nginx:**
   ```bash
   ./dock prod
   ```

4. **Access via HTTPS:**
   ```
   https://localhost
   ```

## Environment Variables

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | `gc-streamlit` |
| `APP_ENV` | Environment (development/production) | `development` |
| `STREAMLIT_SERVER_PORT` | Streamlit port | `8501` |
| `ENABLE_SSL` | Enable SSL/HTTPS | `false` |

See `.env.example` for complete list.

## Development Workflow

1. Edit code in `app/main.py` or `app/pages/*.py`
2. Changes auto-reload in browser (dev mode)
3. Write tests in `tests/`
4. Run `./dock test` to verify
5. Run `./dock lint` to check code quality
6. Commit and deploy

## Multi-Page Routing

Streamlit automatically creates navigation from the `pages/` directory:

- `app/main.py` → Home page (always first in navigation)
- `app/pages/about.py` → About page (appears in sidebar)
- `app/pages/xyz.py` → Would create an "Xyz" page

**Adding a new page:**
1. Create `app/pages/my_page.py`
2. Add your Streamlit code with a `main()` function
3. The page automatically appears in the sidebar navigation
4. Hot-reload works for all pages in development mode

**File naming:**
- Use lowercase with underscores: `my_new_page.py`
- Streamlit converts to title case: "My New Page"
- Use number prefixes to control order: `1_first.py`, `2_second.py`

## Troubleshooting

### Port already in use
```bash
./dock stop
# Or manually: docker-compose down
```

### Container won't start
```bash
./dock logs
```

### Clean rebuild needed
```bash
./dock clean
./dock rebuild dev
```

### Hot-reload not working
Ensure you're using `./dock dev` and volumes are properly mounted in `docker-compose.yml`.

## Technology Stack

- **Python 3.13** - Programming language
- **Streamlit** - Web framework
- **uv** - Package management
- **Docker** - Containerization
- **pytest** - Testing framework
- **ruff** - Linting and formatting
- **nginx** - Reverse proxy (optional, for SSL)

## Contributing

1. Make your changes
2. Run tests: `./dock test`
3. Check linting: `./dock lint`
4. Format code: `./dock format`
5. Commit your changes

## License

MIT

## Author

Glenn Cueto

---

Built with ❤️ using Docker, Python, and Streamlit
```

### Success Criteria:

#### Automated Verification:
- [ ] README.md exists: `test -f README.md`
- [ ] README has required sections: `grep -q "Quick Start" README.md && grep -q "Usage" README.md`

#### Manual Verification:
- [ ] Documentation is clear and complete
- [ ] Examples are accurate and runnable
- [ ] Troubleshooting section is helpful

---

## Testing Strategy

### Unit Tests:
- Test Streamlit page configuration
- Test page rendering without errors
- Test interactive components (name input)
- Mock Streamlit functions to isolate logic

### Integration Tests:
- Build Docker development image successfully
- Build Docker production image successfully
- Container starts and serves on port 8501
- Hot-reload works in development mode

### Manual Testing Steps:
1. Run `./dock dev` and verify app loads at http://localhost:8501
2. Verify home page displays correctly with name input
3. Click "About" in sidebar and verify about page loads
4. Edit `app/main.py` and verify hot-reload triggers on home page
5. Edit `app/pages/about.py` and verify hot-reload triggers on about page
6. Enter a name in the text input on home page and verify greeting appears
7. Run `./dock test` and verify all 6 tests pass (3 for home, 3 for about)
8. Run `./dock lint` and verify no errors
9. Run `./dock prod` and verify production build works with both pages
10. Stop containers with `./dock stop`

## Performance Considerations

- **Multi-stage builds** reduce production image size by excluding dev dependencies
- **uv** provides faster dependency resolution and installation vs pip
- **Layer caching** in Dockerfile optimizes rebuild times
- **Volume mounts** in dev mode avoid copying files into container
- **Non-root user** in production improves security
- **Health checks** enable container orchestration and load balancing

## Migration Notes

N/A - This is a greenfield project with no existing data or systems to migrate.

## References

- Python 3.13: https://docs.python.org/3.13/
- Streamlit: https://docs.streamlit.io/
- uv: https://github.com/astral-sh/uv
- Docker multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- nginx SSL configuration: https://nginx.org/en/docs/http/configuring_https_servers.html
- pytest: https://docs.pytest.org/
- ruff: https://docs.astral.sh/ruff/
