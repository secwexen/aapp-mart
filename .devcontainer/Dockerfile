FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        make \
        build-essential \
        curl \
        git \
        net-tools \
        iputils-ping \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

USER vscode