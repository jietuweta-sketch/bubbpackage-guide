#!/bin/bash
# 无需 SaaS 后台权限：通过已验证的百度站点 API 提交公开主站页面。
# 用法: BAIDU_MAIN_TOKEN="平台生成的 token" bash baidu_push_main.sh

set -euo pipefail

if [ -z "${BAIDU_MAIN_TOKEN:-}" ]; then
  echo "缺少 BAIDU_MAIN_TOKEN。请从 bubbpackage.com 的普通收录 API 页面获取。" >&2
  exit 1
fi

URLS=(
  "https://bubbpackage.com/"
  "https://bubbpackage.com/help-center"
  "https://bubbpackage.com/product"
  "https://bubbpackage.com/smart-matcher"
  "https://bubbpackage.com/solutions"
)

BODY=$(printf "%s\n" "${URLS[@]}")

curl -s -w "\nHTTP:%{http_code}" -X POST \
  "https://data.zz.baidu.com/urls?site=bubbpackage.com&token=${BAIDU_MAIN_TOKEN}" \
  -H "Content-Type: text/plain" \
  --data-binary "$BODY"
