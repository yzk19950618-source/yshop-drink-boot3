# yshop-drink-boot3 — 微信云托管 / 通用容器部署
# 构建：在 yshop-drink-boot3 仓库根目录执行 docker build -t yshop-server .
# 云托管：构建目录选仓库根；容器端口与「服务设置」中的监听端口一致（默认常用 8080，平台会注入 PORT）
#
# 必配环境变量（示例）：MYSQL_HOST、MYSQL_DATABASE、MYSQL_USERNAME、MYSQL_PASSWORD、REDIS_HOST
# 可选：MYSQL_PORT、REDIS_PORT、REDIS_PASSWORD、SPRING_PROFILES_ACTIVE（默认 local,cloud）

FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY . .
RUN mvn -f pom.xml clean package -pl yshop-server -am -DskipTests -B

FROM eclipse-temurin:17-jre-jammy

RUN mkdir -p /app \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/yshop-server/target/yshop-server.jar app.jar

ENV TZ=Asia/Shanghai
ENV JAVA_OPTS="-Xms512m -Xmx1024m -Djava.security.egd=file:/dev/./urandom"
ENV SPRING_PROFILES_ACTIVE=local,cloud
# 与微信云托管未注入 PORT 时的本地习惯端口一致；云上以平台注入为准
ENV PORT=48081

EXPOSE 48081

# 命令行 server.port 优先于配置文件，兼容云托管 PORT
ENTRYPOINT ["sh", "-c", "exec java ${JAVA_OPTS} -jar /app/app.jar --server.port=${PORT}"]
