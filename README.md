# website-auditor

## Comprehensive Multi-Dimensional Website Audit Skill

A Claude skill that evaluates any public website across six dimensions — **UX, SEO, Performance, Accessibility, Content Quality, and CRO** — using world-renowned evaluation frameworks. Produces a professional audit report with per-dimension scores, an overall weighted grade, competitive benchmarks, and a prioritized improvement roadmap.

## Quick Start

```
/website-auditor https://example.com
```

The skill will:
1. Confirm the URL is reachable
2. Ask you to confirm the website type and audit scope
3. Execute a 9-stage audit harness
4. Deliver a structured report with scores, benchmarks, and a prioritized roadmap

## Architecture

```
/website-auditor [URL]
    │
    ├── Stage 1: URL Intake & Scope Definition
    ├── Stage 2: Technical Reconnaissance ──── [sub-technical-audit]
    ├── Stage 3: Framework Selection ────────── [sub-evaluation-framework-selector]
    ├── Stage 4: Multi-Dimensional Audit
    │   ├── Track A: UX + Accessibility ────── [sub-ux-accessibility-audit]
    │   ├── Track B: Performance + SEO ──────── [sub-technical-audit]
    │   ├── Track C: Content Quality ─────────── (inline)
    │   └── Track D: CRO ─────────────────────── (inline)
    ├── Stage 5: Competitive Benchmarking ───── [sub-competitive-benchmarker]
    ├── Stage 6: Scoring & Synthesis ────────── [sub-scoring-engine]
    ├── Stage 7: Improvement Roadmap ────────── [sub-improvement-roadmap]
    ├── Stage 8: Quality Gate Review + Devil's Advocate
    └── Stage 9: Final Report Output
```

## File Structure

```
website-auditor/
├── CLAUDE.md                              # Skill manifest and instructions
├── PROJECT-detail.md                      # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md # Phase tracking
├── SECOND-KNOWLEDGE-BRAIN.md             # Self-improving knowledge base
├── README.md                              # This file
├── skills/
│   ├── main.md                            # Primary 9-stage harness entry point
│   ├── sub-technical-audit.md             # SEO + Performance reconnaissance
│   ├── sub-ux-accessibility-audit.md      # Nielsen heuristics + WCAG 2.2
│   ├── sub-evaluation-framework-selector.md # Framework matching + weights
│   ├── sub-scoring-engine.md              # Weighted scoring + grading
│   ├── sub-improvement-roadmap.md          # Effort × Impact prioritization
│   └── sub-competitive-benchmarker.md     # Peer comparison + gap analysis
├── tools/
│   ├── knowledge_updater.py              # Crawl pipeline for SECOND-KNOWLEDGE-BRAIN
│   └── requirements.txt                   # Python dependencies for knowledge_updater
├── tests/
│   ├── test-scenarios.md                 # 7 concrete test scenarios
│   ├── test_knowledge_updater.py         # Unit tests for knowledge_updater
│   └── test_skill_validation.py          # Structural validation tests
└── docs/
    └── cross-skill-compatibility.md      # Cluster B shared sub-skill documentation
```

## Sub-Skills

| Sub-Skill | Purpose | Framework |
|-----------|---------|-----------|
| sub-technical-audit | SEO signals + performance reconnaissance | Google Search Quality Guidelines, Core Web Vitals |
| sub-ux-accessibility-audit | UX heuristic evaluation + WCAG compliance | Nielsen's 10 Heuristics, WCAG 2.2 |
| sub-evaluation-framework-selector | Match frameworks to website type | Dynamic (per website type) |
| sub-scoring-engine | Weighted scoring + grading | Custom 0–100 with A–F grades |
| sub-improvement-roadmap | Prioritized action plan | Effort × Impact matrix |
| sub-competitive-benchmarker | Peer comparison | Surface-level signal comparison |

## Knowledge Updater

Keep SECOND-KNOWLEDGE-BRAIN.md current with the latest research:

```bash
# Install dependencies
pip install -r tools/requirements.txt

# Full crawl (all sources)
python tools/knowledge_updater.py

# Crawl only specific sources
python tools/knowledge_updater.py --source webdev nngroup

# Preview without writing
python tools/knowledge_updater.py --dry-run

# Limit entries
python tools/knowledge_updater.py --max-entries 5

# List available sources
python tools/knowledge_updater.py --list-sources

# Weekly cron (every Sunday at 02:00)
# Add to crontab: 0 2 * * 0 python /path/to/tools/knowledge_updater.py
```

### Sources Configured

| Source ID | Domain | URL |
|-----------|--------|-----|
| webdev | Performance | web.dev/blog |
| nngroup | UX | nngroup.com/articles |
| w3cwai | Accessibility | w3.org/WAI/news |
| googlesearch | SEO | developers.google.com/search/blog |
| cxl | CRO | cxl.com/blog |
| httparchive | Performance | httparchive.org/reports |
| arxiv_hc | UX | arxiv.org/list/cs.HC/recent |
| arxiv_ir | SEO | arxiv.org/list/cs.IR/recent |
| webaim | Accessibility | webaim.org/blog |
| baymard | UX | baymard.com/blog |

## Testing

```bash
# Run all unit tests
python tests/test_knowledge_updater.py

# Run skill structure validation
python tests/test_skill_validation.py

# Both test suites should pass with 0 failures
```

## Evaluation Dimensions

| Dimension | Weight Range | Framework |
|-----------|-------------|-----------|
| UX | 15–25% | Nielsen's 10 Heuristics + Gestalt Principles |
| SEO | 10–25% | Google Search Quality Guidelines |
| Performance | 15–20% | Core Web Vitals (LCP, INP, CLS, TTFB, FCP) |
| Accessibility | 10–30% | WCAG 2.2 Level AA |
| Content Quality | 10–30% | E-E-A-T, Flesch–Kincaid Readability |
| CRO | 5–35% | LIFT Model, Cialdini's Persuasion Principles |

Weights vary by website type (landing page, SaaS, e-commerce, blog, portal, government).

## Quality Gates

The harness enforces quality gates at critical stage transitions:

| Gate | Location | Criteria |
|------|----------|----------|
| Stage 2→3 | After Recon | Page HTML successfully fetched |
| Stage 3→4 | After Framework Selection | All dimensions have framework + weight; weights = 100% |
| Stage 4→5 | After Audit | All tracks completed; ≥3 findings per dimension; evidence cited |
| Stage 5→6 | After Benchmark | ≥2 comparison sites (or fallback documented); gap analysis present |
| Stage 6→7 | After Scoring | All dimensions scored; deductions reference findings |
| Stage 8→9 | After Quality Review | All quality gates pass; devil's advocate completed; format matches spec |

## License

This skill is designed for use with the Claude AI assistant. See CLAUDE.md for skill-specific instructions.
