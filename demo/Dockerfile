FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY nginx/landing.conf /etc/nginx/conf.d/default.conf

RUN chmod 644 /usr/share/nginx/html/index.html /etc/nginx/conf.d/default.conf
