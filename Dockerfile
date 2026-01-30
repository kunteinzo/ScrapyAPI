FROM python:slim
LABEL authors="kunteinzo"

WORKDIR /app
COPY *.py .
COPY *.txt .
COPY *.json .
COPY *.sh .

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/run_api.sh"]
