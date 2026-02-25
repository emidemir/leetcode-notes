from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

# ── Color Palette (identical to Prefix Sum guide) ─────────────────────────────
C_BG        = colors.HexColor("#0F172A")
C_ACCENT    = colors.HexColor("#38BDF8")
C_ACCENT2   = colors.HexColor("#818CF8")
C_GREEN     = colors.HexColor("#34D399")
C_YELLOW    = colors.HexColor("#FBBF24")
C_RED       = colors.HexColor("#F87171")
C_PURPLE    = colors.HexColor("#C084FC")
C_CODE_BG   = colors.HexColor("#1E293B")
C_CODE_FG   = colors.HexColor("#E2E8F0")
C_HEADING   = colors.HexColor("#F1F5F9")
C_BODY      = colors.HexColor("#CBD5E1")
C_MUTED     = colors.HexColor("#64748B")
C_BORDER    = colors.HexColor("#334155")
C_CARD      = colors.HexColor("#1E293B")
C_HIGHLIGHT = colors.HexColor("#0EA5E9")
C_ORANGE    = colors.HexColor("#FB923C")

PAGE_W, PAGE_H = letter

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Two_Pointers_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)

# ── Styles ─────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle    = S("sTitle",    fontName="Helvetica-Bold", fontSize=32, leading=40, textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)
sSubtitle = S("sSubtitle", fontName="Helvetica",      fontSize=13, leading=18, textColor=C_ACCENT,  alignment=TA_CENTER, spaceAfter=4)
sAuthor   = S("sAuthor",   fontName="Helvetica-Oblique", fontSize=10, textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=20)
sH1       = S("sH1",       fontName="Helvetica-Bold", fontSize=20, leading=26, textColor=C_ACCENT,  spaceBefore=18, spaceAfter=8)
sH2       = S("sH2",       fontName="Helvetica-Bold", fontSize=14, leading=19, textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)
sH3       = S("sH3",       fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=C_GREEN,   spaceBefore=8,  spaceAfter=4)
sBody     = S("sBody",     fontName="Helvetica",      fontSize=10, leading=15, textColor=C_BODY,    spaceAfter=6, alignment=TA_JUSTIFY)
sBullet   = S("sBullet",   fontName="Helvetica",      fontSize=10, leading=14, textColor=C_BODY,    spaceAfter=3, leftIndent=16, bulletIndent=4)
sCode     = S("sCode",     fontName="Courier",        fontSize=8.5, leading=13, textColor=C_CODE_FG, spaceAfter=2, leftIndent=12, rightIndent=12, backColor=C_CODE_BG)
sCodeCmt  = S("sCodeCmt",  fontName="Courier-Oblique",fontSize=8.5, leading=13, textColor=C_MUTED,   spaceAfter=2, leftIndent=12, rightIndent=12, backColor=C_CODE_BG)
sFormula  = S("sFormula",  fontName="Courier-Bold",   fontSize=10, leading=14, textColor=C_GREEN,   alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
sCaption  = S("sCaption",  fontName="Helvetica-Oblique", fontSize=8.5, textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=6)
sTOC      = S("sTOC",      fontName="Helvetica",      fontSize=10, leading=16, textColor=C_BODY)
sTOCSub   = S("sTOCSub",   fontName="Helvetica",      fontSize=9,  leading=14, textColor=C_MUTED,   leftIndent=18)
sNote     = S("sNote",     fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor=C_YELLOW, spaceAfter=4)

P = Paragraph

# ── Helpers ────────────────────────────────────────────────────────────────────
def code_block(lines, lang="python"):
    header = Table([[P(f"<b>{lang}</b>", S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
        colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0D1929")),
            ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
        ]))
    rows = []
    for line in lines:
        st = sCodeCmt if line.startswith("##") else sCode
        rows.append([P(line if line else " ", st)])
    body_tbl = Table(rows, colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
            ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
    wrapper = Table([[header], [body_tbl]], colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('ROUNDEDCORNERS', [4]),
            ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
    return [wrapper, Spacer(1, 8)]

def callout(text, color=C_ACCENT, icon="💡"):
    tbl = Table([[P(f"{icon}  {text}", S("_", fontName="Helvetica", fontSize=9.5, leading=14, textColor=color))]],
        colWidths=[PAGE_W - 1.3*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0C1F35")),
            ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ('TOPPADDING', (0,0), (-1,-1), 9),   ('BOTTOMPADDING', (0,0), (-1,-1), 9),
            ('LINEBEFORE', (0,0), (0,-1), 3, color),
        ]))
    return [tbl, Spacer(1, 6)]

def section_divider(num, title):
    label = f"{num:02d}" if num > 0 else "  "
    return [
        Spacer(1, 10),
        Table([[
            P(f"<b>{label}</b>", S("_", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT)),
            P(f"<b>{title}</b>", S("_", fontName="Helvetica-Bold", fontSize=18, textColor=C_HEADING, leading=24)),
        ]], colWidths=[40, PAGE_W - 1.3*inch - 40],
        style=TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (0,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 2, C_ACCENT),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ])),
        Spacer(1, 8),
    ]

def pointer_vis(cells, left_idx=0, right_idx=None, labels=None, mid_idx=None, extra_idx=None):
    """Render a visual array showing pointer positions."""
    n = len(cells)
    if right_idx is None:
        right_idx = n - 1

    col_w = min(52, int((PAGE_W - 1.5*inch) / n))
    total_w = col_w * n

    # Value row
    val_row = []
    for i, v in enumerate(cells):
        if i == left_idx:
            bg = colors.HexColor("#0A2E3A")
            fg = C_ACCENT
        elif i == right_idx and right_idx != left_idx:
            bg = colors.HexColor("#1A1040")
            fg = C_ACCENT2
        elif mid_idx is not None and i == mid_idx:
            bg = colors.HexColor("#1A2E0A")
            fg = C_GREEN
        elif extra_idx is not None and i == extra_idx:
            bg = colors.HexColor("#2E1A0A")
            fg = C_ORANGE
        else:
            bg = C_CARD
            fg = C_BODY
        val_row.append(P(f"<b>{v}</b>", S("_", fontName="Courier-Bold", fontSize=11, textColor=fg, alignment=TA_CENTER)))

    # Index row
    idx_row = [P(str(i), S("_", fontName="Courier", fontSize=8, textColor=C_MUTED, alignment=TA_CENTER)) for i in range(n)]

    # Pointer label row
    ptr_row = []
    for i in range(n):
        pts = []
        if i == left_idx:
            pts.append(labels[0] if labels else "L")
        if i == right_idx and right_idx != left_idx:
            pts.append(labels[1] if labels and len(labels) > 1 else "R")
        if mid_idx is not None and i == mid_idx:
            pts.append(labels[2] if labels and len(labels) > 2 else "M")
        if extra_idx is not None and i == extra_idx:
            pts.append(labels[3] if labels and len(labels) > 3 else "E")
        label_txt = "/".join(pts) if pts else ""
        clr = C_ACCENT if (i == left_idx) else (C_ACCENT2 if i == right_idx else (C_GREEN if i == mid_idx else C_ORANGE))
        ptr_row.append(P(f"<b>{label_txt}</b>", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=clr, alignment=TA_CENTER)))

    tbl = Table([ptr_row, val_row, idx_row],
        colWidths=[col_w]*n,
        style=TableStyle([
            ('BACKGROUND', (0,1), (-1,1), C_CARD),
            ('BOX', (0,1), (-1,1), 1, C_BORDER),
            ('INNERGRID', (0,1), (-1,1), 0.5, C_BORDER),
            ('BACKGROUND', (left_idx,1), (left_idx,1), colors.HexColor("#0A2E3A")),
            ('BACKGROUND', (right_idx,1), (right_idx,1), colors.HexColor("#1A1040")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,1), (-1,1), 8), ('BOTTOMPADDING', (0,1), (-1,1), 8),
            ('TOPPADDING', (0,0), (-1,0), 2), ('BOTTOMPADDING', (0,0), (-1,0), 2),
            ('TOPPADDING', (0,2), (-1,2), 2), ('BOTTOMPADDING', (0,2), (-1,2), 2),
        ]))
    return [tbl, Spacer(1, 6)]

# ── Story ──────────────────────────────────────────────────────────────────────
story = []

# ════════════════════════════════════════════════════════
# COVER
# ════════════════════════════════════════════════════════
story.append(Spacer(1, 0.5*inch))
story.append(Table([[""]], colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([('BACKGROUND', (0,0), (-1,-1), C_ACCENT), ('ROWHEIGHT', (0,0), (-1,-1), 6)])))
story.append(Spacer(1, 0.3*inch))

story.append(P("TWO POINTERS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Intuition · Pointer Movement · Complexity · Patterns", sAuthor))
story.append(Spacer(1, 0.2*inch))

cover_data = [
    [P("<b>What You Will Master</b>", S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· The core philosophy: Search Space Reduction\n"
       "· Pattern 1 — Opposite Ends (Converging Pointers)\n"
       "· Pattern 2 — Slow &amp; Fast (Tortoise and Hare)\n"
       "· Pattern 3 — Two Arrays / Two Sequences\n"
       "· Dutch National Flag (3-pointer single-pass partition)\n"
       "· Two Pointers vs. Sliding Window decision framework\n"
       "· 20+ categorized LeetCode problems with key insights\n"
       "· Off-by-one errors, overflow, and loop condition pitfalls",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))],
]
story.append(Table(cover_data, colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD), ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
    ])))
story.append(Spacer(1, 0.3*inch))

cx_data = [
    [P("<b>Brute Force</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Two Pointers</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Space</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("O(n<super>2</super>) nested loops", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_RED, alignment=TA_CENTER)),
     P("O(n) single pass", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_GREEN, alignment=TA_CENTER)),
     P("O(1) extra", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_YELLOW, alignment=TA_CENTER))],
]
story.append(Table(cx_data, colWidths=[(PAGE_W - 1.3*inch)/3]*3,
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0A1628")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ])))
story.append(Spacer(1, 0.4*inch))
story.append(Table([[""]], colWidths=[PAGE_W - 1.3*inch],
    style=TableStyle([('BACKGROUND', (0,0), (-1,-1), C_ACCENT2), ('ROWHEIGHT', (0,0), (-1,-1), 4)])))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════════════════════
story += section_divider(0, "Table of Contents")

toc_items = [
    ("01", "The Core Philosophy", ["Search Space Reduction", "Why O(n) Instead of O(n²)", "The Prerequisite of Order"]),
    ("02", "Pattern 1: Opposite Ends (Converging)", ["Two Sum on Sorted Array", "Palindrome Check", "Container With Most Water"]),
    ("03", "Pattern 2: Slow & Fast (Tortoise & Hare)", ["Cycle Detection in Linked List", "Middle of Linked List", "Find Duplicate Number"]),
    ("04", "Pattern 3: Two Arrays / Two Sequences", ["Merge Sorted Arrays", "Intersection of Arrays", "Compare Version Numbers"]),
    ("05", "Mathematical Prerequisites", ["Why Sorting Enables Two Pointers", "Monotonicity Requirement", "When Two Pointers Fails"]),
    ("06", "Comparison & Decision Making", ["Two Pointers vs. Sliding Window", "Decision Flowchart", "Hybrid Techniques"]),
    ("07", "Advanced: Dutch National Flag (3-Pointer)", ["Problem Statement & Intuition", "The Partition Invariant", "Backend Engineering Applications"]),
    ("08", "Problem Roadmap", ["Easy Problems", "Medium Problems", "Hard Problems"]),
    ("09", "Common Pitfalls & Edge Cases", ["Off-By-One in Loop Conditions", "Integer Overflow", "Empty & Single-Element Inputs"]),
]
for num, title, subs in toc_items:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1, 3))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 1: CORE PHILOSOPHY
# ════════════════════════════════════════════════════════
story += section_divider(1, "The Core Philosophy")

story.append(P("<b>The Fundamental Problem: O(n²) Nested Loops</b>", sH2))
story.append(P(
    "Many array/string problems ask you to find a <b>pair</b> or <b>combination</b> "
    "of elements satisfying some condition. The naive instinct is to check every "
    "possible pair with a double loop — O(n²) time. For n=10,000 that is 100 million "
    "operations. Two Pointers is the systematic technique for collapsing this to O(n).",
    sBody))

story += code_block([
    "## ─── Brute Force: O(n²) — check every pair ────────────────────",
    "def brute_force_pair(arr, target):",
    "    for i in range(len(arr)):",
    "        for j in range(i + 1, len(arr)):   ## inner loop = O(n) per outer step",
    "            if arr[i] + arr[j] == target:",
    "                return (i, j)",
    "    return None                             ## Total: O(n²)",
    "",
    "## ─── Two Pointers: O(n) — intelligent pointer movement ─────────",
    "def two_pointer_pair(arr, target):          ## arr must be sorted!",
    "    left, right = 0, len(arr) - 1",
    "    while left < right:",
    "        current_sum = arr[left] + arr[right]",
    "        if current_sum == target:   return (left, right)",
    "        elif current_sum < target:  left  += 1   ## need bigger sum",
    "        else:                       right -= 1   ## need smaller sum",
    "    return None                             ## Total: O(n)",
])

story.append(P("<b>Search Space Reduction: The Core Insight</b>", sH2))
story.append(P(
    "With two pointers, every single step <b>eliminates an entire column or row</b> "
    "of the implicit n×n search matrix. This is the essence of the technique: "
    "we use the <i>structure of the data</i> (usually sortedness) to make a "
    "guaranteed-correct decision about which pointer to move. No guessing — "
    "each movement is logically justified.",
    sBody))

# Search space diagram
story.append(P("<b>Visual: Eliminating the Search Space</b>", sH3))
story.append(P(
    "Imagine a sorted array [1, 3, 5, 8, 11]. For target=9, the pairs matrix below "
    "shows all possible sums. Two pointers traverses only the anti-diagonal, "
    "eliminating entire rows/columns at each step:",
    sBody))

arr_ex = [1, 3, 5, 8, 11]
matrix_rows = []
header = [P("<b>+</b>", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_MUTED, alignment=TA_CENTER))]
for v in arr_ex:
    header.append(P(str(v), S("_", fontName="Courier-Bold", fontSize=9, textColor=C_ACCENT, alignment=TA_CENTER)))
matrix_rows.append(header)
for i, vi in enumerate(arr_ex):
    row = [P(str(vi), S("_", fontName="Courier-Bold", fontSize=9, textColor=C_ACCENT2, alignment=TA_CENTER))]
    for j, vj in enumerate(arr_ex):
        s = vi + vj
        if s == 9:
            clr = C_GREEN; bg_str = "hit"
        elif i == j:
            clr = C_MUTED; bg_str = "diag"
        elif s < 9:
            clr = colors.HexColor("#374151"); bg_str = "low"
        else:
            clr = colors.HexColor("#374151"); bg_str = "high"
        row.append(P(str(s), S("_", fontName="Courier", fontSize=9, textColor=clr, alignment=TA_CENTER)))
    matrix_rows.append(row)

matrix_tbl = Table(matrix_rows, colWidths=[36]*6,
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('BACKGROUND', (0,0), (0,-1), C_BG),
        ('BACKGROUND', (1,1), (-1,-1), C_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (5,1), (5,1), colors.HexColor("#0A2E1A")),  # 1+8=9
        ('BACKGROUND', (4,2), (4,2), colors.HexColor("#0A2E1A")),  # 3+... no
        ('BACKGROUND', (3,3), (3,3), colors.HexColor("#0A2E1A")),  # 5+... no wait
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
story.append(matrix_tbl)
story.append(P("Green cells = sum equals target (9). Two pointers finds these by moving along the anti-diagonal, never revisiting eliminated cells.", sCaption))

story += callout(
    "Key Insight: With a sorted array, if arr[L] + arr[R] is too small, "
    "every pair involving arr[L] paired with any element ≤ arr[R] is also too small. "
    "We eliminate the entire LEFT column in one step by moving L rightward.",
    C_ACCENT, icon="💡")

story.append(P("<b>The Three Prerequisites for Two Pointers</b>", sH2))
prereq_data = [
    [P("<b>Prerequisite</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Why It Matters</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Patterns That Need It</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Order / Sortedness", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("Enables predictable search space reduction — knowing which direction changes the result.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends, Two-Sum variants", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("Monotonicity", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT2)),
     P("Moving a pointer in one direction must always change result in a predictable way (e.g., sum always increases if left moves right).", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("All converging patterns", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("Index Validity", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
     P("Both pointers must stay in bounds. Loop condition (< vs <=) controls whether they can meet or cross.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("All patterns", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
]
story.append(Table(prereq_data, colWidths=[110, 270, 100],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2: PATTERN 1 — OPPOSITE ENDS
# ════════════════════════════════════════════════════════
story += section_divider(2, "Pattern 1: Opposite Ends (Converging)")

story.append(P("<b>Intuition</b>", sH2))
story.append(P(
    "Place one pointer at the leftmost position and one at the rightmost. "
    "Move them <b>toward each other</b> based on a comparison condition. "
    "This works because the sorted structure guarantees that moving left right "
    "increases the sum, and moving right left decreases it. "
    "The two pointers act as a \"closing jaw\" on the answer.",
    sBody))

story.append(P("<b>Template: Converging Two Pointers</b>", sH2))
story += code_block([
    "## ─── Opposite Ends Template ────────────────────────────────────",
    "def opposite_ends_template(arr):            ## arr is SORTED",
    "    left  = 0",
    "    right = len(arr) - 1",
    "",
    "    while left < right:                     ## '<' not '<=' — stop before crossing",
    "        result = some_function(arr[left], arr[right])",
    "",
    "        if result == TARGET:",
    "            ## Found the answer",
    "            return (left, right)",
    "",
    "        elif result < TARGET:",
    "            left  += 1   ## current value too small → move left pointer right",
    "                         ## (all pairs with arr[right] and any arr[i] <= arr[left]",
    "                         ##  are also too small → safely skip entire column)",
    "",
    "        else:            ## result > TARGET",
    "            right -= 1   ## current value too large → move right pointer left",
    "                         ## (all pairs with arr[left] and any arr[j] >= arr[right]",
    "                         ##  are also too large → safely skip entire row)",
    "",
    "    return None          ## no valid pair found",
])

# Visual walkthrough
story.append(P("<b>Visual Walkthrough: Two Sum on Sorted Array</b>", sH2))
story.append(P("Target = 9, arr = [1, 3, 5, 8, 11]. Watch the pointers converge:", sBody))

steps = [
    ([1,3,5,8,11], 0, 4, "Step 1: 1+11=12 > 9 → move right left"),
    ([1,3,5,8,11], 0, 3, "Step 2: 1+8=9 == 9 → FOUND! Return (0,3)"),
]
for arr_s, l, r, desc in steps:
    story += pointer_vis(arr_s, l, r, labels=["left", "right"])
    story.append(P(f"<b>{desc}</b>", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW, spaceAfter=8)))

story.append(P("<b>Problem: Palindrome Check</b>", sH3))
story.append(P(
    "Check if a string is a palindrome by comparing characters from both ends, "
    "moving inward. Terminates in O(n/2) = O(n) time.",
    sBody))
story += code_block([
    "## ─── Palindrome Check ──────────────────────────────────────────",
    "def is_palindrome(s):",
    "    left, right = 0, len(s) - 1",
    "    while left < right:",
    "        if s[left] != s[right]:",
    "            return False       ## mismatch found — not a palindrome",
    "        left  += 1",
    "        right -= 1",
    "    return True                ## all pairs matched",
    "",
    "## Variant: skip non-alphanumeric (LC 125 Valid Palindrome)",
    "def is_palindrome_ii(s):",
    "    left, right = 0, len(s) - 1",
    "    while left < right:",
    "        while left < right and not s[left].isalnum():  left  += 1",
    "        while left < right and not s[right].isalnum(): right -= 1",
    "        if s[left].lower() != s[right].lower(): return False",
    "        left += 1; right -= 1",
    "    return True",
])

story.append(P("<b>Problem: Container With Most Water (Max Area)</b>", sH3))
story.append(P(
    "Given an array of heights, find two lines that together with the x-axis "
    "form a container holding the most water. The area = min(height[L], height[R]) × (R - L). "
    "We always move the pointer at the <b>shorter</b> height, because keeping it "
    "cannot possibly increase the minimum, while moving it might find a taller wall.",
    sBody))
story += code_block([
    "## ─── Container With Most Water ─────────────────────────────────",
    "def max_area(heights):",
    "    left, right = 0, len(heights) - 1",
    "    max_water   = 0",
    "",
    "    while left < right:",
    "        h     = min(heights[left], heights[right])",
    "        width = right - left",
    "        max_water = max(max_water, h * width)",
    "",
    "        ## Greedy: always move the shorter wall",
    "        ## Moving the taller wall can only shrink width without gaining height",
    "        if heights[left] < heights[right]:",
    "            left  += 1",
    "        else:",
    "            right -= 1",
    "",
    "    return max_water",
])

story += callout(
    "Pattern Recognition: When you see 'sorted array + find pair/triplet with condition', "
    "default to Opposite Ends. The key question is: does the monotonicity hold? "
    "Can you always justify pointer movement with a logical argument?",
    C_ACCENT2, icon="🎯")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3: PATTERN 2 — SLOW & FAST
# ════════════════════════════════════════════════════════
story += section_divider(3, "Pattern 2: Slow & Fast (Tortoise & Hare)")

story.append(P("<b>Intuition: The Race on a Track</b>", sH2))
story.append(P(
    "Instead of starting at opposite ends, both pointers begin at the same position "
    "and move in the <b>same direction</b> — but at different speeds. "
    "The slow pointer moves one step at a time; the fast pointer moves two. "
    "This speed differential creates powerful invariants for cycle detection, "
    "finding midpoints, and locating duplicates.",
    sBody))

story += callout(
    "Analogy: Two runners on a circular track. The faster runner will always "
    "lap the slower one if there is a cycle. If the track has no cycle (it ends), "
    "the fast runner simply reaches the end first.",
    C_ACCENT, icon="🏃")

story.append(P("<b>Core Invariants of Slow & Fast</b>", sH2))
inv_data = [
    [P("<b>Property</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Guaranteed Behaviour</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Fast moves 2× speed", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("When slow reaches midpoint, fast has reached the end (linear list). Use this to find the middle node.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Cycle present", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT2)),
     P("Fast will eventually catch slow from behind — they WILL meet inside the cycle. Meeting point ≠ cycle start.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("No cycle present", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
     P("Fast reaches null/end before catching slow. The pointers never meet.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Gap narrows by 1/step", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Each iteration: slow advances 1, fast advances 2. Their distance closes by 1 per step inside a cycle.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
]
story.append(Table(inv_data, colWidths=[150, 330],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(Spacer(1, 8))

story.append(P("<b>Template: Slow & Fast Pointer</b>", sH2))
story += code_block([
    "## ─── Slow & Fast Template (Linked List) ────────────────────────",
    "def slow_fast_template(head):",
    "    slow = head",
    "    fast = head",
    "",
    "    while fast is not None and fast.next is not None:",
    "        slow = slow.next           ## advances 1 step",
    "        fast = fast.next.next      ## advances 2 steps",
    "",
    "        if slow is fast:           ## cycle detected",
    "            return True",
    "",
    "    return False                   ## fast reached end → no cycle",
    "",
    "## ─── Find Middle of Linked List ─────────────────────────────────",
    "def find_middle(head):",
    "    slow = fast = head",
    "    while fast and fast.next:      ## when fast hits end, slow is at middle",
    "        slow = slow.next",
    "        fast = fast.next.next",
    "    return slow                    ## slow is the middle node",
])

story.append(P("<b>Why Floyd's Algorithm Works (Cycle Entry Point)</b>", sH3))
story.append(P(
    "After slow and fast meet inside the cycle, reset one pointer to the head. "
    "Now advance both pointers <b>one step at a time</b>. They will meet exactly "
    "at the <b>cycle entry node</b>. This works because of the mathematical "
    "relationship between the distances: dist(head→entry) = dist(meeting→entry) "
    "when traversing the cycle.",
    sBody))
story += code_block([
    "## ─── Floyd's Cycle Detection + Entry Point ──────────────────────",
    "def detect_cycle_entry(head):",
    "    slow = fast = head",
    "",
    "    ## Phase 1: detect if cycle exists",
    "    while fast and fast.next:",
    "        slow = slow.next",
    "        fast = fast.next.next",
    "        if slow is fast:",
    "            break",
    "    else:",
    "        return None               ## no cycle",
    "",
    "    ## Phase 2: find entry point",
    "    slow = head                   ## reset one pointer to head",
    "    while slow is not fast:",
    "        slow = slow.next          ## both move 1 step",
    "        fast = fast.next",
    "",
    "    return slow                   ## cycle entry node",
])

story.append(P("<b>Slow & Fast on Arrays: Find the Duplicate</b>", sH3))
story.append(P(
    "LC 287 — Given an array of n+1 integers where each value is in [1..n], "
    "find the duplicate without extra space. Treat array values as pointer "
    "indices (like a linked list with implicit next pointers), then apply Floyd's:",
    sBody))
story += code_block([
    "## ─── Find Duplicate (LC 287) ───────────────────────────────────",
    "def find_duplicate(nums):",
    "    ## Treat arr[i] as a pointer to index arr[i]",
    "    ## Duplicate value = cycle entry point",
    "    slow = fast = nums[0]",
    "",
    "    ## Phase 1: find intersection",
    "    while True:",
    "        slow = nums[slow]",
    "        fast = nums[nums[fast]]",
    "        if slow == fast: break",
    "",
    "    ## Phase 2: find entry (= duplicate)",
    "    slow = nums[0]",
    "    while slow != fast:",
    "        slow = nums[slow]",
    "        fast = nums[fast]",
    "    return slow",
])

story += callout(
    "The Slow & Fast pattern is primarily for LINKED LISTS. "
    "On arrays, it only applies when you can model the array as an implicit linked list "
    "(i.e., each value is an index into the next position). LC 287 is the canonical example.",
    C_YELLOW, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4: PATTERN 3 — TWO ARRAYS
# ════════════════════════════════════════════════════════
story += section_divider(4, "Pattern 3: Two Arrays / Two Sequences")

story.append(P("<b>Intuition</b>", sH2))
story.append(P(
    "When you have <b>two separate sorted arrays/lists</b>, one pointer per array "
    "allows you to traverse both simultaneously in O(m + n) time instead of O(m × n). "
    "At each step, you compare the elements at both pointers and advance the pointer "
    "pointing to the smaller (or matching) element.",
    sBody))

story += code_block([
    "## ─── Two-Array Template ────────────────────────────────────────",
    "def two_array_template(arr1, arr2):",
    "    i, j   = 0, 0",
    "    result = []",
    "",
    "    while i < len(arr1) and j < len(arr2):",
    "        if arr1[i] == arr2[j]:",
    "            result.append(arr1[i])   ## match found",
    "            i += 1; j += 1",
    "        elif arr1[i] < arr2[j]:",
    "            i += 1                   ## arr1 is behind, advance it",
    "        else:",
    "            j += 1                   ## arr2 is behind, advance it",
    "",
    "    ## Optionally process remaining elements",
    "    ## while i < len(arr1): ...",
    "    ## while j < len(arr2): ...",
    "    return result",
])

story.append(P("<b>Merge Two Sorted Arrays</b>", sH3))
story.append(P(
    "The classic merge step from Merge Sort. Compare front elements of both "
    "arrays and always take the smaller one, advancing that pointer.",
    sBody))
story += code_block([
    "## ─── Merge Two Sorted Lists ────────────────────────────────────",
    "def merge_sorted(arr1, arr2):",
    "    merged = []",
    "    i, j   = 0, 0",
    "",
    "    while i < len(arr1) and j < len(arr2):",
    "        if arr1[i] <= arr2[j]:      ## take from arr1",
    "            merged.append(arr1[i])",
    "            i += 1",
    "        else:                       ## take from arr2",
    "            merged.append(arr2[j])",
    "            j += 1",
    "",
    "    ## Append remaining elements (at most one while loop executes)",
    "    merged.extend(arr1[i:])",
    "    merged.extend(arr2[j:])",
    "    return merged",
])

story.append(P("<b>Visual: Two-Array Pointer Movement</b>", sH3))
story.append(P("Merging [1, 4, 7] and [2, 5, 6]. Watch pointers advance:", sBody))

merge_steps = [
    ("arr1=[1,4,7]  arr2=[2,5,6]", "1<2 → take 1 from arr1, i++"),
    ("arr1=[1,4,7]  arr2=[2,5,6]", "2<4 → take 2 from arr2, j++"),
    ("arr1=[1,4,7]  arr2=[2,5,6]", "4<5 → take 4 from arr1, i++"),
]
for state, action in merge_steps:
    row = Table([[
        P(state,  S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
        P(action, S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
    ]], colWidths=[280, 200],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, C_BORDER),
    ]))
    story.append(row)

story.append(P("Result builds up: [1, 2, 4, 5, 6, 7]", sCaption))
story.append(Spacer(1, 8))

story.append(P("<b>Comparing Strings / Version Numbers</b>", sH3))
story.append(P(
    "Compare two version strings like '1.10.3' vs '1.9.5'. Split by '.', "
    "then use two pointers (one per version) to compare each numeric segment. "
    "Treat missing segments as 0.",
    sBody))
story += code_block([
    "## ─── Compare Version Numbers ───────────────────────────────────",
    "def compare_versions(v1, v2):",
    "    parts1 = [int(x) for x in v1.split('.')]",
    "    parts2 = [int(x) for x in v2.split('.')]",
    "    i, j   = 0, 0",
    "",
    "    while i < len(parts1) or j < len(parts2):",
    "        seg1 = parts1[i] if i < len(parts1) else 0   ## missing = 0",
    "        seg2 = parts2[j] if j < len(parts2) else 0",
    "",
    "        if   seg1 < seg2: return -1",
    "        elif seg1 > seg2: return  1",
    "",
    "        i += 1; j += 1",
    "",
    "    return 0   ## versions are equal",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5: MATHEMATICAL PREREQUISITES
# ════════════════════════════════════════════════════════
story += section_divider(5, "Mathematical Prerequisites")

story.append(P("<b>Why Sorting is the Gateway</b>", sH2))
story.append(P(
    "The Opposite Ends pattern requires a <b>monotone relationship</b>: moving a "
    "pointer in one direction must <i>always</i> change the result in a predictable "
    "way. Sorting provides exactly this guarantee.",
    sBody))

mono_data = [
    [P("<b>Action</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Effect on Sum</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Why Guaranteed?</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Move left → right (left++)", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
     P("Sum INCREASES or stays same", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("arr[left+1] >= arr[left] because array is sorted ascending", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Move right → left (right--)", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT2)),
     P("Sum DECREASES or stays same", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("arr[right-1] <= arr[right] because array is sorted ascending", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
]
story.append(Table(mono_data, colWidths=[165, 165, 150],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(Spacer(1, 8))

story.append(P("<b>The Monotonicity Requirement</b>", sH2))
story.append(P(
    "Monotonicity means the evaluation function changes in only <b>one direction</b> "
    "as a pointer moves. If this breaks — for example if the array has arbitrary "
    "order — you cannot guarantee that skipping elements is safe.",
    sBody))
story += code_block([
    "## Monotonicity HOLDS (sorted array, sum function):",
    "## f(left, right) = arr[left] + arr[right]",
    "## Moving left right  →  f strictly increases (or stays same)",
    "## Moving right left →  f strictly decreases (or stays same)",
    "## ✅ Safe to use two pointers",
    "",
    "## Monotonicity BREAKS (unsorted array):",
    "## arr = [5, 1, 8, 2, 7]",
    "## arr[0]+arr[4] = 12; arr[1]+arr[4] = 8  (decreased, but we moved left right!)",
    "## Moving left right could DECREASE the sum → can't make safe pointer decisions",
    "## ❌ Two pointer logic invalid on unsorted input",
])

story.append(P("<b>When Two Pointers Cannot Be Applied</b>", sH3))
fail_data = [
    [P("<b>Scenario</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Why It Fails</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Alternative</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Unsorted array, exact sum query", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("No monotonicity — pointer movements unpredictable", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("Sort first (O(n log n) + O(n)) or HashMap O(n)", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("Non-contiguous subarrays", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Two pointers work on contiguous ranges only", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("DP, bitmask, or recursive search", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("Multi-dimensional search", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Two pointers cover one dimension at a time", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("Prefix sum + HashMap or 2D DP", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("Non-linear evaluation function", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("f(L, R) may oscillate — no monotone direction", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED)),
     P("Binary search or brute force", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
]
story.append(Table(fail_data, colWidths=[160, 190, 130],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6: TWO POINTERS vs SLIDING WINDOW
# ════════════════════════════════════════════════════════
story += section_divider(6, "Comparison & Decision Making")

story.append(P("<b>Two Pointers vs. Sliding Window</b>", sH2))
story.append(P(
    "Sliding Window is technically a two-pointer technique — it uses a left and right "
    "pointer. However, the <b>mental model and application differ significantly</b>. "
    "The distinction is about what you care about: the <i>endpoints</i> themselves, "
    "or the <i>content of the window between them</i>.",
    sBody))

sw_data = [
    [P("<b>Dimension</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>General Two Pointers</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("<b>Sliding Window</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_PURPLE))],
    [P("Focus", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("The specific ELEMENTS at left and right positions", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("The RANGE/WINDOW between left and right (its sum, count, frequency map)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Pointer direction", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("Can converge (opposite ends) or same direction (fast/slow)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Always same direction — left never passes right", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Negative numbers", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("✅ Sorted array handles it; or use HashMap", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN)),
     P("❌ Fixed-size OK; variable-size breaks monotonicity", S("_", fontName="Helvetica", fontSize=9, textColor=C_RED))],
    [P("Sorting required?", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("Usually YES for converging pattern", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW)),
     P("Usually NO — works on original order", S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))],
    [P("State tracked", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("Comparison result of arr[L] and arr[R]", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Aggregate of window: sum, count, hashmap of frequencies", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Typical goal", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("Find pair/triplet, palindrome check, cycle detection", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Longest/shortest subarray with property, max sum window", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("Key question", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("'Do these two elements satisfy a condition?'", S("_", fontName="Helvetica-Oblique", fontSize=9, textColor=C_ACCENT)),
     P("'Does this range/window satisfy a condition?'", S("_", fontName="Helvetica-Oblique", fontSize=9, textColor=C_PURPLE))],
    [P("Classic problems", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_BODY)),
     P("Two Sum (sorted), 3Sum, Trapping Rain Water, Cycle Detection", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED)),
     P("Max Sum Subarray of K, Longest Substring Without Repeating, Min Window Substring", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
]
story.append(Table(sw_data, colWidths=[120, 210, 150],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(Spacer(1, 8))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow_steps = [
    ("Q1", "Is the array/string SORTED (or can you sort it)?", C_ACCENT),
    ("  → YES", "Consider Opposite Ends Two Pointers for pair/triplet problems", C_GREEN),
    ("  → NO", "Consider Sliding Window (if window/range) or HashMap (if pair finding)", C_YELLOW),
    ("Q2", "Do you care about two SPECIFIC ELEMENTS or a RANGE between them?", C_ACCENT),
    ("  → Elements", "Use Two Pointers (converging or fast/slow)", C_GREEN),
    ("  → Range/Window", "Use Sliding Window with window-state tracking", C_PURPLE),
    ("Q3", "Does the array contain NEGATIVE numbers?", C_ACCENT),
    ("  → YES", "Sliding Window (variable size) likely fails; use Prefix+HashMap instead", C_RED),
    ("  → NO", "Both Sliding Window and Two Pointers are viable — compare requirements", C_GREEN),
]
for label, text, clr in flow_steps:
    tbl = Table([[
        P(f"<b>{label}</b>", S("_", fontName="Courier-Bold", fontSize=9, textColor=clr, alignment=TA_LEFT)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[70, 410],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CARD if "→" not in label else colors.HexColor("#141E2E")),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('LINEBELOW', (0,0), (-1,-1), 0.5, C_BORDER),
    ]))
    story.append(tbl)

story.append(Spacer(1, 8))
story += callout(
    "Heuristic: If you find yourself maintaining a hashmap or counter INSIDE your "
    "two-pointer loop, you are likely doing Sliding Window. Pure Two Pointers only "
    "compares the two pointed elements and makes a binary move decision.",
    C_ACCENT2, icon="🔑")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7: DUTCH NATIONAL FLAG
# ════════════════════════════════════════════════════════
story += section_divider(7, "Advanced: Dutch National Flag (3-Pointer)")

story.append(P("<b>The Problem: Three-Way Partition in a Single Pass</b>", sH2))
story.append(P(
    "Given an array containing only three distinct values (e.g., 0, 1, 2 representing "
    "red, white, blue — or 'low', 'medium', 'high' priority), sort it <b>in-place "
    "in a single O(n) pass using O(1) extra space</b>. No comparison sort needed.",
    sBody))

story += callout(
    "Backend Engineering Application: This algorithm directly models real-world "
    "three-tier data partitioning — priority queues with low/medium/high buckets, "
    "HTTP request classification, or database record tagging. A single O(n) scan "
    "beats a full sort (O(n log n)) when data already has a three-value structure.",
    C_PURPLE, icon="🏗️")

story.append(P("<b>The Three-Pointer Invariant</b>", sH2))
story.append(P(
    "Use three pointers to maintain a partition invariant at every step of the algorithm:",
    sBody))

inv3_data = [
    [P("<b>Pointer</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Name</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Invariant</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Everything to its LEFT is...</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("low", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_ACCENT)),
     P("Left boundary", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("arr[0..low-1] = 0", S("_", fontName="Courier", fontSize=9, textColor=C_ACCENT)),
     P("All zeros — fully processed and placed", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("mid", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_GREEN)),
     P("Current scanner", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("arr[low..mid-1] = 1", S("_", fontName="Courier", fontSize=9, textColor=C_GREEN)),
     P("All ones — known and correctly placed", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("high", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_RED)),
     P("Right boundary", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("arr[high+1..n-1] = 2", S("_", fontName="Courier", fontSize=9, textColor=C_RED)),
     P("All twos — fully processed and placed", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
    [P("mid..high", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_YELLOW)),
     P("Unknown zone", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Unclassified", S("_", fontName="Courier", fontSize=9, textColor=C_YELLOW)),
     P("Region yet to be processed by mid pointer", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY))],
]
story.append(Table(inv3_data, colWidths=[65, 90, 130, 195],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(Spacer(1, 8))

story.append(P("<b>The Algorithm: Three Decision Branches</b>", sH2))
story += code_block([
    "## ─── Dutch National Flag (Sort Colors) ─────────────────────────",
    "def sort_colors(nums):",
    '    """',
    "    Partition arr into [0...0, 1...1, 2...2] in a single pass.",
    "    Three pointers: low, mid, high.",
    "    Loop continues while mid <= high (unknown zone is non-empty).",
    '    """',
    "    low  = 0",
    "    mid  = 0",
    "    high = len(nums) - 1",
    "",
    "    while mid <= high:          ## process unknown zone: arr[mid..high]",
    "",
    "        if nums[mid] == 0:",
    "            ## 0 belongs at the left — swap with low boundary",
    "            nums[low], nums[mid] = nums[mid], nums[low]",
    "            low += 1            ## expand left (zero) region",
    "            mid += 1            ## element at mid is now 1 (safe to advance)",
    "",
    "        elif nums[mid] == 1:",
    "            ## 1 is already in the right place (low..mid-1)",
    "            mid += 1            ## just advance scanner",
    "",
    "        else:  ## nums[mid] == 2",
    "            ## 2 belongs at the right — swap with high boundary",
    "            nums[mid], nums[high] = nums[high], nums[mid]",
    "            high -= 1           ## expand right (two) region",
    "            ## DO NOT increment mid — swapped element is unknown!",
    "",
    "    ## Done: arr = [0..0, 1..1, 2..2]  in O(n) time, O(1) space",
])

story.append(P("<b>Step-by-Step Visual Trace</b>", sH2))
story.append(P("Input: [2, 0, 2, 1, 1, 0]. Watch all three pointers:", sBody))

dnf_steps = [
    ([2,0,2,1,1,0], 0, 5, 0, "Initial: low=0, mid=0, high=5. nums[mid]=2 → swap(mid,high), high--"),
    ([0,0,2,1,1,2], 0, 4, 0, "nums[mid]=0 → swap(low,mid), low++, mid++"),
    ([0,0,2,1,1,2], 1, 4, 1, "nums[mid]=0 → swap(low,mid), low++, mid++"),
    ([0,0,2,1,1,2], 2, 4, 2, "nums[mid]=2 → swap(mid,high), high--"),
    ([0,0,1,1,2,2], 2, 3, 2, "nums[mid]=1 → mid++"),
    ([0,0,1,1,2,2], 2, 3, 3, "nums[mid]=1 → mid++. mid>high: DONE!"),
]
for arr_s, low, high, mid_p, desc in dnf_steps:
    # render pointer row manually
    col_w = 52
    n = len(arr_s)
    ptr_row = []
    val_row = []
    for i, v in enumerate(arr_s):
        pts = []
        if i == low:   pts.append("low")
        if i == mid_p: pts.append("mid")
        if i == high:  pts.append("high")
        label = "/".join(pts)
        lclr = C_ACCENT if "low" in label else (C_GREEN if "mid" in label else (C_RED if "high" in label else C_MUTED))
        ptr_row.append(P(f"<b>{label}</b>", S("_", fontName="Helvetica-Bold", fontSize=7, textColor=lclr, alignment=TA_CENTER)))
        bg = colors.HexColor("#0A2E3A") if i < low else (colors.HexColor("#0A2E1A") if low <= i < mid_p else (colors.HexColor("#2E0A0A") if i > high else C_CARD))
        fclr = C_ACCENT if v == 0 else (C_GREEN if v == 1 else C_RED)
        val_row.append(P(f"<b>{v}</b>", S("_", fontName="Courier-Bold", fontSize=11, textColor=fclr, alignment=TA_CENTER)))

    vis = Table([ptr_row, val_row], colWidths=[col_w]*n,
        style=TableStyle([
            ('BOX', (0,1), (-1,1), 1, C_BORDER), ('INNERGRID', (0,1), (-1,1), 0.5, C_BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,1), (-1,1), 7), ('BOTTOMPADDING', (0,1), (-1,1), 7),
            ('TOPPADDING', (0,0), (-1,0), 2), ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ]))
    story.append(vis)
    story.append(P(desc, S("_", fontName="Helvetica", fontSize=8.5, textColor=C_YELLOW, spaceAfter=6)))

story += callout(
    "CRITICAL: When swapping nums[mid] with nums[high] (the 2-case), do NOT increment mid. "
    "The swapped element came from the unknown zone and must be re-examined. "
    "This is the most common bug in DNF implementations.",
    C_RED, icon="⚠️")

story.append(P("<b>The Generalized K-Way Partition</b>", sH3))
story.append(P(
    "The DNF principle generalizes to any fixed number of categories k. "
    "For k=2 it's the classic partition step of QuickSort. "
    "For k=3 it's DNF. For k>3, it requires k-1 pointers and becomes more complex "
    "(typically use counting sort instead). In practice, k=3 covers most interview problems.",
    sBody))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8: PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(8, "LeetCode Problem Roadmap")

story.append(P(
    "Problems organized by difficulty and sub-pattern. Solve them in order — "
    "each one reinforces and extends the previous concept.",
    sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("125", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Valid Palindrome", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Skip non-alnum; compare s[L] and s[R] from both ends.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("167", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Two Sum II (Input Sorted)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("The canonical converging pointer problem. Sort then squeeze.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("344", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Reverse String", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Swap s[L] and s[R], converge. Terminates in n/2 swaps.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("876", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Middle of Linked List", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("When fast hits end, slow is at middle. Odd/even length handled naturally.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("141", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Linked List Cycle", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Floyd's algorithm. If they meet, cycle exists.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("977", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Squares of Sorted Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Largest squares at either end. Fill result from right to left.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("26", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Remove Duplicates from Sorted Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast (Array)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Slow writes unique values; fast scans ahead. Classic in-place.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
story.append(Table(easy_data, colWidths=[35, 175, 105, 165],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ])))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("15", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("3Sum", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Fix one element, two-pointer the rest. Sort first. Skip duplicates carefully.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("11", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Container With Most Water", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Always move the shorter height pointer — greedy + monotonicity.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("142", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Linked List Cycle II (Entry Point)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Floyd's Phase 2: reset one pointer to head, advance both 1 step.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("75", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Sort Colors (DNF)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("3-Pointer (DNF)", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("The definitive DNF problem. Three-way partition in one O(n) pass.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("287", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Find the Duplicate Number", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast (Array)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Treat array as linked list via index pointers. Apply Floyd's.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("16", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("3Sum Closest", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Fix one, two-pointer for closest sum. Track minimum absolute difference.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("80", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Remove Duplicates II (at most twice)", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast (Array)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Slow pointer writes; compare with slow-2 to allow at-most-2.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("189", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("Rotate Array", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends (3× reverse)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Reverse full array, then first k, then last n-k. Uses reverse helper.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("443", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW)),
     P("String Compression", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Slow & Fast (Array)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Fast scans groups; slow writes compressed result in-place.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
story.append(Table(med_data, colWidths=[35, 185, 105, 155],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ])))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [P("<b>#</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Problem</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Key Insight</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("42", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Trapping Rain Water", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Track max_left, max_right. Always process the shorter side — water level bounded by shorter wall.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("4", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Median of Two Sorted Arrays", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Two Array + Binary Search", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT2)),
     P("Two-pointer merge is O(m+n); optimal is binary search O(log(min(m,n))).", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("18", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("4Sum", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Opposite Ends (Nested)", S("_", fontName="Helvetica", fontSize=9, textColor=C_ACCENT)),
     P("Fix two elements with two loops; two-pointer the remaining pair. O(n³).", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
    [P("30", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED)),
     P("Substring with All Words", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Two Array + Sliding Window", S("_", fontName="Helvetica", fontSize=9, textColor=C_PURPLE)),
     P("Hybrid: two pointer over word boundaries + frequency map comparison.", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_MUTED))],
]
story.append(Table(hard_data, colWidths=[35, 185, 120, 140],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ])))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9: PITFALLS & EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(9, "Common Pitfalls & Edge Cases")

story.append(P(
    "Even with perfect pattern recognition, these are the implementation bugs "
    "that cost points in interviews. Study each one carefully.",
    sBody))

story.append(P("<b>Pitfall 1: while left < right vs. while left <= right</b>", sH2))
story.append(P(
    "This is the single most common off-by-one error in Two Pointers. "
    "The correct condition depends entirely on whether the two pointers "
    "can validly occupy the <b>same position</b>.",
    sBody))

loop_data = [
    [P("<b>Condition</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Use When</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Example</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("while left < right", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_ACCENT)),
     P("Pointers must NOT be at the same index. Comparing two DIFFERENT elements (palindrome, two-sum). Meeting means they've crossed.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Two Sum, Palindrome, Reverse String, Container With Water", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("while left <= right", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_ACCENT2)),
     P("Pointers can share same index. Binary search-style, or when a single-element window is valid. Loop processes the 'equal' case.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Binary Search, 3-pointer DNF (mid <= high)", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
    [P("while fast and fast.next", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Slow & Fast on linked list. Checks that fast has TWO hops available before taking them.", S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
     P("Cycle Detection, Middle of List, Floyd's", S("_", fontName="Helvetica", fontSize=9, textColor=C_MUTED))],
]
story.append(Table(loop_data, colWidths=[135, 230, 115],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
story.append(Spacer(1, 8))

story.append(P("<b>Pitfall 2: Integer Overflow in Midpoint Calculation</b>", sH2))
story.append(P(
    "When calculating a midpoint or checking sums in typed languages (Java, C++), "
    "the naive formula (left + right) / 2 can overflow if left and right are "
    "large integers near INT_MAX.",
    sBody))
story += code_block([
    "## ─── Integer Overflow When Finding Midpoint ─────────────────────",
    "",
    "## WRONG — can overflow in Java/C++ if left+right > INT_MAX:",
    "## mid = (left + right) / 2",
    "",
    "## CORRECT — safe subtraction form:",
    "## mid = left + (right - left) / 2",
    "",
    "## In Python this is not an issue (arbitrary precision integers),",
    "## but mentioning it in interviews shows senior awareness.",
    "",
    "## Similarly for two-sum check with large values:",
    "## WRONG in Java:  if (nums[left] + nums[right] == target)  ← may overflow",
    "## CORRECT:        if (nums[left] == target - nums[right])  ← safe rearrangement",
])

story.append(P("<b>Pitfall 3: Missing Duplicate Skip in 3Sum / kSum</b>", sH3))
story.append(P(
    "After finding a valid triplet in 3Sum, both left and right pointers must skip "
    "all duplicate values before continuing the search. Missing this produces "
    "duplicate triplets in the output.",
    sBody))
story += code_block([
    "## ─── 3Sum: Correct Duplicate Skipping ──────────────────────────",
    "def three_sum(nums):",
    "    nums.sort()",
    "    result = []",
    "    for i in range(len(nums) - 2):",
    "        if i > 0 and nums[i] == nums[i-1]: continue   ## skip dup fixed elem",
    "        left, right = i + 1, len(nums) - 1",
    "        while left < right:",
    "            s = nums[i] + nums[left] + nums[right]",
    "            if s == 0:",
    "                result.append([nums[i], nums[left], nums[right]])",
    "                ## MUST skip duplicates after finding a match",
    "                while left < right and nums[left]  == nums[left+1]:  left  += 1",
    "                while left < right and nums[right] == nums[right-1]: right -= 1",
    "                left += 1; right -= 1",
    "            elif s < 0: left  += 1",
    "            else:       right -= 1",
    "    return result",
])

story.append(P("<b>Pitfall 4: Empty Array & Single-Element Edge Cases</b>", sH3))
story += code_block([
    "## Always guard before entering two-pointer logic:",
    "def safe_two_pointer(arr, target):",
    "    if not arr or len(arr) < 2:   ## need at least 2 elements for two pointers",
    "        return []",
    "    ## ... proceed with left=0, right=len(arr)-1 ...",
    "",
    "## For linked list, guard against None head:",
    "def safe_ll(head):",
    "    if head is None or head.next is None:",
    "        return head   ## trivially handled",
    "    ## ... proceed with slow=fast=head ...",
])

story.append(P("<b>Pitfall 5: Not Incrementing mid in DNF (2-case bug)</b>", sH3))
story.append(P(
    "In the Dutch National Flag algorithm, the nums[mid]==2 case must NOT advance mid. "
    "The value swapped from position high is unknown — it has never been examined. "
    "Advancing mid would skip it. This produces incorrect sorted output.",
    sBody))

story += callout(
    "Rule of thumb: In DNF, only increment mid when you KNOW the new value at mid "
    "is correctly placed (case 0: after swap, mid now has a 1; case 1: mid was already 1). "
    "The 2-case swaps in an unknown value from high — you cannot advance mid.",
    C_RED, icon="🔴")

# Final cheat sheet
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")

story.append(P("One-page reference for all three patterns, loop conditions, and decision rules.", sBody))

cheat_data = [
    [P("<b>Pattern</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Setup</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Move Condition</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Loop Guard</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED)),
     P("<b>Use For</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED))],
    [P("Opposite Ends", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT)),
     P("L=0, R=n-1", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT)),
     P("sum&lt;target→L++; sum&gt;target→R--", S("_", fontName="Courier", fontSize=8, textColor=C_BODY)),
     P("L &lt; R", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Pair/triplet sum, palindrome, max area, rain water", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Slow &amp; Fast", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_ACCENT2)),
     P("slow=fast=head", S("_", fontName="Courier", fontSize=8, textColor=C_ACCENT2)),
     P("slow+=1, fast+=2 each iteration", S("_", fontName="Courier", fontSize=8, textColor=C_BODY)),
     P("fast and fast.next", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Cycle detect, middle node, duplicate number", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Two Arrays", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
     P("i=0, j=0", S("_", fontName="Courier", fontSize=8, textColor=C_GREEN)),
     P("advance pointer at smaller element", S("_", fontName="Courier", fontSize=8, textColor=C_BODY)),
     P("i&lt;m and j&lt;n", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("Merge, intersect, compare sequences", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
    [P("Dutch National Flag", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_PURPLE)),
     P("low=mid=0, high=n-1", S("_", fontName="Courier", fontSize=8, textColor=C_PURPLE)),
     P("0→swap(low,mid),low++,mid++; 1→mid++; 2→swap(mid,high),high--", S("_", fontName="Courier", fontSize=8, textColor=C_BODY)),
     P("mid &lt;= high", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_GREEN)),
     P("3-way partition in O(n)/O(1)", S("_", fontName="Helvetica", fontSize=8.5, textColor=C_BODY))],
]
story.append(Table(cheat_data, colWidths=[85, 80, 150, 70, 95],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BG),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_CARD, colors.HexColor("#141E2E")]),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER), ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ])))
story.append(Spacer(1, 12))

# Pitfall checklist
story.append(P("<b>Pre-Submit Checklist</b>", sH2))
checks = [
    "Loop condition: left < right (converging) or mid <= high (DNF) or fast and fast.next (slow/fast)",
    "Sorted? — If Opposite Ends is used on array data, ensure sort() is called first",
    "Duplicate skip — in 3Sum/kSum, skip equal elements after each found triplet",
    "DNF 2-case — do NOT increment mid when swapping nums[mid] with nums[high]",
    "Overflow — in Java/C++, use mid = left + (right - left) // 2, not (left + right) // 2",
    "Empty/null guard — check len(arr) < 2 or head is None before entering loop",
    "Pointer bounds — ensure left and right stay within [0, n-1] after each update",
    "Monotonicity — verify that moving each pointer changes result in exactly one predictable direction",
]
for item in checks:
    story.append(P(f"<b><font color='#34D399'>  [ ] </font></b>  {item}",
        S("_", fontName="Helvetica", fontSize=9.5, leading=15, textColor=C_BODY, leftIndent=8, spaceAfter=3)))

story.append(Spacer(1, 14))
story.append(Table([[
    P("<b>You now have the complete Two Pointers mental model.</b><br/><br/>"
      "The power of Two Pointers lies not in complexity but in insight: "
      "understanding WHY a pointer can safely move — that moving it eliminates an "
      "entire class of solutions from consideration — is what separates a mechanical "
      "memorization of templates from genuine algorithmic thinking.<br/><br/>"
      "Work the roadmap: 344 → 167 → 15 → 11 → 141 → 75. After these six problems "
      "you will see two-pointer opportunities across domains you haven't even studied yet.",
      S("_", fontName="Helvetica", fontSize=10, leading=16, textColor=C_BODY))
]], colWidths=[PAGE_W - 1.3*inch],
style=TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_CARD),
    ('BOX', (0,0), (-1,-1), 2, C_ACCENT),
    ('TOPPADDING', (0,0), (-1,-1), 16), ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 20), ('RIGHTPADDING', (0,0), (-1,-1), 20),
])))

# ── Page background ────────────────────────────────────────────────────────────
def add_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.65*inch, 0.55*inch, PAGE_W - 0.65*inch, 0.55*inch)
    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, f"Two Pointers — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")