"""Tourism Audit PDF Generator — fpdf2.

Generates a branded PDF report from the raw Deep Research audit output.
Adapted from devidevs-frontend/scripts/generate-audit-pdf.py for tourism context.

Brand: Teal #0D9488 (primary), Amber #F59E0B (CTA), Plus Jakarta Sans + Inter (body).
Since fpdf2 only supports built-in fonts (Helvetica = latin-1), we use Helvetica
and handle Romanian diacritics via latin-1 encoding with fallback replacements.
"""

import io
import logging
import re
from datetime import datetime

from fpdf import FPDF

from src.models import PropertyData

logger = logging.getLogger(__name__)

# ── Brand Colors (RGB) ───────────────────────────────────────────────
TEAL = (13, 148, 136)          # Primary — #0D9488
TEAL_DARK = (15, 118, 110)     # Headers — #0F766E
TEAL_LIGHT = (94, 234, 212)    # Accents — #5EEBD4
AMBER = (245, 158, 11)         # CTA — #F59E0B
AMBER_LIGHT = (251, 191, 36)   # CTA gradient end — #FBBF24
WHITE = (255, 255, 255)
DARK_BG = (30, 30, 30)         # Cover dark — #1E1E1E (matches email)
GRAY_900 = (23, 23, 23)
GRAY_700 = (64, 64, 64)
GRAY_600 = (82, 82, 82)
GRAY_500 = (115, 115, 115)
GRAY_400 = (163, 163, 163)
GRAY_300 = (212, 212, 212)
GRAY_200 = (229, 229, 229)
GRAY_100 = (245, 245, 245)
GRAY_50 = (250, 250, 250)

# Score colors for the 0-10 rating display
SCORE_GOOD = (22, 163, 74)     # 8-10 green
SCORE_OK = (217, 119, 6)       # 5-7 amber
SCORE_BAD = (220, 38, 38)      # 0-4 red

# Status icon mappings (unicode → latin-1 safe text)
STATUS_MAP = {
    "\u2705": "[OK]",    # ✅
    "\u26a0\ufe0f": "[!]",  # ⚠️
    "\u274c": "[X]",     # ❌
}

# Page dimensions
PW = 210  # A4 width mm
PH = 297  # A4 height mm
MARGIN = 18
CONTENT_W = PW - 2 * MARGIN


class TourismAuditPDF(FPDF):
    """Custom PDF class with DeviDevs Tourism branding."""

    def __init__(self, property_name: str, property_address: str, score_text: str = ""):
        super().__init__()
        self.property_name = property_name
        self.property_address = property_address
        self.score_text = score_text
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(MARGIN, MARGIN, MARGIN)

    # ── Header / Footer ─────────────────────────────────────────────

    def header(self):
        if self.page_no() == 1:
            return  # Cover page has custom layout

        # Thin teal accent line at top
        self.set_fill_color(*TEAL)
        self.rect(0, 0, PW, 2, "F")

        # Header text
        self.set_y(5)
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*GRAY_500)
        prop = self._safe(self.property_name)
        self.cell(0, 6, f"AUDIT DIGITAL  -  {prop}", align="R")

        # Thin separator
        self.set_draw_color(*GRAY_200)
        self.set_line_width(0.2)
        self.line(MARGIN, 12, PW - MARGIN, 12)
        self.set_y(15)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*GRAY_200)
        self.set_line_width(0.2)
        self.line(MARGIN, PH - 14, PW - MARGIN, PH - 14)
        self.set_y(-12)
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*GRAY_400)
        self.cell(
            CONTENT_W / 2, 5,
            "DeviDevs  |  Audit Digital Turism  |  devidevs.com",
            align="L",
        )
        self.cell(CONTENT_W / 2, 5, f"Pagina {self.page_no()}/{{nb}}", align="R")

    # ── Cover Page ──────────────────────────────────────────────────

    def cover_page(self):
        self.add_page()

        # Full dark background
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, PW, PH, "F")

        # Top teal gradient bar
        self.set_fill_color(*TEAL)
        self.rect(0, 0, PW, 5, "F")

        # Main title
        self.set_y(55)
        self.set_font("Helvetica", "B", 30)
        self.set_text_color(*WHITE)
        self.cell(0, 13, "AUDIT DIGITAL", align="C")

        # Subtitle in amber
        self.ln(16)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*AMBER)
        self.cell(0, 8, "Raport Complet de Prezenta Digitala", align="C")

        # Divider
        self.ln(18)
        y = self.get_y()
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        self.line(55, y, 155, y)

        # Property info
        self.ln(14)
        meta_items = [
            ("Proprietate", self._safe(self.property_name)),
            ("Locatie", self._safe(self.property_address)),
            ("Data raportului", datetime.now().strftime("%d.%m.%Y")),
            ("Generat de", "DeviDevs - Audit Digital Turism"),
        ]

        for label, value in meta_items:
            self.set_x(35)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*GRAY_500)
            self.cell(50, 7, label, align="R")
            self.cell(6, 7, "")
            self.set_font("Helvetica", "B", 9.5)
            self.set_text_color(*WHITE)
            self.cell(75, 7, value, align="L")
            self.ln(8)

        # Score badge (if available)
        if self.score_text:
            self.ln(15)
            badge_text = f"SCOR DIGITAL: {self.score_text}"
            badge_w = self.get_string_width(badge_text) + 24
            badge_x = (PW - badge_w) / 2
            badge_y = self.get_y()
            self.set_fill_color(*TEAL)
            self.rect(badge_x, badge_y, badge_w, 12, "F")
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(*WHITE)
            self.set_y(badge_y)
            self.cell(0, 12, badge_text, align="C")

        # Bottom section
        self.set_auto_page_break(auto=False)
        self.set_y(220)
        self.set_draw_color(*GRAY_600)
        self.set_line_width(0.2)
        self.line(70, self.get_y(), 140, self.get_y())
        self.ln(8)

        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY_500)
        self.cell(0, 5, "Generat de", align="C")
        self.ln(6)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.cell(0, 6, "DeviDevs  |  Solutii Digitale pentru Turism", align="C")
        self.ln(7)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRAY_400)
        self.cell(0, 5, "Bucuresti, Romania", align="C")
        self.ln(6)
        self.set_text_color(*TEAL_LIGHT)
        self.cell(0, 5, "devidevs.com  |  petru@devidevs.com", align="C")

        # Confidentiality-style notice
        self.set_y(264)
        self.set_font("Helvetica", "I", 6)
        self.set_text_color(*GRAY_600)
        self.multi_cell(
            0, 3,
            "Acest raport a fost generat automat pe baza datelor publice disponibile online. "
            "Informatiile prezentate sunt cu scop informativ si nu constituie o garantie. "
            "Pentru un plan de actiune personalizat, programeaza o consultatie gratuita.",
            align="C",
        )

        # Bottom teal bar
        self.set_fill_color(*TEAL)
        self.rect(0, PH - 5, PW, 5, "F")

        # Re-enable auto page break
        self.set_auto_page_break(auto=True, margin=22)

    # ── Content Rendering ───────────────────────────────────────────

    def section_header(self, text: str, level: int = 2):
        """Render section header with teal accent."""
        if level <= 2:
            self.ln(4)
        else:
            self.ln(2)

        if self.get_y() > 255:
            self.add_page()

        clean = self._safe(text)

        if level == 1:
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*TEAL_DARK)
        elif level == 2:
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(*GRAY_900)
        elif level == 3:
            self.set_font("Helvetica", "B", 10.5)
            self.set_text_color(*GRAY_700)
        else:
            self.set_font("Helvetica", "B", 9.5)
            self.set_text_color(*GRAY_700)

        self.multi_cell(CONTENT_W, 6 if level <= 2 else 5, clean)

        if level <= 2:
            self.set_draw_color(*TEAL)
            self.set_line_width(0.5 if level == 1 else 0.3)
            line_end = MARGIN + (CONTENT_W * 0.6 if level == 2 else CONTENT_W * 0.5)
            self.line(MARGIN, self.get_y() + 1, line_end, self.get_y() + 1)
            self.ln(3)
        else:
            self.ln(1.5)

    def body_text(self, text: str):
        """Render body text with inline bold support."""
        if not text.strip():
            return
        if self.get_y() > 270:
            self.add_page()
        self._render_rich_text(text, font_size=9, line_h=4.5)
        self.ln(2)

    def bullet(self, text: str, indent: int = 0):
        """Render a bullet point."""
        if self.get_y() > 270:
            self.add_page()

        x = MARGIN + indent * 5
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEAL)
        self.cell(5, 4.5, "-")
        self.set_text_color(*GRAY_900)
        self._render_rich_text(text, font_size=8.5, line_h=4.2)
        self.ln(1)

    def numbered_item(self, num: str, text: str):
        """Render numbered list item."""
        if self.get_y() > 270:
            self.add_page()

        self.set_x(MARGIN)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*TEAL)
        self.cell(7, 4.5, f"{num}.")
        self.set_text_color(*GRAY_900)
        self._render_rich_text(text, font_size=8.5, line_h=4.2)
        self.ln(1.5)

    def render_table(self, headers: list[str], rows: list[list[str]]):
        """Render table with proper multi-cell row height."""
        if not headers:
            return

        col_widths = self._calc_col_widths(headers, rows, CONTENT_W)

        if self.get_y() > 250:
            self.add_page()

        self.ln(2)

        # Header row
        self.set_fill_color(*TEAL_DARK)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 7)
        self.set_draw_color(*GRAY_300)
        self.set_line_width(0.15)

        y0 = self.get_y()
        max_h = 7
        for i, h in enumerate(headers):
            txt = self._safe(h.strip())
            needed = self._measure_cell_height(txt, col_widths[i], 3.5)
            max_h = max(max_h, needed)

        for i, h in enumerate(headers):
            x = MARGIN + sum(col_widths[:i])
            self.set_xy(x, y0)
            txt = self._safe(h.strip())
            self.cell(col_widths[i], max_h, txt, border=1, fill=True, align="C")

        self.set_y(y0 + max_h)

        # Data rows
        self.set_font("Helvetica", "", 7)
        for row_idx, row in enumerate(rows):
            fill_color = GRAY_50 if row_idx % 2 == 0 else WHITE
            self.set_fill_color(*fill_color)

            while len(row) < len(headers):
                row.append("")

            y0 = self.get_y()
            max_h = 5.5
            cell_texts = []
            for i, cell in enumerate(row):
                txt = self._safe(cell.strip())
                cell_texts.append(txt)
                needed = self._measure_cell_height(txt, col_widths[i], 3.5)
                max_h = max(max_h, needed)

            if y0 + max_h > PH - 22:
                self.add_page()
                y0 = self.get_y()

            for i, txt in enumerate(cell_texts):
                x = MARGIN + sum(col_widths[:i])
                self.set_xy(x, y0)
                self.set_text_color(*GRAY_900)
                self.set_font("Helvetica", "", 7)
                self.rect(x, y0, col_widths[i], max_h, "DF")
                self.set_xy(x + 1, y0 + 1)
                self.multi_cell(col_widths[i] - 2, 3.5, txt, align="L")

            self.set_y(y0 + max_h)

        self.ln(4)

    def blockquote(self, text: str):
        """Render blockquote with teal left border."""
        if self.get_y() > 265:
            self.add_page()

        y_start = self.get_y()
        self.set_fill_color(*GRAY_50)
        self.set_x(MARGIN + 4)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY_600)
        clean = self._safe(text)
        self.multi_cell(CONTENT_W - 8, 4, clean, fill=True)
        y_end = self.get_y()

        # Teal left border
        self.set_draw_color(*TEAL)
        self.set_line_width(1)
        self.line(MARGIN + 2, y_start, MARGIN + 2, y_end)
        self.ln(4)

    def score_badge(self, category: str, score: str):
        """Render a score line: category name + colored score badge."""
        if self.get_y() > 270:
            self.add_page()

        self.set_x(MARGIN)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRAY_900)
        self.cell(CONTENT_W * 0.65, 6, self._safe(category))

        # Parse score number for coloring
        try:
            score_num = int(re.search(r"(\d+)", score).group(1))
        except (AttributeError, ValueError):
            score_num = 5

        if score_num >= 8:
            color = SCORE_GOOD
        elif score_num >= 5:
            color = SCORE_OK
        else:
            color = SCORE_BAD

        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*color)
        self.cell(CONTENT_W * 0.35, 6, self._safe(score), align="R")
        self.ln(6)

    # ── CTA Section ────────────────────────────────────────────────

    def cta_section(self, meeting_link: str):
        """Render the call-to-action page at the end."""
        self.add_page()

        self.ln(20)
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*TEAL_DARK)
        self.multi_cell(CONTENT_W, 10, "Urmatorul Pas", align="C")

        self.ln(8)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*GRAY_700)
        self.multi_cell(
            CONTENT_W, 6,
            self._safe(
                "Acest raport identifica atat punctele forte, cat si oportunitatile "
                "de imbunatatire ale prezentei tale digitale. Implementarea actiunilor "
                "recomandate poate parea complexa, dar nu trebuie sa faci totul singur."
            ),
            align="C",
        )

        self.ln(12)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*AMBER)
        self.multi_cell(
            CONTENT_W, 7,
            "Programeaza o consultatie gratuita pentru un plan personalizat:",
            align="C",
        )

        self.ln(6)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*TEAL)
        self.multi_cell(CONTENT_W, 6, meeting_link, align="C")

        self.ln(20)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.3)
        self.line(60, self.get_y(), 150, self.get_y())

        self.ln(10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRAY_500)
        self.multi_cell(
            CONTENT_W, 5,
            self._safe(
                "Solutiile moderne de automatizare AI pot prelua multe dintre "
                "aceste sarcini (social media, raspunsuri la recenzii, optimizare "
                "continut), economisind timp si asigurand consistenta."
            ),
            align="C",
        )

    # ── Rich text rendering ────────────────────────────────────────

    def _render_rich_text(self, text: str, font_size: float = 9, line_h: float = 4.5):
        """Render text with **bold** and *italic* inline."""
        parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
        self.set_font("Helvetica", "", font_size)
        self.set_text_color(*GRAY_900)

        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", font_size)
                self.write(line_h, self._safe(part.strip("*")))
                self.set_font("Helvetica", "", font_size)
            elif part.startswith("*") and part.endswith("*"):
                self.set_font("Helvetica", "I", font_size)
                self.write(line_h, self._safe(part.strip("*")))
                self.set_font("Helvetica", "", font_size)
            else:
                self.write(line_h, self._safe(part))

        self.ln(line_h)

    # ── Utility ────────────────────────────────────────────────────

    def _safe(self, text: str) -> str:
        """Make text safe for latin-1 Helvetica rendering."""
        if not text:
            return ""
        # Replace status emoji with text markers
        for emoji, replacement in STATUS_MAP.items():
            text = text.replace(emoji, replacement)
        # Romanian diacritics → ASCII (Helvetica limitation)
        diacritics = {
            "\u0103": "a",  # ă
            "\u0102": "A",  # Ă
            "\u00e2": "a",  # â
            "\u00c2": "A",  # Â
            "\u00ee": "i",  # î
            "\u00ce": "I",  # Î
            "\u0219": "s",  # ș
            "\u0218": "S",  # Ș
            "\u015f": "s",  # ş (legacy)
            "\u015e": "S",  # Ş (legacy)
            "\u021b": "t",  # ț
            "\u021a": "T",  # Ț
            "\u0163": "t",  # ţ (legacy)
            "\u0162": "T",  # Ţ (legacy)
        }
        for char, repl in diacritics.items():
            text = text.replace(char, repl)
        # Common unicode chars
        text = text.replace("\u2192", "->")
        text = text.replace("\u2022", "-")
        text = text.replace("\u2013", "-")
        text = text.replace("\u2014", "--")
        text = text.replace("\u2018", "'")
        text = text.replace("\u2019", "'")
        text = text.replace("\u201c", '"')
        text = text.replace("\u201d", '"')
        text = text.replace("\u2026", "...")
        text = text.replace("\u00a0", " ")
        # Strip markdown formatting
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"`(.+?)`", r"\1", text)
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
        text = re.sub(r"<[^>]+>", "", text)
        # Final encode safety
        text = text.encode("latin-1", errors="replace").decode("latin-1")
        return text

    def _measure_cell_height(self, text: str, width: float, line_h: float) -> float:
        if not text:
            return line_h + 2
        chars_per_line = max(1, int(width / 1.8))
        lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
        return lines * line_h + 2

    def _calc_col_widths(
        self, headers: list[str], rows: list[list[str]], total_w: float
    ) -> list[float]:
        n = len(headers)
        if n == 0:
            return []

        max_lens = []
        for i in range(n):
            h_len = len(self._safe(headers[i].strip()))
            max_cell = h_len
            for row in rows[:15]:
                if i < len(row):
                    cell_len = len(self._safe(row[i].strip()))
                    max_cell = max(max_cell, min(cell_len, 80))
            max_lens.append(max(max_cell, 5))

        total_len = sum(max_lens) or 1
        widths = [max(12, (ml / total_len) * total_w) for ml in max_lens]
        scale = total_w / sum(widths)
        return [w * scale for w in widths]


# ── Raw audit text parser ────────────────────────────────────────────

def _parse_raw_audit_to_blocks(raw_audit: str) -> list[tuple]:
    """Parse raw Deep Research audit text into structured blocks.

    The raw audit from Gemini Deep Research is semi-structured text with:
    - Section headers (##, ###, ####)
    - Bullet points (-, *)
    - Numbered lists (1., 2., etc.)
    - Tables (| col1 | col2 |)
    - Regular paragraphs
    - Score lines (Category: X/10)
    """
    blocks = []
    lines = raw_audit.split("\n")
    i = 0
    in_table = False
    table_headers: list[str] = []
    table_rows: list[list[str]] = []

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            if in_table:
                blocks.append(("table", table_headers, table_rows))
                in_table = False
                table_headers = []
                table_rows = []
            i += 1
            continue

        # Table
        if "|" in line and not line.strip().startswith("#"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.match(r"^[-:]+$", c) for c in cells if c):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            blocks.append(("table", table_headers, table_rows))
            in_table = False
            table_headers = []
            table_rows = []

        # Headings
        m = re.match(r"^(#{1,4})\s+(.+)", line)
        if m:
            blocks.append(("heading", len(m.group(1)), m.group(2)))
            i += 1
            continue

        # HR
        if re.match(r"^---+\s*$", line):
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            blocks.append(("quote", " ".join(quote_lines)))
            continue

        # Score line (e.g., "Prezenta Digitala: 7/10" or "TOTAL: 65/110")
        score_match = re.match(
            r"^[-*]?\s*(.+?):\s*(\d+/\d+(?:\s*\(\d+%\))?)\s*$", line.strip()
        )
        if score_match:
            blocks.append(("score", score_match.group(1).strip(), score_match.group(2).strip()))
            i += 1
            continue

        # Numbered list
        m = re.match(r"^(\d+)[.)]\s+(.+)", line)
        if m:
            num = m.group(1)
            text = m.group(2)
            i += 1
            while i < len(lines) and lines[i].startswith("   ") and not re.match(r"^\d+[.)]", lines[i].strip()):
                text += " " + lines[i].strip()
                i += 1
            blocks.append(("numbered", num, text))
            continue

        # Bullet
        m = re.match(r"^(\s*)([-*])\s+(.+)", line)
        if m:
            indent = 1 if len(m.group(1)) >= 2 else 0
            text = m.group(3)
            i += 1
            while i < len(lines) and lines[i].startswith("  ") and not re.match(r"^\s*[-*]\s+", lines[i]):
                text += " " + lines[i].strip()
                i += 1
            blocks.append(("bullet", text, indent))
            continue

        # Paragraph
        if line.strip():
            para_lines = [line]
            i += 1
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith("#")
                and not lines[i].startswith("|")
                and not lines[i].startswith(">")
                and not re.match(r"^[-*]\s+", lines[i])
                and not re.match(r"^\d+[.)]\s+", lines[i])
                and not re.match(r"^---", lines[i])
            ):
                para_lines.append(lines[i])
                i += 1
            blocks.append(("paragraph", " ".join(para_lines)))
            continue

        i += 1

    if in_table:
        blocks.append(("table", table_headers, table_rows))

    return blocks


def _extract_total_score(raw_audit: str) -> str:
    """Extract TOTAL: XX/110 (XX%) from the raw audit text."""
    m = re.search(r"TOTAL:\s*(\d+/\d+(?:\s*\(\d+%\))?)", raw_audit)
    if m:
        return m.group(1)
    return ""


# ── Public API ────────────────────────────────────────────────────────

def generate_audit_pdf(
    raw_audit: str,
    property_data: PropertyData,
    meeting_link: str = "",
) -> bytes:
    """Generate a complete PDF audit report from raw Deep Research output.

    Returns the PDF content as bytes (ready to attach to email or save).
    """
    logger.info(
        "Generating PDF for '%s' (%d chars raw audit)",
        property_data.property_name,
        len(raw_audit),
    )

    score_text = _extract_total_score(raw_audit)

    pdf = TourismAuditPDF(
        property_name=property_data.property_name,
        property_address=property_data.property_address,
        score_text=score_text,
    )
    pdf.alias_nb_pages()

    # Cover page
    pdf.cover_page()

    # Content pages
    pdf.add_page()

    blocks = _parse_raw_audit_to_blocks(raw_audit)

    for block in blocks:
        if block[0] == "heading":
            pdf.section_header(block[2], block[1])
        elif block[0] == "paragraph":
            pdf.body_text(block[1])
        elif block[0] == "bullet":
            pdf.bullet(block[1], block[2])
        elif block[0] == "numbered":
            pdf.numbered_item(block[1], block[2])
        elif block[0] == "table":
            pdf.render_table(block[1], block[2])
        elif block[0] == "quote":
            pdf.blockquote(block[1])
        elif block[0] == "score":
            pdf.score_badge(block[1], block[2])

    # CTA page at the end
    if meeting_link:
        pdf.cta_section(meeting_link)

    # Return bytes
    pdf_bytes = pdf.output()
    logger.info(
        "PDF generated: %d pages, %.1f KB",
        pdf.page_no(),
        len(pdf_bytes) / 1024,
    )
    return pdf_bytes
