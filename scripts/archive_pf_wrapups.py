#!/usr/bin/env python3
"""
Archive GSoC wrap-up pages from processingfoundation.org as Markdown files.

These pages (2011–2015) are simpler than Medium posts: plain HTML with no images.

Usage:
  python3 scripts/archive_pf_wrapups.py
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "wrapups"

WRAPUPS = {
    2015: "https://processingfoundation.org/advocacy/google-summer-of-code/2015",
    2014: "https://processingfoundation.org/advocacy/google-summer-of-code/2014",
    2013: "https://processingfoundation.org/advocacy/google-summer-of-code/2013",
    2012: "https://processingfoundation.org/advocacy/google-summer-of-code/2012",
    2011: "https://processingfoundation.org/advocacy/google-summer-of-code/2011",
}

USER_AGENT = "Mozilla/5.0 (compatible; GSoC-Archiver/1.0)"

# ── Network helper ─────────────────────────────────────────────────────────────

def fetch_url(url):
    cmd = ["curl", "-sL", "--max-time", "30", "-H", f"User-Agent: {USER_AGENT}", url]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=35)
        if result.returncode != 0:
            print(f"  [WARN] curl failed for {url}", file=sys.stderr)
            return None
        return result.stdout.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return None


# ── HTML → Markdown ────────────────────────────────────────────────────────────

def html_to_markdown(html):
    """Convert a small subset of HTML to Markdown."""
    # Normalise line endings
    html = html.replace("\r\n", "\n").replace("\r", "\n")

    # Strip tags we don't want to convert but whose text we keep
    html = re.sub(r'<br\s*/?>', "\n", html, flags=re.IGNORECASE)

    # Block elements → blank lines
    for tag in ("p", "div", "section", "article", "li"):
        html = re.sub(rf'<{tag}[^>]*>', "\n\n", html, flags=re.IGNORECASE)
        html = re.sub(rf'</{tag}>', "\n\n", html, flags=re.IGNORECASE)

    # Headings
    for level in range(1, 7):
        html = re.sub(
            rf'<h{level}[^>]*>(.*?)</h{level}>',
            lambda m, l=level: f"\n\n{'#' * l} {_strip_tags(m.group(1)).strip()}\n\n",
            html, flags=re.IGNORECASE | re.DOTALL,
        )

    # Lists
    html = re.sub(r'<ul[^>]*>', "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r'</ul>', "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r'<ol[^>]*>', "\n\n", html, flags=re.IGNORECASE)
    html = re.sub(r'</ol>', "\n\n", html, flags=re.IGNORECASE)

    # Inline: bold, italic, links
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(
        r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        r'[\2](\1)',
        html, flags=re.IGNORECASE | re.DOTALL,
    )

    # Strip remaining tags
    html = re.sub(r'<[^>]+>', '', html)

    # Decode common HTML entities
    entities = {
        "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
        "&#39;": "'", "&apos;": "'", "&nbsp;": " ",
        "&#8217;": "\u2019", "&#8216;": "\u2018",
        "&#8220;": "\u201c", "&#8221;": "\u201d",
        "&#8212;": "—", "&#8211;": "–", "&#8230;": "…",
    }
    for entity, char in entities.items():
        html = html.replace(entity, char)

    # Collapse excessive blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()


def _strip_tags(html):
    return re.sub(r'<[^>]+>', '', html)


# ── Archiver ───────────────────────────────────────────────────────────────────

def archive_year(year, url):
    print(f"[{year}] Fetching {url} ...")
    raw = fetch_url(url)
    if not raw:
        print(f"  [ERROR] Could not fetch page, skipping.")
        return None

    # Extract <main> content
    m = re.search(r'<main[^>]*>(.*?)</main>', raw, re.DOTALL | re.IGNORECASE)
    if not m:
        print(f"  [WARN] No <main> tag found, using <body>", file=sys.stderr)
        m = re.search(r'<body[^>]*>(.*?)</body>', raw, re.DOTALL | re.IGNORECASE)
    if not m:
        print(f"  [ERROR] Could not find content", file=sys.stderr)
        return None

    main_html = m.group(1)

    # Extract title
    title_m = re.search(r'<h1[^>]*>(.*?)</h1>', main_html, re.DOTALL | re.IGNORECASE)
    if title_m:
        title = _strip_tags(title_m.group(1)).strip()
    else:
        title = f"Google Summer of Code {year}"

    body_md = html_to_markdown(main_html)

    archived_today = date.today().isoformat()

    frontmatter = f"""---
title: "{title.replace('"', "'")}"
year: {year}
source_url: "{url}"
published: "{year}"
archived: "{archived_today}"
---

"""

    footer = f"""

---

*Originally published on [processingfoundation.org]({url}). Archived {archived_today}.*
"""

    out_file = OUTPUT_DIR / f"{year}-gsoc-wrapup.md"
    out_file.write_text(frontmatter + body_md + footer, encoding="utf-8")
    print(f"  Saved: {out_file.relative_to(REPO_ROOT)}")
    return title


# ── README update ──────────────────────────────────────────────────────────────

def update_readme(newly_archived):
    """Append newly archived years to the README tables."""
    readme = OUTPUT_DIR / "README.md"
    text = readme.read_text(encoding="utf-8")

    archived_today = date.today().isoformat()

    # Update the "Available Archives" table — insert rows for new years
    for year, title in sorted(newly_archived.items(), reverse=True):
        md_file = f"{year}-gsoc-wrapup.md"
        row = f"| {year} | [{title}]({md_file}) |"
        if md_file not in text:
            # Insert after the last table row (before empty line after table)
            text = re.sub(
                r'(\| \d{4} \|[^\n]+\n)(\n)',
                lambda m, r=row: m.group(1) + r + "\n" + m.group(2),
                text, count=1,
            )

    # Update the "On processingfoundation.org" section header
    if newly_archived:
        text = text.replace(
            "### On processingfoundation.org (not archived here)",
            "### Archived from processingfoundation.org",
        )
        # Move archived years from "not archived" list into the medium section
        # (they now have their own section header above)

    # Update the archived date in the intro line
    text = re.sub(
        r'Archived from Medium on \d{4}-\d{2}-\d{2}\.',
        f"Archived from Medium and processingfoundation.org on {archived_today}.",
        text,
    )

    readme.write_text(text, encoding="utf-8")
    print(f"\nREADME updated: {readme.relative_to(REPO_ROOT)}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    newly_archived = {}
    for year in sorted(WRAPUPS.keys(), reverse=True):
        url = WRAPUPS[year]
        title = archive_year(year, url)
        if title:
            newly_archived[year] = title

    if newly_archived:
        update_readme(newly_archived)

    print("\n" + "=" * 60)
    print(f"Archived: {list(newly_archived.keys())}")
    print("=" * 60)


if __name__ == "__main__":
    main()
