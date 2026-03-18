from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# ── Palette ────────────────────────────────────────────────────────────────────
C_BG      = colors.HexColor("#0F172A")
C_ACCENT  = colors.HexColor("#38BDF8")
C_ACCENT2 = colors.HexColor("#818CF8")
C_GREEN   = colors.HexColor("#34D399")
C_YELLOW  = colors.HexColor("#FBBF24")
C_RED     = colors.HexColor("#F87171")
C_PURPLE  = colors.HexColor("#C084FC")
C_CODE_BG = colors.HexColor("#1E293B")
C_CODE_FG = colors.HexColor("#E2E8F0")
C_HEADING = colors.HexColor("#F1F5F9")
C_BODY    = colors.HexColor("#CBD5E1")
C_MUTED   = colors.HexColor("#64748B")
C_BORDER  = colors.HexColor("#334155")
C_CARD    = colors.HexColor("#1E293B")
C_DARK2   = colors.HexColor("#141E2E")
C_ORANGE  = colors.HexColor("#FB923C")
C_TEAL    = colors.HexColor("#2DD4BF")
C_ROSE    = colors.HexColor("#FB7185")
C_LIME    = colors.HexColor("#A3E635")
C_AMBER   = colors.HexColor("#F59E0B")
C_INDIGO  = colors.HexColor("#6366F1")

PAGE_W, PAGE_H = letter
OUT = "/mnt/user-data/outputs/Dynamic_Programming_Zero_To_Hero.pdf"

doc = SimpleDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)
CW = PAGE_W - 1.3 * inch

# ── Styles ─────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("T",  fontName="Helvetica-Bold",   fontSize=30, leading=38,
              textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)
sSubT    = S("Su", fontName="Helvetica",         fontSize=13, leading=18,
              textColor=C_ACCENT,  alignment=TA_CENTER, spaceAfter=4)
sAuthor  = S("Au", fontName="Helvetica-Oblique", fontSize=10,
              textColor=C_MUTED,  alignment=TA_CENTER, spaceAfter=20)
sH2      = S("H2", fontName="Helvetica-Bold",   fontSize=14, leading=19,
              textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)
sH3      = S("H3", fontName="Helvetica-Bold",   fontSize=11, leading=15,
              textColor=C_GREEN,   spaceBefore=8,  spaceAfter=4)
sBody    = S("Bd", fontName="Helvetica",         fontSize=10, leading=15,
              textColor=C_BODY,   spaceAfter=6, alignment=TA_JUSTIFY)
sCode    = S("Co", fontName="Courier",           fontSize=8.5, leading=13,
              textColor=C_CODE_FG, spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sCodeCmt = S("Cm", fontName="Courier-Oblique",  fontSize=8.5, leading=13,
              textColor=C_MUTED,  spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sFormula = S("Fm", fontName="Courier-Bold",     fontSize=10, leading=14,
              textColor=C_GREEN,  alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)
sCaption = S("Ca", fontName="Helvetica-Oblique", fontSize=8.5,
              textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=6)
sTOC     = S("TO", fontName="Helvetica",         fontSize=10, leading=16, textColor=C_BODY)
sTOCSub  = S("TS", fontName="Helvetica",         fontSize=9,  leading=14,
              textColor=C_MUTED, leftIndent=18)

P = Paragraph


# ── Core components ────────────────────────────────────────────────────────────
def code_block(lines, lang="python"):
    hdr  = Table([[P(f"<b>{lang}</b>",
                     S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
                 colWidths=[CW],
                 style=TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0D1929")),
                                   ("TOPPADDING",(0,0),(-1,-1),5),
                                   ("BOTTOMPADDING",(0,0),(-1,-1),5),
                                   ("LEFTPADDING",(0,0),(-1,-1),14)]))
    rows = [[P(ln or " ", sCodeCmt if ln.startswith("##") else sCode)] for ln in lines]
    body = Table(rows, colWidths=[CW],
                 style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CODE_BG),
                                   ("TOPPADDING",(0,0),(-1,-1),1),
                                   ("BOTTOMPADDING",(0,0),(-1,-1),1),
                                   ("LEFTPADDING",(0,0),(-1,-1),0),
                                   ("RIGHTPADDING",(0,0),(-1,-1),8)]))
    wrap = Table([[hdr],[body]], colWidths=[CW],
                 style=TableStyle([("BOX",(0,0),(-1,-1),1,C_BORDER),
                                   ("ROUNDEDCORNERS",[4]),
                                   ("TOPPADDING",(0,0),(-1,-1),0),
                                   ("BOTTOMPADDING",(0,0),(-1,-1),0),
                                   ("LEFTPADDING",(0,0),(-1,-1),0),
                                   ("RIGHTPADDING",(0,0),(-1,-1),0)]))
    return [wrap, Spacer(1, 8)]


def callout(text, color=C_ACCENT, icon="💡"):
    tbl = Table([[P(f"{icon}  {text}",
                    S("_", fontName="Helvetica", fontSize=9.5, leading=14,
                      textColor=color))]],
                colWidths=[CW],
                style=TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0C1F35")),
                                  ("LEFTPADDING",(0,0),(-1,-1),14),
                                  ("RIGHTPADDING",(0,0),(-1,-1),14),
                                  ("TOPPADDING",(0,0),(-1,-1),9),
                                  ("BOTTOMPADDING",(0,0),(-1,-1),9),
                                  ("LINEBEFORE",(0,0),(0,-1),3,color)]))
    return [tbl, Spacer(1, 6)]


def section_divider(num, title):
    lbl = f"{num:02d}" if num > 0 else "  "
    return [
        Spacer(1, 10),
        Table([[
            P(f"<b>{lbl}</b>",
              S("_", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT)),
            P(f"<b>{title}</b>",
              S("_", fontName="Helvetica-Bold", fontSize=18,
                textColor=C_HEADING, leading=24)),
        ]], colWidths=[44, CW-44],
            style=TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("LEFTPADDING",(0,0),(0,-1),0),
                              ("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("LINEBELOW",(0,0),(-1,-1),2,C_ACCENT),
                              ("BOTTOMPADDING",(0,0),(-1,-1),6)])),
        Spacer(1, 8)]


def std_table(data, col_widths):
    return Table(data, colWidths=col_widths,
                 style=TableStyle([
                     ("BACKGROUND",(0,0),(-1,0),C_BG),
                     ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD, C_DARK2]),
                     ("BOX",(0,0),(-1,-1),1,C_BORDER),
                     ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
                     ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                     ("TOPPADDING",(0,0),(-1,-1),7),
                     ("BOTTOMPADDING",(0,0),(-1,-1),7),
                     ("LEFTPADDING",(0,0),(-1,-1),8)]))


def th(t, c=C_MUTED):
    return P(f"<b>{t}</b>",
             S("_", fontName="Helvetica-Bold", fontSize=9, textColor=c))

def td(t, c=C_BODY, f="Helvetica", sz=9):
    return P(t, S("_", fontName=f, fontSize=sz, textColor=c, leading=13))

def tdc(t, c=C_BODY):
    return P(t, S("_", fontName="Courier", fontSize=9, textColor=c))


# ── DP Table Visualiser ────────────────────────────────────────────────────────
def dp_row(label, values, highlight_idx=None, label_color=C_MUTED,
           val_color=C_HEADING, hi_color=None, cell_w=38):
    """Single labelled row of DP values."""
    hi_color = hi_color or C_TEAL
    highlight_idx = highlight_idx or set()
    if isinstance(highlight_idx, int):
        highlight_idx = {highlight_idx}
    cells  = [P(f"<b>{label}</b>",
                S("_", fontName="Helvetica-Bold", fontSize=8,
                  textColor=label_color, alignment=TA_CENTER))]
    widths = [52]
    style_cmds = [
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("BOX",(0,0),(-1,-1),0.5,C_BORDER),
        ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("BACKGROUND",(0,0),(0,0),C_BG),
    ]
    for i, v in enumerate(values):
        fg  = hi_color    if i in highlight_idx else val_color
        bg  = colors.HexColor("#0A2E3A") if i in highlight_idx else C_CARD
        cells.append(P(str(v),
                       S("_", fontName="Courier-Bold", fontSize=10,
                         textColor=fg, alignment=TA_CENTER)))
        widths.append(cell_w)
        style_cmds.append(("BACKGROUND",(i+1,0),(i+1,0), bg))
    return Table([cells], colWidths=widths, style=TableStyle(style_cmds))


def dp_table_block(idx_labels, rows_data, caption=""):
    """
    Full DP table: index row then data rows.
    rows_data: list of (label, values, highlight_set)
    """
    result = []
    # Index header row
    idx_cells  = [P("idx",S("_",fontName="Helvetica",fontSize=7.5,
                             textColor=C_MUTED,alignment=TA_CENTER))]
    for lbl in idx_labels:
        idx_cells.append(P(f"<b>{lbl}</b>",
                           S("_",fontName="Courier-Bold",fontSize=9,
                             textColor=C_MUTED,alignment=TA_CENTER)))
    cell_w = 38
    widths = [52] + [cell_w]*len(idx_labels)
    idx_tbl = Table([idx_cells], colWidths=widths,
                    style=TableStyle([
                        ("BACKGROUND",(0,0),(-1,-1),C_BG),
                        ("TOPPADDING",(0,0),(-1,-1),4),
                        ("BOTTOMPADDING",(0,0),(-1,-1),4),
                        ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
                    ]))
    result.append(idx_tbl)
    for label, vals, hi in rows_data:
        result.append(dp_row(label, vals, hi, cell_w=cell_w))
    if caption:
        result.append(P(caption, sCaption))
    result.append(Spacer(1, 6))
    return result


def dp_2d_table(row_labels, col_labels, grid, hi_cells=None, cell_w=34):
    """2D DP table for LCS / grid problems."""
    hi_cells = hi_cells or set()
    data = []
    # Header row
    hdr = [P("",sCaption)]
    for c in col_labels:
        hdr.append(P(f"<b>{c}</b>",
                     S("_",fontName="Courier-Bold",fontSize=9,
                       textColor=C_MUTED,alignment=TA_CENTER)))
    data.append(hdr)

    for ri, (rl, row) in enumerate(zip(row_labels, grid)):
        row_cells = [P(f"<b>{rl}</b>",
                       S("_",fontName="Helvetica-Bold",fontSize=9,
                         textColor=C_MUTED,alignment=TA_CENTER))]
        for ci, v in enumerate(row):
            is_hi = (ri, ci) in hi_cells
            fg    = C_TEAL if is_hi else C_HEADING
            bg    = colors.HexColor("#0A2E3A") if is_hi else (C_CARD if ri%2==0 else C_DARK2)
            row_cells.append(P(str(v),
                               S("_",fontName="Courier-Bold",fontSize=10,
                                 textColor=fg,alignment=TA_CENTER)))
        data.append(row_cells)

    style_cmds = [
        ("BACKGROUND",(0,0),(-1,0),C_BG),
        ("BACKGROUND",(0,0),(0,-1),C_BG),
        ("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]
    for (ri, ci) in hi_cells:
        style_cmds.append(("BACKGROUND",(ci+1,ri+1),(ci+1,ri+1),
                           colors.HexColor("#0A2E3A")))
    n_cols = len(col_labels) + 1
    widths  = [38] + [cell_w]*len(col_labels)
    return [Table(data, colWidths=widths, style=TableStyle(style_cmds)),
            Spacer(1,6)]


def step_card(step_num, title, body_text, color=C_ACCENT):
    """Numbered step card for the 3-step framework."""
    inner = Table([[
        P(f"<b>{step_num}</b>",
          S("_", fontName="Helvetica-Bold", fontSize=26, textColor=color,
            alignment=TA_CENTER)),
        Table([[
            P(f"<b>{title}</b>",
              S("_", fontName="Helvetica-Bold", fontSize=12, textColor=color)),
            P(body_text,
              S("_", fontName="Helvetica", fontSize=9.5, leading=14,
                textColor=C_BODY)),
        ]], colWidths=[CW-95],
            style=TableStyle([
                ("TOPPADDING",(0,0),(-1,-1),4),
                ("BOTTOMPADDING",(0,0),(-1,-1),4),
                ("LEFTPADDING",(0,0),(-1,-1),0),
            ]))
    ]], colWidths=[55, CW-55],
        style=TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),0),
            ("LEFTPADDING",(0,0),(-1,-1),0),
        ]))
    return [
        Table([[inner]], colWidths=[CW],
              style=TableStyle([
                  ("BACKGROUND",(0,0),(-1,-1),C_CARD),
                  ("BOX",(0,0),(-1,-1),1,C_BORDER),
                  ("LINEBEFORE",(0,0),(0,-1),3,color),
                  ("TOPPADDING",(0,0),(-1,-1),10),
                  ("BOTTOMPADDING",(0,0),(-1,-1),10),
                  ("LEFTPADDING",(0,0),(-1,-1),14),
                  ("RIGHTPADDING",(0,0),(-1,-1),14),
              ])),
        Spacer(1, 8)
    ]


def add_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.65*inch, 0.55*inch, PAGE_W-0.65*inch, 0.55*inch)
    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch,
        f"Dynamic Programming — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.4*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),
                      ("ROWHEIGHT",(0,0),(-1,-1),5)])))
story.append(Spacer(1, 0.28*inch))
story.append(P("DYNAMIC PROGRAMMING", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubT))
story.append(Spacer(1, 0.12*inch))
story.append(P("Overlapping Subproblems · Optimal Substructure · State Transitions · Space Optimisation", sAuthor))
story.append(Spacer(1, 0.18*inch))

story.append(Table([[
    P("<b>What You Will Master</b>",
      S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· The two DP requirements: Optimal Substructure and Overlapping Subproblems\n"
       "· DP vs Recursion vs Greedy: when each approach wins and why\n"
       "· Top-Down Memoisation: recursion + cache — 'look up before calculating'\n"
       "· Bottom-Up Tabulation: iterative DP table built from base cases upward\n"
       "· The 3-Step Framework: Define State, Find Recurrence, Identify Base Cases\n"
       "· Linear DP: Fibonacci, Climbing Stairs, House Robber, Max Subarray\n"
       "· Knapsack Patterns: 0/1 Knapsack and Unbounded Knapsack (Coin Change)\n"
       "· String DP: Longest Common Subsequence, Edit Distance, Word Break\n"
       "· 2D / Grid DP: Unique Paths, Minimum Path Sum, Triangle\n"
       "· Interval DP: Longest Palindromic Substring, Burst Balloons\n"
       "· Space optimisation: collapsing O(n^2) tables to O(n) rolling arrays\n"
       "· 30+ categorised LeetCode problems with pattern labels and recurrences",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))
]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CARD),
                      ("BOX",(0,0),(-1,-1),1,C_BORDER),
                      ("TOPPADDING",(0,0),(-1,-1),12),
                      ("BOTTOMPADDING",(0,0),(-1,-1),12),
                      ("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.22*inch))

# Cover quick-ref
qr = [
    [th("Pattern"),             th("Recurrence Shape"),             th("Typical Complexity"),   th("Classic Problem")],
    [td("Linear 1D"),           tdc("dp[i] = f(dp[i-1], dp[i-2])"), td("O(n) time / O(1)*",C_GREEN), td("Fibonacci, House Robber",C_MUTED)],
    [td("0/1 Knapsack"),        tdc("dp[i][w] = max(skip, take)"),  td("O(n*W) time/space",C_YELLOW),  td("Target Sum, Partition Equal",C_MUTED)],
    [td("Unbounded Knapsack"),  tdc("dp[w] = min over coins"),       td("O(n*W) time / O(W)",C_GREEN),  td("Coin Change, Rod Cutting",C_MUTED)],
    [td("String DP (2D)"),      tdc("dp[i][j] = f(dp[i-1][j-1].."),td("O(n*m) time/space",C_YELLOW),  td("LCS, Edit Distance",C_MUTED)],
    [td("Grid DP"),             tdc("dp[r][c] = f(dp[r-1][c], dp[r][c-1])"),td("O(r*c)",C_YELLOW),   td("Unique Paths, Min Path Sum",C_MUTED)],
    [td("Interval DP"),         tdc("dp[i][j] = f(dp[i][k], dp[k+1][j])"),td("O(n^3) typical",C_RED),td("Burst Balloons, MCM",C_MUTED)],
    [td("Decision DP (states)"),tdc("dp[i][state] = max/min(...)"), td("O(n * states)",C_YELLOW),      td("Stock with cooldown, Robber II",C_MUTED)],
]
story.append(std_table(qr, [115, 165, 110, 128]))
story.append(Spacer(1, 0.18*inch))
story.append(P("* After space optimisation. See Section 05.", sCaption))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),
                      ("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ────────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",
     ["Optimal Substructure and Overlapping Subproblems",
      "DP vs Recursion vs Greedy","Recognising a DP Problem"]),
    ("02","The Two Approaches",
     ["Top-Down Memoisation: Recursion + Cache",
      "Bottom-Up Tabulation: Building the DP Table",
      "Comparing the Two Approaches"]),
    ("03","The 3-Step Framework",
     ["Step 1: Define the State",
      "Step 2: Find the Recurrence Relation",
      "Step 3: Identify Base Cases"]),
    ("04","Common DP Patterns",
     ["Linear DP: Fibonacci, Climbing Stairs, House Robber",
      "0/1 Knapsack: Choose Items with Weight Constraint",
      "Unbounded Knapsack: Coin Change, Word Break",
      "String DP: LCS, Edit Distance",
      "Interval DP: Longest Palindromic Substring"]),
    ("05","Space Optimisation",
     ["Rolling Variables for 1D DP",
      "Rolling Array for 2D DP",
      "When Space Optimisation is Impossible"]),
    ("06","DP on Grids",
     ["Unique Paths","Minimum Path Sum","Triangle (Top-Down)"]),
    ("07","Comparison and Decision Making",
     ["Memoisation vs Tabulation","DP vs BFS/DFS vs Greedy",
      "Decision Flowchart"]),
    ("08","Problem Roadmap",
     ["Easy Problems","Medium Problems","Hard Problems"]),
    ("09","Edge Case Checklist",
     ["Initialisation: 0 vs Infinity vs -1",
      "Off-by-One Errors and Array Sizes",
      "Empty Strings and Zero-Capacity Constraints"]),
]
for num, title, subs in toc:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1, 3))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §1  CORE PHILOSOPHY
# ════════════════════════════════════════════════════════
story += section_divider(1, "The Core Philosophy")

story.append(P("<b>What Is Dynamic Programming?</b>", sH2))
story.append(P(
    "Dynamic Programming is a technique for solving problems by "
    "<b>breaking them into overlapping subproblems</b>, solving each subproblem "
    "exactly once, and <b>storing the result</b> so it is never recomputed. "
    "The name is historical (coined by Richard Bellman in the 1950s) and "
    "does not describe the technique — think of it as "
    "<i>smart recursion with a memory</i>.",
    sBody))

story.append(P("<b>The Two Requirements</b>", sH2))

req_data = [
    [th("Requirement"),             th("Definition"),                                th("Test Question")],
    [td("Optimal Substructure",C_ACCENT),
     td("The optimal solution to the whole problem can be constructed from optimal solutions to its subproblems.",C_BODY),
     td("'If I knew the best answer for every smaller version, could I compute the answer for the full problem?'",C_MUTED)],
    [td("Overlapping Subproblems",C_GREEN),
     td("The same subproblems recur multiple times during the naive recursive solution.",C_BODY),
     td("'Does the recursion tree recompute the same (i,j) pair more than once?'",C_MUTED)],
]
story.append(std_table(req_data, [145, 215, 158]))
story.append(Spacer(1, 8))

story += callout(
    "Quick diagnostic: draw the first 3 levels of the recursion tree. "
    "If you see the same function call appear more than once, you have overlapping "
    "subproblems — DP will help. If not, divide-and-conquer (merge sort, quick sort) "
    "is sufficient.",
    C_ACCENT, icon="🔍")

story.append(P("<b>DP vs Recursion vs Greedy</b>", sH2))
cmp3 = [
    [th("Approach"),          th("Strategy"),                         th("Subproblem reuse?"), th("Optimal guarantee?"), th("When to use")],
    [td("Brute Force Recursion",C_BODY),
     td("Try all possibilities, backtrack",C_BODY),
     td("No — recomputes",C_RED),
     td("Yes — tries all",C_GREEN),
     td("n is tiny (n <= 20); no structure",C_MUTED)],
    [td("DP (Memoisation)",C_ACCENT),
     td("Recursion + cache results",C_BODY),
     td("Yes — O(1) lookup",C_GREEN),
     td("Yes — proves optimality",C_GREEN),
     td("Overlapping subproblems + optimal substructure",C_MUTED)],
    [td("DP (Tabulation)",C_ACCENT),
     td("Bottom-up iterative table",C_BODY),
     td("Yes — table lookup",C_GREEN),
     td("Yes",C_GREEN),
     td("Same as memoisation; prefer when recursion depth is a risk",C_MUTED)],
    [td("Greedy",C_YELLOW),
     td("Locally optimal choice at each step",C_BODY),
     td("N/A — no recomputation",C_MUTED),
     td("Only if greedy choice property holds",C_YELLOW),
     td("Can prove locally optimal = globally optimal (activity selection, Dijkstra)",C_MUTED)],
    [td("Divide and Conquer",C_PURPLE),
     td("Split into non-overlapping subproblems",C_BODY),
     td("No overlap — independent",C_MUTED),
     td("Yes",C_GREEN),
     td("Merge sort, binary search — subproblems do NOT overlap",C_MUTED)],
]
story.append(std_table(cmp3, [110, 125, 80, 80, 123]))
story.append(Spacer(1, 8))

story.append(P("<b>Recognising a DP Problem</b>", sH3))
recog_data = [
    [th("Signal in the problem"),                   th("Likely DP pattern")],
    [td("'Find the maximum / minimum ...'",C_BODY), td("Optimisation DP — dp[i] = max/min over choices",C_MUTED)],
    [td("'Count the number of ways ...'",C_BODY),   td("Counting DP — dp[i] += dp[i-k]",C_MUTED)],
    [td("'Can you reach / is it possible ...'",C_BODY),td("Boolean DP — dp[i] = dp[i-k] or dp[i-j]",C_MUTED)],
    [td("'Subsequence / substring ...'",C_BODY),    td("String DP — dp[i][j] over two indices",C_MUTED)],
    [td("'Partition into parts ...'",C_BODY),       td("Knapsack / subset-sum variant",C_MUTED)],
    [td("'Intervals / ranges ...'",C_BODY),         td("Interval DP — dp[i][j] over range [i,j]",C_MUTED)],
    [td("'Decisions at each step with state ...'",C_BODY),td("State-machine DP — dp[i][state]",C_MUTED)],
]
story.append(std_table(recog_data, [225, 293]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §2  THE TWO APPROACHES
# ════════════════════════════════════════════════════════
story += section_divider(2, "The Two Approaches")

story.append(P("<b>Top-Down Memoisation: Recursion + Cache</b>", sH2))
story.append(P(
    "Start with the recursive solution and add a cache. "
    "The golden rule: <b>look up before calculating</b>. "
    "If the answer for this set of parameters is already in the memo, "
    "return it immediately. Otherwise compute, store, then return.",
    sBody))

story += code_block([
    "## ─── Top-Down Memoisation Template ─────────────────────────────",
    "from functools import lru_cache",
    "",
    "## Approach A: @lru_cache (cleanest for interviews)",
    "@lru_cache(maxsize=None)",
    "def dp(state_params):",
    "    ## Base cases first",
    "    if base_condition: return base_value",
    "    ## Recurrence: combine results of subproblems",
    "    return combine(dp(smaller_state_1), dp(smaller_state_2))",
    "",
    "## Approach B: explicit dictionary memo",
    "memo = {}",
    "def dp(state_params):",
    "    if state_params in memo: return memo[state_params]  ## LOOK UP FIRST",
    "    if base_condition: return base_value",
    "    result = combine(dp(smaller_1), dp(smaller_2))",
    "    memo[state_params] = result                         ## STORE RESULT",
    "    return result",
    "",
    "## ─── Fibonacci with memoisation ─────────────────────────────────",
    "## WITHOUT memo: O(2^n) — exponential recomputation",
    "## WITH memo:    O(n)   — each fib(k) computed exactly once",
    "memo = {}",
    "def fib(n):",
    "    if n <= 1: return n                 ## base cases",
    "    if n in memo: return memo[n]        ## look up",
    "    memo[n] = fib(n-1) + fib(n-2)      ## compute and store",
    "    return memo[n]",
])

story.append(P("<b>Bottom-Up Tabulation: Building the DP Table</b>", sH2))
story.append(P(
    "Start from the smallest subproblems (base cases) and iteratively fill "
    "a table until you reach the target. No recursion, no stack frames — "
    "just array indexing. The table's last cell (or a specific cell) holds the answer.",
    sBody))

story += code_block([
    "## ─── Bottom-Up Tabulation Template ─────────────────────────────",
    "def dp_tabulation(n, input_data):",
    "    ## 1. Allocate DP table with appropriate size",
    "    dp = [INITIAL_VALUE] * (n + 1)  ## often n+1 to handle 0-indexed base",
    "",
    "    ## 2. Set base cases explicitly",
    "    dp[0] = BASE_CASE_0",
    "    dp[1] = BASE_CASE_1",
    "",
    "    ## 3. Fill table in dependency order (small -> large)",
    "    for i in range(2, n + 1):",
    "        dp[i] = recurrence(dp[i-1], dp[i-2], input_data[i])",
    "",
    "    ## 4. Answer is in dp[target]",
    "    return dp[n]",
    "",
    "## ─── Fibonacci with tabulation ──────────────────────────────────",
    "def fib_tab(n):",
    "    if n <= 1: return n",
    "    dp = [0] * (n + 1)",
    "    dp[0], dp[1] = 0, 1",
    "    for i in range(2, n + 1):",
    "        dp[i] = dp[i-1] + dp[i-2]",
    "    return dp[n]",
])

# DP table for fibonacci
story.append(P("<b>Visual: Fibonacci DP Table (n=6)</b>", sH3))
story += dp_table_block(
    ["0", "1", "2", "3", "4", "5", "6"],
    [("dp[i]", [0, 1, 1, 2, 3, 5, 8], {6})],
    "dp[i] = dp[i-1] + dp[i-2].  Base: dp[0]=0, dp[1]=1.  Answer: dp[6] = 8"
)

story.append(P("<b>Comparing the Two Approaches</b>", sH3))
memo_tab = [
    [th("Dimension"),          th("Top-Down (Memoisation)"),           th("Bottom-Up (Tabulation)")],
    [td("Code style"),         td("Recursive — mirrors problem definition",C_BODY),
     td("Iterative — explicit loops",C_BODY)],
    [td("Subproblem order"),   td("Computed on demand — only needed states",C_GREEN),
     td("All states in fixed order — may compute unneeded ones",C_YELLOW)],
    [td("Stack frames"),       td("O(depth) call stack — risk of RecursionError",C_RED),
     td("O(1) — no recursion depth issue",C_GREEN)],
    [td("Initialisation"),     td("Base cases in if-guards at function top",C_BODY),
     td("Explicit dp[0], dp[1] assignments before loop",C_BODY)],
    [td("Cache overhead"),     td("Dict/lru_cache has hash overhead",C_YELLOW),
     td("Direct array indexing — faster in practice",C_GREEN)],
    [td("Space optimisation"), td("Harder — memo dict persists all states",C_YELLOW),
     td("Easy — just keep last 1-2 rows",C_GREEN)],
    [td("Debugging"),          td("Easier to trace — follows natural call order",C_GREEN),
     td("Requires understanding fill order",C_YELLOW)],
    [td("Interview preference"),td("Great for explaining — code writes itself",C_GREEN),
     td("Preferred when asked 'O(1) space' or n is very large",C_BODY)],
]
story.append(std_table(memo_tab, [125, 200, 193]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §3  THE 3-STEP FRAMEWORK
# ════════════════════════════════════════════════════════
story += section_divider(3, "The 3-Step Framework for Any DP Problem")

story.append(P(
    "Every DP problem — regardless of difficulty — can be cracked with "
    "the same three questions. Answer them in order and the code writes itself.",
    sBody))

story += step_card("1", "Define the State",
    "What does dp[i] (or dp[i][j]) represent in plain English? "
    "Be precise: 'dp[i] = the maximum profit achievable using the first i items' "
    "is correct. 'dp[i] = some value at i' is not. "
    "A vague state definition is the #1 cause of DP bugs.",
    C_ACCENT)

story += step_card("2", "Find the Recurrence Relation",
    "How do you compute dp[i] from previously computed dp[j] where j < i? "
    "This is the transition equation — the mathematical heart of the solution. "
    "Ask: 'What choice am I making at step i? What are my options? "
    "Which option leads to the optimal dp[i]?'",
    C_GREEN)

story += step_card("3", "Identify the Base Cases",
    "Where does the computation start? Base cases are the smallest valid inputs "
    "for which the answer is known directly (no recursion needed). "
    "Typical bases: dp[0] = 0 (empty set), dp[1] = first element, "
    "dp[i][0] = 0 (empty string). Wrong base cases propagate incorrect values "
    "through the entire table.",
    C_PURPLE)

# Worked example: House Robber
story.append(P("<b>Worked Example: House Robber</b>", sH2))
story.append(P(
    "Given a row of houses with values, find the maximum sum "
    "you can steal without robbing two adjacent houses.",
    sBody))

story.append(P("<b>Step 1 — State:</b>  dp[i] = maximum money robbable from houses 0..i", sFormula))
story.append(P("<b>Step 2 — Recurrence:</b>  dp[i] = max(dp[i-1],  dp[i-2] + nums[i])", sFormula))
story.append(P("<b>              Choice:</b>  skip house i  OR  rob house i + best up to i-2", sFormula))
story.append(P("<b>Step 3 — Base cases:</b>  dp[0] = nums[0]    dp[1] = max(nums[0], nums[1])", sFormula))
story.append(Spacer(1, 6))

# House Robber trace: nums = [2, 7, 9, 3, 1]
story.append(P("nums = [2, 7, 9, 3, 1]", sH3))
story += dp_table_block(
    ["0", "1", "2", "3", "4"],
    [("nums[i]", [2, 7, 9, 3, 1], set()),
     ("dp[i]",   [2, 7, 11,11,12], {4})],
    "dp[2]=max(7, 2+9)=11.  dp[3]=max(11, 7+3)=11.  dp[4]=max(11, 11+1)=12.  Answer=12"
)

story += code_block([
    "## ─── House Robber — bottom-up O(n) time, O(n) space ─────────────",
    "def rob(nums):",
    "    n = len(nums)",
    "    if n == 1: return nums[0]",
    "    dp = [0] * n",
    "    dp[0] = nums[0]",
    "    dp[1] = max(nums[0], nums[1])",
    "    for i in range(2, n):",
    "        dp[i] = max(dp[i-1],          ## skip house i",
    "                    dp[i-2] + nums[i]) ## rob house i",
    "    return dp[n-1]",
    "",
    "## Space-optimised O(1) — see Section 05 for full explanation",
    "def rob_optimised(nums):",
    "    prev2, prev1 = 0, 0",
    "    for num in nums:",
    "        prev2, prev1 = prev1, max(prev1, prev2 + num)",
    "    return prev1",
])
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §4  COMMON DP PATTERNS
# ════════════════════════════════════════════════════════
story += section_divider(4, "Common DP Patterns")

# ──────────────────────────────────────────────────────
# 4A: Linear DP
# ──────────────────────────────────────────────────────
story.append(P("<b>Pattern 1 — Linear DP</b>", sH2))
story.append(P(
    "The simplest DP shape: dp[i] depends only on a constant number of "
    "previous entries (dp[i-1], dp[i-2], ...). "
    "State is a single index; transitions look left.",
    sBody))

lin_data = [
    [th("Problem"),            th("State"),             th("Recurrence"),                           th("Base Cases")],
    [td("Fibonacci",C_BODY),   tdc("dp[i] = F(i)"),    tdc("dp[i-1] + dp[i-2]"),                   tdc("dp[0]=0, dp[1]=1")],
    [td("Climbing Stairs",C_BODY),tdc("dp[i] = ways"),  tdc("dp[i-1] + dp[i-2]"),                   tdc("dp[1]=1, dp[2]=2")],
    [td("House Robber",C_BODY), tdc("dp[i] = max rob"), tdc("max(dp[i-1], dp[i-2]+nums[i])"),        tdc("dp[0]=nums[0]")],
    [td("Max Subarray",C_BODY), tdc("dp[i] = max ending at i"),tdc("max(nums[i], dp[i-1]+nums[i])"), tdc("dp[0]=nums[0]")],
    [td("Min Cost Stairs",C_BODY),tdc("dp[i] = min cost"),tdc("min(dp[i-1], dp[i-2]) + cost[i]"),   tdc("dp[0]=cost[0]")],
]
story.append(std_table(lin_data, [110, 130, 175, 103]))
story.append(Spacer(1, 10))

# ──────────────────────────────────────────────────────
# 4B: 0/1 Knapsack
# ──────────────────────────────────────────────────────
story.append(P("<b>Pattern 2 — 0/1 Knapsack</b>", sH2))
story.append(P(
    "Given n items, each with a weight and value, fill a knapsack of capacity W "
    "to maximise total value. Each item is used at most once (0 or 1 time). "
    "The DP table has two axes: items considered (rows) and remaining capacity (columns).",
    sBody))

story.append(P("State:  dp[i][w] = max value using first i items with capacity w", sFormula))
story.append(P("Recurrence:  dp[i][w] = max(dp[i-1][w],  dp[i-1][w - weight[i]] + value[i])", sFormula))

story += code_block([
    "## ─── 0/1 Knapsack — O(n*W) time and space ──────────────────────",
    "def knapsack_01(weights, values, W):",
    "    n  = len(weights)",
    "    dp = [[0]*(W+1) for _ in range(n+1)]",
    "",
    "    for i in range(1, n+1):       ## for each item (1-indexed)",
    "        for w in range(W+1):      ## for each capacity",
    "            ## Option 1: skip item i",
    "            dp[i][w] = dp[i-1][w]",
    "            ## Option 2: take item i (only if it fits)",
    "            if weights[i-1] <= w:",
    "                take = dp[i-1][w - weights[i-1]] + values[i-1]",
    "                dp[i][w] = max(dp[i][w], take)",
    "",
    "    return dp[n][W]",
    "",
    "## ─── Space-optimised: 1D rolling array O(W) space ───────────────",
    "def knapsack_01_opt(weights, values, W):",
    "    dp = [0] * (W + 1)",
    "    for i in range(len(weights)):",
    "        ## CRITICAL: iterate W down to prevent reusing same item",
    "        for w in range(W, weights[i]-1, -1):",
    "            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])",
    "    return dp[W]",
])

story += callout(
    "Key 0/1 Knapsack insight: when collapsing to 1D, iterate capacity "
    "RIGHT TO LEFT (W down to weight[i]). This ensures dp[w - weight[i]] "
    "still refers to the PREVIOUS item's state, not the current item — "
    "preventing an item from being selected more than once.",
    C_YELLOW, icon="⚠️")

# ──────────────────────────────────────────────────────
# 4C: Unbounded Knapsack
# ──────────────────────────────────────────────────────
story.append(P("<b>Pattern 3 — Unbounded Knapsack (Coin Change)</b>", sH2))
story.append(P(
    "Like 0/1 Knapsack, but each item can be used <i>unlimited</i> times. "
    "The structural change is subtle: iterate capacity LEFT TO RIGHT in the "
    "1D optimised form, allowing the same item to be reused in one pass.",
    sBody))

story.append(P("State:  dp[amount] = minimum coins needed to make exactly 'amount'", sFormula))
story.append(P("Recurrence:  dp[amount] = min over coins c:  dp[amount - c] + 1", sFormula))

story += code_block([
    "## ─── Coin Change (Minimum Coins) — O(amount * len(coins)) ──────",
    "def coin_change(coins, amount):",
    "    dp = [float('inf')] * (amount + 1)",
    "    dp[0] = 0                     ## base: 0 coins needed for amount 0",
    "",
    "    for a in range(1, amount + 1):",
    "        for coin in coins:",
    "            if coin <= a:",
    "                dp[a] = min(dp[a], dp[a - coin] + 1)",
    "",
    "    return dp[amount] if dp[amount] != float('inf') else -1",
    "",
    "## ─── Coin Change II (Count Ways) ────────────────────────────────",
    "def coin_change_ways(coins, amount):",
    "    dp = [0] * (amount + 1)",
    "    dp[0] = 1                     ## one way to make 0: use no coins",
    "    for coin in coins:",
    "        ## Outer loop over coins = each coin considered once across all amounts",
    "        for a in range(coin, amount + 1):",
    "            dp[a] += dp[a - coin]",
    "    return dp[amount]",
    "",
    "## ─── Word Break ─────────────────────────────────────────────────",
    "def word_break(s, word_dict):",
    "    word_set = set(word_dict)",
    "    n  = len(s)",
    "    dp = [False] * (n + 1)",
    "    dp[0] = True                  ## empty string is always breakable",
    "    for i in range(1, n + 1):",
    "        for j in range(i):        ## try all splits s[j:i]",
    "            if dp[j] and s[j:i] in word_set:",
    "                dp[i] = True",
    "                break",
    "    return dp[n]",
])
story.append(PageBreak())

# ──────────────────────────────────────────────────────
# 4D: String DP (LCS / Edit Distance)
# ──────────────────────────────────────────────────────
story.append(P("<b>Pattern 4 — String DP: LCS and Edit Distance</b>", sH2))
story.append(P(
    "String DP uses a 2D table where dp[i][j] represents the answer for "
    "the first i characters of string s and the first j characters of string t. "
    "The transition depends on whether s[i-1] == t[j-1].",
    sBody))

story.append(P("LCS Recurrence:", sH3))
story.append(P(
    "dp[i][j] = dp[i-1][j-1] + 1              if s[i-1] == t[j-1]", sFormula))
story.append(P(
    "dp[i][j] = max(dp[i-1][j], dp[i][j-1])   otherwise", sFormula))

# LCS Table: "ABCBDAB" vs "BDCABA" — show small 4x4 example "ABCD" vs "ACBD"
s1, s2 = "ABCD", "ACBD"
lcs_grid = [[0]*5 for _ in range(5)]
for i in range(1,5):
    for j in range(1,5):
        if s1[i-1] == s2[j-1]:
            lcs_grid[i][j] = lcs_grid[i-1][j-1] + 1
        else:
            lcs_grid[i][j] = max(lcs_grid[i-1][j], lcs_grid[i][j-1])

story.append(P("LCS Table: s1='ABCD'  s2='ACBD'  — result = LCS length = 3 (ABD or ACD)", sH3))
story += dp_2d_table(
    ["", "A", "B", "C", "D"],
    ["", "A", "C", "B", "D"],
    lcs_grid,
    hi_cells={(4,4)},
    cell_w=36
)

story += code_block([
    "## ─── Longest Common Subsequence ────────────────────────────────",
    "def lcs(s, t):",
    "    m, n = len(s), len(t)",
    "    dp = [[0]*(n+1) for _ in range(m+1)]",
    "    for i in range(1, m+1):",
    "        for j in range(1, n+1):",
    "            if s[i-1] == t[j-1]:           ## characters match",
    "                dp[i][j] = dp[i-1][j-1] + 1",
    "            else:                           ## skip one character from either",
    "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])",
    "    return dp[m][n]",
    "",
    "## ─── Edit Distance (Levenshtein) ────────────────────────────────",
    "## dp[i][j] = min edits to convert s[:i] to t[:j]",
    "def edit_distance(s, t):",
    "    m, n = len(s), len(t)",
    "    dp = [[0]*(n+1) for _ in range(m+1)]",
    "    for i in range(m+1): dp[i][0] = i   ## delete all of s",
    "    for j in range(n+1): dp[0][j] = j   ## insert all of t",
    "    for i in range(1, m+1):",
    "        for j in range(1, n+1):",
    "            if s[i-1] == t[j-1]:",
    "                dp[i][j] = dp[i-1][j-1]        ## no edit needed",
    "            else:",
    "                dp[i][j] = 1 + min(",
    "                    dp[i-1][j],   ## delete from s",
    "                    dp[i][j-1],   ## insert into s",
    "                    dp[i-1][j-1]) ## replace",
    "    return dp[m][n]",
])

# ──────────────────────────────────────────────────────
# 4E: Interval DP
# ──────────────────────────────────────────────────────
story.append(P("<b>Pattern 5 — Interval DP</b>", sH2))
story.append(P(
    "Interval DP defines dp[i][j] as the answer over the subarray or substring "
    "from index i to j. The key structural insight: every interval [i,j] can be "
    "split at some pivot k, with the answer combining results from [i,k] and [k+1,j] "
    "(or [i,k-1] and [k+1,j] depending on the problem). "
    "Fill order must respect interval length: shorter intervals before longer ones.",
    sBody))

story.append(P("Longest Palindromic Substring:", sH3))
story.append(P("dp[i][j] = True if s[i..j] is a palindrome", sFormula))
story.append(P("dp[i][j] = (s[i]==s[j]) AND dp[i+1][j-1]   [base: all len-1 and len-2]", sFormula))

story += code_block([
    "## ─── Longest Palindromic Substring — O(n^2) DP ─────────────────",
    "def longest_palindrome(s):",
    "    n  = len(s)",
    "    dp = [[False]*n for _ in range(n)]",
    "    start, max_len = 0, 1",
    "",
    "    ## Base case: all length-1 substrings are palindromes",
    "    for i in range(n): dp[i][i] = True",
    "",
    "    ## Base case: length-2 substrings",
    "    for i in range(n-1):",
    "        if s[i] == s[i+1]:",
    "            dp[i][i+1] = True",
    "            start, max_len = i, 2",
    "",
    "    ## Fill by increasing LENGTH (critical for interval DP)",
    "    for length in range(3, n+1):      ## window size 3, 4, ..., n",
    "        for i in range(n - length + 1):",
    "            j = i + length - 1",
    "            if s[i] == s[j] and dp[i+1][j-1]:",
    "                dp[i][j] = True",
    "                if length > max_len:",
    "                    start, max_len = i, length",
    "",
    "    return s[start : start + max_len]",
    "",
    "## ─── Burst Balloons (harder interval DP) ────────────────────────",
    "## dp[i][j] = max coins from bursting all balloons in (i, j)",
    "## For each LAST balloon k to burst in range (i, j):",
    "## dp[i][j] = max over k: dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j]",
])
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §5  SPACE OPTIMISATION
# ════════════════════════════════════════════════════════
story += section_divider(5, "Space Optimisation")

story.append(P("<b>The Core Insight</b>", sH2))
story.append(P(
    "Most 1D DP recurrences only look at the previous 1 or 2 entries — "
    "the entire dp[] array is never needed simultaneously. "
    "Replacing the array with a few scalar variables collapses O(n) to O(1). "
    "For 2D DP, if row i only depends on row i-1, keep only two rows — "
    "O(n^2) collapses to O(n).",
    sBody))

story.append(P("<b>1D Space Optimisation: Rolling Variables</b>", sH3))

so_data = [
    [th("Pattern"),          th("Before optimisation"),  th("After optimisation"),       th("Space saved")],
    [td("Fibonacci / Climbing Stairs",C_BODY),
     tdc("dp[i] = dp[i-1] + dp[i-2]"),
     tdc("a, b = b, a+b"),
     td("O(n) -> O(1)",C_GREEN)],
    [td("House Robber",C_BODY),
     tdc("dp[i] = max(dp[i-1], dp[i-2]+v)"),
     tdc("prev2, prev1 = prev1, max(prev1, prev2+v)"),
     td("O(n) -> O(1)",C_GREEN)],
    [td("Coin Change (1D)",C_BODY),
     tdc("dp[a] = min(dp[a], dp[a-c]+1)"),
     tdc("Same — 1D already optimal"),
     td("Already O(amount)",C_MUTED)],
    [td("LCS / Edit Distance (2D)",C_BODY),
     tdc("dp[i][j] uses only row i-1"),
     tdc("Alternate two rows: cur[], prev[]"),
     td("O(mn) -> O(min(m,n))",C_GREEN)],
    [td("0/1 Knapsack (2D)",C_BODY),
     tdc("dp[i][w] = max(dp[i-1][w], ...)"),
     tdc("Reverse loop: for w in range(W, wt-1, -1)"),
     td("O(nW) -> O(W)",C_GREEN)],
]
story.append(std_table(so_data, [140, 165, 155, 58]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Before: O(n) space ─────────────────────────────────────────",
    "dp = [0] * (n + 1)",
    "dp[0], dp[1] = 0, 1",
    "for i in range(2, n+1):",
    "    dp[i] = dp[i-1] + dp[i-2]",
    "return dp[n]",
    "",
    "## ─── After: O(1) space — rolling variables ──────────────────────",
    "a, b = 0, 1                ## a = dp[i-2], b = dp[i-1]",
    "for _ in range(2, n+1):",
    "    a, b = b, a + b        ## slide the window forward",
    "return b",
    "",
    "## ─── 2D -> 1D: LCS space optimisation ──────────────────────────",
    "## Before: dp[m+1][n+1]  — O(m*n)",
    "## After: only keep previous row  — O(n)",
    "def lcs_space_opt(s, t):",
    "    m, n = len(s), len(t)",
    "    prev = [0] * (n + 1)   ## represents dp[i-1][*]",
    "    for i in range(1, m+1):",
    "        curr = [0] * (n + 1)",
    "        for j in range(1, n+1):",
    "            if s[i-1] == t[j-1]:",
    "                curr[j] = prev[j-1] + 1",
    "            else:",
    "                curr[j] = max(prev[j], curr[j-1])",
    "        prev = curr",
    "    return prev[n]",
    "",
    "## ─── Caution: when space optimisation is NOT possible ───────────",
    "## If you need to reconstruct the solution (not just the value),",
    "## you must keep the full table to trace back the optimal choices.",
    "## Example: actual LCS string requires the full dp table for backtracking.",
])

story += callout(
    "Rule for 0/1 Knapsack 1D: iterate capacity RIGHT TO LEFT. "
    "This ensures dp[w - weight[i]] still holds the i-1 row value. "
    "For Unbounded Knapsack: iterate LEFT TO RIGHT — "
    "you WANT dp[w - coin] to already include the current coin.",
    C_ORANGE, icon="🔄")
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §6  DP ON GRIDS
# ════════════════════════════════════════════════════════
story += section_divider(6, "DP on Grids")

story.append(P("<b>The Pattern</b>", sH2))
story.append(P(
    "Grid DP defines dp[r][c] as the answer for the subproblem ending at cell (r, c). "
    "Because movement is typically right or down only, "
    "each cell depends only on its left neighbour dp[r][c-1] "
    "and/or upper neighbour dp[r-1][c]. "
    "Base cases are the first row and first column.",
    sBody))

grid_data = [
    [th("Problem"),               th("State"),                   th("Recurrence"),                          th("Answer")],
    [td("Unique Paths",C_BODY),   tdc("dp[r][c] = num ways"),    tdc("dp[r-1][c] + dp[r][c-1]"),           tdc("dp[m-1][n-1]")],
    [td("Min Path Sum",C_BODY),   tdc("dp[r][c] = min cost"),    tdc("grid[r][c] + min(dp[r-1][c], dp[r][c-1])"),tdc("dp[m-1][n-1]")],
    [td("Max Gold",C_BODY),       tdc("dp[r][c] = max gold"),    tdc("grid[r][c] + max of valid neighbours"),tdc("max over all dp")],
    [td("Dungeon Game",C_BODY),   tdc("dp[r][c] = min HP needed"),tdc("max(1, min(right,down) - dungeon[r][c])"),tdc("dp[0][0]")],
    [td("Triangle",C_BODY),       tdc("dp[i][j] = min path"),    tdc("triangle[i][j] + min(dp[i-1][j-1], dp[i-1][j])"),tdc("min(dp[-1])")],
]
story.append(std_table(grid_data, [110, 130, 195, 83]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Unique Paths — O(m*n) time, O(n) space ────────────────────",
    "def unique_paths(m, n):",
    "    dp = [1] * n           ## first row: only 1 way to reach any cell (go right)",
    "    for r in range(1, m):",
    "        for c in range(1, n):",
    "            dp[c] += dp[c-1]   ## dp[c] = from above (dp[c]) + from left (dp[c-1])",
    "    return dp[n-1]",
    "",
    "## ─── Minimum Path Sum — O(m*n) time, O(n) space ─────────────────",
    "def min_path_sum(grid):",
    "    m, n = len(grid), len(grid[0])",
    "    dp = [float('inf')] * n",
    "    dp[0] = 0",
    "    for r in range(m):",
    "        for c in range(n):",
    "            if c == 0:",
    "                dp[c] = dp[c] + grid[r][c]     ## can only come from above",
    "            else:",
    "                dp[c] = grid[r][c] + min(dp[c], dp[c-1])",
    "    return dp[n-1]",
    "",
    "## ─── Unique Paths II (with obstacles) ──────────────────────────",
    "def unique_paths_with_obstacles(grid):",
    "    m, n = len(grid), len(grid[0])",
    "    dp   = [0] * n",
    "    dp[0] = 1 if grid[0][0] == 0 else 0   ## 0 if start is blocked",
    "    for r in range(m):",
    "        for c in range(n):",
    "            if grid[r][c] == 1:            ## obstacle: no ways to reach here",
    "                dp[c] = 0",
    "            elif c > 0:",
    "                dp[c] += dp[c-1]",
    "    return dp[n-1]",
])

# Visual 3x3 grid trace
story.append(P("<b>Visual: Min Path Sum on 3x3 Grid</b>", sH3))
grid_vis = [[1,3,1],[1,5,1],[4,2,1]]
dp_g = [[0]*3 for _ in range(3)]
dp_g[0][0] = grid_vis[0][0]
for c in range(1,3): dp_g[0][c] = dp_g[0][c-1] + grid_vis[0][c]
for r in range(1,3): dp_g[r][0] = dp_g[r-1][0] + grid_vis[r][0]
for r in range(1,3):
    for c in range(1,3):
        dp_g[r][c] = grid_vis[r][c] + min(dp_g[r-1][c], dp_g[r][c-1])

story += dp_2d_table(
    ["r=0","r=1","r=2"],
    ["c=0","c=1","c=2"],
    dp_g,
    hi_cells={(2,2)},
    cell_w=48
)
story.append(P("grid=[[1,3,1],[1,5,1],[4,2,1]] — Min Path Sum = 7  (1+3+1+1+1)", sCaption))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §7  COMPARISON & DECISION
# ════════════════════════════════════════════════════════
story += section_divider(7, "Comparison & Decision Making")

story.append(P("<b>DP vs BFS/DFS vs Greedy</b>", sH2))
dp_vs = [
    [th("Dimension"),          th("Dynamic Programming"),             th("BFS / DFS"),                   th("Greedy")],
    [td("Core idea"),          td("Optimal subproblems + caching",C_BODY),
     td("Exhaustive traversal / shortest path",C_BODY),
     td("Locally optimal choice at each step",C_BODY)],
    [td("Shortest path (unweighted)"),td("Possible but overkill",C_YELLOW),
     td("BFS — O(V+E), guaranteed shortest",C_GREEN),
     td("Not applicable without structure",C_RED)],
    [td("Shortest path (weighted)"),td("DP/Bellman-Ford — handles negatives",C_GREEN),
     td("Dijkstra (special BFS) — non-neg weights",C_GREEN),
     td("Not general",C_RED)],
    [td("Count all ways"),     td("Yes — dp[i] sums over choices",C_GREEN),
     td("DFS backtracking — exponential",C_RED),
     td("No",C_RED)],
    [td("Optimal partition"),  td("Yes — 0/1 Knapsack, Coin Change",C_GREEN),
     td("BFS can explore states",C_YELLOW),
     td("Only if exchange argument holds",C_YELLOW)],
    [td("Cycle handling"),     td("Requires DAG or bounded state",C_YELLOW),
     td("Handles cycles with visited set",C_GREEN),
     td("Not applicable",C_RED)],
    [td("Complexity"),         td("Polynomial — O(states * transitions)",C_GREEN),
     td("O(V+E) — linear",C_GREEN),
     td("O(n log n) typical",C_GREEN)],
    [td("Use when"),
     td("Overlapping subproblems + optimal substructure; count/min/max queries",C_MUTED),
     td("Graph traversal; shortest path; reachability; connected components",C_MUTED),
     td("Local choice = global optimum provable; activity selection; scheduling",C_MUTED)],
]
story.append(std_table(dp_vs, [120, 160, 130, 108]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1","Does the problem ask for minimum, maximum, or count of something?",    C_ACCENT, False),
    (" YES","Likely DP or Greedy. Continue to Q2.",                              C_GREEN,  True),
    (" NO", "Likely BFS/DFS for connectivity or exhaustive search.",             C_MUTED,  True),
    ("Q2","Can a locally optimal choice at each step guarantee global optimum?", C_ACCENT, False),
    (" YES","Try Greedy first — O(n log n) and simpler. Verify with exchange argument.",C_YELLOW,True),
    (" NO", "Use DP. Continue to Q3.",                                           C_MUTED,  True),
    ("Q3","Does the problem involve a sequence, substring, or grid?",            C_ACCENT, False),
    (" YES 1D","Single index i: Linear DP. dp[i] from dp[i-1], dp[i-2].",       C_GREEN,  True),
    (" YES 2D","Two indices i,j: String DP or Grid DP. dp[i][j] table.",         C_TEAL,   True),
    ("Q4","Does the problem involve choosing items with a capacity constraint?", C_ACCENT, False),
    (" YES once","0/1 Knapsack. Reverse iteration on capacity.",                 C_PURPLE, True),
    (" YES unlimited","Unbounded Knapsack. Forward iteration on capacity.",      C_PURPLE, True),
    ("Q5","Does the problem define a range or interval [i,j]?",                 C_ACCENT, False),
    (" YES","Interval DP. Fill by increasing length. O(n^3) typical.",           C_ROSE,   True),
    (" NO", "State-machine DP. Add dimension for 'state' (holding, cooldown...).",C_MUTED, True),
]
for label, text, clr, is_branch in flow:
    bg = C_DARK2 if is_branch else C_CARD
    story.append(Table([[
        P(f"<b>{label}</b>",
          S("_", fontName="Courier-Bold", fontSize=9, textColor=clr)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[80, CW-80],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),bg),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 8))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §8  PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(8, "LeetCode Problem Roadmap")
story.append(P("Solve in order — each problem introduces exactly one new DP concept.", sBody))

story.append(P("<b>🟢 Easy — Build the Mental Model</b>", sH2))
easy = [
    [th("#"),  th("Problem"),                          th("Pattern"),         th("Recurrence / Key Insight")],
    [tdc("70", C_GREEN),  td("Climbing Stairs",       C_BODY),
     td("Linear DP",        C_ACCENT),  td("dp[i] = dp[i-1] + dp[i-2]. Same as Fibonacci.",C_MUTED)],
    [tdc("509",C_GREEN),  td("Fibonacci Number",      C_BODY),
     td("Linear DP",        C_ACCENT),  td("dp[n] = dp[n-1] + dp[n-2]. Base: 0, 1.",C_MUTED)],
    [tdc("746",C_GREEN),  td("Min Cost Climbing Stairs",C_BODY),
     td("Linear DP",        C_ACCENT),  td("dp[i] = cost[i] + min(dp[i-1], dp[i-2]).",C_MUTED)],
    [tdc("118",C_GREEN),  td("Pascal's Triangle",     C_BODY),
     td("2D DP",            C_TEAL),    td("row[j] = prev[j-1] + prev[j]. Triangle shape.",C_MUTED)],
    [tdc("338",C_GREEN),  td("Counting Bits",         C_BODY),
     td("Linear DP",        C_ACCENT),  td("dp[i] = dp[i >> 1] + (i & 1).",C_MUTED)],
]
story.append(std_table(easy, [38, 195, 110, 175]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med = [
    [th("#"),   th("Problem"),                              th("Pattern"),              th("Recurrence / Key Insight")],
    [tdc("198", C_YELLOW), td("House Robber",              C_BODY),
     td("Linear DP",          C_ACCENT),
     td("max(dp[i-1], dp[i-2]+nums[i]). Can't rob adjacent.",C_MUTED)],
    [tdc("322", C_YELLOW), td("Coin Change",               C_BODY),
     td("Unbounded Knapsack",  C_PURPLE),
     td("dp[a] = min(dp[a], dp[a-c]+1). Init inf except dp[0]=0.",C_MUTED)],
    [tdc("518", C_YELLOW), td("Coin Change II",            C_BODY),
     td("Unbounded Knapsack",  C_PURPLE),
     td("dp[a] += dp[a-coin]. Count ways.",C_MUTED)],
    [tdc("300", C_YELLOW), td("Longest Increasing Subsequence",C_BODY),
     td("Linear DP O(n^2)",   C_ACCENT),
     td("dp[i]=max dp[j]+1 where j&lt;i and nums[j]&lt;nums[i].",C_MUTED)],
    [tdc("1143",C_YELLOW), td("Longest Common Subsequence",C_BODY),
     td("String DP",           C_TEAL),
     td("dp[i][j]=dp[i-1][j-1]+1 if match else max(dp[i-1][j], dp[i][j-1]).",C_MUTED)],
    [tdc("72",  C_YELLOW), td("Edit Distance",             C_BODY),
     td("String DP",           C_TEAL),
     td("1+min(insert,delete,replace). Base: dp[i][0]=i, dp[0][j]=j.",C_MUTED)],
    [tdc("62",  C_YELLOW), td("Unique Paths",              C_BODY),
     td("Grid DP",             C_ORANGE),
     td("dp[r][c]=dp[r-1][c]+dp[r][c-1]. Base: row 0 and col 0 = 1.",C_MUTED)],
    [tdc("64",  C_YELLOW), td("Minimum Path Sum",          C_BODY),
     td("Grid DP",             C_ORANGE),
     td("grid[r][c]+min(up, left). Fill row by row.",C_MUTED)],
    [tdc("416", C_YELLOW), td("Partition Equal Subset Sum",C_BODY),
     td("0/1 Knapsack bool",   C_ACCENT2),
     td("dp[w] |= dp[w-num]. Reverse loop. Target = sum//2.",C_MUTED)],
    [tdc("139", C_YELLOW), td("Word Break",                C_BODY),
     td("Unbounded Knapsack",  C_PURPLE),
     td("dp[i] = any dp[j] and s[j:i] in word_set.",C_MUTED)],
]
story.append(std_table(med, [38, 195, 120, 165]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard = [
    [th("#"),   th("Problem"),                                 th("Pattern"),                th("Key Insight")],
    [tdc("72",  C_RED),  td("Edit Distance (Hard variant)",  C_BODY),
     td("String DP",           C_TEAL),
     td("Full table with traceback for actual operations sequence.",C_MUTED)],
    [tdc("312", C_RED),  td("Burst Balloons",                C_BODY),
     td("Interval DP",         C_ROSE),
     td("dp[i][j] = last balloon k in (i,j): nums[i]*nums[k]*nums[j]+dp[i][k]+dp[k][j].",C_MUTED)],
    [tdc("188", C_RED),  td("Best Time to Buy/Sell Stock IV",C_BODY),
     td("State-machine DP",    C_INDIGO),
     td("dp[k][i] = max profit with at most k transactions up to day i.",C_MUTED)],
    [tdc("10",  C_RED),  td("Regular Expression Matching",  C_BODY),
     td("String DP",           C_TEAL),
     td("dp[i][j]: s[:i] matches p[:j]. Handle '*' for 0 or more.",C_MUTED)],
    [tdc("1312",C_RED),  td("Minimum Insertions for Palindrome",C_BODY),
     td("Interval DP",         C_ROSE),
     td("n - LPS length. Or direct interval DP on string.",C_MUTED)],
    [tdc("329", C_RED),  td("Longest Increasing Path in Matrix",C_BODY),
     td("Memoised DFS on DAG", C_AMBER),
     td("DFS + memo on each cell. Implicit topological order by sorting.",C_MUTED)],
]
story.append(std_table(hard, [38, 200, 130, 150]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §9  EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(9, "Edge Case Checklist")

story.append(P(
    "DP problems fail silently — wrong initialisations produce wrong answers "
    "with no error. These are the most common correctness traps.",
    sBody))

story.append(P("<b>Edge Case 1: Initialisation — 0 vs Infinity vs -1</b>", sH2))
init_data = [
    [th("DP Goal"),              th("Initial value"),          th("Reasoning")],
    [td("Minimum cost / steps",C_BODY), tdc("float('inf')",C_RED),
     td("Any real answer beats infinity. Ensures min() starts from scratch.",C_MUTED)],
    [td("Maximum value / profit",C_BODY),tdc("float('-inf') or 0",C_BODY),
     td("Use -inf if negative answers are possible; 0 if answers are non-negative.",C_MUTED)],
    [td("Count number of ways",C_BODY), tdc("0",C_GREEN),
     td("Zero ways by default; base case(s) set dp[0]=1 (one way to do nothing).",C_MUTED)],
    [td("Boolean reachability",C_BODY), tdc("False",C_BODY),
     td("dp[i] = True when state i is reachable.",C_MUTED)],
    [td("Unseen / uncomputed",C_BODY),  tdc("-1",C_YELLOW),
     td("Sentinel for memoisation — distinct from a valid answer of 0.",C_MUTED)],
]
story.append(std_table(init_data, [145, 115, 258]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Wrong initialisation example ─────────────────────────────",
    "## Coin Change: find minimum coins for amount A",
    "",
    "## WRONG: init with 0",
    "dp = [0] * (amount + 1)  ## dp[a] = 0 means '0 coins', not 'unreachable'",
    "## This will incorrectly return 0 for any amount",
    "",
    "## CORRECT: init with infinity, set dp[0] = 0",
    "dp = [float('inf')] * (amount + 1)",
    "dp[0] = 0   ## 0 coins needed for amount 0",
    "## Now dp[a] = inf means 'impossible' and min() works correctly",
])

story.append(P("<b>Edge Case 2: Off-by-One Errors and Array Sizes</b>", sH2))
story += code_block([
    "## Problem: dp needs to represent n+1 states (0 through n)",
    "",
    "## WRONG: dp = [0] * n   -> indices 0..n-1, dp[n] causes IndexError",
    "## CORRECT: dp = [0] * (n + 1)  -> indices 0..n",
    "",
    "## String DP: dp[i][j] represents first i chars of s, first j chars of t",
    "## Table size must be (len(s)+1) x (len(t)+1) to include the empty string",
    "dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]",
    "## dp[0][j] = 0: empty s vs any t (0 common chars)",
    "## dp[i][0] = 0: any s vs empty t",
    "",
    "## 0/1 Knapsack: w in range(W+1) not range(W)",
    "dp = [0] * (W + 1)  ## capacities 0, 1, 2, ..., W — needs W+1 slots",
    "",
    "## Climbing stairs: n steps — dp[n] is the answer",
    "dp = [0] * (n + 1)  ## dp[0]=1, dp[1]=1, ..., dp[n]=answer",
])

story.append(P("<b>Edge Case 3: Empty Strings and Zero-Capacity Constraints</b>", sH2))
story += code_block([
    "## Empty string / array guards",
    "def solve(s):",
    "    if not s: return 0   ## empty input: trivial answer",
    "    ## ...",
    "",
    "## LCS: one or both strings empty",
    "## dp[0][j] = dp[i][0] = 0 — handled by initialisation, no special guard needed",
    "",
    "## Knapsack with W=0: dp[0] is already the base case; returns 0 items taken",
    "",
    "## Word Break with empty string: dp[0] = True (empty string is breakable)",
    "dp[0] = True   ## must set this before the main loop",
    "",
    "## Palindrome: single character is always a palindrome",
    "for i in range(n): dp[i][i] = True   ## base case: length 1",
    "",
    "## ─── Memoisation: check for -1 sentinel vs falsy 0 ───────────────",
    "## WRONG: if memo[n] is False — misidentifies 0 as uncached",
    "## CORRECT: if memo[n] != -1  — explicitly checks uninitialised sentinel",
    "memo = [-1] * (n + 1)",
    "def dp(i):",
    "    if memo[i] != -1: return memo[i]   ## -1 means 'not yet computed'",
    "    ## ...",
    "    memo[i] = result                   ## even if result is 0, store it",
    "    return memo[i]",
])

story += callout(
    "The most common DP bug: using 0 as both 'not yet computed' and "
    "'valid answer = 0'. Fix: use -1 as the uncomputed sentinel in memoisation "
    "arrays. Only use None if your cache is a dict (missing key = not computed).",
    C_RED, icon="⚠️")

# ── MASTER CHEAT SHEET ─────────────────────────────────────────────────────────
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")

cheat = [
    [th("Pattern"),                 th("State"),           th("Recurrence"),                   th("Space"),      th("Classic Problem")],
    [td("Fibonacci / Stairs",C_ACCENT), tdc("dp[i]"),      tdc("dp[i-1] + dp[i-2]"),           tdc("O(1)*"),     td("LC 70, 509",C_MUTED)],
    [td("House Robber",C_ACCENT),   tdc("dp[i]"),          tdc("max(dp[i-1], dp[i-2]+v)"),      tdc("O(1)*"),     td("LC 198, 213",C_MUTED)],
    [td("Max Subarray",C_ACCENT),   tdc("dp[i]"),          tdc("max(nums[i], dp[i-1]+nums[i])"),tdc("O(1)*"),     td("LC 53",C_MUTED)],
    [td("0/1 Knapsack",C_GREEN),    tdc("dp[i][w]"),       tdc("max(skip, take)"),              tdc("O(W)*"),     td("LC 416, 494",C_MUTED)],
    [td("Unbounded Knapsack",C_GREEN),tdc("dp[w]"),        tdc("min/count over items"),         tdc("O(W)"),      td("LC 322, 518",C_MUTED)],
    [td("LCS",C_TEAL),              tdc("dp[i][j]"),       tdc("match+1 or max(up,left)"),      tdc("O(min(m,n))*"),td("LC 1143",C_MUTED)],
    [td("Edit Distance",C_TEAL),    tdc("dp[i][j]"),       tdc("1+min(ins,del,rep)"),           tdc("O(min(m,n))*"),td("LC 72",C_MUTED)],
    [td("Grid DP",C_ORANGE),        tdc("dp[r][c]"),       tdc("f(dp[r-1][c], dp[r][c-1])"),   tdc("O(n)*"),     td("LC 62, 64",C_MUTED)],
    [td("Interval DP",C_ROSE),      tdc("dp[i][j]"),       tdc("f(dp[i][k], dp[k+1][j])"),     tdc("O(n^2)"),    td("LC 516, 312",C_MUTED)],
    [td("State Machine",C_INDIGO),  tdc("dp[i][state]"),   tdc("max(hold,sold,rest)"),          tdc("O(states)"), td("LC 188, 309",C_MUTED)],
]
story.append(std_table(cheat, [125, 75, 155, 72, 91]))
story.append(P("* After space optimisation with rolling variables / 1D array.", sCaption))
story.append(Spacer(1, 10))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
checks = [
    ("Clearly defined state?",    "Write dp[i] = '...' in English before writing any code."),
    ("Recurrence derived?",       "Express dp[i] as a function of strictly smaller dp[j] (j < i)."),
    ("Base cases set?",           "What is dp[0]? dp[1]? What if input is empty?"),
    ("Array size correct?",       "Usually n+1 slots for problems with indices 0..n."),
    ("Init value right?",         "Min problem: inf. Max problem: -inf or 0. Count: 0. Memo: -1."),
    ("Fill order correct?",       "Always fill smaller subproblems before larger ones."),
    ("0/1 vs Unbounded?",         "0/1: reverse capacity loop. Unbounded: forward capacity loop."),
    ("Space optimisable?",        "If dp[i] only needs dp[i-1] and dp[i-2], use two variables."),
    ("Reconstruction needed?",    "If actual path/sequence required, keep full table for traceback."),
    ("Disconnected case handled?","Empty input or n=0 returns correct default immediately."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ]  {q}</font></b>",
          S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[185, CW-185],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_CARD),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

story.append(Table([[P(
    "<b>You now have the complete Dynamic Programming mental model.</b><br/><br/>"
    "Every DP problem reduces to the same three questions: "
    "<i>What is the state? What is the recurrence? What are the base cases?</i><br/><br/>"
    "Choose memoisation when the problem's structure is easier to express "
    "recursively, or when only a fraction of states are reachable. "
    "Choose tabulation when recursion depth is a concern, "
    "or when space optimisation to O(1) or O(n) is required.<br/><br/>"
    "Recommended path: LC 70 -> LC 198 -> LC 322 -> LC 300 -> "
    "LC 1143 -> LC 72 -> LC 62 -> LC 416 -> LC 312. "
    "These nine problems cover every major pattern: "
    "linear 1D, house robber, unbounded knapsack, LIS, LCS, "
    "edit distance, grid DP, 0/1 knapsack, and interval DP.",
    S("_", fontName="Helvetica", fontSize=10, leading=16, textColor=C_BODY)
)]], colWidths=[CW],
    style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("BOX",(0,0),(-1,-1),2,C_ACCENT),
        ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
        ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20)])))

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")