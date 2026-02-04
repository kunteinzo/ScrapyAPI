FROM python:slim
LABEL authors="kunteinzo"

WORKDIR /app
COPY route .
COPY scrape .
COPY task .
COPY websocket .
COPY *.py .
COPY *.txt .
COPY *.json .

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN chown -R appuser:appuser /app

# ENTRYPOINT ["/app/run.sh"]
