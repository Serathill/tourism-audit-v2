#!/usr/bin/env python3
"""
GSC API - Check indexing status + submit sitemap for audit-turism.ro.

Setup (one-time):
  1. GCP project: cohesive-idiom-398915
  2. Search Console API: enabled
  3. Service Account: gsc-indexing@cohesive-idiom-398915.iam.gserviceaccount.com
  4. SA key: tools/gsc-sa-key.json (gitignored, copy from devidevs-frontend/tools/)
  5. SA added to GSC property sc-domain:audit-turism.ro with Owner permission
  6. pip install google-auth google-api-python-client requests

Usage:
  python3 tools/gsc-check.py                    # Check all URLs
  python3 tools/gsc-check.py --submit-sitemap   # Submit sitemap first, then check
  python3 tools/gsc-check.py --not-indexed       # Show only non-indexed
"""

import argparse
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install google-auth google-api-python-client requests")
    sys.exit(1)

import requests

SCOPES = ["https://www.googleapis.com/auth/webmasters"]
SITE_URL = "sc-domain:audit-turism.ro"
SITEMAP_URL = "https://audit-turism.ro/sitemap.xml"
TOOLS_DIR = Path(__file__).parent
SA_KEY_FILE = TOOLS_DIR / "gsc-sa-key.json"

RATE_LIMIT_DELAY = 0.3


def authenticate():
    if not SA_KEY_FILE.exists():
        print(f"Error: {SA_KEY_FILE} not found.")
        print()
        print("Copy from devidevs-frontend:")
        print("  cp ../devidevs-frontend/tools/gsc-sa-key.json tools/gsc-sa-key.json")
        print()
        print("SA email: gsc-indexing@cohesive-idiom-398915.iam.gserviceaccount.com")
        print("Must be added as Owner on sc-domain:audit-turism.ro in Search Console")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(
        str(SA_KEY_FILE), scopes=SCOPES
    )
    return creds


def get_sitemap_urls():
    resp = requests.get(SITEMAP_URL, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//sm:loc", ns)]


def inspect_url(service, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = (
                service.urlInspection()
                .index()
                .inspect(body={"inspectionUrl": url, "siteUrl": SITE_URL})
                .execute()
            )
            inspection = result.get("inspectionResult", {})
            index_status = inspection.get("indexStatusResult", {})
            return {
                "url": url,
                "verdict": index_status.get("verdict", "UNKNOWN"),
                "coverage_state": index_status.get("coverageState", "UNKNOWN"),
                "last_crawl_time": index_status.get("lastCrawlTime", ""),
                "error": None,
            }
        except Exception as e:
            err_str = str(e)
            if ("500" in err_str or "503" in err_str) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {
                "url": url,
                "verdict": "ERROR",
                "coverage_state": err_str[:80],
                "last_crawl_time": "",
                "error": err_str,
            }


def main():
    parser = argparse.ArgumentParser(description="GSC indexing check for audit-turism.ro")
    parser.add_argument("--submit-sitemap", action="store_true", help="Submit sitemap before checking")
    parser.add_argument("--not-indexed", action="store_true", help="Show only non-indexed URLs")
    args = parser.parse_args()

    print("Authenticating...")
    creds = authenticate()
    service = build("searchconsole", "v1", credentials=creds)

    if args.submit_sitemap:
        print(f"Submitting sitemap: {SITEMAP_URL}")
        service.sitemaps().submit(siteUrl=SITE_URL, feedpath=SITEMAP_URL).execute()
        print("Sitemap submitted!")
        print()

    print("Fetching sitemap URLs...")
    urls = get_sitemap_urls()
    print(f"Found {len(urls)} URLs\n")

    print(f"{'VERDICT':8s} | {'STATE':40s} | {'CRAWLED':10s} | URL")
    print("-" * 100)

    indexed = 0
    for i, url in enumerate(urls, 1):
        result = inspect_url(service, url)
        crawl = result["last_crawl_time"][:10] if result["last_crawl_time"] else "never"
        verdict = result["verdict"]

        if verdict == "PASS":
            indexed += 1

        if args.not_indexed and verdict == "PASS":
            continue

        print(f"{verdict:8s} | {result['coverage_state'][:40]:40s} | {crawl:10s} | {url}")
        time.sleep(RATE_LIMIT_DELAY)

    print("-" * 100)
    print(f"Total: {len(urls)} | Indexed: {indexed} | Not indexed: {len(urls) - indexed}")


if __name__ == "__main__":
    main()
