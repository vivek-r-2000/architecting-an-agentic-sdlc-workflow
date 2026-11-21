# SDLC Workflow Stage Map & Boundary Matrix

This document defines the 6 discrete stages of the Autonomous Software Engineering (AutoSE) SDLC workflow, their respective agent roles, inputs, outputs, verification checks, and feedback transition rules.

---

## 1. Stage Definitions & Hand-off Matrix

| # | Stage | Responsible Agent | Primary Inputs | Delivered Artifact | Mandatory Exit Check | Failure / Feedback Transition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Requirements Engineering** | `RequirementsAgent` (Gemini 2.5 Flash) | User issue title, body, labels, issue author metadata | `spec.md` | All Acceptance Criteria (ACs) follow Gherkin syntax (`Given/When/Then`) and are programmatically testable. | If underspecified or contradictory, record in `Uncertainty Register` within `spec.md` with explicit working assumptions. Run aborts if core intent cannot be triangulated. |
| **2** | **Architectural Design** | `DesignAgent` (Gemini 2.5 Flash) | `spec.md`, `ARCHITECTURE.md`, repository file tree, symbol index | `design.md` | Explicit enumeration of target files, classes, methods to modify, and contract invariants. Must comply with TinyDB constraints. | If design requires violating `ARCHITECTURE.md` constraints, revise plan or fail with explicit architectural violation notice. |
| **3** | **Implementation** | `ImplementationAgent` (Gemini 2.5 Flash) | `design.md`, codebase source files, git branch `autose/issue-<id>` | `diff.patch` | Code passes syntax check (`py_compile`), static typing check (`mypy`), and packaging build (`uv pip check`). | Retry patch generation within budget (max 3 attempts). If syntax fails repeatedly, abort stage. |
| **4** | **Testing & Verification** | `TestAgent` (Gemini 2.5 Flash) | `spec.md`, `design.md`, working tree with `diff.patch` applied | `test_report.md` | 100% of baseline tests pass (228/228 regression-free) AND 100% of newly authored acceptance tests pass. | If tests fail, route error traceback and failing assertion back to **Stage 3 (Implementation)** for targeted remediation (max 3 retry cycles). |
| **5** | **Release & PR Management** | `ReleaseAgent` (GitHub Actions runner / `gh` CLI) | Feature branch, `spec.md`, `design.md`, `test_report.md` | `pr.md`, Git commit, Pull Request URL | Feature branch pushed cleanly; PR created with structured changelog; GitHub CI workflow triggered and green. | If git push or PR creation fails (network or permissions), retry with exponential backoff (max 3 retries). |
| **6** | **Independent Review** | `ReviewerAgent` (Gemini 2.5 Pro - Adversarial) | Issue title/body, git diff (`origin/main...HEAD`), repository source code (read-only), pytest results. *(Zero implementer memory)* | `review.md` | Verdict must be one of: `APPROVE`, `REQUEST_CHANGES: CODE_ISSUE`, or `REQUEST_CHANGES: APPROACH_ISSUE`. | If `CODE_ISSUE`, route diff and review feedback to **Stage 3**; if `APPROACH_ISSUE`, route back to **Stage 2** (max 2 review rounds). If budget exhausted or approved, hand over to Human Maintainer. |
| **--** | **Human Decision** | Maintainer (Human) | Pull request, full artifact bundle (`spec.md`, `design.md`, `test_report.md`, `review.md`) | Merge / Close PR | Human review and merge authorization. | Workflow never merges autonomously. Human maintainer retains sovereign decision authority. |

---

## 2. Information Boundaries & Least-Privilege Access

```
                    ┌────────────────────────────┐
                    │ Issue: Labeled or Comment  │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │  1. Requirements Agent     │ ◄─── A1 requirements-engineer skill
                    └─────────────┬──────────────┘
                                  │ spec.md
                                  ▼
                    ┌────────────────────────────┐
                    │  2. Design Agent           │ ◄─── A2 ARCHITECTURE.md
                    └─────────────┬──────────────┘
                                  │ design.md
                                  ▼
            ┌─────────► ┌────────────────────────────┐
            │           │  3. Implementation Agent   │ ◄─── Edit tool / Write tool
            │           └─────────────┬──────────────┘
            │                         │ diff.patch
            │                         ▼
            │ Retry     ┌────────────────────────────┐
            │ (max 3)   │  4. Testing Agent          │ ◄─── Baseline + New Pytest
            └───────────┤                            ├──────┐
              Failures  └─────────────┬──────────────┘      │
                                      │ All Pass            │
                                      ▼                     │
                        ┌────────────────────────────┐      │
                        │  5. Release Agent          │      │
                        └─────────────┬──────────────┘      │
                                      │ PR URL              │
                                      ▼                     │
            Code Issue  ┌────────────────────────────┐      │
        ┌───────────────┤  6. Independent Reviewer   │ ◄────┘ Diff & repo only
        │ (max 2)       │     (Gemini 2.5 Pro)       │        (Zero reasoning leak)
        │               └──────┬───────────────┬─────┘
        │                      │               │
        │                      │ Approach Issue│ (max 2)
        │                      │               ▼
        │                      │         ┌───────────┐
        │                      │         │  Stage 2  │
        │                      │         └───────────┘
        │                      ▼ Approve or Rounds Exhausted
        │               ┌────────────────────────────┐
        └──────────────►│   Human Maintainer Gate    │
                        │      (Merge or Close)      │
                        └────────────────────────────┘
```

---

## 3. Feedback Loop Guardrails

1. **Test Failure Loop (Stage 4 -> Stage 3):**
   - Maximum retries: `3`.
   - Payload returned to Stage 3: Only the specific pytest failure traceback, line numbers, and assertion failure. No unconstrained re-prompting.
   - Termination: If tests still fail after attempt 3, the workflow marks `test_report.md` as `FAILED`, stops execution, and posts a failure comment on the issue.

2. **Reviewer Change Request Loop (Stage 6 -> Stage 3 or Stage 2):**
   - Maximum rounds: `2`.
   - Classification:
     - `CODE_ISSUE`: Syntax bug, off-by-one, missing edge-case validation, unhandled exception -> Routes to Stage 3.
     - `APPROACH_ISSUE`: Architectural constraint violation, incorrect module placement, improper abstraction -> Routes to Stage 2.
   - Termination: If after round 2 the reviewer still requests changes, the workflow transitions to terminal state, leaves detailed findings in `review.md`, and requests human intervention.
