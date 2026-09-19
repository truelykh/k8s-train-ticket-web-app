# Build context: repository root (compose sets context: .)
FROM openresty/openresty:alpine

ENV TZ=Asia/Shanghai

COPY ts-ui-dashboard/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ts-ui-dashboard/static /usr/share/nginx/html

EXPOSE 8080
