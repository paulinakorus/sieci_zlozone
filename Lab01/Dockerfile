FROM python:3.14

ARG UID
ARG GID

WORKDIR /app

RUN groupadd --gid $GID myuser && useradd -u $UID --gid $GID -m myuser && chown -R myuser /app

COPY requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt

USER myuser