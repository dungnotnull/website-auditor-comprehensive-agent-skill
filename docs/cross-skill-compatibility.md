# Cross-Skill Compatibility — Cluster B Shared Sub-Skills

## Overview

The `website-auditor` skill (Skill 8) belongs to **Cluster B — Technical Evaluation Harnesses**, alongside:

- **Skill 4:** `uiux-code-auditor` — Evaluates UI/UX code quality
- **Skill 6:** `code-quality-auditor` — Evaluates general code quality

Three sub-skills are designed to be **shared across all Cluster B skills** because they solve generic evaluation problems (framework selection, scoring, and prioritization) that apply regardless of whether the audit target is a website, UI code, or general source code.

---

## Shared Sub-Skills

### 1. `sub-evaluation-framework-selector.md`

**Purpose:** Selects evaluation frameworks and scoring weights based on the target type and audit goals.

**Why it's shared:** Every Cluster B skill needs to select an appropriate evaluation framework. The framework-selection logic is parameterized by `target_type` (website, UI code, general code) and `audit_goals`, making it reusable across skills.

**Skill-specific overrides for website-auditor:**
- Website type weight table (landing page, SaaS, e-commerce, blog, portal, government) — this is website-auditor-specific
- CRO frameworks (LIFT Model, Cialdini) — unique to website audits, not applicable to code audits
- Content Quality frameworks (E-E-A-T, Flesch–Kincaid) — unique to website audits

**Compatibility with other Cluster B skills:**
- In `uiux-code-auditor`: Replace website type weight table with UI component type weights. Remove CRO/Content dimensions. Add code-quality-specific frameworks (Material Design, Apple HIG, etc.)
- In `code-quality-auditor`: Replace weight table with code type weights (frontend, backend, API, etc.). Remove CRO, Content, UX, Accessibility dimensions. Add code-smell frameworks (SOLID, Clean Code, etc.)

### 2. `sub-scoring-engine.md`

**Purpose:** Computes weighted per-dimension scores and an overall aggregate grade from raw findings.

**Why it's shared:** The scoring engine is a pure computation step. It takes dimension findings and weights as input, and produces a scorecard. This logic is identical across all evaluation skills — only the dimensions and their severities change.

**Skill-specific overrides for website-auditor:**
- 6 dimensions: UX, SEO, Performance, Accessibility, Content Quality, CRO
- Severity calibration per dimension (e.g., WCAG A failure = Critical, Nielsen severity 4 = Critical)
- Grade boundaries: A ≥ 90, B ≥ 75, C ≥ 60, D ≥ 45, F < 45

**Compatibility with other Cluster B skills:**
- In `uiux-code-auditor`: Dimensions change to UX Design, Accessibility, Visual Design, Interaction Patterns, Code Quality. Severity calibration changes to code-specific definitions.
- In `code-quality-auditor`: Dimensions change to Correctness, Readability, Maintainability, Performance, Security, Testing. Severity calibration uses code-smell taxonomy.

### 3. `sub-improvement-roadmap.md`

**Purpose:** Synthesizes all findings into a prioritized action plan using an Effort × Impact matrix.

**Why it's shared:** The prioritization logic (Quick Wins / Strategic Investments / Low Priority) is universal. Every evaluation skill produces findings that need to be organized by effort and impact.

**Skill-specific overrides for website-auditor:**
- Dimension names map to website dimensions (UX, SEO, etc.)
- Effort estimates are in hours/days for web development tasks
- Impact measured in audit score points recovered + business outcomes

**Compatibility with other Cluster B skills:**
- In `uiux-code-auditor`: Dimension names map to code dimensions. Effort measured in development hours. Impact measured in code quality metrics.
- In `code-quality-auditor`: Same structure, different dimension labels and effort/impact scales.

---

## How to Use Shared Sub-Skills in Other Cluster B Skills

### Option 1: Copy and Customize (Recommended)

Copy the shared sub-skill file to the target skill's `skills/` directory and apply the documented overrides. This is the simplest approach and avoids cross-repository dependencies.

```bash
# From uiux-code-auditor repo:
cp /path/to/website-auditor/skills/sub-evaluation-framework-selector.md skills/
cp /path/to/website-auditor/skills/sub-scoring-engine.md skills/
cp /path/to/website-auditor/skills/sub-improvement-roadmap.md skills/
# Then apply skill-specific overrides as documented above
```

### Option 2: Symlink (For Development Only)

During development, symlinks can be used to share the files. This is not recommended for production because it creates a hard dependency between repositories.

```bash
# From uiux-code-auditor repo:
ln -s /path/to/website-auditor/skills/sub-evaluation-framework-selector.md skills/
ln -s /path/to/website-auditor/skills/sub-scoring-engine.md skills/
ln -s /path/to/website-auditor/skills/sub-improvement-roadmap.md skills/
```

### Option 3: Canonical Reference (For Documentation Only)

Reference the website-auditor versions as the canonical source in the other skill's documentation. When changes are needed, update the canonical version and then propagate changes manually.

---

## Verification Checklist

When adapting shared sub-skills for another Cluster B skill:

- [ ] All dimension references updated (website → target type)
- [ ] Weight table replaced with skill-appropriate weights
- [ ] Framework citations updated (remove website-specific frameworks, add code-specific ones)
- [ ] Severity calibration updated for the new domain
- [ ] Output format still produces scorecard + roadmap
- [ ] Quality gates still enforce completeness
- [ ] No website-auditor-specific logic bleeds into the shared file
- [ ] The shared sub-skill still works correctly when invoked from website-auditor

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-06-15 | Initial cross-skill compatibility documentation | website-auditor skill |
