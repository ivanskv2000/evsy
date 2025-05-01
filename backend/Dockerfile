# ----------------------
# Stage 1: Build environment
# ----------------------
FROM python:3.13-bullseye AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

COPY ./app ./app
COPY alembic.ini .
COPY migrations/ migrations/


# ----------------------
# Stage 2: Dev environment
# ----------------------
FROM builder AS dev

RUN poetry install --only dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


# ----------------------
# Stage 3: Production image
# ----------------------
FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY ./app ./app
COPY alembic.ini .
COPY migrations/ migrations/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
