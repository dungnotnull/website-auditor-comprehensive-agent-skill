# test-scenarios.md — Skill 8: website-auditor

## Purpose

This file defines concrete scenario-based tests for the `website-auditor` skill. Each scenario specifies: the input, expected behavior at each stage, and the success criteria for the final output.

---

## Scenario 1: SaaS Landing Page — Full 6-Dimension Audit

**Input:**
```
/website-auditor https://stripe.com
Website type: SaaS Landing Page
Audit scope: Full 6-dimension audit
Primary persona: Developer / startup founder evaluating payment APIs
Primary goal: Drive sign-up for free account
```

**Expected Behavior:**
- Stage 1: URL confirmed reachable; type set to SaaS; goal = conversion
- Stage 2: Technical recon extracts `<title>`, meta description, structured data (stripe.com uses JSON-LD), canonical, and performance indicators
- Stage 3: Framework selector applies landing-page weights: CRO 35%, UX 15%, Performance 15%, Content 15%, SEO 10%, Accessibility 10%
- Stage 4 Track A: UX finds strong value proposition (H1), clean visual hierarchy → low heuristic violations; Accessibility: likely WCAG AA compliant (large company site)
- Stage 4 Track B: Performance signals strong (known fast CDN); SEO: title optimized, meta description present, schema.org used
- Stage 4 Tracks C/D: Content: strong E-E-A-T (Stripe brand authority); CRO: single dominant CTA, strong social proof (logo wall)
- Stage 5: Competitors identified (Braintree, Adyen, PayPal Checkout); gap table produced
- Stage 6: Overall score expected B–A range (75–90) given stripe.com quality
- Stage 7: Roadmap likely in CRO/Accessibility dimension (minor improvements)

**Success Criteria:**
- [ ] All 6 dimensions scored
- [ ] Score ≥ 75 for stripe.com overall (expected high quality)
- [ ] Competitive benchmark includes at least Braintree and one other
- [ ] Roadmap has ≥ 5 items despite high overall score (even best sites have improvements)
- [ ] CRO dimension score highest (stripe.com optimizes heavily for conversion)
- [ ] Report follows exact output format from main.md

---

## Scenario 2: E-Commerce Product Page — CRO + Accessibility Focus

**Input:**
```
/website-auditor https://www.allbirds.com/products/mens-tree-runners
Website type: E-commerce (product page)
Audit scope: Full audit with CRO and Accessibility emphasis
Primary persona: Eco-conscious consumer, 28–45
Primary goal: Add to cart / purchase
```

**Expected Behavior:**
- Stage 3: E-commerce weights applied: CRO 25%, UX 20%, Performance 20%, SEO 15%, Accessibility 10%, Content 10%
- Stage 4 Track A: Check for product image alt text, form labels on size/color selectors, add-to-cart button accessible name, keyboard navigation of product variants
- Stage 4 Track D (CRO): Evaluate add-to-cart CTA prominence, trust signals (free returns, sustainability claims), social proof (reviews count visible), urgency signals (low stock messaging), variant selector friction
- Stage 5: Compare against other D2C e-commerce product pages (e.g., Patagonia, Casper)
- Baymard Institute e-commerce UX standards referenced in framework selection

**Success Criteria:**
- [ ] Baymard Institute referenced in framework selection for e-commerce UX
- [ ] Accessibility evaluation includes form input labels on product variant selectors
- [ ] CRO evaluation covers add-to-cart friction, trust signals, and social proof
- [ ] Benchmark includes at least one other D2C e-commerce product page
- [ ] Report Section "Dimension 4 (Accessibility)" covers variant selector inputs
- [ ] Roadmap Tier A contains at least one e-commerce-specific CRO quick win

---

## Scenario 3: Corporate Blog / Content Site — Content + SEO Focus

**Input:**
```
/website-auditor https://buffer.com/resources/social-media-marketing
Website type: Blog/Content Site
Audit scope: Full audit with Content Quality and SEO emphasis
Primary persona: Social media manager, small business owner
Primary goal: Increase organic search traffic; build brand authority
```

**Expected Behavior:**
- Stage 3: Blog/content weights applied: Content 30%, SEO 25%, UX 15%, Performance 15%, Accessibility 10%, CRO 5%
- Stage 4 Track C (Content): E-E-A-T evaluation — check for author byline with credentials, publication and updated dates, citations, content depth (estimated word count from HTML)
- Stage 4 Track B (SEO): Check structured data (Article schema), internal linking structure, heading hierarchy quality, meta description optimization for target keyword
- Flesch–Kincaid readability estimated from sample text
- Stage 5: Compare against competing marketing blogs (HubSpot, Sprout Social)
- CRO evaluation is minimal (newsletter signup only) — correctly weighted at 5%

**Success Criteria:**
- [ ] E-E-A-T evaluation present with author byline and date checks
- [ ] Flesch–Kincaid estimate or readability assessment included
- [ ] Article JSON-LD schema evaluated (present or missing)
- [ ] CRO dimension weighted at 5% (correct for blog type)
- [ ] Competitive benchmark includes HubSpot or Sprout Social
- [ ] Content Quality and SEO are the two largest sections in the final report

---

## Scenario 4: Government / Nonprofit Portal — Accessibility + Performance Focus

**Input:**
```
/website-auditor https://www.usa.gov
Website type: Government Portal
Audit scope: Full audit with Accessibility as critical priority
Primary persona: General public, including users with disabilities
Primary goal: Citizens find government services and information
```

**Expected Behavior:**
- Stage 3: Government weights applied: Accessibility 30%, UX 20%, Content 20%, Performance 15%, SEO 10%, CRO 5%
- Accessibility weight adjusted upward (user specified it as critical) → documented override
- Stage 4 Track A: WCAG 2.2 Level AA evaluation comprehensive; Section 508 flag added for US government context
- All 10 Nielsen heuristics evaluated with government service user context (older users, limited digital literacy)
- Stage 4 Track D (CRO): Near-minimal — citizens don't "convert" but do need to complete task flows (service request, form submission) → LIFT model applied to task completion, not purchase
- Stage 5: Compare with digital-leader government sites (gov.uk, singapore.gov.sg, canada.ca known for excellent digital service design)

**Success Criteria:**
- [ ] Accessibility weight ≥ 30% in framework matrix
- [ ] Section 508 mentioned as supplementary framework alongside WCAG 2.2
- [ ] WCAG 2.2 Level A and AA criteria both evaluated
- [ ] Benchmark includes at least one best-practice government site (gov.uk or equivalent)
- [ ] UX evaluation addresses navigation clarity for non-technical users
- [ ] CRO section reframed as "task completion" not "purchase conversion" (correct persona adaptation)

---

## Scenario 5: Startup Homepage — Full Audit + Competitive Benchmarking

**Input:**
```
/website-auditor https://linear.app
Website type: SaaS Product Page
Audit scope: Full audit
Primary persona: Engineering team lead, startup CTO
Primary goal: Start free trial or book demo
```

**Expected Behavior:**
- Stage 1: Auto-detects SaaS type from content
- All 6 dimensions covered per standard SaaS weights
- Stage 5: Competitive benchmarking against Notion, Asana, Jira (project management space)
- Stage 6: linear.app is known for excellent design → UX and CRO scores expected high; Accessibility may flag some contrast issues (dark theme)
- Stage 7: Roadmap reflects benchmark gaps vs. Notion (content depth) and Asana (social proof) even if absolute scores are high
- Devil's advocate check: validate that high UX score is not inflated by subjective preference

**Success Criteria:**
- [ ] SaaS weights applied (not landing page weights — this is a full product marketing site)
- [ ] Accessibility dimension evaluates dark-theme contrast ratios
- [ ] Benchmark includes 2–3 project management competitors
- [ ] Devil's advocate check completed (noted in Methodology Notes)
- [ ] Roadmap has benchmark-gap-derived items even if overall score is high
- [ ] Performance dimension estimates note that static analysis may underestimate JS-heavy SaaS app performance

---

## Scenario 6: Graceful Degradation — URL Unreachable (Negative Test)

**Input:**
```
/website-auditor https://this-domain-does-not-exist-xyzabc123.com
```

**Expected Behavior:**
- Stage 1: WebFetch returns connection error
- Harness reports: "URL is not reachable: [error details]. Please provide:
  a. A valid accessible URL
  b. Cached HTML content for analysis
  c. A public cache URL (e.g., Google Cache, Wayback Machine)"
- Harness does NOT proceed to Stage 2 with an empty result
- Harness DOES offer to continue with any HTML the user pastes directly

**Success Criteria:**
- [ ] Audit does not proceed silently with empty/error data
- [ ] Error message is human-readable with recovery options
- [ ] No scores or report sections generated from null data
- [ ] User is prompted with 3 clear recovery options

---

## Scenario 7: Partial Audit — SEO Only

**Input:**
```
/website-auditor https://example-blog.com
Audit scope: SEO only
```

**Expected Behavior:**
- Stage 3: Framework selector acknowledges single-dimension scope
- Stages 4B only: technical-audit run for SEO signals; performance skipped unless it overlaps SEO (page speed is a ranking factor — noted)
- Stages 4A, 4C, 4D: skipped (UX, Accessibility, Content, CRO not requested)
- Stage 5: Competitive benchmark focuses on SEO signals only
- Stage 6: Only SEO dimension scored; overall score not computed (insufficient dimensions)
- Stage 7: Roadmap SEO-only

**Success Criteria:**
- [ ] Harness respects partial scope request
- [ ] Report clearly states "Partial audit — SEO dimension only"
- [ ] Overall score section shows "N/A — partial audit"
- [ ] No fabricated scores for unevaluated dimensions
- [ ] Note in Methodology Notes explaining that a full audit is recommended for complete picture
