FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --only main

COPY . /app

CMD ["poetry", "run", "python", "-m", "flexius_monorepo"]
