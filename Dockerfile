FROM python:3.10-slim-buster as builder

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* &&\
    pip install --user -r requirements.txt

FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* && \
    useradd -m appuser
USER appuser

WORKDIR /home/appuser

COPY --from=builder /root/.local /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH

COPY --chown=appuser:appuser . .

ENV PORT=1000 SECRET_KEY=BuyBreadTomorrow
EXPOSE $PORT

CMD uvicorn backend:app --host 0.0.0.0 --port $PORT