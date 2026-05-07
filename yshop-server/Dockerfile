# 可选：在已执行 `mvn package` 生成 target/yshop-server.jar 后，于本目录构建运行时镜像
#   docker build -t yshop-server -f Dockerfile .
#
# 微信云托管 / CI 推荐：使用仓库根目录的 Dockerfile（多阶段含 Maven 编译），构建上下文为 yshop-drink-boot3 根路径。

FROM eclipse-temurin:17-jre-jammy

RUN mkdir -p /app
WORKDIR /app
COPY target/yshop-server.jar app.jar

ENV TZ=Asia/Shanghai
ENV JAVA_OPTS="-Xms512m -Xmx1024m -Djava.security.egd=file:/dev/./urandom"
ENV SPRING_PROFILES_ACTIVE=local,cloud
ENV PORT=48081

EXPOSE 48081

ENTRYPOINT ["sh", "-c", "exec java ${JAVA_OPTS} -jar /app/app.jar --server.port=${PORT}"]
