# yshop-drink-boot3 — 微信云托管 / 通用容器部署
# 构建：在 yshop-drink-boot3 仓库根目录执行 docker build -t yshop-server .
#
# 微信云托管「部署失败 / Readiness:Liveness probe failed dial tcp :80 connection refused」：
#   控制台「容器端口」与健康检查端口必须与进程监听端口一致。本镜像默认监听 8080（ENV PORT=8080）。
#   若控制台误填为 80，探针会连 80 而应用开在 8080 → connection refused。
#   请在服务设置中将容器端口、HTTP 路径检查或 TCP 检查端口一律改为 8080；可选路径 /actuator/health
#
# 必配（二选一）：
#   ① cloud 生效时：MYSQL_HOST、MYSQL_PORT、MYSQL_DATABASE、MYSQL_USERNAME、MYSQL_PASSWORD、REDIS_HOST
#   ② cloud 未生效时：用 Spring 标准变量覆盖主库（见 application-cloud.yaml 文件头注释）
# 可选：REDIS_PORT、REDIS_PASSWORD；SPRING_PROFILES_ACTIVE 默认 local,cloud（控制台若写不下逗号可用方式②）

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
