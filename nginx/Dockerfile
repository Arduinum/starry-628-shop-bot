FROM nginx:alpine

WORKDIR /app

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx

COPY ssl_keys/fullchain.pem /app/ssl_keys/fullchain.pem
COPY ssl_keys/privkey.pem /app/ssl_keys/privkey.pem