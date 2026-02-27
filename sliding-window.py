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

# ── Color Palette ──────────────────────────────────────────────────────────────
C_BG       = colors.HexColor("#0F172A")
C_ACCENT   = colors.HexColor("#38BDF8")
C_ACCENT2  = colors.HexColor("#818CF8")
C_GREEN    = colors.HexColor("#34D399")
C_YELLOW   = colors.HexColor("#FBBF24")
C_RED      = colors.HexColor("#F87171")
C_PURPLE   = colors.HexColor("#C084FC")
C_CODE_BG  = colors.HexColor("#1E293B")
C_CODE_FG  = colors.HexColor("#E2E8F0")
C_HEADING  = colors.HexColor("#F1F5F9")
C_BODY     = colors.HexColor("#CBD5E1")
C_MUTED    = colors.HexColor("#64748B")
C_BORDER   = colors.HexColor("#334155")
C_CARD     = colors.HexColor("#1E293B")
C_ORANGE   = colors.HexColor("#FB923C")
C_TEAL     = colors.HexColor("#2DD4BF")
C_DARK2    = colors.HexColor("#141E2E")

PAGE_W, PAGE_H = letter

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Sliding_Window_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)

# ── Style Factory ──────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("sTitle",   fontName="Helvetica-Bold",    fontSize=32, leading=40, textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)
sSubtitle= S("sSub",     fontName="Helvetica",          fontSize=13, leading=18, textColor=C_ACCENT,  alignment=TA_CENTER, spaceAfter=4)
sAuthor  = S("sAuth",    fontName="Helvetica-Oblique",  fontSize=10, textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=20)
sH2      = S("sH2",      fontName="Helvetica-Bold",    fontSize=14, leading=19, textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)
sH3      = S("sH3",      fontName="Helvetica-Bold",    fontSize=11, leading=15, textColor=C_GREEN,   spaceBefore=8,  spaceAfter=4)
sBody    = S("sBody",    fontName="Helvetica",          fontSize=10, leading=15, textColor=C_BODY,    spaceAfter=6, alignment=TA_JUSTIFY)
sCode    = S("sCode",    fontName="Courier",            fontSize=8.5,leading=13, textColor=C_CODE_FG, spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sCodeCmt = S("sCodeCmt", fontName="Courier-Oblique",   fontSize=8.5,leading=13, textColor=C_MUTED,   spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sFormula = S("sFormula", fontName="Courier-Bold",      fontSize=10, leading=14, textColor=C_GREEN,   alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
sCaption = S("sCaption", fontName="Helvetica-Oblique", fontSize=8.5, textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=6)
sTOC     = S("sTOC",     fontName="Helvetica",          fontSize=10, leading=16, textColor=C_BODY)
sTOCSub  = S("sTOCSub",  fontName="Helvetica",          fontSize=9,  leading=14, textColor=C_MUTED, leftIndent=18)

P = Paragraph   # shorthand

# ── Helpers ────────────────────────────────────────────────────────────────────
CW = PAGE_W - 1.3*inch   # usable content width

def code_block(lines, lang="python"):
    hdr = Table([[P(f"<b>{lang}</b>", S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
        colWidths=[CW],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0D1929")),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),14),
        ]))
    rows = [[P(ln if ln else " ", sCodeCmt if ln.startswith("##") else sCode)] for ln in lines]
    body = Table(rows, colWidths=[CW],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_CODE_BG),
            ("TOPPADDING",(0,0),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-1),1),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8),
        ]))
    wrap = Table([[hdr],[body]], colWidths=[CW],
        style=TableStyle([
            ("BOX",(0,0),(-1,-1),1,C_BORDER),("ROUNDEDCORNERS",[4]),
            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ]))
    return [wrap, Spacer(1,8)]

def callout(text, color=C_ACCENT, icon="💡"):
    tbl = Table([[P(f"{icon}  {text}", S("_", fontName="Helvetica", fontSize=9.5, leading=14, textColor=color))]],
        colWidths=[CW],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0C1F35")),
            ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
            ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
            ("LINEBEFORE",(0,0),(0,-1),3,color),
        ]))
    return [tbl, Spacer(1,6)]

def section_divider(num, title):
    lbl = f"{num:02d}" if num > 0 else "  "
    return [
        Spacer(1,10),
        Table([[
            P(f"<b>{lbl}</b>", S("_", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT)),
            P(f"<b>{title}</b>", S("_", fontName="Helvetica-Bold", fontSize=18, textColor=C_HEADING, leading=24)),
        ]], colWidths=[40, CW-40],
        style=TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(0,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
            ("LINEBELOW",(0,0),(-1,-1),2,C_ACCENT),
            ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ])),
        Spacer(1,8),
    ]

def std_table(data, col_widths, row_colors=None):
    """Render a styled data table."""
    rc = row_colors or [C_CARD, C_DARK2]
    return Table(data, colWidths=col_widths,
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,0),C_BG),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),rc),
            ("BOX",(0,0),(-1,-1),1,C_BORDER),
            ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),7),
            ("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1),8),
        ]))

def th(text, color=C_MUTED):
    return P(f"<b>{text}</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=color))

def td(text, color=C_BODY, font="Helvetica", size=9):
    return P(text, S("_", fontName=font, fontSize=size, textColor=color))

def tdc(text, color=C_BODY):
    return P(text, S("_", fontName="Courier", fontSize=9, textColor=color))

# ── Window visualiser ──────────────────────────────────────────────────────────
def window_vis(cells, left, right, highlight_color=C_ACCENT, labels=("left","right"), extra=None):
    """Render array with highlighted window [left..right]."""
    n = len(cells)
    col_w = min(50, int(CW / n))
    ptr_row, val_row, idx_row = [], [], []
    for i, v in enumerate(cells):
        in_win = left <= i <= right
        is_left  = i == left
        is_right = i == right
        is_extra = extra is not None and i == extra

        pts = []
        if is_left:  pts.append(labels[0])
        if is_right and not (is_left and left == right): pts.append(labels[1])
        if is_extra: pts.append("mid")
        ptr_label = "/".join(pts)
        ptr_color = C_ACCENT if is_left else (C_ACCENT2 if is_right else C_GREEN)

        bg = highlight_color if in_win else C_CARD
        if is_left:  bg = colors.HexColor("#0A2E3A")
        if is_right: bg = colors.HexColor("#0A1A3A")
        if in_win and not is_left and not is_right: bg = colors.HexColor("#0A1E2E")

        fg = C_HEADING if in_win else C_MUTED
        ptr_row.append(P(f"<b>{ptr_label}</b>", S("_", fontName="Helvetica-Bold", fontSize=7.5, textColor=ptr_color, alignment=TA_CENTER)))
        val_row.append(P(f"<b>{v}</b>",          S("_", fontName="Courier-Bold",   fontSize=11, textColor=fg, alignment=TA_CENTER)))
        idx_row.append(P(str(i),                  S("_", fontName="Courier",         fontSize=8,  textColor=C_MUTED, alignment=TA_CENTER)))

    tbl = Table([ptr_row, val_row, idx_row], colWidths=[col_w]*n,
        style=TableStyle([
            ("BOX",(0,1),(-1,1),1,C_BORDER),("INNERGRID",(0,1),(-1,1),0.5,C_BORDER),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
            ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2),
            ("TOPPADDING",(0,2),(-1,2),2),("BOTTOMPADDING",(0,2),(-1,2),2),
        ]))
    for i in range(left, right+1):
        bg_c = colors.HexColor("#0A1E2E") if (i != left and i != right) else (colors.HexColor("#0A2E3A") if i == left else colors.HexColor("#0A1A3A"))
        tbl._argH[1] if False else None  # no-op placeholder
    return [tbl, Spacer(1,5)]

# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),("ROWHEIGHT",(0,0),(-1,-1),6)])))
story.append(Spacer(1, 0.3*inch))
story.append(P("SLIDING WINDOW", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Window State · Expansion &amp; Contraction · Monotonic Deque", sAuthor))
story.append(Spacer(1, 0.2*inch))

story.append(Table([[P("<b>What You Will Master</b>", S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· The 'Reuse Results' intuition — why recalculating destroys performance\n"
       "· Fixed-Size Window: the clean for-loop k-length approach\n"
       "· Variable-Size Window: expand-until-invalid, contract-until-valid\n"
       "· Window State management: sum, hashmap, frequency counters\n"
       "· Sliding Window Maximum with Monotonic Deque in O(1) per step\n"
       "· Shrinkable vs. Non-Shrinkable window optimization\n"
       "· Sliding Window vs. Two Pointers vs. Prefix Sum decision framework\n"
       "· Universal Template + 20+ categorized LeetCode problems",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CARD),("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.3*inch))

cx_data = [
    [th("Brute Force"), th("Fixed Window"), th("Variable Window")],
    [td("O(n<super>2</super>) per window", C_RED),
     td("O(n) one pass", C_GREEN),
     td("O(n) amortized", C_GREEN)],
    [td("Recomputes entire range", C_MUTED),
     td("Add right, remove left", C_BODY),
     td("Expand right, shrink left", C_BODY)],
]
story.append(Table(cx_data, colWidths=[CW/3]*3,
    style=TableStyle([
        ("BACKGROUND",(0,0),(-1,0),C_BG),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#0A1628")),
        ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
    ])))
story.append(Spacer(1, 0.35*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Intuition",["Why Recalculating is Wasteful","The Reuse Results Principle","Defining Window State"]),
    ("02","Pattern 1: Fixed-Size Window",["The for-loop Approach","Adding / Removing One Element","Visual Trace"]),
    ("03","Pattern 2: Variable-Size Window",["Expand Until Invalid","Contract Until Valid","The Inner while Loop"]),
    ("04","Window State Management",["Sum as State","HashMap / Counter as State","The Invalid State Trigger"]),
    ("05","Mathematical Prerequisites",["Monotonicity Requirement","When Negative Numbers Break It","Non-Shrinkable Optimisation"]),
    ("06","Comparison & Decision Making",["Sliding Window vs Two Pointers","Sliding Window vs Prefix Sum","Decision Flowchart"]),
    ("07","Advanced: Sliding Window Maximum",["Brute Force O(nk)","Monotonic Deque O(n)","Implementation Deep Dive"]),
    ("08","Universal Template & Mental Models",["Variable Window Template","Fixed Window Template","Checklist Before Coding"]),
    ("09","Problem Roadmap",["Fixed Problems","Variable Problems","Hard Problems"]),
    ("10","Edge Cases & Pitfalls",["k > n, k=0, empty input","Off-by-One in Shrink Loop","Forgetting to Remove State"]),
]
for num, title, subs in toc:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1,3))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 1 — INTUITION
# ════════════════════════════════════════════════════════
story += section_divider(1, "The Intuition")

story.append(P("<b>The Waste in Brute Force</b>", sH2))
story.append(P(
    "Consider finding the maximum sum of any contiguous subarray of length k. "
    "The naive approach iterates over every starting position and re-sums k elements "
    "from scratch — O(n·k). For n=100,000 and k=50,000 that is 5 billion operations. "
    "Yet when the window slides one step, <b>only one element leaves and one enters</b>. "
    "All the other k−2 elements are shared between the old and new window. "
    "Recomputing their sum is pure waste.",
    sBody))

story += code_block([
    "## ─── Brute Force: O(n·k) ───────────────────────────────────────",
    "def max_sum_brute(arr, k):",
    "    max_s = float('-inf')",
    "    for i in range(len(arr) - k + 1):      ## O(n) starting positions",
    "        window_sum = sum(arr[i : i+k])      ## O(k) re-sum every time ← waste!",
    "        max_s = max(max_s, window_sum)",
    "    return max_s",
    "",
    "## ─── Sliding Window: O(n) ───────────────────────────────────────",
    "def max_sum_sliding(arr, k):",
    "    window_sum = sum(arr[:k])               ## O(k) — build initial window once",
    "    max_s      = window_sum",
    "    for i in range(k, len(arr)):            ## O(n-k) slides",
    "        window_sum += arr[i]      ## add incoming element (right edge)",
    "        window_sum -= arr[i - k]  ## remove outgoing element (left edge)",
    "        max_s = max(max_s, window_sum)",
    "    return max_s",
])

story += callout(
    "The Reuse Results Principle: Instead of recomputing the entire window "
    "from scratch on each slide, we maintain a running 'window state' and apply "
    "an incremental update — one addition, one subtraction. This collapses O(k) "
    "work per step into O(1), yielding a net complexity of O(n).",
    C_ACCENT, icon="💡")

story.append(P("<b>Defining Window State</b>", sH2))
story.append(P(
    "The <b>Window State</b> is the single data structure that summarises "
    "everything you need to know about the current window contents — without "
    "re-examining all elements inside it. Choosing the right state representation "
    "is the central design decision for every sliding window problem.",
    sBody))

state_data = [
    [th("State Type"), th("Data Structure"), th("Update Cost"), th("Used For")],
    [td("Running Sum",  C_ACCENT), tdc("window_sum: int"),
     tdc("O(1): += right, -= left"), td("Max/min sum, average, fixed-k problems", C_BODY)],
    [td("Frequency Map",C_ACCENT2),tdc("counter: dict"),
     tdc("O(1): counter[c] +/- 1"),  td("Distinct chars, anagram detection, repeating elements", C_BODY)],
    [td("Distinct Count",C_GREEN), tdc("unique: int"),
     tdc("O(1): incr/decr when cnt→1"), td("At-most-k distinct, longest without repeating", C_BODY)],
    [td("Max / Min",    C_YELLOW), tdc("deque (monotonic)"),
     tdc("O(1) amortised"),          td("Sliding window maximum/minimum (LC 239)", C_BODY)],
    [td("Boolean Valid",C_ORANGE), tdc("satisfied: bool/int"),
     tdc("O(1): recheck on change"),  td("Contains all required chars (min window substring)", C_BODY)],
]
story.append(std_table(state_data, [85,130,130,135]))
story.append(Spacer(1,8))

story += callout(
    "The window state is your contract: it must be cheaply updatable when one "
    "element enters (right++) and one leaves (left++). If an update costs O(k), "
    "you haven't escaped O(n·k) — you've just hidden it.",
    C_YELLOW, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2 — FIXED SIZE WINDOW
# ════════════════════════════════════════════════════════
story += section_divider(2, "Pattern 1: Fixed-Size Window")

story.append(P("<b>The k-Length Window</b>", sH2))
story.append(P(
    "When the problem specifies an <b>exact window size k</b>, the algorithm is "
    "beautifully clean: build the first window of size k, then slide it one position "
    "at a time to the right — adding the new right element and removing the "
    "departing left element. No inner loop, no shrinking. Pure O(n).",
    sBody))

story.append(P("<b>Fixed Window Template</b>", sH2))
story += code_block([
    "## ─── Fixed-Size Sliding Window Template ────────────────────────",
    "def fixed_window(arr, k):",
    "    if len(arr) < k or k == 0:    ## guard: window larger than array or k=0",
    "        return []                 ## or return appropriate sentinel",
    "",
    "    ## ── Phase 1: Build initial window (indices 0 .. k-1) ────────",
    "    window_state = initialise_state(arr[:k])",
    "    best = evaluate(window_state)",
    "",
    "    ## ── Phase 2: Slide the window ────────────────────────────────",
    "    for right in range(k, len(arr)):",
    "        left = right - k          ## left edge of current window",
    "",
    "        ## Step A — add the incoming element at the RIGHT edge",
    "        add_to_state(window_state, arr[right])",
    "",
    "        ## Step B — remove the outgoing element at the LEFT edge",
    "        remove_from_state(window_state, arr[left])",
    "",
    "        ## Step C — evaluate and update answer",
    "        best = update_best(best, window_state)",
    "",
    "    return best",
])

story.append(P("<b>Visual Trace: Maximum Sum of k=3 Window</b>", sH2))
story.append(P("Array: [2, 1, 5, 1, 3, 2], k=3. Watch the window slide and state update:", sBody))

slides = [
    ([2,1,5,1,3,2], 0, 2, "Initial window: sum=2+1+5=8 → best=8"),
    ([2,1,5,1,3,2], 1, 3, "Slide: +arr[3]=1, -arr[0]=2 → sum=7 → best=8"),
    ([2,1,5,1,3,2], 2, 4, "Slide: +arr[4]=3, -arr[1]=1 → sum=9 → best=9"),
    ([2,1,5,1,3,2], 3, 5, "Slide: +arr[5]=2, -arr[2]=5 → sum=6 → best=9"),
]
for arr_s, l, r, desc in slides:
    n = len(arr_s)
    col_w = 50
    ptr_row, val_row, idx_row = [], [], []
    for i, v in enumerate(arr_s):
        in_w = l <= i <= r
        is_l = i == l; is_r = i == r
        pts = (["left"] if is_l else []) + (["right"] if is_r else [])
        lbl = "/".join(pts)
        pc  = C_ACCENT if is_l else (C_ACCENT2 if is_r else C_MUTED)
        bg  = colors.HexColor("#0A2E3A") if is_l else (colors.HexColor("#0A1A3A") if is_r else (colors.HexColor("#0A1E2E") if in_w else C_CARD))
        fg  = C_HEADING if in_w else C_MUTED
        ptr_row.append(P(f"<b>{lbl}</b>",  S("_", fontName="Helvetica-Bold", fontSize=7.5, textColor=pc, alignment=TA_CENTER)))
        val_row.append(P(f"<b>{v}</b>",    S("_", fontName="Courier-Bold",   fontSize=11, textColor=fg, alignment=TA_CENTER)))
        idx_row.append(P(str(i),           S("_", fontName="Courier",         fontSize=8, textColor=C_MUTED, alignment=TA_CENTER)))
    vis = Table([ptr_row, val_row, idx_row], colWidths=[col_w]*n,
        style=TableStyle([
            ("BOX",(0,1),(-1,1),1,C_BORDER),("INNERGRID",(0,1),(-1,1),0.5,C_BORDER),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
            ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2),
            ("TOPPADDING",(0,2),(-1,2),2),("BOTTOMPADDING",(0,2),(-1,2),2),
        ]))
    story.append(vis)
    story.append(P(f"<b>{desc}</b>", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW, spaceAfter=7)))

story.append(P("Answer: maximum sum subarray of length 3 is <b>9</b> (elements [5,1,3])", sCaption))

story.append(P("<b>The Invariant: Window Always Has Exactly k Elements</b>", sH3))
story.append(P(
    "The loop condition <b>for right in range(k, len(arr))</b> and the derived "
    "<b>left = right - k</b> guarantee that the window always contains exactly k "
    "elements: arr[left], arr[left+1], ..., arr[right]. This is the fixed-window "
    "invariant, and it eliminates the need for any shrink logic.",
    sBody))

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3 — VARIABLE SIZE WINDOW
# ════════════════════════════════════════════════════════
story += section_divider(3, "Pattern 2: Variable-Size Window")

story.append(P("<b>Expand Until Invalid — Contract Until Valid</b>", sH2))
story.append(P(
    "Variable-size windows have no fixed length. Instead, the window has a "
    "<b>validity condition</b>. The right pointer always moves forward (expansion). "
    "When expansion makes the window invalid, the left pointer moves forward "
    "(contraction) until the window is valid again. "
    "This two-phase rhythm is the heartbeat of every variable-window algorithm.",
    sBody))

# The two-phase rhythm diagram
phases = [
    ("EXPAND", C_GREEN, "right += 1", "Add arr[right] to window state", "Window grows until invalid"),
    ("CONTRACT", C_RED, "left += 1",  "Remove arr[left] from state",    "Shrink until valid again"),
    ("EVALUATE", C_YELLOW, "record",  "Capture current window as answer","After each step (varies by problem)"),
]
phase_data = [[th("Phase"), th("Pointer"), th("Action"), th("Effect"), th("Trigger")]]
for name, color, ptr, act, trig in phases:
    phase_data.append([
        td(f"<b>{name}</b>", color),
        tdc(ptr, color),
        td(act, C_BODY),
        td(trig, C_MUTED, size=8.5),
        td(trig, C_MUTED, size=8.5),
    ])
# fix: remove duplicate column
phase_data = [[th("Phase"), th("Pointer"), th("State Change"), th("Trigger")]]
for name, color, ptr, act, trig in phases:
    phase_data.append([td(f"<b>{name}</b>", color), tdc(ptr, color), td(act, C_BODY), td(trig, C_MUTED, size=8.5)])
story.append(std_table(phase_data, [80, 90, 175, 135]))
story.append(Spacer(1, 8))

story.append(P("<b>Universal Variable-Size Template</b>", sH2))
story += code_block([
    "## ─── Variable-Size Sliding Window — Universal Template ─────────",
    "def variable_window(arr_or_str):",
    "    left  = 0",
    "    state = initialise()         ## sum=0, counter={}, distinct=0, etc.",
    "    best  = 0                    ## or float('-inf') depending on problem",
    "",
    "    for right in range(len(arr_or_str)):    ## right pointer ALWAYS advances",
    "",
    "        ## ── Step 1: EXPAND — incorporate new element ─────────────",
    "        add_to_state(state, arr_or_str[right])",
    "",
    "        ## ── Step 2: CONTRACT — restore validity ──────────────────",
    "        while is_invalid(state):            ## condition specific to problem",
    "            remove_from_state(state, arr_or_str[left])",
    "            left += 1",
    "",
    "        ## ── Step 3: EVALUATE — window is now valid ───────────────",
    "        ## For LONGEST problems: record window size = right - left + 1",
    "        ## For SHORTEST problems: record inside the while loop (see below)",
    "        best = update_best(best, right, left, state)",
    "",
    "    return best",
    "",
    "## ─── Variation for MINIMUM window problems ──────────────────────",
    "## Move evaluate INSIDE the while loop:",
    "##     while is_valid(state):              ## shrink as long as valid",
    "##         best = min(best, right-left+1)  ## capture before shrinking",
    "##         remove(state, arr[left])",
    "##         left += 1",
])

story += callout(
    "Key distinction: For LONGEST window problems, evaluate AFTER the while loop "
    "(window is maximally valid). For SHORTEST/MINIMUM window problems, evaluate "
    "INSIDE the contraction loop (capture every valid configuration before it becomes invalid).",
    C_PURPLE, icon="🔑")

story.append(P("<b>Concrete Example: Longest Substring Without Repeating Characters</b>", sH2))
story.append(P(
    "State = a frequency counter. Invalid = any character has count > 1. "
    "Evaluate = window size after each contraction.",
    sBody))
story += code_block([
    "## ─── Longest Substring Without Repeating Characters ────────────",
    "def length_of_longest_substring(s):",
    "    freq  = {}",
    "    left  = 0",
    "    best  = 0",
    "",
    "    for right in range(len(s)):",
    "        c = s[right]",
    "        freq[c] = freq.get(c, 0) + 1          ## EXPAND: add right char",
    "",
    "        while freq[c] > 1:                     ## INVALID: duplicate found",
    "            freq[s[left]] -= 1                 ## CONTRACT: remove left char",
    "            if freq[s[left]] == 0:",
    "                del freq[s[left]]",
    "            left += 1",
    "",
    "        best = max(best, right - left + 1)     ## EVALUATE: valid window",
    "",
    "    return best",
])

story.append(P("<b>Step-by-Step Trace: s = 'a b c a b c b b'</b>", sH3))
story.append(P("Watch the state (freq map) update as the window expands and contracts:", sBody))

trace_str = list("abcabcbb")
trace_steps = [
    (0,0,{"a":1}, "Expand: add 'a'. No dup. best=1"),
    (0,1,{"a":1,"b":1}, "Expand: add 'b'. No dup. best=2"),
    (0,2,{"a":1,"b":1,"c":1}, "Expand: add 'c'. No dup. best=3"),
    (0,3,{"a":2,"b":1,"c":1}, "Expand: add 'a'. a=2 → INVALID"),
    (1,3,{"a":1,"b":1,"c":1}, "Contract: remove 'a'. a=1 → valid. best=3"),
    (1,4,{"a":1,"b":2,"c":1}, "Expand: add 'b'. b=2 → INVALID"),
    (2,4,{"a":1,"b":1,"c":1}, "Contract: remove 'b'. b=1 → valid. best=3"),
    (2,5,{"a":1,"b":1,"c":2}, "Expand: add 'c'. c=2 → INVALID"),
    (3,5,{"a":0,"b":1,"c":2}, "Contract: remove 'a'..."),
    (3,6,{"a":0,"b":2,"c":1}, "...and so on. Final best=3"),
]
trace_data = [[th("L"), th("R"), th("char[R]"), th("Window"), th("State"), th("Action")]]
for l, r, state, action in trace_steps[:7]:
    win = "".join(trace_str[l:r+1])
    sc = ", ".join(f"{k}:{v}" for k,v in state.items())
    trace_data.append([
        tdc(str(l), C_ACCENT), tdc(str(r), C_ACCENT2),
        tdc(f"'{trace_str[r]}'", C_GREEN),
        tdc(f'"{win}"', C_BODY),
        tdc(sc, C_MUTED),
        td(action, C_YELLOW, size=8.5),
    ])
story.append(std_table(trace_data, [30,30,50,80,130,160]))
story.append(P("Final answer: 3 (window 'abc')", sCaption))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4 — STATE MANAGEMENT
# ════════════════════════════════════════════════════════
story += section_divider(4, "Window State Management")

story.append(P("<b>The HashMap / Counter State</b>", sH2))
story.append(P(
    "For problems involving characters, strings, or element frequencies, "
    "a <b>HashMap (Counter)</b> is the go-to window state. It answers "
    "\"how many times does element X appear in the current window?\" in O(1). "
    "The critical discipline: you must <b>always</b> update the map both when "
    "adding (right++) and removing (left++) elements.",
    sBody))

story += code_block([
    "## ─── HashMap State Pattern ──────────────────────────────────────",
    "from collections import defaultdict",
    "",
    "def hashmap_window(s, condition):",
    "    freq  = defaultdict(int)",
    "    left  = 0",
    "    best  = 0",
    "",
    "    for right in range(len(s)):",
    "",
    "        ## ADD incoming element",
    "        freq[s[right]] += 1",
    "",
    "        ## CONTRACT while invalid",
    "        while not is_valid(freq, condition):",
    "            freq[s[left]] -= 1",
    "            if freq[s[left]] == 0:",
    "                del freq[s[left]]   ## optional: keep map clean",
    "            left += 1",
    "",
    "        ## EVALUATE",
    "        best = max(best, right - left + 1)",
    "",
    "    return best",
])

story.append(P("<b>Derived Count: The 'distinct' Shortcut</b>", sH3))
story.append(P(
    "Instead of checking the entire map on every step (expensive), maintain a "
    "<b>separate integer</b> that tracks the property you care about. "
    "Update it only when an element's count crosses the threshold (0↔1). "
    "This keeps the invalidity check O(1).",
    sBody))
story += code_block([
    "## ─── Distinct-Count Optimisation ───────────────────────────────",
    "def at_most_k_distinct(s, k):",
    "    freq     = defaultdict(int)",
    "    distinct = 0             ## ← tracks unique element count in window",
    "    left     = 0",
    "    best     = 0",
    "",
    "    for right in range(len(s)):",
    "        freq[s[right]] += 1",
    "        if freq[s[right]] == 1:      ## first occurrence: new distinct element",
    "            distinct += 1",
    "",
    "        while distinct > k:          ## INVALID: too many distinct chars",
    "            freq[s[left]] -= 1",
    "            if freq[s[left]] == 0:   ## last occurrence: losing a distinct elem",
    "                distinct -= 1",
    "            left += 1",
    "",
    "        best = max(best, right - left + 1)",
    "",
    "    return best",
])

story.append(P("<b>The Invalid State Trigger</b>", sH2))
story.append(P(
    "The <b>Invalid State</b> is the precise condition that forces contraction. "
    "Identifying it correctly is the hardest part of variable-window problems. "
    "Here are the most common triggers:",
    sBody))

inv_data = [
    [th("Problem Type"), th("Invalid Condition"), th("State Checked")],
    [td("Longest without repeating",   C_BODY), tdc("freq[c] > 1",        C_RED),    td("Character frequency map",          C_MUTED)],
    [td("At most k distinct chars",    C_BODY), tdc("distinct > k",       C_RED),    td("Distinct element counter",         C_MUTED)],
    [td("Sum at most target (pos.)",   C_BODY), tdc("window_sum > target",C_RED),    td("Running integer sum",              C_MUTED)],
    [td("Anagram / permutation check", C_BODY), tdc("window != pattern",  C_RED),    td("Frequency map match",              C_MUTED)],
    [td("Min window substring",        C_BODY), tdc("not all t chars covered",C_RED),td("'satisfied' counter (int)",        C_MUTED)],
    [td("No zeros in window",          C_BODY), tdc("zero_count > 0",     C_RED),    td("Zero counter",                     C_MUTED)],
]
story.append(std_table(inv_data, [160, 130, 190]))
story.append(Spacer(1, 8))

story += callout(
    "Naming the invalid condition BEFORE writing code is the single most powerful "
    "habit for sliding window problems. Write it as a comment at the top: "
    "'# INVALID when: freq[char] > 1'. This becomes your while-loop condition.",
    C_GREEN, icon="✅")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5 — MATHEMATICAL PREREQUISITES
# ════════════════════════════════════════════════════════
story += section_divider(5, "Mathematical Prerequisites")

story.append(P("<b>The Monotonicity Requirement</b>", sH2))
story.append(P(
    "Variable-size sliding windows rely on <b>monotonicity</b>: expanding the "
    "window (adding one more element) should make the window state "
    "<i>worse or equal</i> relative to the validity constraint, not randomly better. "
    "This guarantees that once a window becomes invalid, contraction from the left "
    "is the correct — and only necessary — response.",
    sBody))

story += code_block([
    "## Monotonicity HOLDS (all positive integers, sum constraint):",
    "## Adding arr[right] to window → sum increases or stays same (arr[right] >= 0)",
    "## If sum > target (invalid): removing arr[left] will bring it back down",
    "## ✅ Sliding window works",
    "",
    "## Monotonicity BREAKS (array with negative numbers):",
    "## arr = [10, -5, 3, 2, -8, 15], target = 10",
    "## Window [10,-5,3,2] has sum=10 (valid). Add -8 → sum=2 (still valid!)",
    "## Add 15 → sum=17 (invalid). Remove arr[left]=10 → sum=7.",
    "## But maybe arr[left+1..]  has a valid subarray we MISSED by moving left!",
    "## ❌ Sliding window may skip valid windows when negatives are present",
])

story += callout(
    "Negative numbers destroy the monotonicity guarantee for variable-size windows: "
    "adding a negative element can make the window MORE valid (sum decreases), "
    "meaning the window should not shrink after adding it. "
    "In this case, use Prefix Sum + HashMap instead.",
    C_RED, icon="⚠️")

story.append(P("<b>The Non-Shrinkable Window Optimisation</b>", sH2))
story.append(P(
    "For problems asking for the <b>maximum window length</b>, there's a powerful "
    "optimisation: instead of fully shrinking back to a valid state, <b>just shift "
    "the window one position</b>. The window size never decreases — it only "
    "grows or slides. This removes the inner while loop entirely.",
    sBody))
story += code_block([
    "## ─── Non-Shrinkable (Fixed-Max-Size) Pattern ───────────────────",
    "## Used for: longest subarray / longest window type problems",
    "## Insight: once the max_len window is found, we only care if a LARGER",
    "##          window exists — never need to shrink below current max.",
    "",
    "def non_shrinkable_window(arr, k):",
    "    freq  = defaultdict(int)",
    "    left  = 0",
    "",
    "    for right in range(len(arr)):",
    "        freq[arr[right]] += 1                  ## EXPAND",
    "",
    "        ## If invalid: shift window right by 1 (don't shrink further)",
    "        if is_invalid(freq, k):                ## e.g. distinct > k",
    "            freq[arr[left]] -= 1               ## remove outgoing left",
    "            if freq[arr[left]] == 0: del freq[arr[left]]",
    "            left += 1                          ## advance left by exactly 1",
    "        ## Note: NO while loop — window size never decreases",
    "",
    "    ## Window size at end = right - left + 1 = max valid length found",
    "    return len(arr) - left                     ## equivalent to right-left+1 at end",
])

story += callout(
    "The non-shrinkable pattern replaces 'while invalid: shrink' with "
    "'if invalid: shift by 1'. This sacrifices tracking intermediate valid windows "
    "(which you don't need for longest problems) and eliminates the inner loop. "
    "The window acts like a ratchet — it only ever stays the same or grows.",
    C_ACCENT2, icon="⚡")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6 — COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(6, "Comparison & Decision Making")

story.append(P("<b>Sliding Window vs. Two Pointers</b>", sH2))
story.append(P(
    "Sliding Window is a <b>specialisation</b> of Two Pointers. Both use a left "
    "and right index. The conceptual distinction: Two Pointers cares about the "
    "<i>specific elements</i> at those two positions; Sliding Window cares about "
    "the <i>aggregate state of the range between them</i>.",
    sBody))

sw_tp_data = [
    [th("Dimension"), th("Sliding Window"), th("General Two Pointers")],
    [td("Focus",             C_BODY), td("Content/aggregate of the range [L..R]", C_BODY), td("The specific elements AT positions L and R", C_BODY)],
    [td("Pointer direction", C_BODY), td("Both move left→right only (same direction)", C_BODY), td("Can converge (opposite ends) or same direction", C_BODY)],
    [td("State tracked",     C_BODY), td("Sum, counter, frequency map of window contents", C_BODY), td("Comparison result of arr[L] and arr[R]", C_BODY)],
    [td("Sorting required?", C_BODY), td("❌ No — works on original order", C_GREEN), td("✅ Usually yes for converging pattern", C_YELLOW)],
    [td("Negative numbers",  C_BODY), td("❌ Variable-size breaks; fixed-size OK", C_RED), td("✅ With sorting + HashMap", C_GREEN)],
    [td("Typical goal",      C_BODY), td("Longest/shortest subarray/substring with property", C_BODY), td("Find pair/triplet, palindrome, cycle detection", C_BODY)],
    [td("Key question",      C_BODY), td("'Does this RANGE satisfy a condition?'", C_ACCENT, "Helvetica-Oblique"), td("'Do these TWO ELEMENTS satisfy a condition?'", C_PURPLE, "Helvetica-Oblique")],
]
story.append(std_table(sw_tp_data, [110, 215, 155]))
story.append(Spacer(1, 10))

story.append(P("<b>Sliding Window vs. Prefix Sum</b>", sH2))

sw_ps_data = [
    [th("Dimension"), th("Sliding Window"), th("Prefix Sum + HashMap")],
    [td("Negative numbers", C_BODY), td("❌ Variable window breaks", C_RED), td("✅ Fully supported", C_GREEN)],
    [td("Query type",       C_BODY), td("Contiguous range with condition", C_BODY), td("Exact sum = K, count of valid subarrays", C_BODY)],
    [td("State maintained", C_BODY), td("Running window state (live)", C_BODY), td("Prefix totals (precomputed)", C_BODY)],
    [td("Preprocessing",    C_BODY), td("❌ None — processes on the fly", C_GREEN), td("O(n) prefix array build", C_YELLOW)],
    [td("Multiple queries", C_BODY), td("❌ Must re-run for each query", C_RED), td("✅ O(1) per query after build", C_GREEN)],
    [td("Exact sum = K",    C_BODY), td("⚠️ Only for non-negative arrays", C_YELLOW), td("✅ Natural: prefix[R+1] - prefix[L] = K", C_GREEN)],
    [td("Best for",         C_BODY), td("Longest/shortest window, max/min over range", C_ACCENT, "Helvetica-Oblique"), td("Count of subarrays, exact-sum queries, negatives", C_PURPLE, "Helvetica-Oblique")],
]
story.append(std_table(sw_ps_data, [120, 205, 155]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1", "Does the problem involve a CONTIGUOUS subarray or substring?",   C_ACCENT),
    (" → NO",  "Not a sliding window problem. Consider sort + two pointers, DP, etc.", C_MUTED),
    (" → YES", "Continue to Q2.",                                             C_GREEN),
    ("Q2", "Is the window size FIXED (given k) or VARIABLE?",                C_ACCENT),
    (" → FIXED",    "Use Fixed-Size Window template. O(n), no inner loop.",  C_ACCENT2),
    (" → VARIABLE", "Continue to Q3.",                                       C_GREEN),
    ("Q3", "Can the array contain NEGATIVE numbers?",                        C_ACCENT),
    (" → YES",  "Sliding window (variable) likely fails. Use Prefix Sum + HashMap.", C_RED),
    (" → NO",   "Continue to Q4.",                                           C_GREEN),
    ("Q4", "Are you looking for LONGEST/MAXIMUM or SHORTEST/MINIMUM window?",C_ACCENT),
    (" → LONGEST",  "Evaluate AFTER inner while loop. Consider non-shrinkable opt.", C_GREEN),
    (" → SHORTEST", "Evaluate INSIDE inner while loop (before each left++).",C_YELLOW),
]
for label, text, clr in flow:
    bg = C_CARD if not label.startswith(" ") else C_DARK2
    story.append(Table([[
        P(f"<b>{label}</b>", S("_", fontName="Courier-Bold", fontSize=9, textColor=clr)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[80, CW-80],
    style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER),
    ])))
story.append(Spacer(1,8))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7 — SLIDING WINDOW MAXIMUM
# ════════════════════════════════════════════════════════
story += section_divider(7, "Advanced: Sliding Window Maximum")

story.append(P("<b>The Problem</b>", sH2))
story.append(P(
    "Given an array and a window size k, find the maximum element in every "
    "contiguous window of size k. Output is an array of length n−k+1. "
    "The naive approach checks all k elements per window: O(n·k). "
    "The optimal solution uses a <b>Monotonic Deque</b> to answer each step in O(1) "
    "amortised, giving O(n) total.",
    sBody))

story += code_block([
    "## ─── Brute Force: O(n·k) — for reference ───────────────────────",
    "def sliding_max_brute(arr, k):",
    "    return [max(arr[i:i+k]) for i in range(len(arr)-k+1)]",
    "## Simple but: max() scans k elements → O(n·k) total",
])

story.append(P("<b>The Monotonic Deque (Decreasing)</b>", sH2))
story.append(P(
    "A <b>Monotonic Deque</b> is a double-ended queue that maintains a "
    "<b>decreasing sequence of indices</b>. The front always holds the index "
    "of the maximum element in the current window. Two invariants are enforced "
    "on every step:",
    sBody))

deq_inv = [
    [th("Invariant"), th("Enforcement"), th("Why")],
    [td("Front index is within the window [left..right]", C_ACCENT),
     td("Pop front if deque[0] <= right - k",    C_BODY),
     td("Expired elements cannot be the maximum", C_MUTED)],
    [td("Deque is strictly decreasing",           C_ACCENT2),
     td("Pop back while arr[back] <= arr[right]", C_BODY),
     td("A smaller element behind right can never be max while right is in window", C_MUTED)],
]
story.append(std_table(deq_inv, [170, 165, 145]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Sliding Window Maximum: O(n) with Monotonic Deque ─────────",
    "from collections import deque",
    "",
    "def sliding_max(arr, k):",
    "    if not arr or k == 0: return []",
    "    dq     = deque()   ## stores INDICES, not values; front = max index",
    "    result = []",
    "",
    "    for right in range(len(arr)):",
    "",
    "        ## ── Invariant 1: remove indices outside the window ───────",
    "        while dq and dq[0] <= right - k:",
    "            dq.popleft()",
    "",
    "        ## ── Invariant 2: maintain decreasing order ───────────────",
    "        ## Remove all back indices whose VALUES are <= arr[right]",
    "        ## (they can never be the max while right is in window)",
    "        while dq and arr[dq[-1]] <= arr[right]:",
    "            dq.pop()",
    "",
    "        dq.append(right)",
    "",
    "        ## ── Record result once first full window is formed ───────",
    "        if right >= k - 1:",
    "            result.append(arr[dq[0]])  ## dq[0] = index of max",
    "",
    "    return result",
])

story.append(P("<b>Visual Trace: arr=[3,1,3,5,2,4], k=3</b>", sH3))
deq_trace = [
    (0, "3",  "[0]",         "—",       "Build window"),
    (1, "1",  "[0,1]",       "—",       "1 < 3, append"),
    (2, "3",  "[0,2]",       "3",       "3≤3 pop idx1; window full → max=arr[0]=3"),
    (3, "5",  "[3]",         "5",       "5>3 pop all; new max=arr[3]=5"),
    (4, "2",  "[3,4]",       "5",       "2<5, append; max=arr[3]=5"),
    (5, "4",  "[3,5]",       "5",       "4>2 pop idx4; idx3 in window; max=5"),
]
dt_data = [[th("right"), th("arr[R]"), th("Deque (indices)"), th("Output"), th("Action")]]
for r, val, dq, out, act in deq_trace:
    out_disp = td(out, C_GREEN) if out != "—" else td("—", C_MUTED)
    dt_data.append([tdc(str(r), C_ACCENT), tdc(val, C_HEADING), tdc(dq, C_ACCENT2), out_disp, td(act, C_MUTED, size=8.5)])
story.append(std_table(dt_data, [45, 55, 120, 60, 200]))
story.append(P("Result: [3, 5, 5, 5]", sCaption))
story.append(Spacer(1, 8))

story += callout(
    "Why O(n)? Each element is added to and removed from the deque at most once "
    "across the entire algorithm. Total deque operations ≤ 2n = O(n), "
    "regardless of k. This is the amortised argument that beats the O(nk) brute force.",
    C_GREEN, icon="📊")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8 — UNIVERSAL TEMPLATE
# ════════════════════════════════════════════════════════
story += section_divider(8, "Universal Template & Mental Models")

story.append(P("<b>The Complete Variable Window Template</b>", sH2))
story += code_block([
    "## ════════════════════════════════════════════════════════════════",
    "## UNIVERSAL SLIDING WINDOW TEMPLATE — Variable Size",
    "## ════════════════════════════════════════════════════════════════",
    "def sliding_window(arr):",
    "    ## ── 0. Initialise state ──────────────────────────────────────",
    "    left        = 0",
    "    window_sum  = 0          ## or: freq = defaultdict(int)",
    "    best        = 0          ## or: float('inf') for minimization",
    "",
    "    ## ── 1. Right pointer sweeps entire array (never goes back) ──",
    "    for right in range(len(arr)):",
    "",
    "        ## ── 2. EXPAND: add arr[right] to window state ────────────",
    "        window_sum += arr[right]",
    "        ## (or: freq[arr[right]] += 1; distinct += (freq[x]==1))",
    "",
    "        ## ── 3. CONTRACT: restore validity ────────────────────────",
    "        ## For LONGEST: while is_invalid(state) → shrink",
    "        ## For SHORTEST: while is_valid(state)  → record then shrink",
    "        while window_sum > TARGET:       ## ← customise this condition",
    "            window_sum -= arr[left]",
    "            ## (or: freq[arr[left]] -= 1; distinct -= (freq[x]==0))",
    "            left += 1",
    "",
    "        ## ── 4. EVALUATE: window [left..right] is now valid ───────",
    "        ## Longest: best = max(best, right - left + 1)",
    "        ## Counting: best += 1 (or right - left + 1 for # valid windows)",
    "        ## Minimum: best = min(best, right - left + 1)  ← inside while",
    "        best = max(best, right - left + 1)",
    "",
    "    return best",
    "",
    "## ════════════════════════════════════════════════════════════════",
    "## UNIVERSAL SLIDING WINDOW TEMPLATE — Fixed Size (k)",
    "## ════════════════════════════════════════════════════════════════",
    "def fixed_sliding_window(arr, k):",
    "    if len(arr) < k: return []",
    "    state  = sum(arr[:k])    ## initialise first window",
    "    result = [state]",
    "    for right in range(k, len(arr)):",
    "        state += arr[right]       ## add right",
    "        state -= arr[right - k]   ## remove left (= right - k)",
    "        result.append(state)",
    "    return result",
])

story.append(P("<b>When to Evaluate: The Exact Placement Rule</b>", sH2))
eval_data = [
    [th("Problem Asks For"), th("Evaluate WHERE?"), th("Condition")],
    [td("Longest subarray/substring",      C_ACCENT),  td("AFTER the while loop",         C_GREEN),  tdc("best = max(best, r-l+1)")],
    [td("Shortest / minimum window",       C_ACCENT2), td("INSIDE the while loop",        C_YELLOW), tdc("best = min(best, r-l+1) before left++")],
    [td("Count of valid windows",          C_GREEN),   td("AFTER the while loop",         C_GREEN),  tdc("count += right - left + 1")],
    [td("Fixed-size result array",         C_PURPLE),  td("EACH iteration (after remove)",C_BODY),   tdc("result.append(state)")],
    [td("Maximum value in window",         C_ORANGE),  td("After window is full (r>=k-1)",C_BODY),   tdc("result.append(arr[dq[0]])")],
]
story.append(std_table(eval_data, [155, 160, 165]))
story.append(Spacer(1, 8))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
story.append(P("Answer these questions before writing a single line:", sBody))
checklist_items = [
    ("Fixed or Variable?",     "Is window size given (k) or determined by a condition?"),
    ("Name the state",         "What data structure tracks the window content? (int sum / dict freq / int distinct)"),
    ("Name the invalid cond.", "Write the exact while-loop condition as a comment before coding"),
    ("Expand action",          "What changes in state when arr[right] enters?"),
    ("Contract action",        "What changes in state when arr[left] leaves?"),
    ("Evaluate placement",     "After while loop (longest)? Inside while loop (shortest)?"),
    ("Negative numbers?",      "If yes, variable window fails → use Prefix Sum + HashMap"),
    ("Edge cases",             "Empty input? k=0? k > n? Single element?"),
]
for q, a in checklist_items:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ] {q}</font></b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[165, CW-165],
    style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER),
    ])))
story.append(Spacer(1, 8))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9 — PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(9, "LeetCode Problem Roadmap")
story.append(P("Solve in order — each problem introduces exactly one new concept.", sBody))

# Fixed
story.append(P("<b>🟢 Fixed-Size Window</b>", sH2))
fixed_data = [
    [th("#"), th("Problem"), th("State"), th("Key Insight")],
    [tdc("643", C_GREEN), td("Maximum Average Subarray I",             C_BODY), tdc("sum: int"),        td("Canonical fixed-window. sum÷k, slide.", C_MUTED)],
    [tdc("1343",C_GREEN), td("Number of Sub-arrays of Size K",         C_BODY), tdc("avg: float"),      td("Count windows where avg >= threshold.", C_MUTED)],
    [tdc("567", C_GREEN), td("Permutation in String",                  C_BODY), tdc("freq: dict"),      td("Two freq maps; compare on each slide.", C_MUTED)],
    [tdc("438", C_GREEN), td("Find All Anagrams in a String",          C_BODY), tdc("freq: dict"),      td("Fixed k=len(p); record when maps match.", C_MUTED)],
    [tdc("1456",C_GREEN), td("Max Number of Vowels in Substring of K", C_BODY), tdc("vowel_ct: int"),   td("Count vowels; +1 right, -1 if left was vowel.", C_MUTED)],
    [tdc("2090",C_GREEN), td("K Radius Subarray Averages",             C_BODY), tdc("sum: int"),        td("Window size = 2k+1; fill result array.", C_MUTED)],
]
story.append(std_table(fixed_data, [38, 205, 90, 147]))
story.append(Spacer(1, 10))

# Variable
story.append(P("<b>🟡 Variable-Size Window</b>", sH2))
var_data = [
    [th("#"), th("Problem"), th("State"), th("Invalid Condition")],
    [tdc("3",   C_YELLOW), td("Longest Substring Without Repeating Chars", C_BODY), tdc("freq: dict"),        td("freq[c] > 1", C_RED)],
    [tdc("1004",C_YELLOW), td("Max Consecutive Ones III (flip k zeros)", C_BODY),   tdc("zero_ct: int"),      td("zero_ct > k", C_RED)],
    [tdc("424", C_YELLOW), td("Longest Repeating Character Replacement",  C_BODY),  tdc("freq+max_f: int"),   td("(r-l+1) - max_freq > k", C_RED)],
    [tdc("904", C_YELLOW), td("Fruit Into Baskets (at most 2 types)",     C_BODY),  tdc("distinct: int"),     td("distinct > 2", C_RED)],
    [tdc("487", C_YELLOW), td("Max Consecutive Ones II",                  C_BODY),  tdc("zero_ct: int"),      td("zero_ct > 1", C_RED)],
    [tdc("1695",C_YELLOW), td("Maximum Erasure Value",                    C_BODY),  tdc("seen: set, sum"),    td("duplicate element in window", C_RED)],
    [tdc("2024",C_YELLOW), td("Maximize the Confusion of Exam",           C_BODY),  tdc("freq: dict"),        td("min(freq[T],freq[F]) > k", C_RED)],
    [tdc("1208",C_YELLOW), td("Get Equal Substrings Within Budget",       C_BODY),  tdc("cost: int"),         td("cost > maxCost", C_RED)],
]
story.append(std_table(var_data, [38, 205, 110, 127]))
story.append(Spacer(1, 10))

# Hard
story.append(P("<b>🔴 Hard — Master Problems</b>", sH2))
hard_data = [
    [th("#"), th("Problem"), th("Technique"), th("Key Insight")],
    [tdc("76",  C_RED), td("Minimum Window Substring",             C_BODY), td("Variable + satisfied counter", C_PURPLE),
     td("Track 'formed' count (chars at required freq). Evaluate inside shrink loop.", C_MUTED)],
    [tdc("239", C_RED), td("Sliding Window Maximum",               C_BODY), td("Fixed + Monotonic Deque",      C_PURPLE),
     td("Decreasing deque of indices. Front = max. Pop expired front, smaller back.", C_MUTED)],
    [tdc("992", C_RED), td("Subarrays with K Different Integers",  C_BODY), td("Variable: exactly(k)=atMost(k)-atMost(k-1)", C_PURPLE),
     td("Exact K = at-most K minus at-most K-1. Two variable windows.", C_MUTED)],
    [tdc("480", C_RED), td("Sliding Window Median",                C_BODY), td("Fixed + Two Heaps",            C_PURPLE),
     td("Max-heap for lower half, min-heap for upper. Rebalance on slide.", C_MUTED)],
    [tdc("30",  C_RED), td("Substring with Concatenation of All Words",C_BODY),td("Fixed (word-level)",        C_PURPLE),
     td("Window size=len(words)*word_len. Slide word by word, not char by char.", C_MUTED)],
]
story.append(std_table(hard_data, [38, 175, 130, 137]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 10 — EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(10, "Edge Cases & Pitfalls")

story.append(P("<b>Pitfall 1: k > n (Window Larger Than Array)</b>", sH2))
story.append(P(
    "For fixed-size windows, always guard against k > len(arr) at the top of "
    "the function. The loop range(len(arr) - k + 1) silently produces an empty "
    "range (no iterations) when k > n in Python, but will crash or misbehave "
    "in other languages. Explicit guards make intent clear.",
    sBody))
story += code_block([
    "def fixed_window_safe(arr, k):",
    "    if not arr:       return 0    ## empty input",
    "    if k == 0:        return 0    ## k=0 is usually undefined behaviour",
    "    if k > len(arr):  return 0    ## window larger than array",
    "    ## ... proceed safely ...",
])

story.append(P("<b>Pitfall 2: Off-by-One in Contraction</b>", sH2))
story.append(P(
    "The shrink condition must use <b>while</b>, not <b>if</b>. A single contraction "
    "step might not restore validity — multiple left++ moves may be needed. "
    "Using if instead of while causes the algorithm to stop shrinking too early, "
    "leaving invalid windows that corrupt the answer.",
    sBody))
story += code_block([
    "## WRONG — if only shrinks once:",
    "## if window_sum > target:",
    "##     window_sum -= arr[left]; left += 1",
    "## After this, window might STILL be invalid!",
    "",
    "## CORRECT — while shrinks until valid:",
    "while window_sum > target:   ## keep going until sum is within bounds",
    "    window_sum -= arr[left]",
    "    left += 1",
    "",
    "## Exception: non-shrinkable pattern intentionally uses 'if' (see Section 5)",
])

story.append(P("<b>Pitfall 3: Forgetting to Remove State on Left++</b>", sH2))
story.append(P(
    "When using a frequency map, you must <b>decrement the count</b> for arr[left] "
    "before incrementing left. Forgetting this leaves stale entries in the map, "
    "making the window state reflect elements that are no longer inside it.",
    sBody))
story += code_block([
    "## WRONG — state not cleaned up:",
    "## left += 1   ## left moved but freq[arr[left-1]] still > 0 in map!",
    "",
    "## CORRECT sequence for map-based windows:",
    "freq[arr[left]] -= 1              ## 1. Decrement count",
    "if freq[arr[left]] == 0:",
    "    del freq[arr[left]]           ## 2. Optional: remove zero-count entry",
    "left += 1                         ## 3. THEN advance pointer",
    "",
    "## Also update any derived counters BEFORE moving left:",
    "if freq[arr[left]] == 1:          ## about to become 0 → losing a distinct elem",
    "    distinct -= 1",
    "freq[arr[left]] -= 1",
    "left += 1",
])

story.append(P("<b>Pitfall 4: Using Variable Window on Negative Numbers</b>", sH2))
story += code_block([
    "## BROKEN: variable window with negatives",
    "## arr = [1, -1, 1, -1, 1], target_sum = 1",
    "## At right=4: window=[1,-1,1,-1,1], sum=1 → valid",
    "## Contract: remove arr[0]=1 → sum=0 → while continues → LEFT over-shrinks",
    "## The algorithm misses valid windows containing early negatives",
    "",
    "## CORRECT for this case: use Prefix Sum + HashMap",
    "## prefix_map = {0: 1}; running = 0",
    "## for val in arr: running += val",
    "##     if running - target in prefix_map: count += prefix_map[running - target]",
    "##     prefix_map[running] = prefix_map.get(running, 0) + 1",
])

story.append(P("<b>Pitfall 5: Evaluating at the Wrong Step</b>", sH3))
story += code_block([
    "## For MINIMUM window: evaluate INSIDE the while (before shrinking)",
    "while is_valid(state):",
    "    best = min(best, right - left + 1)   ## ← capture BEFORE removing left",
    "    remove(state, arr[left])",
    "    left += 1",
    "",
    "## For LONGEST window: evaluate AFTER the while (window is max-valid)",
    "while is_invalid(state):",
    "    remove(state, arr[left])",
    "    left += 1",
    "best = max(best, right - left + 1)       ## ← after contraction is complete",
])

story += callout(
    "Mnemonic: MINIMUM windows hide inside the valid state (evaluate before they escape). "
    "MAXIMUM windows stay as large as possible (evaluate after the shrink restores validity).",
    C_ACCENT2, icon="🧠")

# Final cheat sheet
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")
story.append(P("One-page reference for templates, state types, and all decision rules.", sBody))

cheat = [
    [th("Type"), th("Loop Structure"), th("State Update"), th("Evaluate Where"), th("Complexity")],
    [td("Fixed Window",      C_ACCENT),  tdc("for right: left=right-k"),      tdc("+=arr[r], -=arr[l]"), tdc("after remove"),        tdc("O(n) time O(1)")],
    [td("Variable (Longest)",C_ACCENT2), tdc("for r: while invalid: l++"),    tdc("add r, remove l"),    tdc("after while"),         tdc("O(n) amortised")],
    [td("Variable (Shortest)",C_GREEN),  tdc("for r: while valid: record+l++"),tdc("add r, remove l"),   tdc("inside while"),        tdc("O(n) amortised")],
    [td("Non-Shrinkable",    C_PURPLE),  tdc("for r: if invalid: l+=1"),      tdc("add r, remove l"),    tdc("len(arr)-left at end"),tdc("O(n) no inner loop")],
    [td("Monotonic Deque",   C_ORANGE),  tdc("for r: pop+append deque"),      tdc("pop expired+smaller"),tdc("arr[dq[0]] when r>=k-1"),tdc("O(n) amortised")],
]
story.append(std_table(cheat, [95, 140, 120, 120, 105]))
story.append(Spacer(1, 10))

story.append(P("<b>State Type Quick Reference</b>", sH2))
state_ref = [
    [th("Problem Signal"),                          th("State to Use"),             th("Invalid Trigger")],
    [td("max/min sum of subarray",    C_BODY),      tdc("window_sum: int"),         tdc("sum > target")],
    [td("no repeating chars",         C_BODY),      tdc("freq: dict"),              tdc("freq[c] > 1")],
    [td("at most k distinct",         C_BODY),      tdc("freq+distinct: int"),      tdc("distinct > k")],
    [td("contains all chars of t",    C_BODY),      tdc("freq+formed: int"),        tdc("formed < len(t)")],
    [td("max window element",         C_BODY),      tdc("deque (indices)",),        tdc("dq[0] <= right-k")],
    [td("flip at most k zeros",       C_BODY),      tdc("zero_count: int"),         tdc("zero_count > k")],
    [td("exact sum K (any signs)",    C_BODY),      td("→ Prefix Sum + HashMap",C_YELLOW), tdc("N/A — use complement lookup")],
]
story.append(std_table(state_ref, [175, 155, 150]))
story.append(Spacer(1, 12))

story.append(Table([[
    P("<b>You now have the complete Sliding Window mental model.</b><br/><br/>"
      "The technique rests on one insight: don't recompute — reuse. "
      "Maintain a window state that updates in O(1) as one element enters "
      "and one leaves. The rest is choosing the right state representation, "
      "correctly naming your invalid condition, and placing your evaluation "
      "call in exactly the right location relative to the contraction loop.<br/><br/>"
      "Suggested path: 643 → 3 → 424 → 76 → 239. "
      "After these five problems you will have internalized fixed, variable, "
      "minimum-window, and deque patterns — covering ~80% of all sliding window interviews.",
      S("_", fontName="Helvetica", fontSize=10, leading=16, textColor=C_BODY))
]], colWidths=[CW],
style=TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),C_CARD),
    ("BOX",(0,0),(-1,-1),2,C_ACCENT),
    ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20),
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
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, f"Sliding Window — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")