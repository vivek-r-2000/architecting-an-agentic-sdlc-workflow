# ADR-010: Workflow Triggers, Permission Gates, and Concurrency Control

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
A GitHub Actions workflow that responds to public events must be tightly regulated:
- Anyone can open issues or post comments on a public repository. If every issue automatically triggered a 6-stage multi-agent run, malicious actors could spawn hundreds of concurrent jobs (Denial of Service and quota exhaustion).
- If multiple maintainers comment `/autose` simultaneously, or if a user modifies an issue while a workflow is actively writing a patch, concurrent git operations will clash, causing branch conflict errors, non-atomic commits, and corrupted PR states.

We must define the triggering criteria, actor authorization gates, and concurrency handling strategy.

## Decision
We enforce **Maintainer-Gated Triggers with Per-Issue Concurrency Serialization**:

1. **Triggering Events:**
   The workflow is triggered exclusively by two events in `.github/workflows/autose.yml`:
   ```yaml
   on:
     issues:
       types: [labeled]
     issue_comment:
       types: [created]
   ```
2. **Actor Authorization & Gating Filters:**
   - **Label Trigger:** Triggers only when the label added is exactly `autose`.
   - **Comment Trigger:** Triggers only when the comment begins with the command `/autose`.
   - **Authorization Gate:** The triggering user (`github.actor`) must possess repository `write` or `admin` permissions (`github.event.comment.author_association in ['COLLABORATOR', 'MEMBER', 'OWNER']`). Comments from unauthorized external users are ignored immediately with a polite explanatory reaction or comment.
3. **Concurrency Control:**
   - Workflows are serialized at the per-issue level using GitHub Actions concurrency groups:
     ```yaml
     concurrency:
       group: autose-issue-${{ github.event.issue.number }}
       cancel-in-progress: false
     ```
   - `cancel-in-progress: false` ensures that an active agent run is never killed midway through a git commit or branch creation. If a second maintainer triggers the workflow on the same issue, the second run queues politely until the first run settles.
   - Separate issues (e.g. Issue #42 and Issue #43) run concurrently in parallel up to the runner limit.

## Alternatives Considered
* **Alternative 1: Trigger on Every `issues: [opened]`.** Automatically running on all newly created issues.
  * *Rejection Rationale:* Extremely dangerous on public open-source forks. Spam issues or bot issues would immediately drain API quotas and spam the repository with dozens of speculative pull requests.
* **Alternative 2: Global Concurrency Lock (`group: autose-global`).** Allowing only one issue to be processed across the entire repository at any given time.
  * *Rejection Rationale:* Unnecessarily bottlenecks team productivity when unrelated issues (e.g., a bug in `queries.py` and a doc update in `storages.py`) can be safely developed on distinct feature branches in parallel.

## Consequences
* **Positive:**
  * Complete protection against unauthorized quota exhaustion: Only trusted maintainers can start a run.
  * Race-condition free: Per-issue concurrency guarantees atomic branch updates and clean PR creation without git conflicts.
  * Safe multi-tenancy: Independent issues are processed in parallel without blocking each other.
* **Negative:**
  * Maintainers must remember to apply the `autose` label or type `/autose` to initiate the agent pipeline.
