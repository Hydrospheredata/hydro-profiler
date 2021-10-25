# syntax=docker/dockerfile:1
FROM node:14.16.1 AS build

WORKDIR /opt/ng

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build
RUN ls -la


FROM openresty/openresty:1.19.9.1-0-amzn2
LABEL maintainer="support@hydrosphere.io"

RUN yum update -y && yum upgrade -y && yum clean all

RUN useradd -u 42069 --create-home --shell /bin/bash app && \
    chown -R app:app /usr/local/openresty/

USER app

ENV OSS=true;

EXPOSE 8080

COPY --chown=app:app docker/nginx/conf.d /etc/nginx/conf.d/
COPY --chown=app:app docker/nginx/config/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY --chown=app:app --from=build /opt/ng/dist/profiler-fe /usr/share/nginx/html

CMD exec /usr/local/openresty/bin/openresty -g 'daemon off;'
