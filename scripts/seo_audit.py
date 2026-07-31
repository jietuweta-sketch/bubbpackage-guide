#!/usr/bin/env python3
"""Validate core SEO metadata, JSON-LD and sitemap coverage."""

from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("**/index.html"))
ERRORS = []
TITLES = {}
DESCRIPTIONS = {}


for path in HTML_FILES:
    text = path.read_text(encoding="utf-8")
    titles = re.findall(r"<title>(.*?)</title>", text, re.S)
    descriptions = re.findall(
        r'<meta\s+name="description"\s+content="([^"]+)"', text
    )
    canonicals = re.findall(
        r'<link\s+rel="canonical"\s+href="([^"]+)"', text
    )
    h1s = re.findall(r"<h1(?:\s[^>]*)?>(.*?)</h1>", text, re.S)

    counts = {
        "title": len(titles),
        "description": len(descriptions),
        "canonical": len(canonicals),
        "h1": len(h1s),
    }
    if any(value != 1 for value in counts.values()):
        ERRORS.append(f"{path.relative_to(ROOT)} metadata counts: {counts}")

    if titles:
        if titles[0] in TITLES:
            ERRORS.append(f"Duplicate title: {titles[0]}")
        TITLES[titles[0]] = path

    if descriptions:
        if descriptions[0] in DESCRIPTIONS:
            ERRORS.append(f"Duplicate description: {descriptions[0]}")
        DESCRIPTIONS[descriptions[0]] = path

    for block in re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.S
    ):
        try:
            json.loads(block)
        except json.JSONDecodeError as error:
            ERRORS.append(
                f"{path.relative_to(ROOT)} invalid JSON-LD: {error}"
            )


namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
sitemap = ET.parse(ROOT / "sitemap.xml")
sitemap_urls = [
    element.text for element in sitemap.findall(".//s:loc", namespace)
]
expected_urls = []

for path in HTML_FILES:
    relative = path.relative_to(ROOT)
    if relative.as_posix() == "index.html":
        expected_urls.append("https://guide.bubbpackage.com/")
    else:
        expected_urls.append(
            f"https://guide.bubbpackage.com/{relative.parent.as_posix()}/"
        )

missing = set(expected_urls) - set(sitemap_urls)
extra = set(sitemap_urls) - set(expected_urls)
if missing or extra:
    ERRORS.append(f"Sitemap mismatch. Missing={missing}; extra={extra}")

print(f"HTML pages: {len(HTML_FILES)}")
print(f"Sitemap URLs: {len(sitemap_urls)}")
print(
    f"Unique titles: {len(TITLES)}; "
    f"unique descriptions: {len(DESCRIPTIONS)}"
)

if ERRORS:
    print("Errors:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("Errors: none")
