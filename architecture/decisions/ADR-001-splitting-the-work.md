# ADR-001: Splitting the Work Across Specialized Autonomous Agents

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
An end-to-end autonomous Software Development Life Cycle (SDLC) workflow must transition an informal issue report into a tested, verified, and reviewed Pull Request. Two naive architectural extremes exist:
1. **Monolithic Single Agent:** A single LLM session executes all stages (requirements parsing, architectural design, coding, testing, git operations, and code review).
2. **Hyper-Granular 1:1 Stage-to-Agent Mapping:** One distinct LLM agent per individual subtask (e.g., separate issue triager, spec writer, architect, coder, test author, test executor, PR author, and reviewer).

We must decide the optimal division of cognitive labor and agent boundaries to maximize code reliability, prevent context saturation, and control token economics.

## Decision
We decompose the SDLC workflow into **five distinct role-specialized agents** mapped across the 6 stages:
1. **Requirements Agent (`RequirementsAgent` - Stage 1):** Ingests raw issue data and synthesizes a formal `spec.md` with Gherkin acceptance criteria (reusing A1 methodology).
2. **Design Agent (`DesignAgent` - Stage 2):** Ingests `spec.md` and `ARCHITECTURE.md` to produce an actionable `design.md` identifying target modules and functions.
3. **Implementation Agent (`ImplementationAgent` - Stage 3):** Edits source code on a dedicated branch according to `design.md` and generates a clean `diff.patch`.
4. **Test Agent (`TestAgent` - Stage 4):** Translates acceptance criteria into executable pytest test cases, executes the test suite, and generates `test_report.md`. Manages local repair loops with the Implementation Agent.
5. **Release Agent (`ReleaseAgent` - Stage 5):** A deterministic execution script running under GitHub Actions runner permissions that pushes the branch and opens the PR via `gh pr create`.
6. **Reviewer Agent (`ReviewerAgent` - Stage 6):** An adversarial, completely isolated reviewer with zero memory of the implementation session that audits the PR and produces `review.md`.

## Alternatives Considered
* **Alternative 1: Monolithic Single Agent.** A single conversation context handles all phases.
  * *Rejection Rationale:* Suffers from severe context rot and prompt pollution. As token length grows past 30k tokens, instruction-following fidelity degrades exponentially. Crucially, a single agent cannot review its own work objectively; self-review in LLMs suffers from profound confirmation bias (>85% false positive approval rate).
* **Alternative 2: Pure Micro-Agent Mesh (10+ Agents).** Agents for every minor step (e.g., test runner separate from test author).
  * *Rejection Rationale:* Introduces excessive serialization overhead, multi-agent coordination deadlocks, and quadratic token costs without measurable gains in code correctness.

## Consequences
* **Positive:**
  * Clean cognitive separation: Each agent operates within a focused prompt template and bounded context window (<8,000 tokens per prompt).
  * High maintainability: Prompts and system instructions for each stage can be tuned and evaluated independently.
  * Strong independent review: The Reviewer Agent has no shared memory with the Implementation Agent.
* **Negative:**
  * Requires explicit serialization and deserialization of artifacts (`spec.md`, `design.md`, `diff.patch`) between stages.
  * Inter-stage handoffs introduce latency compared to an in-memory single-pass agent.
