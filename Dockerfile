FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmetis-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY dev-requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 && pip install --no-cache-dir -r dev-requirements.txt
 && pip install gunicorn

RUN useradd -m aappmart
USER aappmart

COPY src/ ./src/
ENV PYTHONPATH=/app/src

EXPOSE 8080

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "aapp_mart.app:app", "--bind", "0.0.0.0:8080", "--workers", "4"]
