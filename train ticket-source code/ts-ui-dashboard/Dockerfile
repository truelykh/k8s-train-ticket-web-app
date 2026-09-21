# Multi-stage optimized OpenResty / Nginx Alpine Frontend
FROM openresty/openresty:alpine
ENV TZ=Asia/Shanghai

COPY ts-ui-dashboard/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ts-ui-dashboard/static /usr/share/nginx/html

EXPOSE 8080

CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
