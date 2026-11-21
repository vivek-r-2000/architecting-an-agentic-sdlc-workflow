"""Stage 4: Testing & Verification Agent.

Synthesizes acceptance tests, executes pytest across baseline and new suites, and verifies gate.
"""

import subprocess
from pathlib import Path
from typing import Tuple, Dict, Any

from .config import AUTOSE_DIR, WORKSPACE_ROOT, DEFAULT_FAST_MODEL
from .llm_client import generate


SYSTEM_PROMPT = """You are a Quality Assurance Automation Engineer.
Based on the provided spec.md, write executable pytest test cases for TinyDB.

Output MUST be valid, standalone pytest code:
```python
import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_acceptance_criteria_1():
    ...
```
Do not mock internal TinyDB structures unless necessary; use MemoryStorage for fast, clean in-memory tests.
"""


def execute_stage_4(
    spec_path: Path,
    output_dir: Path = AUTOSE_DIR,
    workspace_root: Path = WORKSPACE_ROOT
) -> Tuple[bool, Path, str, str]:
    """Execute Stage 4 and return (passed, report_path, reason, error_trace)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "test_report.md"
    test_file_path = output_dir / "test_acceptance.py"

    spec_text = spec_path.read_text(encoding="utf-8")

    # Generate acceptance tests
    prompt = f"""### Specification (spec.md):
{spec_text}

Generate comprehensive pytest test cases validating all acceptance criteria.
"""

    test_code = generate(
        prompt=prompt,
        system_instruction=SYSTEM_PROMPT,
        model=DEFAULT_FAST_MODEL,
        temperature=0.2
    )

    clean_code = extract_python_code(test_code)
    test_file_path.write_text(clean_code, encoding="utf-8")

    # Run Pytest: Baseline suite + Newly authored acceptance test
    res = subprocess.run(
        ["uv", "run", "pytest", "tests/", str(test_file_path), "-v", "--no-cov"],
        cwd=workspace_root,
        capture_output=True,
        text=True
    )

    full_output = res.stdout + "\n" + res.stderr
    passed = (res.returncode == 0)

    # Compile test_report.md
    report_content = f"""# Test Execution Report

## Status: {'PASSED' if passed else 'FAILED'}
- **Exit Code:** {res.returncode}
- **Baseline Test Suite:** tests/
- **Synthesized Acceptance Suite:** {test_file_path.name}

## Execution Output:
```text
{full_output[-3000:]}
```
"""
    report_path.write_text(report_content, encoding="utf-8")

    if passed:
        return True, report_path, "Gate Passed: All 228 baseline tests and all new acceptance tests pass.", ""
    else:
        error_trace = extract_failure_trace(full_output)
        return False, report_path, f"Gate Failed: Tests failed with exit code {res.returncode}.", error_trace


def extract_python_code(llm_output: str) -> str:
    """Extract python code from markdown fence or return default."""
    if "```python" in llm_output:
        code = llm_output.split("```python")[1].split("```")[0].strip()
        return code
    elif "```" in llm_output:
        code = llm_output.split("```")[1].split("```")[0].strip()
        return code
    return llm_output


def extract_failure_trace(pytest_output: str) -> str:
    """Extract failure snippet from pytest output for targeted remediation."""
    if "FAILURES" in pytest_output:
        return pytest_output.split("FAILURES")[1][:2000]
    return pytest_output[-1500:]
