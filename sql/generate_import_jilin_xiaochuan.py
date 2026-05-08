# -*- coding: utf-8 -*-
"""One-off generator for import-jilin-xiaochuan-menu.sql — run: python generate_import_jilin_xiaochuan.py"""
import hashlib
import json
from datetime import datetime

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Category id block (explicit ids after wipe)
CAT_IDS = list(range(9001, 9010))  # 9001..9009

CATEGORIES = [
    (9001, 1, "肉类", None),
    (9002, 2, "成把类", None),
    (9003, 3, "鱼类", None),
    (9004, 4, "肠类", None),
    (9005, 5, "素菜类", None),
    (9006, 6, "主食/凉菜类", None),
    (9007, 7, "锡纸类", None),
    (9008, 8, "小龙虾类", None),
    (9009, 9, "特殊预定类", "每天17:00前可预订"),
]

# (cate_idx 0..8, name, price, unit, description or None)
# cate_idx maps to CAT_IDS[cate_idx]
PRODUCTS = []
MEAT = 0
BUNDLE = 1
FISH = 2
SAUSAGE = 3
VEG = 4
STAPLE = 5
FOIL = 6
CRAYFISH = 7
SPECIAL = 8

def p(cat_i, name, price, unit, desc=None):
    PRODUCTS.append((cat_i, name, price, unit, desc))

# 肉类
for item in [
    ("羊排肉", 4, "串"),
    ("牛肥瘦", 4, "串"),
    ("酱油筋", 3, "串"),
    ("五花肉", 3, "串"),
    ("宫后夹肉", 5, "串"),
    ("油边", 10, "串"),
    ("雪花牛肉粒", 5, "串"),
    ("一根筋", 5, "串"),
    ("腰子", 10, "串"),
    ("牛窝骨筋", 10, "串"),
    ("筋皮子", 5, "串"),
    ("牛板筋", 4, "串"),
    ("鸡胗", 3, "串"),
    ("鸡心", 3, "串"),
    ("千层筋", 5, "串"),
    ("鸡爪", 8, "串"),
    ("五花肉卷酸菜", 5, "串"),
    ("风干油边", 10, "串"),
    ("肥肠", 5, "串"),
    ("大梅花肉", 6, "串"),
    ("蚂蚱", 5, "串"),
    ("鸡翅", 8, "串"),
    ("鸡皮", 3, "串"),
    ("掌中宝", 3, "串"),
    ("多味鱼", 5, "串"),
]:
    p(MEAT, item[0], item[1], item[2])

# 成把类
for item in [
    ("玉米粒", 6, "把"),
    ("腊肠", 8, "把"),
    ("鸭肠", 10, "把"),
    ("小肉串", 10, "把"),
    ("牛油", 10, "把"),
    ("牛肚", 10, "把"),
    ("鸡肉干豆腐", 8, "把"),
]:
    p(BUNDLE, item[0], item[1], item[2])

# 鱼类
for item in [
    ("鱿鱼", 8, "串"),
    ("秋刀鱼", 10, "串"),
    ("鱿鱼须", 5, "串"),
    ("酱烤明太鱼", 15, "条"),
]:
    p(FISH, item[0], item[1], item[2])

# 肠类
for item in [
    ("火山石烤肠", 5, "串"),
    ("淀粉肠", 2, "串"),
]:
    p(SAUSAGE, item[0], item[1], item[2])

# 素菜类
for item in [
    ("小饼", 2, "串"),
    ("包浆豆腐", 2, "串"),
    ("年糕", 2, "串"),
    ("辣椒", 3, "串"),
    ("菜卷", 3, "串"),
    ("香菇", 2, "串"),
    ("吐司", 3, "串"),
    ("臭干", 3, "串"),
    ("苕皮", 5, "串"),
    ("面筋", 2, "串"),
    ("韭菜", 3, "串"),
    ("蘑菇", 1, "串"),
    ("娃娃菜", 2, "串"),
    ("土豆片", 2, "串"),
    ("金针菇", 2, "串"),
    ("包菜", 2, "串"),
    ("西葫芦", 2, "串"),
    ("蒜薹", 3, "串"),
]:
    p(VEG, item[0], item[1], item[2])
p(VEG, "烤茄子", 18, "串", "可加粉丝")

# 主食/凉菜类
p(STAPLE, "凉拌面（方便面）", 10, "份", None)
p(
    STAPLE,
    "炒面",
    11,
    "份",
    "默认加蛋；加淀粉肠+2元；加王中王+5元",
)
for item in [
    ("拍黄瓜", 12, "份"),
    ("皮蛋豆腐", 12, "份"),
    ("油炸花生米", 8, "份"),
    ("水煮花生", 10, "份"),
]:
    p(STAPLE, item[0], item[1], item[2])

# 锡纸类
for item in [
    ("锡纸金针菇", 10, "份"),
    ("锡纸娃娃菜", 10, "份"),
    ("锡纸鸭血", 12, "份"),
    ("锡纸方便面", 10, "份"),
]:
    p(FOIL, item[0], item[1], item[2])

# 小龙虾类 — 合并一条
p(
    CRAYFISH,
    "小龙虾",
    100,
    "份",
    "口味：蒜蓉/十三香/香辣/麻辣；三斤足称。可加年糕/手擀面/方便面 +5/份。",
)

# 特殊预定类
for item in [
    ("锡纸烤鱼（鲫鱼或鳊鱼）", 35, "份", None),
    ("铁板鲫鱼", 38, "份", None),
    ("生蚝/扇贝", 10, "个", None),
]:
    p(SPECIAL, item[0], item[1], item[2], item[3])


def esc_sql(s):
    if s is None:
        return "NULL"
    return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"


def html_desc(text):
    if not text:
        return "NULL"
    inner = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return esc_sql(f"<p>{inner}</p>")


def uniq(pid):
    return hashlib.md5(f"yshop-sku-{pid}".encode()).hexdigest()


def attr_result_json(price, placeholder_img=""):
    """Single-SKU JSON aligned with demo product id=18 style."""
    pr = float(price)
    obj = {
        "attr": [
            {
                "attrHidden": "",
                "detail": ["默认"],
                "detailValue": "",
                "value": "规格",
            }
        ],
        "value": [
            {
                "barCode": "",
                "brokerage": 0.0,
                "brokerageTwo": 0.0,
                "cost": pr,
                "detail": {"规格": "默认"},
                "integral": 0,
                "otPrice": pr,
                "pic": placeholder_img,
                "pinkPrice": 0.0,
                "pinkStock": 0,
                "price": pr,
                "seckillPrice": 0.0,
                "seckillStock": 0,
                "sku": "",
                "stock": 9999,
                "value1": "规格",
                "value2": "",
                "volume": 0.0,
                "weight": 0.0,
            }
        ],
    }
    # Compact JSON for SQL — escape single quotes
    j = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return esc_sql(j)


OUT = []
ap = OUT.append

ap("-- =====================================================================")
ap("-- 吉林小串：清空门店/商品相关演示数据并导入菜单（MySQL）")
ap("-- 执行前请备份数据库。按需修改以下会话变量：")
ap("-- 若库中无表 yshop_store_cart，请注释掉下文 DELETE FROM yshop_store_cart。")
ap("-- =====================================================================")
ap("SET NAMES utf8mb4;")
ap("SET @tenant_id := 1;")
ap("-- 门店管理员用户 id（system_users.id），默认 1；请改为实际账号")
ap("SET @admin_user_id := '1';")
ap("-- 占位图（商品主图/轮播，NOT NULL；可改为你的 CDN 地址）")
ap("SET @placeholder_img := '';")
ap("")
ap("START TRANSACTION;")
ap("")
ap("-- ----- 可选：清空订单（演示环境推荐） -----")
ap("DELETE FROM yshop_store_order_status WHERE 1=1;")
ap("DELETE FROM yshop_store_order_cart_info WHERE 1=1;")
ap("DELETE FROM yshop_store_order WHERE 1=1;")
ap("DELETE FROM yshop_order_number WHERE 1=1;")
ap("")
ap("-- ----- 购物车 -----")
ap("DELETE FROM yshop_store_cart WHERE 1=1;")
ap("")
ap("-- ----- 商品从表 -----")
ap("DELETE FROM yshop_store_product_attr_value WHERE 1=1;")
ap("DELETE FROM yshop_store_product_attr WHERE 1=1;")
ap("DELETE FROM yshop_store_product_attr_result WHERE 1=1;")
ap("DELETE FROM yshop_store_product_relation WHERE 1=1;")
ap("-- 若存在评论表则清空")
ap("DELETE FROM yshop_store_product_reply WHERE 1=1;")
ap("")
ap("-- ----- 商品与分类 -----")
ap("DELETE FROM yshop_store_product WHERE 1=1;")
ap("DELETE FROM yshop_store_product_category WHERE 1=1;")
ap("")
ap("-- ----- 广告（含吉林小串店铺） -----")
ap("DELETE FROM yshop_shop_ads WHERE 1=1;")
ap("")
ap("-- ----- 仅保留即将插入的门店：删除全部旧门店 -----")
ap("DELETE FROM yshop_store_shop WHERE 1=1;")
ap("")
ap("-- ----- 插入唯一门店「吉林小串」 -----")
ap(
    "INSERT INTO yshop_store_shop ("
    "id, name, mobile, image, images, address, address_map, start_time, end_time, "
    "lng, lat, distance, min_price, delivery_price, notice, status, admin_id, uniprint_id, "
    "create_time, update_time, creator, updater"
    ") VALUES ("
    "1, "
    + esc_sql("吉林小串")
    + ", "
    + esc_sql("19000000000")
    + ", "
    "@placeholder_img, "
    + esc_sql("[]")
    + ", "
    + esc_sql("吉林省")
    + ", "
    + esc_sql("吉林省")
    + ", "
    + esc_sql("2024-01-01 11:00:00")
    + ", "
    + esc_sql("2024-01-01 23:00:00")
    + ", "
    + esc_sql("126.549572")
    + ", "
    + esc_sql("43.837883")
    + ", "
    "10, 0.00, 3.00, "
    + esc_sql("吉林小串欢迎您")
    + ", "
    "1, @admin_user_id, '', "
    + esc_sql(NOW)
    + ", "
    + esc_sql(NOW)
    + ", '1', '1'"
    ");"
)
ap("")
ap("SET @shop_id := 1;")
ap("-- 与插入的门店 id 对齐 AUTO_INCREMENT（避免后续手动插入 id 冲突）")
ap("ALTER TABLE yshop_store_shop AUTO_INCREMENT = 2;")
ap("")

# Categories
ap("-- ----- 9 个一级分类 -----")
for cid, sort_order, cname, cdesc in CATEGORIES:
    dsql = esc_sql(cdesc) if cdesc else "NULL"
    pic = "''"
    ap(
        f"INSERT INTO yshop_store_product_category ("
        f"id, shop_id, parent_id, shop_name, name, pic_url, sort, description, status, "
        f"creator, create_time, updater, update_time, deleted, tenant_id"
        f") VALUES ("
        f"{cid}, @shop_id, 0, '吉林小串', {esc_sql(cname)}, {pic}, {sort_order}, {dsql}, 0, "
        f"'1', {esc_sql(NOW)}, '1', {esc_sql(NOW)}, b'0', @tenant_id"
        f");"
    )

ap("")
ap("-- ----- 商品（单规格 spec_type=0） -----")
PID_START = 30001
pid = PID_START
attr_id_base = 800000
res_id_base = 810000
val_id_base = 820000

for idx, (cat_i, pname, price, unit, pdesc) in enumerate(PRODUCTS):
    pid_current = pid + idx
    cate_str = str(CAT_IDS[cat_i])
    sort_in_cat = sum(1 for x in PRODUCTS[: idx + 1] if x[0] == cat_i)
    store_info = pname[: min(256, len(pname))]
    keyword = pname[: min(256, len(pname))]
    desc_sql = html_desc(pdesc) if pdesc else html_desc(pname)

    ap(
        f"INSERT INTO yshop_store_product ("
        f"id, shop_id, shop_name, image, slider_image, store_name, store_info, keyword, bar_code, brand_id, "
        f"cate_id, price, vip_price, ot_price, postage, unit_name, sort, sales, stock, is_show, "
        f"is_hot, is_benefit, is_best, is_new, description, creator, create_time, update_time, updater, "
        f"is_postage, deleted, mer_use, give_integral, cost, is_seckill, is_bargain, is_good, ficti, browse, "
        f"code_path, is_sub, temp_id, spec_type, is_integral, integral, tenant_id"
        f") VALUES ("
        f"{pid_current}, @shop_id, '吉林小串', @placeholder_img, @placeholder_img, "
        f"{esc_sql(pname)}, {esc_sql(store_info)}, {esc_sql(keyword)}, '', NULL, "
        f"{esc_sql(cate_str)}, {price:.2f}, 0.00, {price:.2f}, 0.00, {esc_sql(unit)}, {sort_in_cat}, 0, 9999, 1, "
        f"0, 0, 0, 0, {desc_sql}, '1', {esc_sql(NOW)}, {esc_sql(NOW)}, '1', "
        f"0, b'0', 0, NULL, {price:.2f}, 0, NULL, 0, 100, 0, "
        f"'', 0, 0, 0, 0, 0, @tenant_id"
        f");"
    )

    aid = attr_id_base + idx
    rid = res_id_base + idx
    vid = val_id_base + idx
    u = uniq(pid_current)

    ap(
        f"INSERT INTO yshop_store_product_attr (id, product_id, attr_name, attr_values) VALUES "
        f"({aid}, {pid_current}, '规格', '默认');"
    )
    ap(
        f"INSERT INTO yshop_store_product_attr_result (id, product_id, result, change_time) VALUES "
        f"({rid}, {pid_current}, {attr_result_json(price)}, {esc_sql(NOW)});"
    )
    ap(
        f"INSERT INTO yshop_store_product_attr_value ("
        f"id, product_id, sku, stock, sales, price, image, `unique`, cost, bar_code, ot_price, "
        f"weight, volume, brokerage, brokerage_two, pink_price, pink_stock, seckill_price, seckill_stock, integral"
        f") VALUES ("
        f"{vid}, {pid_current}, '默认', 9999, 0, {price:.2f}, @placeholder_img, {esc_sql(u)}, {price:.2f}, '', "
        f"{price:.2f}, 0.00, 0.00, 0.00, 0.00, 0.00, 0, 0.00, 0, 0"
        f");"
    )

next_pid = PID_START + len(PRODUCTS)
n = len(PRODUCTS)
ap("")
ap(f"ALTER TABLE yshop_store_product AUTO_INCREMENT = {next_pid};")
ap("ALTER TABLE yshop_store_product_category AUTO_INCREMENT = 9010;")
ap(f"ALTER TABLE yshop_store_product_attr AUTO_INCREMENT = {attr_id_base + n};")
ap(f"ALTER TABLE yshop_store_product_attr_result AUTO_INCREMENT = {res_id_base + n};")
ap(f"ALTER TABLE yshop_store_product_attr_value AUTO_INCREMENT = {val_id_base + n};")

ap("")
ap("COMMIT;")
ap("")
ap("-- 校验：分类 9 条、商品 "
    + str(len(PRODUCTS))
    + " 条")
ap("-- SELECT COUNT(*) FROM yshop_store_shop;")
ap("-- SELECT COUNT(*) FROM yshop_store_product_category WHERE shop_id=@shop_id;")
ap("-- SELECT COUNT(*) FROM yshop_store_product WHERE shop_id=@shop_id;")

text = "\n".join(OUT)
out_path = __file__.replace("generate_import_jilin_xiaochuan.py", "import-jilin-xiaochuan-menu.sql")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)
print("Wrote", out_path, "products:", len(PRODUCTS))
