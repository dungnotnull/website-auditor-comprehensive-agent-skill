"""
test_skill_validation.py -- Validation tests for the website-auditor skill structure.

Validates skill files have correct sections, quality gates, harness flow, etc.

Run: python tests/test_skill_validation.py
"""

import sys
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = SKILL_DIR / "skills"
TOOLS_DIR = SKILL_DIR / "tools"
TESTS_DIR = SKILL_DIR / "tests"


def read_file(path: Path) -> str:
    """Read file, stripping BOM if present."""
    content = path.read_text(encoding="utf-8-sig")
    return content


passed = 0
failed = 0

def check(name, condition, msg=""):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name} -- {msg}")
        failed += 1


# ── Main Harness ─────────────────────────────────────────────
main_content = read_file(SKILLS_DIR / "main.md")

check("main.md has YAML frontmatter", main_content.lstrip().startswith("---"))
check("main.md has Role & Persona", "## Role & Persona" in main_content)

for i in range(1, 10):
    check(f"main.md has Stage {i}", f"### Stage {i}:" in main_content)

check("main.md has Stage 4->5 Quality Gate", "Stage 4" in main_content and "Quality Gate" in main_content)
check("main.md has Stage 5->6 Quality Gate", "Stage 5" in main_content and "Quality Gate" in main_content)
check("main.md has Stage 6->7 Quality Gate", "Stage 6" in main_content and "Quality Gate" in main_content)
check("main.md has Stage 8->9 Quality Gate", "Stage 8" in main_content and "Quality Gate" in main_content)
check("main.md has Devils Advocate", "devil" in main_content.lower() and "advocate" in main_content.lower())
check("main.md has E-E-A-T Content Quality", "E-E-A-T" in main_content)
check("main.md has Experience in Content", "Experience" in main_content)
check("main.md has Expertise in Content", "Expertise" in main_content)
check("main.md has Readability in Content", "Readability" in main_content or "Flesch" in main_content)
check("main.md has Freshness in Content", "Freshness" in main_content)
check("main.md has LIFT Model CRO", "LIFT Model" in main_content or "LIFT" in main_content)
check("main.md has CTA in CRO", "CTA" in main_content)
check("main.md has Social proof in CRO", "social proof" in main_content.lower())
check("main.md has Trust signals in CRO", "trust signal" in main_content.lower())
check("main.md has Friction in CRO", "Friction" in main_content or "friction" in main_content)
check("main.md has Graceful Degradation", "Graceful Degradation" in main_content)
check("main.md has Partial Audit", "Partial Audit" in main_content)
check("main.md has Output Format", "## Output Format" in main_content)
check("main.md has Executive Summary in output", "Executive Summary" in main_content)
check("main.md has Dimension Scores in output", "Dimension Scores" in main_content)
check("main.md has Competitive Benchmark in output", "Competitive Benchmark" in main_content)
check("main.md has Improvement Roadmap in output", "Improvement Roadmap" in main_content or "Prioritized Improvement Roadmap" in main_content)
check("main.md has Methodology Notes in output", "Methodology Notes" in main_content)
check("main.md has sub-technical-audit", "sub-technical-audit" in main_content)
check("main.md has sub-evaluation-framework-selector", "sub-evaluation-framework-selector" in main_content)
check("main.md has sub-ux-accessibility-audit", "sub-ux-accessibility-audit" in main_content)
check("main.md has sub-competitive-benchmarker", "sub-competitive-benchmarker" in main_content)
check("main.md has sub-scoring-engine", "sub-scoring-engine" in main_content)
check("main.md has sub-improvement-roadmap", "sub-improvement-roadmap" in main_content)
check("main.md has Quality Gates Summary", "Quality Gates" in main_content)

# ── Sub-Skill Files ──────────────────────────────────────────
SUB_SKILLS = [
    "sub-technical-audit.md",
    "sub-ux-accessibility-audit.md",
    "sub-evaluation-framework-selector.md",
    "sub-scoring-engine.md",
    "sub-improvement-roadmap.md",
    "sub-competitive-benchmarker.md",
]

REQUIRED_SECTIONS = ["Role & Persona", "Workflow", "Tools", "Output Format", "Quality Gates"]

for filename in SUB_SKILLS:
    path = SKILLS_DIR / filename
    check(f"{filename} exists", path.exists())
    if path.exists():
        content = read_file(path)
        check(f"{filename} has YAML frontmatter", content.lstrip().startswith("---"))
        frontmatter = content.split("---")[1] if "---" in content else ""
        check(f"{filename} has name in frontmatter", "name:" in frontmatter)
        check(f"{filename} has description in frontmatter", "description:" in frontmatter)
        for section in REQUIRED_SECTIONS:
            check(f"{filename} has {section}", section in content)

# Sub-skill specific checks
tech_audit = read_file(SKILLS_DIR / "sub-technical-audit.md")
check("sub-technical-audit covers >= 10 SEO signals", "SEO" in tech_audit and ("15" in tech_audit or "minimum 15" in tech_audit.lower() or "15 distinct" in tech_audit.lower() or "Minimum 15" in tech_audit))

ux_audit = read_file(SKILLS_DIR / "sub-ux-accessibility-audit.md")
for i in range(1, 11):
    check(f"sub-ux-audit has Heuristic {i}", f"Heuristic {i}" in ux_audit)
check("sub-ux-audit covers WCAG 2.2", "WCAG 2.2" in ux_audit)
check("sub-ux-audit covers Level A", "Level A" in ux_audit)
check("sub-ux-audit covers Level AA", "Level AA" in ux_audit)

scoring = read_file(SKILLS_DIR / "sub-scoring-engine.md")
check("sub-scoring-engine has grade thresholds", "90" in scoring and "75" in scoring and "60" in scoring)

benchmarker = read_file(SKILLS_DIR / "sub-competitive-benchmarker.md")
for dim in ["UX", "SEO", "Performance", "Accessibility", "Content", "CRO"]:
    check(f"sub-competitive-benchmarker has {dim}", dim in benchmarker)

roadmap = read_file(SKILLS_DIR / "sub-improvement-roadmap.md")
check("sub-improvement-roadmap has Quick Wins", "Quick Wins" in roadmap or "Quick Win" in roadmap)
check("sub-improvement-roadmap has Strategic", "Strategic" in roadmap)
check("sub-improvement-roadmap has Effort and Impact", "Effort" in roadmap and "Impact" in roadmap)

framework = read_file(SKILLS_DIR / "sub-evaluation-framework-selector.md")
check("sub-framework-selector has weight table", "Landing Page" in framework or "landing page" in framework)
check("sub-framework-selector has SaaS weights", "SaaS" in framework)
check("sub-framework-selector has E-commerce weights", "E-commerce" in framework or "e-commerce" in framework)

# ── Knowledge Updater ────────────────────────────────────────
check("knowledge_updater.py exists", (TOOLS_DIR / "knowledge_updater.py").exists())
check("requirements.txt exists", (TOOLS_DIR / "requirements.txt").exists())

ku_content = read_file(TOOLS_DIR / "knowledge_updater.py")
check("knowledge_updater has SOURCES", "SOURCES" in ku_content)
check("knowledge_updater has web.dev source", "web.dev" in ku_content)
check("knowledge_updater has nngroup source", "nngroup" in ku_content)
check("knowledge_updater has W3C source", "w3.org" in ku_content or "WAI" in ku_content)
check("knowledge_updater has conversionxl/cxl source", "cxl" in ku_content or "conversionxl" in ku_content)
check("knowledge_updater has arxiv source", "arxiv" in ku_content)
check("knowledge_updater has dedup (url_hash)", "url_hash" in ku_content)
check("knowledge_updater has dedup (is_duplicate)", "is_duplicate" in ku_content)
check("knowledge_updater has DOI dedup", "doi_hash" in ku_content or "seen_dois" in ku_content)
check("knowledge_updater has CLI argparse", "argparse" in ku_content)
check("knowledge_updater has --dry-run", "--dry-run" in ku_content)
check("knowledge_updater has [ADDED: date] format", "[ADDED:" in ku_content or "ADDED:" in ku_content)
check("knowledge_updater has crawl4ai integration", "crawl4ai" in ku_content)
check("knowledge_updater has requests fallback", "requests" in ku_content)

# ── SECOND-KNOWLEDGE-BRAIN ────────────────────────────────────
skb_content = read_file(SKILL_DIR / "SECOND-KNOWLEDGE-BRAIN.md")

for dim in ["Dimension 1", "Dimension 2", "Dimension 3", "Dimension 4", "Dimension 5", "Dimension 6"]:
    check(f"SKB has {dim}", dim in skb_content)

check("SKB has Nielsen heuristics", "Nielsen" in skb_content)
check("SKB has WCAG", "WCAG" in skb_content and "2.2" in skb_content)
check("SKB has Core Web Vitals", "Core Web Vitals" in skb_content)
check("SKB has LCP", "LCP" in skb_content)
check("SKB has CLS", "CLS" in skb_content)
check("SKB has INP", "INP" in skb_content)
check("SKB has E-E-A-T", "E-E-A-T" in skb_content)
check("SKB has LIFT model", "LIFT" in skb_content)
check("SKB has Knowledge Update Log", "Knowledge Update Log" in skb_content)
check("SKB has Analytical Frameworks", "Analytical Frameworks" in skb_content)
check("SKB has Self-Update Protocol", "Self-Update Protocol" in skb_content or "crawl_sources" in skb_content)

# ── Test Scenarios ──────────────────────────────────────────
test_scenarios = read_file(TESTS_DIR / "test-scenarios.md")
for i in range(1, 8):
    check(f"test-scenarios has Scenario {i}", f"Scenario {i}" in test_scenarios)
check("test-scenarios has Success Criteria", "Success Criteria" in test_scenarios)
check("test-scenarios has negative test (unreachable)", "unreachable" in test_scenarios.lower() or "does not exist" in test_scenarios.lower() or "Unreachable" in test_scenarios)
check("test-scenarios has partial audit test", "Partial" in test_scenarios or "partial" in test_scenarios or "SEO only" in test_scenarios)
check("test-scenarios has Expected Behavior", "Expected Behavior" in test_scenarios)

# ── Project Tracking ────────────────────────────────────────
tracking = read_file(SKILL_DIR / "PROJECT-DEVELOPMENT-PHASE-TRACKING.md")
for phase in ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]:
    check(f"tracking has {phase}", phase in tracking)

# ── CLAUDE.md ────────────────────────────────────────────────
claude = read_file(SKILL_DIR / "CLAUDE.md")
check("CLAUDE.md has Skill Identity", "Skill Identity" in claude)
check("CLAUDE.md has sub-technical-audit", "sub-technical-audit" in claude)
check("CLAUDE.md has sub-evaluation-framework-selector", "sub-evaluation-framework-selector" in claude)
check("CLAUDE.md has sub-scoring-engine", "sub-scoring-engine" in claude)
check("CLAUDE.md has sub-improvement-roadmap", "sub-improvement-roadmap" in claude)
check("CLAUDE.md has sub-ux-accessibility-audit", "sub-ux-accessibility-audit" in claude)
check("CLAUDE.md has sub-competitive-benchmarker", "sub-competitive-benchmarker" in claude)
check("CLAUDE.md has SECOND-KNOWLEDGE-BRAIN", "SECOND-KNOWLEDGE-BRAIN" in claude)

# ── Summary ─────────────────────────────────────────────────
print(f"\nResults: {passed} passed, {failed} failed, {passed + failed} total")
if failed > 0:
    sys.exit(1)
print("All skill validation tests passed!")
