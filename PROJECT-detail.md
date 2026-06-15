# PROJECT-detail.md — Skill 8: website-auditor

## Executive Summary

The `website-auditor` skill is a comprehensive harness that evaluates any public website across six dimensions — UX, SEO, Performance, Accessibility, Content Quality, and Conversion Rate Optimization (CRO) — using world-renowned evaluation frameworks. It produces a professional audit report with per-dimension scores, an overall weighted grade, competitive benchmarks, and a prioritized improvement roadmap. All findings are traceable to authoritative sources. The skill's knowledge base self-improves via a weekly crawl4ai pipeline.

---

## Problem Statement

Website quality is multidimensional: a technically fast site can still fail at UX; a visually polished site can rank poorly in search. Most teams evaluate only one or two dimensions (usually "does it look good?" and "is it fast?"), leaving critical gaps. Agencies that perform professional audits are expensive and often non-repeatable. This skill closes that gap by systematically applying the same evaluation methodology that elite digital agencies use — covering all six dimensions — in a reproducible, evidence-backed, Claude-executed harness.

---

## Target Users & Use Cases

| User | Trigger | Expected Output |
|------|---------|-----------------|
| Product Manager | "Audit our new SaaS landing page before launch" | Full 6-dimension report with scores and ranked improvements |
| SEO Specialist | "What's wrong with our website's SEO and content?" | SEO + Content Quality sub-reports with specific fixes |
| Frontend Developer | "Can you review this portfolio site for UX and accessibility?" | UX + Accessibility findings with WCAG violation references |
| Startup Founder | "How does our website compare to competitors?" | Benchmarking report with competitive gap analysis |
| Digital Marketer | "Why isn't our landing page converting?" | CRO audit with A/B test hypotheses and priority improvements |
| Agency Account Manager | "I need a client-ready audit report for this e-commerce site" | Full professional report, suitable for client delivery |

---

## Harness Architecture

```
/website-auditor [URL] [options]
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  Stage 1: URL Intake & Scope Definition             │
│  • Confirm URL accessibility (WebFetch check)       │
│  • Identify website type & primary user persona     │
│  • Clarify audit scope (all 6 dims vs. targeted)    │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 2: Technical Reconnaissance                  │
│  [sub-technical-audit]                              │
│  • Fetch HTML, headers, sitemap, robots.txt         │
│  • Extract meta tags, structured data, link profile │
│  • Record raw performance signals (load time, size) │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 3: Framework Selection                       │
│  [sub-evaluation-framework-selector]                │
│  • Match frameworks to website type                 │
│  • Confirm scoring weights per dimension            │
└───────────────────┬─────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
  [Dim 1+4]     [Dim 2+3]   [Dim 5+6]
  sub-ux-       sub-tech-   Direct harness
  accessibility  audit      (content + CRO)
  -audit
         │          │          │
         └──────────┼──────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 5: Competitive Benchmarking                  │
│  [sub-competitive-benchmarker]                      │
│  • Identify 2–3 industry peers                      │
│  • Compare dimension scores vs. benchmarks          │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 6: Scoring & Synthesis                       │
│  [sub-scoring-engine]                               │
│  • Weighted aggregate score (0–100 per dimension)   │
│  • Overall grade: A/B/C/D/F with percentile         │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 7: Improvement Roadmap                       │
│  [sub-improvement-roadmap]                          │
│  • Effort × Impact matrix (Quick Wins / Strategic)  │
│  • Numbered prioritized action list                 │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 8: Quality Gate Review                       │
│  • All 6 dimensions covered?                        │
│  • All scores traceable to evidence?                │
│  • Roadmap has at least 5 actionable items?         │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 9: Final Report Output                       │
│  • Executive Summary                                │
│  • Dimension Score Table                            │
│  • Per-Dimension Findings                           │
│  • Competitive Benchmark Summary                    │
│  • Overall Grade + Interpretation                   │
│  • Prioritized Improvement Roadmap                  │
└─────────────────────────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-evaluation-framework-selector
- **Purpose:** Matches evaluation frameworks to the website type and audit goals.
- **Inputs:** Website type (landing page / SaaS / e-commerce / blog / portal), audit goals
- **Outputs:** Framework selection matrix — which framework applies to each dimension, scoring weights per dimension
- **Tools:** WebSearch (look up latest framework updates), Read (SECOND-KNOWLEDGE-BRAIN.md)
- **Quality Gate:** At least one named, citable framework per dimension

### sub-scoring-engine
- **Purpose:** Computes weighted scores per dimension and an overall aggregate grade.
- **Inputs:** Raw findings per dimension (list of pass/fail/partial checks with severity)
- **Outputs:** Dimension scorecard (0–100 per dimension), weighted overall score (0–100), grade (A–F), percentile interpretation
- **Tools:** No external tools — pure computation from inputs
- **Quality Gate:** Scores sum correctly; weights defined and documented

### sub-improvement-roadmap
- **Purpose:** Synthesizes all findings into a prioritized action plan.
- **Inputs:** All dimension findings, scores, competitive benchmark gaps
- **Outputs:** Effort × Impact matrix (Quick Wins / Strategic Investments / Low Priority), numbered action list with estimated effort (hours/days) and expected impact
- **Tools:** No external tools — synthesis step
- **Quality Gate:** Minimum 5 actionable items; each item has dimension, effort, and expected outcome

### sub-technical-audit
- **Purpose:** Deep technical analysis covering performance and SEO signals.
- **Inputs:** URL
- **Outputs:** Performance metrics (load time, page size, request count, Core Web Vitals estimates), SEO signals (meta tags, canonical, robots, sitemap, structured data, internal links), HTTP headers, security headers
- **Tools:** WebFetch (live data), WebSearch (PageSpeed API reference, SEO checklist)
- **Quality Gate:** At least 15 distinct technical signals checked

### sub-ux-accessibility-audit
- **Purpose:** Evaluates UX design quality using Nielsen's 10 heuristics + Gestalt principles; evaluates accessibility against WCAG 2.2.
- **Inputs:** Website HTML (fetched), screenshots or visual description
- **Outputs:** Heuristic violation list (heuristic name, severity 1–3, evidence), WCAG compliance checklist (Level A/AA), UX score, Accessibility score
- **Tools:** WebFetch (fetch live HTML), Read (SECOND-KNOWLEDGE-BRAIN.md for heuristic definitions), WebSearch (WCAG 2.2 criteria)
- **Quality Gate:** All 10 Nielsen heuristics evaluated; WCAG Level AA criteria checked

### sub-competitive-benchmarker
- **Purpose:** Identifies industry peer websites and compares audit dimension scores.
- **Inputs:** Website URL, website type/industry
- **Outputs:** Table of 2–3 competitor/benchmark sites with per-dimension comparison, gap analysis highlighting where target site lags most
- **Tools:** WebSearch (find competitors), WebFetch (fetch competitor pages for surface-level comparison)
- **Quality Gate:** At least 2 comparison sites identified; gap analysis references specific dimension scores

---

## Skill File Format Specification

Each skill file (main.md and sub-*.md) must have:

```yaml
---
name: skill-name
description: One-line summary
---
```

Followed by required sections:
- `## Role & Persona`
- `## Workflow (Harness Flow)` — numbered steps
- `## Sub-skills Available` (main only)
- `## Tools`
- `## Output Format`
- `## Quality Gates`

---

## E2E Execution Flow

1. User invokes `/website-auditor https://example.com`
2. Harness confirms URL is reachable (WebFetch HEAD request)
3. User is asked to confirm website type and audit scope (or harness auto-detects from HTML)
4. [sub-technical-audit] fetches full page HTML, headers, sitemap.xml, robots.txt; extracts SEO signals and performance indicators
5. [sub-evaluation-framework-selector] reviews SECOND-KNOWLEDGE-BRAIN.md and confirms framework + weight selection
6. [sub-ux-accessibility-audit] evaluates UX (heuristics) and accessibility (WCAG 2.2) from fetched HTML
7. Harness performs Content Quality audit: checks E-E-A-T signals (expertise, authoritativeness, trustworthiness, experience), readability (Flesch–Kincaid or equivalent), content depth, freshness
8. Harness performs CRO audit: checks CTA clarity, value proposition, social proof, trust signals, friction points in key conversion flows
9. [sub-competitive-benchmarker] searches for 2–3 peer sites, fetches them, compares surface signals
10. [sub-scoring-engine] aggregates all findings into dimension scores and overall grade
11. [sub-improvement-roadmap] generates prioritized action plan
12. Quality gate check: validates completeness
13. Final report is written and presented

**Error handling:**
- If WebFetch fails for the target URL: report as unreachable; continue with HTML provided by user or public cache
- If WebSearch is unavailable: fall back to SECOND-KNOWLEDGE-BRAIN.md frameworks; note limitation
- If competitor sites are unreachable: use known industry benchmarks from SECOND-KNOWLEDGE-BRAIN.md

---

## SECOND-KNOWLEDGE-BRAIN Integration

The `SECOND-KNOWLEDGE-BRAIN.md` file stores:
- Core Web Vitals thresholds (current Google-published values)
- Nielsen's 10 heuristics (canonical definitions)
- WCAG 2.2 Level A/AA success criteria checklist
- E-E-A-T guidelines and content quality rubrics
- CRO principles (loss aversion, social proof, trust signals, friction taxonomy)
- Benchmark data: industry-average scores by site type
- Research papers: HCI, information architecture, web performance, SEO

**Crawl sources:** web.dev, nngroup.com, w3.org/WAI, developers.google.com/search, baymard.com, conversionxl.com, arxiv.org (cs.HC, cs.IR)

**Append format:** Each new entry tagged with `[ADDED: YYYY-MM-DD]` and evidence tier.

---

## Quality Gates

Before the final report is presented, ALL of the following must be true:

- [ ] All 6 audit dimensions evaluated (UX, SEO, Performance, Accessibility, Content, CRO)
- [ ] Every dimension score has at least 3 supporting evidence points
- [ ] Evaluation framework cited for each dimension score
- [ ] Competitive benchmark includes at least 2 peer sites
- [ ] Improvement roadmap has at minimum 5 actionable items
- [ ] Each roadmap item has: dimension, description, estimated effort, expected impact
- [ ] Executive summary accurately reflects overall grade and top 3 issues
- [ ] No unsupported claims (every assertion backed by fetched data or cited framework)

---

## Test Scenarios

See `tests/test-scenarios.md` for the full scenario set.

**Summary:**
1. SaaS landing page — full 6-dimension audit
2. E-commerce product page — CRO + Accessibility focused
3. Corporate blog — Content Quality + SEO focused
4. Government/nonprofit portal — Accessibility + Performance focused
5. Startup homepage — Full audit + competitive benchmarking

---

## Key Design Decisions

1. **Six dimensions, not more** — covering UX, SEO, Performance, Accessibility, Content, CRO captures the full quality surface without audit fatigue. Adding more dimensions (e.g., security) would require a separate specialized harness.
2. **Weighted scoring, not uniform** — different website types have different priorities (e.g., landing page: CRO > SEO; blog: Content > Performance). Weights are set by the framework-selector sub-skill.
3. **Live data where possible** — WebFetch pulls the real, current page. This distinguishes the audit from static analyses that miss runtime behavior.
4. **Framework citations mandatory** — every dimension score references a named framework (Nielsen, WCAG, Core Web Vitals, E-E-A-T, etc.). This makes the audit defensible and educational.
5. **Competitive benchmarking as a required stage** — clients understand scores better when they see how they compare to peers, not just absolute numbers.
6. **Self-improving knowledge** — the crawl pipeline ensures the skill stays current with evolving standards (Core Web Vitals thresholds change; WCAG versions update).
7. **Graceful degradation** — if live data is unavailable, the skill falls back to SECOND-KNOWLEDGE-BRAIN.md and clearly flags the limitation in the report.
8. **Effort × Impact matrix** — recommendations are not a raw list; they are organized by business impact vs. implementation effort so stakeholders can prioritize without needing technical expertise.
