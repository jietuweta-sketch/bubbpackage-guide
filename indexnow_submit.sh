#!/bin/bash
# Notify IndexNow participants after guide pages are added or updated.

set -euo pipefail

HOST="guide.bubbpackage.com"
KEY_FILE="70ab5436820143a9a24d6afb3580ee18.txt"
KEY=$(tr -d '\r\n' < "$KEY_FILE")
KEY_LOCATION="https://${HOST}/${KEY_FILE}"

mapfile -t URLS < <(sed -n 's|.*<loc>\(https://guide\.bubbpackage\.com[^<]*\)</loc>.*|\1|p' sitemap.xml)

if [ "${#URLS[@]}" -eq 0 ]; then
  echo "No guide URLs found in sitemap.xml" >&2
  exit 1
fi

accepted=0
for url in "${URLS[@]}"; do
  status=$(curl --silent --show-error --output /tmp/indexnow-response.txt --write-out "%{http_code}" \
    --get "https://api.indexnow.org/indexnow" \
    --data-urlencode "url=${url}" \
    --data-urlencode "key=${KEY}" \
    --data-urlencode "keyLocation=${KEY_LOCATION}")

  if [ "$status" = "200" ] || [ "$status" = "202" ]; then
    echo "Accepted (${status}): ${url}"
    accepted=$((accepted + 1))
  else
    echo "IndexNow rejected ${url} with HTTP ${status}" >&2
    cat /tmp/indexnow-response.txt >&2
    exit 1
  fi
done

echo "IndexNow accepted ${accepted}/${#URLS[@]} guide URLs."
