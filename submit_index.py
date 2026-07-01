#!/usr/bin/env python3
"""Submit URLs to Google Indexing API for faster crawling."""
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = "/home/wenjun/bubbpackage-guide/key.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

URLS = [
    "https://bubbpackage.com/guide/",
    "https://bubbpackage.com/guide/beauty-skincare/",
    "https://bubbpackage.com/guide/3c-digital/",
    "https://bubbpackage.com/guide/electronics-packaging/",
    "https://bubbpackage.com/guide/food-beverage/",
    "https://bubbpackage.com/guide/ecommerce-retail/",
    "https://bubbpackage.com/guide/gift-box-custom/",
    "https://bubbpackage.com/guide/apparel-packaging/",
    "https://bubbpackage.com/guide/health-supplement-packaging/",
    "https://bubbpackage.com/guide/individual-packaging/",
    "https://bubbpackage.com/guide/custom-box-manufacturer/",
    "https://bubbpackage.com/guide/carton-customization/",
]

def submit_urls():
    creds = service_account.Credentials.from_service_account_file(
        KEY_PATH, scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=creds)

    for url in URLS:
        try:
            resp = service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            notify_time = resp.get("urlNotificationMetadata", {}).get(
                "latestUpdate", {}
            ).get("notifyTime", "unknown")
            print(f"  ✓ {url}")
        except Exception as e:
            print(f"  ✗ {url}  → {e}")

    print(f"\nDone. {len(URLS)} URLs submitted.")

if __name__ == "__main__":
    submit_urls()
