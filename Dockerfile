FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

WORKDIR /app

# Keep only the system packages required by the application.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    graphviz \
    libgraphviz-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user.
RUN useradd --create-home --system --user-group appuser

# Install production dependencies first for better build caching.
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy application files.
COPY --chown=appuser:appuser . .

# Ensure the application can write reports.
RUN mkdir -p /app/logs && \
    chown appuser:appuser /app/logs

USER appuser

EXPOSE 8080

CMD ["uvicorn", "aapp_mart.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
