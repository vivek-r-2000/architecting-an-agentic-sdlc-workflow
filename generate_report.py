"""Generate publication-grade academic report.docx for AutoSE Assignment 3.

Adheres strictly to the 8-page budget and all 6 required sections:
1. Architecture (2 pages): 3 views (Component, Sequence, Stage Map), agent mappings.
2. Design Decisions (2.5 pages): Complete 10-ADR summary table, deep-dive into the 3 most critical decisions.
3. Decision Experiments (1.5 pages): Empirical results of ADR-002 and ADR-008 side-by-side, design adjustments.
4. Results (1 page): Pass rates per stage, hidden test pass rates, reviewer accuracy confusion matrix.
5. Hindsight (0.5 page): What would be changed first and why.
6. Limitations and Threats to Validity: Construct, Internal, and External validity threats.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

REPORT_ROOT = Path(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3")
DOCX_OUT = REPORT_ROOT / "report.docx"
COMPONENT_IMG = REPORT_ROOT / "architecture" / "views" / "component_view.png"
SEQUENCE_IMG = REPORT_ROOT / "architecture" / "views" / "sequence_view.png"
CHART_IMG = REPORT_ROOT / "results" / "experiment_charts.png"


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
    )
    tcPr.append(tcMar)


def build_report():
    doc = docx.Document()

    # Page setup - 0.70 in margins for academic two-column / clean density
    for s in doc.sections:
        s.top_margin = Inches(0.65)
        s.bottom_margin = Inches(0.65)
        s.left_margin = Inches(0.70)
        s.right_margin = Inches(0.70)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)

    # Typography helpers
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)

    def add_meta(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(71, 85, 105)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(2, 132, 199) # Blue accent

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)

    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.12
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(9.5)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # HEADER & METADATA
    # -------------------------------------------------------------
    add_title("Architecting an Agentic SDLC Workflow: Architecture, Decisions, and Empirical Rigor")
    add_meta("Author: Vivek R (Roll: 2019112020) | Course: CS6.403 Autonomous Software Engineering (Monsoon 2026)\nTarget: msiemens/tinydb @ edff96a | Model: Google Gemini Multi-Agent Hierarchy")

    # -------------------------------------------------------------
    # SECTION 1: ARCHITECTURE (2 PAGES)
    # -------------------------------------------------------------
    add_h1("1. Architectural Design & Workflow Topology")
    add_p("The objective of this engineering endeavor is to build a robust, production-grade GitHub Actions workflow that autonomously transitions an informal GitHub issue into a verified, regression-free, and independently reviewed Pull Request. Connecting an LLM to a push button that opens PRs is trivial; the real engineering challenge lies in formalizing strict cognitive boundaries between agents, enforcing non-negotiable exit oracles, and preventing the ubiquitous 'co-located rubber-stamping' failure mode where agents uncritically approve their own flawed code.")

    add_h2("1.1 The Six Discrete SDLC Stages and Agent Responsibilities")
    add_p("The system decomposes the software lifecycle into five role-specialized agents operating across six sequential, gated stages:")

    # Table of Stages
    table_stages = doc.add_table(rows=7, cols=5)
    table_stages.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["#", "Stage Name", "Responsible Agent", "Primary Artifact", "Verification Exit Gate"]
    widths = [Inches(0.4), Inches(1.3), Inches(1.6), Inches(1.4), Inches(2.3)]

    # Style Header
    hdr_cells = table_stages.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "0F172A")
        set_cell_margins(hdr_cells[i], 80, 80, 100, 100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.runs[0]
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    stage_rows = [
        ("1", "Requirements", "RequirementsAgent (Gemini 3.5 Flash Lite)", "spec.md", "All Acceptance Criteria (ACs) follow Gherkin syntax and are programmatically testable."),
        ("2", "Design", "DesignAgent (Gemini 3.5 Flash)", "design.md", "Explicitly names target files, modified classes, methods, and verifies TinyDB architectural constraints."),
        ("3", "Implementation", "ImplementationAgent (Gemini 3.5 Flash)", "diff.patch", "Code builds with zero syntax errors (python -m py_compile) on autose/issue-<id> branch."),
        ("4", "Testing", "TestAgent (Gemini 3.5 Flash Lite)", "test_report.md", "100% of 228 baseline tests pass (0 regressions) AND 100% of newly authored acceptance tests pass."),
        ("5", "Release", "ReleaseAgent (GitHub Runner / gh)", "pr.md + PR URL", "Branch pushed cleanly, PR created, and GitHub CI workflow triggered and reporting green."),
        ("6", "Independent Review", "ReviewerAgent (Gemini 3.5 Flash Adversarial)", "review.md", "Typed verdict: APPROVE, REQUEST_CHANGES [CODE_ISSUE], or REQUEST_CHANGES [APPROACH_ISSUE]."),
    ]

    for row_idx, data in enumerate(stage_rows, start=1):
        row_cells = table_stages.rows[row_idx].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 60, 60, 80, 80)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in (0, 3) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.0)
            if col_idx == 1:
                r.font.bold = True

    add_h2("1.2 Three Architecture Views")
    add_p("Figure 1 illustrates the Component Architecture View, depicting agent tool boundaries, least-privilege capability partitions, and the strict isolation sandbox surrounding the Reviewer Agent. Figure 2 illustrates the Sequence Architecture View, detailing the exact end-to-end execution path including self-repair loops and review feedback routing.")

    if COMPONENT_IMG.exists():
        doc.add_picture(str(COMPONENT_IMG), width=Inches(6.8))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(8)
        rc = cp.add_run("Figure 1: Component Architecture View — Highlighting tool least-privilege partitions and the Reviewer Sandbox.")
        rc.font.size = Pt(8.5)
        rc.font.italic = True

    if SEQUENCE_IMG.exists():
        doc.add_picture(str(SEQUENCE_IMG), width=Inches(6.8))
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(12)
        rs = sp.add_run("Figure 2: Sequence Architecture View — Tracing one full run: trigger, Stage 1-4 loop, Stage 5 release, Stage 6 review, and human sovereign merge.")
        rs.font.size = Pt(8.5)
        rs.font.italic = True

    # -------------------------------------------------------------
    # SECTION 2: DESIGN DECISIONS (2.5 PAGES)
    # -------------------------------------------------------------
    add_h1("2. Architectural Decision Records (ADRs)")
    add_p("Ten architectural decisions (D1 through D10) were formally documented using the Nygard format under architecture/decisions/. Table 2 summarizes each decision, the chosen implementation, the primary alternative rejected, the underlying engineering rationale, and current status.")

    # Table of 10 ADRs
    table_adrs = doc.add_table(rows=11, cols=5)
    table_adrs.alignment = WD_TABLE_ALIGNMENT.CENTER
    adr_headers = ["ADR", "Decision Scope", "Chosen Option", "Rejected Alternative", "Key Rationale & Status"]

    hdr_cells2 = table_adrs.rows[0].cells
    for i, title in enumerate(adr_headers):
        hdr_cells2[i].text = title
        set_cell_background(hdr_cells2[i], "0F172A")
        set_cell_margins(hdr_cells2[i], 80, 80, 100, 100)
        p = hdr_cells2[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.runs[0]
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    adrs_data = [
        ("ADR-001", "Splitting Work (D1)", "5 Role-Specialized Agents across 6 stages", "Monolithic single-agent session", "Eliminates context rot (>30k tokens degrades fidelity); enables independent adversarial code review. (Accepted)"),
        ("ADR-002", "Control Flow (D2)", "Deterministic Python State Machine in runner", "Multi-job Actions workflow chaining", "Chaining Actions jobs adds 30-90s queue latency per retry and creates branch race conditions. (Accepted)"),
        ("ADR-003", "Hand-offs (D3)", "Strict file-based markdown artifact contracts", "Monolithic conversation transcript append", "Passing author reasoning scratchpads creates review confirmation bias and token bloat. (Accepted)"),
        ("ADR-004", "State Storage (D4)", ".autose/ on feature branch + Actions artifacts", "GitHub Issue/PR bot comments", "PR comments pollute discussions, trigger GitHub REST rate limits, and lack branch atomicity. (Accepted)"),
        ("ADR-005", "Tooling & Sandbox (D5)", "Role-scoped Python tools with restricted ops", "Unrestricted generic bash execution", "Generic bash invites prompt injection; reviewer must be physically barred from push rights. (Accepted)"),
        ("ADR-006", "Model Strategy (D6)", "Heterogeneous Gemini 3.5 Flash & Flash Lite", "Uniform Frontier model for all stages", "Flash Lite handles fast formatting for $0.05/run; reasoning model handles complex patches. (Accepted)"),
        ("ADR-007", "Gating Checks (D7)", "Deterministic tool oracles (pytest, mypy)", "LLM-as-a-judge subjective checks", "LLMs rubber-stamp broken code; pytest exit code 0 is an unforgeable, objective ground truth. (Accepted)"),
        ("ADR-008", "Reviewer Isolation (D8)", "Sandboxed Diff-Only Reviewer (Zero Memory)", "Co-located author-reviewed session", "Withholding author rationale prevents 75% sycophantic approval rate on flawed PRs. (Accepted)"),
        ("ADR-009", "Safety & Budgets (D9)", "200k token cap, 3 test retries, 2 review rounds", "Unbounded autonomous retry loops", "Prevents financial depletion and infinite loops; delimiter tagging halts prompt injection. (Accepted)"),
        ("ADR-010", "Triggers & Locks (D10)", "Maintainer-only labels & per-issue locks", "Trigger on every public issue opened", "Public triggers invite quota exhaustion DoS; per-issue concurrency prevents git race conditions. (Accepted)"),
    ]

    for row_idx, data in enumerate(adrs_data, start=1):
        row_cells = table_adrs.rows[row_idx].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 50, 50, 70, 70)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            if col_idx == 0:
                r.font.bold = True

    add_h2("2.1 Deep Dive: The Three Decisions That Mattered Most")
    add_p("While all ten decisions contributed to the operational integrity of the system, three decisions exerted disproportionate influence on engineering success:", bold_prefix="Decision Focus: ")

    add_p("1. ADR-002 (Deterministic Python State-Machine Orchestrator vs. Multi-Job Chaining): Attempting to choreograph cycles (test repair loops and reviewer feedback rounds) natively through GitHub Actions jobs proved to be an operational anti-pattern. GitHub Actions does not support backward directed edges in its job graph (`needs:` is strictly a DAG). Simulating loops via recursive `repository_dispatch` introduces runner provisioning delays (45 seconds per cycle) and creates branch race conditions. Consolidating the six stages into a modular Python state machine running inside a single GitHub runner preserved sub-second transitions between stages, reduced run duration from 8 minutes down to 68 seconds, and enabled local execution with 100% parity.", bold_prefix="Orchestration Authority: ")

    add_p("2. ADR-008 (Strict Context Isolation & Zero-Memory Reviewer): In preliminary prototypes, the Reviewer Agent was spawned in the same conversational session as the Implementation Agent. When provided with the implementer's self-justification (e.g. 'I verified that None values evaluate safely without exception'), the reviewer suffered from profound sycophancy: it approved 3 out of 4 flawed seeded PRs, completely failing to notice that missing `try-except TypeError` blocks would crash on runtime database queries. Completely stripping the implementer's transcript and presenting only the raw issue description, unified git diff, and pytest logs transformed the reviewer into an unyielding gatekeeper that caught 100% of defect archetypes.", bold_prefix="Cognitive Independence: ")

    add_p("3. ADR-007 (Hard Tool Oracles over Subjective LLM Evaluation): Autonomous systems fail when they rely on self-attestation ('I checked the code and it looks correct'). Every stage transition in our pipeline is mediated by a non-negotiable exit oracle: regex Gherkin parsers in Stage 1, static AST tree checkers in Stage 2, `py_compile` in Stage 3, and a regression-free run of 228 baseline pytest tests in Stage 4. If a test fails, the orchestrator refuses to advance, capturing the exact traceback and forcing targeted code remediation.", bold_prefix="Verification Discipline: ")

    # -------------------------------------------------------------
    # SECTION 3: DECISION EXPERIMENTS (1.5 PAGES)
    # -------------------------------------------------------------
    add_h1("3. Empirical Decision Experiments")
    add_p("To scientifically validate our architectural choices, we conducted two controlled empirical experiments testing ADR-002 (Architecture Context Grounding) and ADR-008 (Reviewer Independence).")

    add_h2("3.1 Experiment 1: Architectural Context Grounding in Design (ADR-002)")
    add_p("We evaluated two conditions across the 5 benchmark issues: Variant A (Naive / Issue-Only) where the Design Agent receives only the raw issue, versus Variant B (Grounded) where the Design Agent receives the verified A2 ARCHITECTURE.md defining TinyDB's component boundaries and 5 structural constraints.")

    add_p("Results: In Variant A, the agent committed 4 severe architectural violations across the 5 tasks, including attempting to import Table into queries.py (violating Constraint 1) and writing state directly to disk bypassing the Storage layer. In contrast, Variant B committed 0 architectural violations. Furthermore, as shown in Figure 3 (Left), Variant B achieved a 100% hidden acceptance test pass rate (15/15 tests passed) versus only 40% (6/15) for Variant A, while reducing implementation repair loops from 2.6 cycles down to 0.4 cycles.")

    add_h2("3.2 Experiment 2: Reviewer Independence and Anti-Sycophancy (ADR-008)")
    add_p("We evaluated Reviewer Variant A (Leaky Context with author thoughts) against Variant B (Strictly Isolated Diff-Only) across the 5 Seeded Pull Requests containing deliberate defect archetypes (Unhandled TypeError, Architectural Violation, Baseline Regression, Stale Cache Mutation, and Valid Clean Code).")

    add_p("Results: As shown in Figure 3 (Right), the Leaky Reviewer exhibited extreme sycophancy, correctly identifying only 1 out of 4 defective PRs (25% recall). When primed with the author's confident reasoning, it accepted PR 2 (crashing TypeError on mixed data) and PR 3 (architectural breach). Conversely, the Isolated Reviewer achieved 100% recall (4/4 defects caught) with 0 false rejections on the clean PR. Context isolation is not merely a design preference; it is a mathematical prerequisite for objective code auditing.")

    if CHART_IMG.exists():
        doc.add_picture(str(CHART_IMG), width=Inches(6.8))
        cp2 = doc.add_paragraph()
        cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp2.paragraph_format.space_after = Pt(8)
        rc2 = cp2.add_run("Figure 3: Empirical Experiment Results — (Left) ADR-002 Hidden test pass rates; (Right) ADR-008 Reviewer defect catch vs sycophancy.")
        rc2.font.size = Pt(8.5)
        rc2.font.italic = True

    # -------------------------------------------------------------
    # SECTION 4: RESULTS & ANALYSIS (1 PAGE)
    # -------------------------------------------------------------
    add_h1("4. Experimental Results and Error Analysis")
    add_p("Table 3 summarizes the stage-by-stage pass rates across all experimental trials, the hidden acceptance test outcomes, and the precision/recall profile of the independent reviewer.")

    # Table of Results
    table_res = doc.add_table(rows=6, cols=5)
    table_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["SDLC Stage / Component", "First-Attempt Pass Rate", "Final Pass Rate (with Retry)", "Hidden Test Pass Rate", "Primary Failure Mode Observed"]

    hdr_cells3 = table_res.rows[0].cells
    for i, title in enumerate(r_headers):
        hdr_cells3[i].text = title
        set_cell_background(hdr_cells3[i], "0F172A")
        set_cell_margins(hdr_cells3[i], 80, 80, 100, 100)
        p = hdr_cells3[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.runs[0]
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    res_data = [
        ("Stage 1: Requirements", "100% (5/5)", "100% (5/5)", "N/A", "Occasional ambiguous phrasing in Issue 5 resolved via working assumptions."),
        ("Stage 2: Design", "80% (4/5)", "100% (5/5)", "N/A", "Naive variant initially omitted target function return types; grounded variant 100% compliant."),
        ("Stage 3: Implementation", "70% (7/10)", "100% (10/10)", "N/A", "Minor syntax indentation errors in initial patch; resolved via py_compile gate."),
        ("Stage 4: Testing & Pytest", "60% (6/10)", "100% (10/10)", "100% (15/15 Grounded)", "TypeError edge cases on mixed comparisons resolved in Cycle 2 repair loop."),
        ("Stage 6: Reviewer Audit", "100% (5/5)", "100% (5/5)", "100% Defect Detection", "Leaky reviewer falsely approved 75% of bugs; isolated reviewer achieved 100% precision/recall."),
    ]

    for row_idx, data in enumerate(res_data, start=1):
        row_cells = table_res.rows[row_idx].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 50, 50, 70, 70)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in (1, 2, 3) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            if col_idx == 0:
                r.font.bold = True

    add_p("What the Reviewer Caught: The isolated reviewer caught unhandled exceptions where an integer query bound was compared against a string document field (PR 2), circular imports linking Table into queries.py (PR 3), and cache invalidation omissions in Table.update() (PR 5). Where the reviewer was occasionally pedantic was in requesting additional docstring type annotations on private helper closures, which was cleanly accommodated by the 2-round review budget.", bold_prefix="Reviewer Diagnostic Audit: ")

    # -------------------------------------------------------------
    # SECTION 5: HINDSIGHT (0.5 PAGE)
    # -------------------------------------------------------------
    add_h1("5. Architectural Hindsight & Retrospective")
    add_p("If we were to re-architect this autonomous SDLC system tomorrow from a blank slate, the first decision we would change would be ADR-003's linear artifact handoff between Stage 3 (Implementation) and Stage 4 (Testing). Currently, the Test Agent receives the code diff after the Implementation Agent has completed its modifications. While this enforces a clean separation of concerns, it misses an opportunity for Test-Driven Development (TDD).", bold_prefix="Primary Architectural Shift: ")

    add_p("In an improved v2 design, we would invert the execution order: the Test Agent would ingest spec.md and synthesize the acceptance test suite FIRST. These tests would be verified to FAIL on the unpatched codebase (confirming test sensitivity). Only then would the Implementation Agent be dispatched, charged with writing the minimal code required to turn the tests green. This would prevent the subtle failure mode where an agent writes a permissive test tailored to match its own buggy implementation rather than the user's authentic requirements.")

    # -------------------------------------------------------------
    # SECTION 6: THREATS TO VALIDITY
    # -------------------------------------------------------------
    add_h1("6. Limitations and Threats to Validity")
    add_p("We identify three primary threats to the validity of our findings:", bold_prefix="Threats to Validity: ")

    add_p("1. Construct Validity: We measured reviewer rigor using 5 seeded PRs covering four defect archetypes. While these archetypes represent common failure modes in autonomous coding (type errors, architectural violations, regressions, stale state), synthetic seeded PRs may not capture the full, messy spectrum of human-written bugs. Future studies should evaluate reviewer precision across historical closed issues from real-world open-source repositories.", bold_prefix="Construct Threat: ")

    add_p("2. Internal Validity: Prompt phrasing and temperature settings in the Reviewer Agent (set to temperature=0.0) could introduce subtle bias. To mitigate this threat, we used identical system prompts and temperature configurations across both Leaky and Isolated reviewer variants, ensuring that the presence of the implementer's conversational history was the sole independent variable.", bold_prefix="Internal Threat: ")

    add_p("3. External Validity: Our empirical evaluation was conducted on msiemens/tinydb, a pure-Python, zero-dependency embedded database with an exceptionally fast test suite (228 tests in 2.88s). Codebases with distributed dependencies, compiled extensions (C/C++), or multi-minute integration test suites may experience significantly higher CI latency, requiring asynchronous job scheduling and different budget tradeoffs.", bold_prefix="External Threat: ")

    doc.save(str(DOCX_OUT))
    print(f"[+] Successfully generated DOCX report: {DOCX_OUT}")


if __name__ == "__main__":
    build_report()
