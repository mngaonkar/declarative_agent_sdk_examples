---
name: web-crawl-indexer
description: Crawl one or more pages, follow links, and build a JSON index of links matching a specific file type or URL pattern. Use this skill when the user wants to discover and catalog links like PDFs, CSVs, ZIPs, docs, images, or other extension-based resources across a site without downloading them.
---

# Web Crawl Indexer

Build a lightweight index of links from a starting page or small site crawl.
This skill uses a single standard-library Python script and does not download
the matched files. It only follows HTML pages, extracts links, and records the
ones matching the requested type.

## When to use this

Use it when the user wants to:

- find all links of a given type on a site
- crawl a page and its sub-pages to collect matching resources
- generate a machine-readable index before deciding what to download

Good examples are requests like "index all CSV links from this portal",
"crawl this docs site and list ZIP files", or "find every PDF and DOCX link up
to one level deep".

## Quick start

Start with a dry run so the user can inspect the matches:

```bash
python scripts/index_links.py https://example.org/resources --ext .pdf --dry-run
```

Then write a JSON index file:

```bash
python scripts/index_links.py https://example.org/resources \
  --ext .pdf,.docx \
  -o ../../workspace/link_index.json
```

## How it works

- fetches each starting page with `urllib`
- parses HTML with `html.parser`
- follows links up to `--crawl-depth`
- stays on the same registered domain unless `--follow-external` is set
- matches discovered URLs by extension and optional regex
- writes a JSON file containing the crawl inputs and matched links

## Options

- `--ext .pdf,.csv,.zip` — comma-separated extensions to match
- `--match REGEX` — optional regex applied to the full normalized URL
- `--crawl-depth N` — how many HTML link levels to follow
- `--follow-external` — allow crawling onto other domains
- `--max-pages N` — stop after visiting N pages
- `--max-links N` — stop after collecting N matching links
- `--delay SECONDS` — wait between requests
- `--timeout SECONDS` — per-request timeout
- `--retries N` — retries per request
- `-o, --output FILE` — JSON output path
- `--dry-run` — print matched links instead of writing JSON

## Output format

The JSON file contains:

```json
{
  "start_urls": ["https://example.org/resources"],
  "crawl_depth": 1,
  "extensions": [".pdf"],
  "pattern": null,
  "count": 2,
  "links": [
    "https://example.org/files/report.pdf",
    "https://example.org/files/spec.pdf"
  ]
}
```

## Example

```bash
python scripts/index_links.py https://example.edu/library \
  --ext .pdf,.csv \
  --crawl-depth 1 \
  --max-pages 50 \
  -o ../../workspace/library_links.json
```

## Limitations

- It does not execute JavaScript, so client-rendered links will be missed.
- It does not log in or handle authenticated sessions.
- It identifies HTML pages through URL/content type heuristics and is meant for
  lightweight crawling, not full site mirroring.

## Dependencies

None beyond Python 3.8+. The script uses only the standard library.