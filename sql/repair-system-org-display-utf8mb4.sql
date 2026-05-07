-- 修复「用户/角色/部门/岗位」管理及各类列表中状态、名称显示为问号的问题（库内中文被损坏时执行）
-- 请先备份。使用 utf8mb4 客户端执行，例如：
--   mysql -u root -p --default-character-set=utf8mb4 yixiang-drink-open < repair-system-org-display-utf8mb4.sql
-- 执行后重启后端；浏览器强刷并清空 sessionStorage 中的字典缓存（或重新登录）

SET NAMES utf8mb4;

-- 列表「状态」列依赖的字典（common_status）
UPDATE system_dict_data SET label = '开启', remark = '开启状态' WHERE dict_type = 'common_status' AND `value` = '0';
UPDATE system_dict_data SET label = '关闭', remark = '关闭状态' WHERE dict_type = 'common_status' AND `value` = '1';

-- 角色管理「角色类型」列
UPDATE system_dict_data SET label = '内置', remark = '内置角色' WHERE dict_type = 'system_role_type' AND `value` = '1';
UPDATE system_dict_data SET label = '自定义', remark = '自定义角色' WHERE dict_type = 'system_role_type' AND `value` = '2';

-- 部门名称（与 yixiang-drink-open.sql 默认数据一致）
UPDATE system_dept SET name = 'yshop公司' WHERE id = 100;
UPDATE system_dept SET name = '深圳总公司' WHERE id = 101;
UPDATE system_dept SET name = '长沙分公司' WHERE id = 102;
UPDATE system_dept SET name = '研发部门' WHERE id = 103;
UPDATE system_dept SET name = '市场部门' WHERE id = 104;
UPDATE system_dept SET name = '测试部门' WHERE id = 105;
UPDATE system_dept SET name = '财务部门' WHERE id = 106;
UPDATE system_dept SET name = '运维部门' WHERE id = 107;
UPDATE system_dept SET name = '市场部门' WHERE id = 108;
UPDATE system_dept SET name = '财务部门' WHERE id = 109;
UPDATE system_dept SET name = '新部门' WHERE id = 110;
UPDATE system_dept SET name = '顶级部门' WHERE id = 111;

-- 角色名称与备注
UPDATE system_role SET name = '超级管理员', remark = '超级管理员' WHERE id = 1;
UPDATE system_role SET name = '门店角色', remark = '普通角色' WHERE id = 2;

-- 岗位名称（name 为展示名；code 为编码）
UPDATE system_post SET name = '董事长' WHERE id = 1;
UPDATE system_post SET name = '项目经理' WHERE id = 2;
UPDATE system_post SET name = '普通员工' WHERE id = 4;

-- 用户昵称/备注（按官方初始化；不修改密码）
UPDATE system_users SET nickname = 'yshop', remark = '管理员' WHERE id = 1;
UPDATE system_users SET nickname = 'yixiang', remark = '不要吓我' WHERE id = 100;
UPDATE system_users SET nickname = '意向餐饮管理员', remark = '' WHERE id = 126;
