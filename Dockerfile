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
# 微信云托管常见监听 8080；平台注入 PORT 时仍优先生效（命令行覆盖 ENV）
ENV PORT=8080

EXPOSE 8080

# 命令行显式激活 cloud，避免控制台未继承镜像 ENV 时仍只用 local（会连 127.0.0.1）
ENTRYPOINT ["sh", "-c", "exec java ${JAVA_OPTS} -jar /app/app.jar --spring.profiles.active=local,cloud --server.port=${PORT}"]
