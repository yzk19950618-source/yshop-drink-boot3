-- 小程序「饮品附加规格」（辣度/甜度/冰量等）：全局字典，可在管理后台「字典管理」中增删改。
-- 执行前请备份。连接使用 utf8mb4。
-- 执行后重启后端并清理字典缓存（Redis 中 dict 相关 key，若使用缓存）。
SET NAMES utf8mb4;

-- 字典类型（不存在则插入）
INSERT INTO system_dict_type (name, type, status, remark, creator, create_time, updater, update_time, deleted, deleted_time)
SELECT '饮品附加规格分组', 'mall_drink_extra_group', 0, 'label=分组展示名；value=子字典类型（须与 system_dict_type.type 一致）', '1', NOW(), '1', NOW(), b'0', NULL
WHERE NOT EXISTS (SELECT 1 FROM system_dict_type t WHERE t.type = 'mall_drink_extra_group');

INSERT INTO system_dict_type (name, type, status, remark, creator, create_time, updater, update_time, deleted, deleted_time)
SELECT '饮品附加-辣度', 'mall_drink_extra_spicy', 0, '小程序选规格下方可选', '1', NOW(), '1', NOW(), b'0', NULL
WHERE NOT EXISTS (SELECT 1 FROM system_dict_type t WHERE t.type = 'mall_drink_extra_spicy');

INSERT INTO system_dict_type (name, type, status, remark, creator, create_time, updater, update_time, deleted, deleted_time)
SELECT '饮品附加-甜度', 'mall_drink_extra_sugar', 0, NULL, '1', NOW(), '1', NOW(), b'0', NULL
WHERE NOT EXISTS (SELECT 1 FROM system_dict_type t WHERE t.type = 'mall_drink_extra_sugar');

INSERT INTO system_dict_type (name, type, status, remark, creator, create_time, updater, update_time, deleted, deleted_time)
SELECT '饮品附加-冰量', 'mall_drink_extra_ice', 0, NULL, '1', NOW(), '1', NOW(), b'0', NULL
WHERE NOT EXISTS (SELECT 1 FROM system_dict_type t WHERE t.type = 'mall_drink_extra_ice');

-- 分组行：sort 决定顺序；value 必须为已存在的子字典 type
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 10, '辣度', 'mall_drink_extra_spicy', 'mall_drink_extra_group', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_group' AND d.value = 'mall_drink_extra_spicy');

INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 20, '甜度', 'mall_drink_extra_sugar', 'mall_drink_extra_group', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_group' AND d.value = 'mall_drink_extra_sugar');

INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 30, '冰量', 'mall_drink_extra_ice', 'mall_drink_extra_group', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_group' AND d.value = 'mall_drink_extra_ice');

-- 辣度选项（value 在同 dict_type 下唯一）
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 1, '不辣', '1', 'mall_drink_extra_spicy', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_spicy' AND d.value = '1');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 2, '微辣', '2', 'mall_drink_extra_spicy', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_spicy' AND d.value = '2');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 3, '中辣', '3', 'mall_drink_extra_spicy', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_spicy' AND d.value = '3');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 4, '重辣', '4', 'mall_drink_extra_spicy', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_spicy' AND d.value = '4');

INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 1, '无糖', '1', 'mall_drink_extra_sugar', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_sugar' AND d.value = '1');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 2, '少糖', '2', 'mall_drink_extra_sugar', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_sugar' AND d.value = '2');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 3, '正常', '3', 'mall_drink_extra_sugar', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_sugar' AND d.value = '3');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 4, '多糖', '4', 'mall_drink_extra_sugar', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_sugar' AND d.value = '4');

INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 1, '去冰', '1', 'mall_drink_extra_ice', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_ice' AND d.value = '1');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 2, '少冰', '2', 'mall_drink_extra_ice', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_ice' AND d.value = '2');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 3, '正常冰', '3', 'mall_drink_extra_ice', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_ice' AND d.value = '3');
INSERT INTO system_dict_data (sort, label, value, dict_type, status, color_type, css_class, remark, creator, create_time, updater, update_time, deleted)
SELECT 4, '多冰', '4', 'mall_drink_extra_ice', 0, '', '', NULL, '1', NOW(), '1', NOW(), b'0'
WHERE NOT EXISTS (SELECT 1 FROM system_dict_data d WHERE d.dict_type = 'mall_drink_extra_ice' AND d.value = '4');
