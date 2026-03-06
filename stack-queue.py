from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

# ── Color Palette ──────────────────────────────────────────────────────────────
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
C_ORANGE  = colors.HexColor("#FB923C")
C_TEAL    = colors.HexColor("#2DD4BF")
C_DARK2   = colors.HexColor("#141E2E")
C_ROSE    = colors.HexColor("#FB7185")
C_AMBER   = colors.HexColor("#F59E0B")
C_LIME    = colors.HexColor("#A3E635")

PAGE_W, PAGE_H = letter

doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Stack_Queue_Patterns_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)
CW = PAGE_W - 1.3*inch

# ── Style factory ──────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("T",  fontName="Helvetica-Bold",   fontSize=32, leading=40, textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)
sSubtitle= S("Su", fontName="Helvetica",         fontSize=13, leading=18, textColor=C_ACCENT,  alignment=TA_CENTER, spaceAfter=4)
sAuthor  = S("Au", fontName="Helvetica-Oblique", fontSize=10, textColor=C_MUTED,   alignment=TA_CENTER, spaceAfter=20)
sH2      = S("H2", fontName="Helvetica-Bold",   fontSize=14, leading=19, textColor=C_ACCENT2, spaceBefore=12, spaceAfter=5)
sH3      = S("H3", fontName="Helvetica-Bold",   fontSize=11, leading=15, textColor=C_GREEN,   spaceBefore=8,  spaceAfter=4)
sBody    = S("Bd", fontName="Helvetica",         fontSize=10, leading=15, textColor=C_BODY,    spaceAfter=6, alignment=TA_JUSTIFY)
sCode    = S("Co", fontName="Courier",           fontSize=8.5,leading=13, textColor=C_CODE_FG, spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sCodeCmt = S("Cm", fontName="Courier-Oblique",  fontSize=8.5,leading=13, textColor=C_MUTED,   spaceAfter=2, leftIndent=12, backColor=C_CODE_BG)
sFormula = S("Fm", fontName="Courier-Bold",     fontSize=10, leading=14, textColor=C_GREEN,   alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
sCaption = S("Ca", fontName="Helvetica-Oblique",fontSize=8.5, textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=6)
sTOC     = S("TO", fontName="Helvetica",         fontSize=10, leading=16, textColor=C_BODY)
sTOCSub  = S("TS", fontName="Helvetica",         fontSize=9,  leading=14, textColor=C_MUTED,  leftIndent=18)

P = Paragraph

# ── Helpers ────────────────────────────────────────────────────────────────────
def code_block(lines, lang="python"):
    hdr = Table([[P(f"<b>{lang}</b>", S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
        colWidths=[CW], style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0D1929")),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),14)]))
    rows = [[P(ln if ln else " ", sCodeCmt if ln.startswith("##") else sCode)] for ln in lines]
    body = Table(rows, colWidths=[CW], style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_CODE_BG),
            ("TOPPADDING",(0,0),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-1),1),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8)]))
    wrap = Table([[hdr],[body]], colWidths=[CW], style=TableStyle([
            ("BOX",(0,0),(-1,-1),1,C_BORDER),("ROUNDEDCORNERS",[4]),
            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
            ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0)]))
    return [wrap, Spacer(1,8)]

def callout(text, color=C_ACCENT, icon="💡"):
    tbl = Table([[P(f"{icon}  {text}", S("_", fontName="Helvetica", fontSize=9.5, leading=14, textColor=color))]],
        colWidths=[CW], style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0C1F35")),
            ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
            ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
            ("LINEBEFORE",(0,0),(0,-1),3,color)]))
    return [tbl, Spacer(1,6)]

def section_divider(num, title):
    lbl = f"{num:02d}" if num > 0 else "  "
    return [
        Spacer(1,10),
        Table([[
            P(f"<b>{lbl}</b>", S("_", fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT)),
            P(f"<b>{title}</b>", S("_", fontName="Helvetica-Bold", fontSize=18, textColor=C_HEADING, leading=24)),
        ]], colWidths=[40, CW-40], style=TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(0,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
            ("LINEBELOW",(0,0),(-1,-1),2,C_ACCENT),("BOTTOMPADDING",(0,0),(-1,-1),6)])),
        Spacer(1,8)]

def std_table(data, col_widths):
    return Table(data, colWidths=col_widths, style=TableStyle([
        ("BACKGROUND",(0,0),(-1,0),C_BG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD, C_DARK2]),
        ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))

def th(t, c=C_MUTED): return P(f"<b>{t}</b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=c))
def td(t, c=C_BODY, f="Helvetica", sz=9): return P(t, S("_", fontName=f, fontSize=sz, textColor=c, leading=13))
def tdc(t, c=C_BODY): return P(t, S("_", fontName="Courier", fontSize=9, textColor=c))

# ── Stack/Queue visual renderer ────────────────────────────────────────────────
def stack_vis(items, label="Stack", highlight_top=True, direction="vertical"):
    """Render a vertical stack with top-of-stack indicated."""
    if not items:
        tbl = Table([[P("(empty)", S("_", fontName="Courier-Oblique", fontSize=9,
            textColor=C_MUTED, alignment=TA_CENTER))]],
            colWidths=[90], style=TableStyle([
                ("BOX",(0,0),(-1,-1),1,C_BORDER),("BACKGROUND",(0,0),(-1,-1),C_CARD),
                ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
        return [tbl, Spacer(1,4)]

    rows = []
    for i, v in enumerate(reversed(items)):
        is_top = (i == 0)
        bg  = colors.HexColor("#0A2E3A") if (is_top and highlight_top) else C_CARD
        fg  = C_ACCENT if (is_top and highlight_top) else C_BODY
        lbl_txt = " ← top" if (is_top and highlight_top) else ""
        rows.append([
            P(f"<b>{v}</b>", S("_", fontName="Courier-Bold", fontSize=11, textColor=fg, alignment=TA_CENTER)),
            P(lbl_txt, S("_", fontName="Helvetica", fontSize=8, textColor=C_ACCENT))
        ])
    tbl = Table(rows, colWidths=[70, 60], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("BACKGROUND",(0,0),(1,0), colors.HexColor("#0A2E3A")) if highlight_top else ("BACKGROUND",(0,0),(0,0),C_CARD),
        ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),8)]))
    return [tbl, Spacer(1,4)]

def queue_vis(items, label="Queue"):
    """Render a horizontal queue with front/rear indicated."""
    if not items:
        tbl = Table([[P("(empty)", S("_", fontName="Courier-Oblique", fontSize=9,
            textColor=C_MUTED, alignment=TA_CENTER))]],
            colWidths=[100], style=TableStyle([
                ("BOX",(0,0),(-1,-1),1,C_BORDER),("BACKGROUND",(0,0),(-1,-1),C_CARD),
                ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
        return [tbl, Spacer(1,4)]

    n = len(items)
    col_w = min(55, int(CW / (n + 2)))
    lbl_row, val_row = [], []

    for i, v in enumerate(items):
        is_front = (i == 0)
        is_rear  = (i == n - 1)
        fg  = C_ACCENT if is_front else (C_GREEN if is_rear else C_BODY)
        bg  = colors.HexColor("#0A2E3A") if is_front else (colors.HexColor("#0A2E1A") if is_rear else C_CARD)
        lbl = "front" if is_front else ("rear" if is_rear else "")
        lbl_row.append(P(f"<b>{lbl}</b>", S("_", fontName="Helvetica-Bold", fontSize=7.5, textColor=fg, alignment=TA_CENTER)))
        val_row.append(P(f"<b>{v}</b>",   S("_", fontName="Courier-Bold",   fontSize=11, textColor=fg, alignment=TA_CENTER)))

    tbl = Table([lbl_row, val_row], colWidths=[col_w]*n, style=TableStyle([
        ("BOX",(0,1),(-1,1),1,C_BORDER),("INNERGRID",(0,1),(-1,1),0.5,C_BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
        ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2)]))
    return [tbl, Spacer(1,4)]

def mono_stack_vis(stack_vals, current=None, action="", result_map=None, arr=None, arr_highlight=None):
    """Show monotonic stack state with current element and action."""
    rows = []
    # Array context row
    if arr is not None:
        hl = arr_highlight or []
        arr_cells = []
        for i, v in enumerate(arr):
            fg = C_YELLOW if i in hl else C_MUTED
            arr_cells.append(P(str(v), S("_", fontName="Courier-Bold", fontSize=9, textColor=fg, alignment=TA_CENTER)))
        arr_tbl = Table([arr_cells], colWidths=[28]*len(arr), style=TableStyle([
            ("BOX",(0,0),(-1,-1),0.5,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
            ("BACKGROUND",(0,0),(-1,-1),C_DARK2),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        rows.append([arr_tbl, P("", sCaption), P("", sCaption)])

    # Stack row
    if stack_vals:
        s_cells = [P(str(v), S("_", fontName="Courier-Bold", fontSize=10,
            textColor=C_ACCENT, alignment=TA_CENTER)) for v in stack_vals]
        s_tbl = Table([s_cells], colWidths=[30]*len(stack_vals), style=TableStyle([
            ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0A1E3A")),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        stack_label = P("stack →", S("_", fontName="Helvetica", fontSize=8, textColor=C_MUTED))
    else:
        s_tbl = P("stack: []", S("_", fontName="Courier", fontSize=9, textColor=C_MUTED))
        stack_label = P("", sCaption)

    curr_p = P(f"curr={current}" if current is not None else "",
        S("_", fontName="Courier-Bold", fontSize=9, textColor=C_YELLOW))
    act_p  = P(action, S("_", fontName="Helvetica", fontSize=9, textColor=C_GREEN))

    tbl = Table([[stack_label, s_tbl, curr_p, act_p]],
        colWidths=[50, min(len(stack_vals)*30+10 if stack_vals else 60, 200), 70, CW-50-min(len(stack_vals)*30+10 if stack_vals else 60, 200)-70],
        style=TableStyle([
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LEFTPADDING",(0,0),(-1,-1),0)]))
    return [tbl, Spacer(1,3)]

# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.45*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),("ROWHEIGHT",(0,0),(-1,-1),6)])))
story.append(Spacer(1, 0.3*inch))
story.append(P("STACK &amp; QUEUE PATTERNS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("State Tracking · Processing Order · Monotonic Structures · BFS", sAuthor))
story.append(Spacer(1, 0.2*inch))

story.append(Table([[P("<b>What You Will Master</b>",
    S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· Stack (LIFO) and Queue (FIFO): O(1) operations and structural guarantees\n"
       "· Monotonic Stack: Next Greater/Smaller Element in O(n) vs O(n²)\n"
       "· Monotonic Deque: Sliding Window Maximum in O(n)\n"
       "· Expression Evaluation: Parentheses matching, calculator-style parsing\n"
       "· BFS with Queue: Level-order traversal and shortest-path on unweighted graphs\n"
       "· Queue from Two Stacks (and vice versa): amortised O(1) analysis\n"
       "· Circular Queue: memory-efficient fixed-capacity ring buffer\n"
       "· Stack vs Queue vs Deque vs DFS vs BFS decision framework\n"
       "· Pitfalls: underflow, overflow, deque vs list performance, empty-check order\n"
       "· 25+ categorized LeetCode problems with pattern labels and key insights",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))]],
    colWidths=[CW], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.3*inch))

cx = [
    [th("Operation"),       th("Stack"),    th("Queue"),   th("Array List"),   th("deque")],
    [td("Push / Enqueue",C_BODY), td("O(1)",C_GREEN), td("O(1)",C_GREEN),  td("O(1) amort.",C_GREEN), td("O(1)",C_GREEN)],
    [td("Pop / Dequeue", C_BODY), td("O(1)",C_GREEN), td("O(1)",C_GREEN),  td("O(n) front / O(1) rear",C_YELLOW), td("O(1) both ends",C_GREEN)],
    [td("Peek / Front",  C_BODY), td("O(1)",C_GREEN), td("O(1)",C_GREEN),  td("O(1)",C_GREEN),  td("O(1)",C_GREEN)],
    [td("Access middle", C_BODY), td("O(n)",C_RED),   td("O(n)",C_RED),    td("O(1)",C_GREEN),  td("O(n)",C_RED)],
]
story.append(Table(cx, colWidths=[120,70,70,130,90], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_BG),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD,C_DARK2]),
    ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ("LEFTPADDING",(0,0),(-1,-1),8)])))
story.append(Spacer(1, 0.32*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",["Stack (LIFO) Deep Dive","Queue (FIFO) Deep Dive","Why Not Just Use an Array?"]),
    ("02","Monotonic Stack (The Powerhouse)",["Increasing vs Decreasing Stack","Next Greater Element","Reducing O(n²) to O(n)"]),
    ("03","Monotonic Deque Pattern",["Deque Structure & Operations","Sliding Window Maximum O(n)","Monotonic Deque Template"]),
    ("04","Expression Evaluation & Parsing",["Parentheses Matching","Postfix / RPN Evaluation","Calculator-Style Problems"]),
    ("05","BFS Foundations with Queue",["Level-Order Tree Traversal","Shortest Path on Unweighted Graph","Multi-Source BFS"]),
    ("06","Implementation Strategies",["Queue from Two Stacks","Stack from Two Queues","Circular Queue (Ring Buffer)"]),
    ("07","Comparison & Decision Making",["Stack vs Queue vs Deque","DFS vs BFS","Decision Flowchart"]),
    ("08","Problem Roadmap",["Easy Problems","Medium Problems","Hard Problems"]),
    ("09","Common Pitfalls & Edge Cases",["Underflow vs Overflow","list vs deque Performance","Empty-Check Before Access"]),
]
for num, title, subs in toc:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1,3))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 1 — CORE PHILOSOPHY
# ════════════════════════════════════════════════════════
story += section_divider(1, "The Core Philosophy")

story.append(P("<b>Stack: Last In, First Out (LIFO)</b>", sH2))
story.append(P(
    "A <b>stack</b> is a linear data structure where insertions and removals "
    "happen only at one end — the <b>top</b>. The last element pushed is the "
    "first to be popped. Think of a stack of plates: you always add and remove "
    "from the top. This LIFO order is not a constraint — it is a deliberate "
    "<i>state-tracking guarantee</i> that algorithms exploit.",
    sBody))

# Visual: stack states
story.append(P("State evolution: push(3), push(7), push(2), pop()", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=4)))
stack_states = [
    ([], "Initial"),
    ([3], "push(3)"),
    ([3,7], "push(7)"),
    ([3,7,2], "push(2)"),
    ([3,7], "pop() → 2"),
]
state_cells = []
label_cells = []
for items, lbl in stack_states:
    n = max(len(items), 1)
    item_rows = []
    for i, v in enumerate(reversed(items)):
        is_top = (i == 0)
        fg = C_ACCENT if is_top else C_BODY
        bg = colors.HexColor("#0A2E3A") if is_top else C_CARD
        item_rows.append([P(f"<b>{v}</b>", S("_", fontName="Courier-Bold", fontSize=10,
            textColor=fg, alignment=TA_CENTER))])
    if not items:
        item_rows = [[P("—", S("_", fontName="Courier", fontSize=10, textColor=C_MUTED, alignment=TA_CENTER))]]
    box = Table(item_rows, colWidths=[45], style=TableStyle([
        ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    state_cells.append(box)
    label_cells.append(P(lbl, S("_", fontName="Helvetica", fontSize=8.5, textColor=C_YELLOW, alignment=TA_CENTER)))

col_w_s = int(CW / 5)
story.append(Table([state_cells, label_cells], colWidths=[col_w_s]*5, style=TableStyle([
    ("VALIGN",(0,0),(-1,-1),"BOTTOM"),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("ALIGN",(0,0),(-1,-1),"CENTER")])))
story.append(Spacer(1,6))

story += code_block([
    "## ─── Stack in Python ───────────────────────────────────────────",
    "stack = []              ## Python list as stack",
    "stack.append(val)       ## push  — O(1) amortised",
    "top   = stack[-1]       ## peek  — O(1), no removal",
    "val   = stack.pop()     ## pop   — O(1) amortised",
    "empty = len(stack) == 0 ## empty check — always do before pop/peek",
    "",
    "## Key stack API summary:",
    "## push(x):    place x on top",
    "## pop():      remove and return top",
    "## peek()/top: return top without removing (stack[-1] in Python)",
    "## isEmpty():  return True if no elements",
])

story.append(P("<b>Queue: First In, First Out (FIFO)</b>", sH2))
story.append(P(
    "A <b>queue</b> processes elements in the order they arrive. "
    "Insertions (<b>enqueue</b>) happen at the <b>rear</b>; "
    "removals (<b>dequeue</b>) happen at the <b>front</b>. "
    "Think of a checkout line: the first customer to join is served first. "
    "FIFO order is the foundation of BFS and any fair-scheduling system.",
    sBody))

story.append(P("State evolution: enqueue(A), enqueue(B), enqueue(C), dequeue()", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=4)))
queue_states = [
    ([], "Initial"),
    (["A"], "enqueue(A)"),
    (["A","B"], "enqueue(B)"),
    (["A","B","C"], "enqueue(C)"),
    (["B","C"], "dequeue() → A"),
]
q_state_cells = []
q_label_cells = []
for items, lbl in queue_states:
    if items:
        q_cells = [P(f"<b>{v}</b>", S("_", fontName="Courier-Bold", fontSize=10,
            textColor=C_ACCENT if i==0 else (C_GREEN if i==len(items)-1 else C_BODY),
            alignment=TA_CENTER)) for i,v in enumerate(items)]
        box = Table([q_cells], colWidths=[30]*len(items), style=TableStyle([
            ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
            ("BACKGROUND",(0,0),(-1,-1),C_CARD),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    else:
        box = Table([[P("—", S("_", fontName="Courier", fontSize=10, textColor=C_MUTED, alignment=TA_CENTER))]],
            colWidths=[30], style=TableStyle([("BOX",(0,0),(-1,-1),1,C_BORDER),("BACKGROUND",(0,0),(-1,-1),C_CARD),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    q_state_cells.append(box)
    q_label_cells.append(P(lbl, S("_", fontName="Helvetica", fontSize=8.5, textColor=C_YELLOW, alignment=TA_CENTER)))

story.append(Table([q_state_cells, q_label_cells], colWidths=[col_w_s]*5, style=TableStyle([
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("ALIGN",(0,0),(-1,-1),"CENTER")])))
story.append(Spacer(1,6))

story += code_block([
    "## ─── Queue in Python — use deque, NOT list ────────────────────",
    "from collections import deque",
    "queue = deque()",
    "queue.append(val)       ## enqueue (add to rear)  — O(1)",
    "val = queue.popleft()   ## dequeue (remove front) — O(1)",
    "front = queue[0]        ## peek front             — O(1)",
    "",
    "## WHY NOT list.pop(0)?",
    "## list.pop(0) shifts ALL remaining elements left → O(n)!",
    "## deque.popleft() is O(1) — it uses a doubly-linked block structure.",
    "## For n=100,000 dequeue operations: list = 10 billion ops, deque = 100,000 ops.",
])

story.append(P("<b>Why Not Just Use an Array for Everything?</b>", sH2))

why_data = [
    [th("Scenario"),                            th("Array"),              th("Stack / Queue")],
    [td("Undo/redo, call stack, DFS",C_BODY),   td("No LIFO guarantee — wrong element may be accessed",C_RED),
     td("Stack enforces LIFO; no accidental mid-access",C_GREEN)],
    [td("BFS, job scheduling, event loop",C_BODY),td("pop(0) is O(n) — shifts all elements",C_RED),
     td("deque.popleft() is O(1)",C_GREEN)],
    [td("Monotonic tracking (NGE)",C_BODY),     td("Requires O(n²) nested scan to find next greater",C_RED),
     td("Monotonic stack finds NGE for all elements in O(n)",C_GREEN)],
    [td("Semantic clarity",C_BODY),             td("arr[-1], arr.pop(0) — intent is implicit",C_MUTED),
     td("push/pop/enqueue/dequeue — intent is explicit",C_GREEN)],
]
story.append(std_table(why_data, [155, 165, 160]))
story.append(Spacer(1,8))

story += callout(
    "Choose Stack or Queue not for performance — Python lists are fast — but for "
    "<b>semantic guarantees</b>. A stack tells every reader of your code: "
    "'only the most recent element is accessible.' This constraint IS the algorithm.",
    C_ACCENT, icon="💡")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2 — MONOTONIC STACK
# ════════════════════════════════════════════════════════
story += section_divider(2, "Monotonic Stack (The Powerhouse)")

story.append(P("<b>What is a Monotonic Stack?</b>", sH2))
story.append(P(
    "A <b>monotonic stack</b> maintains elements in either strictly increasing "
    "or strictly decreasing order from bottom to top. When a new element "
    "violates the order, elements are <b>popped until the order is restored</b>. "
    "This controlled popping is when answers are recorded — the popping condition "
    "directly encodes what each element has been 'waiting for'.",
    sBody))

mono_types = [
    [th("Type"),              th("Stack Order"),          th("Pop Condition"),               th("What It Solves")],
    [td("Mono Increasing",C_ACCENT),  td("Bottom→Top: small→large",C_BODY),
     td("Pop when new element is SMALLER",C_BODY),  td("Next Smaller Element, stock span",C_MUTED)],
    [td("Mono Decreasing",C_ACCENT2), td("Bottom→Top: large→small",C_BODY),
     td("Pop when new element is LARGER",C_BODY),   td("Next Greater Element, max histogram",C_MUTED)],
]
story.append(std_table(mono_types, [110, 155, 155, 60]))
story.append(Spacer(1,8))

story += callout(
    "Memory hook: 'Decreasing stack for next GREATER element' — "
    "you pop when something GREATER arrives, so the popped elements have "
    "found their Next Greater Element (the thing that kicked them out).",
    C_ACCENT2, icon="🧠")

story.append(P("<b>Next Greater Element: O(n²) → O(n)</b>", sH2))
story.append(P(
    "For each element in arr, find the next element to its right that is "
    "strictly greater. Brute force scans rightward for each element: O(n²). "
    "The monotonic decreasing stack processes every element exactly twice "
    "(once pushed, once popped): O(n) total.",
    sBody))

story += code_block([
    "## ─── Next Greater Element — O(n) Monotonic Stack ───────────────",
    "def next_greater_element(arr):",
    "    n      = len(arr)",
    "    result = [-1] * n          ## default: no greater element = -1",
    "    stack  = []                ## monotonic decreasing stack (stores INDICES)",
    "",
    "    for i in range(n):",
    "        ## While stack is non-empty AND current element is greater than",
    "        ## the element at the top of the stack:",
    "        while stack and arr[i] > arr[stack[-1]]:",
    "            idx        = stack.pop()    ## this element found its NGE!",
    "            result[idx] = arr[i]        ## arr[i] is its Next Greater Element",
    "",
    "        stack.append(i)        ## push current index",
    "",
    "    ## Remaining elements in stack have no NGE → result stays -1",
    "    return result",
    "",
    "## ─── Why store INDICES (not values)? ───────────────────────────",
    "## Storing index lets us update result[idx] directly.",
    "## We can always get the value back: arr[stack[-1]]",
])

story.append(P("<b>Step-by-Step Trace: arr = [2, 1, 5, 3, 4]</b>", sH3))
arr_nge = [2,1,5,3,4]

nge_trace = [
    ([],  0, "push idx 0 (val=2)"),
    ([0], 1, "arr[1]=1 < arr[top=0]=2 → just push idx 1"),
    ([0,1], 2, "arr[2]=5 > arr[top=1]=1 → POP 1: result[1]=5. Then 5>arr[0]=2 → POP 0: result[0]=5. Push 2"),
    ([2], 3, "arr[3]=3 < arr[top=2]=5 → just push idx 3"),
    ([2,3], 4, "arr[4]=4 > arr[top=3]=3 → POP 3: result[3]=4. 4 < arr[2]=5 → push idx 4"),
    ([2,4], None, "Loop ends. Stack [2,4] → result[2]=result[4]=-1"),
]
nge_data = [[th("Stack (indices)"), th("i"), th("arr[i]"), th("Action"), th("result so far")]]
result_state = [-1]*5
for stack_s, i_s, action in nge_trace:
    # simulate result
    if "POP" in action:
        pass  # already described in action text
    i_txt  = str(i_s) if i_s is not None else "—"
    v_txt  = str(arr_nge[i_s]) if i_s is not None else "—"
    stk_txt = str(stack_s)
    nge_data.append([
        tdc(stk_txt, C_ACCENT),
        tdc(i_txt,   C_YELLOW),
        tdc(v_txt,   C_BODY),
        td(action,   C_BODY, sz=8.5),
        tdc("see trace", C_MUTED),
    ])
story.append(std_table(nge_data, [90, 30, 50, 215, 75]))
story.append(P("Final result: [5, 5, -1, 4, -1] — each element's Next Greater Element", sCaption))
story.append(Spacer(1,8))

story.append(P("<b>Why O(n)? The Amortised Argument</b>", sH3))
story.append(P(
    "Each index is pushed onto the stack exactly <b>once</b> and popped "
    "at most <b>once</b>. Total push + pop operations across the entire loop "
    "= at most 2n. The while loop may run multiple times in a single iteration, "
    "but those iterations 'use up' previous pushes. Charge each pop to "
    "the original push — total cost O(n) amortised.",
    sBody))

story.append(P("<b>Variations of the Monotonic Stack Pattern</b>", sH3))
vars_data = [
    [th("Problem Variant"),           th("Stack Type"),        th("Pop When"),          th("Record At")],
    [td("Next Greater Element",  C_BODY), td("Decreasing",C_ACCENT2), tdc("arr[i] > arr[top]"),  td("pop time",  C_MUTED)],
    [td("Next Smaller Element",  C_BODY), td("Increasing",C_ACCENT),  tdc("arr[i] < arr[top]"),  td("pop time",  C_MUTED)],
    [td("Previous Greater",      C_BODY), td("Decreasing",C_ACCENT2), tdc("arr[i] >= arr[top]"), td("push time (stack top = prev greater)", C_MUTED)],
    [td("Largest Rectangle (Histogram)",C_BODY),td("Increasing",C_ACCENT),tdc("arr[i] < arr[top]"),  td("pop time (width = i - stack[-1] - 1)",C_MUTED)],
    [td("Trapping Rain Water",   C_BODY), td("Decreasing",C_ACCENT2), tdc("arr[i] > arr[top]"),  td("pop time (area = width × height_diff)",C_MUTED)],
]
story.append(std_table(vars_data, [145, 85, 115, 135]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3 — MONOTONIC DEQUE
# ════════════════════════════════════════════════════════
story += section_divider(3, "Monotonic Deque Pattern")

story.append(P("<b>The Deque Data Structure</b>", sH2))
story.append(P(
    "A <b>deque</b> (double-ended queue) supports O(1) insertions and removals "
    "at <b>both</b> the front and the rear. This bidirectional access is what "
    "enables the Monotonic Deque — we push new elements at the rear "
    "and evict expired elements from the front, while maintaining monotonic "
    "order by trimming the rear.",
    sBody))

story += code_block([
    "## ─── deque operations ──────────────────────────────────────────",
    "from collections import deque",
    "dq = deque()",
    "",
    "dq.append(x)       ## add to REAR   — O(1)  (used for new elements)",
    "dq.appendleft(x)   ## add to FRONT  — O(1)  (rarely used in mono deque)",
    "dq.pop()           ## remove REAR   — O(1)  (trim: remove smaller rear elements)",
    "dq.popleft()       ## remove FRONT  — O(1)  (evict: remove expired window elements)",
    "dq[-1]             ## peek REAR     — O(1)",
    "dq[0]              ## peek FRONT    — O(1)  (always the current window's max/min)",
])

story.append(P("<b>Sliding Window Maximum: O(nk) → O(n)</b>", sH2))
story.append(P(
    "For a sliding window of size k, find the maximum element in each position. "
    "Brute force calls max() on every window: O(nk). The Monotonic Decreasing "
    "Deque maintains the maximum at the front in O(1) per step.",
    sBody))

story.append(P("Two invariants enforced at every step:", sH3))
inv_data = [
    [th("Invariant"),                                       th("Enforcement"),                       th("Why")],
    [td("Front is always the window maximum",     C_BODY),  tdc("if dq[0] <= i-k: popleft()"),       td("Expired indices cannot be the max",C_MUTED)],
    [td("Deque is monotone decreasing (indices)", C_BODY),  tdc("while dq and arr[dq[-1]] <= arr[i]: pop()"),
     td("A smaller element behind i can never be future max while i is in window",C_MUTED)],
]
story.append(std_table(inv_data, [155, 205, 120]))
story.append(Spacer(1,8))

story += code_block([
    "## ─── Sliding Window Maximum — O(n) with Monotonic Deque ────────",
    "from collections import deque",
    "",
    "def sliding_window_max(arr, k):",
    "    dq     = deque()   ## stores INDICES; arr[dq[0]] is always window max",
    "    result = []",
    "",
    "    for i in range(len(arr)):",
    "        ## ── Invariant 1: evict expired front index ───────────────",
    "        while dq and dq[0] <= i - k:",
    "            dq.popleft()",
    "",
    "        ## ── Invariant 2: maintain decreasing order ───────────────",
    "        while dq and arr[dq[-1]] <= arr[i]:",
    "            dq.pop()            ## smaller elements can never be max",
    "",
    "        dq.append(i)            ## add current index to rear",
    "",
    "        ## Record max once the first full window is formed",
    "        if i >= k - 1:",
    "            result.append(arr[dq[0]])   ## front = current window max",
    "",
    "    return result",
])

story.append(P("<b>Visual Trace: arr=[3,1,3,5,2,4], k=3</b>", sH3))
sw_trace = [
    (0, 3,  [0],    "—",   "push 0. Window not full yet."),
    (1, 1,  [0,1],  "—",   "1<3, push 1. Not full yet."),
    (2, 3,  [0,2],  "3",   "3<=3, pop 1; push 2. Full! max=arr[0]=3"),
    (3, 5,  [3],    "5",   "5>3, pop 0; pop 2; push 3. max=arr[3]=5"),
    (4, 2,  [3,4],  "5",   "2<5, push 4. max=arr[3]=5"),
    (5, 4,  [3,5],  "5",   "4>2, pop 4; 4<5, push 5. max=arr[3]=5"),
]
sw_data = [[th("i"), th("arr[i]"), th("deque (idx)"), th("output"), th("action")]]
for i_v, val, dq_v, out, act in sw_trace:
    out_c = C_GREEN if out != "—" else C_MUTED
    sw_data.append([
        tdc(str(i_v), C_ACCENT), tdc(str(val), C_HEADING),
        tdc(str(dq_v), C_ACCENT2), td(out, out_c),
        td(act, C_MUTED, sz=8.5)])
story.append(std_table(sw_data, [28,50,80,55,267]))
story.append(P("Result: [3, 5, 5, 5] — note all steps are O(1) amortised", sCaption))
story.append(Spacer(1,8))

story += callout(
    "The Monotonic Deque is the Monotonic Stack's cousin: same invariant-maintenance "
    "idea, but with an expiry condition at the front. Stack = remember all relevant "
    "history. Deque = remember relevant history within a fixed window.",
    C_TEAL, icon="🔁")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4 — EXPRESSION EVALUATION
# ════════════════════════════════════════════════════════
story += section_divider(4, "Expression Evaluation & Parsing")

story.append(P("<b>Parentheses Matching</b>", sH2))
story.append(P(
    "The stack is the natural structure for matching brackets because a "
    "closing bracket always matches the <i>most recently opened</i> "
    "unmatched bracket — which is precisely what sits on the stack's top. "
    "This is the LIFO guarantee applied directly.",
    sBody))

story += code_block([
    "## ─── Valid Parentheses ─────────────────────────────────────────",
    "def is_valid(s):",
    "    stack = []",
    "    pairs = {')':'(', ']':'[', '}':'{'}   ## closing → expected opening",
    "",
    "    for ch in s:",
    "        if ch in '([{':",
    "            stack.append(ch)         ## push opening bracket",
    "        else:                        ## it's a closing bracket",
    "            if not stack:            ## nothing to match — invalid",
    "                return False",
    "            if stack[-1] != pairs[ch]:  ## top doesn't match — invalid",
    "                return False",
    "            stack.pop()              ## matched pair — remove from stack",
    "",
    "    return len(stack) == 0           ## valid iff all brackets matched",
    "",
    "## ─── Trace: s = '([)]'  → False ───────────────────────────────",
    "## push '(' → stack=['(']",
    "## push '[' → stack=['(','[']",
    "## see ')' → top is '[', pairs[')']='(' → mismatch → return False",
])

story.append(P("<b>Postfix / RPN Evaluation</b>", sH2))
story.append(P(
    "Postfix notation (Reverse Polish Notation) eliminates parentheses "
    "by placing operators after their operands: 3 4 + = 7. "
    "A stack evaluates any postfix expression in a single O(n) pass: "
    "push numbers, and on each operator pop two operands, apply, push result.",
    sBody))

story += code_block([
    "## ─── Evaluate Reverse Polish Notation ──────────────────────────",
    "def eval_rpn(tokens):",
    "    stack = []",
    "    ops   = {",
    "        '+': lambda a, b: a + b,",
    "        '-': lambda a, b: a - b,",
    "        '*': lambda a, b: a * b,",
    "        '/': lambda a, b: int(a / b),  ## truncate toward zero",
    "    }",
    "    for token in tokens:",
    "        if token in ops:",
    "            b = stack.pop()      ## second operand (pushed later)",
    "            a = stack.pop()      ## first operand  (pushed earlier)",
    "            stack.append(ops[token](a, b))",
    "        else:",
    "            stack.append(int(token))   ## push number",
    "",
    "    return stack[0]    ## final result",
    "",
    "## ─── Trace: ['3','4','+','2','*'] = (3+4)*2 = 14 ───────────────",
    "## push 3 → [3]  | push 4 → [3,4]  | '+' → pop 4,3 → push 7 → [7]",
    "## push 2 → [7,2] | '*' → pop 2,7 → push 14 → [14]  → return 14",
])

story.append(P("<b>Calculator-Style Problems (Infix with +/- and */÷)</b>", sH3))
story.append(P(
    "For expressions like '3 + 2 * 4 - 1' respecting operator precedence, "
    "the stack stores 'signed terms'. Parse left-to-right, tracking the "
    "current sign and handling * and / immediately while deferring + and - "
    "until a lower-precedence boundary is reached.",
    sBody))
story += code_block([
    "## ─── Basic Calculator II (+, -, *, /) ──────────────────────────",
    "def calculate(s):",
    "    stack, num, sign = [], 0, '+'",
    "    s = s.replace(' ', '') + '+'    ## sentinel '+' flushes last term",
    "",
    "    for ch in s:",
    "        if ch.isdigit():",
    "            num = num * 10 + int(ch)",
    "        elif ch in '+-*/':",
    "            if   sign == '+': stack.append(num)",
    "            elif sign == '-': stack.append(-num)",
    "            elif sign == '*': stack.append(stack.pop() * num)",
    "            elif sign == '/': stack.append(int(stack.pop() / num))",
    "            sign = ch; num = 0",
    "",
    "    return sum(stack)",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5 — BFS FOUNDATIONS
# ════════════════════════════════════════════════════════
story += section_divider(5, "BFS Foundations with Queue")

story.append(P("<b>The Queue's Role in BFS</b>", sH2))
story.append(P(
    "Breadth-First Search processes nodes <b>level by level</b>: "
    "all nodes at distance d are visited before any at distance d+1. "
    "A queue enforces this by ensuring nodes are processed in the "
    "order they were discovered — FIFO guarantees that the oldest "
    "(closest) node is always processed next.",
    sBody))

story += code_block([
    "## ─── BFS Template ──────────────────────────────────────────────",
    "from collections import deque",
    "",
    "def bfs(start, goal, graph):",
    "    queue   = deque([start])",
    "    visited = {start}",
    "    dist    = {start: 0}           ## distance from start",
    "",
    "    while queue:",
    "        node = queue.popleft()     ## process oldest/closest node first",
    "",
    "        if node == goal:",
    "            return dist[node]      ## shortest path found",
    "",
    "        for neighbour in graph[node]:",
    "            if neighbour not in visited:",
    "                visited.add(neighbour)",
    "                dist[neighbour] = dist[node] + 1",
    "                queue.append(neighbour)",
    "",
    "    return -1   ## goal not reachable",
])

story.append(P("<b>Level-Order Tree Traversal</b>", sH2))
story.append(P(
    "Process a binary tree level by level. The queue size at the "
    "<i>start</i> of each iteration tells you exactly how many nodes "
    "belong to the current level — process exactly that many, then "
    "the remaining queue contains only the next level.",
    sBody))
story += code_block([
    "## ─── Level-Order Traversal ─────────────────────────────────────",
    "def level_order(root):",
    "    if not root: return []",
    "    queue  = deque([root])",
    "    result = []",
    "",
    "    while queue:",
    "        level_size = len(queue)    ## snapshot: nodes at current level",
    "        level = []",
    "",
    "        for _ in range(level_size):    ## process EXACTLY this many nodes",
    "            node = queue.popleft()",
    "            level.append(node.val)",
    "            if node.left:  queue.append(node.left)",
    "            if node.right: queue.append(node.right)",
    "",
    "        result.append(level)",
    "",
    "    return result",
    "## Time: O(n) — every node enqueued and dequeued exactly once",
    "## Space: O(w) where w = max width of tree (O(n) worst case for full tree)",
])

story.append(P("<b>Multi-Source BFS</b>", sH3))
story.append(P(
    "When the problem has <i>multiple</i> starting points (e.g., all '1' cells "
    "spreading outward on a grid, all 'rotten oranges' infecting simultaneously), "
    "seed the queue with ALL starting points at once before the first iteration. "
    "This naturally computes the distance from the nearest source to each cell.",
    sBody))
story += code_block([
    "## ─── Multi-Source BFS Template ─────────────────────────────────",
    "def multi_source_bfs(grid):",
    "    rows, cols = len(grid), len(grid[0])",
    "    queue = deque()",
    "",
    "    ## Seed with ALL sources simultaneously",
    "    for r in range(rows):",
    "        for c in range(cols):",
    "            if grid[r][c] == SOURCE:     ## e.g., rotten orange, gate, etc.",
    "                queue.append((r, c, 0))  ## (row, col, distance)",
    "",
    "    directions = [(0,1),(0,-1),(1,0),(-1,0)]  ## 4-directional",
    "    while queue:",
    "        r, c, dist = queue.popleft()",
    "        for dr, dc in directions:",
    "            nr, nc = r+dr, c+dc",
    "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == TARGET:",
    "                grid[nr][nc] = VISITED    ## mark to avoid revisit",
    "                queue.append((nr, nc, dist+1))",
])

story += callout(
    "Key insight: Multi-source BFS is equivalent to adding a virtual 'super-source' "
    "node connected to all real sources with distance 0. The queue starts with all "
    "real sources, so the first dequeue is any source at distance 0 — exactly "
    "as if they all started simultaneously.",
    C_PURPLE, icon="🌐")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6 — IMPLEMENTATION STRATEGIES
# ════════════════════════════════════════════════════════
story += section_divider(6, "Implementation Strategies")

story.append(P("<b>Queue from Two Stacks</b>", sH2))
story.append(P(
    "Simulate a FIFO queue using two LIFO stacks: "
    "<b>inbox</b> (for enqueue) and <b>outbox</b> (for dequeue). "
    "Enqueue always pushes to inbox. Dequeue pops from outbox; "
    "when outbox is empty, transfer all inbox elements to outbox "
    "(which reverses their order — turning LIFO into FIFO).",
    sBody))
story += code_block([
    "## ─── Queue Using Two Stacks ─────────────────────────────────────",
    "class MyQueue:",
    "    def __init__(self):",
    "        self.inbox  = []   ## new elements pushed here",
    "        self.outbox = []   ## elements dequeued from here",
    "",
    "    def enqueue(self, val):        ## always O(1)",
    "        self.inbox.append(val)",
    "",
    "    def dequeue(self):             ## amortised O(1)",
    "        self._transfer_if_needed()",
    "        return self.outbox.pop()",
    "",
    "    def peek(self):                ## amortised O(1)",
    "        self._transfer_if_needed()",
    "        return self.outbox[-1]",
    "",
    "    def _transfer_if_needed(self):",
    "        if not self.outbox:        ## only transfer when outbox is empty",
    "            while self.inbox:",
    "                self.outbox.append(self.inbox.pop())   ## reverses order",
    "",
    "## Amortised O(1): each element is pushed once and popped once total.",
    "## Worst single call: O(n) transfer. Across n operations: O(n) total.",
])

story.append(P("<b>Visual: Queue from Two Stacks (enqueue A,B,C then dequeue twice)</b>", sH3))
twostk_trace = [
    ("enqueue(A)", ["A"], [],    "inbox←[A]"),
    ("enqueue(B)", ["A","B"],[],  "inbox←[A,B]"),
    ("enqueue(C)", ["A","B","C"],[],  "inbox←[A,B,C]"),
    ("dequeue()",  [],    ["C","B","A"], "outbox empty→transfer. outbox←[C,B,A]. pop A"),
    ("dequeue()",  [],    ["C","B"],    "outbox has items. pop B"),
]
tst_data = [[th("Operation"), th("inbox (top→)"), th("outbox (top→)"), th("Action")]]
for op, ib, ob, act in twostk_trace:
    tst_data.append([
        tdc(op, C_YELLOW),
        tdc(str(list(reversed(ib))) if ib else "[]", C_ACCENT),
        tdc(str(list(reversed(ob))) if ob else "[]", C_GREEN),
        td(act, C_MUTED)])
story.append(std_table(tst_data, [90, 120, 150, 120]))
story.append(Spacer(1,8))

story.append(P("<b>Circular Queue (Ring Buffer)</b>", sH2))
story.append(P(
    "A <b>circular queue</b> is a fixed-capacity array where the front and rear "
    "pointers wrap around using modular arithmetic. It eliminates the O(n) shift "
    "of a naive array-based queue while using exactly <i>capacity</i> slots — "
    "no dynamic reallocation. Used in memory-constrained environments, "
    "OS ring buffers, and data stream processing.",
    sBody))
story += code_block([
    "## ─── Circular Queue (Fixed Capacity) ──────────────────────────",
    "class CircularQueue:",
    "    def __init__(self, k):",
    "        self.data  = [None] * k",
    "        self.head  = 0         ## front pointer",
    "        self.tail  = -1        ## rear pointer (points to last inserted)",
    "        self.size  = 0",
    "        self.cap   = k",
    "",
    "    def enqueue(self, val):",
    "        if self.size == self.cap: return False   ## full",
    "        self.tail = (self.tail + 1) % self.cap   ## wrap around",
    "        self.data[self.tail] = val",
    "        self.size += 1",
    "        return True",
    "",
    "    def dequeue(self):",
    "        if self.size == 0: return False          ## empty",
    "        self.head = (self.head + 1) % self.cap   ## wrap around",
    "        self.size -= 1",
    "        return True",
    "",
    "    def front(self):  return self.data[self.head] if self.size else -1",
    "    def rear(self):   return self.data[self.tail] if self.size else -1",
    "    def is_full(self):  return self.size == self.cap",
    "    def is_empty(self): return self.size == 0",
    "",
    "## Key: (idx + 1) % cap wraps index from cap-1 back to 0.",
    "## No shifting, no resizing — exactly O(1) per operation.",
])

story += callout(
    "The critical insight of a circular queue: head and tail are positions, "
    "not pointers to actual first/last elements. size (or a full-flag) "
    "disambiguates the case where head == tail (which means either empty OR full).",
    C_ORANGE, icon="🔄")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7 — COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(7, "Comparison & Decision Making")

story.append(P("<b>Stack vs. Queue vs. Deque</b>", sH2))
sqd_data = [
    [th("Dimension"),       th("Stack"),               th("Queue"),              th("Deque")],
    [td("Access",  C_BODY), td("Top only (LIFO)",C_BODY), td("Front (FIFO)",C_BODY), td("Both ends",C_BODY)],
    [td("Insert",  C_BODY), tdc("push (top)",C_ACCENT),   tdc("enqueue (rear)",C_GREEN), tdc("appendleft / append",C_TEAL)],
    [td("Remove",  C_BODY), tdc("pop (top)",C_ACCENT),    tdc("dequeue (front)",C_GREEN),tdc("popleft / pop",C_TEAL)],
    [td("Python",  C_BODY), tdc("list",C_MUTED),          tdc("deque",C_MUTED),          tdc("deque",C_MUTED)],
    [td("Use for", C_BODY),
     td("DFS, undo/redo, call stack, expression eval, monotonic tracking",C_BODY),
     td("BFS, level-order traversal, job scheduling, FIFO buffer",C_BODY),
     td("Sliding window max/min, queue-from-stacks, palindrome check",C_BODY)],
    [td("Classic problems",C_BODY),
     td("Valid Parentheses, NGE, Histogram, Calculator",C_MUTED),
     td("Binary Tree Level Order, Rotten Oranges, Walls & Gates",C_MUTED),
     td("Sliding Window Max, Max Sliding Window, Monotonic Deque",C_MUTED)],
]
story.append(std_table(sqd_data, [80, 145, 145, 110]))
story.append(Spacer(1,10))

story.append(P("<b>DFS (Stack-based) vs. BFS (Queue-based)</b>", sH2))
db_data = [
    [th("Dimension"),          th("DFS (Stack / Recursion)"),          th("BFS (Queue)")],
    [td("Data structure",C_BODY), td("Stack (implicit via recursion or explicit)",C_BODY), td("Queue (always explicit)",C_BODY)],
    [td("Traversal order",C_BODY),td("Deep first — follows one path to its end",C_BODY), td("Wide first — all nodes at distance d before d+1",C_BODY)],
    [td("Shortest path",C_BODY),  td("❌ NOT guaranteed on unweighted graphs",C_RED),  td("✅ Guaranteed on unweighted graphs",C_GREEN)],
    [td("Memory usage",C_BODY),   td("O(depth) — can be O(n) for skewed trees",C_YELLOW), td("O(width) — can be O(n) for wide trees",C_YELLOW)],
    [td("Cycle detection",C_BODY),td("✅ Natural with visited set",C_GREEN),  td("✅ Natural with visited set",C_GREEN)],
    [td("Find ALL paths",C_BODY), td("✅ Natural with backtracking",C_GREEN), td("⚠️ Requires extra bookkeeping",C_YELLOW)],
    [td("Use when",C_BODY),
     td("Exploring all possibilities, backtracking, topological sort, path existence",C_ACCENT,"Helvetica-Oblique"),
     td("Shortest path (unweighted), level-by-level processing, nearest neighbor",C_GREEN,"Helvetica-Oblique")],
]
story.append(std_table(db_data, [115, 190, 175]))
story.append(Spacer(1,10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1", "Does the problem involve processing order (not just storage)?",  C_ACCENT),
    (" → Most recent first",  "→ Stack (LIFO). DFS, undo, expression eval.", C_ACCENT2),
    (" → Arrival order first","→ Queue (FIFO). BFS, level traversal, scheduling.", C_GREEN),
    ("Q2", "Do you need access at BOTH ends?",                               C_ACCENT),
    (" → YES",  "→ Deque. Sliding window max, palindrome, two-stack queue.", C_TEAL),
    (" → NO",   "→ Use plain Stack or Queue.",                                C_MUTED),
    ("Q3", "Is the problem about 'next greater/smaller' or 'sliding max/min'?", C_ACCENT),
    (" → Next greater/smaller", "→ Monotonic Stack. Process each element once.", C_ORANGE),
    (" → Sliding max/min",      "→ Monotonic Deque with window expiry.",          C_PURPLE),
    ("Q4", "Does the problem ask for shortest path or level-by-level result?", C_ACCENT),
    (" → YES", "→ BFS with Queue. Guarantee shortest path on unweighted graph.", C_GREEN),
    (" → NO",  "→ DFS with Stack or recursion may be simpler.",                  C_MUTED),
]
for label, text, clr in flow:
    bg = C_CARD if not label.startswith(" ") else C_DARK2
    story.append(Table([[
        P(f"<b>{label}</b>", S("_", fontName="Courier-Bold", fontSize=9, textColor=clr)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[100, CW-100], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1,8))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8 — PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(8, "LeetCode Problem Roadmap")
story.append(P("Solve in sequence — each problem introduces one new stack or queue technique.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("20",  C_GREEN), td("Valid Parentheses",              C_BODY), td("Stack: brackets", C_ACCENT),
     td("Push open; on close, check top matches. Empty at end = valid.", C_MUTED)],
    [tdc("225", C_GREEN), td("Implement Stack using Queues",   C_BODY), td("Two Queues",       C_ACCENT2),
     td("Re-enqueue n-1 elements after each push to keep newest at front.", C_MUTED)],
    [tdc("232", C_GREEN), td("Implement Queue using Stacks",   C_BODY), td("Two Stacks",       C_ACCENT2),
     td("inbox/outbox; transfer only when outbox empty. Amortised O(1).", C_MUTED)],
    [tdc("496", C_GREEN), td("Next Greater Element I",         C_BODY), td("Mono Stack",       C_ORANGE),
     td("Process nums2 with mono stack; store NGE in map; query for nums1.", C_MUTED)],
    [tdc("1021",C_GREEN), td("Remove Outermost Parentheses",   C_BODY), td("Stack counter",    C_TEAL),
     td("Track depth; include chars only when depth > 0 after open.", C_MUTED)],
    [tdc("155", C_GREEN), td("Min Stack",                      C_BODY), td("Aux min stack",    C_ACCENT),
     td("Parallel min_stack; push current min alongside each element.", C_MUTED)],
]
story.append(std_table(easy_data, [38, 200, 110, 132]))
story.append(Spacer(1,10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("150", C_YELLOW), td("Evaluate Reverse Polish Notation", C_BODY), td("Stack: RPN",         C_ACCENT),
     td("Nums push; ops pop two, compute, push result.", C_MUTED)],
    [tdc("739", C_YELLOW), td("Daily Temperatures",               C_BODY), td("Mono Stack (dec.)",  C_ORANGE),
     td("Store indices; pop when warmer day found; result[idx]=i-idx.", C_MUTED)],
    [tdc("853", C_YELLOW), td("Car Fleet",                        C_BODY), td("Mono Stack",         C_ORANGE),
     td("Sort by position; stack times; pop when fleet catches fleet ahead.", C_MUTED)],
    [tdc("22",  C_YELLOW), td("Generate Parentheses",             C_BODY), td("Backtracking/Stack", C_ACCENT2),
     td("Recurse with open/close counts; add ')' only when close < open.", C_MUTED)],
    [tdc("394", C_YELLOW), td("Decode String",                    C_BODY), td("Two Stacks",         C_ACCENT),
     td("count_stack and str_stack; unwind on ']'.", C_MUTED)],
    [tdc("862", C_YELLOW), td("Shortest Subarray with Sum >= K",  C_BODY), td("Mono Deque+Prefix",  C_TEAL),
     td("Monotonic deque over prefix sums; pop front when constraint met.", C_MUTED)],
    [tdc("239", C_YELLOW), td("Sliding Window Maximum",           C_BODY), td("Mono Deque",         C_TEAL),
     td("Decreasing deque of indices; front=max; evict expired; pop smaller rear.", C_MUTED)],
    [tdc("622", C_YELLOW), td("Design Circular Queue",            C_BODY), td("Ring Buffer",        C_PURPLE),
     td("head/tail/size with (ptr+1)%cap modular arithmetic.", C_MUTED)],
    [tdc("102", C_YELLOW), td("Binary Tree Level Order Traversal",C_BODY), td("BFS Queue",          C_GREEN),
     td("Snapshot len(queue) at start of each level; process exactly that many.", C_MUTED)],
    [tdc("994", C_YELLOW), td("Rotting Oranges",                  C_BODY), td("Multi-Source BFS",   C_GREEN),
     td("Seed queue with all rotten; BFS spreads. Count minutes = levels.", C_MUTED)],
]
story.append(std_table(med_data, [38, 195, 120, 127]))
story.append(Spacer(1,10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("84",  C_RED), td("Largest Rectangle in Histogram",    C_BODY), td("Mono Stack (inc.)",   C_ORANGE),
     td("Pop when shorter bar; width = i - stack[-1] - 1. Sentinel 0 at end.", C_MUTED)],
    [tdc("42",  C_RED), td("Trapping Rain Water",               C_BODY), td("Mono Stack or 2-ptr", C_ORANGE),
     td("Stack: pop on taller right wall; water = width × height_diff.", C_MUTED)],
    [tdc("32",  C_RED), td("Longest Valid Parentheses",         C_BODY), td("Stack of indices",    C_ACCENT),
     td("Push -1 sentinel; push open indices; on ')' pop and measure gap.", C_MUTED)],
    [tdc("316", C_RED), td("Remove Duplicate Letters",          C_BODY), td("Greedy + Mono Stack", C_ORANGE),
     td("Pop larger chars if they appear later; use last_occurrence map.", C_MUTED)],
    [tdc("407", C_RED), td("Trapping Rain Water II (3D)",       C_BODY), td("BFS + Min-Heap",      C_GREEN),
     td("Heap as priority queue; expand from border inward by min boundary.", C_MUTED)],
]
story.append(std_table(hard_data, [38, 185, 120, 137]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9 — PITFALLS
# ════════════════════════════════════════════════════════
story += section_divider(9, "Common Pitfalls & Edge Cases")

story.append(P("<b>Pitfall 1: Stack Underflow — Popping an Empty Stack</b>", sH2))
story.append(P(
    "<b>Underflow</b> occurs when pop() or peek() is called on an empty structure. "
    "In Python, list.pop() on an empty list raises IndexError. "
    "Always guard with an empty check <i>before</i> accessing the top.",
    sBody))
story += code_block([
    "## WRONG — crashes on empty input like s=')(':",
    "## def is_valid(s):",
    "##     stack = []",
    "##     for ch in s:",
    "##         if ch == ')': stack.pop()   ## IndexError if stack empty!",
    "",
    "## CORRECT — check before pop:",
    "def is_valid_safe(s):",
    "    stack = []",
    "    for ch in s:",
    "        if ch == '(':",
    "            stack.append(ch)",
    "        elif ch == ')':",
    "            if not stack: return False   ## guard: underflow check",
    "            stack.pop()",
    "    return len(stack) == 0",
    "",
    "## General rule: ALWAYS check 'if stack:' or 'if not stack: return ...'",
    "## BEFORE calling stack.pop() or stack[-1]",
])

story.append(P("<b>Pitfall 2: Conceptual Stack Overflow</b>", sH3))
story.append(P(
    "In low-level languages and recursive algorithms, a <b>stack overflow</b> "
    "occurs when the call stack exceeds its maximum depth (typically ~1000-10000 "
    "frames in Python). Deep recursion on large inputs crashes with "
    "RecursionError. The fix: convert recursive DFS to iterative DFS with an "
    "explicit stack.",
    sBody))
story += code_block([
    "## ─── Recursive DFS → may overflow for deep trees ───────────────",
    "## def dfs_recursive(node):",
    "##     if not node: return",
    "##     process(node)",
    "##     dfs_recursive(node.left)   ## each call = 1 stack frame",
    "##     dfs_recursive(node.right)  ## depth-10000 tree → overflow",
    "",
    "## ─── Iterative DFS → explicit stack, no recursion limit ─────────",
    "def dfs_iterative(root):",
    "    if not root: return",
    "    stack = [root]",
    "    while stack:",
    "        node = stack.pop()",
    "        process(node)",
    "        if node.right: stack.append(node.right)  ## right first: left processed first",
    "        if node.left:  stack.append(node.left)",
])

story.append(P("<b>Pitfall 3: list.pop(0) vs. deque.popleft()</b>", sH2))
story.append(P(
    "This is the single most common performance bug in Python queue implementations. "
    "The Python list is backed by a dynamic array — removing from the front "
    "requires shifting every remaining element left: O(n). "
    "For n dequeue operations this is O(n²) total. Use <b>collections.deque</b>.",
    sBody))

perf_data = [
    [th("Operation"),                    th("list"),          th("collections.deque"),  th("Impact at n=100k")],
    [td("Append to rear",      C_BODY),  tdc("O(1) amort.",C_GREEN),  tdc("O(1)",C_GREEN),       td("Negligible",C_MUTED)],
    [td("Pop from rear",       C_BODY),  tdc("O(1)",C_GREEN),         tdc("O(1)",C_GREEN),       td("Negligible",C_MUTED)],
    [td("Pop from front",      C_BODY),  tdc("O(n) ← SLOW",C_RED),   tdc("O(1)",C_GREEN),       td("list: ~5 billion ops. deque: 100k ops",C_RED)],
    [td("Append to front",     C_BODY),  tdc("O(n)",C_RED),           tdc("O(1)",C_GREEN),       td("Same problem in reverse",C_RED)],
    [td("Random access arr[i]",C_BODY),  tdc("O(1)",C_GREEN),         tdc("O(n)",C_YELLOW),      td("Deque loses here — use list",C_YELLOW)],
]
story.append(std_table(perf_data, [130, 95, 110, 145]))
story.append(Spacer(1,8))

story.append(P("<b>Pitfall 4: Checking Empty After Instead of Before</b>", sH3))
story += code_block([
    "## WRONG order: access then check (crashes on empty structure)",
    "## val = queue.popleft()   ## IndexError if empty!",
    "## if val: process(val)",
    "",
    "## CORRECT order: check THEN access",
    "if queue:",
    "    val = queue.popleft()  ## safe: we know it's non-empty",
    "    process(val)",
    "",
    "## In BFS loops: the 'while queue' guard handles this automatically.",
    "## The bug surfaces in one-shot dequeues outside a loop.",
    "",
    "## For stack peek:",
    "## WRONG: top = stack[-1]  → IndexError on empty list",
    "## RIGHT: top = stack[-1] if stack else default_value",
])

story.append(P("<b>Pitfall 5: Monotonic Stack — Storing Values vs. Indices</b>", sH3))
story.append(P(
    "Always store <b>indices</b> in a monotonic stack unless the problem "
    "explicitly only needs values. Storing indices lets you compute width "
    "(i - stack[-1] - 1), distances, and update result arrays by position. "
    "You can always recover the value: arr[stack[-1]].",
    sBody))
story += code_block([
    "## RISKY — storing values loses position information:",
    "## stack.append(arr[i])   ## can't compute i - prev_index",
    "",
    "## SAFE — always store indices:",
    "stack.append(i)            ## recover value with arr[stack[-1]]",
    "",
    "## When width calculation is needed (histogram, rain water):",
    "## width = i - stack[-1] - 1   ## from current index to previous unpopped index",
    "## This REQUIRES the index to be stored, not the value.",
])

story += callout(
    "Summary rule: indices in monotonic stacks, values in simple counting/matching stacks. "
    "When in doubt, always store the index — you lose nothing and gain flexibility.",
    C_GREEN, icon="✅")

# Master cheat sheet
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")
story.append(P("One-page reference for all patterns, operations, and decision rules.", sBody))

cheat = [
    [th("Pattern"),                 th("Structure"),              th("Pop/Dequeue When"),              th("Classic Problem")],
    [td("LIFO (Stack)",    C_ACCENT),  tdc("list / deque"),         td("Top accessed in LIFO order",C_BODY),   td("Valid Parens, Min Stack",    C_MUTED)],
    [td("FIFO (Queue)",    C_GREEN),   tdc("deque"),                td("Front dequeued in FIFO order",C_BODY),  td("Level Order BFS",            C_MUTED)],
    [td("Mono Decreasing", C_ACCENT2), tdc("stack of indices"),     td("arr[i] > arr[stack top]",    C_BODY),   td("Next Greater Element",       C_MUTED)],
    [td("Mono Increasing", C_ORANGE),  tdc("stack of indices"),     td("arr[i] < arr[stack top]",    C_BODY),   td("Largest Histogram Rectangle",C_MUTED)],
    [td("Mono Deque",      C_TEAL),    tdc("deque of indices"),     td("Expired OR smaller rear",    C_BODY),   td("Sliding Window Maximum",     C_MUTED)],
    [td("Two-Stack Queue", C_PURPLE),  tdc("inbox + outbox"),       td("Transfer when outbox empty", C_BODY),   td("Queue via Two Stacks",       C_MUTED)],
    [td("Circular Queue",  C_LIME),    tdc("array + head/tail/sz"), td("(head+1)%cap, size--",       C_BODY),   td("Design Circular Queue",      C_MUTED)],
    [td("Multi-Src BFS",   C_ROSE),    tdc("deque"),                td("All sources seeded at once", C_BODY),   td("Rotten Oranges, 01 Matrix",  C_MUTED)],
]
story.append(std_table(cheat, [110, 120, 180, 70]))
story.append(Spacer(1, 10))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
checks = [
    ("Stack or Queue?",      "LIFO = Stack. FIFO / BFS = Queue. Both ends = Deque."),
    ("Monotonic direction?", "NGE / rain water → decreasing. Histogram → increasing. Window max → decreasing deque."),
    ("Store index or value?","Always store index in monotonic stack unless only values matter."),
    ("Empty guard?",         "Check 'if stack:' before every pop(), stack[-1], or queue.popleft()."),
    ("list vs deque?",       "Any popleft / pop-from-front → use deque. Pure stack → list is fine."),
    ("BFS shortest path?",   "Only guaranteed on UNWEIGHTED graphs. Use Dijkstra for weighted."),
    ("Recursive → iterative?","Deep input may cause RecursionError. Convert DFS to explicit stack if depth > 1k."),
    ("Amortised O(1)?",      "Two-stack queue and circular queue are O(1) amortised, not worst-case."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ] {q}</font></b>",
          S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[170, CW-170], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

story.append(Table([[
    P("<b>You now have the complete Stack &amp; Queue mental model.</b><br/><br/>"
      "The core insight is processing order: Stack enforces 'most recent first' "
      "(LIFO), Queue enforces 'arrival order' (FIFO). "
      "The Monotonic Stack and Deque are the advanced forms — they add an "
      "invariant (monotonicity) on top of the basic LIFO/FIFO property, "
      "enabling O(n) solutions to problems that would otherwise require O(n²) scans.<br/><br/>"
      "Recommended path: LC 20 → LC 155 → LC 232 → LC 739 → LC 239 → LC 84 → LC 42. "
      "After these seven problems you will recognise stack and queue patterns "
      "across tree traversals, graph search, expression parsing, and beyond.",
      S("_", fontName="Helvetica", fontSize=10, leading=16, textColor=C_BODY))
]], colWidths=[CW], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),C_CARD),
    ("BOX",(0,0),(-1,-1),2,C_ACCENT),
    ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ("LEFTPADDING",(0,0),(-1,-1),20),("RIGHTPADDING",(0,0),(-1,-1),20)])))

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
    canvas.drawCentredString(PAGE_W/2, 0.35*inch,
        f"Stack & Queue Patterns — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")