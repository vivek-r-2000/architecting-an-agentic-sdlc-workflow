# ADR-003: Hand-offs, Artifact Contracts, and Information Boundaries

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
In a multi-agent system, unconstrained information sharing causes context bloat, prompt degradation, and cognitive cross-contamination. If an agent receives an earlier agent's stream-of-consciousness reasoning, it tends to adopt the earlier agent's assumptions and overlook edge cases. Conversely, insufficient context leads to hallucinations and structural defects.

We must decide the exact contract, format, and boundaries of data passed between consecutive stages.

## Decision
We enforce **Strict File-Based Artifact Contracts with Deliberate Information Omission**:

1. **Stage 1 -> Stage 2 (Requirements to Design):**
   - *Transferred:* `spec.md` containing parsed user intent, scope, and Gherkin acceptance criteria (`Given/When/Then`).
   - *Omitted:* Raw user issue comments, author profile details, and sentiment tokens.
2. **Stage 2 -> Stage 3 (Design to Implementation):**
   - *Transferred:* `design.md` detailing exact target files, modified function signatures, data flow invariants, and architectural constraints.
   - *Omitted:* Intermediate alternative architectures considered and discarded by the Design Agent.
3. **Stage 3 -> Stage 4 (Implementation to Testing):**
   - *Transferred:* `diff.patch` applied to the working repository, plus `spec.md` (so the Test Agent knows what acceptance criteria must be tested).
   - *Omitted:* The Implementation Agent's internal prompt history, conversational back-and-forth, and temporary scratchpad edits.
4. **Stage 4 -> Stage 5 (Testing to Release):**
   - *Transferred:* Git commit on the feature branch, `test_report.md` proving 100% test pass rate, and summary of changes for PR description.
5. **Stage 5 -> Stage 6 (Release to Independent Review):**
   - *Transferred:* Original issue description, git diff (`git diff origin/main...HEAD`), repository at the latest commit, and pytest test execution output.
   - *Strictly Omitted:* All previous agent prompt transcripts, design scratchpads, implementation reasoning, and retry histories.

## Alternatives Considered
* **Alternative 1: Cumulative Context Append (Monolithic History).** Appending each stage's conversation transcript to an ongoing multi-turn conversation.
  * *Rejection Rationale:* Total context quickly exceeds 50,000 tokens, degrading attention on edge cases. More critically, the reviewer becomes sycophantic when reading the implementer's justification ("I checked for NoneType and it is safe"), blinding the reviewer to latent bugs.
* **Alternative 2: Raw Codebase Only (Zero Specification Handoff).** The Implementation Agent receives only the raw issue without `design.md`.
  * *Rejection Rationale:* As proven in AutoSE Assignment 2, ungrounded agents violate codebase architecture, create redundant modules, and fail cross-component integration tasks.

## Consequences
* **Positive:**
  * Clean isolation: Each agent's input is transparent, inspectable, and auditable as a markdown artifact on disk.
  * Sycophancy elimination: The Reviewer evaluates code strictly against requirements and codebase reality, not against the author's stated intentions.
  * Reproducibility: Any single stage can be re-run in isolation using its input file artifacts.
* **Negative:**
  * Requires robust schema validation on artifacts (e.g., verifying `design.md` actually lists file paths before proceeding to Stage 3).
