FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    graphviz \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "bash" ]
