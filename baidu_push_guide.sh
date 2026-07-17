#!/bin/bash
# 百度搜索资源平台 API 推送 — guide.bubbpackage.com 全部落地页
# 用法: BAIDU_GUIDE_TOKEN="平台生成的新 token" bash baidu_push_guide.sh

set -euo pipefail

if [ -z "${BAIDU_GUIDE_TOKEN:-}" ]; then
  echo "缺少 BAIDU_GUIDE_TOKEN。请先在百度搜索资源平台重新生成 token，并通过环境变量提供。" >&2
  exit 1
fi

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
  "https://data.zz.baidu.com/urls?site=guide.bubbpackage.com&token=${BAIDU_GUIDE_TOKEN}" \
  -H "Content-Type: text/plain" \
  --data-binary "$BODY"
