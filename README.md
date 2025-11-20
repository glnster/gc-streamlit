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
