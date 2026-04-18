FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md manage.py ./
COPY apps ./apps
COPY config ./config

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -e '.[dev]'

COPY tests ./tests
COPY .agents ./.agents

CMD ["python", "manage.py", "check", "--settings=config.settings.test"]
