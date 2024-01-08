FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

ENV PORT=1000 \
    SECRET_KEY=BuyBreadTomorrow

EXPOSE $PORT

CMD uvicorn backend:app --host 0.0.0.0 --port $PORT