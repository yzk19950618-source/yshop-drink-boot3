-- 修复 yshop_service.name 中文乱码（如 ????????），与官方 yixiang-drink-open.sql 种子一致。
-- 执行前请备份。客户端与连接请使用 utf8mb4，例如：
--   mysql -u root -p --default-character-set=utf8mb4 your_database < repair-yshop-service-names-utf8mb4.sql
-- 若 JDBC 未指定 characterEncoding=UTF-8，请与 repair-system-dictionary-utf8mb4.sql 相同策略核对数据源配置。

SET NAMES utf8mb4;

UPDATE `yshop_service` SET `name` = '积分签到' WHERE `id` = 20;
UPDATE `yshop_service` SET `name` = '我的订单' WHERE `id` = 21;
UPDATE `yshop_service` SET `name` = '积分商城' WHERE `id` = 22;
UPDATE `yshop_service` SET `name` = '兑换订单' WHERE `id` = 23;
UPDATE `yshop_service` SET `name` = '联系客服' WHERE `id` = 24;
UPDATE `yshop_service` SET `name` = '我的地址' WHERE `id` = 25;
UPDATE `yshop_service` SET `name` = '帮助中心' WHERE `id` = 26;
UPDATE `yshop_service` SET `name` = '关于我们' WHERE `id` = 27;
UPDATE `yshop_service` SET `name` = '退出登录' WHERE `id` = 28;
UPDATE `yshop_service` SET `name` = '用户协议' WHERE `id` = 29;
UPDATE `yshop_service` SET `name` = '隐私政策' WHERE `id` = 30;
UPDATE `yshop_service` SET `name` = '积分订单' WHERE `id` = 31;
