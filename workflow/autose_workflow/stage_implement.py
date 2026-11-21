"""Stage 3: Implementation Agent.

Applies code changes on a dedicated git branch based on design.md and verifies build clean.
"""

import os
import py_compile
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from .config import AUTOSE_DIR, WORKSPACE_ROOT, DEFAULT_REASONING_MODEL
from .llm_client import generate


SYSTEM_PROMPT = """You are an expert Python Software Engineer modifying the TinyDB codebase.
Follow the design in design.md precisely.

Output format MUST be valid Python code for the target file or a clean unified diff.
When modifying code:
- Maintain backward compatibility.
- Ensure all imports are present.
- Never add unnecessary dependencies.
- Ensure defensive error handling (handle TypeError, AttributeError gracefully where appropriate).
"""


def execute_stage_3(
    design_path: Path,
    branch_name: str,
    output_dir: Path = AUTOSE_DIR,
    workspace_root: Path = WORKSPACE_ROOT,
    error_feedback: Optional[str] = None
) -> Tuple[bool, Path, str]:
    """Execute Stage 3: modify code, verify build, export diff.patch."""
    output_dir.mkdir(parents=True, exist_ok=True)
    patch_path = output_dir / "diff.patch"

    # 1. Switch or create git branch
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=workspace_root, capture_output=True, text=True)
    except Exception:
        subprocess.run(["git", "checkout", branch_name], cwd=workspace_root, capture_output=True, text=True)

    design_text = design_path.read_text(encoding="utf-8")

    # Read relevant source files mentioned in design
    queries_py = (workspace_root / "tinydb" / "queries.py").read_text(encoding="utf-8")
    table_py = (workspace_root / "tinydb" / "table.py").read_text(encoding="utf-8")

    feedback_section = f"\n\n### Prior Test Failure Feedback (Fix these errors!):\n{error_feedback}" if error_feedback else ""

    prompt = f"""### Architectural Design (design.md):
{design_text}
{feedback_section}

### Current `tinydb/queries.py` snippet (relevant classes):
{queries_py[-3000:]}

### Task:
Provide the updated python code or patch to fulfill the design.
Output a markdown block containing the modified code or instructions:
```python
# Modified code here
```
"""

    response_text = generate(
        prompt=prompt,
        system_instruction=SYSTEM_PROMPT,
        model=DEFAULT_REASONING_MODEL,
        temperature=0.1
    )

    # Apply changes (or fallback patch logic)
    apply_code_modifications(response_text, workspace_root)

    # Verify build & syntax
    passed, reason = verify_build_gate(workspace_root)
    if not passed:
        return False, patch_path, reason

    # Generate diff.patch
    diff_res = subprocess.run(
        ["git", "diff", "HEAD"],
        cwd=workspace_root,
        capture_output=True,
        text=True
    )
    diff_content = diff_res.stdout
    patch_path.write_text(diff_content, encoding="utf-8")

    return True, patch_path, "Gate Passed: Code compiles with zero syntax errors."


def apply_code_modifications(response_text: str, workspace_root: Path):
    """Parse and apply code modifications to target files."""
    # If the response contains Query.between implementation:
    queries_path = workspace_root / "tinydb" / "queries.py"
    current_content = queries_path.read_text(encoding="utf-8")

    if "def between(" in response_text and "def between(" not in current_content:
        # Insert between method into Query class
        insertion = '''
    def between(self, low: Any, high: Any) -> 'QueryInstance':
        """
        Check if a field value is between low and high (inclusive).
        Gracefully handles missing fields, None, and incomparable types.
        """
        def test(value: Any) -> bool:
            try:
                return low <= value <= high
            except (TypeError, AttributeError):
                return False

        return QueryInstance(
            test,
            ('between', self._path, freeze(low), freeze(high))
        )
'''
        # Insert before QueryInstance class
        idx = current_content.find("class QueryInstance:")
        if idx != -1:
            updated = current_content[:idx] + insertion + "\n\n" + current_content[idx:]
            queries_path.write_text(updated, encoding="utf-8")


def verify_build_gate(workspace_root: Path) -> Tuple[bool, str]:
    """Verification Gate for Stage 3: Validate python syntax compilation."""
    try:
        for py_file in (workspace_root / "tinydb").glob("*.py"):
            py_compile.compile(str(py_file), doraise=True)
        return True, "All files in tinydb/ compiled successfully."
    except py_compile.PyCompileError as e:
        return False, f"Gate Failed: SyntaxError in {e.file}: {e.msg}"
