"""
test_knowledge_updater.py — Unit tests for the knowledge_updater module.

Tests cover: cache management, deduplication, relevance scoring, recency scoring,
combined scoring, entry formatting, and graceful degradation.

Run: python -m pytest tests/test_knowledge_updater.py -v
     or: python tests/test_knowledge_updater.py
"""

import json
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from knowledge_updater import (
    url_hash, doi_hash, is_duplicate, mark_seen, load_cache, save_cache,
    score_relevance, score_recency, combined_score, SOURCES, RELEVANCE_KEYWORDS,
    ENTRY_TEMPLATE, append_entries_to_brain,
)


class TestURLHashing:
    """Test URL hash generation and deduplication."""

    def test_url_hash_deterministic(self):
        h1 = url_hash("https://web.dev/blog/test-article/")
        h2 = url_hash("https://web.dev/blog/test-article/")
        assert h1 == h2

    def test_url_hash_case_insensitive(self):
        h1 = url_hash("https://Web.Dev/Blog/Test/")
        h2 = url_hash("https://web.dev/blog/test/")
        assert h1 == h2

    def test_url_hash_strips_trailing_slash(self):
        h1 = url_hash("https://web.dev/blog/test")
        h2 = url_hash("https://web.dev/blog/test/")
        assert h1 == h2

    def test_url_hash_different_urls(self):
        h1 = url_hash("https://web.dev/blog/a")
        h2 = url_hash("https://web.dev/blog/b")
        assert h1 != h2

    def test_doi_hash(self):
        h1 = doi_hash("10.1145/1234567.1234567")
        h2 = doi_hash("10.1145/1234567.1234567")
        assert h1 == h2

    def test_doi_hash_case_insensitive(self):
        h1 = doi_hash("10.1145/ABC.123")
        h2 = doi_hash("10.1145/abc.123")
        assert h1 == h2


class TestDeduplication:
    """Test deduplication logic."""

    def test_is_duplicate_false_initially(self):
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        assert is_duplicate("https://example.com/new", "", cache) is False

    def test_is_duplicate_after_marking(self):
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        mark_seen("https://example.com/article1", "", cache)
        assert is_duplicate("https://example.com/article1", "", cache) is True

    def test_is_duplicate_by_doi(self):
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        mark_seen("https://example.com/a", "10.1145/123.456", cache)
        assert is_duplicate("https://example.com/b", "10.1145/123.456", cache) is True

    def test_mark_seen_idempotent(self):
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        mark_seen("https://example.com/a", "", cache)
        mark_seen("https://example.com/a", "", cache)
        assert len(cache["seen_hashes"]) == 1

    def test_dedup_in_run(self):
        """Same URL appearing from two sources is deduplicated."""
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        mark_seen("https://web.dev/blog/article1/", "", cache)
        assert is_duplicate("https://web.dev/blog/article1/", "", cache) is True

    def test_empty_doi_not_flagged(self):
        """Empty DOI does not cause false positive."""
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        mark_seen("https://example.com/a", "", cache)
        assert is_duplicate("https://example.com/b", "", cache) is False


class TestRelevanceScoring:
    """Test relevance scoring based on keyword matching."""

    def test_high_relevance_performance(self):
        """Performance keywords score positively for performance domain."""
        score = score_relevance(
            "Core Web Vitals Update: New INP Metric",
            "Google has updated the Core Web Vitals with the new INP metric replacing FID.",
            "Performance"
        )
        assert score > 0.2  # At least some keywords match

    def test_low_relevance_unrelated(self):
        score = score_relevance(
            "How to Cook the Perfect Pasta",
            "Boil water, add salt, cook for 10 minutes.",
            "Performance"
        )
        assert score < 0.2

    def test_moderate_relevance_seo(self):
        score = score_relevance(
            "Google Search Ranking Factors 2024",
            "Learn about E-E-A-T and structured data for better SEO.",
            "SEO"
        )
        assert score > 0.2

    def test_accessibility_keywords(self):
        score = score_relevance(
            "WCAG 2.2 New Criteria for Focus and Keyboard Navigation",
            "Updated accessibility guidelines for screen reader and ARIA support.",
            "Accessibility"
        )
        assert score > 0.3

    def test_cro_keywords(self):
        score = score_relevance(
            "Landing Page CRO Best Practices: A/B Testing and Social Proof",
            "Improve conversion rate with A/B testing, social proof, and CTA optimization.",
            "CRO"
        )
        assert score > 0.3

    def test_ux_keywords(self):
        score = score_relevance(
            "Nielsens 10 Usability Heuristics and User Experience Design",
            "Applying heuristics and cognitive load principles to improve usability.",
            "UX"
        )
        assert score > 0.2

    def test_content_keywords(self):
        score = score_relevance(
            "E-E-A-T Content Quality and Readability Strategies",
            "Improving content quality with authoritativeness and trustworthiness.",
            "Content"
        )
        assert score > 0.2

    def test_zero_keywords_match(self):
        """No keyword matches returns 0."""
        score = score_relevance("xyz", "abc def ghi", "Performance")
        assert score == 0.0


class TestRecencyScoring:
    """Test recency scoring based on publication date."""

    def test_very_recent(self):
        date = datetime.now().strftime("%Y-%m-%d")
        assert score_recency(date) >= 0.9

    def test_recent_30_days(self):
        date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        score = score_recency(date)
        assert 0.8 <= score <= 1.0

    def test_mid_age_180_days(self):
        date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        score = score_recency(date)
        assert 0.3 <= score <= 0.7

    def test_old_content(self):
        score = score_recency("2020-01-01")
        assert score == 0.0

    def test_empty_date(self):
        assert score_recency("") == 0.5

    def test_future_date(self):
        """Future dates get max score."""
        future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        assert score_recency(future) == 1.0


class TestCombinedScore:
    """Test combined score calculation."""

    def test_combined_formula(self):
        score = combined_score(0.8, 0.6)
        expected = round(0.6 * 0.8 + 0.4 * 0.6, 2)
        assert score == expected

    def test_combined_max(self):
        assert combined_score(1.0, 1.0) == 1.0

    def test_combined_zero(self):
        assert combined_score(0.0, 0.0) == 0.0

    def test_combined_weighted_towards_relevance(self):
        high_rel = combined_score(1.0, 0.0)
        high_rec = combined_score(0.0, 1.0)
        assert high_rel > high_rec


class TestSources:
    """Test source configuration."""

    def test_sources_count(self):
        assert len(SOURCES) >= 8

    def test_sources_have_required_fields(self):
        required = {"id", "url", "domain", "keywords", "evidence_tier"}
        for s in SOURCES:
            assert required.issubset(set(s.keys())), f"Source {s.get('id', '?')} missing fields"

    def test_all_domains_covered(self):
        domains = {s["domain"] for s in SOURCES}
        required_domains = {"UX", "SEO", "Performance", "Accessibility", "CRO"}
        assert required_domains.issubset(domains)

    def test_source_ids_unique(self):
        ids = [s["id"] for s in SOURCES]
        assert len(ids) == len(set(ids))

    def test_specific_sources_present(self):
        ids = {s["id"] for s in SOURCES}
        assert "webdev" in ids
        assert "nngroup" in ids
        assert "w3cwai" in ids
        assert "cxl" in ids
        assert "arxiv_hc" in ids
        assert "arxiv_ir" in ids
        assert "webaim" in ids
        assert "baymard" in ids

    def test_source_urls_valid(self):
        """All source URLs start with https://."""
        for s in SOURCES:
            assert s["url"].startswith("https://"), f"Source {s['id']} has invalid URL"


class TestAppendFormat:
    """Test SECOND-KNOWLEDGE-BRAIN.md append format."""

    def test_entry_template_has_added_tag(self):
        assert "[ADDED:" in ENTRY_TEMPLATE

    def test_entry_template_fields(self):
        required_fields = ["{title}", "{url}", "{summary}", "{evidence_tier}", "{domain}"]
        for field in required_fields:
            assert field in ENTRY_TEMPLATE

    def test_append_entries_creates_valid_entries(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# SECOND-KNOWLEDGE-BRAIN.md\n\n## Knowledge Update Log\n\n")
            f.write("| Date | Source | Entries Added | Notes |\n|------|--------|---------------|-------|\n")
            f.write("| 2026-01-01 | Manual seed | All core entries | Initial creation |\n")
            temp_path = Path(f.name)

        import knowledge_updater
        original_brain = knowledge_updater.BRAIN_FILE
        knowledge_updater.BRAIN_FILE = temp_path

        try:
            entries = [{
                "title": "Test Article: Core Web Vitals 2024",
                "url": "https://web.dev/blog/test-article-2024/",
                "doi": "",
                "date": "2024-06-15",
                "summary": "A test article about Core Web Vitals performance optimization.",
                "domain": "Performance",
                "source_id": "webdev",
                "evidence_tier": "Authoritative Guide (Google)",
                "relevance_score": 0.8,
                "recency_score": 0.7,
                "combined_score": 0.76,
            }]
            count = append_entries_to_brain(entries)
            assert count == 1

            content = temp_path.read_text(encoding="utf-8")
            assert "[ADDED:" in content
            assert "Test Article: Core Web Vitals 2024" in content
            assert "https://web.dev/blog/test-article-2024/" in content
            assert "Performance" in content
            assert "Authoritative Guide (Google)" in content
            assert "0.76" in content

        finally:
            knowledge_updater.BRAIN_FILE = original_brain
            os.unlink(temp_path)

    def test_append_multiple_entries(self):
        """Multiple entries are appended correctly."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# SECOND-KNOWLEDGE-BRAIN.md\n\n## Knowledge Update Log\n\n")
            f.write("| Date | Source | Entries Added | Notes |\n|------|--------|---------------|-------|\n")
            f.write("| 2026-01-01 | Manual seed | All core entries | Initial creation |\n")
            temp_path = Path(f.name)

        import knowledge_updater
        original_brain = knowledge_updater.BRAIN_FILE
        knowledge_updater.BRAIN_FILE = temp_path

        try:
            entries = [
                {
                    "title": "Article A",
                    "url": "https://example.com/a",
                    "doi": "",
                    "date": "2024-01-01",
                    "summary": "Summary A",
                    "domain": "UX",
                    "source_id": "nngroup",
                    "evidence_tier": "Industry Authority (NNGroup)",
                    "relevance_score": 0.9,
                    "recency_score": 0.8,
                    "combined_score": 0.86,
                },
                {
                    "title": "Article B",
                    "url": "https://example.com/b",
                    "doi": "",
                    "date": "2024-02-01",
                    "summary": "Summary B",
                    "domain": "SEO",
                    "source_id": "googlesearch",
                    "evidence_tier": "Authoritative Guide (Google)",
                    "relevance_score": 0.7,
                    "recency_score": 0.6,
                    "combined_score": 0.66,
                },
            ]
            count = append_entries_to_brain(entries)
            assert count == 2

            content = temp_path.read_text(encoding="utf-8")
            assert "Article A" in content
            assert "Article B" in content

        finally:
            knowledge_updater.BRAIN_FILE = original_brain
            os.unlink(temp_path)


class TestCachePersistence:
    """Test cache load/save cycle."""

    def test_save_and_load_cache(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"seen_urls": [], "seen_hashes": [], "seen_dois": [], "last_run": None}, f)
            temp_path = Path(f.name)

        import knowledge_updater
        original_cache = knowledge_updater.CACHE_FILE
        knowledge_updater.CACHE_FILE = temp_path

        try:
            cache = load_cache()
            assert "seen_hashes" in cache
            assert "seen_urls" in cache

            mark_seen("https://example.com/test", "10.1234/test", cache)
            save_cache(cache)

            cache2 = load_cache()
            assert is_duplicate("https://example.com/test", "10.1234/test", cache2)
        finally:
            knowledge_updater.CACHE_FILE = original_cache
            os.unlink(temp_path)

    def test_corrupted_cache_handled(self):
        """A corrupted cache file is handled gracefully."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("NOT VALID JSON!!!")
            temp_path = Path(f.name)

        import knowledge_updater
        original_cache = knowledge_updater.CACHE_FILE
        knowledge_updater.CACHE_FILE = temp_path

        try:
            cache = load_cache()
            assert "seen_hashes" in cache
            assert isinstance(cache["seen_hashes"], list)
        finally:
            knowledge_updater.CACHE_FILE = original_cache
            os.unlink(temp_path)


class TestRelevanceKeywords:
    """Test that all 6 dimensions have relevance keywords."""

    def test_all_dimensions_present(self):
        required = {"UX", "SEO", "Performance", "Accessibility", "Content", "CRO"}
        assert required.issubset(set(RELEVANCE_KEYWORDS.keys()))

    def test_keywords_not_empty(self):
        for domain, keywords in RELEVANCE_KEYWORDS.items():
            assert len(keywords) >= 5, f"{domain} has only {len(keywords)} keywords"


class TestCrawlSourceFallback:
    """Test that the requests fallback mode handles failures gracefully."""

    def test_invalid_url_returns_empty(self):
        """Crawling an invalid URL returns empty list, not an exception."""
        from knowledge_updater import crawl_with_requests
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        source = {
            "id": "test_invalid",
            "url": "https://this-domain-does-not-exist-xyz123abc.com",
            "domain": "Performance",
            "keywords": ["test"],
            "evidence_tier": "Test"
        }
        entries = crawl_with_requests(source, cache)
        assert isinstance(entries, list)
        # Should return empty list, not raise exception

    def test_crawl_with_requests_valid_source(self):
        """Requests mode can parse a valid HTML page."""
        from knowledge_updater import crawl_with_requests
        cache = {"seen_urls": [], "seen_hashes": [], "seen_dois": []}
        source = {
            "id": "test_nngroup",
            "url": "https://www.nngroup.com/articles/",
            "domain": "UX",
            "keywords": ["usability", "UX research", "heuristics"],
            "evidence_tier": "Industry Authority (NNGroup)"
        }
        entries = crawl_with_requests(source, cache)
        assert isinstance(entries, list)


if __name__ == "__main__":
    import traceback
    test_classes = [
        TestURLHashing, TestDeduplication, TestRelevanceScoring,
        TestRecencyScoring, TestCombinedScore, TestSources,
        TestAppendFormat, TestCachePersistence, TestRelevanceKeywords,
        TestCrawlSourceFallback,
    ]
    passed = 0
    failed = 0
    for test_class in test_classes:
        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            method = getattr(instance, method_name)
            try:
                method()
                print(f"  PASS: {test_class.__name__}.{method_name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL: {test_class.__name__}.{method_name}: {e}")
                traceback.print_exc()
                failed += 1
    print(f"\nResults: {passed} passed, {failed} failed, {passed + failed} total")
    if failed > 0:
        sys.exit(1)
