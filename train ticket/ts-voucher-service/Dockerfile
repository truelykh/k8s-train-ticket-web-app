# Build context: repository root (compose sets context: .)
FROM python:3-slim

ENV TZ=Asia/Shanghai

RUN mkdir -p /app
WORKDIR /app

COPY ts-voucher-service/requirements.txt ./
RUN pip install cryptography && pip install --no-cache-dir -r requirements.txt

COPY ts-voucher-service/server.py /app/
CMD ["python", "server.py"]

EXPOSE 16101
