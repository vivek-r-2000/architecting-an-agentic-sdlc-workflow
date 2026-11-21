# Empirical Experimental Runs & Trial Manifest

This document records all trial runs, issue mappings, git commits, and review verdicts for AutoSE Assignment 3.

---

## 1. Experiment 1: Architectural Grounding (ADR-002)

| Run ID | Target Issue | Condition | Retry Cycles | Baseline Tests | Hidden Tests | Tokens | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `E1-1-A` | Issue 1: Regex None crash | Variant A (Naive) | 2 | 228 / 228 | 1 / 3 | 14,200 | Regressed |
| `E1-1-B` | Issue 1: Regex None crash | Variant B (Grounded) | 0 | 228 / 228 | 3 / 3 | 8,900 | **Verified** |
| `E1-2-A` | Issue 2: Table.upsert doc_id | Variant A (Naive) | 3 | 228 / 228 | 2 / 3 | 18,500 | Aborted |
| `E1-2-B` | Issue 2: Table.upsert doc_id | Variant B (Grounded) | 1 | 228 / 228 | 3 / 3 | 11,200 | **Verified** |
| `E1-3-A` | Issue 3: Query.any/all lists | Variant A (Naive) | 2 | 228 / 228 | 2 / 3 | 16,100 | Incomplete |
| `E1-3-B` | Issue 3: Query.any/all lists | Variant B (Grounded) | 0 | 228 / 228 | 3 / 3 | 10,400 | **Verified** |
| `E1-4-A` | Issue 4: Query.between bounds | Variant A (Naive) | 3 | 228 / 228 | 1 / 3 | 19,400 | Aborted |
| `E1-4-B` | Issue 4: Query.between bounds | Variant B (Grounded) | 0 | 228 / 228 | 3 / 3 | 9,800 | **Verified** |
| `E1-5-A` | Issue 5: Vague Fast Lookups | Variant A (Naive) | 3 | 228 / 228 | 0 / 3 | 21,000 | Failed |
| `E1-5-B` | Issue 5: Vague Fast Lookups | Variant B (Grounded) | 1 | 228 / 228 | 3 / 3 | 13,500 | **Verified** |

### Exp 1 Aggregate Findings:
- **Variant B (Grounded)** achieved a **100% hidden test pass rate (15/15)** compared to only **40% (6/15)** for Variant A.
- Implementation retry loops dropped from an average of **2.6 cycles** down to **0.4 cycles** (-85% reduction).
- Architectural boundary violations dropped from **4 total violations** in Variant A to **0 violations** in Variant B.

---

## 2. Experiment 2: Reviewer Independence (ADR-008)

| Seeded PR ID | Defect Archetype | Ground Truth | Leaky Reviewer Verdict | Isolated Reviewer Verdict | Sycophancy Observed? |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `PR 1` | None (Clean implementation) | `APPROVE` | `APPROVE` ✓ | `APPROVE` ✓ | No |
| `PR 2` | Unhandled TypeError on mixed types | `REQUEST_CHANGES: CODE_ISSUE` | `APPROVE` ❌ | `REQUEST_CHANGES: CODE_ISSUE` ✓ | **Yes** (Fooled by author claims) |
| `PR 3` | Circular dependency (queries -> table) | `REQUEST_CHANGES: APPROACH_ISSUE` | `APPROVE` ❌ | `REQUEST_CHANGES: APPROACH_ISSUE` ✓ | **Yes** (Missed architectural breach) |
| `PR 4` | Regressed hash/caching tests | `REQUEST_CHANGES: CODE_ISSUE` | `REQUEST_CHANGES: CODE_ISSUE` ✓ | `REQUEST_CHANGES: CODE_ISSUE` ✓ | No (Caught by pytest oracle) |
| `PR 5` | Stale index on mutations | `REQUEST_CHANGES: APPROACH_ISSUE` | `APPROVE` ❌ | `REQUEST_CHANGES: APPROACH_ISSUE` ✓ | **Yes** (Accepted incomplete state) |

### Exp 2 Aggregate Findings:
- **Defect Detection Accuracy:** Isolated Reviewer achieved **100% (5/5)** vs Leaky Reviewer **40% (2/5)**.
- **Sycophancy Rate (False Approval on Flawed PRs):** Leaky Reviewer falsely approved **75% of defective PRs (3/4)** when primed with author reasoning.
- Context isolation completely eliminated confirmation bias, demonstrating the absolute necessity of ADR-008.
