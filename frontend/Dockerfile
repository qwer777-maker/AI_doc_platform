FROM ubuntu:20.04 as build-stage

WORKDIR /app

# 安装Node.js和npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 利用Docker的缓存机制
COPY package*.json ./
RUN npm install

# 复制必要的源代码文件
COPY src ./src
COPY vue.config.js ./
COPY .env.* ./
COPY .eslintrc.js ./

# 构建应用
RUN npm run build

# 生产环境使用nginx
FROM ubuntu:20.04 as production-stage

# 安装nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 从构建阶段复制构建产物
COPY --from=build-stage /app/dist /var/www/html

# 创建默认nginx配置
RUN echo 'server { \n\
    listen 80; \n\
    server_name localhost; \n\
    \n\
    location / { \n\
        root /var/www/html; \n\
        index index.html index.htm; \n\
        try_files $uri $uri/ /index.html; \n\
    } \n\
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 