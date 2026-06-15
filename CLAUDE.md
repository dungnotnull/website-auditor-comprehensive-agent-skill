# CLAUDE.md — Skill 8: website-auditor

## Skill Identity
- **Name:** website-auditor
- **Tagline:** Comprehensive multi-dimensional scoring evaluation of any website, grounded in world-renowned frameworks, with self-improving knowledge.
- **Current Phase:** Complete — All phases (0–5) delivered, production-ready
- **Cluster:** B — Technical Evaluation Harnesses (shared with Skills 4 and 6)

---

## Problem This Skill Solves

Businesses, developers, and digital marketers often lack an objective, structured method for evaluating website quality. Ad hoc feedback ("the design looks bad", "the site is slow") misses systemic issues and fails to prioritize fixes by impact. This skill fills that gap: it applies the same rigorous, multi-framework methodology that top digital agencies use — covering UX, SEO, Core Web Vitals performance, WCAG accessibility, content quality, and conversion rate optimization — and delivers a scored, evidence-backed report with a prioritized improvement roadmap. The result is a professional audit artifact, not a chat answer.

---

## Harness Flow Summary

```
/website-auditor [URL]
  │
  ├── Stage 1: URL Intake & Scope Definition
  │     └── Identify website type (landing page / SaaS / e-commerce / blog / portal)
  │         Clarify audit goals and primary user persona
  │
  ├── Stage 2: Technical Reconnaissance
  │     └── [sub-technical-audit] WebFetch live data, headers, sitemap, robots.txt
  │         Collect Core Web Vitals signals, TTFB, page size, resource counts
  │
  ├── Stage 3: Framework Selection
  │     └── [sub-evaluation-framework-selector] Match frameworks to website type
  │         (Nielsen's 10 heuristics, WCAG 2.2, Core Web Vitals, E-E-A-T, CRO frameworks)
  │
  ├── Stage 4: Multi-Dimensional Audit (6 Dimensions)
  │     ├── [sub-ux-accessibility-audit] Dimension 1: UX + Dimension 4: Accessibility
  │     ├── [sub-technical-audit]        Dimension 3: Performance + Dimension 2: SEO
  │     └── Direct harness               Dimension 5: Content Quality + Dimension 6: CRO
  │
  ├── Stage 5: Competitive Benchmarking
  │     └── [sub-competitive-benchmarker] Compare scores vs. industry peers / best-in-class
  │
  ├── Stage 6: Scoring & Synthesis
  │     └── [sub-scoring-engine] Weighted aggregate score per dimension; overall grade
  │
  ├── Stage 7: Improvement Roadmap
  │     └── [sub-improvement-roadmap] Prioritized fix list: effort × impact matrix
  │
  ├── Stage 8: Quality Gate Review + Devil's Advocate Challenge
  │     └── Validate all 6 dimensions covered; all findings traced to evidence
  │         Challenge scores for defensibility; note limitations
  │
  └── Stage 9: Final Report Output
        └── Structured audit report (executive summary → dimension scores → roadmap)
```

---

## Sub-Skills List

| File | Description | Shared Across Cluster B? |
|------|-------------|--------------------------|
| `skills/main.md` | Primary 9-stage harness entry point | No (website-auditor specific) |
| `skills/sub-technical-audit.md` | Deep technical analysis: performance metrics, SEO signals, HTTP headers, crawl data | No (website-auditor specific) |
| `skills/sub-ux-accessibility-audit.md` | UX heuristic evaluation (Nielsen) + WCAG 2.2 accessibility scoring | No (website-auditor specific) |
| `skills/sub-competitive-benchmarker.md` | Industry peer comparison and benchmarking against best-in-class sites | No (website-auditor specific) |
| `skills/sub-evaluation-framework-selector.md` | Selects evaluation frameworks and scoring weights based on target type and audit goals | **Yes** — shared with Skills 4, 6 |
| `skills/sub-scoring-engine.md` | Computes weighted multi-dimensional scores and overall grade | **Yes** — shared with Skills 4, 6 |
| `skills/sub-improvement-roadmap.md` | Generates prioritized improvement roadmap with effort/impact matrix | **Yes** — shared with Skills 4, 6 |

### Cluster B Shared Sub-Skills

Three sub-skills are designed to be reusable across Cluster B (Skills 4, 6, 8):

1. **sub-evaluation-framework-selector** — Framework matching logic is parameterized by target type. For website-auditor: website types (landing page, SaaS, etc.). For code auditors: code types (frontend, backend, etc.).
2. **sub-scoring-engine** — Pure computation step. Takes findings + weights, produces scorecard. Dimension names and severity calibrations are inputs.
3. **sub-improvement-roadmap** — Prioritization logic (Effort × Impact) is universal. Dimension labels and effort scales are inputs.

See `docs/cross-skill-compatibility.md` for detailed adaptation instructions.

### Website-Auditor-Specific Overrides

When using shared sub-skills within the website-auditor context, the following overrides apply:

- **sub-evaluation-framework-selector:** Uses website type weight table (landing page, SaaS, e-commerce, blog, portal, government). Includes CRO and Content Quality dimensions that other skills may not need.
- **sub-scoring-engine:** 6 dimensions (UX, SEO, Performance, Accessibility, Content Quality, CRO). Severity calibration maps WCAG A failures to Critical, Nielsen severity 4 to Critical, etc.
- **sub-improvement-roadmap:** Effort measured in web development hours/days. Impact measured in audit score points + business outcomes (conversion rate, search ranking, etc.).

---

## Tools Required

- **WebFetch** — fetch live website HTML, headers, sitemap.xml, robots.txt, structured data
- **WebSearch** — research industry benchmarks, find competitor URLs, look up framework specs
- **Read / Write** — read SECOND-KNOWLEDGE-BRAIN.md; write final report artifact
- **Bash** — optional: run Lighthouse CLI or PageSpeed Insights API if available
- **Skill (sub-skill invocation)** — invoke sub-skills at each stage

---

## Knowledge Sources

- **Performance:** web.dev/performance, developers.google.com/speed/docs/insights/rules, Core Web Vitals thresholds
- **Accessibility:** w3.org/WAI/WCAG22, deque.com/axe, WebAIM
- **UX:** Nielsen Norman Group (nngroup.com), Baymard Institute (baymard.com)
- **SEO:** developers.google.com/search, moz.com/learn/seo, ahrefs.com/blog
- **CRO:** conversionxl.com, marketingexperiments.com, unbounce.com/blog
- **Research:** ArXiv cs.HC, cs.IR; ACM Digital Library (CHI, CSCW, WWW); IWC journal

---

## Supporting Python Tools

| File | Purpose |
|------|---------|
| `tools/knowledge_updater.py` | crawl4ai pipeline — fetches latest papers and articles from authoritative sources, appends new entries to SECOND-KNOWLEDGE-BRAIN.md, deduplicates by URL/DOI |
| `tools/requirements.txt` | Python dependencies for knowledge_updater (crawl4ai, requests, beautifulsoup4, python-dateutil) |

### Running the Knowledge Updater

```bash
# Install dependencies
pip install -r tools/requirements.txt

# Full crawl (all sources)
python tools/knowledge_updater.py

# Crawl only specific sources
python tools/knowledge_updater.py --source webdev nngroup

# Preview without writing
python tools/knowledge_updater.py --dry-run

# List available sources
python tools/knowledge_updater.py --list-sources

# Weekly cron (every Sunday at 02:00)
0 2 * * 0 python /path/to/tools/knowledge_updater.py
```

---

## Testing

```bash
# Run knowledge_updater unit tests
python tests/test_knowledge_updater.py

# Run skill structure validation tests
python tests/test_skill_validation.py
```

---

## Completed Development Tasks

- [x] Write `skills/main.md` — primary 9-stage harness entry point
- [x] Write `skills/sub-evaluation-framework-selector.md`
- [x] Write `skills/sub-scoring-engine.md`
- [x] Write `skills/sub-improvement-roadmap.md`
- [x] Write `skills/sub-technical-audit.md`
- [x] Write `skills/sub-ux-accessibility-audit.md`
- [x] Write `skills/sub-competitive-benchmarker.md`
- [x] Write `tools/knowledge_updater.py`
- [x] Write `tests/test-scenarios.md`
- [x] Populate initial `SECOND-KNOWLEDGE-BRAIN.md`
- [x] Write `tests/test_knowledge_updater.py` — unit tests
- [x] Write `tests/test_skill_validation.py` — structural validation
- [x] Write `docs/cross-skill-compatibility.md` — Cluster B shared sub-skill docs
- [x] Write `README.md` — project documentation
- [x] Write `tools/requirements.txt` — Python dependencies

---

## Reference Files

- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase-by-phase build roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving domain knowledge base
- `README.md` — project documentation and quick start
- `docs/cross-skill-compatibility.md` — Cluster B shared sub-skill adaptation guide
