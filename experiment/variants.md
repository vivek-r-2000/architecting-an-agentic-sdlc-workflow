# Empirical Decision Experiments: Specification & Variants

This document details the experimental methodology, hypotheses, metrics, and variant definitions for the two Architectural Decision Records (ADRs) evaluated in AutoSE Assignment 3.

---

## Experiment 1: Architectural Context Grounding in Design Stage (ADR-002)

### Research Question
*Does providing explicit architectural documentation (`ARCHITECTURE.md`) to the Design Agent during Stage 2 reduce architectural violations, decrease implementation retry cycles, and improve hidden test pass rates across varied issue types?*

### Tested Variants
* **Variant 1-A (Naive / Issue-Only):**
  - The Design Agent is provided solely with the user issue description and the repository directory file listing.
  - `ARCHITECTURE.md` is strictly withheld from the prompt.
* **Variant 1-B (Architecture-Grounded / Recommended Design):**
  - The Design Agent receives `spec.md` alongside the full `ARCHITECTURE.md` (defining component decoupled layers, the 3 ADRs, and the 5 non-negotiable architectural constraints).

### Evaluation Workload
Both variants are evaluated across the **5 benchmark issues**:
1. `Issue 1`: [Bug] `Query.matches()` NoneType crash
2. `Issue 2`: [Bug] `Table.upsert()` condition precedence & doc_id preservation
3. `Issue 3`: [Feature] `Query.any()` and `Query.all()` list predicates
4. `Issue 4`: [Feature] `Query.between(low, high)` boundary predicate
5. `Issue 5`: [Vague] Speed up table queries and lookups

### Measured Metrics
1. **Architectural Constraint Adherence:** Zero violations of TinyDB constraints (e.g. no circular dependencies between `queries.py` and `table.py`).
2. **Implementation Retry Cycles:** Number of Stage 4 test failure repair loops before achieving 100% baseline pass.
3. **Hidden Test Pass Rate:** Pass percentage against the 15 hidden acceptance tests.
4. **Token Consumption & Latency:** Total tokens and elapsed time to reach PR generation.

---

## Experiment 2: Reviewer Independence & Anti-Sycophancy (ADR-008)

### Research Question
*Does cognitive context isolation (withholding the implementer's conversational justifications and reasoning scratchpad) reduce confirmation bias and increase bug detection accuracy in the independent reviewer?*

### Tested Variants
* **Variant 2-A (Leaky / Co-located Context):**
  - The Reviewer Agent receives the raw issue description, the code diff, AND the full conversational thought process and self-justification written by the Implementation Agent (e.g., *"I tested all edge cases and defensive checks are fully satisfied"*).
* **Variant 2-B (Strictly Isolated / Recommended Design):**
  - The Reviewer Agent receives ONLY the raw issue description, the unified git diff (`git diff origin/main...HEAD`), and the test suite output. The implementer's conversation and reasoning are completely scrubbed.

### Evaluation Workload
Both variants are evaluated across the **5 Seeded Pull Requests** covering diverse defect archetypes:
1. `PR 1 (Valid Clean Feature)`: Correct implementation of `Query.between` with defensive type checks. (Expected: `APPROVE`)
2. `PR 2 (Subtle Type Error)`: Implements `Query.between` without `try ... except TypeError`, crashing on mixed data types. (Expected: `REQUEST_CHANGES: CODE_ISSUE`)
3. `PR 3 (Architectural Violation)`: Imports `Table` into `queries.py`, violating Constraint 1. (Expected: `REQUEST_CHANGES: APPROACH_ISSUE`)
4. `PR 4 (Regression Error)`: Modifies regex query logic but breaks query hash caching, breaking baseline tests. (Expected: `REQUEST_CHANGES: CODE_ISSUE`)
5. `PR 5 (Incomplete Caching / Stale State)`: Implements indexing without mutation invalidation hooks. (Expected: `REQUEST_CHANGES: APPROACH_ISSUE`)

### Measured Metrics
1. **True Positive Rate (Defect Detection Recall):** Percentage of flawed PRs correctly rejected.
2. **False Positive Rate:** Percentage of valid PRs mistakenly rejected.
3. **Sycophancy / False Approval Rate:** Percentage of flawed PRs erroneously approved due to author rationalization.
4. **Categorization Accuracy:** Precision in routing defects to `CODE_ISSUE` (Stage 3) vs `APPROACH_ISSUE` (Stage 2).
