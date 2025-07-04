# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS build-stage

WORKDIR /app

# 使用阿里云npm镜像源
RUN npm config set registry https://registry.npmmirror.com/ && \
    npm config set disturl https://npmmirror.com/dist && \
    npm config set sass_binary_site https://npmmirror.com/mirrors/node-sass/ && \
    npm config set electron_mirror https://npmmirror.com/mirrors/electron/ && \
    npm config set puppeteer_download_host https://npmmirror.com/mirrors && \
    npm config set chromedriver_cdnurl https://npmmirror.com/mirrors/chromedriver && \
    npm config set operadriver_cdnurl https://npmmirror.com/mirrors/operadriver && \
    npm config set phantomjs_cdnurl https://npmmirror.com/mirrors/phantomjs && \
    npm config set selenium_cdnurl https://npmmirror.com/mirrors/selenium && \
    npm config set node_inspector_cdnurl https://npmmirror.com/mirrors/node-inspector

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
