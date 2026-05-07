#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为每个商品生成小尺寸烧烤风缩略图（Pillow 程序化绘制，无需逐张人工确认）。

依赖安装:
  pip install Pillow
可选（连库更新）:
  pip install PyMySQL

用法示例:
  cd yshop-drink-boot3
  python scripts/generate_shop_product_thumbnails.py

  # 从 SQL 导出文件读取商品（默认）
  python scripts/generate_shop_product_thumbnails.py --sql sql/yixiang-drink-open.sql

  # 从本机 MySQL 读取（需与 application-local 一致）
  python scripts/generate_shop_product_thumbnails.py --mysql --mysql-host 127.0.0.1 --mysql-user root --mysql-password root --mysql-db yixiang-drink-open

  # 生成图后并直接 UPDATE 数据库
  python scripts/generate_shop_product_thumbnails.py --mysql ... --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------- paths ----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
BOOT3_ROOT = SCRIPT_DIR.parent
DEFAULT_SQL = BOOT3_ROOT / "sql" / "yixiang-drink-open.sql"
OUT_DIR = BOOT3_ROOT / "yshop-server" / "src" / "main" / "resources" / "static" / "shop-products"
SQL_OUT = BOOT3_ROOT / "sql" / "update-shop-product-images-from-static.sql"

SIZE = 280


def parse_mysql_values_tuple(inner: str) -> list[str]:
    """Parse one row inside VALUES (...); handles '...' strings, NULL, numbers, b'0'."""
    parts: list[str] = []
    i = 0
    n = len(inner)
    while i < n:
        while i < n and inner[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        if inner.startswith("NULL", i) and (i + 4 >= n or inner[i + 4] in ",)"):
            parts.append("NULL")
            i += 4
        elif inner[i] == "'":
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = inner[j]
                if c == "\\" and j + 1 < n:
                    buf.append(inner[j + 1])
                    j += 2
                    continue
                if c == "'":
                    if j + 1 < n and inner[j + 1] == "'":
                        buf.append("'")
                        j += 2
                        continue
                    break
                buf.append(c)
                j += 1
            parts.append("".join(buf))
            i = j + 1
        elif inner.startswith("b'", i):
            j = inner.find("'", i + 2)
            if j < 0:
                raise ValueError("unterminated bit literal")
            parts.append(inner[i : j + 1])
            i = j + 1
        else:
            j = i
            while j < n and inner[j] not in ",)":
                j += 1
            parts.append(inner[i:j].strip())
            i = j
        while i < n and inner[i] in " \t\r\n":
            i += 1
        if i < n and inner[i] == ",":
            i += 1
    return parts


def load_products_from_sql(sql_path: Path) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    pat = re.compile(r"INSERT INTO `yshop_store_product` VALUES\s*\((.*)\)\s*;\s*$", re.IGNORECASE)
    for line in sql_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if "INSERT INTO `yshop_store_product`" not in line:
            continue
        m = pat.search(line)
        if not m:
            continue
        inner = m.group(1)
        try:
            vals = parse_mysql_values_tuple(inner)
        except Exception as e:
            print(f"skip malformed INSERT: {e}", file=sys.stderr)
            continue
        if len(vals) < 6:
            continue
        try:
            pid = int(vals[0].strip())
        except ValueError:
            continue
        store_name = vals[5].strip() or f"商品{pid}"
        rows.append((pid, store_name))
    rows.sort(key=lambda x: x[0])
    return rows


def load_products_mysql(args: argparse.Namespace) -> list[tuple[int, str]]:
    import pymysql

    conn = pymysql.connect(
        host=args.mysql_host,
        port=args.mysql_port,
        user=args.mysql_user,
        password=args.mysql_password,
        database=args.mysql_db,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, store_name FROM yshop_store_product WHERE deleted = 0 ORDER BY id"
            )
            return [(int(r[0]), (r[1] or "").strip() or f"商品{r[0]}") for r in cur.fetchall()]
    finally:
        conn.close()


def pick_font(size: int):
    from PIL import ImageFont

    candidates = [
        os.environ.get("YSHOP_PRODUCT_FONT"),
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for p in candidates:
        if not p:
            continue
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """h:0-360 s,v:0-1"""
    import colorsys

    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def _wrap_name_lines(name: str, max_chars: int, max_lines: int) -> list[str]:
    s = (name or "").strip() or "商品"
    lines: list[str] = []
    for k in range(max_lines):
        start = k * max_chars
        if start >= len(s):
            break
        if k == max_lines - 1 and len(s) > start + max_chars:
            lines.append(s[start : start + max_chars - 1] + "…")
            break
        lines.append(s[start : start + max_chars])
    return lines if lines else ["商品"]


def draw_thumbnail(product_id: int, store_name: str, out_path: Path) -> None:
    from PIL import Image, ImageDraw

    # 按商品 id 微调色调，便于区分预览图
    hue = (product_id * 41) % 360
    top_c = _hsv_to_rgb(hue, 0.55, 0.95)
    bot_c = _hsv_to_rgb((hue + 25) % 360, 0.65, 0.35)

    img = Image.new("RGB", (SIZE, SIZE), top_c)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        r = int(top_c[0] + (bot_c[0] - top_c[0]) * t)
        g = int(top_c[1] + (bot_c[1] - top_c[1]) * t)
        b = int(top_c[2] + (bot_c[2] - top_c[2]) * t)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b))
    # simple "grill" bars
    for gx in range(40, SIZE - 40, 28):
        draw.rounded_rectangle([gx, SIZE // 2 + 30, gx + 18, SIZE - 35], fill=(35, 35, 35), radius=4)
    # skewer sticks
    for sx in (90, 140, 190):
        draw.line([(sx, 55), (sx + 12, SIZE // 2 + 25)], fill=(139, 90, 43), width=5)
        for k in range(3):
            cy = 75 + k * 22
            draw.ellipse([sx - 4 + k * 3, cy, sx + 14 + k * 3, cy + 12], fill=(160, 82, 45))
    # flame hint
    draw.polygon([(SIZE // 2 - 20, SIZE - 50), (SIZE // 2, SIZE - 85), (SIZE // 2 + 20, SIZE - 50)], fill=(255, 120, 40))
    draw.polygon([(SIZE // 2 - 12, SIZE - 48), (SIZE // 2, SIZE - 72), (SIZE // 2 + 12, SIZE - 48)], fill=(255, 200, 80))

    font_title = pick_font(20)
    font_small = pick_font(15)
    lines = _wrap_name_lines(store_name, max_chars=8, max_lines=3)
    line_gap = 5
    y0 = 14
    box_pad = 8
    line_heights: list[int] = []
    max_w = 0
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        max_w = max(max_w, tw)
        line_heights.append(th)
    total_h = sum(line_heights) + line_gap * (len(lines) - 1 if len(lines) > 1 else 0)
    bg_left = max(4, (SIZE - max_w) // 2 - box_pad)
    bg_right = min(SIZE - 4, bg_left + max_w + box_pad * 2)
    draw.rectangle(
        [bg_left, y0 - 4, bg_right, y0 + total_h + 6],
        fill=(20, 12, 8),
    )
    y = y0
    for i, ln in enumerate(lines):
        bbox = draw.textbbox((0, 0), ln, font=font_title)
        tw = bbox[2] - bbox[0]
        tx = (SIZE - tw) // 2
        draw.text((tx, y), ln, fill=(255, 248, 220), font=font_title)
        y += line_heights[i] + (line_gap if i < len(lines) - 1 else 0)
    sub = f"#{product_id}"
    draw.text((SIZE - 52, SIZE - 28), sub, fill=(255, 220, 180), font=font_small)
    img.save(out_path, format="PNG", optimize=True)


def write_sql_file(product_ids: list[int], base_url: str) -> None:
    base = base_url.rstrip("/").replace("'", "''")
    lines = [
        "-- 由 scripts/generate_shop_product_thumbnails.py 生成",
        "-- 每条语句独立，避免 JDBC allowMultiQueries=false 时 SET 与 UPDATE 同批报错",
        "-- 真机请将 URL 中主机改为局域网 IP，例如 http://192.168.1.10:48081",
        "",
    ]
    for pid in product_ids:
        u = f"{base}/shop-products/{pid}.png"
        lines.append(
            f"UPDATE yshop_store_product SET image = '{u}', slider_image = '{u}' WHERE id = {pid};"
        )
    SQL_OUT.parent.mkdir(parents=True, exist_ok=True)
    SQL_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SQL_OUT}")


def apply_mysql(args: argparse.Namespace, product_ids: list[int], base_url: str) -> None:
    import pymysql

    conn = pymysql.connect(
        host=args.mysql_host,
        port=args.mysql_port,
        user=args.mysql_user,
        password=args.mysql_password,
        database=args.mysql_db,
        charset="utf8mb4",
    )
    base = base_url.rstrip("/")
    try:
        with conn.cursor() as cur:
            for pid in product_ids:
                url = f"{base}/shop-products/{pid}.png"
                cur.execute(
                    "UPDATE yshop_store_product SET image = %s, slider_image = %s WHERE id = %s",
                    (url, url, pid),
                )
        conn.commit()
        print(f"Applied UPDATE for {len(product_ids)} products.")
    finally:
        conn.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate BBQ-style product thumbnails per id.")
    ap.add_argument("--sql", type=Path, default=DEFAULT_SQL, help="Path to yixiang-drink-open.sql")
    ap.add_argument("--base-url", default="http://127.0.0.1:48081", help="Public base URL for SQL file")
    ap.add_argument("--mysql", action="store_true", help="Load products from MySQL instead of SQL file")
    ap.add_argument("--mysql-host", default="127.0.0.1")
    ap.add_argument("--mysql-port", type=int, default=3306)
    ap.add_argument("--mysql-user", default="root")
    ap.add_argument("--mysql-password", default="root")
    ap.add_argument("--mysql-db", default="yixiang-drink-open")
    ap.add_argument("--apply", action="store_true", help="Run UPDATE on MySQL (--mysql required)")
    args = ap.parse_args()

    if args.mysql or args.apply:
        try:
            import pymysql  # noqa: F401
        except ImportError:
            print("Install PyMySQL: pip install PyMySQL", file=sys.stderr)
            return 1

    if args.apply and not args.mysql:
        print("--apply requires --mysql", file=sys.stderr)
        return 1

    if args.mysql:
        products = load_products_mysql(args)
    else:
        if not args.sql.is_file():
            print(f"SQL file not found: {args.sql}", file=sys.stderr)
            return 1
        products = load_products_from_sql(args.sql)

    if not products:
        print("No products found.", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # keep directory in git with .gitkeep if empty — we add readme in shop-products
    for pid, name in products:
        out_path = OUT_DIR / f"{pid}.png"
        draw_thumbnail(pid, name, out_path)
        print(f"Wrote {out_path.name} ({name})")

    ids = [p[0] for p in products]
    write_sql_file(ids, args.base_url)

    if args.apply:
        apply_mysql(args, ids, args.base_url)

    return 0


if __name__ == "__main__":
    sys.exit(main())
