# ADR-007: Verification Strategy and Stage Gating Checks

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
A critical failure mode of agentic coding systems is "silent hallucinated progress" — an agent asserting that code is complete, correct, and tested when in reality it fails to build, introduces breaking regressions, or does not satisfy requirements. To prevent cascading failures, each of the six stages must be guarded by an objective, testable exit check before handing over to the subsequent stage.

We must decide the mechanism and authority responsible for conducting and evaluating each stage's gating check.

## Decision
We implement **Deterministic Hybrid Gating: Hard Tool Oracles Over Subjective LLM Judgments**:

Every stage is guarded by an explicit programmatic check enforced by the orchestrator:

| Stage | Artifact | Gating Check Type | Exact Oracle Command / Verification Routine |
| :--- | :--- | :--- | :--- |
| **1. Requirements** | `spec.md` | Static Schema & Testability | Regex / AST validator checks presence of `[AC-1]`, `[AC-2]` tags, standard Gherkin clauses (`Given/When/Then`), and absence of unresolved `[BLOCKED]` flags. |
| **2. Design** | `design.md` | Concrete Target Verification | Parser extracts referenced file paths and function names, verifying that target files exist in the repository tree and adhere to TinyDB architectural boundaries. |
| **3. Implementation** | `diff.patch` | Build & Static Typing | `python -m py_compile tinydb/*.py` (Zero syntax errors) AND `mypy tinydb/` (Static typing check). |
| **4. Testing** | `test_report.md` | Test Suite Execution | `pytest tests/` (100% of 228 baseline tests pass, 0 regressions) AND `pytest .autose/test_acceptance.py` (100% of newly authored acceptance tests pass). |
| **5. Release** | `pr.md` + PR URL | GitHub API / CI Status | `gh pr view <pr_id> --json state,statusCheckRollup` confirms PR is open and CI workflow is green. |
| **6. Review** | `review.md` | Structured Adversarial Audit | JSON schema validation on Reviewer verdict (`APPROVE` or `REQUEST_CHANGES` with valid routing category). |

**Authority:** The final pass/fail decision at every stage is made by **deterministic Python code (oracles)**, never by the authoring agent's subjective declaration.

## Alternatives Considered
* **Alternative 1: LLM-as-a-Judge for All Stage Checks.** Asking an LLM prompt: "Did Stage 3 pass its check? Answer Yes or No."
  * *Rejection Rationale:* LLMs are notorious for rubber-stamping broken code, missing subtle runtime errors, and hallucinating test outcomes. A real test execution process (`pytest`) that exits code 0 or 1 is an unforgeable ground truth.
* **Alternative 2: Deferring All Testing to GitHub CI (Stage 5 Only).** Letting Stage 3 push directly and waiting for GitHub Actions CI to report failures.
  * *Rejection Rationale:* Extremely slow (adds 2-4 minutes per attempt) and consumes GitHub Actions runner concurrency. Local pre-push testing in Stage 4 allows rapid 3-second self-correction loops.

## Consequences
* **Positive:**
  * Zero tolerance for broken code: Broken syntax, failing unit tests, or regressed baseline tests cannot pass to Stage 5.
  * Rapid feedback: Pytest runs in ~2.8 seconds locally, enabling instantaneous repair loops in Stage 4.
  * Objective audit trail: Every gate's output is saved verbatim in `.autose/`.
* **Negative:**
  * Tests that require external services or mocking can be challenging for agents to synthesize without comprehensive mocking utilities.
