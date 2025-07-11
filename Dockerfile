# Dockerfile (維持原樣，不需要動)

FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 注意：這裡沒有 COPY .env 檔案！
COPY ./bot ./bot

CMD ["python", "bot/main.py"]
