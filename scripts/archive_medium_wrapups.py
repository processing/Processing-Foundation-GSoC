#!/usr/bin/env python3
"""
Archive GSoC wrap-up posts from Medium as Markdown files with local images.

Strategy:
1. Try Medium RSS feeds first (returns full HTML content, recent posts only)
2. Fall back to Wayback Machine for older posts not in RSS

Usage: python3 scripts/archive_medium_wrapups.py
"""

import os
import re
import sys
import json
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from datetime import date, datetime
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "wrapups"
IMAGES_DIR = OUTPUT_DIR / "images"

RSS_FEEDS = [
    "https://medium.com/feed/@ProcessingOrg",
    "https://medium.com/feed/processing-foundation",
]

# Target articles: year → (slug, canonical URL)
# For Wayback fallback, some articles live on /processing-foundation/ not @ProcessingOrg
WRAPUPS = {
    2025: (
        "google-summer-of-code-2025-wrap-up-and-mentor-summit-d1e565e9fe1f",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2025-wrap-up-and-mentor-summit-d1e565e9fe1f",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2025-wrap-up-and-mentor-summit-d1e565e9fe1f",
    ),
    2023: (
        "google-summer-of-code-2023-wrap-ups-961f73edcd1b",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2023-wrap-ups-961f73edcd1b",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2023-wrap-ups-961f73edcd1b",
    ),
    2022: (
        "google-summer-of-code-2022-wrap-up-post-cb64caa840f0",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2022-wrap-up-post-cb64caa840f0",
        "https://medium.com/@ProcessingOrg/google-summer-of-code-2022-wrap-up-post-cb64caa840f0",
    ),
    2021: (
        "wrap-up-post-of-all-2021-google-summer-of-code-projects-d3bcb8713ebb",
        "https://medium.com/processing-foundation/wrap-up-post-of-all-2021-google-summer-of-code-projects-d3bcb8713ebb",
        "https://medium.com/processing-foundation/wrap-up-post-of-all-2021-google-summer-of-code-projects-d3bcb8713ebb",
    ),
    2020: (
        "google-summer-of-code-2020-wrap-up-post-14dd16d4e9be",
        "https://medium.com/processing-foundation/google-summer-of-code-2020-wrap-up-post-14dd16d4e9be",
        "https://medium.com/processing-foundation/google-summer-of-code-2020-wrap-up-post-14dd16d4e9be",
    ),
    2019: (
        "google-summer-of-code-2019-wrap-up-post-3478323bb0ea",
        "https://medium.com/processing-foundation/google-summer-of-code-2019-wrap-up-post-3478323bb0ea",
        "https://medium.com/processing-foundation/google-summer-of-code-2019-wrap-up-post-3478323bb0ea",
    ),
    2018: (
        "2018-google-summer-of-code-grand-wrap-up-post-c13a5ea449e8",
        "https://medium.com/processing-foundation/2018-google-summer-of-code-grand-wrap-up-post-c13a5ea449e8",
        "https://medium.com/processing-foundation/2018-google-summer-of-code-grand-wrap-up-post-c13a5ea449e8",
    ),
    2017: (
        "2017-google-summer-of-code-grand-wrap-up-post-16680b1438db",
        "https://medium.com/@ProcessingOrg/2017-google-summer-of-code-grand-wrap-up-post-16680b1438db",
        # 2017 redirects to processing-foundation channel in Wayback
        "https://medium.com/processing-foundation/2017-google-summer-of-code-grand-wrap-up-post-16680b1438db",
    ),
}

USER_AGENT = "Mozilla/5.0 (compatible; GSoC-Archiver/1.0)"

# ── Network helpers ────────────────────────────────────────────────────────────

def fetch_url(url, binary=False):
    """Fetch URL using curl subprocess (handles HTTPS reliably)."""
    cmd = [
        "curl", "-sL", "--max-time", "45",
        "-H", f"User-Agent: {USER_AGENT}",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=50)
        if result.returncode != 0:
            print(f"  [WARN] curl failed for {url}: exit {result.returncode}", file=sys.stderr)
            return None
        return result.stdout if binary else result.stdout.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return None


# ── RSS fetcher ────────────────────────────────────────────────────────────────

def fetch_rss(feed_url):
    """Return list of (title, link, content_html, pub_date) from a Medium RSS feed."""
    raw = fetch_url(feed_url)
    if not raw:
        return []

    # Strip XML namespace declarations so ElementTree can parse without them
    raw = re.sub(r'\s+xmlns(?::\w+)?="[^"]*"', "", raw)
    # Replace prefixed tags with flat names
    raw = re.sub(r'<content:encoded>', '<contentEncoded>', raw)
    raw = re.sub(r'</content:encoded>', '</contentEncoded>', raw)
    raw = re.sub(r'<dc:creator>', '<dcCreator>', raw)
    raw = re.sub(r'</dc:creator>', '</dcCreator>', raw)
    # Drop other prefixed tags that ET would choke on
    for prefix in ("atom", "cc", "dc"):
        raw = re.sub(rf'<{prefix}:[^>]+/>', '', raw)
        raw = re.sub(rf'<{prefix}:[^>]+>', '', raw)
        raw = re.sub(rf'</{prefix}:[^>]+>', '', raw)

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"  [WARN] XML parse error for {feed_url}: {e}", file=sys.stderr)
        return []

    items = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        content_el = item.find("contentEncoded")
        pub_el = item.find("pubDate")

        title = (title_el.text or "").strip()
        link = (link_el.text or "").strip()
        content = content_el.text or ""
        pub_date = (pub_el.text or "").strip()

        items.append((title, link, content, pub_date))

    return items


# ── Wayback Machine fetcher ────────────────────────────────────────────────────

def get_wayback_url(canonical_url):
    """Find the best Wayback Machine snapshot URL for a given article URL."""
    # Use CDX API to find most recent 200 snapshot
    path = canonical_url.replace("https://", "").replace("http://", "")
    cdx_url = (
        f"https://web.archive.org/cdx/search/cdx"
        f"?url={urllib.parse.quote(path)}"
        f"&output=json&limit=5&fl=timestamp,statuscode&filter=statuscode:200"
    )
    raw = fetch_url(cdx_url)
    if not raw:
        return None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None

    # data[0] is header row, rest are results
    if len(data) < 2:
        return None

    # Pick most recent
    rows = data[1:]
    rows.sort(key=lambda r: r[0], reverse=True)
    timestamp = rows[0][0]
    return f"https://web.archive.org/web/{timestamp}/{canonical_url}"


def extract_from_wayback(wayback_url, year):
    """
    Fetch a Wayback Machine snapshot of a Medium article and extract
    title, pub_date, and article HTML content.
    Returns (title, content_html, pub_date) or None.
    """
    print(f"  Fetching Wayback snapshot: {wayback_url[:80]}...")
    raw = fetch_url(wayback_url)
    if not raw:
        return None

    # Extract title
    title_m = re.search(r'<h1[^>]*class="[^"]*pw-post-title[^"]*"[^>]*>(.*?)</h1>', raw, re.DOTALL)
    if not title_m:
        # Fallback: og:title
        og_m = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
        title = og_m.group(1) if og_m else f"GSoC {year} Wrap-Up"
    else:
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()

    # Extract pub_date from meta
    date_m = re.search(r'<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"', raw)
    pub_date = date_m.group(1)[:10] if date_m else str(year)

    # Extract article body paragraphs using pw-post-body-paragraph class
    # and other structural elements from the article tag
    article_m = re.search(r'<article[^>]*>(.*?)</article>', raw, re.DOTALL)
    if not article_m:
        print(f"  [WARN] No <article> tag found in Wayback snapshot", file=sys.stderr)
        return None

    art_html = article_m.group(1)

    # Build clean HTML from recognized Medium content elements:
    # - pw-post-title (h1)
    # - pw-post-body-paragraph (p)
    # - pw-post-subtitle (h4)
    # - pw-post-image-caption (figcaption)
    # - img tags (figures)
    # - h1/h2/h3/h4 headings

    chunks = []

    # Extract structured content: build a simplified HTML representation
    # that our HtmlToMarkdown parser can handle

    # 1. Title
    if title:
        chunks.append(f"<h1>{title}</h1>")

    # 2. Walk the article content in order
    # Find all elements we care about, in document order
    content_elements = []

    # Paragraphs with class pw-post-body-paragraph
    for m in re.finditer(r'<p[^>]*class="[^"]*pw-post-body-paragraph[^"]*"[^>]*>(.*?)</p>', art_html, re.DOTALL):
        content_elements.append((m.start(), 'p', m.group(1)))

    # Headings h2/h3/h4 inside article body
    for m in re.finditer(r'<(h[2-4])[^>]*class="[^"]*pw-post-body[^"]*"[^>]*>(.*?)</\1>', art_html, re.DOTALL):
        content_elements.append((m.start(), m.group(1), m.group(2)))

    # Any h2/h3 in article (broader catch)
    for m in re.finditer(r'<(h[2-3])[^>]*>(.*?)</\1>', art_html, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if len(text) > 3:
            content_elements.append((m.start(), m.group(1), m.group(2)))

    # Strong headings used as section titles (bold paragraphs at start)
    # not needed - handled by inline <strong>

    # Figures with images — handle both direct miro.medium.com URLs and
    # Wayback-wrapped versions (web.archive.org/web/TIMESTAMPim_/https://miro...)
    img_src_pattern = re.compile(
        r'src="((?:https://web\.archive\.org/web/\d+im_/)?https://(?:miro\.medium\.com|cdn-images[^"]+))"'
        r'(?:[^>]*?alt="([^"]*)")?'
    )
    for m in re.finditer(r'<figure[^>]*>(.*?)</figure>', art_html, re.DOTALL):
        fig_content = m.group(1)
        # Look for img inside figure or picture inside figure
        img_m = img_src_pattern.search(fig_content)
        if not img_m:
            # Also try <source srcset> from <picture> — take first URL
            srcset_m = re.search(r'srcset="([^"]+)"', fig_content)
            if srcset_m:
                first_src = srcset_m.group(1).split()[0]
                img_m_alt = re.search(r'alt="([^"]*)"', fig_content)
                alt = img_m_alt.group(1) if img_m_alt else ""
                src = first_src
            else:
                continue
        else:
            src = img_m.group(1)
            alt = img_m.group(2) or ""
        # Skip small avatar/profile images
        if any(x in src for x in ("/fill:64:64/", "/fill:88:88/", "/fit/c/150/", "/fit/c/48/")):
            continue
        cap_m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', fig_content, re.DOTALL)
        cap = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip() if cap_m else ""
        fig_html = f'<figure><img src="{src}" alt="{alt}"/>'
        if cap:
            fig_html += f'<figcaption>{cap}</figcaption>'
        fig_html += '</figure>'
        content_elements.append((m.start(), 'figure', fig_html))

    # Lists
    for m in re.finditer(r'<(ul|ol)[^>]*>(.*?)</\1>', art_html, re.DOTALL):
        list_content = m.group(2)
        if 'pw-' in art_html[max(0, m.start()-200):m.start()+200]:
            content_elements.append((m.start(), m.group(1), list_content))

    # Blockquotes
    for m in re.finditer(r'<blockquote[^>]*>(.*?)</blockquote>', art_html, re.DOTALL):
        content_elements.append((m.start(), 'blockquote', m.group(1)))

    # Sort all elements by document order
    content_elements.sort(key=lambda x: x[0])

    # Deduplicate by position (keep earliest occurrence of each start pos)
    seen_pos = set()
    deduped = []
    for pos, tag, content in content_elements:
        if pos not in seen_pos:
            seen_pos.add(pos)
            deduped.append((pos, tag, content))

    # Remove duplicate text content (headings may appear multiple times)
    seen_text = set()
    final_elements = []
    for pos, tag, content in deduped:
        text_key = re.sub(r'<[^>]+>', '', content).strip()[:100]
        if text_key and text_key not in seen_text:
            seen_text.add(text_key)
            final_elements.append((pos, tag, content))

    for pos, tag, content in final_elements:
        if tag == 'figure':
            chunks.append(content)
        elif tag in ('ul', 'ol'):
            # Reconstruct list with li items
            items = re.findall(r'<li[^>]*>(.*?)</li>', content, re.DOTALL)
            if items:
                list_html = f'<{tag}>' + ''.join(f'<li>{item}</li>' for item in items) + f'</{tag}>'
                chunks.append(list_html)
        else:
            chunks.append(f'<{tag}>{content}</{tag}>')

    assembled_html = "\n".join(chunks)
    return title, assembled_html, pub_date


# ── HTML → Markdown converter ──────────────────────────────────────────────────

class HtmlToMarkdown(HTMLParser):
    """Pure-stdlib HTML to Markdown converter."""

    def __init__(self):
        super().__init__()
        self.output = []
        self._stack = []
        self._list_stack = []
        self._skip = False
        self._link_href = None
        self._link_text = []
        self._in_pre = False
        self._in_code = False
        self._pending_newlines = 0
        self._img_callback = None

    def _emit(self, text):
        if self._skip:
            return
        self.output.append(text)

    def _newline(self, n=1):
        self._pending_newlines = max(self._pending_newlines, n)

    def _flush_newlines(self):
        if self._pending_newlines:
            self.output.append("\n" * self._pending_newlines)
            self._pending_newlines = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self._stack.append(tag)

        if tag in ("script", "style", "noscript"):
            self._skip = True
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush_newlines()
            level = int(tag[1])
            self._emit("\n" + "#" * level + " ")

        elif tag == "p":
            self._flush_newlines()
            self._newline(2)

        elif tag == "br":
            self._emit("  \n")

        elif tag in ("strong", "b"):
            self._emit("**")

        elif tag in ("em", "i"):
            self._emit("*")

        elif tag == "a":
            self._link_href = attrs.get("href", "")
            self._link_text = []

        elif tag == "ul":
            self._list_stack.append(("ul", 0))
            self._newline(1)

        elif tag == "ol":
            self._list_stack.append(("ol", 0))
            self._newline(1)

        elif tag == "li":
            self._flush_newlines()
            if self._list_stack:
                kind, counter = self._list_stack[-1]
                indent = "  " * (len(self._list_stack) - 1)
                if kind == "ul":
                    self._emit(f"\n{indent}- ")
                else:
                    counter += 1
                    self._list_stack[-1] = (kind, counter)
                    self._emit(f"\n{indent}{counter}. ")

        elif tag == "blockquote":
            self._newline(2)
            self._emit("> ")

        elif tag == "pre":
            self._newline(2)
            self._emit("```\n")
            self._in_pre = True

        elif tag == "code":
            if not self._in_pre:
                self._emit("`")
            self._in_code = True

        elif tag == "figure":
            self._newline(2)

        elif tag == "img":
            src = attrs.get("src", "")
            alt = attrs.get("alt", "")
            # Skip tracking pixels and tiny avatars
            if "_/stat?event=" in src:
                return
            w = attrs.get("width", "")
            h = attrs.get("height", "")
            if w == "1" and h == "1":
                return
            # Skip small avatar/profile images
            _avatar_markers = ("/fill:64:64/", "/fill:88:88/", "/fill:48:48/",
                                "/fit/c/150/", "/fit/c/48/", "/fit/c/96/",
                                "resize:fill:64:", "resize:fill:88:", "resize:fill:48:")
            if any(x in src for x in _avatar_markers):
                return
            if self._img_callback:
                src = self._img_callback(src)
            self._flush_newlines()
            self._emit(f"\n![{alt}]({src})\n")

        elif tag == "figcaption":
            self._emit("\n*")

        elif tag == "hr":
            self._newline(2)
            self._emit("---")
            self._newline(2)

    def handle_endtag(self, tag):
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

        if tag in ("script", "style", "noscript"):
            self._skip = False
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._newline(2)

        elif tag == "p":
            self._newline(2)

        elif tag in ("strong", "b"):
            self._emit("**")

        elif tag in ("em", "i"):
            self._emit("*")

        elif tag == "a":
            if self._link_href is not None:
                text = "".join(self._link_text).strip()
                href = self._link_href
                if text:
                    self._emit(f"[{text}]({href})")
                else:
                    self._emit(href)
                self._link_href = None
                self._link_text = []

        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
            self._newline(2)

        elif tag == "blockquote":
            self._newline(2)

        elif tag == "pre":
            self._emit("\n```")
            self._newline(2)
            self._in_pre = False

        elif tag == "code":
            if not self._in_pre:
                self._emit("`")
            self._in_code = False

        elif tag == "figure":
            self._newline(2)

        elif tag == "figcaption":
            self._emit("*\n")

    def handle_data(self, data):
        if self._skip:
            return
        if self._link_href is not None:
            self._link_text.append(data)
            return
        self._flush_newlines()
        self._emit(data)

    def handle_entityref(self, name):
        entities = {
            "amp": "&", "lt": "<", "gt": ">", "quot": '"',
            "apos": "'", "nbsp": " ", "mdash": "—", "ndash": "–",
            "ldquo": "\u201c", "rdquo": "\u201d", "lsquo": "\u2018",
            "rsquo": "\u2019", "hellip": "…", "copy": "©",
        }
        self.handle_data(entities.get(name, f"&{name};"))

    def handle_charref(self, name):
        try:
            char = chr(int(name[1:], 16) if name.startswith("x") else int(name))
            self.handle_data(char)
        except (ValueError, OverflowError):
            pass

    def get_markdown(self):
        self._flush_newlines()
        text = "".join(self.output)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_markdown(html, img_callback=None):
    parser = HtmlToMarkdown()
    parser._img_callback = img_callback
    parser.feed(html)
    return parser.get_markdown()


# ── Image downloader ───────────────────────────────────────────────────────────

def download_images(html, year):
    """
    Find all CDN image URLs in html, download them, return image_map.
    image_map: {original_src: local_relative_path}
    """
    img_dir = IMAGES_DIR / str(year)
    img_dir.mkdir(parents=True, exist_ok=True)

    # Find all img src URLs
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)

    def unwrap(src):
        """Strip Wayback Machine wrapper from image URL."""
        m = re.match(r'https?://web\.archive\.org/web/\d+im_/(https?://.*)', src)
        return m.group(1) if m else src

    def is_avatar(src):
        """True if URL looks like a small profile/avatar image to skip."""
        return any(x in src for x in (
            "/fill:64:64/", "/fill:88:88/", "/fill:48:48/",
            "/fit/c/150/", "/fit/c/48/", "/fit/c/96/",
            "resize:fill:64:", "resize:fill:88:", "resize:fill:48:",
        ))

    image_map = {}  # original_src → local_relative_path
    counter = 0

    for orig_src in srcs:
        real_src = unwrap(orig_src)
        if "_/stat?event=" in real_src:
            continue
        if is_avatar(real_src):
            continue
        if orig_src in image_map:
            continue

        counter += 1
        parsed = urllib.parse.urlparse(real_src)
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
            ext = ".jpg"

        filename = f"img-{counter:03d}{ext}"
        local_path = img_dir / filename
        rel_path = f"images/{year}/{filename}"

        print(f"    Downloading image {counter}: {real_src[:70]}...")
        data = fetch_url(real_src, binary=True)
        if data and len(data) > 100:
            local_path.write_bytes(data)
            image_map[orig_src] = rel_path
        else:
            print(f"    [WARN] Could not download, keeping original URL")
            image_map[orig_src] = real_src

    return image_map


# ── Article archiver ───────────────────────────────────────────────────────────

def archive_article(year, title, content_html, pub_date):
    slug, canonical_url, _ = WRAPUPS[year]
    out_file = OUTPUT_DIR / f"{year}-gsoc-wrapup.md"

    print(f"  Downloading images for {year}...")
    image_map = download_images(content_html, year)

    def img_callback(src):
        return image_map.get(src, src)

    print(f"  Converting HTML to Markdown...")
    body_md = html_to_markdown(content_html, img_callback=img_callback)

    archived_today = date.today().isoformat()
    if len(pub_date) == 10:
        published = pub_date
    else:
        try:
            dt = datetime.strptime(pub_date[:25], "%a, %d %b %Y %H:%M:%S")
            published = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            published = str(year)

    frontmatter = f"""---
title: "{title.replace('"', "'")}"
year: {year}
source_url: "{canonical_url}"
published: "{published}"
archived: "{archived_today}"
---

"""

    footer = f"""

---

*Originally published on [Medium]({canonical_url}). Archived {archived_today}.*
"""

    out_file.write_text(frontmatter + body_md + footer, encoding="utf-8")
    print(f"  Saved: {out_file.relative_to(REPO_ROOT)}")
    return title


def create_stub(year):
    slug, canonical_url, _ = WRAPUPS[year]
    out_file = OUTPUT_DIR / f"{year}-gsoc-wrapup.md"
    archived_today = date.today().isoformat()

    stub = f"""---
title: "GSoC {year} Wrap-Up"
year: {year}
source_url: "{canonical_url}"
archived: null
status: "not-archived"
---

# GSoC {year} Wrap-Up

> **Note:** This article could not be automatically archived ({archived_today}).
> The original article is at: [{canonical_url}]({canonical_url})
>
> To archive manually: visit the URL above and copy the content here.
"""
    out_file.write_text(stub, encoding="utf-8")
    print(f"  Created stub: {out_file.relative_to(REPO_ROOT)}")


# ── Index generator ────────────────────────────────────────────────────────────

def generate_index(archived, missing):
    index_file = OUTPUT_DIR / "index.md"
    archived_today = date.today().isoformat()

    lines = [
        "# GSoC Wrap-Up Posts Archive",
        "",
        f"Archived from Medium on {archived_today}. "
        "Each file includes the full article text and locally-stored images.",
        "",
        "## Available Archives",
        "",
        "| Year | Title | Status |",
        "|------|-------|--------|",
    ]

    for year in sorted(WRAPUPS.keys(), reverse=True):
        _, canonical_url, _ = WRAPUPS[year]
        md_file = f"{year}-gsoc-wrapup.md"
        if year in archived:
            title = archived[year]
            lines.append(f"| {year} | [{title}]({md_file}) | ✅ Archived |")
        else:
            lines.append(f"| {year} | [GSoC {year} Wrap-Up]({md_file}) | ⚠️ Stub only — [original]({canonical_url}) |")

    lines += [
        "",
        "## Notes",
        "",
        "- Articles marked ✅ are fully archived with local images.",
        "- Articles marked ⚠️ were not available and only have stubs.",
        "  Visit the original URL to read the article.",
        "",
        "## Source URLs",
        "",
    ]

    for year in sorted(WRAPUPS.keys(), reverse=True):
        _, canonical_url, _ = WRAPUPS[year]
        lines.append(f"- **{year}**: {canonical_url}")

    index_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nIndex written: {index_file.relative_to(REPO_ROOT)}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Phase 1: Try Medium RSS feeds (fast, full HTML content)
    print("Phase 1: Fetching Medium RSS feeds...")
    all_items = []
    for feed_url in RSS_FEEDS:
        print(f"  {feed_url}")
        items = fetch_rss(feed_url)
        print(f"  → {len(items)} items")
        all_items.extend(items)

    # Match RSS items to target articles
    rss_by_year = {}
    for title, link, content, pub_date in all_items:
        for year, (slug, _canonical_url, _wayback_url) in WRAPUPS.items():
            if slug in link:
                rss_by_year[year] = (title, content, pub_date)
                break

    print(f"\nFound {len(rss_by_year)}/{len(WRAPUPS)} articles in RSS\n")

    # Phase 2: Wayback Machine for articles not in RSS
    wayback_by_year = {}
    missing_years = [y for y in WRAPUPS if y not in rss_by_year]
    if missing_years:
        print(f"Phase 2: Fetching {len(missing_years)} articles from Wayback Machine...")
        for year in sorted(missing_years, reverse=True):
            slug, canonical_url, wayback_canonical = WRAPUPS[year]
            print(f"\n  [{year}] Looking up Wayback snapshot for: {wayback_canonical[:60]}...")
            wb_url = get_wayback_url(wayback_canonical)
            if not wb_url:
                print(f"  [{year}] No Wayback snapshot found")
                continue
            result = extract_from_wayback(wb_url, year)
            if result:
                title, content_html, pub_date = result
                wayback_by_year[year] = (title, content_html, pub_date)
                print(f"  [{year}] OK: {title[:60]}")
            else:
                print(f"  [{year}] Failed to extract content")

    # Phase 3: Archive all found articles
    print(f"\nPhase 3: Archiving articles...")
    archived = {}
    stubbed = []

    for year in sorted(WRAPUPS.keys(), reverse=True):
        if year in rss_by_year:
            title, content, pub_date = rss_by_year[year]
            print(f"\n[{year}] (RSS) {title[:60]}")
            archived_title = archive_article(year, title, content, pub_date)
            archived[year] = archived_title
        elif year in wayback_by_year:
            title, content, pub_date = wayback_by_year[year]
            print(f"\n[{year}] (Wayback) {title[:60]}")
            archived_title = archive_article(year, title, content, pub_date)
            archived[year] = archived_title
        else:
            print(f"\n[{year}] Creating stub (no source available)")
            create_stub(year)
            stubbed.append(year)

    generate_index(archived, stubbed)

    print("\n" + "=" * 60)
    print(f"Archived:      {len(archived)} articles")
    if stubbed:
        print(f"Stubs created: {stubbed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
