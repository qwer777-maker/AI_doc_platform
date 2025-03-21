FROM ubuntu:20.04

# 安装nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 创建下载目录
RUN mkdir -p /usr/share/nginx/html/downloads

# 设置适当的权限
RUN chown -R www-data:www-data /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 