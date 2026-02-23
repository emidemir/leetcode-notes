from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import reportlab.lib.colors as lcolors

# ── Color Palette ──────────────────────────────────────────────────────────────
C_BG        = colors.HexColor("#0F172A")   # dark navy
C_ACCENT    = colors.HexColor("#38BDF8")   # sky blue
C_ACCENT2   = colors.HexColor("#818CF8")   # indigo
C_GREEN     = colors.HexColor("#34D399")   # emerald
C_YELLOW    = colors.HexColor("#FBBF24")   # amber
C_RED       = colors.HexColor("#F87171")   # rose
C_PURPLE    = colors.HexColor("#C084FC")   # purple
C_CODE_BG   = colors.HexColor("#1E293B")   # code panel
C_CODE_FG   = colors.HexColor("#E2E8F0")   # code text
C_HEADING   = colors.HexColor("#F1F5F9")   # near-white
C_BODY      = colors.HexColor("#CBD5E1")   # light slate
C_MUTED     = colors.HexColor("#64748B")   # muted slate
C_BORDER    = colors.HexColor("#334155")   # subtle border
C_CARD      = colors.HexColor("#1E293B")   # card bg
C_HIGHLIGHT = colors.HexColor("#0EA5E9")   # bright blue

PAGE_W, PAGE_H = letter

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Prefix_Sum_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S("sTitle",
    fontName="Helvetica-Bold", fontSize=32, leading=40,
    textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)

sSubtitle = S("sSubtitle",
    fontName="Helvetica", fontSize=13, leading=18,
    textColor=C_ACCENT, alignment=TA_CENTER, spaceAfter=4)

sAuthor = S("sAuthor",
    fontName="Helvetica-Oblique", fontSize=10,
    textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=20)

sH1 = S("sH1",
    fontName="Helvetica-Bold", fontSize=20, leading=26,
    textColor=C_ACCENT, spaceBefore=18, spaceAfter=8)

sH2 = S("sH2",
    fontName="Helvetica-Bold", fontSize=14, leading=19,
    textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)

sH3 = S("sH3",
    fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=C_GREEN, spaceBefore=8, spaceAfter=4)

sBody = S("sBody",
    fontName="Helvetica", fontSize=10, leading=15,
    textColor=C_BODY, spaceAfter=6, alignment=TA_JUSTIFY)

sBullet = S("sBullet",
    fontName="Helvetica", fontSize=10, leading=14,
    textColor=C_BODY, spaceAfter=3,
    leftIndent=16, bulletIndent=4)

sCode = S("sCode",
    fontName="Courier", fontSize=8.5, leading=13,
    textColor=C_CODE_FG, spaceAfter=2,
    leftIndent=12, rightIndent=12,
    backColor=C_CODE_BG)

sCodeComment = S("sCodeComment",
    fontName="Courier-Oblique", fontSize=8.5, leading=13,
    textColor=C_MUTED, spaceAfter=2,
    leftIndent=12, rightIndent=12,
    backColor=C_CODE_BG)

sLabel = S("sLabel",
    fontName="Helvetica-Bold", fontSize=9,
    textColor=C_YELLOW, spaceAfter=2)

sNote = S("sNote",
    fontName="Helvetica-Oblique", fontSize=9, leading=13,
    textColor=C_YELLOW, spaceAfter=4)

sFormula = S("sFormula",
    fontName="Courier-Bold", fontSize=10, leading=14,
    textColor=C_GREEN, alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=4)

sCaption = S("sCaption",
    fontName="Helvetica-Oblique", fontSize=8.5,
    textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=6)

sTOC = S("sTOC",
    fontName="Helvetica", fontSize=10, leading=16,
    textColor=C_BODY, leftIndent=0)

sTOCSub = S("sTOCSub",
    fontName="Helvetica", fontSize=9, leading=14,
    textColor=C_MUTED, leftIndent=18)

sTag = S("sTag",
    fontName="Helvetica-Bold", fontSize=8,
    textColor=C_BG, spaceAfter=2)

# ── Custom Flowables ────────────────────────────────────────────────────────────
class ColorRect(Flowable):
    def __init__(self, w, h, color, radius=4):
        self.w, self.h, self.color, self.r = w, h, color, radius
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.w, self.h, self.r, fill=1, stroke=0)
    def wrap(self, *args): return self.w, self.h

class HRule(Flowable):
    def __init__(self, color=C_BORDER, thickness=1, spaceB=6):
        self.color, self.t, self.spaceB = color, thickness, spaceB
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.t)
        self.canv.line(0, 0, self.width, 0)
    def wrap(self, avail_w, avail_h):
        self.width = avail_w
        return avail_w, self.t + self.spaceB

def badge(text, bg=C_ACCENT, fg=C_BG):
    return Table([[Paragraph(f"<b>{text}</b>", S("_", fontName="Helvetica-Bold",
        fontSize=8, textColor=fg))]],
        colWidths=[len(text)*6+14],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('ROUNDEDCORNERS', [4]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ]))

def code_block(lines, lang="python"):
    """Render a styled code block"""
    elems = []
    # header bar
    header = Table([[Paragraph(f"<b>{lang}</b>",
        S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
        colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0D1929")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
        ]))
    rows = []
    for line in lines:
        if line.startswith("##"):
            rows.append([Paragraph(line, sCodeComment)])
        else:
            rows.append([Paragraph(line if line else " ", sCode)])
    code_tbl = Table(rows, colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
    wrapper = Table([[header], [code_tbl]],
        colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BOX', (0,0), (-1,-1), 1, C_BORDER),
            ('ROUNDEDCORNERS', [4]),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
    elems.append(wrapper)
    elems.append(Spacer(1, 8))
    return elems

def callout(text, color=C_ACCENT, icon="💡"):
    tbl = Table([[Paragraph(f"{icon}  {text}",
        S("_", fontName="Helvetica", fontSize=9.5, leading=14, textColor=color))]],
        colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0C1F35")),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ('TOPPADDING', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 9),
            ('LINEBEFORE', (0,0), (0,-1), 3, color),
        ]))
    return [tbl, Spacer(1, 6)]

def section_divider(num, title):
    return [
        Spacer(1, 10),
        Table([[
            Paragraph(f"<b>{num:02d}</b>",
                S("_", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT)),
            Paragraph(f"<b>{title}</b>",
                S("_", fontName="Helvetica-Bold", fontSize=18, textColor=C_HEADING,
                  leading=24)),
        ]], colWidths=[40, PAGE_W - 1.3*inch - 40],
        style=TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (0,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 2, C_ACCENT),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ])),
        Spacer(1, 8),
    ]

# ── Build Story ────────────────────────────────────────────────────────────────
story = []
P = Paragraph  # shorthand

# ════════════════════════════════════════════════════════
# COVER PAGE
# ════════════════════════════════════════════════════════
story.append(Spacer(1, 0.5*inch))

# Big accent bar at top
story.append(Table([[""]], colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_ACCENT),
        ('ROWHEIGHT', (0,0), (-1,-1), 6),
    ])))
story.append(Spacer(1, 0.3*inch))

story.append(P("PREFIX SUM", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Intuition · Patterns · Problems · Edge Cases", sAuthor))
story.append(Spacer(1, 0.2*inch))

# Cover summary card
cover_data = [
    [P("<b>What You Will Master</b>",
       S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· 1D &amp; 2D Prefix Sums (Summed-Area Tables)\n· Prefix Sum + HashMap for subarray problems\n· Difference Arrays for range updates\n· XOR Prefix, Suffix Sums, Product arrays\n· 20+ categorized LeetCode problems\n· Pattern recognition &amp; decision framework",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))],
]
cover_tbl = Table(cover_data, colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
    ]))
story.append(cover_tbl)
story.append(Spacer(1, 0.3*inch))

# Complexity quick ref on cover
cx_data = [
    [P("<b>Brute Force Query</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>After Preprocessing</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Build Cost</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("O(n) per query", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_RED)),
     P("O(1) per query", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_GREEN)),
     P("O(n) one-time", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_YELLOW))],
]
cx_tbl = Table(cx_data, colWidths=[(PAGE_W - 1.3*inch)/3]*3,
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0A1628")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
story.append(cx_tbl)
story.append(Spacer(1, 0.4*inch))

story.append(Table([[""]], colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_ACCENT2),
        ('ROWHEIGHT', (0,0), (-1,-1), 4),
    ])))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════════════════════
story += section_divider(0, "Table of Contents")

toc_items = [
    ("01", "Foundations of Prefix Sum", [
        "What is Prefix Sum?",
        "Brute Force vs. Prefix Sum",
        "1-Based vs 0-Based Indexing",
    ]),
    ("02", "Core Pattern: 1D Prefix Sum", [
        "Building the Prefix Array",
        "The Range Query Formula",
        "Visual Walkthrough",
    ]),
    ("03", "Core Pattern: 2D Prefix Sum", [
        "Summed-Area Table Construction",
        "Inclusion-Exclusion Principle",
        "Sub-Rectangle Query",
    ]),
    ("04", "Core Pattern: Prefix Sum + HashMap", [
        "Why HashMap?",
        "Finding Subarrays with Sum K",
        "Handling Negatives & Zero",
    ]),
    ("05", "Comparison & Decision Making", [
        "Prefix Sum vs. Sliding Window",
        "Difference Arrays",
        "When to Use What",
    ]),
    ("06", "Advanced Variations", [
        "Suffix Sums",
        "Product of Array Except Self",
        "XOR Prefix",
    ]),
    ("07", "Problem Roadmap", [
        "Easy Problems",
        "Medium Problems",
        "Hard Problems",
    ]),
    ("08", "Edge Cases & Pitfalls", [
        "Empty Arrays & Single Elements",
        "K=0 and Negative Values",
        "Integer Overflow",
    ]),
]

for num, title, subs in toc_items:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1, 3))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 1: FOUNDATIONS
# ════════════════════════════════════════════════════════
story += section_divider(1, "Foundations of Prefix Sum")

story.append(P("<b>What is a Prefix Sum?</b>", sH2))
story.append(P(
    "A <b>prefix sum</b> (also called a <i>cumulative sum</i> or <i>scan</i>) is a precomputed "
    "array where each element at index <b>i</b> stores the <b>sum of all original elements "
    "from index 0 up to and including index i</b>. It is one of the most powerful and "
    "versatile preprocessing techniques in competitive programming and interview prep.",
    sBody))

story.append(P(
    "The key insight is deceptively simple: if you want to answer many range-sum queries "
    "on the same array, doing it naively costs O(n) per query. By investing O(n) once to "
    "build a prefix array, every future query drops to O(1). This is the classic "
    "<b>precompute once, query many times</b> paradigm.",
    sBody))

story += callout(
    "Core Intuition: A prefix sum transforms repeated range-sum queries from O(n) "
    "each into O(1) each, at the cost of O(n) preprocessing time and O(n) space.",
    C_ACCENT)

# --- Brute Force vs Prefix Sum ---
story.append(P("<b>Brute Force vs. Prefix Sum: The Performance Argument</b>", sH2))
story.append(P(
    "Imagine you have an array of n numbers and you receive Q range-sum queries. "
    "Each query asks: <i>what is the sum of elements from index L to R?</i>",
    sBody))

perf_data = [
    [P("<b>Approach</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Preprocessing</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Per Query</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Q Queries Total</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Brute Force Loop", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("O(1)", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN)),
     P("O(n)", S("_", fontName="Courier", fontSize=9, textColor=C_RED)),
     P("O(n * Q)", S("_", fontName="Courier", fontSize=9, textColor=C_RED))],
    [P("Prefix Sum", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("O(n)", S("_", fontName="Courier", fontSize=9, textColor=C_YELLOW)),
     P("O(1)", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN)),
     P("O(n + Q)", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN))],
]
perf_tbl = Table(perf_data, colWidths=[160, 100, 100, 120],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,1), C_CARD),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#0A1E10")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,-1), 10),
    ]))
story.append(perf_tbl)
story.append(Spacer(1, 8))

story.append(P(
    "For n=10,000 and Q=10,000 queries: brute force does ~100 million operations; "
    "prefix sum does ~20,000. That is a <b>5000x speedup</b>. This is why prefix sums "
    "appear in almost every domain: finance, signal processing, image convolution, and "
    "of course, algorithm interviews.",
    sBody))

# --- 0-based vs 1-based ---
story.append(P("<b>Indexing Convention: 0-Based vs 1-Based</b>", sH2))
story.append(P(
    "There are two common conventions for building prefix sum arrays. Understanding "
    "both is critical because the LeetCode community and textbooks mix them freely.",
    sBody))

story.append(P("<b>Convention A: 0-Based (Direct Mapping)</b>", sH3))
story.append(P(
    "prefix[i] holds the sum of arr[0..i] inclusive. The range query for [L, R] is "
    "then prefix[R] - prefix[L-1], with a special case when L=0.",
    sBody))
story += code_block([
    "## 0-based prefix sum",
    "arr     = [3, 1, 4, 1, 5, 9, 2, 6]",
    "prefix  = [0] * len(arr)",
    "",
    "prefix[0] = arr[0]",
    "for i in range(1, len(arr)):",
    "    prefix[i] = prefix[i-1] + arr[i]",
    "",
    "## Query sum of arr[L..R]",
    "def query(L, R):",
    "    if L == 0:",
    "        return prefix[R]",
    "    return prefix[R] - prefix[L-1]   ## Special case needed when L=0",
])

story.append(P("<b>Convention B: 1-Based (Dummy Element — RECOMMENDED)</b>", sH3))
story.append(P(
    "A dummy element <b>prefix[0] = 0</b> is prepended. Now prefix[i] holds the sum "
    "of the first i elements (arr[0..i-1]). The range query for arr[L..R] (0-indexed) "
    "becomes prefix[R+1] - prefix[L] with <b>no special case needed</b>. This is "
    "cleaner and less error-prone.",
    sBody))
story += code_block([
    "## 1-based prefix sum (RECOMMENDED convention)",
    "arr    = [3, 1, 4, 1, 5, 9, 2, 6]   ## 0-indexed",
    "n      = len(arr)",
    "prefix = [0] * (n + 1)              ## size n+1, prefix[0]=0 is the sentinel",
    "",
    "for i in range(1, n + 1):",
    "    prefix[i] = prefix[i-1] + arr[i-1]",
    "",
    "## prefix now looks like: [0, 3, 4, 8, 9, 14, 23, 25, 31]",
    "",
    "## Query sum of arr[L..R] (both 0-indexed, inclusive)",
    "def query(L, R):",
    "    return prefix[R+1] - prefix[L]   ## Clean! No special case.",
])

story += callout(
    "The 1-based convention with a dummy prefix[0]=0 is universally preferred in "
    "interviews because it eliminates the L=0 edge case and makes the formula "
    "prefix[R+1] - prefix[L] uniformly applicable.",
    C_GREEN, icon="✅")

# Visual array diagram
story.append(P("<b>Visual: What prefix[i] represents</b>", sH3))
arr_vals = [3, 1, 4, 1, 5, 9]
pre_vals = [0, 3, 4, 8, 9, 14, 23]
idx_row = [P("<b>Index</b>", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_MUTED))] + \
    [P(str(i), S("_", fontName="Courier-Bold", fontSize=9, textColor=C_MUTED, alignment=TA_CENTER))
     for i in range(len(arr_vals))]
arr_row = [P("<b>arr[ ]</b>", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_ACCENT2))] + \
    [P(str(v), S("_", fontName="Courier-Bold", fontSize=11, textColor=C_ACCENT, alignment=TA_CENTER))
     for v in arr_vals]
pre_idx = [P("<b>prefix[i]</b>", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_ACCENT2))] + \
    [P(str(v), S("_", fontName="Courier-Bold", fontSize=11, textColor=C_GREEN, alignment=TA_CENTER))
     for v in pre_vals[1:]]
pre_row0 = [P("<b>Sentinel</b>", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_MUTED)),
    P("prefix[0]=0", S("_", fontName="Courier", fontSize=8, textColor=C_MUTED, alignment=TA_CENTER))] + \
    [P("", sBody)] * (len(arr_vals)-1)

cw = [80] + [55]*len(arr_vals)
vis_tbl = Table([idx_row, arr_row, pre_idx],
    colWidths=cw,
    style=TableStyle([
        ('BACKGROUND', (0,0), (0,-1), C_BG),
        ('BACKGROUND', (1,0), (-1,0), C_BG),
        ('BACKGROUND', (1,1), (-1,1), C_CARD),
        ('BACKGROUND', (1,2), (-1,2), colors.HexColor("#0A1E10")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
story.append(vis_tbl)
story.append(P("prefix[i] accumulates the running sum up to position i (1-based)", sCaption))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2: 1D PREFIX SUM
# ════════════════════════════════════════════════════════
story += section_divider(2, "Core Pattern: 1D Prefix Sum")

story.append(P("<b>The Master Formula</b>", sH2))
story.append(P(
    "Once the prefix array is built using the 1-based convention, any contiguous "
    "subarray sum query is answered in O(1) using a single subtraction:",
    sBody))

story.append(P("Sum(L, R)  =  prefix[R+1]  −  prefix[L]", sFormula))

story.append(P(
    "Intuitively: prefix[R+1] is the total sum from the start up to R. "
    "prefix[L] is the total sum from the start up to L-1. "
    "Subtracting removes the left portion you don't want, leaving exactly the sum "
    "from L to R.",
    sBody))

story += callout(
    "Mental model: Think of prefix sums like odometer readings. "
    "To find the distance traveled between mile-marker A and mile-marker B, "
    "you simply compute odometer_B - odometer_A.",
    C_ACCENT2, icon="🚗")

story.append(P("<b>Step-by-Step: Building and Querying</b>", sH2))
story += code_block([
    "## ─── STEP 1: Build the prefix array ──────────────────────────",
    "def build_prefix(arr):",
    '    """',
    "    Given a list of numbers, return a prefix sum array (1-based).",
    "    prefix[0] = 0  (sentinel / dummy element)",
    "    prefix[i] = arr[0] + arr[1] + ... + arr[i-1]",
    '    """',
    "    n = len(arr)",
    "    prefix = [0] * (n + 1)",
    "    for i in range(1, n + 1):",
    "        prefix[i] = prefix[i - 1] + arr[i - 1]",
    "    return prefix",
    "",
    "## ─── STEP 2: Answer range sum queries in O(1) ──────────────────",
    "def range_sum(prefix, L, R):",
    '    """',
    "    Returns sum of arr[L..R] (0-indexed, both inclusive).",
    "    Converts to 1-based: prefix[R+1] - prefix[L]",
    '    """',
    "    return prefix[R + 1] - prefix[L]",
    "",
    "## ─── Example Usage ─────────────────────────────────────────────",
    "arr    = [2, 4, 6, 8, 10]",
    "prefix = build_prefix(arr)  ## [0, 2, 6, 12, 20, 30]",
    "",
    "print(range_sum(prefix, 1, 3))  ## arr[1]+arr[2]+arr[3] = 4+6+8 = 18",
    "print(range_sum(prefix, 0, 4))  ## entire array = 30",
    "print(range_sum(prefix, 2, 2))  ## single element = 6",
])

story.append(P("<b>Visual Walkthrough: Tracing a Query</b>", sH2))
story.append(P(
    "Let's trace <b>range_sum(prefix, 1, 3)</b> on arr = [2, 4, 6, 8, 10] step by step:",
    sBody))

trace_data = [
    [P("<b>Step</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Operation</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Value</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Meaning</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("1", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("prefix[R+1] = prefix[4]", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
     P("20", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_GREEN)),
     P("Sum of arr[0..3] = 2+4+6+8", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("2", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("prefix[L] = prefix[1]", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
     P("2", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_RED)),
     P("Sum of arr[0..0] = 2 (to be removed)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("3", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("prefix[4] - prefix[1]", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
     P("18", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_GREEN)),
     P("Sum of arr[1..3] = 4+6+8 ✓", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
]
trace_tbl = Table(trace_data, colWidths=[40, 160, 60, 220],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,1), C_CARD),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#1A1030")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#0A1E10")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
story.append(trace_tbl)
story.append(Spacer(1, 8))

story.append(P("<b>Pattern Recognition Template</b>", sH2))
story.append(P(
    "You should reach for a 1D prefix sum when you see these signals in a problem:",
    sBody))

signals = [
    ("🔍", "Array + multiple range sum queries", "Build prefix, answer in O(1)"),
    ("🔍", "\"Sum of subarray\" or \"contiguous elements\"", "Prefix sum is almost always involved"),
    ("🔍", "Fixed array, many queries", "Preprocessing pays off"),
    ("🔍", "Need to compare sums of sub-segments", "Compute both with prefix, subtract"),
]
for icon, signal, action in signals:
    row_tbl = Table([[
        P(icon, S("_", fontSize=12, alignment=TA_CENTER)),
        P(f"<b>{signal}</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
        P(f"→ {action}", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[28, 220, 230],
    style=TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(row_tbl)

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3: 2D PREFIX SUM
# ════════════════════════════════════════════════════════
story += section_divider(3, "Core Pattern: 2D Prefix Sum")

story.append(P("<b>Extending to Two Dimensions</b>", sH2))
story.append(P(
    "The same concept extends naturally to 2D grids (matrices). Given a matrix, "
    "we precompute a <b>Summed-Area Table</b> (also called a 2D prefix sum or "
    "integral image) so that any sub-rectangle sum can be answered in O(1).",
    sBody))

story.append(P(
    "prefix[i][j] stores the sum of all elements in the sub-rectangle from "
    "the top-left corner (0,0) to (i-1, j-1). Just like 1D, we use a "
    "1-based convention with an extra row and column of zeros.",
    sBody))

story.append(P("<b>Building the Summed-Area Table</b>", sH2))
story.append(P("The construction formula uses overlapping rectangles:", sBody))

story.append(P("prefix[i][j]  =  matrix[i-1][j-1]  +  prefix[i-1][j]  +  prefix[i][j-1]  −  prefix[i-1][j-1]", sFormula))

story.append(P(
    "We add the element itself, plus the rectangle above, plus the rectangle to the left, "
    "then subtract the overlap (top-left rectangle) which was counted twice.",
    sBody))

story += code_block([
    "## ─── Build 2D Prefix Sum (1-based) ───────────────────────────",
    "def build_2d_prefix(matrix):",
    "    rows, cols = len(matrix), len(matrix[0])",
    "    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]",
    "",
    "    for i in range(1, rows + 1):",
    "        for j in range(1, cols + 1):",
    "            prefix[i][j] = (matrix[i-1][j-1]",
    "                          + prefix[i-1][j]    ## rectangle above",
    "                          + prefix[i][j-1]    ## rectangle to left",
    "                          - prefix[i-1][j-1]) ## subtract double-counted overlap",
    "    return prefix",
    "",
    "## ─── Query: sum of sub-rectangle (r1,c1) to (r2,c2) (0-indexed) ─",
    "def rect_sum(prefix, r1, c1, r2, c2):",
    "    ## Convert to 1-based: add 1 to r2, c2; r1, c1 stay as-is",
    "    return (prefix[r2+1][c2+1]",
    "          - prefix[r1][c2+1]    ## remove top strip",
    "          - prefix[r2+1][c1]    ## remove left strip",
    "          + prefix[r1][c1])     ## add back top-left corner (subtracted twice)",
])

story.append(P("<b>Inclusion-Exclusion Principle: Visual Breakdown</b>", sH2))
story.append(P(
    "The query formula is driven by the inclusion-exclusion principle. "
    "Here is how to visualize it for a query on sub-rectangle (r1,c1) to (r2,c2):",
    sBody))

ie_data = [
    [P("<b>Term</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>What it represents</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Operation</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("prefix[r2+1][c2+1]", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN)),
     P("Big rectangle from (0,0) to (r2,c2)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("+ (start here)", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("prefix[r1][c2+1]", S("_", fontName="Courier", fontSize=9, textColor=C_RED)),
     P("Strip above the target (rows 0..r1-1, all cols)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("− (remove)", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED))],
    [P("prefix[r2+1][c1]", S("_", fontName="Courier", fontSize=9, textColor=C_RED)),
     P("Strip left of target (all rows, cols 0..c1-1)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("− (remove)", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED))],
    [P("prefix[r1][c1]", S("_", fontName="Courier", fontSize=9, textColor=C_YELLOW)),
     P("Top-left corner (rows 0..r1-1, cols 0..c1-1)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("+ (add back — was subtracted twice)", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW))],
]
ie_tbl = Table(ie_data, colWidths=[140, 250, 90],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#0A1E10")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#1A1010")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#1A1010")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#1A1508")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
story.append(ie_tbl)
story.append(P("The inclusion-exclusion principle ensures exact sub-rectangle coverage with no double-counting", sCaption))

story += callout(
    "Memory aid for the 2D query: 'Big MINUS top-strip MINUS left-strip PLUS corner'. "
    "Draw a big rectangle, cut the top, cut the left, patch back the corner you cut twice.",
    C_PURPLE, icon="🧩")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4: PREFIX SUM + HASHMAP
# ════════════════════════════════════════════════════════
story += section_divider(4, "Core Pattern: Prefix Sum + HashMap")

story.append(P("<b>Why Combine Prefix Sum with a HashMap?</b>", sH2))
story.append(P(
    "The 1D prefix sum tells us the sum from index 0 to any index i. But what if "
    "we want to find a <b>subarray with a specific sum K</b>? A naive approach "
    "tries all (L, R) pairs: O(n<super>2</super>). The prefix sum reduces each "
    "query to O(1), but we still need to find the right pair.",
    sBody))

story.append(P(
    "The key insight: we need sum(L, R) = K, which means prefix[R+1] - prefix[L] = K, "
    "which means <b>prefix[L] = prefix[R+1] - K</b>. So as we scan left-to-right "
    "computing running prefix sums, we ask: <i>\"have I seen a prefix sum equal to "
    "(current_prefix - K) before?\"</i> A HashMap answers this in O(1).",
    sBody))

story.append(P("We need:  prefix[R+1] − prefix[L]  =  K   →   prefix[L]  =  prefix[R+1] − K", sFormula))

story += callout(
    "This is the #1 most tested prefix sum pattern on LeetCode. "
    "Mastering it unlocks ~15 medium/hard problems instantly.",
    C_YELLOW, icon="⭐")

story += code_block([
    "## ─── Find number of subarrays with sum exactly K ───────────────",
    "def count_subarrays_with_sum_k(arr, K):",
    '    """',
    "    Uses prefix sum + hashmap.",
    "    Time: O(n)   Space: O(n)",
    '    """',
    "    count        = 0",
    "    running_sum  = 0",
    "    ## Seed the map: a prefix sum of 0 has occurred once (before any element)",
    "    prefix_count = {0: 1}",
    "",
    "    for num in arr:",
    "        running_sum += num",
    "",
    "        ## Check: have we seen (running_sum - K) before?",
    "        complement = running_sum - K",
    "        if complement in prefix_count:",
    "            count += prefix_count[complement]",
    "",
    "        ## Record this prefix sum",
    "        prefix_count[running_sum] = prefix_count.get(running_sum, 0) + 1",
    "",
    "    return count",
])

story.append(P("<b>Handling Negatives and K=0</b>", sH2))
story.append(P(
    "Unlike the sliding window technique (which requires non-negative numbers for "
    "monotonicity), the HashMap approach works flawlessly with <b>negative numbers</b> "
    "and <b>K=0</b>. This is its biggest advantage.",
    sBody))

neg_data = [
    [P("<b>Scenario</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Sliding Window</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Prefix + HashMap</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("All non-negative, sum = K",  S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("✅ Works perfectly", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("✅ Works perfectly", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("Contains negatives, sum = K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("❌ Breaks (no monotonicity)", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("✅ Works perfectly", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("K = 0", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("⚠️  Tricky edge case", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("✅ Handled by {0:1} seed", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("Count all valid subarrays", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("❌ Complex modification needed", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("✅ Count by map lookup", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
]
neg_tbl = Table(neg_data, colWidths=[180, 150, 150],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,-1), C_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
story.append(neg_tbl)
story.append(Spacer(1, 8))

story.append(P("<b>Why {0: 1} is seeded in the HashMap</b>", sH3))
story.append(P(
    "The seed {0: 1} represents: <i>\"before processing any element, we have seen a "
    "prefix sum of 0 exactly once.\"</i> Without this, we miss subarrays that start "
    "from index 0. For example, if K=3 and the array starts with [1,2,...], the "
    "subarray arr[0..1] sums to 3. We need running_sum - K = 3 - 3 = 0 to be in "
    "our map when we process index 1. The seed ensures it is.",
    sBody))

story += callout(
    "Always seed the HashMap with {0: 1} before entering the loop. "
    "Forgetting this is one of the most common interview bugs for this pattern.",
    C_RED, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5: COMPARISON & DECISION MAKING
# ════════════════════════════════════════════════════════
story += section_divider(5, "Comparison & Decision Making")

story.append(P("<b>Prefix Sum vs. Sliding Window: Choose Wisely</b>", sH2))
story.append(P(
    "Prefix Sum and Sliding Window are the two dominant O(n) techniques for "
    "contiguous subarray problems. Knowing which to apply is a key interview skill.",
    sBody))

sw_data = [
    [P("<b>Dimension</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Prefix Sum (+ HashMap)</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("<b>Sliding Window</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_PURPLE))],
    [P("Negative numbers", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("✅ Fully supported", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("❌ Breaks (no monotonicity)", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED))],
    [P("K = 0", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("✅ Natural (seed {0:1})", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("⚠️  Special handling needed", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW))],
    [P("Count of valid subarrays", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("✅ Map stores frequencies", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("⚠️  Requires careful counting", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW))],
    [P("Exact sum = K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("✅ Direct complement lookup", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("⚠️  Works only for non-negatives", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW))],
    [P("Maximum/minimum subarray", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("⚠️  Possible but indirect", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("✅ Natural fit (expand/contract)", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("Sum at most K / at least K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("⚠️  Needs sorted map / trick", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("✅ Natural expand/shrink", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("Space complexity", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("O(n) for prefix array + map", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("O(1) extra space", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN))],
    [P("Requires monotonicity?", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("❌ No", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("✅ Yes (window must shrink predictably)", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED))],
]
sw_tbl = Table(sw_data, colWidths=[165, 175, 140],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,-1), C_CARD),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
story.append(sw_tbl)
story.append(Spacer(1, 8))

story += callout(
    "Decision rule: If the array can contain negative numbers, or if you need to count "
    "exact matches, default to Prefix Sum + HashMap. If the array is non-negative and "
    "you need a maximum/minimum length window, try Sliding Window first.",
    C_ACCENT, icon="🎯")

# --- Difference Arrays ---
story.append(P("<b>Difference Arrays: The Inverse of Prefix Sum</b>", sH2))
story.append(P(
    "A <b>Difference Array</b> is the conceptual inverse of a prefix sum. While prefix "
    "sums are optimized for <i>range queries</i>, difference arrays are optimized for "
    "<i>range updates</i> — adding a constant to every element in a range [L, R].",
    sBody))

story.append(P(
    "A naive range update costs O(n) per operation. With a difference array, each "
    "range update costs O(1), and the final array is recovered in O(n) with one "
    "prefix sum pass at the end.",
    sBody))

story.append(P("diff[L] += val     diff[R+1] -= val     →     then prefix-sum diff to get result", sFormula))

story += code_block([
    "## ─── Difference Array for range updates ───────────────────────",
    "def range_updates(n, updates):",
    '    """',
    "    Apply multiple range updates to an array of zeros.",
    "    Each update: (L, R, val) adds val to arr[L..R].",
    "    Time: O(n + Q)  instead of O(n * Q)",
    '    """',
    "    diff = [0] * (n + 1)          ## difference array with sentinel",
    "",
    "    for L, R, val in updates:",
    "        diff[L]     += val         ## start the effect at L",
    "        diff[R + 1] -= val         ## cancel the effect after R",
    "",
    "    ## Recover the actual array by prefix-summing diff",
    "    result = [0] * n",
    "    running = 0",
    "    for i in range(n):",
    "        running    += diff[i]",
    "        result[i]   = running",
    "",
    "    return result",
    "",
    "## ─── Example ────────────────────────────────────────────────────",
    "## n=6, updates: [(1,3,+5), (2,5,+3), (0,2,-2)]",
    "## After all updates: [-2, 3, 6, 8, 3, 3]",
])

story += callout(
    "Think of diff[L] += val as 'turn on a faucet at L' and diff[R+1] -= val as "
    "'turn it off after R'. The prefix sum accumulates all the flowing water.",
    C_ACCENT2, icon="🚰")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6: ADVANCED VARIATIONS
# ════════════════════════════════════════════════════════
story += section_divider(6, "Advanced Variations")

story.append(P("<b>Suffix Sums</b>", sH2))
story.append(P(
    "A <b>suffix sum</b> is the mirror image of a prefix sum: suffix[i] stores the sum "
    "of elements from index i to the end of the array. They appear in problems that "
    "involve comparing left vs. right halves, or where you need to evaluate 'cost "
    "from here to the end.'",
    sBody))

story += code_block([
    "## ─── Suffix Sum Array ──────────────────────────────────────────",
    "def build_suffix(arr):",
    "    n = len(arr)",
    "    suffix = [0] * (n + 1)       ## suffix[n] = 0 (sentinel)",
    "    for i in range(n - 1, -1, -1):",
    "        suffix[i] = suffix[i + 1] + arr[i]",
    "    return suffix",
    "",
    "## Use case: find pivot index where left_sum == right_sum",
    "def find_pivot(arr):",
    "    prefix = build_prefix(arr)   ## from Section 2",
    "    suffix = build_suffix(arr)",
    "    for i in range(len(arr)):",
    "        if prefix[i] == suffix[i + 1]:  ## left sum == right sum",
    "            return i",
    "    return -1",
])

story.append(P("<b>Product of Array Except Self</b>", sH2))
story.append(P(
    "This classic problem asks for an output array where output[i] = product of all "
    "elements in arr except arr[i], <b>without using division and in O(n) time</b>. "
    "The solution uses a prefix-product pass (left-to-right) and a suffix-product "
    "pass (right-to-left) combined in a single output array.",
    sBody))

story += code_block([
    "## ─── Product Except Self ───────────────────────────────────────",
    "def product_except_self(arr):",
    '    """',
    "    Two-pass approach using prefix and suffix products.",
    "    Space-optimized: O(1) extra space (not counting output).",
    '    """',
    "    n = len(arr)",
    "    output = [1] * n",
    "",
    "    ## Pass 1 (left to right): output[i] = product of all elements LEFT of i",
    "    left_product = 1",
    "    for i in range(n):",
    "        output[i]    = left_product",
    "        left_product *= arr[i]",
    "",
    "    ## Pass 2 (right to left): multiply by product of all elements RIGHT of i",
    "    right_product = 1",
    "    for i in range(n - 1, -1, -1):",
    "        output[i]     *= right_product",
    "        right_product  *= arr[i]",
    "",
    "    return output",
    "",
    "## arr = [1, 2, 3, 4]  →  output = [24, 12, 8, 6]",
])

story.append(P("<b>XOR-Based Prefix</b>", sH2))
story.append(P(
    "XOR has a beautiful property: <b>x XOR x = 0</b> and <b>x XOR 0 = x</b>. "
    "This makes XOR prefix sums powerful for range-XOR queries. If prefix_xor[i] "
    "is the XOR of arr[0..i-1], then the XOR of arr[L..R] is simply "
    "prefix_xor[R+1] XOR prefix_xor[L] — the same subtraction-style formula, "
    "but with XOR instead of minus.",
    sBody))

story += code_block([
    "## ─── XOR Prefix Sum ────────────────────────────────────────────",
    "def build_xor_prefix(arr):",
    "    n = len(arr)",
    "    xor_prefix = [0] * (n + 1)   ## xor_prefix[0] = 0 (identity for XOR)",
    "    for i in range(1, n + 1):",
    "        xor_prefix[i] = xor_prefix[i - 1] ^ arr[i - 1]",
    "    return xor_prefix",
    "",
    "## XOR of arr[L..R] in O(1)",
    "def xor_range(xor_prefix, L, R):",
    "    return xor_prefix[R + 1] ^ xor_prefix[L]",
    "",
    "## Common use: find if XOR of subarray = 0 → duplicates / cancellation",
    "## Also used in: XOR triplets, single non-duplicate element problems",
])

story += callout(
    "The XOR prefix technique generalizes to any associative binary operation with "
    "an identity element and an inverse (XOR is its own inverse). This is why the "
    "formula looks identical to the sum version.",
    C_PURPLE, icon="⚡")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7: PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(7, "LeetCode Problem Roadmap")

story.append(P(
    "Problems are organized by difficulty and sub-pattern. Work through them in "
    "order — each level reinforces the pattern from the previous.",
    sBody))

# Easy Problems
story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("303", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Range Sum Query - Immutable", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("1D Basic", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("The canonical intro problem. Build prefix once, query many times.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1480", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Running Sum of 1D Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("1D Basic", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("The prefix array IS the answer. In-place possible.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("724", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Find Pivot Index", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + Suffix", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("left_sum == right_sum at pivot. Use total sum trick.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1991", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Find the Middle Index", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + Suffix", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Variant of 724. Same pattern.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("2574", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Left and Right Sum Differences", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + Suffix", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("|prefix[i] - suffix[i]| for each index.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1422", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Maximum Score After Splitting", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + Suffix", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Try all split points using precomputed suffix sums.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
easy_tbl = Table(easy_data, colWidths=[38, 180, 90, 172],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ]))
story.append(easy_tbl)
story.append(Spacer(1, 10))

# Medium Problems
story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("560", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Subarray Sum Equals K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("The definitive HashMap pattern. Seed {0:1}.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("974", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Subarray Sums Divisible by K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("Store prefix % K in map. Two equal remainders = valid subarray.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("525", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Contiguous Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("Replace 0s with -1; find longest subarray with sum 0.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("304", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Range Sum Query 2D - Immutable", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("2D Prefix", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("Summed-Area Table. The canonical 2D problem.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("238", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Product of Array Except Self", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix × Suffix", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("No division. Left-pass then right-pass on output array.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1248", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Count Number of Nice Subarrays", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("Replace even=0, odd=1; find subarrays with sum=K.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1524", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Number of Sub-arrays with Odd Sum", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Prefix Parity", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Track odd/even prefix counts. Odd sum iff different parity.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1109", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Corporate Flight Bookings", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Difference Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("Classic range-update → prefix sum to recover final array.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1094", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Car Pooling", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Difference Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("Passengers board/alight at stops. Diff array + check max.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
med_tbl = Table(med_data, colWidths=[38, 180, 90, 172],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ]))
story.append(med_tbl)
story.append(Spacer(1, 10))

# Hard Problems
story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("1074", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Number of Submatrices that Sum to Target", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("2D + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("Fix top/bottom rows; compress to 1D; apply subarray-sum-K.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("363", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Max Sum of Rectangle No Larger Than K", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("2D + Sorted Set", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("2D prefix + SortedList to find best prefix in O(n log n).", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1542", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Find Longest Awesome Substring", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("XOR Prefix + HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("XOR bitmask for character frequency parity; find earliest same mask.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("1906", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Minimum Absolute Difference Queries", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("2D Prefix (value-dim)", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("Prefix count per value [1..100]; query range frequency.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
hard_tbl = Table(hard_data, colWidths=[38, 195, 90, 157],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ]))
story.append(hard_tbl)

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8: EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(8, "Edge Cases & Pitfalls")

story.append(P(
    "Even perfect pattern recognition fails if edge cases are not handled. "
    "These are the most common sources of bugs and wrong answers.",
    sBody))

story.append(P("<b>Edge Case 1: Empty Array</b>", sH3))
story.append(P(
    "Always guard against empty input before building any prefix array. An empty "
    "array produces prefix = [0], and any query on it is undefined. Return 0, -1, "
    "or [] as appropriate for the problem.",
    sBody))
story += code_block([
    "def safe_prefix(arr):",
    "    if not arr:          ## or: if len(arr) == 0",
    "        return [0]       ## sentinel only, no queries possible",
    "    ## ... normal build ...",
])

story.append(P("<b>Edge Case 2: Single Element</b>", sH3))
story.append(P(
    "With the 1-based convention, a single-element array [x] produces prefix = [0, x]. "
    "The query range_sum(prefix, 0, 0) = prefix[1] - prefix[0] = x. Works correctly "
    "with no special handling needed — this is another virtue of the 1-based sentinel.",
    sBody))

story.append(P("<b>Edge Case 3: K = 0 in HashMap Pattern</b>", sH3))
story.append(P(
    "When searching for subarrays with sum 0, the seed {0: 1} in the HashMap is "
    "critical. Without it, subarrays starting from index 0 with sum 0 are missed. "
    "Additionally, if the array contains zeros, multiple subarrays can have sum 0 "
    "even with non-zero elements — the HashMap counting handles this automatically.",
    sBody))
story += code_block([
    "## Example: arr = [1, -1, 2, -2, 3],  K = 0",
    "## Valid subarrays: [1,-1], [-1,2,-2,1 NO: entire prefix up to idx 3], [2,-2], [1,-1,2,-2]",
    "## Without seed {0:1}: misses the subarray arr[0..1] = [1,-1] because",
    "## when running_sum=0 at idx=1, complement=0-0=0 needs to be in map already.",
    "## With seed: prefix_count[0]=1 is found → count increments correctly.",
])

story.append(P("<b>Edge Case 4: Negative Numbers in HashMap Pattern</b>", sH3))
story.append(P(
    "Negative numbers do NOT break the Prefix + HashMap approach. They do, however, "
    "mean that prefix sums can decrease and revisit the same value multiple times. "
    "The HashMap must store <i>counts</i> (not just existence) to handle all cases:",
    sBody))
story += code_block([
    "## arr = [3, 4, -7, 5],  K = 0",
    "## Running prefix sums: 0, 3, 7, 0, 5",
    "## At index 2 (running_sum=0): complement=0 is in map with count=1 (the seed)",
    "## This correctly finds subarray arr[0..2] = [3,4,-7] which sums to 0",
    "## The map MUST store count=1 for 0 initially, not just True/False",
])

story.append(P("<b>Edge Case 5: Integer Overflow</b>", sH3))
story.append(P(
    "In Python, integers have arbitrary precision, so overflow is not a concern. "
    "In Java/C++ however, summing a large array of large integers can overflow int. "
    "Use long (64-bit) for prefix sums when values are large:",
    sBody))
story += code_block([
    "// Java: use long[] instead of int[]",
    "long[] prefix = new long[n + 1];",
    "",
    "// C++: use long long",
    "vector<long long> prefix(n + 1, 0LL);",
])

story.append(P("<b>Edge Case 6: Off-by-One in 2D Prefix</b>", sH3))
story.append(P(
    "The most common bug in 2D prefix sums is mixing up 0-indexed matrix coordinates "
    "with 1-indexed prefix coordinates. Always draw out the mapping:",
    sBody))
story += code_block([
    "## matrix[i][j]  ←→  prefix[i+1][j+1]   (accessing the element)",
    "## matrix row i     ←→  prefix row i+1",
    "## matrix col j     ←→  prefix col j+1",
    "",
    "## Sub-rectangle query for matrix rows r1..r2, cols c1..c2 (0-indexed):",
    "## prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]",
    "##        ↑                    ↑                   ↑                 ↑",
    "## bottom-right          top strip           left strip        corner patch",
])

story.append(P("<b>Quick Edge Case Checklist</b>", sH2))
checklist = [
    ("[ ]", "Guard against empty input before building prefix array"),
    ("[ ]", "Seed HashMap with {0: 1} before the loop for prefix+hashmap pattern"),
    ("[ ]", "In K=0 problems, verify the seed handles subarrays from index 0"),
    ("[ ]", "Use long/long long in typed languages for large value arrays"),
    ("[ ]", "In 2D, remember matrix[i][j] maps to prefix[i+1][j+1]"),
    ("[ ]", "For difference arrays, use size n+1 to avoid out-of-bounds on diff[R+1]"),
    ("[ ]", "Verify L <= R in range queries (caller contract vs. internal guard)"),
    ("[ ]", "For 'longest' subarray problems: store FIRST occurrence in HashMap, not last"),
]
for box, item in checklist:
    story.append(P(f"<b><font color='#34D399'>  {box}</font></b>  {item}",
        S("_", fontName="Helvetica", fontSize=9.5, leading=15, textColor=C_BODY,
          leftIndent=8, spaceAfter=3)))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# FINAL CHEAT SHEET
# ════════════════════════════════════════════════════════
story += section_divider(0, "Master Cheat Sheet")

story.append(P(
    "One-page reference for all the formulas, patterns, and decision rules covered "
    "in this guide. Keep this page bookmarked.",
    sBody))

cheat_data = [
    [P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Build Formula</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Query Formula</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Use When</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("1D Prefix Sum", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("prefix[i] = prefix[i-1] + arr[i-1]", S("_", fontName="Courier", fontSize=8, textColor=C_GREEN)),
     P("prefix[R+1] - prefix[L]", S("_", fontName="Courier", fontSize=8, textColor=C_GREEN)),
     P("Range sum queries, immutable array", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("2D Prefix Sum", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_PURPLE)),
     P("p[i][j] = mat+p[i-1][j]+p[i][j-1]-p[i-1][j-1]", S("_", fontName="Courier", fontSize=8, textColor=C_PURPLE)),
     P("p[r2+1][c2+1]-p[r1][c2+1]-p[r2+1][c1]+p[r1][c1]", S("_", fontName="Courier", fontSize=8, textColor=C_PURPLE)),
     P("Sub-rectangle sums on grid", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Prefix + HashMap", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_YELLOW)),
     P("map = {0:1}; running += num", S("_", fontName="Courier", fontSize=8, textColor=C_YELLOW)),
     P("if (running-K) in map: count += map[running-K]", S("_", fontName="Courier", fontSize=8, textColor=C_YELLOW)),
     P("Subarray sum = K, negatives OK", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Difference Array", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_RED)),
     P("diff[L]+=val; diff[R+1]-=val", S("_", fontName="Courier", fontSize=8, textColor=C_RED)),
     P("prefix-sum diff to get final array", S("_", fontName="Courier", fontSize=8, textColor=C_RED)),
     P("Multiple range-update operations", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Suffix Sum", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT2)),
     P("suffix[i] = suffix[i+1] + arr[i]", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT2)),
     P("suffix[L] - suffix[R+1]", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT2)),
     P("Compare left vs. right halves, pivot", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("XOR Prefix", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
     P("xp[i] = xp[i-1] ^ arr[i-1]", S("_", fontName="Courier", fontSize=8, textColor=C_GREEN)),
     P("xp[R+1] ^ xp[L]", S("_", fontName="Courier", fontSize=8, textColor=C_GREEN)),
     P("Range XOR, parity checks, bitmasks", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Product Prefix×Suffix", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("Two passes: left-product then right-product", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT)),
     P("output[i] = left_prod[i] * right_prod[i]", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT)),
     P("Product except self, no division", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
]
cheat_tbl = Table(cheat_data,
    colWidths=[90, 165, 165, 60],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
story.append(cheat_tbl)
story.append(Spacer(1, 14))

# Final motivational callout
story.append(Table([[
    Paragraph(
        "<b>You now have the complete mental model for Prefix Sum.</b><br/><br/>"
        "The technique is simple at its core: precompute running totals, "
        "then answer range questions in O(1) using subtraction. What makes it powerful "
        "is how it combines with HashMaps, extends to 2D grids, inverts into difference "
        "arrays, and generalizes to XOR and products.<br/><br/>"
        "Work the problem roadmap in order. After LC 303, 560, 304, and 238 — "
        "you will recognize this pattern instantly in any context.",
        S("_", fontName="Helvetica", fontSize=10, leading=16, textColor=C_BODY))
]], colWidths=[PAGE_W - 1.3*inch],
style=TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_CARD),
    ('BOX', (0,0), (-1,-1), 2, C_ACCENT),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
])))

# ── Page background via canvas callback ───────────────────────────────────────
def add_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Footer line
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.65*inch, 0.55*inch, PAGE_W - 0.65*inch, 0.55*inch)

    # Page number
    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, f"Prefix Sum — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")