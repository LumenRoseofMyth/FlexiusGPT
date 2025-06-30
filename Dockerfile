# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    build-essential \
    curl \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry globally
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Disable virtualenv creation so dependencies install globally
RUN poetry config virtualenvs.create false

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml poetry.lock /app/

# Install Python dependencies (main only)
RUN poetry install --no-root --only main

# Copy the rest of the application code
COPY . /app

# Default command to run the app
CMD ["poetry", "run", "python", "-m", "flexius_monorepo"]
