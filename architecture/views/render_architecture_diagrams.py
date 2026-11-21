"""Render publication-grade architecture diagram images for inclusion in report.docx and report.pdf."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

VIEWS_DIR = Path(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3\architecture\views")


def render_component_view():
    fig, ax = plt.subplots(figsize=(12.4, 8.8), dpi=300)
    ax.set_xlim(0, 1240)
    ax.set_ylim(0, 880)
    ax.axis("off")

    # Header Title & Subtitle
    ax.text(40, 842, "AutoSE SDLC Workflow: Component Architecture View", fontsize=15, fontweight="bold", color="#0f172a")
    ax.text(40, 820, "Decoupled 6-Stage Agentic Pipeline · Sandboxed Adversarial Reviewer · Sovereign Human Governance", fontsize=9.5, color="#64748b")

    # Header Metadata Badges
    pills = [
        (770, 818, 135, "TinyDB edff96a", "#0284c7", "#f8fafc", "#e2e8f0"),
        (915, 818, 145, "10 Nygard ADRs", "#16a34a", "#f8fafc", "#e2e8f0"),
        (1070, 818, 130, "Gemini 3.5 / 3.8", "#2563eb", "#eff6ff", "#bfdbfe"),
    ]
    for px, py, pw, ptext, pdot, pbg, pborder in pills:
        pill = patches.FancyBboxPatch((px, py), pw, 26, boxstyle="round,pad=2,rounding_size=13",
                                      facecolor=pbg, edgecolor=pborder, linewidth=1)
        ax.add_patch(pill)
        ax.plot([px + 14], [py + 13], marker="o", markersize=5, color=pdot)
        ax.text(px + (pw / 2) + 6, py + 13, ptext, fontsize=8.5, fontweight="bold", ha="center", va="center", color="#334155")

    # External Trigger Container (y_mpl: 726..798)
    ext_rect = patches.FancyBboxPatch((40, 726), 1160, 72, boxstyle="round,pad=4,rounding_size=8",
                                      facecolor="#f8fafc", edgecolor="#e2e8f0", linewidth=1.2)
    ax.add_patch(ext_rect)
    ax.text(56, 781, "EXTERNAL ENVIRONMENT & GITHUB PLATFORM TRIGGERS", fontsize=8.5, fontweight="bold", color="#64748b")

    # Trigger Cards
    t_cards = [
        (56, 738, 360, "Issue Labeled (autose)", "issues: [labeled]", "#2563eb"),
        (440, 738, 360, "Comment Trigger (/autose)", "issue_comment", "#2563eb"),
        (824, 738, 360, "GitHub Secrets & Context", "GEMINI_API_KEY", "#475569"),
    ]
    for tx, ty, tw, ttitle, ttag, tdot in t_cards:
        tbox = patches.FancyBboxPatch((tx, ty), tw, 36, boxstyle="round,pad=3,rounding_size=6",
                                      facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.2)
        ax.add_patch(tbox)
        ax.plot([tx + 18], [ty + 18], marker="o", markersize=5, color=tdot)
        ax.text(tx + 30, ty + 18, ttitle, fontsize=8.5, fontweight="bold", va="center", color="#1e293b")
        t_pill = patches.FancyBboxPatch((tx + tw - 120, ty + 8), 110, 20, boxstyle="round,pad=2,rounding_size=4",
                                        facecolor="#f1f5f9", edgecolor="#e2e8f0", linewidth=0.8)
        ax.add_patch(t_pill)
        ax.text(tx + tw - 65, ty + 18, ttag, fontsize=7.5, ha="center", va="center", color="#475569")

    # Trigger Bus Arrow
    ax.annotate("", xy=(370, 664), xytext=(370, 726),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))

    # Main Left Container: Autonomous SDLC Pipeline (y_mpl: 78..708)
    pipe_rect = patches.FancyBboxPatch((40, 78), 630, 630, boxstyle="round,pad=5,rounding_size=8",
                                       facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.2)
    ax.add_patch(pipe_rect)
    ax.text(60, 689, "AUTONOMOUS SDLC PIPELINE (ORCHESTRATOR STATE MACHINE)", fontsize=9.5, fontweight="bold", color="#0f172a")

    p_badge = patches.FancyBboxPatch((480, 680), 175, 20, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#f1f5f9", edgecolor="#e2e8f0", linewidth=0.8)
    ax.add_patch(p_badge)
    ax.text(567, 690, "Deterministic State Machine", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#475569")

    # Main Right Container: Isolated Reviewer Enclave (y_mpl: 78..708)
    rev_rect = patches.FancyBboxPatch((700, 78), 500, 630, boxstyle="round,pad=5,rounding_size=8",
                                      facecolor="#f8fafc", edgecolor="#0284c7", linewidth=1.2, linestyle="dashed")
    ax.add_patch(rev_rect)
    ax.text(720, 689, "ISOLATED REVIEWER ENCLAVE & HUMAN GOVERNANCE", fontsize=9.5, fontweight="bold", color="#0369a1")

    r_badge = patches.FancyBboxPatch((1055, 680), 130, 20, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#e0f2fe", edgecolor="#bae6fd", linewidth=0.8)
    ax.add_patch(r_badge)
    ax.text(1120, 690, "Zero-Trust Sandbox", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#0369a1")

    # Stages 1 to 5 inside Left Container
    stages = [
        {"y": 576, "name": "Stage 1: Requirements Engineering Agent", "model": "gemini-3.5-flash-lite",
         "role": "Synthesizes Acceptance Criteria", "sub": "Functional boundary extraction", "inv": "Uncertainty Register triangulation",
         "tool": "Tools: Issue Parser, Gherkin", "inp": "Input: Issue title, body, author", "fmt": "Format: Given / When / Then",
         "art": "Artifact: spec.md", "gate": "Gate 1: ACs Testable ✓"},
        {"y": 456, "name": "Stage 2: Architectural Design Agent", "model": "gemini-3.5-flash",
         "role": "Architecture Grounding (ADR-002)", "sub": "Enforces TinyDB 3 ADRs & 5 rules", "inv": "Prevents circular query-storage deps",
         "tool": "Context: ARCHITECTURE.md", "inp": "Input: spec.md + AST Symbol Tree", "fmt": "Specifies target files & signatures",
         "art": "Artifact: design.md", "gate": "Gate 2: Files & APIs Verified ✓"},
        {"y": 336, "name": "Stage 3: Code Implementation Agent", "model": "gemini-3.5-flash",
         "role": "Direct Source Code Modification", "sub": "Branch: autose/issue-<id>", "inv": "Generates minimal unified diff",
         "tool": "Tools: Edit/Write File, Git", "inp": "Input: design.md + Codebase files", "fmt": "Syntax: py_compile validator",
         "art": "Artifact: diff.patch", "gate": "Gate 3: Build & Syntax Pass ✓"},
        {"y": 216, "name": "Stage 4: Testing & Verification Agent", "model": "gemini-3.5-flash-lite",
         "role": "Test Synthesis & Suite Execution", "sub": "228 baseline regression tests", "inv": "+ 3 acceptance tests authored",
         "tool": "Tools: Pytest Execution Runner", "inp": "Input: spec.md + Patched Tree", "fmt": "Captures trace on assertion fail",
         "art": "Artifact: test_report.md", "gate": "Gate 4: 228 Base + New Pass ✓"},
        {"y": 96, "name": "Stage 5: Release & PR Management Agent", "model": "Actions Runner / gh CLI",
         "role": "Git Branch Push & PR Creation", "sub": "Structured changelog formatting", "inv": "Links issue, spec, and test runs",
         "tool": "Tools: git commit, push, gh pr", "inp": "Input: Feature branch & reports", "fmt": "CI: Triggers Python CI suite",
         "art": "Artifact: pr.md + PR #43", "gate": "Gate 5: Branch & PR Live ✓"},
    ]

    for s in stages:
        sy = s["y"]
        sbox = patches.FancyBboxPatch((90, sy), 560, 88, boxstyle="round,pad=3,rounding_size=6",
                                      facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2)
        ax.add_patch(sbox)
        # Header strip
        shead = patches.Rectangle((90, sy + 64), 560, 24, facecolor="#f1f5f9")
        ax.add_patch(shead)
        ax.plot([90, 650], [sy + 64, sy + 64], color="#cbd5e1", linewidth=1)
        ax.text(102, sy + 76, s["name"], fontsize=8.5, fontweight="bold", va="center", color="#1e293b")

        # Model pill
        mpill = patches.FancyBboxPatch((510, sy + 67), 135, 18, boxstyle="round,pad=2,rounding_size=4",
                                       facecolor="#ffffff", edgecolor="#e2e8f0", linewidth=0.8)
        ax.add_patch(mpill)
        ax.text(577, sy + 76, s["model"], fontsize=7.5, fontweight="bold", ha="center", va="center", color="#475569")

        # Col 1: Role
        ax.text(102, sy + 48, s["role"], fontsize=7.5, fontweight="bold", color="#334155")
        ax.text(102, sy + 32, s["sub"], fontsize=7.2, color="#64748b")
        ax.text(102, sy + 16, s["inv"], fontsize=7, color="#94a3b8")
        ax.plot([250, 250], [sy + 10, sy + 58], color="#e2e8f0", linewidth=1)

        # Col 2: Tools
        ax.text(262, sy + 48, s["tool"], fontsize=7.5, fontweight="bold", color="#334155")
        ax.text(262, sy + 32, s["inp"], fontsize=7.2, color="#64748b")
        ax.text(262, sy + 16, s["fmt"], fontsize=7, color="#94a3b8")
        ax.plot([430, 430], [sy + 10, sy + 58], color="#e2e8f0", linewidth=1)

        # Col 3: Artifact & Gate
        ax.text(442, sy + 46, s["art"], fontsize=8.2, fontweight="bold", color="#0284c7")
        gbadge = patches.FancyBboxPatch((442, sy + 12), 195, 24, boxstyle="round,pad=2,rounding_size=4",
                                        facecolor="#f0fdf4", edgecolor="#bbf7d0", linewidth=1)
        ax.add_patch(gbadge)
        ax.text(539, sy + 24, s["gate"], fontsize=7.5, fontweight="bold", ha="center", va="center", color="#15803d")

    # Inter-stage vertical arrows (downward)
    ax.annotate("", xy=(370, 544), xytext=(370, 576), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    ax.annotate("", xy=(370, 424), xytext=(370, 456), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    ax.annotate("", xy=(370, 304), xytext=(370, 336), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    ax.annotate("", xy=(370, 184), xytext=(370, 216), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))

    # Left Rail: Test Failure Repair Loop (Stage 4 -> Stage 3)
    ax.annotate("", xy=(90, 380), xytext=(62, 380),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5))
    ax.plot([90, 62, 62], [260, 260, 380], color="#d97706", linewidth=1.5, linestyle="dashed")
    t_retry_box = patches.FancyBboxPatch((42, 300), 38, 40, boxstyle="round,pad=2,rounding_size=3",
                                         facecolor="#ffffff", edgecolor="#fde68a", linewidth=1)
    ax.add_patch(t_retry_box)
    ax.text(61, 328, "TEST", fontsize=6.8, fontweight="bold", ha="center", color="#b45309")
    ax.text(61, 318, "RETRY", fontsize=6.8, fontweight="bold", ha="center", color="#b45309")
    ax.text(61, 308, "(≤ 3)", fontsize=6.5, ha="center", color="#d97706")

    # Right Container Components:
    # 1. Isolation Security Banner (y_mpl: 616..664)
    sec_rect = patches.FancyBboxPatch((720, 616), 460, 48, boxstyle="round,pad=3,rounding_size=6",
                                      facecolor="#eff6ff", edgecolor="#bfdbfe", linewidth=1.2)
    ax.add_patch(sec_rect)
    sec_pill = patches.FancyBboxPatch((732, 638), 160, 18, boxstyle="round,pad=2,rounding_size=4",
                                      facecolor="#dbeafe", edgecolor="#bfdbfe", linewidth=0.8)
    ax.add_patch(sec_pill)
    ax.text(812, 647, "ADR-008 CONTEXT ISOLATION", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#1e40af")
    ax.text(732, 626, "Zero implementer memory · No transcript / chain-of-thought leak · Read-only files", fontsize=7.2, color="#1e40af")

    # 2. Stage 6 Reviewer Agent Card (y_mpl: 326..606, h=280)
    rev_box = patches.FancyBboxPatch((720, 326), 460, 280, boxstyle="round,pad=3,rounding_size=6",
                                     facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.5)
    ax.add_patch(rev_box)
    rhead = patches.Rectangle((720, 582), 460, 24, facecolor="#e0f2fe")
    ax.add_patch(rhead)
    ax.plot([720, 1180], [582, 582], color="#bae6fd", linewidth=1)
    ax.text(732, 594, "Stage 6: Independent Reviewer Agent (Sandboxed)", fontsize=8.5, fontweight="bold", va="center", color="#0369a1")

    rm_pill = patches.FancyBboxPatch((1030, 585), 140, 18, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#ffffff", edgecolor="#bae6fd", linewidth=0.8)
    ax.add_patch(rm_pill)
    ax.text(1100, 594, "gemini-3.5-flash (T=0.0)", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#0369a1")

    ax.text(732, 565, "Inputs: Issue Context + Git Diff (origin/main...HEAD) + Read-Only Repo", fontsize=7.2, fontweight="bold", color="#334155")
    ax.text(732, 550, "Security Invariant: Forbidden from git push, branch mutation, or merge", fontsize=7.2, fontweight="bold", color="#dc2626")
    ax.text(732, 535, "Delivered Artifact: review.md (Formal Verification Audit)", fontsize=7.5, fontweight="bold", color="#0284c7")
    ax.plot([732, 1168], [526, 526], color="#e2e8f0", linewidth=1)

    ax.text(732, 514, "TYPED VERDICT ROUTING & FEEDBACK GATES", fontsize=7.5, fontweight="bold", color="#475569")

    # Verdict 1: Approach Issue (y_mpl: 454..500)
    v1_box = patches.FancyBboxPatch((732, 454), 436, 46, boxstyle="round,pad=2,rounding_size=4",
                                    facecolor="#fef3c7", edgecolor="#fde68a", linewidth=1)
    ax.add_patch(v1_box)
    ax.text(744, 484, "REQUEST_CHANGES [APPROACH_ISSUE]", fontsize=7.5, fontweight="bold", color="#b45309")
    ax.text(744, 466, "Violates ARCHITECTURE.md constraints -> Routes to Stage 2 (Max 2 rounds)", fontsize=7, color="#92400e")

    # Verdict 2: Code Issue (y_mpl: 402..448)
    v2_box = patches.FancyBboxPatch((732, 402), 436, 46, boxstyle="round,pad=2,rounding_size=4",
                                    facecolor="#ffedd5", edgecolor="#fed7aa", linewidth=1)
    ax.add_patch(v2_box)
    ax.text(744, 432, "REQUEST_CHANGES [CODE_ISSUE]", fontsize=7.5, fontweight="bold", color="#c2410c")
    ax.text(744, 414, "Syntax / logic bug, missing guard -> Routes to Stage 3 (Max 2 rounds)", fontsize=7, color="#9a3412")

    # Verdict 3: Approve (y_mpl: 350..396)
    v3_box = patches.FancyBboxPatch((732, 350), 436, 46, boxstyle="round,pad=2,rounding_size=4",
                                    facecolor="#dcfce7", edgecolor="#bbf7d0", linewidth=1)
    ax.add_patch(v3_box)
    ax.text(744, 380, "APPROVE", fontsize=7.5, fontweight="bold", color="#15803d")
    ax.text(744, 362, "100% verified -> Escalates to Human Maintainer for final merge decision", fontsize=7, color="#166534")

    # 3. Human Maintainer Sovereign Gate (y_mpl: 96..306, h=210)
    hum_box = patches.FancyBboxPatch((720, 96), 460, 210, boxstyle="round,pad=3,rounding_size=6",
                                     facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=1.5)
    ax.add_patch(hum_box)
    hhead = patches.Rectangle((720, 280), 460, 26, facecolor="#dcfce7")
    ax.add_patch(hhead)
    ax.plot([720, 1180], [280, 280], color="#bbf7d0", linewidth=1)
    ax.text(732, 293, "Human Maintainer Sovereign Gate (Final Authority)", fontsize=8.5, fontweight="bold", va="center", color="#15803d")

    hm_pill = patches.FancyBboxPatch((1035, 284), 135, 18, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#ffffff", edgecolor="#bbf7d0", linewidth=0.8)
    ax.add_patch(hm_pill)
    ax.text(1102, 293, "Autonomous Merge Banned", fontsize=7.2, fontweight="bold", ha="center", va="center", color="#15803d")

    ax.text(732, 264, "Complete Audit Package: spec.md, design.md, test_report.md, review.md", fontsize=7.2, fontweight="bold", color="#1e293b")
    ax.text(732, 248, "Sovereignty Invariant: Automated merge strictly prohibited (ADR-002, ADR-010)", fontsize=7.2, color="#475569")
    ax.text(732, 232, "Human maintainer retains exclusive right to approve PR and trigger release", fontsize=7.2, color="#475569")

    # Console Mockup
    con_box = patches.FancyBboxPatch((732, 108), 436, 110, boxstyle="round,pad=3,rounding_size=6",
                                     facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1)
    ax.add_patch(con_box)
    ax.text(746, 202, "Pull Request #43 · Maintainer Review Console", fontsize=8, fontweight="bold", color="#0f172a")
    ax.text(746, 186, "Reviewer Verdict: APPROVED (0 defects) · Test Suite: 228 baseline + 3 new tests passing", fontsize=7, color="#64748b")
    ax.text(746, 172, "Branch: autose/issue-42 -> main · CI Status: 18/18 Matrix Jobs Passed ✓", fontsize=7, color="#64748b")

    # Buttons
    b1 = patches.FancyBboxPatch((746, 122), 165, 30, boxstyle="round,pad=2,rounding_size=4", facecolor="#15803d", edgecolor="#15803d")
    ax.add_patch(b1)
    ax.text(828, 137, "Merge Pull Request", fontsize=7.8, fontweight="bold", ha="center", va="center", color="#ffffff")

    b2 = patches.FancyBboxPatch((920, 122), 130, 30, boxstyle="round,pad=2,rounding_size=4", facecolor="#f8fafc", edgecolor="#cbd5e1")
    ax.add_patch(b2)
    ax.text(985, 137, "Request Changes", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#334155")

    b3 = patches.FancyBboxPatch((1060, 122), 95, 30, boxstyle="round,pad=2,rounding_size=4", facecolor="#fef2f2", edgecolor="#fecaca")
    ax.add_patch(b3)
    ax.text(1107, 137, "Close PR", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#dc2626")

    # Connectors between Left and Right:
    # Stage 5 to Stage 6 (PR Handoff)
    ax.plot([650, 675, 675, 720], [140, 140, 560, 560], color="#0284c7", linewidth=2)
    ax.annotate("", xy=(720, 560), xytext=(710, 560), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2))
    pr_pill = patches.FancyBboxPatch((635, 335), 80, 22, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.2)
    ax.add_patch(pr_pill)
    ax.text(675, 346, "PR + DIFF", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#0284c7")

    # Approach Issue feedback: Stage 6 -> Stage 2
    ax.plot([732, 688, 688, 650], [477, 477, 500, 500], color="#b45309", linewidth=1.5, linestyle="dashed")
    ax.annotate("", xy=(650, 500), xytext=(660, 500), arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.5))
    s2_pill = patches.FancyBboxPatch((658, 482), 48, 16, boxstyle="round,pad=2,rounding_size=3", facecolor="#ffffff", edgecolor="#fde68a")
    ax.add_patch(s2_pill)
    ax.text(682, 490, "S2 LOOP", fontsize=6.5, fontweight="bold", ha="center", va="center", color="#b45309")

    # Code Issue feedback: Stage 6 -> Stage 3
    ax.plot([732, 688, 688, 650], [425, 425, 380, 380], color="#c2410c", linewidth=1.5, linestyle="dashed")
    ax.annotate("", xy=(650, 380), xytext=(660, 380), arrowprops=dict(arrowstyle="->", color="#c2410c", lw=1.5))
    s3_pill = patches.FancyBboxPatch((658, 395), 48, 16, boxstyle="round,pad=2,rounding_size=3", facecolor="#ffffff", edgecolor="#fed7aa")
    ax.add_patch(s3_pill)
    ax.text(682, 403, "S3 LOOP", fontsize=6.5, fontweight="bold", ha="center", va="center", color="#c2410c")

    # Reviewer approval: Stage 6 -> Human Maintainer
    ax.annotate("", xy=(950, 306), xytext=(950, 326), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2))
    app_pill = patches.FancyBboxPatch((885, 308), 130, 18, boxstyle="round,pad=2,rounding_size=4",
                                      facecolor="#ffffff", edgecolor="#16a34a", linewidth=1)
    ax.add_patch(app_pill)
    ax.text(950, 317, "APPROVED / ESCALATED", fontsize=7.2, fontweight="bold", ha="center", va="center", color="#16a34a")

    # Footer Legend (y_mpl: 16..62)
    leg_rect = patches.FancyBboxPatch((40, 16), 1160, 46, boxstyle="round,pad=3,rounding_size=6",
                                      facecolor="#f8fafc", edgecolor="#e2e8f0", linewidth=1)
    ax.add_patch(leg_rect)

    ax.annotate("", xy=(90, 39), xytext=(60, 39), arrowprops=dict(arrowstyle="->", color="#475569", lw=2))
    ax.text(98, 39, "Sequential Stage Hand-off", fontsize=8, fontweight="bold", va="center", color="#334155")

    ax.annotate("", xy=(310, 39), xytext=(280, 39), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5, linestyle="dashed"))
    ax.text(318, 39, "Self-Repair / Feedback Loop", fontsize=8, fontweight="bold", va="center", color="#b45309")

    ax.annotate("", xy=(550, 39), xytext=(520, 39), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2))
    ax.text(558, 39, "Sandboxed PR Hand-off", fontsize=8, fontweight="bold", va="center", color="#0284c7")

    ax.annotate("", xy=(770, 39), xytext=(740, 39), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2))
    ax.text(778, 39, "Sovereign Merge Escalation", fontsize=8, fontweight="bold", va="center", color="#15803d")

    adr_box = patches.FancyBboxPatch((970, 26), 215, 26, boxstyle="round,pad=2,rounding_size=4",
                                     facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=0.8)
    ax.add_patch(adr_box)
    ax.text(1077, 39, "ADR-002: Autonomous Merge Banned", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#0f172a")

    out_path = VIEWS_DIR / "component_view.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[+] Rendered Component View PNG: {out_path}")


def render_sequence_view():
    fig, ax = plt.subplots(figsize=(11.5, 9), dpi=300)
    ax.set_xlim(0, 1150)
    ax.set_ylim(0, 900)
    ax.axis("off")

    ax.text(40, 870, "AutoSE SDLC Workflow: Sequence Architecture View", fontsize=16, fontweight="bold", color="#0f172a")
    ax.text(40, 848, "Trace of End-to-End Execution: Trigger, 6 Stages, Pytest Self-Repair Loop, Review Routing, Human Merge", fontsize=9.5, color="#64748b")

    lifelines = [
        {"x": 90, "name": "Maintainer (Human)"},
        {"x": 230, "name": "Orchestrator"},
        {"x": 370, "name": "1. Requirements"},
        {"x": 510, "name": "2. Design"},
        {"x": 650, "name": "3. Implement"},
        {"x": 790, "name": "4. Test"},
        {"x": 930, "name": "5. Release"},
        {"x": 1060, "name": "6. Reviewer (Sandbox)"},
    ]

    for l in lifelines:
        box = patches.FancyBboxPatch((l["x"] - 55, 790), 110, 32, boxstyle="round,pad=3,rounding_size=5", facecolor="#f8fafc", edgecolor="#94a3b8")
        ax.add_patch(box)
        ax.text(l["x"], 806, l["name"], fontsize=8.5, fontweight="bold", ha="center", va="center", color="#1e293b")
        ax.plot([l["x"], l["x"]], [50, 790], color="#cbd5e1", linestyle="dashed", linewidth=1.2)

    # Sequence steps
    steps = [
        {"y": 750, "x1": 90, "x2": 230, "text": "1. Add label 'autose' to Issue #42", "color": "#1e293b"},
        {"y": 710, "x1": 230, "x2": 370, "text": "Dispatch(Issue Title + Body)", "color": "#1e293b"},
        {"y": 660, "x1": 370, "x2": 230, "text": "spec.md [Gate 1: ACs Testable ✓]", "color": "#0284c7"},
        {"y": 620, "x1": 230, "x2": 510, "text": "Dispatch(spec.md + ARCHITECTURE.md)", "color": "#1e293b"},
        {"y": 570, "x1": 510, "x2": 230, "text": "design.md [Gate 2: Files/Signatures Named ✓]", "color": "#0284c7"},
        {"y": 530, "x1": 230, "x2": 650, "text": "Dispatch(design.md, branch 'autose/issue-42')", "color": "#1e293b"},
        {"y": 480, "x1": 650, "x2": 230, "text": "diff.patch [Gate 3: Build & Syntax ✓]", "color": "#0284c7"},
        {"y": 440, "x1": 230, "x2": 790, "text": "Dispatch(diff.patch + spec.md) -> Run Pytest", "color": "#1e293b"},
        {"y": 390, "x1": 790, "x2": 650, "text": "Test Failure Loop (Attempt 1): TypeError trace", "color": "#d97706", "dash": True},
        {"y": 360, "x1": 650, "x2": 790, "text": "Re-patch with defensive type guard", "color": "#475569"},
        {"y": 320, "x1": 790, "x2": 230, "text": "test_report.md [Gate 4: 228 Base + New Pass ✓]", "color": "#0284c7"},
        {"y": 270, "x1": 230, "x2": 930, "text": "Dispatch(Commit, Push & gh pr create)", "color": "#1e293b"},
        {"y": 230, "x1": 930, "x2": 230, "text": "pr.md + PR #43 Opened [Gate 5: CI Green ✓]", "color": "#0284c7"},
        {"y": 190, "x1": 230, "x2": 1060, "text": "Dispatch Reviewer: Diff + Issue only (Zero Memory)", "color": "#0369a1"},
        {"y": 140, "x1": 1060, "x2": 230, "text": "review.md: APPROVE [Gate 6: Verified Safe ✓]", "color": "#166534"},
        {"y": 90, "x1": 230, "x2": 90, "text": "Notify Maintainer: PR Ready -> Human Merges", "color": "#166534"},
    ]

    for s in steps:
        y = s["y"]
        x1, x2 = s["x1"], s["x2"]
        ls = "dashed" if s.get("dash") else "solid"
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=s["color"], lw=1.5, linestyle=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 8, s["text"], fontsize=8, fontweight="bold", color=s["color"], ha="center")

    out_path = VIEWS_DIR / "sequence_view.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[+] Rendered Sequence View PNG: {out_path}")


if __name__ == "__main__":
    render_component_view()
    render_sequence_view()
