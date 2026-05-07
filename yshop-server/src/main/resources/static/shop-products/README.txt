商品缩略图目录（按商品 id 命名：<id>.png）

生成方式：
  cd yshop-drink-boot3
  pip install Pillow
  python scripts/generate_shop_product_thumbnails.py

访问 URL（local 默认端口 48081）：
  http://127.0.0.1:48081/shop-products/<id>.png

数据库字段更新见 sql/update-shop-product-images-from-static.sql
