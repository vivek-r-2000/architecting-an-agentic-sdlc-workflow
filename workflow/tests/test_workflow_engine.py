"""Unit tests for the AutoSE Workflow Engine and Verification Gates."""

import pytest
from pathlib import Path

from autose_workflow.stage_requirements import verify_spec_gate
from autose_workflow.stage_design import verify_design_gate
from autose_workflow.stage_implement import verify_build_gate
from autose_workflow.stage_review import parse_verdict
from autose_workflow.orchestrator import SDLCWorkflowOrchestrator


def test_stage_1_spec_gate_validation():
    valid_spec = """# Specification: Feature
## Acceptance Criteria
### [AC-1] Scenario: Basic
- Given an empty database
- When item is inserted
- Then item exists
"""
    passed, msg = verify_spec_gate(valid_spec)
    assert passed is True
    assert "Passed" in msg

    invalid_spec = "Short note with no criteria."
    passed, msg = verify_spec_gate(invalid_spec)
    assert passed is False


def test_stage_2_design_gate_validation():
    valid_design = """# Design Document
## Target Files
- `tinydb/queries.py`
## Signature
```python
def between(self, low: int, high: int) -> QueryInstance:
    pass
```
"""
    passed, msg = verify_design_gate(valid_design)
    assert passed is True
    assert "Passed" in msg

    invalid_design = "Just a high level idea with no files."
    passed, msg = verify_design_gate(invalid_design)
    assert passed is False


def test_stage_3_build_gate(tmp_path):
    # Test valid python file build
    tinydb_dir = tmp_path / "tinydb"
    tinydb_dir.mkdir()
    (tinydb_dir / "valid.py").write_text("x = 10\n", encoding="utf-8")
    passed, msg = verify_build_gate(tmp_path)
    assert passed is True

    # Test syntax error detection
    (tinydb_dir / "invalid.py").write_text("def broken_syntax(\n", encoding="utf-8")
    passed, msg = verify_build_gate(tmp_path)
    assert passed is False
    assert "SyntaxError" in msg


def test_stage_6_verdict_parsing():
    raw_review = """Here is the review.
```json
{
  "verdict": "APPROVE",
  "category": "NONE",
  "summary": "Looks good and tested.",
  "required_actions": []
}
```
"""
    data = parse_verdict(raw_review)
    assert data["verdict"] == "APPROVE"
    assert data["category"] == "NONE"

    change_review = "REQUEST_CHANGES: Missing type check on line 42."
    data = parse_verdict(change_review)
    assert data["verdict"] == "REQUEST_CHANGES"
