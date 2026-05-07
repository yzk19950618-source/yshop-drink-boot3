-- 微信云托管 / 自建 MySQL：先建库（与 application-cloud.yaml 默认 MYSQL_DATABASE 一致）
-- 客户端建议：mysql -h HOST -P 3306 -u root -p --default-character-set=utf8mb4 < 00-create-database-utf8mb4.sql
-- 全量建表请再导入 sql/yixiang-drink-open.sql（见 sql/cloud-mysql-exec-order.txt）

CREATE DATABASE IF NOT EXISTS `yixiang-drink-open`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
