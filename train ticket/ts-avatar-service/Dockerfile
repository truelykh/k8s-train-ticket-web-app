# Build context: repository root (compose sets context: .)
FROM python:3.9-slim

ENV TZ=Asia/Shanghai PYTHONUNBUFFERED=TRUE

RUN apt-get update \
 && apt-get install -y --no-install-recommends cmake libgl1 libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
COPY ts-avatar-service/ /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:17001", "app:app"]

EXPOSE 17001
