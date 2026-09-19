# Build context: repository root (compose sets context: .)
FROM node:18-slim

ENV TZ=Asia/Shanghai

RUN mkdir -p /app
WORKDIR /app

COPY ts-ticket-office-service/node_modules /app/node_modules
COPY ts-ticket-office-service/package.json /app/
COPY ts-ticket-office-service/public /app/public
COPY ts-ticket-office-service/bin /app/bin
COPY ts-ticket-office-service/app.js /app/
CMD ["npm", "start"]

EXPOSE 16108
