import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE


PALETTE = {
    "bg": RGBColor(0x2C, 0x2C, 0x2C),           # charcoal
    "fg": RGBColor(0xF4, 0xF6, 0xF6),           # off-white
    "accent_2022": RGBColor(0x4C, 0x78, 0xA8),  # blue
    "accent_2025": RGBColor(0xF5, 0x85, 0x18),  # orange
    "muted": RGBColor(0xAA, 0xB7, 0xB8),        # silver
}

MARGINS = {
    "left": Inches(0.6),
    "right": Inches(0.6),
    "top": Inches(0.5),
    "bottom": Inches(0.5),
}


def set_slide_background(slide, prs: Presentation) -> None:
    width = prs.slide_width
    height = prs.slide_height
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, width, height
    )
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = PALETTE["bg"]
    shape.line.fill.background()


def add_title_slide(prs: Presentation, title: str, subtitle: Optional[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_slide_background(slide, prs)

    # Accent top bar
    bar_h = Inches(0.7)
    bar = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, bar_h
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = PALETTE["accent_2025"]
    bar.line.fill.background()

    # Title
    tx = slide.shapes.add_textbox(MARGINS["left"], Inches(0.12), prs.slide_width - Inches(1.2), Inches(0.6))
    tf = tx.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = "Arial"
    run.font.size = Pt(34)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    if subtitle:
        subtx = slide.shapes.add_textbox(MARGINS["left"], bar_h + Inches(0.2), prs.slide_width - Inches(1.2), Inches(0.5))
        stf = subtx.text_frame
        stf.clear()
        sp = stf.paragraphs[0]
        srun = sp.add_run()
        srun.text = subtitle
        srun.font.name = "Arial"
        srun.font.size = Pt(18)
        srun.font.color.rgb = PALETTE["fg"]


def add_header(slide, title: str, prs: Presentation) -> None:
    tx = slide.shapes.add_textbox(MARGINS["left"], MARGINS["top"], prs.slide_width - MARGINS["left"] - MARGINS["right"], Inches(0.6))
    tf = tx.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    r.font.name = "Arial"
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = PALETTE["fg"]


def add_bullets_slide(prs: Presentation, title: str, bullets: List[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, prs)
    add_header(slide, title, prs)

    body_y = MARGINS["top"] + Inches(0.75)
    body = slide.shapes.add_textbox(MARGINS["left"], body_y, prs.slide_width - MARGINS["left"] - MARGINS["right"], prs.slide_height - body_y - MARGINS["bottom"]) 
    btf = body.text_frame
    btf.clear()
    for i, item in enumerate(bullets):
        para = btf.add_paragraph() if i > 0 else btf.paragraphs[0]
        para.text = item
        para.font.name = "Arial"
        para.font.size = Pt(18)
        para.font.color.rgb = PALETTE["fg"]
        para.level = 0


def _add_caption(slide, x, y, w, caption: str) -> None:
    cap = slide.shapes.add_textbox(x, y, w, Inches(0.5))
    tf = cap.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = caption
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.color.rgb = PALETTE["muted"]


def _add_scaled_picture(slide, image_path: Path, x, y, max_w, max_h):
    # Try width-fit, then adjust for height if needed
    pic = slide.shapes.add_picture(str(image_path), x, y, width=max_w)
    if pic.height > max_h:
        # Remove and add height-constrained
        pic.element.getparent().remove(pic.element)
        slide.shapes.add_picture(str(image_path), x, y, height=max_h)


def add_image_slide(prs: Presentation, title: str, image_path: Path, caption: Optional[str] = None) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, prs)
    add_header(slide, title, prs)

    y = MARGINS["top"] + Inches(0.75)
    max_w = prs.slide_width - MARGINS["left"] - MARGINS["right"]
    max_h = prs.slide_height - y - MARGINS["bottom"] - (Inches(0.6) if caption else 0)
    if image_path.exists():
        _add_scaled_picture(slide, image_path, MARGINS["left"], y, max_w, max_h)
        if caption:
            _add_caption(slide, MARGINS["left"], prs.slide_height - MARGINS["bottom"] - Inches(0.5), max_w, caption)
    else:
        placeholder = slide.shapes.add_textbox(MARGINS["left"], y, max_w, max_h)
        t = placeholder.text_frame
        t.text = "[Chart missing: " + image_path.name + "]"
        t.paragraphs[0].font.name = "Arial"
        t.paragraphs[0].font.size = Pt(16)
        t.paragraphs[0].font.color.rgb = PALETTE["muted"]


def add_two_images_slide(prs: Presentation, title: str, left: Path, right: Path, left_caption: Optional[str] = None, right_caption: Optional[str] = None) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, prs)
    add_header(slide, title, prs)

    y = MARGINS["top"] + Inches(0.75)
    gap = Inches(0.4)
    col_w = (prs.slide_width - MARGINS["left"] - MARGINS["right"] - gap)
    col_w = col_w / 2
    max_h = prs.slide_height - y - MARGINS["bottom"] - Inches(0.6)

    if left.exists():
        _add_scaled_picture(slide, left, MARGINS["left"], y, col_w, max_h)
        if left_caption:
            _add_caption(slide, MARGINS["left"], prs.slide_height - MARGINS["bottom"] - Inches(0.5), col_w, left_caption)
    if right.exists():
        _add_scaled_picture(slide, right, MARGINS["left"] + col_w + gap, y, col_w, max_h)
        if right_caption:
            _add_caption(slide, MARGINS["left"] + col_w + gap, prs.slide_height - MARGINS["bottom"] - Inches(0.5), col_w, right_caption)


def add_bullets_image_slide(prs: Presentation, title: str, bullets: List[str], image_path: Path) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, prs)
    add_header(slide, title)

    y = MARGINS["top"] + Inches(0.75)
    gap = Inches(0.4)
    col_w = (prs.slide_width - MARGINS["left"] - MARGINS["right"] - gap)
    left_w = col_w * 0.45
    right_w = col_w * 0.55
    max_h = prs.slide_height - y - MARGINS["bottom"]

    # Bullets left
    body = slide.shapes.add_textbox(MARGINS["left"], y, left_w, max_h)
    btf = body.text_frame
    btf.clear()
    for i, item in enumerate(bullets):
        para = btf.add_paragraph() if i > 0 else btf.paragraphs[0]
        para.text = item
        para.font.name = "Arial"
        para.font.size = Pt(16)
        para.font.color.rgb = PALETTE["fg"]
        para.level = 0

    # Image right
    if image_path.exists():
        _add_scaled_picture(slide, image_path, MARGINS["left"] + left_w + gap, y, right_w, max_h)


def build_from_manifest(manifest_path: Path, output_path: Path) -> None:
    data: Dict[str, Any] = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    prs = Presentation()

    assets_root = Path(data.get("assets_root", ""))

    title = data.get("title", "")
    subtitle = data.get("subtitle")
    add_title_slide(prs, title, subtitle)

    for slide in data.get("slides", []):
        layout = slide.get("layout")
        stitle = slide.get("title", "")
        if layout == "bullets":
            bullets = slide.get("bullets", [])
            add_bullets_slide(prs, stitle, bullets)
        elif layout == "image":
            fname = slide.get("image")
            caption = slide.get("caption")
            add_image_slide(prs, stitle, assets_root / fname, caption)
        elif layout == "image_with_caption":
            fname = slide.get("image")
            caption = slide.get("caption")
            add_image_slide(prs, stitle, assets_root / fname, caption)
        elif layout == "two_images":
            left = assets_root / slide.get("left")
            right = assets_root / slide.get("right")
            add_two_images_slide(prs, stitle, left, right, slide.get("left_caption"), slide.get("right_caption"))
        elif layout == "bullets_image":
            bullets = slide.get("bullets", [])
            fname = slide.get("image")
            add_bullets_image_slide(prs, stitle, bullets, assets_root / fname)
        elif layout == "title":
            add_title_slide(prs, stitle or title, slide.get("subtitle"))
        else:
            add_bullets_slide(prs, stitle or "Slide", slide.get("bullets", []))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build PPTX from manifest")
    parser.add_argument("manifest", type=str)
    parser.add_argument("output", type=str)
    args = parser.parse_args()

    build_from_manifest(Path(args.manifest), Path(args.output))
