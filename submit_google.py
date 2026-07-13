# -*- coding: utf-8 -*-
"""
Google Indexing API - 批量提交 guide.bubbpackage.com 所有页面
双击 submit_google.bat 运行
"""
import json, time, urllib.request, urllib.error, ssl

urls = [
    "https://guide.bubbpackage.com/",
    "https://guide.bubbpackage.com/beauty-skincare/",
    "https://guide.bubbpackage.com/food-beverage/",
    "https://guide.bubbpackage.com/tea-packaging/",
    "https://guide.bubbpackage.com/health-supplement-packaging/",
    "https://guide.bubbpackage.com/electronics-packaging/",
    "https://guide.bubbpackage.com/apparel-packaging/",
    "https://guide.bubbpackage.com/gift-box-custom/",
    "https://guide.bubbpackage.com/ecommerce-retail/",
    "https://guide.bubbpackage.com/individual-packaging/",
    "https://guide.bubbpackage.com/3c-digital/",
    "https://guide.bubbpackage.com/carton-customization/",
    "https://guide.bubbpackage.com/xiaopiliang-baozhuang-dingzhi/",
]

# Read service account key
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(script_dir, "key.json")

with open(key_path) as f:
    key_data = json.load(f)

# Get OAuth2 token
import jwt

iat = int(time.time())
exp = iat + 3600

jwt_claims = {
    "iss": key_data["client_email"],
    "scope": "https://www.googleapis.com/auth/indexing",
    "aud": "https://oauth2.googleapis.com/token",
    "iat": iat,
    "exp": exp
}

signed_jwt = jwt.encode(jwt_claims, key_data["private_key"], algorithm="RS256")

token_data = urllib.parse.urlencode({
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": signed_jwt
}).encode()

ctx = ssl.create_default_context()
req = urllib.request.Request(
    "https://oauth2.googleapis.com/token",
    data=token_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    access_token = json.loads(resp.read())["access_token"]
    print("OAuth2 token OK\n")
except Exception as e:
    print(f"Token FAILED: {e}")
    print("Check proxy is running (127.0.0.1:10808)")
    input("Press Enter...")
    exit(1)

# Submit URLs
ok = 0
fail = 0
for i, url in enumerate(urls, 1):
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        result = json.loads(resp.read())
        print(f"  [{i}/12] OK  {url}")
        ok += 1
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  [{i}/12] ERR {e.code}  {url}")
        fail += 1
    except Exception as e:
        print(f"  [{i}/12] ERR {e}  {url}")
        fail += 1
    time.sleep(0.3)

print(f"\nDone! OK={ok} FAIL={fail}")
input("Press Enter...")
