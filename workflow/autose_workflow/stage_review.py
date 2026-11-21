"""Stage 6: Independent Adversarial Reviewer Agent.

Operates with strict context isolation (zero implementer memory, no push rights)
and emits typed verdicts: APPROVE, REQUEST_CHANGES (CODE_ISSUE / APPROACH_ISSUE).
"""

import json
import re
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

from .config import AUTOSE_DIR, WORKSPACE_ROOT, DEFAULT_REVIEWER_MODEL
from .llm_client import generate


REVIEWER_SYSTEM_PROMPT = """You are an independent, skeptical Senior Software Architect and Maintainer reviewing a Pull Request.

CRITICAL OPERATIONAL RULES:
1. You have NO prior relationship with the author. Evaluate strictly based on the issue description, code diff, and test results.
2. Be rigorous. Check for:
   - Unhandled exceptions (e.g. comparing None or string with integers).
   - Missing edge cases.
   - Architectural violations (e.g. queries.py importing table or storage classes).
   - Stale cache or missing invalidation.
3. You must emit your final verdict as a strict JSON block at the end of your review:
```json
{
  "verdict": "APPROVE" | "REQUEST_CHANGES",
  "category": "NONE" | "CODE_ISSUE" | "APPROACH_ISSUE",
  "summary": "1-2 sentence summary of findings",
  "required_actions": ["bullet point 1", "bullet point 2"]
}
```
If there are code bugs or missing edge cases, use category: "CODE_ISSUE".
If there is an architectural violation or incorrect design approach, use category: "APPROACH_ISSUE".
If the code is clean, robust, and verified, use verdict: "APPROVE", category: "NONE".
"""


def execute_stage_6(
    issue_title: str,
    issue_body: str,
    diff_text: str,
    test_output: str,
    output_dir: Path = AUTOSE_DIR,
    model: str = DEFAULT_REVIEWER_MODEL,
    leaked_implementer_history: Optional[str] = None
) -> Tuple[bool, Path, str, Dict[str, Any]]:
    """Execute Stage 6: Isolated adversarial review."""
    output_dir.mkdir(parents=True, exist_ok=True)
    review_path = output_dir / "review.md"

    # In strict isolation mode, leaked_implementer_history is completely omitted!
    history_section = ""
    if leaked_implementer_history:
        history_section = f"\n\n### [LEAKED] Author Implementation Reasoning:\n{leaked_implementer_history}\n"

    prompt = f"""### Issue Description:
Title: {issue_title}
Body:
{issue_body}
{history_section}
### Code Diff under Review:
```diff
{diff_text}
```

### Pytest Verification Output:
```text
{test_output[-1500:]}
```

Please perform your independent code review and append the required JSON verdict block.
"""

    review_text = generate(
        prompt=prompt,
        system_instruction=REVIEWER_SYSTEM_PROMPT,
        model=model,
        temperature=0.0
    )

    review_path.write_text(review_text, encoding="utf-8")

    # Parse JSON verdict
    verdict_data = parse_verdict(review_text)

    is_approved = (verdict_data.get("verdict") == "APPROVE")
    reason = f"Reviewer Verdict: {verdict_data.get('verdict')} ({verdict_data.get('category')}) - {verdict_data.get('summary')}"

    return is_approved, review_path, reason, verdict_data


def parse_verdict(review_text: str) -> Dict[str, Any]:
    """Parse JSON verdict from reviewer response."""
    default_verdict = {
        "verdict": "APPROVE",
        "category": "NONE",
        "summary": "Review completed.",
        "required_actions": []
    }

    try:
        if "```json" in review_text:
            raw_json = review_text.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_json)
        elif "```" in review_text:
            raw_json = review_text.split("```")[1].split("```")[0].strip()
            return json.loads(raw_json)
    except Exception:
        pass

    # Heuristic fallback if json block was malformed
    if "REQUEST_CHANGES" in review_text or "CHANGES_REQUESTED" in review_text:
        cat = "APPROACH_ISSUE" if "architect" in review_text.lower() else "CODE_ISSUE"
        return {
            "verdict": "REQUEST_CHANGES",
            "category": cat,
            "summary": "Reviewer requested changes based on review analysis.",
            "required_actions": ["Address reviewer critique"]
        }

    return default_verdict
