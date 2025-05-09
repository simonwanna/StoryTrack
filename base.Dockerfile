FROM ubuntu:22.04

WORKDIR /app

# Prevent tzdata from asking for input
ENV DEBIAN_FRONTEND=noninteractive

# Basic system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Additional dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    openjdk-11-jre-headless \
    tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install pipenv since Python is externally managed
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt