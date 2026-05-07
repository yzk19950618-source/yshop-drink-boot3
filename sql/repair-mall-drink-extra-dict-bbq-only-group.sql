-- BBQ / 烧烤店：点餐端「附加规格」分组只保留辣度（甜度、冰量不再出现在 mall_drink_extra_group 中）。
-- 子字典类型 mall_drink_extra_sugar / mall_drink_extra_ice 可保留在库里，仅分组引用去掉即可。
-- 执行后重启后端并清理字典缓存（Redis 中 dict 相关 key）。
SET NAMES utf8mb4;

-- 停用分组中的甜度、冰量（status=1 为停用；小程序只拉启用数据）
UPDATE system_dict_data
SET status = 1, updater = '1', update_time = NOW()
WHERE dict_type = 'mall_drink_extra_group'
  AND value IN ('mall_drink_extra_sugar', 'mall_drink_extra_ice')
  AND deleted = b'0';

-- 若希望物理删除分组行（不可恢复），改用下面语句并注释掉上面 UPDATE：
-- DELETE FROM system_dict_data WHERE dict_type = 'mall_drink_extra_group'
--   AND value IN ('mall_drink_extra_sugar', 'mall_drink_extra_ice');
