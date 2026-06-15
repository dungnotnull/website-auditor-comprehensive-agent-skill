# SECOND-KNOWLEDGE-BRAIN.md — Skill 8: website-auditor

> This is a living knowledge base. New entries are appended by `tools/knowledge_updater.py` on a weekly schedule. Every entry is tagged with its evidence tier and date of addition.

---

## Core Concepts & Frameworks

### Dimension 1: User Experience (UX)

**Nielsen's 10 Usability Heuristics (Jakob Nielsen, 1994)**
1. Visibility of system status — users should always know what's happening
2. Match between system and real world — use familiar language and conventions
3. User control and freedom — support undo/redo, easy exits
4. Consistency and standards — follow platform conventions
5. Error prevention — prevent problems before they occur
6. Recognition rather than recall — minimize memory load; make options visible
7. Flexibility and efficiency of use — accelerators for expert users
8. Aesthetic and minimalist design — no irrelevant information
9. Help users recognize, diagnose, and recover from errors — plain-language error messages
10. Help and documentation — easy to search, focused on user task

**Severity Scale (Nielsen):** 0 = not a problem; 1 = cosmetic; 2 = minor; 3 = major; 4 = catastrophe

**Gestalt Principles (applicable to web UI):**
- Proximity — elements close together are perceived as a group
- Similarity — similar elements are grouped visually
- Continuity — the eye follows lines and curves
- Figure/Ground — contrast between subject and background
- Closure — the mind fills in incomplete shapes

**Fitts's Law:** Interaction time is a function of distance and target size. Large, close CTAs convert better.

---

### Dimension 2: SEO

**Google's Core Ranking Factors (as of 2024):**
- Content quality and E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- Backlink authority and relevance
- Page experience signals (Core Web Vitals, mobile-friendliness, HTTPS, no intrusive interstitials)
- Structured data markup (Schema.org)
- Title tag and meta description optimization
- Internal linking structure and crawlability

**Technical SEO Checklist:**
- robots.txt: present, not blocking key pages
- sitemap.xml: present, submitted, up-to-date
- Canonical tags: correct, no self-referencing canonicals on paginated content
- Hreflang: correct for multi-language sites
- 404 handling: custom page with navigation
- Redirect chains: max 1 hop (301 preferred)
- Page speed: direct ranking factor for mobile
- HTTPS: required; HTTP→HTTPS redirect enforced

---

### Dimension 3: Performance (Core Web Vitals)

**Core Web Vitals (Google, current thresholds as of 2024):**

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |
| TTFB (Time to First Byte) | ≤ 800ms | 800ms–1.8s | > 1.8s |
| FCP (First Contentful Paint) | ≤ 1.8s | 1.8–3.0s | > 3.0s |

*Note: FID (First Input Delay) was replaced by INP in March 2024.*

**Performance Budget (mobile, good baseline):**
- Total page weight: < 1.5 MB
- HTTP requests: < 50
- JavaScript (uncompressed): < 300 KB
- Images: use WebP/AVIF; lazy load below-the-fold images

**Key Optimization Techniques:**
- Critical CSS inlining (eliminate render-blocking)
- Font display swap to prevent FOIT
- Image sizing (width/height attributes to prevent CLS)
- Server-side rendering or static generation for LCP improvement
- CDN for TTFB reduction

---

### Dimension 4: Accessibility (WCAG 2.2)

**WCAG 2.2 Conformance Levels:**
- Level A: Minimum (must have)
- Level AA: Standard (should have — legal requirement in many jurisdictions)
- Level AAA: Enhanced (aspirational)

**Key Level AA Success Criteria:**
- 1.1.1 Non-text Content — images have alt text (A)
- 1.3.1 Info and Relationships — structure conveyed programmatically (A)
- 1.4.3 Contrast (Minimum) — text contrast ≥ 4.5:1; large text ≥ 3:1 (AA)
- 1.4.4 Resize Text — text resizable to 200% without loss (AA)
- 2.1.1 Keyboard — all functionality via keyboard (A)
- 2.4.4 Link Purpose — link purpose clear from context (A)
- 2.4.7 Focus Visible — keyboard focus indicator visible (AA)
- 3.1.1 Language of Page — page language specified (A)
- 3.3.1 Error Identification — errors described in text (A)
- 4.1.1 Parsing — valid HTML (A)
- 4.1.2 Name, Role, Value — UI components have accessible names (A)

**New in WCAG 2.2 (vs 2.1):**
- 2.4.11 Focus Not Obscured (Minimum) — focused component not fully hidden
- 2.4.12 Focus Not Obscured (Enhanced) — not partially hidden (AAA)
- 2.4.13 Focus Appearance — focus indicator meets size and contrast requirements (AA)
- 2.5.3 Label in Name — visible label included in accessible name (A)
- 3.2.6 Consistent Help — help in same location across pages (A)
- 3.3.7 Redundant Entry — no re-entry of same information (A)
- 3.3.8 Accessible Authentication (Minimum) — no cognitive function test required (AA)

---

### Dimension 5: Content Quality (E-E-A-T)

**Google's E-E-A-T (Search Quality Rater Guidelines, 2022+):**
- **Experience** — first-hand experience of content creator (e.g., product reviews by actual users)
- **Expertise** — domain knowledge demonstrated in content
- **Authoritativeness** — recognized authority in the field (citations, backlinks, credentials)
- **Trustworthiness** — accuracy, transparency, safety, honesty

**Content Quality Signals:**
- Author byline with credentials
- Publication and last-updated dates
- References and citations to authoritative sources
- Factual accuracy (verifiable claims)
- Readability: Flesch–Kincaid Grade Level ≤ 10 for general audiences
- Content depth: covers the topic comprehensively (not thin content)
- Content freshness: updated within 12 months for time-sensitive topics
- Structured content: headers, bullet points, tables for scanability

**Readability Benchmarks:**
- General audience: Flesch Reading Ease 60–70 (7th–8th grade)
- Technical/B2B: Flesch Reading Ease 40–60 (college level acceptable)
- Healthcare: Plain Language Guidelines — max 6th grade for patient-facing content

---

### Dimension 6: Conversion Rate Optimization (CRO)

**CRO Frameworks:**
- **LIFT Model (Chris Goward, WiderFunnel):** Value Proposition, Relevance, Clarity, Urgency, Anxiety, Distraction — six conversion factors
- **PIE Framework (Widerfunnel):** Prioritize tests by Potential, Importance, Ease
- **BJ Fogg Behavior Model:** Behavior = Motivation × Ability × Trigger — all three must converge for conversion
- **Cialdini's Persuasion Principles:** Reciprocity, Commitment, Social Proof, Authority, Liking, Scarcity

**CRO Audit Checklist:**
- Value proposition clarity: stated above the fold in 5 seconds?
- CTA (Call-to-Action): single, prominent, action-oriented text ("Start Free Trial" > "Learn More")
- Social proof: testimonials, reviews, trust badges, logos, case studies
- Trust signals: SSL badge, privacy policy, contact information, refund policy
- Friction points: form length, required fields, number of steps to conversion
- Scarcity/urgency: legitimate time-limited offers
- Visual hierarchy: eye path guides toward CTA
- Mobile CTA: thumb-friendly size (minimum 44×44px touch target)
- Page load impact on conversion: each 1s delay → ~7% reduction in conversions (Akamai, 2017)

---

## Key Research Papers

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|----------|-----------|
| Usability Engineering | Jakob Nielsen | 1993 | Academic Press | ISBN 978-0125184069 | Foundational heuristics |
| Why Web Performance Matters | P. Souders | 2008 | O'Reilly | oreilly.com | Performance best practices |
| Measuring the User Experience | Tullis & Albert | 2013 | Morgan Kaufmann | ISBN 978-0124157811 | UX measurement methodology |
| The Impact of Page Load Times on Conversions | Multiple | 2017 | Akamai/Deloitte | akamai.com/resources | CRO + performance link |
| Web Content Accessibility Guidelines 2.2 | W3C | 2023 | W3C Recommendation | w3.org/TR/WCAG22 | Accessibility standard |
| Core Web Vitals: A New Ranking Signal | Google | 2021 | Google Search Central | developers.google.com/search | Performance + SEO link |
| Search Quality Evaluator Guidelines | Google | 2022 | Google | Static PDF | E-E-A-T framework |
| Conversion Optimization: The Art and Science | Khalid Saleh | 2014 | O'Reilly | ISBN 978-1449377588 | CRO methodology |
| Don't Make Me Think | Steve Krug | 2014 | New Riders | ISBN 978-0321965516 | UX cognitive load principle |
| Information Architecture for the WWW | Rosenfeld & Morville | 2015 | O'Reilly | ISBN 978-1491911686 | Navigation + IA patterns |

---

## State-of-the-Art Methods & Tools

### Performance Testing
- **Google PageSpeed Insights API** — free, returns Core Web Vitals field data + Lighthouse lab data
- **WebPageTest.org** — detailed waterfall, multi-location testing
- **Lighthouse CLI** — local audit: performance, accessibility, SEO, best practices
- **GTmetrix** — performance + YSlow scoring

### Accessibility Testing
- **axe DevTools** (Deque) — automated WCAG scanning
- **WAVE** (WebAIM) — visual accessibility feedback
- **NVDA / VoiceOver** — manual screen reader testing

### SEO Analysis
- **Google Search Console** — canonical source for indexation and Core Web Vitals field data
- **Screaming Frog SEO Spider** — technical crawl
- **Ahrefs / SEMrush** — backlink and keyword data

### UX Research
- **Hotjar / Microsoft Clarity** — heatmaps and session recordings
- **UserTesting.com** — moderated user testing
- **Maze** — unmoderated user testing

---

## Authoritative Data Sources

| Source | URL | Content Type |
|--------|-----|-------------|
| Google web.dev | web.dev | Performance, PWA, accessibility guides |
| Nielsen Norman Group | nngroup.com | UX research, heuristic articles |
| W3C Web Accessibility Initiative | w3.org/WAI | WCAG specifications |
| Google Search Central | developers.google.com/search | SEO guidelines, E-E-A-T |
| Baymard Institute | baymard.com | E-commerce UX research |
| ConversionXL / CXL | cxl.com | CRO research and frameworks |
| Google PageSpeed Insights | pagespeed.web.dev | Live performance scoring |
| WebAIM | webaim.org | Accessibility research and tools |
| HTTP Archive | httparchive.org | Real-world web performance data |
| ArXiv cs.HC | arxiv.org/list/cs.HC | HCI research papers |

---

## Analytical Frameworks

| Framework | Domain | Citation |
|-----------|--------|---------|
| Nielsen's 10 Usability Heuristics | UX | Nielsen, J. (1994). Usability Engineering |
| WCAG 2.2 | Accessibility | W3C (2023). Web Content Accessibility Guidelines 2.2 |
| Core Web Vitals | Performance | Google (2020–2024). Core Web Vitals Initiative |
| E-E-A-T | Content Quality | Google Search Quality Rater Guidelines (2022) |
| LIFT Model | CRO | Goward, C. (2012). You Should Test That |
| BJ Fogg Behavior Model | CRO | Fogg, B.J. (2009). A Behavior Model for Persuasive Design |
| Cialdini's Influence Principles | CRO | Cialdini, R. (1984). Influence: The Psychology of Persuasion |
| PIE Framework | CRO Prioritization | WiderFunnel (2011) |
| Gestalt Principles | Visual Design | Wertheimer, M. (1923) |
| Flesch–Kincaid Readability | Content Quality | Kincaid et al. (1975) |

---

## Self-Update Protocol

```yaml
crawl_sources:
  - url: "web.dev/blog"
    topics: ["performance", "core web vitals", "accessibility"]
    frequency: weekly
  - url: "nngroup.com/articles"
    topics: ["usability", "UX research", "heuristics"]
    frequency: weekly
  - url: "w3.org/WAI/news"
    topics: ["WCAG updates", "accessibility standards"]
    frequency: monthly
  - url: "developers.google.com/search/blog"
    topics: ["SEO", "ranking signals", "E-E-A-T"]
    frequency: weekly
  - url: "cxl.com/blog"
    topics: ["CRO", "conversion optimization", "A/B testing"]
    frequency: weekly
  - url: "arxiv.org/list/cs.HC/recent"
    topics: ["HCI", "web usability", "user experience"]
    frequency: weekly

append_format: |
  ### [SOURCE TYPE] [ADDED: YYYY-MM-DD]
  **Title:** {title}
  **Source:** {url}
  **Authors/Date:** {authors}, {date}
  **Key Finding:** {summary}
  **Evidence Tier:** {tier}
  **Relevance:** {dimension} — {why_relevant}

deduplication:
  method: URL hash + DOI (if present)
  storage: .knowledge_cache.json in tools/
```

---

## Knowledge Update Log

| Date | Source | Entries Added | Notes |
|------|--------|--------------|-------|
| 2026-06-11 | Manual seed | All core entries | Initial SECOND-KNOWLEDGE-BRAIN.md creation |
