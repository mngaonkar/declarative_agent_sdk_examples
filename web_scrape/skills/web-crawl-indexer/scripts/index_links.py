#!/usr/bin/env python3
"""Crawl pages and build an index of matching links.

Uses only the Python standard library. It follows HTML pages up to a requested
depth, extracts candidate URLs, filters them by extension and optional regex,
and writes the resulting link set to a JSON file.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

DEFAULT_UA = "Mozilla/5.0 (compatible; web-crawl-indexer/1.0; +https://example.invalid/bot)"
URL_ATTRS = [
    ("a", "href"),
    ("area", "href"),
    ("iframe", "src"),
    ("embed", "src"),
    ("object", "data"),
    ("link", "href"),
]


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_by_name = dict(attrs)
        for expected_tag, attr_name in URL_ATTRS:
            if tag != expected_tag:
                continue
            value = attrs_by_name.get(attr_name)
            if isinstance(value, str):
                value = value.strip()
                if value:
                    self.urls.append(value)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def normalize(url: str) -> str:
    parts = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parts._replace(fragment=""))


def same_registered_domain(a: str, b: str) -> bool:
    host_a = urllib.parse.urlparse(a).netloc.lower().split(":")[0]
    host_b = urllib.parse.urlparse(b).netloc.lower().split(":")[0]
    return host_a.split(".")[-2:] == host_b.split(".")[-2:]


def looks_like_html(url: str, ctype: str) -> bool:
    if ctype in ("text/html", "application/xhtml+xml", ""):
        return True
    path = urllib.parse.urlparse(url).path.lower()
    return not path or path.endswith("/") or "." not in path.rsplit("/", 1)[-1]


def fetch(url: Any, timeout: float, retries: int) -> tuple[str, str, bytes]:
    last_err: Exception | None = None
    normalized_url: str
    if isinstance(url, bytes):
        normalized_url = url.decode("utf-8", errors="replace")
    elif isinstance(url, str):
        normalized_url = url
    else:
        raise TypeError(f"url must be str or bytes, got {type(url).__name__}")

    parsed = urllib.parse.urlparse(normalized_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported URL scheme: {parsed.scheme or 'empty'}")

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(normalized_url, headers={"User-Agent": DEFAULT_UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                final_url_raw = resp.geturl()
                if isinstance(final_url_raw, bytes):
                    final_url = final_url_raw.decode("utf-8", errors="replace")
                else:
                    final_url = str(final_url_raw)

                ctype_raw = resp.headers.get("Content-Type") or ""
                if isinstance(ctype_raw, bytes):
                    ctype_raw = ctype_raw.decode("utf-8", errors="replace")
                ctype = str(ctype_raw).split(";")[0].strip().lower()

                body = resp.read()
                if isinstance(body, bytearray):
                    body = bytes(body)
                elif not isinstance(body, bytes):
                    body = bytes(str(body), encoding="utf-8")

                return final_url, ctype, body
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError, TypeError, ValueError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(1.0 + attempt)
    if last_err is not None:
        raise last_err
    raise RuntimeError("fetch failed unexpectedly")


def parse_extensions(value: str) -> list[str]:
    exts = []
    for raw in value.split(","):
        item = raw.strip().lower()
        if not item:
            continue
        if not item.startswith("."):
            item = f".{item}"
        exts.append(item)
    return exts


def matches(url: str, extensions: list[str], pattern: re.Pattern[str] | None) -> bool:
    path = urllib.parse.urlparse(url).path.lower()
    if extensions and not any(path.endswith(ext) for ext in extensions):
        return False
    if pattern and not pattern.search(url):
        return False
    return True


def discover(
    start_urls: list[str],
    extensions: list[str],
    pattern: re.Pattern[str] | None,
    crawl_depth: int,
    same_domain: bool,
    max_pages: int,
    max_links: int,
    timeout: float,
    retries: int,
    delay: float,
) -> list[str]:
    matched: list[str] = []
    seen_links: set[str] = set()
    visited_pages: set[str] = set()
    queue: list[tuple[str, int]] = [(normalize(url), 0) for url in start_urls]

    while queue:
        if max_pages and len(visited_pages) >= max_pages:
            break
        if max_links and len(matched) >= max_links:
            break

        page_url, depth = queue.pop(0)
        if page_url in visited_pages:
            continue
        visited_pages.add(page_url)

        try:
            final_url, ctype, body = fetch(page_url, timeout, retries)
        except Exception as exc:
            log(f"  ! could not fetch {page_url}: {exc}")
            continue

        if matches(final_url, extensions, pattern):
            if final_url not in seen_links:
                seen_links.add(final_url)
                matched.append(final_url)
                if max_links and len(matched) >= max_links:
                    break

        if not looks_like_html(final_url, ctype):
            if delay:
                time.sleep(delay)
            continue

        parser = LinkExtractor()
        try:
            parser.feed(body.decode("utf-8", errors="replace"))
        except Exception as exc:
            log(f"  ! could not parse {page_url}: {exc}")
            continue

        for raw in parser.urls:
            if raw.lower().startswith(("mailto:", "javascript:", "tel:", "data:")):
                continue
            joined: Any = urllib.parse.urljoin(final_url, raw)
            if isinstance(joined, bytes):
                joined = joined.decode("utf-8", errors="replace")
            candidate = normalize(str(joined))
            if matches(candidate, extensions, pattern) and candidate not in seen_links:
                seen_links.add(candidate)
                matched.append(candidate)
                if max_links and len(matched) >= max_links:
                    break

            if depth >= crawl_depth:
                continue
            if not candidate.startswith(("http://", "https://")):
                continue
            if same_domain and not same_registered_domain(candidate, final_url):
                continue
            if candidate not in visited_pages:
                queue.append((candidate, depth + 1))

        if delay:
            time.sleep(delay)

    return matched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Crawl pages and index links matching a specific type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("urls", nargs="+", help="One or more starting page URLs.")
    parser.add_argument(
        "--ext",
        default="",
        help="Comma-separated extensions to match, e.g. .pdf,.csv,.zip",
    )
    parser.add_argument("--match", default="", help="Optional regex to match against full URLs.")
    parser.add_argument("--crawl-depth", type=int, default=0, help="Follow links this many levels deep.")
    parser.add_argument("--follow-external", action="store_true", help="Allow crawling other domains.")
    parser.add_argument("--max-pages", type=int, default=0, help="Maximum number of pages to visit.")
    parser.add_argument("--max-links", type=int, default=0, help="Maximum number of matching links to collect.")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds to wait between requests.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=2, help="Retries per failed request.")
    parser.add_argument(
        "-o",
        "--output",
        default="../../workspace/link_index.json",
        help="Output JSON path.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print matched links instead of writing JSON.")
    args = parser.parse_args(argv)

    extensions = parse_extensions(args.ext)
    pattern = re.compile(args.match) if args.match else None

    if not extensions and pattern is None:
        parser.error("provide at least one of --ext or --match")

    log(f"Indexing links from {len(args.urls)} start page(s)...")
    links = discover(
        start_urls=args.urls,
        extensions=extensions,
        pattern=pattern,
        crawl_depth=args.crawl_depth,
        same_domain=not args.follow_external,
        max_pages=args.max_pages,
        max_links=args.max_links,
        timeout=args.timeout,
        retries=args.retries,
        delay=args.delay,
    )

    log(f"Matched {len(links)} link(s).")
    if args.dry_run:
        for link in links:
            print(link)
        return 0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "start_urls": args.urls,
        "crawl_depth": args.crawl_depth,
        "extensions": extensions,
        "pattern": args.match or None,
        "count": len(links),
        "links": links,
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    log(f"Wrote index to: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())