#!/bin/bash
# 百度站长 API 推送 — guide.bubbpackage.com 全部落地页
# token: ix2iHNHIeVj71uvK
# 用法: bash baidu_push_guide.sh

URLS=(
  "https://guide.bubbpackage.com/"
  "https://guide.bubbpackage.com/beauty-skincare/"
  "https://guide.bubbpackage.com/3c-digital/"
  "https://guide.bubbpackage.com/electronics-packaging/"
  "https://guide.bubbpackage.com/food-beverage/"
  "https://guide.bubbpackage.com/ecommerce-retail/"
  "https://guide.bubbpackage.com/tea-packaging/"
  "https://guide.bubbpackage.com/apparel-packaging/"
  "https://guide.bubbpackage.com/gift-box-custom/"
  "https://guide.bubbpackage.com/health-supplement-packaging/"
  "https://guide.bubbpackage.com/carton-customization/"
  "https://guide.bubbpackage.com/individual-packaging/"
  "https://guide.bubbpackage.com/xiaopiliang-baozhuang-dingzhi/"
)

BODY=$(printf "%s\n" "${URLS[@]}")

curl -s -w "\nHTTP:%{http_code}" -X POST \
  "http://data.zz.baidu.com/urls?site=guide.bubbpackage.com&token=ix2iHNHIeVj71uvK" \
  -H "Content-Type: text/plain" \
  --data-binary "$BODY"
