#!/bin/bash

# Run Redis Docker Container
docker start redis

# Run Celery Worker
screen -dmS celery .venv/bin/celery -A tasks worker -B -l info

# Run FastAPI Server
screen -dmS fastapi .venv/bin/gunicorn app:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000

function stop_the_app() {
  screen -S fastapi -X quit
  screen -S celery -X quit
  docker stop redis
}

while true;
do
  echo 'Stop? (y): '
  read isStop
  if [[ $isStop == 'y' ]];then
    stop_the_app
    exit 0
  fi
done