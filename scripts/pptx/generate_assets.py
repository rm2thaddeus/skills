import argparse
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import shutil


from typing import Optional


def find_latest_op(artifacts_root: Path) -> Optional[Path]:
    ops = [p for p in artifacts_root.glob("*/") if p.is_dir()]
    if not ops:
        return None
    return sorted(ops, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def draw_persona_banner(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
    ax.set_facecolor("#2c2c2c")
    fig.patch.set_facecolor("#2c2c2c")
    ax.axis("off")

    # Boxes: Scientist → LLM Architect
    def pill(xy, w, h, color, text, txt_color="#ffffff"):
        x, y = xy
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=12",
                             facecolor=color, edgecolor="#aab7b8")
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=txt_color, fontsize=16)

    pill((0.8, 0.35), 3.6, 1.1, "#202020", "Scientifique (chimie → données)")
    pill((4.7, 0.35), 3.6, 1.1, "#4c78a8", "Architecte de workflows LLM")

    # Arrow
    arr = FancyArrowPatch((4.4, 0.9), (4.7, 0.9), arrowstyle='-|>', color="#f58518", linewidth=3)
    ax.add_patch(arr)

    ax.text(0.8, 0.2, "Je suis un scientifique tombé dans l’IA générative —\n\nJ’ai transféré ma rigueur expérimentale vers la conception de systèmes.",
            color="#f4f6f6", fontsize=12, ha="left", va="center")

    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 2)
    plt.tight_layout()
    fig.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def draw_mindmap(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    ax.set_facecolor("#2c2c2c")
    fig.patch.set_facecolor("#2c2c2c")
    ax.axis('off')

    # Center node
    center = (0.5, 0.55)
    ax.add_patch(Circle(center, 0.08, color="#f58518"))
    ax.text(*center, "Système\nde candidatures\nassisté par IA", color="#ffffff", fontsize=12, ha="center", va="center")

    nodes = [
        (0.18, 0.8, "Collecte\n& normalisation\ndonnées"),
        (0.82, 0.78, "Génération\nCV / lettre\n(personnalisée)"),
        (0.18, 0.3, "Automatisation\ndépôts / suivi"),
        (0.82, 0.3, "Analytique\n& tableaux de bord"),
        (0.5, 0.18, "Boucle\nde feedback"),
        (0.5, 0.92, "Portfolio\n+ preuves")
    ]

    for (x, y, label) in nodes:
        box = FancyBboxPatch((x-0.12, y-0.05), 0.24, 0.10, boxstyle="round,pad=0.02,rounding_size=8",
                             facecolor="#202020", edgecolor="#aab7b8")
        ax.add_patch(box)
        ax.text(x, y, label, color="#f4f6f6", fontsize=10, ha="center", va="center")
        # edge
        ax.plot([center[0], x], [center[1], y], color="#aab7b8", linewidth=1.5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    fig.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Generate visual assets for PPTX")
    p.add_argument("--artifacts-root", default="artifacts/operations")
    args = p.parse_args()

    artifacts_root = Path(args.artifacts_root)
    op = find_latest_op(artifacts_root)
    if not op:
        print("No op dir found")
        return
    assets_dir = ensure_dir(op / "output" / "assets")

    persona = assets_dir / "persona_banner.png"
    mindmap = assets_dir / "mindmap_system.png"

    draw_persona_banner(persona)
    draw_mindmap(mindmap)

    # Also place copies alongside HTML slides for robust relative linking
    slides_dir = op / "html" / "slides"
    try:
        if slides_dir.exists():
            shutil.copyfile(persona, slides_dir / "persona_banner.png")
            shutil.copyfile(mindmap, slides_dir / "mindmap_system.png")
    except Exception:
        pass

    print({
        "operation_id": op.name,
        "assets": {
            "persona_banner": str(persona),
            "mindmap_system": str(mindmap),
        }
    })


if __name__ == "__main__":
    main()


