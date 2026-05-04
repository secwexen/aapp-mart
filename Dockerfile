FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmetis-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8080

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "aapp_mart.main:app", "--bind", "0.0.0.0:8080", "--workers", "4"]
