FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    build-essential \
    git curl \
    openjdk-11-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN ln -s /usr/bin/python3 /usr/bin/python

# use pipenv since Python is externally managed
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/storytrack/gpx2delta.py .
RUN mkdir -p gpx_files tmp

CMD ["python", "gpx2delta.py"]