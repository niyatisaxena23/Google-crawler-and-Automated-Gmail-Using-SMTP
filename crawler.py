# crawler.py - Updated to use DuckDuckGo (no blocking)
import time
import logging
import re
import csv
import requests
from bs4 import BeautifulSoup
from config import (
    SEARCH_QUERIES, MAX_RESULTS_PER_QUERY,
    CRAWL_DELAY_SECONDS, USER_AGENT, OUTPUT_CSV
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("hackveda.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def fetch_duckduckgo_results(query, num_results=10):
    """Fetch search results from DuckDuckGo HTML search"""
    results = []

    try:
        log.info(f"Searching: '{query}'")

        url = "https://html.duckduckgo.com/html/"
        params = {"q": query, "kl": "in-en"}  # India region

        response = requests.post(url, data=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # DuckDuckGo results are in <div class="result">
        for result in soup.select(".result")[:num_results]:
            title_tag   = result.select_one(".result__title")
            url_tag     = result.select_one(".result__url")
            snippet_tag = result.select_one(".result__snippet")

            if not title_tag:
                continue

            # Build full URL
            href = title_tag.find("a")
            if not href:
                continue

            link = href.get("href", "")
            if link.startswith("//duckduckgo.com"):
                continue

            results.append({
                "title":   title_tag.get_text(strip=True),
                "url":     "https://" + url_tag.get_text(strip=True) if url_tag else link,
                "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
            })

        log.info(f"Found {len(results)} results for '{query}'")

    except Exception as e:
        log.error(f"Search failed for '{query}': {e}")

    return results


def extract_emails_from_url(url):
    emails = []
    try:
        if not url.startswith("http"):
            url = "https://" + url
        response = requests.get(url, headers=HEADERS, timeout=8)
        found = EMAIL_REGEX.findall(response.text)
        emails = list({
            e for e in found
            if not e.endswith((".png", ".jpg", ".css", ".js", ".svg"))
        })
    except Exception as e:
        log.warning(f"Could not fetch {url}: {e}")
    return emails


def crawl_all_queries():
    all_leads = []

    for query in SEARCH_QUERIES:
        results = fetch_duckduckgo_results(query, MAX_RESULTS_PER_QUERY)

        for item in results:
            time.sleep(CRAWL_DELAY_SECONDS)
            emails = extract_emails_from_url(item["url"])

            lead = {
                "query":   query,
                "title":   item["title"],
                "url":     item["url"],
                "snippet": item["snippet"],
                "emails":  ", ".join(emails) if emails else "N/A",
            }
            all_leads.append(lead)
            log.info(f"Lead: {item['title']} | Emails: {emails or 'none'}")

        time.sleep(CRAWL_DELAY_SECONDS * 2)

    return all_leads


def save_leads_to_csv(leads, filepath=OUTPUT_CSV):
    if not leads:
        log.warning("No leads to save.")
        return

    fieldnames = ["query", "title", "url", "snippet", "emails"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)

    log.info(f"Saved {len(leads)} leads to '{filepath}'")


if __name__ == "__main__":
    leads = crawl_all_queries()
    save_leads_to_csv(leads)
    print(f"\n✅ Done! {len(leads)} leads saved to {OUTPUT_CSV}")