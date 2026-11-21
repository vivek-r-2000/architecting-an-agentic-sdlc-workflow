"""Master Orchestrator for AutoSE SDLC Multi-Agent Workflow.

Coordinates Stages 1 through 6, manages retry and review loops, and persists state.
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

from .config import (
    AUTOSE_DIR,
    WORKSPACE_ROOT,
    MAX_TEST_RETRIES,
    MAX_REVIEW_ROUNDS,
)
from .stage_requirements import execute_stage_1
from .stage_design import execute_stage_2
from .stage_implement import execute_stage_3
from .stage_test import execute_stage_4
from .stage_release import execute_stage_5
from .stage_review import execute_stage_6
from .llm_client import global_tracker

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s")
logger = logging.getLogger("autose.orchestrator")


class SDLCWorkflowOrchestrator:
    def __init__(
        self,
        issue_id: int,
        issue_title: str,
        issue_body: str,
        workspace_root: Path = WORKSPACE_ROOT,
        output_dir: Path = AUTOSE_DIR,
        use_architecture_context: bool = True,
        push_to_remote: bool = False
    ):
        self.issue_id = issue_id
        self.issue_title = issue_title
        self.issue_body = issue_body
        self.workspace_root = workspace_root
        self.output_dir = output_dir
        self.use_architecture_context = use_architecture_context
        self.push_to_remote = push_to_remote

        self.branch_name = f"autose/issue-{issue_id}"
        self.state_file = output_dir / "state.json"

        self.state = {
            "issue_id": issue_id,
            "status": "INITIALIZED",
            "stages_completed": [],
            "test_retry_count": 0,
            "review_round_count": 0,
            "final_verdict": None,
            "tokens_used": 0,
            "elapsed_seconds": 0.0,
        }

    def run(self) -> Dict[str, Any]:
        """Execute the complete 6-stage lifecycle."""
        start_time = time.time()
        logger.info(f"::group::AutoSE SDLC Workflow Start: Issue #{self.issue_id} - '{self.issue_title}'")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Stage 1: Requirements
            logger.info("Executing Stage 1: Requirements Engineering...")
            s1_pass, spec_path, s1_msg = execute_stage_1(self.issue_title, self.issue_body, self.output_dir)
            if not s1_pass:
                return self._terminate_failure("STAGE_1_REQUIREMENTS_FAILED", s1_msg)
            self.state["stages_completed"].append("Stage 1: Requirements")

            # Review feedback loop can re-enter at Stage 2 (Approach issue) or Stage 3 (Code issue)
            review_round = 0
            while review_round <= MAX_REVIEW_ROUNDS:
                # Stage 2: Design
                logger.info(f"Executing Stage 2: Architectural Design (Review Round {review_round})...")
                s2_pass, design_path, s2_msg = execute_stage_2(
                    spec_path,
                    output_dir=self.output_dir,
                    use_architecture_context=self.use_architecture_context
                )
                if not s2_pass:
                    return self._terminate_failure("STAGE_2_DESIGN_FAILED", s2_msg)
                if "Stage 2: Design" not in self.state["stages_completed"]:
                    self.state["stages_completed"].append("Stage 2: Design")

                # Stage 3 + 4: Implementation and Test Remediation Loop
                test_passed = False
                error_trace = None
                while self.state["test_retry_count"] < MAX_TEST_RETRIES:
                    logger.info(f"Executing Stage 3: Implementation (Attempt {self.state['test_retry_count'] + 1})...")
                    s3_pass, patch_path, s3_msg = execute_stage_3(
                        design_path,
                        self.branch_name,
                        output_dir=self.output_dir,
                        workspace_root=self.workspace_root,
                        error_feedback=error_trace
                    )
                    if not s3_pass:
                        return self._terminate_failure("STAGE_3_BUILD_FAILED", s3_msg)
                    if "Stage 3: Implementation" not in self.state["stages_completed"]:
                        self.state["stages_completed"].append("Stage 3: Implementation")

                    # Stage 4: Testing
                    logger.info("Executing Stage 4: Testing & Verification...")
                    s4_pass, report_path, s4_msg, error_trace = execute_stage_4(
                        spec_path,
                        output_dir=self.output_dir,
                        workspace_root=self.workspace_root
                    )

                    if s4_pass:
                        test_passed = True
                        if "Stage 4: Testing" not in self.state["stages_completed"]:
                            self.state["stages_completed"].append("Stage 4: Testing")
                        break
                    else:
                        self.state["test_retry_count"] += 1
                        logger.warning(f"Tests failed (attempt {self.state['test_retry_count']}): {s4_msg}. Retrying...")

                if not test_passed:
                    return self._terminate_failure("STAGE_4_TESTS_EXHAUSTED", "Max test retries exhausted without pass.")

                # Stage 5: Release (PR creation)
                logger.info("Executing Stage 5: Release Management...")
                s5_pass, pr_path, s5_msg, pr_url = execute_stage_5(
                    self.issue_id,
                    self.issue_title,
                    self.branch_name,
                    output_dir=self.output_dir,
                    workspace_root=self.workspace_root,
                    push_to_remote=self.push_to_remote
                )
                if not s5_pass:
                    return self._terminate_failure("STAGE_5_RELEASE_FAILED", s5_msg)
                if "Stage 5: Release" not in self.state["stages_completed"]:
                    self.state["stages_completed"].append("Stage 5: Release")

                # Stage 6: Independent Adversarial Review
                logger.info(f"Executing Stage 6: Independent Review (Round {review_round + 1})...")
                diff_text = patch_path.read_text(encoding="utf-8") if patch_path.exists() else ""
                test_output = report_path.read_text(encoding="utf-8") if report_path.exists() else ""

                is_approved, review_path, s6_msg, verdict_data = execute_stage_6(
                    self.issue_title,
                    self.issue_body,
                    diff_text,
                    test_output,
                    output_dir=self.output_dir
                )

                self.state["final_verdict"] = verdict_data
                if "Stage 6: Review" not in self.state["stages_completed"]:
                    self.state["stages_completed"].append("Stage 6: Review")

                if is_approved:
                    logger.info("Reviewer Approved Pull Request!")
                    break
                else:
                    review_round += 1
                    self.state["review_round_count"] = review_round
                    category = verdict_data.get("category", "CODE_ISSUE")
                    logger.warning(f"Reviewer requested changes [{category}]: {verdict_data.get('summary')}")

                    if review_round >= MAX_REVIEW_ROUNDS:
                        logger.info("Maximum review rounds reached. Escalating to human maintainer.")
                        break

            # Completed successfully -> hand over to Human Maintainer
            self.state["status"] = "PENDING_HUMAN_MERGE"
            self.state["elapsed_seconds"] = round(time.time() - start_time, 2)
            self.state["tokens_used"] = global_tracker.total_tokens_used
            self._save_state()

            logger.info("::endgroup::AutoSE SDLC Workflow Completed Successfully.")
            return self.state

        except Exception as e:
            logger.exception(f"Unhandled error in workflow: {e}")
            return self._terminate_failure("CRASH", str(e))

    def _terminate_failure(self, error_code: str, reason: str) -> Dict[str, Any]:
        self.state["status"] = "FAILED"
        self.state["error_code"] = error_code
        self.state["error_reason"] = reason
        self.state["tokens_used"] = global_tracker.total_tokens_used
        self._save_state()
        logger.error(f"::endgroup::AutoSE Workflow Aborted: {error_code} - {reason}")
        return self.state

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="AutoSE Agentic SDLC State Machine Orchestrator")
    parser.add_argument("--issue-id", type=int, default=42, help="Issue number")
    parser.add_argument("--issue-file", type=str, required=True, help="Path to markdown issue file")
    parser.add_argument("--no-arch", action="store_true", help="Disable ARCHITECTURE.md grounding (for ADR-002 experiment)")
    parser.add_argument("--push", action="store_true", help="Enable git push and PR creation")

    args = parser.parse_args()
    issue_path = Path(args.issue_file)
    content = issue_path.read_text(encoding="utf-8")

    lines = content.strip().splitlines()
    title = lines[0].replace("#", "").strip()
    body = "\n".join(lines[1:]).strip()

    orchestrator = SDLCWorkflowOrchestrator(
        issue_id=args.issue_id,
        issue_title=title,
        issue_body=body,
        use_architecture_context=(not args.no_arch),
        push_to_remote=args.push
    )

    result = orchestrator.run()
    print("\nWorkflow Final Summary State:")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PENDING_HUMAN_MERGE" else 1)


if __name__ == "__main__":
    main()
