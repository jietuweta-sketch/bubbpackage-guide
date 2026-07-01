#!/usr/bin/env python3
"""Submit URLs to Google Indexing API for faster crawling."""
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = "/home/wenjun/bubbpackage-guide/key.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

URLS = [
    "https://guide.bubbpackage.com/",
    "https://guide.bubbpackage.com/beauty-skincare/",
    "https://guide.bubbpackage.com/3c-digital/",
    "https://guide.bubbpackage.com/electronics-packaging/",
    "https://guide.bubbpackage.com/food-beverage/",
    "https://guide.bubbpackage.com/ecommerce-retail/",
    "https://guide.bubbpackage.com/gift-box-custom/",
    "https://guide.bubbpackage.com/apparel-packaging/",
    "https://guide.bubbpackage.com/health-supplement-packaging/",
    "https://guide.bubbpackage.com/individual-packaging/",
    "https://guide.bubbpackage.com/custom-box-manufacturer/",
    "https://guide.bubbpackage.com/carton-customization/",
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
