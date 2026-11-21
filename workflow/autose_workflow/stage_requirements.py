"""Stage 1: Requirements Engineering Agent.

Transforms raw issue text into a structured specification with Gherkin acceptance criteria.
"""

import re
from pathlib import Path
from typing import Dict, Any, Tuple

from .config import AUTOSE_DIR, DEFAULT_FAST_MODEL
from .llm_client import generate


SYSTEM_PROMPT = """You are an expert Requirements Engineer in an autonomous software development pipeline.
Your task is to analyze a GitHub issue for the TinyDB repository and formalize it into a rigorous specification.

Output format MUST be valid Markdown with the following exact sections:
# Specification: [Issue Title]

## 1. Problem Statement & Scope
- High-level overview of bug or feature
- In-scope goals
- Out-of-scope non-goals

## 2. Acceptance Criteria (Gherkin Format)
Must contain testable criteria using [AC-1], [AC-2] tags:
### [AC-1] Scenario: Description
- **Given** [preconditions]
- **When** [action or query executed]
- **Then** [expected observable state or return value]

## 3. Edge Cases & Invariants
- Null, missing, or incomparable types handling
- Caching / hashability invariants

Do not write implementation source code. Only provide requirements and acceptance criteria.
"""


def execute_stage_1(
    issue_title: str,
    issue_body: str,
    output_dir: Path = AUTOSE_DIR
) -> Tuple[bool, Path, str]:
    """Execute Stage 1 and return (passed, spec_path, log_message)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    spec_path = output_dir / "spec.md"

    prompt = f"""<UNTRUSTED_USER_INPUT>
Issue Title: {issue_title}

Issue Body:
{issue_body}
</UNTRUSTED_USER_INPUT>

Please produce the formalized spec.md following the Gherkin acceptance criteria rules.
"""

    spec_content = generate(
        prompt=prompt,
        system_instruction=SYSTEM_PROMPT,
        model=DEFAULT_FAST_MODEL,
        temperature=0.2
    )

    spec_path.write_text(spec_content, encoding="utf-8")

    # Gating Check: Verify presence of Acceptance Criteria tags and Given/When/Then clauses
    passed, reason = verify_spec_gate(spec_content)
    return passed, spec_path, reason


def verify_spec_gate(spec_text: str) -> Tuple[bool, str]:
    """Verification Gate for Stage 1: Validate testability of acceptance criteria."""
    if not spec_text or len(spec_text.strip()) < 100:
        return False, "Gate Failed: spec.md is empty or too short."

    has_ac = bool(re.search(r'\[AC-\d+\]', spec_text))
    has_given = "given" in spec_text.lower()
    has_when = "when" in spec_text.lower()
    has_then = "then" in spec_text.lower()

    if not has_ac:
        return False, "Gate Failed: No [AC-x] criteria tags found in spec.md."
    if not (has_given and has_when and has_then):
        return False, "Gate Failed: Criteria must include Given/When/Then Gherkin clauses."

    return True, "Gate Passed: spec.md contains verified testable acceptance criteria."
