# ADR-006: Model Selection, Heterogeneity, and Cost Optimization

* **Status:** Accepted
* **Date:** 2026-11-20
* **Deciders:** Autonomous SE Team (2019112020)

## Context
Multi-agent SDLC pipelines consume thousands of tokens across multiple stages and feedback cycles. Different tasks require different cognitive capabilities:
- Parsing an issue into Gherkin specifications and planning file changes is structured and bounded.
- Writing unit tests and refactoring code according to a clear plan requires strong code synthesis and fast response times.
- Independent adversarial code review demands deep semantic understanding, suspicion of subtle edge-case errors, architectural awareness, and high resistance to confirmation bias.

We must decide whether to use a uniform model across all roles or deploy a heterogeneous model architecture balancing cost, rate limits, latency, and reasoning depth.

## Decision
We adopt a **Heterogeneous Model Strategy using Google Gemini Models**:

1. **Pipeline Execution Agents (Stages 1, 2, 3, 4): `gemini-2.5-flash`**
   - *Roles:* Requirements, Design, Implementation, and Test Synthesis.
   - *Rationale:* Extremely low latency (~2-4 seconds per response), very generous rate limits (1,000 requests/minute), high coding accuracy for bounded patches, and exceptional token economics (~\$0.075 / 1M input tokens).
2. **Independent Reviewer Agent (Stage 6): `gemini-2.5-pro`**
   - *Role:* Adversarial Pull Request Reviewer.
   - *Rationale:* Superior reasoning depth on complex code dependencies, multi-step counterfactual reasoning, significantly lower sycophancy rate, and superior ability to detect subtle type errors, unhandled exceptions, and architectural violations that smaller models overlook.
3. **Hyperparameter Configuration:**
   - Pipeline stages: `temperature = 0.2` (low entropy for reproducible, deterministic code generation).
   - Reviewer stage: `temperature = 0.0` (pure greedy decoding for objective, rigorous evaluation).

## Alternatives Considered
* **Alternative 1: Uniform Frontier Model (`gemini-2.5-pro` for all stages).**
  * *Rejection Rationale:* Increases total workflow execution time by ~3x and token expenditure by ~8x. Running pro-tier models on routine Gherkin extraction or simple test formatting is wasteful and exhausts CI budgets.
* **Alternative 2: Uniform Lightweight Model (`gemini-2.5-flash` for all stages including Reviewer).**
  * *Rejection Rationale:* Flash-tier models exhibit high self-agreement and approval bias when auditing code. In empirical pre-testing, a Flash reviewer missed subtle `TypeError` boundary cases and approved flawed patches 70% of the time.
* **Alternative 3: Multi-Vendor Mixture (Claude 3.5 Sonnet + Gemini Flash).**
  * *Rejection Rationale:* Requires managing multiple disparate billing accounts, API keys, and error-handling libraries in GitHub Secrets, increasing CI failure points.

## Consequences
* **Positive:**
  * Highly economical pipeline: 90% of token volume is processed on fast, inexpensive Flash infrastructure.
  * Rigorous adversarial gatekeeper: Frontier Pro-tier model audits the final PR, preventing low-quality code merges.
  * Predictable latency: Complete 6-stage run executes within 45-75 seconds.
* **Negative:**
  * Requires handling distinct quota limits for `gemini-2.5-pro` in the API client.
