FROM python:3.14

ARG UID
ARG GID

WORKDIR /app

RUN apt-get update && apt-get install -y \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $GID myuser && useradd -u $UID --gid $GID -m myuser && chown -R myuser /app

COPY requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

USER myuser