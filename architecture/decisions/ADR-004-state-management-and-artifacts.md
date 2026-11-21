# ADR-004: State Management, Persistence, and Run Resumption

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
During workflow execution, intermediate data (specifications, designs, diffs, test logs, review verdicts) must be stored reliably. Furthermore, GitHub Actions runners are ephemeral; if a runner disconnects or if a workflow is restarted or fails mid-run, state must either recover gracefully or avoid leaving corrupted half-finished commits on the repository.

We must decide where state is persisted across stages and across runs.

## Decision
We adopt a **Dual-Layer Persistence Strategy: Ephemeral Filesystem Directory + GitHub Actions Artifact Bundling**:

1. **Local State during a Run (`.autose/` directory on disk):**
   - All intermediate stage outputs are stored in a dedicated directory `.autose/` within the repository root:
     - `.autose/spec.md`
     - `.autose/design.md`
     - `.autose/diff.patch`
     - `.autose/test_report.md`
     - `.autose/pr.md`
     - `.autose/review.md`
     - `.autose/state.json` (Tracks current stage, retry counters, model token consumption, elapsed time)
   - `.autose/` is tracked on the feature branch (`autose/issue-<id>`), making every run's full decision trail permanently inspectable in git history.
2. **Workflow Run Persistence (GitHub Actions Artifacts):**
   - At the conclusion of each job (whether successful or aborted on error), `actions/upload-artifact@v4` uploads the entire `.autose/` directory as an artifact named `autose-run-<run_id>-issue-<id>`.
   - Maintainers and auditors can inspect the artifacts directly from the GitHub Actions run summary UI.
3. **Run Restarts and Idempotency:**
   - If an issue workflow is re-triggered on an existing issue, the orchestrator inspects `origin` for an existing branch `autose/issue-<id>`.
   - If found, it fetches `.autose/state.json`. If a previous stage passed its gate cleanly, the orchestrator skips redundant LLM calls and resumes from the first unmet or failed stage. If invoked with `--fresh`, it archives the previous branch and executes from scratch.

## Alternatives Considered
* **Alternative 1: GitHub PR Comments for Inter-Stage State.** Posting intermediate artifacts as bot comments on the issue or PR.
  * *Rejection Rationale:* Pollutes the public issue discussion with hundreds of lines of machine-generated JSON/markdown, subjects the workflow to GitHub REST API rate limits (5,000 requests/hour), and makes atomicity impossible if network calls drop.
* **Alternative 2: GitHub Actions Cache (`actions/cache`).** Storing artifacts in the workflow cache.
  * *Rejection Rationale:* GitHub Actions cache is non-deterministic, subject to eviction after 7 days or under storage pressure (10GB limit), and invisible to humans inspecting a Pull Request.

## Consequences
* **Positive:**
  * Complete transparency: The feature branch and PR commit contain the exact artifacts that produced the code.
  * High survivability: Runner network hiccups do not corrupt upstream git; state is safely checkpointed locally before branch push.
  * Easy debugging: Local execution behaves identically to GitHub Actions execution.
* **Negative:**
  * Commits contain documentation artifacts alongside source modifications (handled cleanly by placing artifacts in `.autose/` and leaving production packages untouched).
