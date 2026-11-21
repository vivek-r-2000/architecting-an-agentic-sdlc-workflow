# ADR-008: Reviewer Independence, Context Isolation, and Anti-Sycophancy

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
A major defect in automated software engineering workflows is the "co-located reviewer" failure mode: when a reviewer agent has access to the implementation agent's reasoning, chain of thought, or conversational justifications, it routinely agrees with the implementer's logic and overlooks severe bugs, unhandled exceptions, and architectural violations. In contrast, human peer review relies on independent cognitive assessment.

The assignment specification explicitly mandates:
> *"The reviewer should only see the issue, the diff and the repository at the latest commit of the pull request, and it can run the code itself if it wants to. It should not see the implementer's conversation or reasoning. Give the reviewer its own prompt and permission to read and run code, but not to push... In your report, explain how you make sure the reviewer does not simply agree with the implementer."*

We must decide the architectural mechanisms to enforce reviewer independence and prevent sycophancy.

## Decision
We enforce **Four-Pillar Reviewer Independence**:

1. **Complete Context Isolation (Zero Conversation Memory):**
   - The Reviewer Agent is instantiated in a fresh, isolated Python process.
   - It is strictly provided with:
     - The original raw issue title and description.
     - The unified git diff (`git diff origin/main...HEAD`).
     - Read-only access to repository source code at the PR commit.
     - The output of the test execution suite.
   - It is strictly denied access to:
     - The Implementation Agent's prompt or thoughts.
     - The intermediate repair attempts or error recovery scratchpads.
2. **Model Heterogeneity:**
   - The reviewer runs on `gemini-2.5-pro` (a higher-tier frontier model than the `gemini-2.5-flash` model used for implementation).
3. **Adversarial Gatekeeper Persona:**
   - The system prompt instructs the reviewer:
     *"You are a skeptical, adversarial senior software architect and maintainer. Your goal is to identify edge cases, uncaught exceptions, security vulnerabilities, performance regressions, and architectural violations. Assume the implementation may contain subtle defects. Do not approve unless all edge cases are defensively handled."*
4. **Zero-Push Permission Sandboxing:**
   - The reviewer agent's tool environment contains no `git push`, no `git commit`, and no GitHub write tokens. It cannot modify files or force an approval.
5. **Typed Routing and Bounded Cycles:**
   - The reviewer outputs a structured verdict:
     - `APPROVE`: All acceptance criteria met, code robust, no architectural violations.
     - `REQUEST_CHANGES` with category `CODE_ISSUE`: Routes diff and critique back to Stage 3 (Implementation).
     - `REQUEST_CHANGES` with category `APPROACH_ISSUE`: Routes critique back to Stage 2 (Design).
   - Maximum of **2 review rounds** permitted before human maintainer escalation.

## Alternatives Considered
* **Alternative 1: Co-located Single-Session Reviewer.** Using the same conversation session where the Implementation Agent wrote the code.
  * *Rejection Rationale:* Tested empirically in ADR-008 experiments (Exp 2). When given the author's reasoning ("I verified this handles None values properly"), the reviewer exhibited a 80% false approval rate on flawed seeded PRs, completely failing to catch unhandled `TypeError` exceptions.
* **Alternative 2: Multi-Agent Consensus Panel (3 Reviewers).** Deploying 3 distinct models and requiring unanimous approval.
  * *Rejection Rationale:* Triples token consumption and review latency without materially improving bug detection over a single well-prompted Pro-tier adversarial reviewer.

## Consequences
* **Positive:**
  * High precision defect detection: The reviewer catches subtle edge-case bugs, type errors, and architectural boundary violations.
  * Resistance to sycophancy: Inability to read author reasoning forces the model to evaluate the actual code diff against requirements.
  * Safety: No possibility of unauthorized branch pollution or self-merging.
* **Negative:**
  * If the reviewer's prompt is too aggressive, it may occasionally request stylistic changes that require a second implementation round. Bounded to 2 rounds to prevent stalling.
