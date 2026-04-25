FROM python:3.12-slim

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	STREAMLIT_SERVER_PORT=8501 \
	STREAMLIT_SERVER_HEADLESS=true \
	STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
	UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	curl \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie les fichiers de config à la racine
COPY pyproject.toml uv.lock* README.md ./

# Installe les dépendances dans .venv avec uv
RUN uv sync --frozen --no-dev

# Copie le code de l'app
COPY streamlit/ ./streamlit/

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
	CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["uv", "run", "streamlit", "run", "streamlit/app.py", \
	 "--server.address=0.0.0.0", \
	 "--server.headless=true", \
	 "--server.enableCORS=false", \
	 "--server.enableXsrfProtection=true"]
