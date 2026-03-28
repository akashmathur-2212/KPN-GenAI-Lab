FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install project dependencies from pyproject.toml
COPY pyproject.toml ./
RUN python -c "import pathlib, tomllib; deps = tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project']['dependencies']; pathlib.Path('requirements.txt').write_text('\n'.join(deps) + '\n')" \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.app:api", "--host", "0.0.0.0", "--port", "8000"]
