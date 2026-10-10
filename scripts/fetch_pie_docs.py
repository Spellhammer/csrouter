"""Snapshot public Pie Calendar articles for local dataset preparation (stdlib only)."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import ssl
import time
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://docs.piecalendar.com/"


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in {"p", "h1", "h2", "h3", "li", "pre", "br", "tr"}:
            self.parts.append("\n")
    def handle_data(self, data):
        self.parts.append(data)


def fetch(url):
    import certifi
    context = ssl.create_default_context(cafile=certifi.where())
    cache = ROOT / "vendor/jeffy/cache/docs-html" / (hashlib.sha256(url.encode()).hexdigest() + ".html")
    if cache.exists():
        return cache.read_text()
    for attempt in range(6):
        try:
            with urlopen(Request(url, headers={"User-Agent": "csrouter-docs-preparation/1.0"}),
                         context=context, timeout=40) as response:
                html = response.read().decode("utf-8")
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(html)
            time.sleep(0.5)
            return html
        except HTTPError as error:
            if error.code != 429 or attempt == 5:
                raise
            time.sleep(min(2 ** (attempt + 1), 16))


def links(html, prefix):
    urls = set()
    for link in re.findall(r'href=["\']([^"\']+)', html):
        url = urljoin(BASE, link).split("#")[0]
        parsed = urlparse(url)
        if parsed.netloc == "docs.piecalendar.com" and parsed.path.startswith(prefix):
            urls.add(url)
    return urls


def article(url):
    html = fetch(url)
    match = re.search(r'<article\b[^>]*id="fullArticle"[^>]*>(.*?)</article>', html, re.S)
    if not match:
        raise ValueError(f"No article content in {url}")
    parser = Text()
    parser.feed(match.group(1))
    text = re.sub(r"\n[ \t]*\n+", "\n", "".join(parser.parts)).strip()
    updated = re.search(r'<time[^>]*datetime=["\']?([^ >"\']+)', html)
    return {"url": url, "title": text.splitlines()[0], "text": text,
            "last_updated": updated.group(1) if updated else None,
            "sha256": hashlib.sha256(text.encode()).hexdigest()}


def main():
    home = fetch(BASE)
    categories = links(home, "/category/")
    urls = links(home, "/article/")
    with ThreadPoolExecutor(max_workers=2) as pool:
        pages = list(pool.map(fetch, sorted(categories)))
        pagination = set()
        for page in pages:
            urls.update(links(page, "/article/"))
            pagination.update(links(page, "/category/"))
        for page in pool.map(fetch, sorted(pagination - categories)):
            urls.update(links(page, "/article/"))
        articles = list(pool.map(article, sorted(urls)))
    result = {"fetched_at": datetime.now(timezone.utc).isoformat(), "articles": articles}
    cache = ROOT / "vendor/jeffy/cache/pie-docs.json"
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    target = ROOT / "data/support/sources.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({**result, "articles": [
        {key: value for key, value in a.items() if key != "text"} for a in articles
    ]}, indent=2, ensure_ascii=False) + "\n")
    print(f"Snapshotted {len(articles)} articles to {cache}")


if __name__ == "__main__":
    main()
