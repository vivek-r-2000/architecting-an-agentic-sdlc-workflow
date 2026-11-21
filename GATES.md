# Verification Gates Ledger: AutoSE Assignment 3

## Module M1: Baseline Setup
- ID: M1-G1
- Status: MET
- Description: Clean TinyDB repository initialized at edff96a with 228 passing tests.
- Evidence: 228 passed in 2.88s (uv run pytest tests/).

## Module M2: Architecture Views
- ID: M2-G2
- Status: MET
- Description: Component view, sequence view, and stage map created and validated.
- Evidence: Validated component_view.svg, component_view.png, sequence_view.svg, sequence_view.png, stage_map.md, and ARCHITECTURE.md.

## Module M3: Architectural Decision Records
- ID: M3-G3
- Status: MET
- Description: All 10 ADRs (D1 through D10) authored in Nygard format under architecture/decisions/.
- Evidence: 10/10 ADRs present and verified with Status, Context, Decision, Consequences.

## Module M4: Agentic SDLC Engine
- ID: M4-G4
- Status: MET
- Description: 6-stage workflow engine and GitHub Actions workflow file implemented.
- Evidence: autose_workflow package imports cleanly, 4/4 engine unit tests pass (0.12s), .github/workflows/autose.yml configured.

## Module M5: Test Issues & Hidden Tests
- ID: M5-G5
- Status: MET
- Description: 5 user issues and 15 hidden acceptance tests created.
- Evidence: 15 hidden tests created; fail as expected on unpatched baseline (10 failed, 5 passed).

## Module M6: Seeded Pull Requests
- ID: M6-G6
- Status: MET
- Description: 5 seeded PR diffs with metadata created for reviewer evaluation.
- Evidence: 5 patches and 5 JSON metadata files verified in experiment/seeded_prs/.

## Module M7: Experiments & Results
- ID: M7-G7
- Status: MET
- Description: ADR-002 and ADR-008 experiments executed, results.csv, runs.md, and plots generated.
- Evidence: results.csv complete, runs.md populated, experiment_charts.png saved at 300 DPI.

## Module M8: Research Report
- ID: M8-G8
- Status: MET
- Description: 6-page academic report compiled to report.pdf via Word COM.
- Evidence: report.pdf compiled (796,602 bytes, 6 pages <= 8 pages constraint, zero unrendered math or raw code).

## Module M9: Demo Video & Packaging
- ID: M9-G9
- Status: MET
- Description: demo walkthrough and submission files packaged.
- Evidence: README.md, demo_walkthrough.md, 2019112020_a3_AutoSE.txt, roll_number_a3_AutoSE.txt present.

## Module M10: Submission Review Gate
- ID: M10-G10
- Status: MET
- Description: Standalone GitHub repository created, initial code pushed, CI secrets set, and live issues opened.
- Evidence: Public repository live at https://github.com/vivek-r-2000/architecting-an-agentic-sdlc-workflow. 5 live issues opened, GEMINI_API_KEY secret configured, main branch protection active. Moodle submission pending user approval.
