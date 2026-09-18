"""Generate Lewy AI pitch deck PDF using fpdf2."""
from fpdf import FPDF

PW, PH = 297, 210  # A4 landscape
MARGIN = 18
CW = PW - 2 * MARGIN  # 261

DARK   = (15,  23,  42)   # slate-900
BLUE   = (37,  99, 235)   # blue-600
LIGHT  = (248, 250, 252)  # slate-50
MID    = (100, 116, 139)  # slate-500
WHITE  = (255, 255, 255)
ACCENT = (239, 68,  68)   # red-500 (PD awareness colour)


class Deck(FPDF):
    def header(self): pass
    def footer(self): pass


def slide(pdf, bg=WHITE):
    pdf.add_page()
    r, g, b = bg
    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, PW, PH, "F")


def title_slide(pdf):
    slide(pdf, DARK)
    # Brand name
    pdf.set_font("Helvetica", "B", 52)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(MARGIN, 38)
    pdf.cell(0, 20, "Lewy", align="L")
    # Tagline
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(*MID)
    pdf.set_xy(MARGIN, 68)
    pdf.cell(0, 10, "Protein AI for Parkinson's disease", align="L")
    # Bar
    pdf.set_fill_color(*BLUE)
    pdf.rect(MARGIN, 84, 60, 2, "F")
    # Sub
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(MARGIN, 92)
    pdf.multi_cell(180, 7,
        "ESM-2, the world's leading protein AI, predicts Parkinson's\n"
        "variants backwards. We fix that.", align="L")
    # Founders
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*MID)
    pdf.set_xy(MARGIN, PH - 30)
    pdf.cell(0, 7, "Evan O'Leary  +  Niall O'Leary (patient co-founder)", align="L")


def problem_slide(pdf):
    slide(pdf, WHITE)
    # Header
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(0, 7, "THE PROBLEM")
    # Title
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN, 30)
    pdf.multi_cell(CW, 13, "Current protein AI fails on\nParkinson's - silently.", align="L")
    # Divider
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(MARGIN, 72, MARGIN + 60, 72)

    # Three pain points
    points = [
        ("$4.9B/yr", "invested in PD drug discovery annually"),
        ("-0.17",     "Spearman rho - ESM-2 on SNCA (vs +0.41 on normal proteins)"),
        ("Backwards", "ESM-2 ranks protective variants as damaging, and vice versa"),
    ]
    x = MARGIN
    col_w = CW / 3
    for stat, desc in points:
        pdf.set_font("Helvetica", "B", 30)
        pdf.set_text_color(*BLUE)
        pdf.set_xy(x, 82)
        pdf.cell(col_w, 14, stat, align="L")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MID)
        pdf.set_xy(x, 98)
        pdf.multi_cell(col_w - 6, 5.5, desc, align="L")
        x += col_w

    # Quote box
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(MARGIN, 130, CW, 40, "F")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN + 8, 138)
    pdf.multi_cell(CW - 16, 6.5,
        '"When a clinician sees an unknown SNCA variant, they run ESM-2.\n'
        'LewyGym shows that model has been misleading them the whole time.\n'
        'The tools are broken for the most important Parkinson\'s gene."', align="L")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*MID)
    pdf.set_xy(MARGIN + 8, 162)
    pdf.cell(0, 5, "- LewyGym preprint, O'Leary & O'Leary, 2026")


def solution_slide(pdf):
    slide(pdf, WHITE)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(0, 7, "THE SOLUTION")

    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN, 30)
    pdf.multi_cell(140, 13, "A variant effect API\nthat actually works\nfor GOF proteins.", align="L")

    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(MARGIN, 84, MARGIN + 60, 84)

    # Steps
    steps = [
        ("1", "Fine-tune",   "Retrain protein LMs on aggregation-specific DMS data, not just evolution"),
        ("2", "Benchmark",   "Evaluate every model against LewyGym - the only PD variant ground truth"),
        ("3", "Ship API",    "POST /score {gene, variant} -> calibrated pathogenicity score + confidence"),
        ("4", "Expand",      "SNCA first, then LRRK2, then ALS (SOD1, TDP-43), then Alzheimer's (APP)"),
    ]
    y = 94
    for num, title, desc in steps:
        pdf.set_fill_color(*BLUE)
        pdf.rect(MARGIN, y, 7, 7, "F")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(MARGIN + 1.5, y + 0.8)
        pdf.cell(7, 5, num)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*DARK)
        pdf.set_xy(MARGIN + 12, y)
        pdf.cell(50, 7, title)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MID)
        pdf.set_xy(MARGIN + 62, y)
        pdf.multi_cell(CW - 62, 5.5, desc, align="L")
        y += 18

    # Right panel - comparison
    rx = MARGIN + 155
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(rx, 28, 106, 150, "F")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*DARK)
    pdf.set_xy(rx + 6, 36)
    pdf.cell(94, 6, "ESM-2 on SNCA today", align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*ACCENT)
    pdf.set_xy(rx + 6, 44)
    pdf.cell(94, 5, "Spearman rho = -0.17  (WRONG)", align="C")
    pdf.set_draw_color(200, 200, 200)
    pdf.line(rx + 10, 54, rx + 100, 54)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*DARK)
    pdf.set_xy(rx + 6, 58)
    pdf.cell(94, 6, "Lewy API (target)", align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(34, 197, 94)
    pdf.set_xy(rx + 6, 66)
    pdf.cell(94, 5, "Spearman rho > +0.30  (calibrated)", align="C")


def traction_slide(pdf):
    slide(pdf, WHITE)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(0, 7, "TRACTION")

    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN, 30)
    pdf.multi_cell(CW, 13, "We already proved the problem.", align="L")

    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(MARGIN, 55, MARGIN + 60, 55)

    items = [
        ("LewyGym benchmark",      "Published on GitHub + HuggingFace. 13,560 scored SNCA variants. ProteinGym-compatible format."),
        ("ESM-2 baseline results", "8M and 650M models benchmarked. Mean rho -0.139 / -0.171. Numbers are in the repo."),
        ("bioRxiv preprint",       "lewygym_preprint.pdf ready to submit. 5 pages, 3 tables, 9 references. Two co-authors."),
        ("Patient co-founder",     "Niall O'Leary (PD diagnosis). Not an advisory role - listed on the paper, in the loop on every decision."),
        ("Open source moat",       "CC0 data + open benchmark = community adoption. Lewy becomes the standard for PD variant evaluation."),
    ]
    y = 64
    for title, desc in items:
        pdf.set_fill_color(*BLUE)
        pdf.rect(MARGIN, y + 1.5, 3, 3, "F")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*DARK)
        pdf.set_xy(MARGIN + 8, y)
        pdf.cell(70, 6, title)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MID)
        pdf.set_xy(MARGIN + 78, y)
        pdf.multi_cell(CW - 78, 5.5, desc, align="L")
        y += 16


def market_slide(pdf):
    slide(pdf, WHITE)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(0, 7, "MARKET")

    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN, 30)
    pdf.multi_cell(CW, 13, "Every pharma company working\non neurodegeneration needs this.", align="L")

    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.4)
    pdf.line(MARGIN, 62, MARGIN + 60, 62)

    segments = [
        ("$4.9B",  "PD drug discovery\nannual spend",       "Beams, AstraZeneca, Sanofi,\nBiogen - all have PD programs"),
        ("$18B",   "Neurodegeneration\ndrug pipeline value", "ALS, Alzheimer's, Huntington's\n- same GOF model failure"),
        ("$2.1B",  "Computational biology\ntools market",    "Growing 15% YoY - pharma\npaying for AI variant tools"),
    ]
    x = MARGIN
    col_w = CW / 3
    for stat, label, detail in segments:
        pdf.set_fill_color(239, 246, 255)
        pdf.rect(x, 70, col_w - 6, 60, "F")
        pdf.set_font("Helvetica", "B", 32)
        pdf.set_text_color(*BLUE)
        pdf.set_xy(x + 4, 76)
        pdf.cell(col_w - 10, 16, stat, align="L")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*DARK)
        pdf.set_xy(x + 4, 94)
        pdf.multi_cell(col_w - 10, 5.5, label, align="L")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*MID)
        pdf.set_xy(x + 4, 108)
        pdf.multi_cell(col_w - 10, 5, detail, align="L")
        x += col_w

    # Business model
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*DARK)
    pdf.set_xy(MARGIN, 142)
    pdf.cell(0, 7, "Business model")
    bm = [
        ("API (per query)",  "$0.01-0.10 per variant scored. Self-serve, instant."),
        ("Enterprise",       "$50K-200K/yr annual license. Full gene panel, SLA, custom models."),
        ("Data licensing",   "Aggregation DMS datasets sold to model trainers and pharma."),
    ]
    y = 153
    for title, desc in bm:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*DARK)
        pdf.set_xy(MARGIN, y)
        pdf.cell(55, 5.5, title)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MID)
        pdf.set_xy(MARGIN + 55, y)
        pdf.cell(CW - 55, 5.5, desc)
        y += 12


def team_ask_slide(pdf):
    slide(pdf, DARK)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(0, 7, "TEAM  +  ASK")

    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(MARGIN, 30)
    pdf.multi_cell(130, 12, "Two co-founders.\nOne of us has Parkinson's.", align="L")

    # Team
    team = [
        ("Evan O'Leary",  "Technical co-founder",
         "Built LewyGym and scoring harness. ESM-2 benchmarking.\nProtein ML, Python, HuggingFace stack."),
        ("Niall O'Leary", "Patient co-founder",
         "Living with Parkinson's disease. Co-author on the preprint.\nProvides patient perspective on every product decision."),
    ]
    y = 72
    for name, role, bio in team:
        pdf.set_fill_color(30, 41, 59)
        pdf.rect(MARGIN, y, 130, 34, "F")
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(MARGIN + 5, y + 4)
        pdf.cell(120, 7, name)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*BLUE)
        pdf.set_xy(MARGIN + 5, y + 12)
        pdf.cell(120, 5, role)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(148, 163, 184)
        pdf.set_xy(MARGIN + 5, y + 19)
        pdf.multi_cell(120, 4.8, bio)
        y += 40

    # Hiring
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*MID)
    pdf.set_xy(MARGIN, 158)
    pdf.cell(130, 5, "Hiring: wet lab collaborator, ML engineer (protein models)")

    # Ask box
    rx = MARGIN + 148
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(rx, 28, 113, 152, "F")
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(rx + 8, 36)
    pdf.cell(97, 8, "Pre-seed ask")
    pdf.set_font("Helvetica", "B", 40)
    pdf.set_xy(rx + 8, 48)
    pdf.cell(97, 20, "$500K", align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(191, 219, 254)
    pdf.set_xy(rx + 8, 72)
    pdf.multi_cell(97, 6,
        "18 months runway\n\n"
        "Use of funds:\n"
        "  40%  Aggregation DMS experiment\n"
        "        (contract Arctoris / CRO)\n\n"
        "  30%  Model training + API build\n\n"
        "  20%  Wet lab hire\n\n"
        "  10%  Ops, legal, cloud", align="L")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(rx + 8, 156)
    pdf.cell(97, 6, "Milestone: rho > +0.30 on SNCA")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(191, 219, 254)
    pdf.set_xy(rx + 8, 164)
    pdf.cell(97, 5, "= Series A ready")


def contact_slide(pdf):
    slide(pdf, DARK)
    pdf.set_font("Helvetica", "B", 44)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(MARGIN, 50)
    pdf.cell(0, 20, "Lewy", align="C")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(*MID)
    pdf.set_xy(MARGIN, 76)
    pdf.cell(0, 10, "Protein AI for Parkinson's disease", align="C")
    pdf.set_fill_color(*BLUE)
    pdf.rect(PW/2 - 30, 92, 60, 2, "F")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(MARGIN, 100)
    pdf.cell(0, 8, "evan.oleary99@gmail.com", align="C")
    pdf.set_xy(MARGIN, 110)
    pdf.cell(0, 8, "github.com/Tyronita/LewyGym", align="C")
    pdf.set_xy(MARGIN, 120)
    pdf.cell(0, 8, "huggingface.co/datasets/EvanOLeary/LewyGym", align="C")


def build():
    pdf = Deck("L", "mm", "A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(False)

    title_slide(pdf)
    problem_slide(pdf)
    solution_slide(pdf)
    traction_slide(pdf)
    market_slide(pdf)
    team_ask_slide(pdf)
    contact_slide(pdf)

    out = "/Users/nialloleary/LewyGym/lewy_pitch.pdf"
    pdf.output(out)
    print(f"Saved {pdf.page} slides -> {out}")


if __name__ == "__main__":
    build()
