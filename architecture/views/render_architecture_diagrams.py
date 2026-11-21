"""Render publication-grade architecture diagram images for inclusion in report.docx and report.pdf."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

VIEWS_DIR = Path(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3\architecture\views")


def render_component_view():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 800)
    ax.axis("off")

    # Title
    ax.text(40, 765, "AutoSE SDLC Workflow: Component Architecture View", fontsize=16, fontweight="bold", color="#0f172a")
    ax.text(40, 742, "Decoupled 6-Stage Agentic Pipeline with Sandboxed Independent Reviewer", fontsize=10, color="#64748b")

    # External Trigger Box
    ext_rect = patches.FancyBboxPatch((40, 650), 1020, 70, boxstyle="round,pad=5,rounding_size=8",
                                      facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(ext_rect)
    ax.text(55, 700, "EXTERNAL TRIGGER & GITHUB ENVIRONMENT", fontsize=9, fontweight="bold", color="#64748b")

    # Triggers
    t1 = patches.FancyBboxPatch((60, 660), 220, 32, boxstyle="round,pad=3,rounding_size=5", facecolor="#ffffff", edgecolor="#94a3b8")
    ax.add_patch(t1)
    ax.text(170, 676, "Issue Labeled (autose)", fontsize=9, fontweight="bold", ha="center", va="center", color="#1e293b")

    t2 = patches.FancyBboxPatch((310, 660), 220, 32, boxstyle="round,pad=3,rounding_size=5", facecolor="#ffffff", edgecolor="#94a3b8")
    ax.add_patch(t2)
    ax.text(420, 676, "Comment (/autose)", fontsize=9, fontweight="bold", ha="center", va="center", color="#1e293b")

    t3 = patches.FancyBboxPatch((560, 660), 230, 32, boxstyle="round,pad=3,rounding_size=5", facecolor="#f0fdf4", edgecolor="#86efac")
    ax.add_patch(t3)
    ax.text(675, 676, "Human Maintainer (Merge Gate)", fontsize=9, fontweight="bold", ha="center", va="center", color="#166534")

    t4 = patches.FancyBboxPatch((820, 660), 220, 32, boxstyle="round,pad=3,rounding_size=5", facecolor="#f1f5f9", edgecolor="#cbd5e1")
    ax.add_patch(t4)
    ax.text(930, 676, "Secrets (GEMINI_API_KEY)", fontsize=9, fontweight="bold", ha="center", va="center", color="#334155")

    # Pipeline Container
    pipe_rect = patches.FancyBboxPatch((40, 40), 660, 580, boxstyle="round,pad=5,rounding_size=8",
                                       facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
    ax.add_patch(pipe_rect)
    ax.text(55, 595, "AUTONOMOUS SDLC PIPELINE (ORCHESTRATOR STATE MACHINE)", fontsize=10, fontweight="bold", color="#0f172a")

    # Stages 1 to 5
    stages = [
        {"x": 60, "y": 460, "w": 280, "h": 110, "name": "Stage 1: Requirements Agent", "model": "Gemini 3.5 Flash Lite", "tool": "Issue Parser & Gherkin", "art": "spec.md (Acceptance Criteria)"},
        {"x": 380, "y": 460, "w": 300, "h": 110, "name": "Stage 2: Design Agent", "model": "Gemini 3.5 Flash", "tool": "ARCHITECTURE.md + Symbol Index", "art": "design.md (Target Files/APIs)"},
        {"x": 60, "y": 300, "w": 280, "h": 110, "name": "Stage 3: Implementation Agent", "model": "Gemini 3.5 Flash", "tool": "Edit/Write File, Git Branching", "art": "diff.patch (Builds Cleanly)"},
        {"x": 380, "y": 300, "w": 300, "h": 110, "name": "Stage 4: Testing Agent", "model": "Gemini 3.5 Flash Lite", "tool": "Pytest Runner (228 Baseline + New)", "art": "test_report.md (100% Pass)"},
        {"x": 220, "y": 140, "w": 300, "h": 110, "name": "Stage 5: Release Agent", "model": "Actions Runner / gh CLI", "tool": "git push, gh pr create, CI checks", "art": "pr.md + Live PR URL"},
    ]

    for s in stages:
        box = patches.FancyBboxPatch((s["x"], s["y"]), s["w"], s["h"], boxstyle="round,pad=4,rounding_size=6",
                                     facecolor="#f8fafc", edgecolor="#94a3b8", linewidth=1.2)
        ax.add_patch(box)
        header = patches.Rectangle((s["x"], s["y"] + s["h"] - 26), s["w"], 26, facecolor="#e2e8f0")
        ax.add_patch(header)
        ax.text(s["x"] + 12, s["y"] + s["h"] - 18, s["name"], fontsize=9.5, fontweight="bold", color="#1e293b")
        ax.text(s["x"] + 12, s["y"] + s["h"] - 45, f"Model: {s['model']}", fontsize=8.5, color="#475569")
        ax.text(s["x"] + 12, s["y"] + s["h"] - 65, f"Tools: {s['tool']}", fontsize=8.5, color="#475569")
        ax.text(s["x"] + 12, s["y"] + s["h"] - 90, f"Artifact: {s['art']}", fontsize=8.5, fontweight="bold", color="#0284c7")

    # Arrows in pipeline
    ax.annotate("", xy=(380, 515), xytext=(340, 515), arrowprops=dict(arrowstyle="->", color="#475569", lw=2))
    ax.annotate("", xy=(200, 410), xytext=(530, 460), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=5"))
    ax.annotate("", xy=(380, 355), xytext=(340, 355), arrowprops=dict(arrowstyle="->", color="#475569", lw=2))
    ax.annotate("", xy=(370, 250), xytext=(530, 300), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=5"))

    # Test loop feedback arrow
    ax.annotate("", xy=(340, 375), xytext=(380, 375), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5, linestyle="dashed"))
    ax.text(360, 385, "retry (≤3)", fontsize=8, color="#d97706", fontweight="bold", ha="center")

    # Reviewer Sandbox
    rev_rect = patches.FancyBboxPatch((730, 40), 330, 580, boxstyle="round,pad=5,rounding_size=8",
                                      facecolor="#f0f9ff", edgecolor="#0284c7", linewidth=2, linestyle="dashed")
    ax.add_patch(rev_rect)
    ax.text(745, 595, "ISOLATED REVIEWER SANDBOX (ADR-008)", fontsize=9.5, fontweight="bold", color="#0369a1")

    # Security tag
    sec_tag = patches.FancyBboxPatch((750, 520), 290, 50, boxstyle="round,pad=3,rounding_size=4", facecolor="#ffffff", edgecolor="#bfdbfe")
    ax.add_patch(sec_tag)
    ax.text(895, 550, "Zero Author Reasoning / Scratchpad Memory", fontsize=8.5, fontweight="bold", ha="center", color="#1e40af")
    ax.text(895, 532, "Read-only tools; Forbidden from git push / merge", fontsize=8, ha="center", color="#3b82f6")

    # Reviewer Box
    rbox = patches.FancyBboxPatch((750, 240), 290, 250, boxstyle="round,pad=4,rounding_size=6", facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.5)
    ax.add_patch(rbox)
    rhead = patches.Rectangle((750, 464), 290, 26, facecolor="#bae6fd")
    ax.add_patch(rhead)
    ax.text(762, 482, "Stage 6: Reviewer Agent", fontsize=10, fontweight="bold", color="#0369a1")
    ax.text(762, 442, "Model: Gemini 3.5 Flash (Adversarial)", fontsize=8.5, color="#0f172a")
    ax.text(762, 420, "Inputs: Issue Text, Git Diff, Pytest Log", fontsize=8.5, color="#475569")
    ax.text(762, 398, "Forbidden: git push, branch modification", fontsize=8.5, fontweight="bold", color="#dc2626")
    ax.text(762, 375, "Artifact: review.md", fontsize=8.5, fontweight="bold", color="#0284c7")

    verdict_box = patches.FancyBboxPatch((762, 255), 266, 95, boxstyle="round,pad=3,rounding_size=4", facecolor="#f8fafc", edgecolor="#cbd5e1")
    ax.add_patch(verdict_box)
    ax.text(895, 332, "VERDICT ROUTING:", fontsize=8.5, fontweight="bold", ha="center", color="#1e293b")
    ax.text(895, 312, "APPROVE -> Hand off to Human", fontsize=8, fontweight="bold", ha="center", color="#166534")
    ax.text(895, 292, "REQUEST_CHANGES [CODE_ISSUE] -> Stage 3", fontsize=8, ha="center", color="#d97706")
    ax.text(895, 272, "REQUEST_CHANGES [APPROACH_ISSUE] -> Stage 2", fontsize=8, ha="center", color="#b45309")

    # Connection from Release to Reviewer
    ax.annotate("", xy=(750, 380), xytext=(520, 200), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2, connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(640, 260, "PR & Diff Handoff", fontsize=8.5, fontweight="bold", color="#0284c7")

    # Approved arrow to human
    ax.annotate("", xy=(675, 660), xytext=(895, 240), arrowprops=dict(arrowstyle="->", color="#166534", lw=2, connectionstyle="angle,angleA=-90,angleB=0,rad=10"))
    ax.text(810, 110, "Approved -> Human Merge Authorization", fontsize=9, fontweight="bold", color="#166534")

    out_path = VIEWS_DIR / "component_view.png"
    plt.savefig(out_path, bbox_inches="tight")
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
