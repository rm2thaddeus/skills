from pathlib import Path
from typing import List, Optional
import json
import math

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

ACCENT_2022 = RGBColor(0x4C, 0x78, 0xA8)
ACCENT_2025 = RGBColor(0xF5, 0x85, 0x18)
FG = RGBColor(0xF4, 0xF6, 0xF6)
BG = RGBColor(0x2C, 0x2C, 0x2C)
MUTED = RGBColor(0xAA, 0xB7, 0xB8)


def add_notes(slide, text: str) -> None:
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    if tf.text:
        tf.text = tf.text + "\n" + text
    else:
        tf.text = text


def add_legend(slide, x: Inches, y: Inches) -> None:
    box_w = Inches(3.0)
    box_h = Inches(0.6)
    rect = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, box_w, box_h)
    rect.fill.solid()
    rect.fill.fore_color.rgb = BG
    rect.line.color.rgb = MUTED
    tf = rect.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "  2022   2025"
    run.font.size = Pt(12)
    run.font.color.rgb = FG
    # Color dots using small shapes over the rect
    dot_size = Inches(0.18)
    dot1 = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x + Inches(0.15), y + Inches(0.2), dot_size, dot_size)
    dot1.fill.solid(); dot1.fill.fore_color.rgb = ACCENT_2022; dot1.line.fill.background()
    dot2 = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, x + Inches(1.1), y + Inches(0.2), dot_size, dot_size)
    dot2.fill.solid(); dot2.fill.fore_color.rgb = ACCENT_2025; dot2.line.fill.background()


def _blank_layout(prs: Presentation):
    # Try to find a blank-like layout; fallback to 0
    for i, layout in enumerate(prs.slide_layouts):
        name = getattr(layout, 'name', '').lower()
        if 'blank' in name or 'empty' in name:
            return layout
    return prs.slide_layouts[0]

def add_kpi_slide(prs: Presentation, kpis: dict) -> None:
    slide = prs.slides.add_slide(_blank_layout(prs))
    # background
    rect = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    rect.fill.solid(); rect.fill.fore_color.rgb = BG; rect.line.fill.background()
    # title
    title = slide.shapes.add_textbox(Inches(0.6), Inches(0.5), prs.slide_width - Inches(1.2), Inches(0.6))
    tf = title.text_frame; tf.clear(); p = tf.paragraphs[0]; r = p.add_run(); r.text = "Key Metrics"; r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = FG
    # tiles
    items = [
        ("Total Applications", str(kpis.get("total_applications", "-"))),
        ("Peak Rate (apps/day)", f"{kpis.get('peak_rate', '-')}"),
        ("Median Daily Rate", f"{kpis.get('median_rate', '-')}"),
        ("# Periods", str(kpis.get("num_periods", "-"))),
        ("Top Company Count", str(kpis.get("top_company_count", "-"))),
    ]
    x = Inches(0.6); y = Inches(1.3); w = Inches(4.3); h = Inches(1.2)
    for i, (label, value) in enumerate(items):
        col = i % 2; row = i // 2
        bx = x + col * (w + Inches(0.4))
        by = y + row * (h + Inches(0.3))
        tile = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, bx, by, w, h)
        tile.fill.solid(); tile.fill.fore_color.rgb = RGBColor(0x20, 0x20, 0x20); tile.line.color.rgb = MUTED
        # value
        vtx = slide.shapes.add_textbox(bx + Inches(0.3), by + Inches(0.2), w - Inches(0.6), Inches(0.5))
        vtf = vtx.text_frame; vtf.clear(); vp = vtf.paragraphs[0]; vr = vp.add_run(); vr.text = value; vr.font.size = Pt(24); vr.font.bold = True; vr.font.color.rgb = FG
        # label
        ltx = slide.shapes.add_textbox(bx + Inches(0.3), by + Inches(0.7), w - Inches(0.6), Inches(0.4))
        ltf = ltx.text_frame; ltf.clear(); lp = ltf.paragraphs[0]; lr = lp.add_run(); lr.text = label; lr.font.size = Pt(12); lr.font.color.rgb = MUTED


def add_recruiter_slide(prs: Presentation, recruiters_csv: Path, employers_csv: Path) -> None:
    slide = prs.slides.add_slide(_blank_layout(prs))
    rect = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    rect.fill.solid(); rect.fill.fore_color.rgb = BG; rect.line.fill.background()
    title = slide.shapes.add_textbox(Inches(0.6), Inches(0.5), prs.slide_width - Inches(1.2), Inches(0.6))
    tf = title.text_frame; tf.clear(); p = tf.paragraphs[0]; r = p.add_run(); r.text = "Recruiters vs Employers"; r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = FG
    import csv
    def read_top(path: Path) -> List[List[str]]:
        if not path or not path.exists():
            return []
        rows = []
        with open(path, newline='', encoding='utf-8') as f:
            for i, row in enumerate(csv.DictReader(f)):
                if i >= 10: break
                rows.append([row.get('company', ''), row.get('applications', '')])
        return rows
    left = read_top(recruiters_csv)
    right = read_top(employers_csv)
    # headers
    lh = slide.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(4.0), Inches(0.4))
    lhtf = lh.text_frame; lhtf.clear(); lhp = lhtf.paragraphs[0]; lhr = lhp.add_run(); lhr.text = "Top Recruiters"; lhr.font.size = Pt(16); lhr.font.bold = True; lhr.font.color.rgb = ACCENT_2022
    rh = slide.shapes.add_textbox(Inches(6.0), Inches(1.2), Inches(4.0), Inches(0.4))
    rhtf = rh.text_frame; rhtf.clear(); rhp = rhtf.paragraphs[0]; rhr = rhp.add_run(); rhr.text = "Top Employers"; rhr.font.size = Pt(16); rhr.font.bold = True; rhr.font.color.rgb = ACCENT_2025
    # lists
    def add_list(items: List[List[str]], x: float):
        y = Inches(1.6)
        for name, cnt in items:
            tb = slide.shapes.add_textbox(Inches(x), y, Inches(4.3), Inches(0.3))
            tbf = tb.text_frame; tbf.clear(); tp = tbf.paragraphs[0]; tr = tp.add_run(); tr.text = f"• {name} — {cnt}"; tr.font.size = Pt(12); tr.font.color.rgb = FG
            y = y + Inches(0.35)
    add_list(left, 0.6)
    add_list(right, 6.0)


def compute_kpis(summary_json: Path) -> dict:
    try:
        data = json.loads(summary_json.read_text(encoding='utf-8'))
        total = data.get('total_applications')
        periods = data.get('periods', [])
        peak_rate = max((p.get('applications_per_day', 0) for p in periods), default=None)
        num_periods = len(periods)
        # median rate
        rates = sorted([p.get('applications_per_day', 0) for p in periods])
        median = rates[len(rates)//2] if rates else None
        # top company count
        # try reading applications_by_company.csv count
        artifacts = Path(summary_json).parent
        comp_csv = artifacts / 'applications_by_company.csv'
        top_company_count = 0
        if comp_csv.exists():
            import csv
            with open(comp_csv, newline='', encoding='utf-8') as f:
                for i, _ in enumerate(csv.reader(f)):
                    if i == 0: continue
                    top_company_count += 1
        return {
            'total_applications': total,
            'peak_rate': round(peak_rate, 2) if peak_rate is not None else None,
            'median_rate': round(median, 2) if median is not None else None,
            'num_periods': num_periods,
            'top_company_count': top_company_count,
        }
    except Exception:
        return {}


def enhance(pptx_in: Path, pptx_out: Path, artifacts_dir: Path) -> None:
    prs = Presentation(str(pptx_in))
    # Add notes to each slide with simple insight placeholders
    notes_map = {
        0: "Introduce objective and pre/post LLM framing.",
        1: "Map: explain zoom path and clusters.",
    }
    for idx, slide in enumerate(prs.slides):
        msg = notes_map.get(idx, "Call out key insight and what-to-do-next.")
        add_notes(slide, msg)
    # Add legends to overlay/cumulative/weekday slides if titles exist
    legend_targets = ["Monthly Overlay", "Cumulative", "Weekday"]
    for slide in prs.slides:
        title_texts = []
        for shp in slide.shapes:
            if hasattr(shp, 'text') and shp.text:
                title_texts.append(shp.text)
        if any(any(tk in t for t in title_texts) for tk in legend_targets):
            add_legend(slide, Inches(8.0), Inches(0.6))
    # KPI slide
    kpis = compute_kpis(artifacts_dir / 'summary.json')
    add_kpi_slide(prs, kpis)
    # Recruiter vs employer slide
    recruiters_csv = artifacts_dir / 'top_recruiters.csv'
    employers_csv = artifacts_dir / 'top_employers.csv'
    add_recruiter_slide(prs, recruiters_csv, employers_csv)
    prs.save(str(pptx_out))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--pptx-in', required=True)
    p.add_argument('--pptx-out', required=True)
    p.add_argument('--artifacts-dir', required=True)
    args = p.parse_args()
    enhance(Path(args.pptx_in), Path(args.pptx_out), Path(args.artifacts_dir))
