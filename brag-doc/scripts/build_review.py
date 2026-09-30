"""Build the designed brag-doc review as a Word file.

Usage:
    python build_review.py review.json "Brag Review - Q3 2026.docx"

Needs python-docx (pip install python-docx). The JSON shape is documented
in check_review.py; run that first.
"""

import json
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

NAVY = RGBColor(0x1F, 0x2A, 0x44)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
GREY = RGBColor(0x5B, 0x64, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
NAVY_HEX, TILE_HEX, RULE_HEX = "1F2A44", "EAF3F3", "0E7C7B"
STATUS_HEX = {"Achieved": "0E7C7B", "On track": "2F6DB5", "At risk": "C77700", "Not started": "8A8F98"}
FONT = "Calibri"
TEXT_WIDTH_CM = 17.0  # A4 width minus 2 cm side margins


def shade(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def no_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tbl_pr.append(borders)


def full_width(table, col_cm, pad_cm=0.0):
    """Fix column widths so every table spans the text width and lines up."""
    table.autofit = False
    tbl_pr = table._tbl.tblPr
    width = OxmlElement("w:tblW")
    width.set(qn("w:w"), str(int(sum(col_cm) * 567)))
    width.set(qn("w:type"), "dxa")
    tbl_pr.append(width)
    ind = OxmlElement("w:tblInd")
    ind.set(qn("w:w"), str(int(pad_cm * 567)))  # Word pulls tables left by the cell padding
    ind.set(qn("w:type"), "dxa")
    tbl_pr.append(ind)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    for row in table.rows:
        for cell, cm in zip(row.cells, col_cm):
            cell.width = Cm(cm)


def cell_margins(cell, cm=0.3):
    tc_pr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(int(cm * 567)))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tc_pr.append(mar)


def rule_under(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), RULE_HEX)
    bdr.append(bottom)
    p_pr.append(bdr)


def run(paragraph, text, size=10.5, bold=False, color=None, italic=False):
    r = paragraph.add_run(text)
    r.font.name = FONT
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color is not None:
        r.font.color.rgb = color
    return r


def para(container, space_after=4):
    p = container.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p


def section_heading(doc, text):
    p = para(doc, space_after=6)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.keep_with_next = True
    run(p, text.upper(), size=11, bold=True, color=TEAL)
    rule_under(p)


def bullet(doc, parts):
    """parts: list of (text, bold) tuples."""
    p = para(doc, space_after=3)
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    run(p, "▪  ", size=9, color=TEAL)
    for text, bold in parts:
        run(p, text, bold=bold, color=NAVY if bold else None)
    return p


def cover(doc, data):
    person, period = data["person"], data["period"]
    table = doc.add_table(rows=1, cols=1)
    no_borders(table)
    full_width(table, [TEXT_WIDTH_CM], 0.6)
    cell = table.rows[0].cells[0]
    shade(cell, NAVY_HEX)
    cell_margins(cell, 0.6)
    p = cell.paragraphs[0]
    run(p, "SELF-ASSESSMENT", size=9, bold=True, color=RGBColor(0x9F, 0xD6, 0xD5))
    p = cell.add_paragraph()
    run(p, period["label"], size=26, bold=True, color=WHITE)
    p = cell.add_paragraph()
    run(p, person["name"], size=13, bold=True, color=WHITE)
    line = " | ".join(x for x in (person.get("title"), f"Manager: {person['manager']}" if person.get("manager") else None) if x)
    if line:
        p = cell.add_paragraph()
        run(p, line, size=10, color=RGBColor(0xD0, 0xD6, 0xE0))
    if period.get("start") and period.get("end"):
        p = cell.add_paragraph()
        run(p, f"{period['start']} to {period['end']}", size=10, color=RGBColor(0xD0, 0xD6, 0xE0))


def kpi_tiles(doc, kpis):
    kpis = kpis[:4]
    if not kpis:
        return
    para(doc, space_after=6)
    table = doc.add_table(rows=1, cols=len(kpis))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    no_borders(table)
    full_width(table, [TEXT_WIDTH_CM / len(kpis)] * len(kpis), 0.35)
    for cell, kpi in zip(table.rows[0].cells, kpis):
        shade(cell, TILE_HEX)
        cell_margins(cell, 0.35)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(p, kpi["value"], size=18, bold=True, color=TEAL)
        p = cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(p, kpi["label"], size=9, color=GREY)


def objective_block(doc, obj):
    p = para(doc, space_after=2)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.keep_with_next = True
    run(p, f"{obj['id']}  ", size=11, bold=True, color=TEAL)
    run(p, obj.get("title", ""), size=11, bold=True, color=NAVY)
    status = obj.get("status")
    if status:
        run(p, f"   ● {status}", size=9, bold=True,
            color=RGBColor.from_string(STATUS_HEX.get(status, "8A8F98")))
    if obj.get("measure"):
        p = para(doc, space_after=4)
        run(p, f"Measure: {obj['measure']}", size=9, italic=True, color=GREY)
    achievements = obj.get("achievements", [])
    if not achievements:
        p = para(doc)
        run(p, "No logged activity in this period.", size=10, italic=True, color=GREY)
    for a in achievements:
        context = " ".join(x.strip().rstrip(".") + "." for x in (a.get("situation"), a.get("task"), a.get("action")) if x)
        parts = [(a["result"].rstrip(".") + ". ", True)]
        if context:
            parts.append((context, False))
        bullet(doc, parts)
        if a.get("stakeholders"):
            p = para(doc, space_after=4)
            p.paragraph_format.left_indent = Cm(0.5)
            run(p, "With: " + ", ".join(a["stakeholders"]), size=9, color=GREY)


def stakeholder_table(doc, stakeholders):
    table = doc.add_table(rows=1, cols=2)
    no_borders(table)
    hdr = table.rows[0].cells
    for cell, label in zip(hdr, ("Stakeholder", "What we worked on")):
        shade(cell, NAVY_HEX)
        cell_margins(cell, 0.2)
        run(cell.paragraphs[0], label, size=9.5, bold=True, color=WHITE)
    for i, s in enumerate(stakeholders):
        row = table.add_row().cells
        for cell in row:
            cell_margins(cell, 0.2)
            if i % 2 == 0:
                shade(cell, TILE_HEX)
        run(row[0].paragraphs[0], s.get("name", ""), size=10, bold=True, color=NAVY)
        run(row[1].paragraphs[0], s.get("work", ""), size=10)
    full_width(table, [5.5, TEXT_WIDTH_CM - 5.5], 0.2)


def references_block(doc, references):
    table = doc.add_table(rows=1, cols=1)
    no_borders(table)
    full_width(table, [TEXT_WIDTH_CM], 0.4)
    cell = table.rows[0].cells[0]
    shade(cell, TILE_HEX)
    cell_margins(cell, 0.4)
    if references:
        first = True
        for ref in references:
            p = cell.paragraphs[0] if first else cell.add_paragraph()
            first = False
            run(p, f"“{ref['quote']}”", size=10.5, italic=True, color=NAVY)
            p = cell.add_paragraph()
            run(p, f"— {ref['from']}", size=9, bold=True, color=TEAL)
    else:
        run(cell.paragraphs[0], "Add stakeholder feedback here: paste a quote or a screenshot.",
            size=10, italic=True, color=GREY)


def build(data, out_path):
    doc = Document()
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)  # A4
        s.top_margin = s.bottom_margin = Cm(1.8)
        s.left_margin = s.right_margin = Cm(2.0)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.5)

    cover(doc, data)
    kpi_tiles(doc, data.get("kpis", []))

    section_heading(doc, "Summary")
    p = para(doc)
    run(p, data["summary"])

    section_heading(doc, "Objectives delivered")
    for obj in data["objectives"]:
        objective_block(doc, obj)

    if data.get("stakeholders"):
        section_heading(doc, "Key stakeholders")
        stakeholder_table(doc, data["stakeholders"])

    if data.get("extra_mile"):
        section_heading(doc, "Beyond my objectives")
        for e in data["extra_mile"]:
            parts = [(e.get("title", "").rstrip(".") + ". ", True)]
            detail = " ".join(x.strip().rstrip(".") + "." for x in (e.get("action"), e.get("result")) if x)
            parts.append((detail, False))
            bullet(doc, parts)

    learning = data.get("learning") or {}
    if learning:
        section_heading(doc, "Learning and growth")
        if learning.get("skills"):
            bullet(doc, [("Skills built: ", True), (", ".join(learning["skills"]), False)])
        if learning.get("development_area"):
            bullet(doc, [("Developing next: ", True), (learning["development_area"], False)])

    section_heading(doc, "Stakeholder feedback")
    references_block(doc, data.get("references", []))

    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(footer, f"{data['person']['name']}  ·  {data['period']['label']} self-assessment", size=8, color=GREY)

    doc.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        build(json.load(f), sys.argv[2])
