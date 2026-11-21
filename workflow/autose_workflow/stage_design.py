"""Stage 2: Architectural Design Agent.

Plans the change by grounding the specification against ARCHITECTURE.md and codebase AST.
"""

import re
from pathlib import Path
from typing import Tuple, List

from .config import AUTOSE_DIR, ARCHITECTURE_FILE, DEFAULT_REASONING_MODEL
from .llm_client import generate


SYSTEM_PROMPT = """You are a Principal Software Architect in an autonomous software development pipeline.
Your task is to design an implementation plan for the given specification, ensuring strict adherence to the repository's architectural constraints.

Read the provided ARCHITECTURE.md carefully:
- Constraint 1: queries.py must NEVER import Table or Database.
- Constraint 2: Storages must implement read(), write(), close().
- Constraint 3: Empty storage read() returns None.
- Constraint 4: Every QueryInstance must produce an immutable _hash tuple with freeze().
- Constraint 5: Middleware transparency via __getattr__.

Output format MUST be valid Markdown with the following exact sections:
# Architecture Design: [Title]

## 1. Target Files & Components
Explicit list of files to modify:
- `tinydb/...`
- `tests/...`

## 2. API & Signature Specifications
Exact method signatures, argument types, and return types to add or alter:
```python
def method_name(self, arg1: Type) -> ReturnType:
```

## 3. Data Flow & Invariants
- Step-by-step logic and state mutations
- Exception handling and edge case behavior

## 4. Architectural Constraint Compliance
- Explicit verification against Constraints 1 through 5.
"""


def execute_stage_2(
    spec_path: Path,
    arch_path: Path = ARCHITECTURE_FILE,
    output_dir: Path = AUTOSE_DIR,
    use_architecture_context: bool = True
) -> Tuple[bool, Path, str]:
    """Execute Stage 2 and return (passed, design_path, log_message)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    design_path = output_dir / "design.md"

    spec_text = spec_path.read_text(encoding="utf-8")
    arch_text = arch_path.read_text(encoding="utf-8") if (use_architecture_context and arch_path.exists()) else ""

    arch_section = f"\n\n### Repository Architecture Document:\n{arch_text}" if arch_text else "\n\n(No architecture documentation provided)."

    prompt = f"""### Specification (spec.md):
{spec_text}
{arch_section}

Please construct the complete design.md detailing target files, method signatures, and architectural invariants.
"""

    design_content = generate(
        prompt=prompt,
        system_instruction=SYSTEM_PROMPT,
        model=DEFAULT_REASONING_MODEL,
        temperature=0.2
    )

    design_path.write_text(design_content, encoding="utf-8")

    # Gating Check: Validate that files and functions to change are explicitly named
    passed, reason = verify_design_gate(design_content)
    return passed, design_path, reason


def verify_design_gate(design_text: str) -> Tuple[bool, str]:
    """Verification Gate for Stage 2: Validate named target files and function signatures."""
    if not design_text or len(design_text.strip()) < 100:
        return False, "Gate Failed: design.md is empty or too short."

    # Must mention tinydb/ path or target file
    has_target_file = bool(re.search(r'tinydb/[\w_]+\.py', design_text))
    # Must specify function/def or class
    has_function_signature = ("def " in design_text) or ("class " in design_text) or ("Signature" in design_text)

    if not has_target_file:
        return False, "Gate Failed: design.md does not name explicit target files under tinydb/."
    if not has_function_signature:
        return False, "Gate Failed: design.md does not name target functions or method signatures."

    return True, "Gate Passed: design.md names explicit target files and signatures."
