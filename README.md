# AutoSE Assignment 3: Architecting an Agentic SDLC Workflow

**Author:** Vivek R (Roll Number: `2019112020`)  
**Course:** CS6.403 Autonomous Software Engineering (Monsoon 2026), IIIT Hyderabad  
**Instructor:** Prof. Karthik Vaidhyanathan  
**Repository URL:** `https://github.com/vivek-r-2000/architecting-an-agentic-sdlc-workflow`  
**Base Repository:** [msiemens/tinydb](https://github.com/msiemens/tinydb) pinned at commit [`edff96aeb2616402e9489d46e90a592c05565621`](https://github.com/msiemens/tinydb/tree/edff96aeb2616402e9489d46e90a592c05565621)  
**Baseline Test Suite:** 228 passed in 2.88s  

---

## 1. System Overview

This repository contains the complete implementation, architectural documentation, decision records (ADRs), empirical experiments, and research report for an autonomous Software Development Life Cycle (SDLC) multi-agent workflow hosted on GitHub Actions.

A human maintainer triggers the autonomous pipeline simply by adding the label `autose` to any issue or posting a `/autose` comment. From there, five specialized agents transition the issue through six formal, gated stages:
1. **Stage 1 (Requirements):** `RequirementsAgent` synthesizes formal Gherkin acceptance criteria into `spec.md` (reusing A1 methodology).
2. **Stage 2 (Design):** `DesignAgent` grounds the specification in `ARCHITECTURE.md` and generates `design.md` detailing target files and function signatures.
3. **Stage 3 (Implementation):** `ImplementationAgent` edits code on branch `autose/issue-<id>`, verified to pass python syntax compilation (`py_compile`).
4. **Stage 4 (Testing):** `TestAgent` authors executable pytest test cases and runs baseline + new test suites; failing tests trigger an automated repair loop (max 3 retries).
5. **Stage 5 (Release):** `ReleaseAgent` commits, pushes the branch, and opens a Pull Request with structured changelogs.
6. **Stage 6 (Independent Review):** `ReviewerAgent` audits the PR inside an isolated context sandbox (zero implementer memory, no push rights) and emits a typed verdict: `APPROVE`, `REQUEST_CHANGES: CODE_ISSUE` (routes to Stage 3), or `REQUEST_CHANGES: APPROACH_ISSUE` (routes to Stage 2), capped at 2 review rounds.

The final merge decision is strictly reserved for the human maintainer.

---

## 2. Directory Structure

```text
2019112020_AutoSE_A3/
├── README.md                          # Repository metadata, setup, and reproduction guide
├── report.pdf                         # Final 6-page academic research report (strictly <= 8 pages)
├── report.docx                        # Source Word document compiled via Word COM
├── demo_walkthrough.md                # Video walkthrough script and trace demonstration
├── roll_number_a3_AutoSE.txt          # Submission file containing repository URL
├── GATES.md                           # Unlazy 10-module verification gates ledger
├── ARCHITECTURE.md                    # TinyDB Architecture Document (3 ADRs, 5 Constraints)
├── architecture/
│   ├── ARCHITECTURE.md
│   ├── views/
│   │   ├── component_view.svg         # Component Architecture Diagram
│   │   ├── component_view.png         # High-resolution rasterized diagram
│   │   ├── sequence_view.svg          # Sequence Architecture Diagram
│   │   ├── sequence_view.png          # High-resolution rasterized diagram
│   │   └── stage_map.md               # 6-Stage Mapping and Hand-off Matrix
│   └── decisions/                     # 10 Nygard Architectural Decision Records
│       ├── ADR-001-splitting-the-work.md
│       ├── ADR-002-control-flow-and-orchestration.md
│       ├── ADR-003-hand-offs-and-information-boundaries.md
│       ├── ADR-004-state-management-and-artifacts.md
│       ├── ADR-005-tools-and-least-privilege-capabilities.md
│       ├── ADR-006-model-selection-and-heterogeneity.md
│       ├── ADR-007-verification-and-quality-checks.md
│       ├── ADR-008-reviewer-independence-and-anti-sycophancy.md
│       ├── ADR-009-safety-budgets-and-prompt-injection-defense.md
│       └── ADR-010-triggers-concurrency-and-rate-limiting.md
├── workflow/
│   ├── .github/workflows/autose.yml   # Mirrored GitHub Actions workflow
│   ├── autose_workflow/
│   │   ├── __init__.py
│   │   ├── config.py                  # Budgets, timeouts, models, paths
│   │   ├── llm_client.py              # Gemini client with IPv4 socket routing & budget tracking
│   │   ├── stage_requirements.py      # Stage 1 Requirements Agent
│   │   ├── stage_design.py            # Stage 2 Design Agent
│   │   ├── stage_implement.py         # Stage 3 Implementation Agent
│   │   ├── stage_test.py              # Stage 4 Testing Agent
│   │   ├── stage_release.py           # Stage 5 Release Agent
│   │   ├── stage_review.py            # Stage 6 Independent Reviewer Agent
│   │   └── orchestrator.py            # State-Machine Orchestrator Engine
│   └── tests/
│       └── test_workflow_engine.py    # Unit test suite for verification gates
├── experiment/
│   ├── variants.md                    # Detailed specification of ADR-002 & ADR-008 experiments
│   ├── run_experiments.py             # Unified empirical experiment execution runner
│   ├── issues/                        # The 5 Benchmark Issues
│   │   ├── issue_1_bug_regex_match_nonstring.md
│   │   ├── issue_2_bug_upsert_keyerror.md
│   │   ├── issue_3_feature_query_any_all_lists.md
│   │   ├── issue_4_feature_query_between.md
│   │   └── issue_5_vague_speed_up_lookups.md
│   ├── hidden_tests/                  # 15 Hidden Acceptance Tests (3 per issue)
│   │   ├── test_issue_1_hidden.py
│   │   ├── test_issue_2_hidden.py
│   │   ├── test_issue_3_hidden.py
│   │   ├── test_issue_4_hidden.py
│   │   └── test_issue_5_hidden.py
│   └── seeded_prs/                    # 5 Seeded PRs evaluating Reviewer Rigor
│       ├── pr_1_valid_clean_feature.patch
│       ├── pr_2_subtle_type_error.patch
│       ├── pr_3_architectural_violation.patch
│       ├── pr_4_baseline_regression.patch
│       └── pr_5_incomplete_caching.patch
└── results/
    ├── results.csv                    # Complete empirical quantitative metric table
    ├── runs.md                        # Execution log manifest and trial links
    └── experiment_charts.png          # Publication-grade comparative visualization plots
```

---

## 3. How to Run & Reproduce

### Prerequisites
- Python 3.12+
- `uv` package manager (`pip install uv` or standalone installer)
- Git

### 1. Verify Baseline Tests (Must pass 228/228 tests)
```bash
uv run pytest tests/
```

### 2. Verify Workflow Engine Unit Tests
```bash
uv run pytest workflow/tests/ -v --no-cov
```

### 3. Run End-to-End Orchestrator on an Issue
```bash
uv run python -m autose_workflow.orchestrator --issue-id 42 --issue-file experiment/issues/issue_4_feature_query_between.md
```

### 4. Reproduce Empirical Experiments (ADR-002 & ADR-008)
```bash
uv run python experiment/run_experiments.py
```

### 5. Re-compile Research Report PDF
```bash
uv run python generate_report.py
uv run python compile_pdf.py
```

---

## 4. Models & API Configuration

- **Models:**
  - Pipeline Execution (Requirements, Testing): `gemini-3.5-flash-lite`
  - Design & Code Synthesis: `gemini-3.5-flash`
  - Adversarial Reviewer: `gemini-3.5-flash` (Greedy decoding, temperature=0.0, adversarial prompt) / `gemini-3.8-flash`
- **Secrets:** Configure `GEMINI_API_KEY` in GitHub Repository Secrets.

---

## 5. Course AI Use Disclosure

In accordance with course academic honesty guidelines:
- Antigravity AI Coding Agent was utilized for scaffolding generation, exploratory testing, and diagram drafting.
- All 10 Architectural Decision Records (ADRs), component designs, empirical hypotheses, and analytical reasoning were conceptualized, directed, authored, and verified by the student.
