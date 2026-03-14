from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# ── Color Palette ──────────────────────────────────────────────────────────────
C_BG      = HexColor("#0F172A")
C_ACCENT  = HexColor("#38BDF8")
C_ACCENT2 = HexColor("#818CF8")
C_GREEN   = HexColor("#34D399")
C_YELLOW  = HexColor("#FBBF24")
C_RED     = HexColor("#F87171")
C_PURPLE  = HexColor("#C084FC")
C_ORANGE  = HexColor("#FB923C")
C_TEAL    = HexColor("#2DD4BF")
C_ROSE    = HexColor("#FB7185")
C_LIME    = HexColor("#A3E635")
C_CODE_BG = HexColor("#1E293B")
C_CODE_FG = HexColor("#E2E8F0")
C_HEADING = HexColor("#F1F5F9")
C_BODY    = HexColor("#CBD5E1")
C_MUTED   = HexColor("#64748B")
C_BORDER  = HexColor("#334155")
C_CARD    = HexColor("#1E293B")
C_DARK2   = HexColor("#141E2E")
C_DARK_CALLOUT = HexColor("#0C1F35")

PAGE_W, PAGE_H = letter
LEFT_MARGIN  = 0.65 * inch
RIGHT_MARGIN = 0.65 * inch
TOP_MARGIN   = 0.75 * inch
BOT_MARGIN   = 0.75 * inch
CW = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN   # ≈ 482 pts

# ── Paragraph Styles ───────────────────────────────────────────────────────────
sTitle    = ParagraphStyle("sTitle",    fontName="Helvetica-Bold",    fontSize=30, textColor=C_HEADING, alignment=TA_CENTER, leading=36, spaceAfter=8)
sSubtitle = ParagraphStyle("sSubtitle", fontName="Helvetica",         fontSize=13, textColor=C_ACCENT,  alignment=TA_CENTER, leading=18, spaceAfter=6)
sAuthor   = ParagraphStyle("sAuthor",   fontName="Helvetica-Oblique", fontSize=10, textColor=C_MUTED,   alignment=TA_CENTER, spaceAfter=18)
sH2       = ParagraphStyle("sH2",       fontName="Helvetica-Bold",    fontSize=14, leading=19, textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)
sH3       = ParagraphStyle("sH3",       fontName="Helvetica-Bold",    fontSize=11, leading=15, textColor=C_GREEN,   spaceBefore=8,  spaceAfter=4)
sBody     = ParagraphStyle("sBody",     fontName="Helvetica",         fontSize=10, leading=15, textColor=C_BODY,    alignment=TA_JUSTIFY, spaceAfter=6)
sBodyL    = ParagraphStyle("sBodyL",    fontName="Helvetica",         fontSize=10, leading=15, textColor=C_BODY,    alignment=TA_LEFT, spaceAfter=4)
sCaption  = ParagraphStyle("sCaption",  fontName="Helvetica-Oblique", fontSize=8.5, textColor=C_MUTED,  alignment=TA_CENTER, spaceAfter=6)
sFormula  = ParagraphStyle("sFormula",  fontName="Courier-Bold",      fontSize=10, leading=14, textColor=C_GREEN,   alignment=TA_CENTER)
sCode     = ParagraphStyle("sCode",     fontName="Courier",           fontSize=8.5, leading=13, textColor=C_CODE_FG, backColor=C_CODE_BG, leftIndent=12)
sCodeCmt  = ParagraphStyle("sCodeCmt",  fontName="Courier-Oblique",   fontSize=8.5, leading=13, textColor=C_MUTED,   backColor=C_CODE_BG, leftIndent=12)
sBullet   = ParagraphStyle("sBullet",   fontName="Helvetica",         fontSize=10, leading=15, textColor=C_BODY,    leftIndent=18, bulletIndent=6, spaceAfter=3)
sBullet2  = ParagraphStyle("sBullet2",  fontName="Helvetica",         fontSize=9.5, leading=14, textColor=C_BODY,   leftIndent=32, bulletIndent=20, spaceAfter=2)

# ── Helper: table cell styles ──────────────────────────────────────────────────
def th(text, color=C_MUTED):
    return Paragraph(f"<b>{text}</b>", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=color, leading=13))

def td(text, color=C_BODY, font="Helvetica", size=9):
    return Paragraph(text, ParagraphStyle("td", fontName=font, fontSize=size, textColor=color, leading=13))

def tdc(text, color=C_BODY):
    return Paragraph(text, ParagraphStyle("tdc", fontName="Courier", fontSize=8.5, textColor=color, leading=13))

# ── Helper: code block ─────────────────────────────────────────────────────────
def code_block(lines, lang="python"):
    header_data = [[Paragraph(f"<b>{lang}</b>",
                    ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=8,
                                   textColor=C_ACCENT, leading=11))]]
    header_style = TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_BORDER),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("BOX",          (0,0), (-1,-1), 0, C_BORDER),
    ])
    header = Table(header_data, colWidths=[CW])
    header.setStyle(header_style)

    body_rows = []
    for line in lines:
        style = sCodeCmt if line.startswith("##") else sCode
        body_rows.append([Paragraph(line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") if False else line, style)])

    body_style = TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), C_CODE_BG),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 1),
        ("BOTTOMPADDING",(0,0), (-1,-1), 1),
        ("BOX",          (0,0), (-1,-1), 1, C_BORDER),
        ("ROUNDEDCORNERS", [0, 0, 4, 4]),
    ])
    body = Table(body_rows, colWidths=[CW])
    body.setStyle(body_style)
    return [header, body, Spacer(1, 8)]

# ── Helper: callout ────────────────────────────────────────────────────────────
def callout(text, color, icon):
    content = Paragraph(f"{icon}  {text}", ParagraphStyle(
        "callout", fontName="Helvetica", fontSize=9.5, textColor=C_BODY,
        leading=14, leftIndent=4))
    t = Table([[content]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), C_DARK_CALLOUT),
        ("LEFTPADDING",  (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LINEBEFORE",   (0,0), (0,-1), 3, color),
        ("BOX",          (0,0), (-1,-1), 0.5, C_BORDER),
    ]))
    return [t, Spacer(1, 6)]

# ── Helper: section divider ────────────────────────────────────────────────────
def section_divider(num, title):
    num_style  = ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT,  alignment=TA_CENTER, leading=26)
    titl_style = ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=18, textColor=C_HEADING, alignment=TA_LEFT,   leading=22)
    row = [[Paragraph(str(num), num_style), Paragraph(title, titl_style)]]
    t = Table(row, colWidths=[40, CW - 40])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LINEBELOW",    (0,0), (-1,-1), 2, C_ACCENT),
    ]))
    return [Spacer(1, 10), t, Spacer(1, 8)]

# ── Helper: std table ─────────────────────────────────────────────────────────
def std_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    style_cmds = [
        ("BACKGROUND",   (0,0),  (-1,0),  C_BG),
        ("BOX",          (0,0),  (-1,-1), 0.8, C_BORDER),
        ("INNERGRID",    (0,0),  (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING",  (0,0),  (-1,-1), 8),
        ("RIGHTPADDING", (0,0),  (-1,-1), 8),
        ("TOPPADDING",   (0,0),  (-1,-1), 7),
        ("BOTTOMPADDING",(0,0),  (-1,-1), 7),
        ("VALIGN",       (0,0),  (-1,-1), "MIDDLE"),
    ]
    for i in range(1, len(data)):
        bg = C_CARD if i % 2 == 1 else C_DARK2
        style_cmds.append(("BACKGROUND", (0,i), (-1,i), bg))
    t.setStyle(TableStyle(style_cmds))
    return [t, Spacer(1, 10)]

# ── Page background callback ───────────────────────────────────────────────────
def add_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT_MARGIN, 0.55*inch, PAGE_W - RIGHT_MARGIN, 0.55*inch)
    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, f"Greedy Algorithms — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

# ══════════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ─────────────────────── COVER ───────────────────────────────────────────────
story.append(Spacer(1, 0.45*inch))
story.append(HRFlowable(width=CW, thickness=6, color=C_ACCENT, spaceAfter=18))
story.append(Paragraph("Greedy Algorithms", sTitle))
story.append(Paragraph("Zero-to-Hero LeetCode Guide", sSubtitle))
story.append(Paragraph("Senior Software Engineering &amp; DSA Series", sAuthor))
story.append(Spacer(1, 12))

# Feature card
feature_rows = [
    [Paragraph("<b>What You Will Learn</b>", ParagraphStyle("fh", fontName="Helvetica-Bold", fontSize=11, textColor=C_ACCENT, leading=16))],
    [Paragraph("&#x2022;  The Greedy Choice Property and Optimal Substructure", sBullet)],
    [Paragraph("&#x2022;  Why sorting is the universal prerequisite", sBullet)],
    [Paragraph("&#x2022;  Interval Scheduling, Partitioning, and Merging patterns", sBullet)],
    [Paragraph("&#x2022;  Two-Pointer Greedy optimizations", sBullet)],
    [Paragraph("&#x2022;  Gas Station &amp; Jump Game state-maintenance technique", sBullet)],
    [Paragraph("&#x2022;  Greedy vs Dynamic Programming — when each wins", sBullet)],
    [Paragraph("&#x2022;  Huffman Coding, Dijkstra, Prim/Kruskal (conceptual)", sBullet)],
    [Paragraph("&#x2022;  The Greedy Checklist &amp; common pitfalls", sBullet)],
]
ft = Table(feature_rows, colWidths=[CW])
ft.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), C_CARD),
    ("LEFTPADDING",  (0,0), (-1,-1), 16),
    ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ("TOPPADDING",   (0,0), (0,0),   10),
    ("BOTTOMPADDING",(0,-1),(-1,-1), 10),
    ("TOPPADDING",   (0,1), (-1,-1), 2),
    ("BOTTOMPADDING",(0,1), (-1,-2), 2),
    ("BOX",          (0,0), (-1,-1), 1, C_BORDER),
    ("LINEBEFORE",   (0,0), (0,-1),  3, C_GREEN),
]))
story.append(ft)
story.append(Spacer(1, 14))

# Quick-ref complexity table on cover
cov_data = [
    [th("Pattern", C_MUTED), th("Time", C_MUTED), th("Space", C_MUTED), th("Key Idea", C_MUTED)],
    [td("Interval Scheduling"), tdc("O(n log n)", C_GREEN), tdc("O(1)", C_GREEN),  td("Sort by end time, pick earliest finish")],
    [td("Interval Partition"),  tdc("O(n log n)", C_YELLOW),tdc("O(n)", C_YELLOW), td("Sort by start time, track active rooms")],
    [td("Two-Pointer Greedy"),  tdc("O(n)",       C_GREEN), tdc("O(1)", C_GREEN),  td("Move pointer that limits the objective")],
    [td("Jump Game"),           tdc("O(n)",       C_GREEN), tdc("O(1)", C_GREEN),  td("Maintain max-reachable index")],
    [td("Huffman Coding"),      tdc("O(n log n)", C_YELLOW),tdc("O(n)", C_YELLOW), td("Min-heap, merge smallest frequencies")],
]
story += std_table(cov_data, [CW*0.28, CW*0.15, CW*0.13, CW*0.44])
story.append(HRFlowable(width=CW, thickness=4, color=C_ACCENT2, spaceAfter=10))
story.append(PageBreak())

# ─────────────────────── SECTION 1: Core Philosophy ──────────────────────────
story += section_divider("01", "The Core Philosophy of Greedy")

story.append(Paragraph("What Is a Greedy Algorithm?", sH2))
story.append(Paragraph(
    "A greedy algorithm builds its solution piece by piece, always picking the option that "
    "looks best <i>right now</i> — the locally optimal choice — without worrying about what "
    "that choice does to future steps. The gamble is that a sequence of locally optimal "
    "decisions leads to a globally optimal answer.", sBody))

story += callout(
    "Greedy Mantra: At every decision point, pick the choice that maximises (or minimises) "
    "your immediate objective. Commit to it. Never look back.",
    C_ACCENT, "💡")

story.append(Paragraph("The Two Formal Requirements", sH2))
story.append(Paragraph("<b>1. Greedy Choice Property</b>", sH3))
story.append(Paragraph(
    "A globally optimal solution can be reached by making locally greedy choices. In other "
    "words, the greedy pick at step k is always consistent with some optimal overall solution — "
    "you never need to undo a committed choice.", sBody))

story.append(Paragraph("<b>2. Optimal Substructure</b>", sH3))
story.append(Paragraph(
    "After making a greedy choice, the remaining sub-problem has the same structure as the "
    "original. Solving it optimally and combining it with the greedy choice yields the optimal "
    "solution to the whole problem. This property is shared with Dynamic Programming; what "
    "differentiates Greedy is property #1.", sBody))

story.append(Paragraph("Complexity Advantage", sH2))
story.append(Paragraph(
    "Because a greedy algorithm commits to one branch and never re-evaluates alternatives, "
    "it avoids the exponential state-space exploration of brute force and the quadratic table-"
    "filling of classic DP. The typical cost is dominated by a sort:", sBody))

story.append(Paragraph("T(n)  =  O(n log n)  [sort]  +  O(n)  [single pass]  =  O(n log n)", sFormula))
story.append(Spacer(1, 8))

comp_data = [
    [th("Approach"), th("Typical Time"), th("Typical Space"), th("Backtracking?")],
    [td("Brute Force"),          tdc("O(2^n) or O(n!)", C_RED),    tdc("O(n)", C_RED),    td("Yes — full")],
    [td("Dynamic Programming"),  tdc("O(n^2) or O(n*W)", C_YELLOW),tdc("O(n^2)", C_YELLOW),td("No — memoised")],
    [td("Greedy"),               tdc("O(n log n)", C_GREEN),        tdc("O(1)–O(n)", C_GREEN), td("No — committed")],
]
story += std_table(comp_data, [CW*0.28, CW*0.22, CW*0.22, CW*0.28])

story.append(Paragraph("Proof of Correctness (Conceptual)", sH2))
story.append(Paragraph(
    "Greedy correctness is typically proved by an <b>Exchange Argument</b>: assume an optimal "
    "solution OPT differs from the greedy solution G. Show that you can swap OPT's choice at "
    "the first point of difference with G's choice without making the solution worse. Repeat "
    "until OPT and G are identical — contradiction, so G must be optimal.", sBody))

story += callout(
    "Exchange Argument Template: 'Suppose OPT skips item i but G picks it. Swapping in item i "
    "cannot increase cost (or decrease value), so the modified OPT is equally good but now "
    "agrees with G on item i. Induction completes the proof.'",
    C_GREEN, "🔁")

story.append(Paragraph("When Greedy Fails — The Danger Zone", sH2))
story.append(Paragraph(
    "Greedy fails when a locally optimal decision <i>locks you out</i> of a globally better "
    "path. The classic example:", sBody))
story += code_block([
    "## Greedy picks the heaviest coin first — WRONG for arbitrary denominations",
    "coins = [1, 3, 4]",
    "amount = 6",
    "",
    "## Greedy: picks 4, then needs 2 more → picks 1, 1  → 3 coins",
    "## DP:     picks 3, 3                              → 2 coins  ✓",
    "",
    "## The greedy choice (4) locked us into a sub-optimal path.",
    "## Exchange argument FAILS → use DP instead.",
])

story.append(PageBreak())

# ─────────────────────── SECTION 2: Sorting Prerequisite ─────────────────────
story += section_divider("02", "The Sorting Prerequisite")

story.append(Paragraph("Why Almost Every Greedy Starts with a Sort", sH2))
story.append(Paragraph(
    "Greedy algorithms make decisions in sequence. To guarantee that each local choice is "
    "globally safe, the input must be presented in an order that aligns with the greedy "
    "criterion. Sorting imposes that order in O(n log n) — a one-time investment that makes "
    "every subsequent O(1) decision correct.", sBody))

story += callout(
    "Rule of Thumb: Ask 'Which attribute determines priority?' Sort by that attribute first. "
    "The rest of the algorithm is usually a single O(n) scan.",
    C_YELLOW, "📌")

story.append(Paragraph("Choosing the Right Sorting Key", sH2))
sort_data = [
    [th("Problem Type"), th("Sort Key"), th("Why This Key Works")],
    [td("Interval Scheduling (max tasks, 1 room)"),    td("End time ↑"),       td("Finishing earliest leaves max room for future tasks")],
    [td("Interval Partitioning (min rooms)"),          td("Start time ↑"),     td("Process events in arrival order; allocate lazily")],
    [td("Fractional Knapsack"),                        td("Value/weight ↓"),   td("Highest density item always worth taking first")],
    [td("Task Scheduling (minimize lateness)"),        td("Deadline ↑"),       td("Earliest deadline first — exchange arg provable")],
    [td("Huffman Coding"),                             td("Frequency ↑ (heap)",C_TEAL), td("Least frequent symbols need longest codes")],
    [td("Jump Game II (min jumps)"),                   td("No sort — index"),  td("Scan left to right; index is natural order")],
    [td("Assign Cookies"),                             td("Both arrays ↑"),    td("Match smallest sufficient cookie to greediest child")],
]
story += std_table(sort_data, [CW*0.30, CW*0.22, CW*0.48])

story.append(Paragraph("End Time vs Start Time — A Concrete Comparison", sH2))
story.append(Paragraph(
    "Consider three intervals: A=[1,10], B=[2,4], C=[5,8]. We want the maximum number of "
    "non-overlapping intervals.", sBody))

story += code_block([
    "intervals = [(1,10), (2,4), (5,8)]",
    "",
    "## Sort by END time:",
    "## → [(2,4), (5,8), (1,10)]",
    "## Pick B=[2,4]  (ends at 4, no conflict yet)",
    "## Pick C=[5,8]  (starts at 5 >= 4, no conflict) ✓",
    "## Skip A=[1,10] (starts at 1 < 8, conflicts)    ✗",
    "## Result: 2 intervals  ← OPTIMAL",
    "",
    "## Sort by START time:",
    "## → [(1,10), (2,4), (5,8)]",
    "## Pick A=[1,10] (starts earliest)",
    "## Skip B=[2,4]  (overlaps A)",
    "## Skip C=[5,8]  (overlaps A)",
    "## Result: 1 interval   ← WRONG",
])

story += callout(
    "Insight: Sorting by start time is greedy about 'when we begin' — irrelevant to how many "
    "tasks fit. Sorting by end time is greedy about 'how soon we free the room' — exactly the "
    "right criterion.",
    C_TEAL, "🧠")

story.append(PageBreak())

# ─────────────────────── SECTION 3: Interval Patterns ────────────────────────
story += section_divider("03", "Interval Patterns — The Bread and Butter")

story.append(Paragraph("Pattern 1 — Interval Scheduling (Maximum Tasks, One Room)", sH2))
story.append(Paragraph(
    "Goal: given a list of tasks with start/end times, select the largest subset of tasks "
    "that can all fit in a single room (no two overlap). This is the canonical greedy "
    "problem and the foundation of every interval variant.", sBody))

story += code_block([
    "def interval_scheduling(intervals):",
    "    ## Sort by end time — the greedy criterion",
    "    intervals.sort(key=lambda x: x[1])",
    "    count = 0",
    "    last_end = float('-inf')",
    "",
    "    for start, end in intervals:",
    "        if start >= last_end:   ## no overlap with last picked task",
    "            count += 1",
    "            last_end = end      ## commit: update the room's free time",
    "",
    "    return count",
    "",
    "## Time: O(n log n) — dominated by sort",
    "## Space: O(1)  — only two scalars tracked",
])

story.append(Paragraph("Why It Works", sH3))
for bullet in [
    "After sorting by end time, the first interval <b>always</b> belongs to some optimal solution (exchange argument).",
    "Selecting it and discarding all conflicting intervals reduces to the same sub-problem on the remaining intervals.",
    "Induction: greedy picks are safe at every level.",
]:
    story.append(Paragraph(f"&#x2022;  {bullet}", sBullet))
story.append(Spacer(1, 6))

story.append(Paragraph("Pattern 2 — Interval Partitioning (Minimum Rooms)", sH2))
story.append(Paragraph(
    "Goal: assign every task to a room so no two tasks in the same room overlap, using the "
    "fewest rooms. Unlike scheduling, we must accommodate <i>all</i> tasks.", sBody))

story += code_block([
    "import heapq",
    "",
    "def interval_partitioning(intervals):",
    "    ## Sort by start time — process arrivals in order",
    "    intervals.sort(key=lambda x: x[0])",
    "    ## Min-heap of end-times of currently active rooms",
    "    rooms = []   ## heap stores the end time of each room",
    "",
    "    for start, end in intervals:",
    "        if rooms and rooms[0] <= start:",
    "            ## Greedy choice: reuse the room that frees up earliest",
    "            heapq.heapreplace(rooms, end)",
    "        else:",
    "            ## No room available — open a new one",
    "            heapq.heappush(rooms, end)",
    "",
    "    return len(rooms)   ## number of rooms used",
    "",
    "## Time: O(n log n)",
    "## Space: O(n)  — heap holds at most n end-times",
])

story += callout(
    "Key Insight: The minimum number of rooms needed equals the maximum number of tasks "
    "active simultaneously. The heap always shows the earliest-available room.",
    C_PURPLE, "🔑")

story.append(Paragraph("Pattern 3 — Merging Intervals", sH2))
story.append(Paragraph(
    "Goal: given a list of possibly overlapping intervals, merge all overlapping ones and "
    "return the minimal set of disjoint intervals.", sBody))

story += code_block([
    "def merge_intervals(intervals):",
    "    if not intervals:",
    "        return []",
    "    ## Sort by start time — merging candidates are adjacent after sort",
    "    intervals.sort(key=lambda x: x[0])",
    "    merged = [intervals[0]]",
    "",
    "    for start, end in intervals[1:]:",
    "        prev_start, prev_end = merged[-1]",
    "        if start <= prev_end:",
    "            ## Overlap: extend the current merged interval",
    "            merged[-1] = (prev_start, max(prev_end, end))",
    "        else:",
    "            ## No overlap: start a new interval in the result",
    "            merged.append((start, end))",
    "",
    "    return merged",
    "",
    "## Time: O(n log n)    Space: O(n)",
])

story.append(Paragraph("Three-Pattern Comparison", sH3))
pat_data = [
    [th("Pattern"), th("Goal"), th("Sort Key"), th("Data Structure"), th("Output")],
    [td("Scheduling"),   td("Max tasks, 1 room"),   td("End ↑"),   td("1 variable"),  td("Count")],
    [td("Partitioning"), td("Min rooms, all tasks"), td("Start ↑"), td("Min-heap"),    td("Room count")],
    [td("Merging"),      td("Combine overlaps"),     td("Start ↑"), td("Result list"), td("Interval list")],
]
story += std_table(pat_data, [CW*0.18, CW*0.24, CW*0.14, CW*0.20, CW*0.24])

story.append(PageBreak())

# ─────────────────────── SECTION 4: Two-Pointer Greedy ───────────────────────
story += section_divider("04", "Two-Pointer Greedy")

story.append(Paragraph("Combining Greedy Choices with Pointers", sH2))
story.append(Paragraph(
    "Many greedy problems involve two ends of a sorted (or already ordered) array. Instead "
    "of trying all pairs in O(n<super>2</super>), we use two pointers that converge inward. "
    "The greedy insight tells us <i>which pointer to move</i>.", sBody))

story.append(Paragraph("The Core Pattern", sH3))
story += code_block([
    "def two_pointer_greedy(arr):",
    "    left, right = 0, len(arr) - 1",
    "    best = 0",
    "",
    "    while left < right:",
    "        ## Compute current objective with (left, right)",
    "        current = objective(arr, left, right)",
    "        best = max(best, current)",
    "",
    "        ## Greedy choice: move the pointer that LIMITS the objective.",
    "        ## Moving the stronger side can never improve things —",
    "        ## only moving the weaker side has a chance.",
    "        if arr[left] < arr[right]:",
    "            left += 1",
    "        else:",
    "            right -= 1",
    "",
    "    return best",
    "## Time: O(n)    Space: O(1)",
])

story.append(Paragraph("Worked Example — Container With Most Water", sH3))
story.append(Paragraph(
    "Given heights h[0..n-1], two walls at indices i and j hold "
    "min(h[i], h[j]) * (j - i) units of water. We want the maximum.", sBody))

story += code_block([
    "## Why move the shorter wall?",
    "## Area = min(h[L], h[R]) * width",
    "## If we move the TALLER wall inward:",
    "##   - width decreases by 1",
    "##   - min can only stay same or decrease",
    "##   - area CANNOT improve → pointless move",
    "## If we move the SHORTER wall inward:",
    "##   - width decreases by 1",
    "##   - but min MIGHT increase → area might improve",
    "## Therefore: always move the shorter wall. ✓",
])

story.append(Paragraph("Worked Example — Assign Cookies", sH3))
story.append(Paragraph(
    "Children have greed factors g[i]; cookies have sizes s[j]. Assign at most one cookie "
    "per child (size >= greed factor). Maximize satisfied children.", sBody))

story += code_block([
    "def assign_cookies(greed, sizes):",
    "    greed.sort()    ## sort both arrays ascending",
    "    sizes.sort()",
    "    child = cookie = 0",
    "",
    "    while child < len(greed) and cookie < len(sizes):",
    "        if sizes[cookie] >= greed[child]:",
    "            ## Greedy: smallest sufficient cookie satisfies this child.",
    "            ## Saving a bigger cookie for a needier child is always better.",
    "            child += 1",
    "        cookie += 1   ## try next cookie regardless",
    "",
    "    return child",
    "## Time: O(n log n)    Space: O(1)",
])

story += callout(
    "Two-Pointer Greedy Rule: Move the pointer whose current value is the bottleneck. "
    "The bottleneck pointer has nothing to lose — moving it is the only way to improve.",
    C_ORANGE, "👆")

story.append(PageBreak())

# ─────────────────────── SECTION 5: Gas Station & Jump Game ──────────────────
story += section_divider("05", "Gas Station and Jump Game — State Maintenance")

story.append(Paragraph("The 'Running Balance / Reachable Range' Pattern", sH2))
story.append(Paragraph(
    "A family of greedy problems requires maintaining a scalar state as you scan left to "
    "right: a running balance (net fuel), a maximum reach index, or a current range. The "
    "greedy key is: <i>'If I cannot survive this position, where should I have started "
    "instead?'</i>", sBody))

story.append(Paragraph("Gas Station — Circular Route Feasibility", sH2))
story += code_block([
    "def can_complete_circuit(gas, cost):",
    "    ## If total gas < total cost, impossible — no starting point helps.",
    "    if sum(gas) < sum(cost):",
    "        return -1",
    "",
    "    tank = 0",
    "    start = 0",
    "",
    "    for i in range(len(gas)):",
    "        tank += gas[i] - cost[i]   ## update running balance",
    "",
    "        if tank < 0:",
    "            ## Greedy insight: any start in [start, i] also fails",
    "            ## because they inherit the negative cumulative deficit.",
    "            ## Reset: try starting from i+1.",
    "            start = i + 1",
    "            tank = 0",
    "",
    "    return start",
    "## Time: O(n)    Space: O(1)",
])

story.append(Paragraph("Why the Greedy Reset Is Safe", sH3))
for b in [
    "If we cannot reach station i starting from <i>start</i>, we also cannot reach it starting from any station between <i>start</i> and i.",
    "This is because the cumulative balance from any intermediate start is strictly greater than from the current start, yet still goes negative at i — so all fail.",
    "Starting from i+1 is the only remaining candidate; by the global-sum check above, it must succeed.",
]:
    story.append(Paragraph(f"&#x2022;  {b}", sBullet))
story.append(Spacer(1, 6))

story.append(Paragraph("Jump Game — Maximum Reach", sH2))
story.append(Paragraph(
    "Given nums[i] = max jump length from index i, can you reach the last index? The greedy "
    "state is <b>max_reach</b>: the furthest index reachable from any position visited so far.", sBody))

story += code_block([
    "def can_jump(nums):",
    "    max_reach = 0",
    "",
    "    for i, jump in enumerate(nums):",
    "        if i > max_reach:",
    "            ## We have fallen into a gap — unreachable zone.",
    "            return False",
    "        ## Greedy: always update to the furthest we can reach",
    "        max_reach = max(max_reach, i + jump)",
    "",
    "    return True",
    "## Time: O(n)    Space: O(1)",
])

story.append(Paragraph("Jump Game II — Minimum Jumps (BFS-like Greedy)", sH2))
story += code_block([
    "def jump_min(nums):",
    "    jumps = 0",
    "    current_end = 0   ## end of the current 'BFS level'",
    "    farthest   = 0   ## farthest we can reach from this level",
    "",
    "    for i in range(len(nums) - 1):",
    "        ## Greedy: always extend farthest as we scan",
    "        farthest = max(farthest, i + nums[i])",
    "",
    "        if i == current_end:    ## we've exhausted this jump level",
    "            jumps += 1",
    "            current_end = farthest  ## commit to next level",
    "",
    "    return jumps",
    "## Time: O(n)    Space: O(1)",
])

story += callout(
    "State Maintenance Pattern: scan left→right; maintain a scalar (balance, reach, window end). "
    "When the scalar goes invalid, reset greedily to the best available starting point.",
    C_TEAL, "📊")

story.append(PageBreak())

# ─────────────────────── SECTION 6: Greedy vs DP ─────────────────────────────
story += section_divider("06", "Greedy vs Dynamic Programming")

story.append(Paragraph("The Fundamental Distinction", sH2))
story.append(Paragraph(
    "Both Greedy and DP exploit optimal substructure. The difference is whether a single "
    "greedy choice is always safe (Greedy) or whether we need to evaluate all choices and "
    "remember their results (DP). Getting this decision wrong is the most common "
    "interview mistake.", sBody))

cmp_data = [
    [th("Dimension"), th("Greedy"), th("Dynamic Programming")],
    [td("Decision method"),   td("One best choice per step"),     td("Try all choices; keep best")],
    [td("Subproblem overlap"), td("No — each sub-problem solved once"), td("Yes — table reuse is the point")],
    [td("Choice property"),   td("Locally optimal ⇒ globally optimal"), td("No such guarantee needed")],
    [td("Time complexity"),   tdc("O(n log n) typical", C_GREEN),  tdc("O(n^2) or O(n*W) typical", C_YELLOW)],
    [td("Space complexity"),  tdc("O(1) or O(n)", C_GREEN),        tdc("O(n) or O(n^2)", C_YELLOW)],
    [td("Backtracking"),      td("Never"),                         td("Implicit via table")],
    [td("Implementation"),    td("Sort + single pass"),            td("Recurrence + memo/tabulation")],
    [td("Proof needed"),      td("Exchange argument required"),    td("Correctness from recurrence")],
    [td("Failure mode"),      td("Local optimum != global"),       td("Exponential time if not memoised")],
]
story += std_table(cmp_data, [CW*0.28, CW*0.36, CW*0.36])

story.append(Paragraph("The Knapsack Duality — Where Greedy Breaks", sH2))
story.append(Paragraph(
    "The knapsack problem is the textbook example showing why Greedy is not universally "
    "applicable. The two variants look identical but have fundamentally different solutions.", sBody))

story.append(Paragraph("Fractional Knapsack — Greedy Wins", sH3))
story += code_block([
    "## Items: (value, weight)  Capacity: W",
    "## You can take fractions of any item.",
    "",
    "def fractional_knapsack(items, W):",
    "    ## Greedy: sort by value-density (value/weight) descending",
    "    items.sort(key=lambda x: x[0]/x[1], reverse=True)",
    "    total_value = 0.0",
    "",
    "    for value, weight in items:",
    "        if W == 0:",
    "            break",
    "        take = min(weight, W)        ## take as much as possible",
    "        total_value += take * (value / weight)",
    "        W -= take",
    "",
    "    return total_value",
    "## Time: O(n log n)   — Greedy is CORRECT here ✓",
])

story.append(Paragraph("0/1 Knapsack — Greedy Fails, Use DP", sH3))
story += code_block([
    "## Same setup, but items are INDIVISIBLE — take all or nothing.",
    "",
    "## Counter-example where Greedy fails:",
    "## items = [(60, 10), (100, 20), (120, 30)]  W = 50",
    "## Density order: 6.0, 5.0, 4.0",
    "## Greedy: take item1 (w=10, v=60), item2 (w=20, v=100) → total value = 160",
    "## DP:     take item2 (w=20) + item3 (w=30) → total value = 220  ✓",
    "",
    "## The greedy density choice 'locked out' a better full-item combination.",
    "## Correct solution requires DP tabulation:",
    "",
    "def knapsack_01(items, W):",
    "    n = len(items)",
    "    dp = [[0] * (W + 1) for _ in range(n + 1)]",
    "",
    "    for i in range(1, n + 1):",
    "        value, weight = items[i-1]",
    "        for w in range(W + 1):",
    "            dp[i][w] = dp[i-1][w]   ## don't take item i",
    "            if weight <= w:",
    "                dp[i][w] = max(dp[i][w], dp[i-1][w-weight] + value)  ## take",
    "",
    "    return dp[n][W]",
    "## Time: O(n * W)   Space: O(n * W)",
])

story += callout(
    "The fractional/0-1 split is the most powerful diagnostic tool: if the problem allows "
    "partial choices (split tasks, fractional resources), Greedy often works. If choices are "
    "binary (take-it-or-leave-it), almost always use DP.",
    C_ROSE, "⚖️")

story.append(Paragraph("Quick Decision Guide", sH3))
dec_data = [
    [th("Signal in Problem"), th("Try")],
    [td("'Maximum number of non-overlapping...'"),  tdc("Greedy — sort by end", C_GREEN)],
    [td("'Minimum number of operations/rooms...'"), tdc("Greedy or DP — check for subproblems", C_YELLOW)],
    [td("'Maximum value with weight limit'"),       tdc("0/1 → DP;  Fractional → Greedy", C_TEAL)],
    [td("'Minimum cost path / longest subseq'"),   tdc("DP", C_YELLOW)],
    [td("'Can you reach the end?'"),               tdc("Greedy — maintain max reach", C_GREEN)],
    [td("Choices depend on previous choices"),     tdc("DP", C_YELLOW)],
    [td("Exchange argument holds"),                tdc("Greedy", C_GREEN)],
]
story += std_table(dec_data, [CW*0.55, CW*0.45])

story.append(PageBreak())

# ─────────────────────── SECTION 7: Huffman & Graphs ─────────────────────────
story += section_divider("07", "Huffman Coding and Graph Algorithms")

story.append(Paragraph("Greedy in Data Compression — Huffman Coding", sH2))
story.append(Paragraph(
    "Huffman coding builds an optimal prefix-free binary code by repeatedly merging the two "
    "least-frequent symbols into a new node. The result is a binary tree where frequent "
    "symbols get shorter codes.", sBody))

story += code_block([
    "import heapq",
    "",
    "def huffman_coding(frequencies):",
    "    ## Build min-heap of (frequency, symbol) pairs",
    "    heap = [[freq, sym] for sym, freq in frequencies.items()]",
    "    heapq.heapify(heap)   ## O(n)",
    "",
    "    while len(heap) > 1:",
    "        ## Greedy: always merge the two LEAST frequent nodes",
    "        left  = heapq.heappop(heap)   ## smallest",
    "        right = heapq.heappop(heap)   ## second smallest",
    "",
    "        ## New internal node with combined frequency",
    "        merged = [left[0] + right[0], left, right]",
    "        heapq.heappush(heap, merged)",
    "",
    "    ## The remaining node is the root of the Huffman tree",
    "    return heap[0]",
    "## Time: O(n log n)   Space: O(n)",
])

story += callout(
    "Huffman Optimality Proof: By exchange argument, swapping any two nodes in the tree "
    "with the two least-frequent symbols into the deepest positions can only improve (or "
    "maintain) total encoded length. Inducting over tree levels proves global optimality.",
    C_GREEN, "📦")

story.append(Paragraph("Greedy in Graph Algorithms", sH2))

story.append(Paragraph("Dijkstra's Shortest Path", sH3))
story.append(Paragraph(
    "Dijkstra maintains a min-heap of (distance, node) pairs. At each step it greedily "
    "extracts the unvisited node with the minimum known distance and relaxes its neighbors. "
    "The greedy choice property holds because, with non-negative weights, the minimum "
    "distance node cannot later be improved — any alternative path would be longer.", sBody))

story += code_block([
    "## Greedy insight: once we pop a node from the min-heap,",
    "## its distance is FINAL. No future path can be shorter",
    "## (all future edges are non-negative).",
    "",
    "## Step 1: Push (0, source) onto heap",
    "## Step 2: Pop minimum (dist, node)",
    "## Step 3: For each neighbor, if dist + edge_weight < known[neighbor]:",
    "##            update known[neighbor]; push to heap",
    "## Step 4: Repeat until heap empty",
    "",
    "## Time: O((V + E) log V)   Space: O(V)",
])

story.append(Paragraph("Prim's and Kruskal's Minimum Spanning Tree", sH3))

mst_data = [
    [th("Algorithm"), th("Greedy Strategy"), th("Data Structure"), th("Best For")],
    [td("Prim's"),    td("Always add the cheapest edge connecting the current tree to an unvisited vertex"), td("Min-heap + visited set"), td("Dense graphs")],
    [td("Kruskal's"), td("Sort all edges by weight; add each if it doesn't create a cycle"), td("Union-Find (DSU)"),       td("Sparse graphs")],
]
story += std_table(mst_data, [CW*0.15, CW*0.38, CW*0.27, CW*0.20])

story += callout(
    "MST Correctness — Cut Property: For any cut of the graph, the minimum-weight edge "
    "crossing the cut is always in some MST. Both Prim and Kruskal exploit this property.",
    C_ACCENT2, "🌐")

story += code_block([
    "## Kruskal's Algorithm Skeleton",
    "def kruskal(n, edges):",
    "    ## Greedy step 1: sort all edges by weight ascending",
    "    edges.sort(key=lambda e: e[2])",
    "    parent = list(range(n))",
    "",
    "    def find(x):    ## Union-Find path compression",
    "        if parent[x] != x: parent[x] = find(parent[x])",
    "        return parent[x]",
    "",
    "    mst_cost = 0",
    "    mst_edges = []",
    "",
    "    for u, v, weight in edges:",
    "        pu, pv = find(u), find(v)",
    "        if pu != pv:    ## Greedy step 2: only add if no cycle",
    "            parent[pu] = pv",
    "            mst_cost += weight",
    "            mst_edges.append((u, v, weight))",
    "",
    "    return mst_cost, mst_edges",
    "## Time: O(E log E)   Space: O(V)",
])

story.append(PageBreak())

# ─────────────────────── SECTION 8: Greedy Checklist ─────────────────────────
story += section_divider("08", "The Greedy Checklist and Common Pitfalls")

story.append(Paragraph("How to Test if a Problem is Greedy-Solvable", sH2))

chk_data = [
    [th("#"), th("Checklist Question"), th("If YES")],
    [tdc("1", C_ACCENT), td("Can I make one locally optimal choice without revisiting it later?"),              td("Strong greedy signal")],
    [tdc("2", C_ACCENT), td("Does the problem have optimal substructure (sub-problems same shape as original)?"),td("Necessary condition met")],
    [tdc("3", C_ACCENT), td("Can I prove an exchange argument — swapping to greedy choice never worsens result?"),td("Greedy is provably correct")],
    [tdc("4", C_ACCENT), td("Is the state reducible to a single scalar (balance, reach, count)?"),              td("O(n) scan likely works")],
    [tdc("5", C_ACCENT), td("After sorting, does a single left-to-right pass decide everything?"),              td("Classic greedy structure")],
    [tdc("6", C_RED),    td("Do choices at step k depend on the outcome of ALL previous choices?"),             td("Use DP instead")],
    [tdc("7", C_RED),    td("Is there a counter-example where local best != global best?"),                     td("Greedy fails — use DP/backtrack")],
]
story += std_table(chk_data, [CW*0.06, CW*0.65, CW*0.29])

story.append(Paragraph("Common Pitfalls", sH2))

pitfalls = [
    ("Wrong sort key", C_RED,
     "Sorting by start time when end time is the criterion (classic interval mistake). "
     "Always ask: 'What property determines which choice opens up the most future options?'"),
    ("Missing the global feasibility check", C_YELLOW,
     "Gas Station: greedy reset works, but only if total gas >= total cost. Skipping the "
     "O(n) global check leads to wrong starting points."),
    ("Greedy on a 0/1 structure", C_RED,
     "Applying density-greedy to an indivisible knapsack. Whenever items are atomic, "
     "enumerate all inclusion/exclusion combinations — that is DP territory."),
    ("Assuming sorted input", C_YELLOW,
     "Jump Game and Gas Station work on unsorted input. Many candidates mistakenly sort "
     "these arrays, destroying the index-based meaning of each element."),
    ("Off-by-one in two-pointer convergence", C_ORANGE,
     "Using 'left < right' vs 'left <= right' incorrectly. In greedy two-pointer, "
     "when left == right you have a single element — no pair exists. Always use strict <."),
    ("Greedy on unbounded sub-problems", C_PURPLE,
     "Coin change with arbitrary denominations has overlapping sub-problems. "
     "The greedy 'pick largest coin' fails for [1,3,4] with amount=6 — DP is required."),
]
for title, color, desc in pitfalls:
    story += callout(f"<b>{title}:</b>  {desc}", color, "⚠️")

story.append(Paragraph("The Four-Question Greedy Litmus Test", sH2))
story += code_block([
    "## Before writing any code, answer these four questions:",
    "",
    "## Q1: What is the 'greedy criterion' — the attribute I'm optimising at each step?",
    "##     (end time, density, minimum gap, etc.)",
    "",
    "## Q2: After committing to the greedy choice, is the remaining problem",
    "##     structurally identical to the original?  → Optimal substructure check.",
    "",
    "## Q3: Can I construct a counter-example in 2 minutes?",
    "##     If yes → greedy fails, switch to DP.",
    "##     If no  → proceed, but write the exchange argument mentally.",
    "",
    "## Q4: What is the natural sort key?",
    "##     Sort by it, then write a single O(n) scan.",
])

story.append(Paragraph("LeetCode Pattern Reference", sH2))
lc_data = [
    [th("LC #"), th("Title"), th("Pattern"), th("Key Greedy Idea")],
    [tdc("435",  C_YELLOW), td("Non-overlapping Intervals"),   td("Interval Scheduling"),   td("Sort end↑; count removals")],
    [tdc("452",  C_YELLOW), td("Minimum Arrows for Balloons"), td("Interval Scheduling"),   td("Sort end↑; arrow at end")],
    [tdc("56",   C_YELLOW), td("Merge Intervals"),             td("Interval Merge"),        td("Sort start↑; extend or append")],
    [tdc("253",  C_YELLOW), td("Meeting Rooms II"),            td("Interval Partition"),    td("Sort start↑; min-heap of ends")],
    [tdc("11",   C_YELLOW), td("Container With Most Water"),   td("Two-Pointer Greedy"),    td("Move shorter wall inward")],
    [tdc("455",  C_GREEN),  td("Assign Cookies"),              td("Two-Pointer Greedy"),    td("Sort both; match smallest sufficient")],
    [tdc("134",  C_YELLOW), td("Gas Station"),                 td("Running Balance"),       td("Reset start on negative tank")],
    [tdc("55",   C_YELLOW), td("Jump Game"),                   td("Max Reach"),             td("Track max_reach; fail if i > max_reach")],
    [tdc("45",   C_YELLOW), td("Jump Game II"),                td("BFS Levels Greedy"),     td("Jump at level boundary")],
    [tdc("1005", C_GREEN),  td("Maximize Sum After K Negations"), td("Sort + Greedy"),      td("Negate smallest negatives first")],
    [tdc("621",  C_YELLOW), td("Task Scheduler"),              td("Frequency Greedy"),      td("Schedule most frequent first")],
    [tdc("406",  C_YELLOW), td("Queue Reconstruction by Height"), td("Sort + Insert"),      td("Sort desc height; insert by k")],
]
story += std_table(lc_data, [CW*0.08, CW*0.28, CW*0.22, CW*0.42])

story.append(PageBreak())

# ─────────────────────── APPENDIX: Quick-Reference ───────────────────────────
story += section_divider("A", "Quick-Reference Summary")

story.append(Paragraph("All Patterns at a Glance", sH2))
summary_data = [
    [th("Pattern"),          th("Sort Key"),  th("State"),         th("Time"),       th("Classic Problems")],
    [td("Interval Sched."),  td("End ↑"),     tdc("last_end"),     tdc("O(n log n)"), td("435, 452, 646")],
    [td("Interval Part."),   td("Start ↑"),   tdc("min-heap"),     tdc("O(n log n)"), td("253, 56")],
    [td("Merge Intervals"),  td("Start ↑"),   tdc("result list"),  tdc("O(n log n)"), td("56, 57, 986")],
    [td("Two-Pointer"),      td("Both ↑ or natural"), tdc("L, R"), tdc("O(n)"),       td("11, 455, 881")],
    [td("Running Balance"),  td("None"),      tdc("tank, start"),  tdc("O(n)"),       td("134, 860")],
    [td("Max Reach"),        td("None"),      tdc("max_reach"),    tdc("O(n)"),       td("55, 45")],
    [td("BFS Levels"),       td("None"),      tdc("cur_end, far"), tdc("O(n)"),       td("45, 1326")],
    [td("Huffman / Heap"),   td("Freq ↑"),    tdc("min-heap"),     tdc("O(n log n)"), td("Huffman, 767, 621")],
    [td("Dijkstra"),         td("Dist ↑"),    tdc("min-heap"),     tdc("O(E log V)"), td("743, 787, 1514")],
    [td("Kruskal MST"),      td("Weight ↑"),  tdc("Union-Find"),   tdc("O(E log E)"), td("1135, 1584, 684")],
]
story += std_table(summary_data, [CW*0.18, CW*0.16, CW*0.14, CW*0.14, CW*0.38])

story.append(Paragraph("The Exchange Argument Template", sH2))
story += code_block([
    "## Template for proving any greedy algorithm correct:",
    "",
    "## 1. ASSUME an optimal solution OPT that differs from greedy G.",
    "## 2. FIND the first position i where they disagree.",
    "## 3. SWAP OPT's choice at i with G's greedy choice.",
    "## 4. SHOW the swap does not increase cost (or decrease value).",
    "## 5. REPEAT until OPT = G — contradiction with OPT being strictly better.",
    "## 6. CONCLUDE G is also optimal. ∎",
    "",
    "## Worked example (Interval Scheduling):",
    "## OPT picks interval X (ends at time 10).",
    "## G picks interval Y (ends at time 6, Y ends earlier).",
    "## Swap X for Y in OPT: Y fits (ends earlier, so nothing after X is blocked",
    "## any more than before). OPT still valid, not worse. Exchange complete. ✓",
])

story += callout(
    "Final Advice: When in doubt, spend 90 seconds trying a counter-example. "
    "If you find one — use DP. If you cannot — sketch the exchange argument, "
    "then code the sort + single-pass greedy.",
    C_ACCENT, "🎯")

story.append(Spacer(1, 20))
story.append(HRFlowable(width=CW, thickness=2, color=C_ACCENT2))
story.append(Spacer(1, 8))
story.append(Paragraph("End of Greedy Algorithms — Zero to Hero Guide", sCaption))

# ── Build PDF ──────────────────────────────────────────────────────────────────
output_path = "/mnt/user-data/outputs/greedy_algorithms_guide.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOT_MARGIN,
)
doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built:", output_path)