"""
knowledge_updater.py — Skill 8: website-auditor
Self-improving knowledge pipeline for SECOND-KNOWLEDGE-BRAIN.md.

Crawls authoritative sources for the latest web audit research (UX, SEO, performance,
accessibility, CRO), scores entries by recency and relevance, deduplicates, and appends
new knowledge to SECOND-KNOWLEDGE-BRAIN.md.

Supports two modes:
    1. crawl4ai mode (default) — uses crawl4ai for full page crawling
    2. requests mode (fallback) — uses requests + BeautifulSoup for simpler fetching

Dependencies:
    pip install crawl4ai requests beautifulsoup4 python-dateutil

Schedule: Weekly cron (e.g., every Sunday 02:00)
    cron: 0 2 * * 0 python tools/knowledge_updater.py

Manual run:
    python tools/knowledge_updater.py                  # Full crawl (all sources)
    python tools/knowledge_updater.py --source webdev   # Crawl only web.dev source
    python tools/knowledge_updater.py --dry-run         # Preview what would be added
    python tools/knowledge_updater.py --max-entries 5   # Limit to top 5 entries
"""

import argparse
import json
import hashlib
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
BRAIN_FILE = SKILL_DIR / "SECOND-KNOWLEDGE-BRAIN.md"
CACHE_FILE = SKILL_DIR / "tools" / ".knowledge_cache.json"
LOG_FILE = SKILL_DIR / "tools" / ".knowledge_update_log.txt"

SOURCES = [
    # Performance & Core Web Vitals
    {
        "id": "webdev",
        "url": "https://web.dev/blog/",
        "domain": "Performance",
        "keywords": ["core web vitals", "performance", "LCP", "CLS", "INP", "TTFB", "lighthouse",
                      "page speed", "rendering", "optimization"],
        "evidence_tier": "Authoritative Guide (Google)"
    },
    # UX Research — Nielsen Norman Group
    {
        "id": "nngroup",
        "url": "https://www.nngroup.com/articles/",
        "domain": "UX",
        "keywords": ["usability", "UX research", "heuristics", "user experience", "eye tracking",
                      "mental model", "cognitive load", "information architecture", "navigation"],
        "evidence_tier": "Industry Authority (NNGroup)"
    },
    # Accessibility — W3C WAI
    {
        "id": "w3cwai",
        "url": "https://www.w3.org/WAI/news/",
        "domain": "Accessibility",
        "keywords": ["WCAG", "accessibility", "screen reader", "ARIA", "keyboard navigation",
                      "contrast", "focus", "assistive technology"],
        "evidence_tier": "International Standard (W3C)"
    },
    # SEO & Content — Google Search Central
    {
        "id": "googlesearch",
        "url": "https://developers.google.com/search/blog",
        "domain": "SEO",
        "keywords": ["SEO", "ranking", "E-E-A-T", "structured data", "core updates",
                      "helpful content", "crawling", "indexing", "canonical", "sitemaps"],
        "evidence_tier": "Authoritative Guide (Google)"
    },
    # CRO Research — ConversionXL
    {
        "id": "cxl",
        "url": "https://cxl.com/blog/",
        "domain": "CRO",
        "keywords": ["conversion rate", "CRO", "A/B testing", "landing page", "persuasion",
                      "social proof", "UX research", "experimentation", "funnel optimization"],
        "evidence_tier": "Industry Research (CXL Institute)"
    },
    # Web Performance Data — HTTP Archive
    {
        "id": "httparchive",
        "url": "https://httparchive.org/reports/",
        "domain": "Performance",
        "keywords": ["web performance", "page weight", "JavaScript", "CSS", "images",
                      "loading speed", "resource sizes", "technology trends"],
        "evidence_tier": "Empirical Data (HTTP Archive)"
    },
    # HCI Academic Papers — ArXiv cs.HC
    {
        "id": "arxiv_hc",
        "url": "https://arxiv.org/list/cs.HC/recent",
        "domain": "UX",
        "keywords": ["user interface", "usability", "interaction design", "web accessibility",
                      "visual design", "human-computer interaction", "cognitive load"],
        "evidence_tier": "Academic Preprint (ArXiv cs.HC)"
    },
    # Information Retrieval — ArXiv cs.IR
    {
        "id": "arxiv_ir",
        "url": "https://arxiv.org/list/cs.IR/recent",
        "domain": "SEO",
        "keywords": ["information retrieval", "search engine", "ranking", "relevance",
                      "query understanding", "document retrieval", "web search"],
        "evidence_tier": "Academic Preprint (ArXiv cs.IR)"
    },
    # WebAIM Accessibility Research
    {
        "id": "webaim",
        "url": "https://webaim.org/blog/",
        "domain": "Accessibility",
        "keywords": ["accessibility", "WCAG", "screen reader", "color contrast",
                      "ARIA", "web accessibility survey", "alt text"],
        "evidence_tier": "Industry Authority (WebAIM)"
    },
    # E-commerce UX — Baymard Institute
    {
        "id": "baymard",
        "url": "https://baymard.com/blog/",
        "domain": "UX",
        "keywords": ["e-commerce", "checkout UX", "cart abandonment", "form design",
                      "product page UX", "search UX", "mobile commerce"],
        "evidence_tier": "Industry Research (Baymard Institute)"
    },
]

RELEVANCE_KEYWORDS = {
    "UX": ["usability", "user experience", "UX", "heuristic", "cognitive load", "mental model",
           "information architecture", "navigation", "interaction design", "visual design",
           "eye tracking", "accessibility"],
    "SEO": ["SEO", "search engine", "ranking", "E-E-A-T", "structured data", "crawl", "index",
            "sitemap", "canonical", "meta tags", "information retrieval", "query understanding"],
    "Performance": ["performance", "core web vitals", "LCP", "CLS", "INP", "TTFB", "page speed",
                    "lighthouse", "load time", "rendering", "optimization", "JavaScript", "images"],
    "Accessibility": ["accessibility", "WCAG", "ARIA", "screen reader", "keyboard", "a11y",
                      "contrast", "focus", "assistive technology", "alt text"],
    "Content": ["content quality", "E-E-A-T", "readability", "copywriting", "content strategy",
                "authoritative", "trustworthiness", "expertise"],
    "CRO": ["conversion", "CRO", "A/B test", "landing page", "CTR", "call to action", "funnel",
            "persuasion", "social proof", "checkout", "experimentation"],
}

MAX_AGE_DAYS = 365  # Ignore articles older than 1 year
MAX_NEW_ENTRIES_PER_RUN = 20

# ──────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────

def log(message: str) -> None:
    """Print message and append to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # logging failures should not halt execution


# ──────────────────────────────────────────────────────────────
# Cache management
# ──────────────────────────────────────────────────────────────

def load_cache() -> dict:
    """Load the deduplication cache from disk."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log(f"Warning: Could not load cache file, starting fresh: {e}")
    return {"seen_urls": [], "seen_hashes": [], "seen_dois": [], "last_run": None}


def save_cache(cache: dict) -> None:
    """Save the deduplication cache to disk."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def url_hash(url: str) -> str:
    """Generate a deterministic hash for a URL (dedup key)."""
    normalized = url.strip().lower().rstrip("/")
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def doi_hash(doi: str) -> str:
    """Generate a deterministic hash for a DOI (dedup key for academic papers)."""
    normalized = doi.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def is_duplicate(url: str, doi: str, cache: dict) -> bool:
    """Check if an entry has already been processed (by URL hash or DOI hash)."""
    h = url_hash(url)
    if h in cache.get("seen_hashes", []):
        return True
    if doi:
        dh = doi_hash(doi)
        if dh in cache.get("seen_dois", []):
            return True
    return False


def mark_seen(url: str, doi: str, cache: dict) -> None:
    """Mark a URL and DOI as processed in the cache."""
    h = url_hash(url)
    if h not in cache["seen_hashes"]:
        cache["seen_hashes"].append(h)
    if url not in cache["seen_urls"]:
        cache["seen_urls"].append(url)
    if doi:
        dh = doi_hash(doi)
        if dh not in cache.get("seen_dois", []):
            cache.setdefault("seen_dois", []).append(dh)


# ──────────────────────────────────────────────────────────────
# Relevance scoring
# ──────────────────────────────────────────────────────────────

def score_relevance(title: str, summary: str, domain: str) -> float:
    """Score 0.0–1.0 based on keyword matches in title+summary for the given domain."""
    text = (title + " " + summary).lower()
    keywords = RELEVANCE_KEYWORDS.get(domain, [])
    if not keywords:
        return 0.5
    matched = sum(1 for kw in keywords if kw.lower() in text)
    return round(min(matched / max(len(keywords) // 2, 1), 1.0), 2)


def score_recency(date_str: str) -> float:
    """Score 0.0–1.0 based on how recent the publication date is."""
    if not date_str:
        return 0.5  # unknown date: neutral score
    try:
        from dateutil import parser as date_parser
        pub_date = date_parser.parse(date_str, fuzzy=True)
        age_days = (datetime.now() - pub_date).days
        if age_days < 0:
            return 1.0
        if age_days > MAX_AGE_DAYS:
            return 0.0
        return round(1.0 - (age_days / MAX_AGE_DAYS), 2)
    except Exception:
        return 0.5


def combined_score(relevance: float, recency: float) -> float:
    """Weighted combination: relevance is more important than recency."""
    return round(0.6 * relevance + 0.4 * recency, 2)


# ──────────────────────────────────────────────────────────────
# crawl4ai integration (primary crawler)
# ──────────────────────────────────────────────────────────────

def crawl_with_crawl4ai(source: dict, cache: dict) -> list[dict]:
    """Use crawl4ai to fetch the source URL and extract article entries."""
    entries = []
    try:
        from crawl4ai import WebCrawler

        crawler = WebCrawler()
        crawler.warmup()
        result = crawler.run(url=source["url"])

        if not result.success:
            log(f"crawl4ai failed for {source['url']}: {result.error_message}")
            return entries

        raw_text = result.markdown or ""
        # Heuristic: split on lines starting with ## or ### as article separators
        blocks = re.split(r"\n(?=#{1,3} )", raw_text)

        for block in blocks[:40]:  # process at most 40 blocks per source
            lines = block.strip().splitlines()
            if not lines:
                continue

            title = lines[0].lstrip("#").strip()
            if len(title) < 10 or len(title) > 300:
                continue

            url_match = re.search(r"https?://[^\s\)\]\"]+", block)
            article_url = url_match.group(0).rstrip(".,);:") if url_match else source["url"]

            if is_duplicate(article_url, "", cache):
                continue

            # Try to extract date
            date_match = re.search(
                r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b"
                r"|\b\d{4}-\d{2}-\d{2}\b",
                block
            )
            pub_date = date_match.group(0) if date_match else ""

            # Try to extract DOI for academic sources
            doi_match = re.search(r"\b10\.\d{4,9}/[^\s\)\]\"]+", block)
            doi = doi_match.group(0) if doi_match else ""

            if is_duplicate(article_url, doi, cache):
                continue

            summary_lines = [l for l in lines[1:] if l.strip() and not l.startswith("#")]
            summary = " ".join(summary_lines[:3])[:500]

            relevance = score_relevance(title, summary, source["domain"])
            recency = score_recency(pub_date)
            score = combined_score(relevance, recency)

            if score < 0.25:
                continue

            entries.append({
                "title": title,
                "url": article_url,
                "doi": doi,
                "date": pub_date,
                "summary": summary,
                "domain": source["domain"],
                "source_id": source["id"],
                "evidence_tier": source["evidence_tier"],
                "relevance_score": relevance,
                "recency_score": recency,
                "combined_score": score,
            })

    except ImportError:
        log("crawl4ai not installed. Falling back to requests mode.")
        return []
    except Exception as e:
        log(f"Unexpected error crawling {source['url']} with crawl4ai: {e}")

    entries.sort(key=lambda x: x["combined_score"], reverse=True)
    return entries


# ──────────────────────────────────────────────────────────────
# requests fallback crawler
# ──────────────────────────────────────────────────────────────

def crawl_with_requests(source: dict, cache: dict) -> list[dict]:
    """Fallback: use requests + BeautifulSoup for simpler HTTP fetching."""
    entries = []
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; website-auditor-knowledge-updater/1.0)"
        }

        try:
            resp = requests.get(source["url"], headers=headers, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            log(f"requests failed for {source['url']}: {e}")
            return entries

        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract article links and titles based on common patterns
        article_elements = (
            soup.find_all("article")
            or soup.find_all("div", class_=re.compile(r"post|article|entry|item", re.I))
            or soup.find_all("li", class_=re.compile(r"post|article|item", re.I))
        )

        # If no article containers found, try anchor tags with title-like content
        if not article_elements:
            article_elements = []
            for a in soup.find_all("a", href=True):
                text = a.get_text(strip=True)
                href = a["href"]
                if len(text) > 15 and len(text) < 300 and href.startswith("http"):
                    article_elements.append(a)

        for elem in article_elements[:25]:
            if hasattr(elem, "find"):
                link = elem.find("a", href=True)
                title_tag = elem.find(["h1", "h2", "h3", "h4"])
            else:
                link = elem
                title_tag = None

            if not link:
                link = elem

            href = link.get("href", "") if hasattr(link, "get") else ""
            title = title_tag.get_text(strip=True) if title_tag else ""
            if not title:
                title = link.get_text(strip=True) if hasattr(link, "get_text") else ""

            if not href or not title:
                continue

            # Resolve relative URLs
            if href.startswith("/"):
                from urllib.parse import urljoin
                href = urljoin(source["url"], href)

            if is_duplicate(href, "", cache):
                continue

            # Extract date from time elements or datetime attributes
            date_str = ""
            time_tag = elem.find("time") if hasattr(elem, "find") else None
            if time_tag:
                date_str = time_tag.get("datetime", "") or time_tag.get_text(strip=True)

            # Extract summary
            summary = ""
            p_tags = elem.find_all("p") if hasattr(elem, "find_all") else []
            if p_tags:
                summary = " ".join(p.get_text(strip=True) for p in p_tags[:2])[:500]

            doi = ""
            doi_match = re.search(r"\b10\.\d{4,9}/[^\s\)\]\"]+", summary + title)
            if doi_match:
                doi = doi_match.group(0)

            if is_duplicate(href, doi, cache):
                continue

            relevance = score_relevance(title, summary, source["domain"])
            recency = score_recency(date_str)
            score = combined_score(relevance, recency)

            if score < 0.25:
                continue

            entries.append({
                "title": title,
                "url": href,
                "doi": doi,
                "date": date_str,
                "summary": summary[:300] if summary else f"Article from {source['url']}",
                "domain": source["domain"],
                "source_id": source["id"],
                "evidence_tier": source["evidence_tier"],
                "relevance_score": relevance,
                "recency_score": recency,
                "combined_score": score,
            })

    except ImportError:
        log("requests and/or beautifulsoup4 not installed. Install with: pip install requests beautifulsoup4")
    except Exception as e:
        log(f"Unexpected error crawling {source['url']} with requests: {e}")

    entries.sort(key=lambda x: x["combined_score"], reverse=True)
    return entries


def crawl_source(source: dict, cache: dict, use_crawl4ai: bool = True) -> list[dict]:
    """Crawl a source using crawl4ai (primary) or requests (fallback)."""
    if use_crawl4ai:
        entries = crawl_with_crawl4ai(source, cache)
        if entries:
            return entries
        # Fall through to requests mode if crawl4ai returns nothing
    return crawl_with_requests(source, cache)


# ──────────────────────────────────────────────────────────────
# SECOND-KNOWLEDGE-BRAIN.md append
# ──────────────────────────────────────────────────────────────

APPEND_SECTION_HEADER = "## Knowledge Update Log"

ENTRY_TEMPLATE = """
### [{source_type}] [ADDED: {date_added}]
**Title:** {title}
**Source:** {url}
**Publication Date:** {pub_date}
**Key Finding:** {summary}
**Evidence Tier:** {evidence_tier}
**Relevance:** {domain} — Relevance: {relevance_score}, Recency: {recency_score}, Combined: {combined_score}
"""


def append_entries_to_brain(entries: list[dict]) -> int:
    """Append new entries to the Knowledge Update Log section. Returns count appended."""
    if not entries:
        return 0

    brain_content = BRAIN_FILE.read_text(encoding="utf-8")

    new_entries_text = ""
    for e in entries:
        new_entries_text += ENTRY_TEMPLATE.format(
            source_type=e["domain"].upper(),
            date_added=datetime.now().strftime("%Y-%m-%d"),
            title=e["title"],
            url=e["url"],
            pub_date=e.get("date", "Unknown"),
            summary=e["summary"][:300],
            evidence_tier=e["evidence_tier"],
            domain=e["domain"],
            relevance_score=e["relevance_score"],
            recency_score=e["recency_score"],
            combined_score=e["combined_score"],
        )

    log_section_pos = brain_content.find(APPEND_SECTION_HEADER)
    if log_section_pos == -1:
        brain_content += f"\n\n{APPEND_SECTION_HEADER}\n{new_entries_text}"
    else:
        # Find the table that follows the header, then append after it
        # Look for end of the table (blank line after last table row)
        table_end = brain_content.find("\n\n", log_section_pos + len(APPEND_SECTION_HEADER))
        if table_end == -1:
            table_end = len(brain_content)
        # Find the position right after the table
        insert_pos = table_end + 2  # skip the two newlines
        # Check if there's already content after the table
        remaining = brain_content[insert_pos:].strip()
        if remaining:
            brain_content = brain_content[:insert_pos] + new_entries_text + "\n\n" + remaining
        else:
            brain_content = brain_content[:insert_pos] + new_entries_text

    BRAIN_FILE.write_text(brain_content, encoding="utf-8")
    return len(entries)


# ──────────────────────────────────────────────────────────────
# Main runner
# ──────────────────────────────────────────────────────────────

def run(sources_filter: Optional[list[str]] = None, dry_run: bool = False,
        max_entries: int = MAX_NEW_ENTRIES_PER_RUN) -> dict:
    """
    Main runner for the knowledge updater.

    Args:
        sources_filter: Optional list of source IDs to crawl (e.g., ['webdev', 'nngroup']).
                       If None, all sources are crawled.
        dry_run: If True, preview what would be added without writing to brain file.
        max_entries: Maximum number of entries to add per run.

    Returns:
        Summary dict with counts and status information.
    """
    log(f"Starting knowledge_updater run at {datetime.now().isoformat()}")
    log(f"Brain file: {BRAIN_FILE}")
    log(f"Sources filter: {sources_filter or 'all'}")
    log(f"Dry run: {dry_run}")

    cache = load_cache()
    all_new_entries = []

    active_sources = SOURCES
    if sources_filter:
        active_sources = [s for s in SOURCES if s["id"] in sources_filter]
        if not active_sources:
            log(f"Warning: No sources matched filter {sources_filter}. Using all sources.")
            active_sources = SOURCES

    # Try crawl4ai first, fall back to requests
    use_crawl4ai = True
    try:
        from crawl4ai import WebCrawler  # noqa: F401
        log("crawl4ai available — using crawl4ai mode")
    except ImportError:
        log("crawl4ai not available — using requests fallback mode")
        use_crawl4ai = False

    for source in active_sources:
        log(f"  Crawling: {source['url']} [{source['domain']}]")
        entries = crawl_source(source, cache, use_crawl4ai=use_crawl4ai)
        log(f"    Found {len(entries)} new candidate entries from {source['id']}")

        for e in entries:
            mark_seen(e["url"], e.get("doi", ""), cache)

        all_new_entries.extend(entries)

    # Global dedup by URL hash (in case same article appears in multiple sources)
    seen_in_run = set()
    deduped = []
    for e in all_new_entries:
        h = url_hash(e["url"])
        doi_h = doi_hash(e.get("doi", "")) if e.get("doi") else ""
        dedup_key = h + doi_h
        if dedup_key not in seen_in_run:
            seen_in_run.add(dedup_key)
            deduped.append(e)

    # Sort by combined score and take top N
    deduped.sort(key=lambda x: x["combined_score"], reverse=True)
    top_entries = deduped[:max_entries]

    if dry_run:
        log(f"[DRY RUN] Would append {len(top_entries)} new entries to SECOND-KNOWLEDGE-BRAIN.md")
        for e in top_entries:
            log(f"  - [{e['domain']}] {e['title'][:80]} (score: {e['combined_score']})")
        return {
            "total_candidates": len(all_new_entries),
            "after_dedup": len(deduped),
            "to_append": len(top_entries),
            "dry_run": True,
            "entries": top_entries,
        }

    appended = append_entries_to_brain(top_entries)
    cache["last_run"] = datetime.now().isoformat()
    save_cache(cache)

    # Update the knowledge update log table in SECOND-KNOWLEDGE-BRAIN.md
    update_log_table(appended)

    log(f"Appended {appended} new entries to SECOND-KNOWLEDGE-BRAIN.md")
    log(f"Cache now contains {len(cache['seen_hashes'])} known URL hashes")
    log(f"Run complete at {datetime.now().isoformat()}")

    return {
        "total_candidates": len(all_new_entries),
        "after_dedup": len(deduped),
        "appended": appended,
        "dry_run": False,
    }


def update_log_table(count: int) -> None:
    """Update the Knowledge Update Log table in SECOND-KNOWLEDGE-BRAIN.md."""
    if not BRAIN_FILE.exists():
        return

    brain_content = BRAIN_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    new_row = f"| {today} | knowledge_updater.py | {count} entries added | Automated crawl |\n"

    # Find the log table and add a row
    log_marker = "| Date | Source | Entries Added | Notes |"
    marker_pos = brain_content.find(log_marker)
    if marker_pos == -1:
        return

    # Find the end of the table header row(s)
    header_end = brain_content.find("\n", marker_pos)
    if header_end == -1:
        return

    # Find the separator row
    sep_end = brain_content.find("\n", header_end + 1)
    if sep_end == -1:
        return

    # Insert after separator row
    insert_pos = sep_end + 1
    brain_content = brain_content[:insert_pos] + new_row + brain_content[insert_pos:]

    BRAIN_FILE.write_text(brain_content, encoding="utf-8")


# ──────────────────────────────────────────────────────────────
# CLI interface
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Knowledge updater for SECOND-KNOWLEDGE-BRAIN.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/knowledge_updater.py                          # Full crawl (all sources)
  python tools/knowledge_updater.py --source webdev nngroup  # Crawl only specific sources
  python tools/knowledge_updater.py --dry-run                # Preview without writing
  python tools/knowledge_updater.py --max-entries 5          # Limit to top 5 entries
  python tools/knowledge_updater.py --list-sources            # Show available sources

Available source IDs: webdev, nngroup, w3cwai, googlesearch, cxl, httparchive,
                      arxiv_hc, arxiv_ir, webaim, baymard

Schedule (cron): 0 2 * * 0 python tools/knowledge_updater.py
  (Runs every Sunday at 02:00)
"""
    )
    parser.add_argument(
        "--source",
        nargs="+",
        dest="sources",
        help="Source ID(s) to crawl (e.g., webdev nngroup). Default: all sources.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be added without modifying SECOND-KNOWLEDGE-BRAIN.md.",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=MAX_NEW_ENTRIES_PER_RUN,
        help=f"Maximum number of entries to add per run. Default: {MAX_NEW_ENTRIES_PER_RUN}",
    )
    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List all available source IDs and exit.",
    )

    args = parser.parse_args()

    if args.list_sources:
        print("Available sources:")
        for s in SOURCES:
            print(f"  {s['id']:15s} [{s['domain']:13s}] {s['url']}")
            print(f"                  Tier: {s['evidence_tier']}")
        sys.exit(0)

    result = run(
        sources_filter=args.sources,
        dry_run=args.dry_run,
        max_entries=args.max_entries,
    )

    if args.dry_run:
        print(f"\n[DRY RUN] Would append {result['to_append']} entries (from {result['after_dedup']} candidates)")
    else:
        print(f"\nAppended {result['appended']} entries (from {result['after_dedup']} candidates)")


if __name__ == "__main__":
    main()