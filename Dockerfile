FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

WORKDIR /app

# Install required system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    graphviz \
    libgraphviz-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user.
RUN useradd --create-home --system --user-group appuser

# Copy the project, including pyproject.toml.
COPY . .

# Install the project and its declared dependencies.
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir .

# Create the logs directory and set permissions.
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app/logs

# Run as a non-root user.
USER appuser

EXPOSE 8080

CMD ["uvicorn", "aapp_mart.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
