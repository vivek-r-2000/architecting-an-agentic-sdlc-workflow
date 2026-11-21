# ADR-002: Workflow Control Flow and State-Machine Orchestration

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
The workflow must transition through six sequential stages, but realistic software engineering is inherently non-linear:
- If newly synthesized tests fail in Stage 4, the workflow must loop back to Stage 3 (Implementation) to repair the code.
- If the Reviewer in Stage 6 detects a flaw, it must classify the problem and route execution either back to Stage 3 (for code-level bugs) or back to Stage 2 (for architectural approach failures).
- The system must avoid infinite looping, deadlock, and runaway GitHub Actions runner consumption.

We need to decide whether to control flow via native GitHub Actions job dependencies (`needs:` / `workflow_dispatch`), an external framework (e.g., LangGraph), or a centralized deterministic Python state machine running inside a runner job.

## Decision
We implement a **Deterministic Python State-Machine Orchestrator (`autose_workflow.orchestrator`)** hosted inside a single GitHub Actions runner job.

1. **State Machine Transitions:**
   - Formal states: `INIT`, `REQUIREMENTS`, `DESIGN`, `IMPLEMENTATION`, `TESTING`, `RELEASE`, `REVIEW`, `TERMINATED_SUCCESS`, `TERMINATED_FAILURE`.
   - Transitions are governed by strict exit checks (Gating Assertions).
2. **Bounded Feedback Loops:**
   - **Test Remediation Loop (Testing -> Implementation):** Maximum budget of **3 retry cycles**. The payload passed back consists solely of the failing test name, assertion error message, and traceback.
   - **Review Remediation Loop (Review -> Implementation or Design):** Maximum budget of **2 review rounds**.
     - `CODE_ISSUE`: Transitions to `IMPLEMENTATION` with targeted diff critique.
     - `APPROACH_ISSUE`: Transitions to `DESIGN` with architectural rejection rationale.
3. **Loop Decision Authority:**
   - The Orchestrator acts as the sole transition arbiter. Individual agents emit structured verdicts (`dict` with `status: PASS | FAIL | REQUEST_CHANGES`), but the state machine enforces cycle decrementing, timeout monitoring, and abort conditions.

## Alternatives Considered
* **Alternative 1: Multi-Job GitHub Actions Chaining (`needs:` & Artifacts).** Separate GitHub Actions jobs per stage.
  * *Rejection Rationale:* GitHub Actions does not natively support backward cycles or while-loops between jobs. Implementing loops requires triggering new workflow runs via `repository_dispatch` or recursive repository dispatches, introducing 30-90 second runner queue delays per cycle, flaky concurrency token race conditions, and poor local debuggability.
* **Alternative 2: Autonomous LLM Orchestrator (ReAct Planning Agent).** Letting an LLM decide which tool/stage to call dynamically on every step.
  * *Rejection Rationale:* LLM planners frequently hallucinate skipped stages, loop infinitely without recognizing budget depletion, or prematurely claim completion. Deterministic Python state machines guarantee that every stage is visited in exact required order.

## Consequences
* **Positive:**
  * Exact deterministic execution: Stages 1 through 6 run in guaranteed order with strict cycle limits.
  * Fast local reproducibility: The entire orchestration can be executed, debugged, and unit-tested locally without waiting for GitHub Actions runner queues.
  * Bounded costs: Hard-coded maximum loop counts (max 3 test retries, max 2 review cycles) eliminate token explosion.
* **Negative:**
  * GitHub Actions job log appears as a single linear console output rather than multiple distinct job tiles in the GitHub Actions UI. (Mitigated by emitting GitHub Actions step groups `::group::` / `::endgroup::`).
