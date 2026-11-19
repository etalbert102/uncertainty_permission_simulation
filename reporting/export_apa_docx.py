#!/usr/bin/env python3
"""Export the Markdown article as a review-ready APA-style Word manuscript.

This reporting-only utility intentionally lives outside the frozen scientific
``scripts/*.py`` inventory. It does not alter simulation inputs, execution, or
analysis artifacts.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


FONT = "Times New Roman"
RUNNING_HEAD = "INCOMPLETE EVIDENCE TO AUTOMATED ACTION"
TITLE = (
    "From Incomplete Evidence to Automated Action: A Formal Model and Dynamic "
    "Simulation of Review Capacity and Timeout Rules, with a Robodebt Application"
)
AUTHOR = "Eli Talbert"
CORRESPONDENCE_EMAIL = "etalbert102@gmail.com"

FIGURE_ALTS = {
    "figure1_evidence_to_action_protocol.svg": (
        "Evidence-to-action chain linking evidence, representation, permission, "
        "review, execution, and restoration to five process-red-team steps."
    ),
    "figure2_robodebt_process_profiles.svg": (
        "Comparison of early and enhanced Online Compliance Intervention process "
        "profiles in the Robodebt application."
    ),
    "figure3_simulation_results.svg": (
        "Three-panel simulation summary showing fail-closed load response, paired "
        "fail-open versus fail-closed differences, and information-first tradeoffs."
    ),
}

INLINE_PATTERN = re.compile(
    r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[[^\]]+\]\(https?://[^)]+\)|"
    r"<sup>.+?</sup>|https?://[^\s]+)"
)


def set_run_font(run, size: float = 12, *, bold=None, italic=None, name: str = FONT):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_style_font(style, size: float, *, bold=False, italic=False):
    style.font.name = FONT
    style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), FONT)
    style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), FONT)
    style._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FONT)
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)


def add_widow_control(paragraph_format):
    ppr = paragraph_format.element
    if ppr.find(qn("w:widowControl")) is None:
        ppr.append(OxmlElement("w:widowControl"))


def configure_styles(doc: Document):
    styles = doc.styles

    normal = styles["Normal"]
    set_style_font(normal, 12)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    add_widow_control(normal.paragraph_format)

    body = styles.add_style("APA Body", WD_STYLE_TYPE.PARAGRAPH)
    body.base_style = normal
    set_style_font(body, 12)
    body.paragraph_format.first_line_indent = Inches(0.5)
    body.paragraph_format.space_before = Pt(0)
    body.paragraph_format.space_after = Pt(0)
    body.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    add_widow_control(body.paragraph_format)

    abstract = styles.add_style("APA Abstract", WD_STYLE_TYPE.PARAGRAPH)
    abstract.base_style = normal
    set_style_font(abstract, 11)
    abstract.paragraph_format.first_line_indent = Inches(0)
    abstract.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    keyword = styles.add_style("APA Keywords", WD_STYLE_TYPE.PARAGRAPH)
    keyword.base_style = normal
    set_style_font(keyword, 11)
    keyword.paragraph_format.first_line_indent = Inches(0.5)
    keyword.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    h1 = styles["Heading 1"]
    set_style_font(h1, 12, bold=True)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(0)
    h1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    h1.paragraph_format.keep_with_next = True
    h1.paragraph_format.keep_together = True

    h2 = styles["Heading 2"]
    set_style_font(h2, 12, bold=True)
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(0)
    h2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    h2.paragraph_format.keep_with_next = True
    h2.paragraph_format.keep_together = True

    title = styles.add_style("APA Title", WD_STYLE_TYPE.PARAGRAPH)
    title.base_style = normal
    set_style_font(title, 12, bold=True)
    title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    title.paragraph_format.space_before = Pt(42)
    title.paragraph_format.space_after = Pt(0)
    title.paragraph_format.keep_together = True

    author = styles.add_style("APA Author", WD_STYLE_TYPE.PARAGRAPH)
    author.base_style = normal
    set_style_font(author, 12)
    author.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    author.paragraph_format.space_before = Pt(0)
    author.paragraph_format.space_after = Pt(0)
    author.paragraph_format.keep_together = True

    label = styles.add_style("APA Exhibit Label", WD_STYLE_TYPE.PARAGRAPH)
    label.base_style = normal
    set_style_font(label, 12, bold=True)
    label.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    label.paragraph_format.keep_with_next = True
    label.paragraph_format.keep_together = True

    exhibit_title = styles.add_style("APA Exhibit Title", WD_STYLE_TYPE.PARAGRAPH)
    exhibit_title.base_style = normal
    set_style_font(exhibit_title, 12, italic=True)
    exhibit_title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    exhibit_title.paragraph_format.keep_with_next = True
    exhibit_title.paragraph_format.keep_together = True

    note = styles.add_style("APA Exhibit Note", WD_STYLE_TYPE.PARAGRAPH)
    note.base_style = normal
    set_style_font(note, 9)
    note.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    note.paragraph_format.space_before = Pt(4)
    note.paragraph_format.space_after = Pt(4)
    note.paragraph_format.keep_together = True

    reference = styles.add_style("APA Reference", WD_STYLE_TYPE.PARAGRAPH)
    reference.base_style = normal
    set_style_font(reference, 12)
    reference.paragraph_format.left_indent = Inches(0.5)
    reference.paragraph_format.first_line_indent = Inches(-0.5)
    reference.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    table_text = styles.add_style("APA Table Text", WD_STYLE_TYPE.PARAGRAPH)
    table_text.base_style = normal
    set_style_font(table_text, 9)
    table_text.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    table_text.paragraph_format.space_before = Pt(0)
    table_text.paragraph_format.space_after = Pt(0)


def set_cell_margins(cell, top=70, start=90, bottom=70, end=90):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_width(cell, width_inches: float):
    width_dxa = int(width_inches * 1440)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(width_dxa))
    tc_w.set(qn("w:type"), "dxa")
    cell.width = Inches(width_inches)


def set_table_geometry(table, widths):
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    tbl_pr = table._tbl.tblPr

    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    total_dxa = int(sum(widths) * 1440)
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(total_dxa))
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "0")
    tbl_ind.set(qn("w:type"), "dxa")

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(width * 1440)))
        grid.append(col)

    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            set_cell_width(cell, widths[idx])
            set_cell_margins(cell)


def set_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "bottom", "insideH"):
        element = borders.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "6" if edge != "insideH" else "3")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "000000" if edge != "insideH" else "B7B7B7")
    for edge in ("left", "right", "insideV"):
        element = borders.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "nil")


def mark_header_row(row):
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    tr_pr.append(repeat)
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def add_page_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instr, separate, text, end):
        run._r.append(element)
    set_run_font(run, 12)


def set_header(section, content_width: float):
    section.header.is_linked_to_previous = False
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.clear()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    paragraph.paragraph_format.tab_stops.add_tab_stop(
        Inches(content_width), WD_TAB_ALIGNMENT.RIGHT
    )
    run = paragraph.add_run(RUNNING_HEAD)
    set_run_font(run, 12)
    paragraph.add_run("\t")
    add_page_field(paragraph)


def configure_section(section, kind: str):
    if kind == "apa":
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        margins = 1.0
        content_width = 6.5
        header_distance = 0.5
    elif kind == "figure":
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        margins = 0.75
        content_width = 7.0
        header_distance = 0.35
    elif kind == "table2":
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Inches(11)
        section.page_height = Inches(8.5)
        margins = 0.75
        content_width = 9.5
        header_distance = 0.35
    else:
        raise ValueError(f"Unknown section kind: {kind}")

    section.top_margin = Inches(margins)
    section.bottom_margin = Inches(margins)
    section.left_margin = Inches(margins)
    section.right_margin = Inches(margins)
    section.header_distance = Inches(header_distance)
    section.footer_distance = Inches(0.35 if kind != "apa" else 0.5)
    set_header(section, content_width)


def new_section(doc: Document, kind: str):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    configure_section(section, kind)
    return section


def add_hyperlink(paragraph, text: str, url: str):
    relationship = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), FONT)
    rfonts.set(qn("w:hAnsi"), FONT)
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "24")
    size_cs = OxmlElement("w:szCs")
    size_cs.set(qn("w:val"), "24")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "000000")
    rpr.extend((rfonts, size, size_cs, color))
    run.append(rpr)
    node = OxmlElement("w:t")
    # LibreOffice and some Word renderers treat a hyperlink as one unbreakable
    # object.  Invisible break opportunities after URL separators prevent long
    # reference entries from colliding with adjacent lines while preserving the
    # hyperlink target and visible APA text.
    node.text = text.replace("/", "/\u200b") if text.startswith(("http://", "https://")) else text
    run.append(node)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_markdown_runs(paragraph, text: str, *, size: float | None = None):
    cursor = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > cursor:
            run = paragraph.add_run(text[cursor : match.start()])
            if size:
                set_run_font(run, size)
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            set_run_font(run, size or 12, bold=True)
        elif token.startswith("*"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, size or 12, italic=True)
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, min(size or 12, 10.5), name="Courier New")
        elif token.startswith("["):
            label, url = re.fullmatch(r"\[([^\]]+)\]\((https?://[^)]+)\)", token).groups()
            add_hyperlink(paragraph, label, url)
        elif token.startswith("<sup>"):
            run = paragraph.add_run(token[5:-6])
            set_run_font(run, size or 12)
            run.font.superscript = True
        else:
            url = token
            trailing = ""
            while url and url[-1] in ".,;":
                trailing = url[-1] + trailing
                url = url[:-1]
            if urlparse(url).scheme in {"http", "https"}:
                add_hyperlink(paragraph, url, url)
                if trailing:
                    run = paragraph.add_run(trailing)
                    if size:
                        set_run_font(run, size)
            else:
                run = paragraph.add_run(token)
                if size:
                    set_run_font(run, size)
        cursor = match.end()
    if cursor < len(text):
        run = paragraph.add_run(text[cursor:])
        if size:
            set_run_font(run, size)


def parse_table_row(line: str):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(cells):
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def add_table(doc: Document, lines: list[str], table_number: int):
    rows = [parse_table_row(line) for line in lines]
    rows = [row for row in rows if not is_separator_row(row)]
    if table_number == 1:
        widths = [1.55, 3.15, 1.80]
        font_size = 9
    else:
        widths = [1.05, 1.85, 1.00, 1.25, 3.60, 0.75]
        font_size = 8.5

    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    set_table_geometry(table, widths)
    set_table_borders(table)
    mark_header_row(table.rows[0])

    for row_index, (row, values) in enumerate(zip(table.rows, rows)):
        prevent_row_split(row)
        for col_index, (cell, value) in enumerate(zip(row.cells, values)):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
            paragraph = cell.paragraphs[0]
            paragraph.style = doc.styles["APA Table Text"]
            if row_index == 0:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif table_number == 2 and col_index in {2, 3, 4, 5}:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_markdown_runs(paragraph, value, size=font_size)
            if row_index == 0:
                for run in paragraph.runs:
                    run.bold = True
    return table


def svg_viewbox(svg_text: str):
    match = re.search(r'viewBox="[-.0-9]+\s+[-.0-9]+\s+([.0-9]+)\s+([.0-9]+)"', svg_text)
    if not match:
        raise ValueError("SVG does not contain a usable viewBox")
    return float(match.group(1)), float(match.group(2))


def make_figure_png(svg_path: Path, out_dir: Path):
    text = svg_path.read_text(encoding="utf-8")
    temp_svg = out_dir / svg_path.name
    temp_svg.write_text(text, encoding="utf-8")
    png = out_dir / f"{svg_path.stem}.png"
    width, height = svg_viewbox(text)
    render_width = 2800
    render_height = round(render_width * height / width)
    subprocess.run(
        [
            "sips",
            "-s",
            "format",
            "png",
            "-z",
            str(render_height),
            str(render_width),
            str(temp_svg),
            "--out",
            str(png),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return png, width / height


def add_figure(doc: Document, svg_path: Path, temp_dir: Path):
    png, aspect = make_figure_png(svg_path, temp_dir)
    max_width = 6.5
    max_height = 7.0
    width = min(max_width, max_height * aspect)
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run()
    shape = run.add_picture(str(png), width=Inches(width))
    shape._inline.docPr.set("descr", FIGURE_ALTS[svg_path.name])
    shape._inline.docPr.set("title", svg_path.stem.replace("_", " ").title())


def set_table_description(table, description: str):
    tbl_pr = table._tbl.tblPr
    caption = OxmlElement("w:tblCaption")
    caption.set(qn("w:val"), description)
    tbl_pr.append(caption)


def add_title_page(doc: Document):
    paragraph = doc.add_paragraph(style="APA Title")
    add_markdown_runs(paragraph, TITLE)
    paragraph = doc.add_paragraph(style="APA Author")
    add_markdown_runs(paragraph, AUTHOR)
    paragraph = doc.add_paragraph(style="APA Author")
    add_markdown_runs(paragraph, f"Correspondence: {CORRESPONDENCE_EMAIL}")
    paragraph.add_run().add_break(WD_BREAK.PAGE)


def export(source: Path, output: Path):
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != f"# {TITLE}":
        raise ValueError("The manuscript title does not match the frozen export title")

    doc = Document()
    configure_styles(doc)
    configure_section(doc.sections[0], "apa")
    doc.core_properties.title = TITLE
    doc.core_properties.subject = "APA-style research manuscript"
    doc.core_properties.keywords = (
        "automated decision-making; human oversight; uncertainty; discrete-event simulation; Robodebt"
    )
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    add_title_page(doc)

    in_abstract = False
    in_references = False
    pending_exhibit_title = False
    current_figure = False
    current_table_number = None
    table2_notes = False
    table2_section_started = False

    with tempfile.TemporaryDirectory(prefix="apa_docx_figures_") as temp_name:
        temp_dir = Path(temp_name)
        index = 1
        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            if not stripped:
                index += 1
                continue

            if stripped in {f"**{AUTHOR}**", f"Correspondence: {CORRESPONDENCE_EMAIL}"}:
                index += 1
                continue

            if stripped.startswith("## "):
                heading = stripped[3:]
                if heading == "References":
                    doc.add_page_break()
                    in_references = True
                in_abstract = heading == "Abstract"
                paragraph = doc.add_paragraph(style="Heading 1")
                add_markdown_runs(paragraph, heading)
                index += 1
                continue

            if stripped.startswith("### "):
                paragraph = doc.add_paragraph(style="Heading 2")
                add_markdown_runs(paragraph, stripped[4:])
                index += 1
                continue

            if stripped.startswith("**Figure "):
                current_figure = True
                pending_exhibit_title = True
                paragraph = doc.add_paragraph(style="APA Exhibit Label")
                add_markdown_runs(paragraph, stripped)
                index += 1
                continue

            if stripped.startswith("**Table "):
                match = re.search(r"Table (\d+)", stripped)
                current_table_number = int(match.group(1))
                if current_table_number == 2 and not table2_section_started:
                    new_section(doc, "table2")
                    table2_section_started = True
                if current_table_number == 2:
                    table2_notes = True
                pending_exhibit_title = True
                paragraph = doc.add_paragraph(style="APA Exhibit Label")
                add_markdown_runs(paragraph, stripped)
                index += 1
                continue

            if pending_exhibit_title and stripped.startswith("*"):
                paragraph = doc.add_paragraph(style="APA Exhibit Title")
                add_markdown_runs(paragraph, stripped)
                pending_exhibit_title = False
                index += 1
                continue

            if stripped.startswith("!["):
                match = re.fullmatch(r"!\[[^\]]+\]\(([^)]+)\)", stripped)
                if not match:
                    raise ValueError(f"Malformed image line: {stripped}")
                svg_path = (source.parent / match.group(1)).resolve()
                add_figure(doc, svg_path, temp_dir)
                index += 1
                continue

            if stripped.startswith("|"):
                table_lines = []
                while index < len(lines) and lines[index].strip().startswith("|"):
                    table_lines.append(lines[index].strip())
                    index += 1
                table = add_table(doc, table_lines, current_table_number)
                set_table_description(
                    table,
                    "Counterfactual policy comparison" if current_table_number == 1 else "Paired simulation estimates",
                )
                continue

            if stripped.startswith("*Note.*"):
                paragraph = doc.add_paragraph(style="APA Exhibit Note")
                add_markdown_runs(paragraph, stripped, size=9)
                if current_figure:
                    current_figure = False
                index += 1
                continue

            if table2_notes and stripped.startswith("<sup>"):
                paragraph = doc.add_paragraph(style="APA Exhibit Note")
                add_markdown_runs(paragraph, stripped, size=9)
                if stripped.startswith("<sup>d</sup>"):
                    new_section(doc, "apa")
                    table2_notes = False
                    table2_section_started = False
                    current_table_number = None
                index += 1
                continue

            if in_references:
                style = "APA Reference"
            elif in_abstract:
                style = "APA Keywords" if stripped.startswith("*Keywords:*") else "APA Abstract"
            else:
                style = "APA Body"
            if stripped.startswith("Table 2 reports") and not table2_section_started:
                new_section(doc, "table2")
                table2_section_started = True
            paragraph = doc.add_paragraph(style=style)
            add_markdown_runs(paragraph, stripped)
            if re.match(r"^Figure [123] (previews|contrasts|visualizes)\b", stripped):
                paragraph.paragraph_format.keep_with_next = True
            index += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    export(args.source.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
