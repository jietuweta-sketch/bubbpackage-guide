#!/bin/bash
# 补推 guide 剩余 4 个 URL
curl -s -X POST "http://data.zz.baidu.com/urls?site=guide.bubbpackage.com&token=ix2iHNHIeVj71uvK" \
  -H "Content-Type: text/plain" \
  -d "https://guide.bubbpackage.com/tea-packaging/
https://guide.bubbpackage.com/apparel-packaging/
https://guide.bubbpackage.com/gift-box-custom/
https://guide.bubbpackage.com/health-supplement-packaging/"
