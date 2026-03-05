from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus.flowables import Flowable

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

PAGE_W, PAGE_H = letter

doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Linked_List_Patterns_Zero_To_Hero.pdf",
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
sNode    = S("Nd", fontName="Courier-Bold",     fontSize=10, leading=13, textColor=C_HEADING, alignment=TA_CENTER)
sArrow   = S("Ar", fontName="Courier-Bold",     fontSize=12, leading=13, textColor=C_ACCENT,  alignment=TA_CENTER)

P = Paragraph
CW_FULL = CW

# ── Helpers ────────────────────────────────────────────────────────────────────
def code_block(lines, lang="python"):
    hdr = Table([[P(f"<b>{lang}</b>", S("_", fontName="Courier-Bold", fontSize=8, textColor=C_MUTED))]],
        colWidths=[CW], style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0D1929")),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),14)]))
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

# ── Linked list node renderer ──────────────────────────────────────────────────
def node_chain(values, highlight=None, null_end=True, labels=None,
               null_label="None", pointer_labels=None):
    """
    Renders a horizontal linked-list chain as a table.
    values: list of node data values (strings or ints)
    highlight: list of indices to colour differently
    labels: list of label strings shown above each node (e.g. 'head', 'curr')
    pointer_labels: dict {index: label} shown BELOW nodes
    """
    highlight = highlight or []
    n = len(values)
    node_w = 52
    arrow_w = 28
    null_w  = 46

    total_nodes = n
    cols = []
    col_ws = []
    for i in range(n):
        cols.append(i)
        col_ws.append(node_w)
        if i < n - 1:
            cols.append(f"a{i}")
            col_ws.append(arrow_w)
    if null_end:
        cols.append("null")
        col_ws.append(null_w)

    # Row 1: pointer labels above
    top_row = []
    for c in cols:
        if isinstance(c, int):
            lbl = (labels[c] if labels and c < len(labels) else "")
            clr = C_ACCENT if c == 0 else (C_ACCENT2 if c == n-1 else C_GREEN)
            top_row.append(P(f"<b>{lbl}</b>", S("_", fontName="Helvetica-Bold",
                fontSize=7.5, textColor=clr if lbl else C_MUTED, alignment=TA_CENTER)))
        else:
            top_row.append(P("", sCaption))

    # Row 2: node boxes and arrows
    mid_row = []
    for c in cols:
        if isinstance(c, int):
            v = str(values[c])
            bg_key = c in highlight
            fg = C_HEADING if bg_key else C_BODY
            mid_row.append(P(f"<b>{v}</b>", S("_", fontName="Courier-Bold",
                fontSize=11, textColor=fg, alignment=TA_CENTER)))
        elif c == "null":
            mid_row.append(P(f"<b>{null_label}</b>", S("_", fontName="Courier-Bold",
                fontSize=9, textColor=C_MUTED, alignment=TA_CENTER)))
        else:
            mid_row.append(P("→", S("_", fontName="Helvetica-Bold",
                fontSize=14, textColor=C_ACCENT, alignment=TA_CENTER)))

    # Row 3: pointer labels below
    bot_row = []
    ptr_lbl = pointer_labels or {}
    for c in cols:
        if isinstance(c, int) and c in ptr_lbl:
            lbl = ptr_lbl[c]
            clrs = {"slow": C_GREEN, "fast": C_RED, "prev": C_ACCENT,
                    "curr": C_ACCENT2, "next": C_YELLOW, "left": C_ACCENT,
                    "right": C_ACCENT2, "dummy": C_PURPLE, "head": C_ACCENT,
                    "mid": C_GREEN, "p1": C_ORANGE, "p2": C_TEAL,
                    "k-group": C_PURPLE}
            clr = clrs.get(lbl.lower().split("/")[0], C_MUTED)
            bot_row.append(P(f"<b>{lbl}</b>", S("_", fontName="Helvetica-Bold",
                fontSize=7.5, textColor=clr, alignment=TA_CENTER)))
        else:
            bot_row.append(P("", sCaption))

    tbl_data = [top_row, mid_row, bot_row]

    # Build background highlights for mid_row
    style_cmds = [
        ("BACKGROUND",(0,1),(-1,1), C_CARD),
        ("BOX",(0,1),(-1,1), 1, C_BORDER),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
        ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2),
        ("TOPPADDING",(0,2),(-1,2),2),("BOTTOMPADDING",(0,2),(-1,2),2),
    ]
    # highlight node cells
    col_pos = 0
    node_col_positions = []
    for c in cols:
        if isinstance(c, int):
            node_col_positions.append((c, col_pos))
            if c in highlight:
                style_cmds.append(("BACKGROUND",(col_pos,1),(col_pos,1), colors.HexColor("#0A2E3A")))
        col_pos += 1

    # draw node borders
    col_pos = 0
    for c in cols:
        if isinstance(c, int):
            style_cmds.append(("BOX",(col_pos,1),(col_pos,1),1,C_BORDER))
        col_pos += 1

    tbl = Table(tbl_data, colWidths=col_ws, style=TableStyle(style_cmds))
    return [tbl, Spacer(1,6)]

# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),("ROWHEIGHT",(0,0),(-1,-1),6)])))
story.append(Spacer(1, 0.3*inch))
story.append(P("LINKED LIST PATTERNS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Pointer Manipulation · Memory Visualization · Structural Integrity", sAuthor))
story.append(Spacer(1, 0.2*inch))

story.append(Table([[P("<b>What You Will Master</b>",
    S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· Memory model: contiguous arrays vs. non-contiguous linked nodes\n"
       "· The Dummy Node technique — the #1 edge-case eliminator\n"
       "· Fast &amp; Slow Pointers: middle detection and Floyd's Cycle Detection\n"
       "· Distance Maintenance: N-th node from end, gap-based two pointers\n"
       "· Three-Pointer Iterative Reversal (prev / curr / next)\n"
       "· K-Group Reversal: identifying, reversing, and reconnecting segments\n"
       "· Multi-list merging and intersection without extra space\n"
       "· Doubly Linked Lists and the LRU Cache design pattern\n"
       "· Circular Lists: traversal and break conditions\n"
       "· Complete edge-case checklist with common bug patterns\n"
       "· 25+ categorized LeetCode problems with key insights",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))]],
    colWidths=[CW], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.3*inch))

cx = [
    [th("Operation"), th("Linked List"), th("Array"), th("Winner")],
    [td("Access by index",C_BODY), td("O(n) — must traverse", C_RED),   td("O(1) — direct indexing",C_GREEN), td("Array",C_GREEN)],
    [td("Insert at head",  C_BODY), td("O(1) — rewire pointer",C_GREEN), td("O(n) — shift elements",  C_RED),  td("Linked List",C_GREEN)],
    [td("Insert at tail",  C_BODY), td("O(1) with tail ptr",   C_GREEN), td("O(1) amortised",         C_GREEN),td("Tie",C_YELLOW)],
    [td("Delete any node", C_BODY), td("O(1) given pointer",   C_GREEN), td("O(n) — shift elements",  C_RED),  td("Linked List",C_GREEN)],
    [td("Search by value", C_BODY), td("O(n) — linear scan",   C_YELLOW),td("O(n) unsorted / O(log n) sorted",C_YELLOW),td("Array (sorted)",C_YELLOW)],
]
story.append(Table(cx, colWidths=[130,140,145,65], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_BG),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD, C_DARK2]),
    ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),("LEFTPADDING",(0,0),(-1,-1),7)])))
story.append(Spacer(1, 0.35*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",["Contiguous vs Non-Contiguous Memory","O(1) Insert/Delete vs O(n) Access","The ListNode Structure"]),
    ("02","The Dummy Node Technique",["Why Sentinels Eliminate Edge Cases","Before vs After: dummy.next","Visual: Merging with a Dummy Head"]),
    ("03","Fast & Slow Pointers",["Finding the Middle Node","Floyd's Cycle Detection","Cycle Entry Point (Phase 2)"]),
    ("04","Distance Maintenance",["Fixed-Gap Two Pointers","N-th Node from End","Remove N-th Node from End"]),
    ("05","Structural Reversal",["Three-Pointer Iterative Reversal","Reversing a Sublist (m to n)","K-Group Reversal Logic"]),
    ("06","Multi-List Coordination",["Merging Two Sorted Lists","Merge K Sorted Lists","Intersection: Switching Heads Trick"]),
    ("07","Advanced Variations",["Doubly Linked List & LRU Cache","Circular Linked List","Skip List (Conceptual)"]),
    ("08","Comparison & Decision Making",["Linked List vs Array Table","When to Choose Each","Backend Engineering Context"]),
    ("09","Problem Roadmap",["Easy Problems","Medium Problems","Hard Problems"]),
    ("10","Edge Case Checklist",["Empty & Single-Node Lists","Losing the Head Reference","Cycle & Off-by-One Bugs"]),
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

story.append(P("<b>Contiguous vs. Non-Contiguous Memory</b>", sH2))
story.append(P(
    "Understanding <i>why</i> linked lists exist requires understanding how arrays "
    "are stored in memory. An array occupies a single <b>contiguous block</b> of RAM. "
    "Every element sits at a predictable offset from the first element, enabling "
    "O(1) index-based access: <b>address = base + (index × element_size)</b>.",
    sBody))
story.append(P(
    "A linked list abandons contiguous storage. Each <b>node</b> can live anywhere "
    "in memory — nodes are connected by <b>pointers</b> (references to the next node). "
    "This eliminates the need to shift elements on insertion or deletion, but "
    "costs the ability to index directly.",
    sBody))

# Memory layout visual
mem_data = [
    [th("Memory Address"), th("Array Value"), th(""), th("Memory Address"), th("Node Value"), th("Next Ptr")],
    [tdc("0x100", C_ACCENT), tdc("10", C_GREEN), td("",C_MUTED), tdc("0x100", C_ACCENT), tdc("10", C_GREEN), tdc("→ 0x240",C_ACCENT2)],
    [tdc("0x104", C_ACCENT), tdc("20", C_GREEN), td("",C_MUTED), tdc("0x240", C_ACCENT), tdc("20", C_GREEN), tdc("→ 0x580",C_ACCENT2)],
    [tdc("0x108", C_ACCENT), tdc("30", C_GREEN), td("",C_MUTED), tdc("0x580", C_ACCENT), tdc("30", C_GREEN), tdc("→ None", C_MUTED)],
    [tdc("0x10C", C_ACCENT), tdc("40", C_GREEN), td("",C_MUTED), td("(anywhere)", C_MUTED), td("scattered", C_MUTED), td("—",C_MUTED)],
]
story.append(Table(mem_data, colWidths=[105,100,20,105,100,50], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_BG),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD, C_DARK2]),
    ("BOX",(0,0),(1,-1),1,C_BORDER),("INNERGRID",(0,0),(1,-1),0.5,C_BORDER),
    ("BOX",(3,0),(5,-1),1,C_BORDER),("INNERGRID",(3,0),(5,-1),0.5,C_BORDER),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),("LEFTPADDING",(0,0),(-1,-1),8)])))
story.append(P("Left: Array (sequential addresses). Right: Linked List (scattered, connected by pointers)", sCaption))
story.append(Spacer(1,6))

story += callout(
    "The pointer overhead is the hidden cost of linked lists. Each node stores "
    "both its data AND a pointer (8 bytes on 64-bit systems). For a list of "
    "integers, this doubles memory usage. For small data types, arrays are "
    "often more memory-efficient despite the O(n) shift cost.",
    C_YELLOW, icon="⚠️")

story.append(P("<b>The ListNode Structure</b>", sH2))
story += code_block([
    "## ─── Standard ListNode definition ─────────────────────────────",
    "class ListNode:",
    "    def __init__(self, val=0, next=None):",
    "        self.val  = val    ## the data payload",
    "        self.next = next   ## pointer to next node (or None if tail)",
    "",
    "## ─── Building a list manually ──────────────────────────────────",
    "## [1] → [2] → [3] → None",
    "head = ListNode(1)",
    "head.next = ListNode(2)",
    "head.next.next = ListNode(3)",
    "",
    "## ─── Traversing a list ─────────────────────────────────────────",
    "curr = head",
    "while curr is not None:       ## stop when pointer falls off the end",
    "    process(curr.val)",
    "    curr = curr.next          ## advance: follow the pointer",
])

story.append(P("<b>O(1) Insert / O(n) Access: The Core Trade-off</b>", sH2))
story += code_block([
    "## ─── O(1) Insert at head ───────────────────────────────────────",
    "def insert_at_head(head, val):",
    "    new_node      = ListNode(val)",
    "    new_node.next = head   ## point new node to old head",
    "    return new_node        ## new node is the new head",
    "## No shifting. No reallocation. Just two pointer assignments.",
    "",
    "## ─── O(1) Delete given pointer to PREVIOUS node ─────────────────",
    "def delete_after(prev):",
    "    if prev.next is None: return   ## nothing to delete",
    "    prev.next = prev.next.next     ## skip the node — it gets garbage-collected",
    "",
    "## ─── O(n) Access by index ──────────────────────────────────────",
    "def get_nth(head, n):",
    "    curr = head",
    "    for _ in range(n):             ## must walk n steps",
    "        curr = curr.next",
    "    return curr",
    "## No shortcut: must start from head and follow pointers.",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2 — DUMMY NODE
# ════════════════════════════════════════════════════════
story += section_divider(2, "The Dummy Node Technique")

story.append(P("<b>The #1 Edge-Case Eliminator</b>", sH2))
story.append(P(
    "Every linked list problem has at least three special cases: "
    "empty list, single-node list, and modifications to the head node. "
    "Without a sentinel, code is cluttered with 'if head is None' guards. "
    "The <b>Dummy Node</b> (also called sentinel or guard node) is a "
    "placeholder prepended to the list. It has no meaningful value — "
    "its only purpose is to give 'prev' a valid starting point so "
    "that the head node is treated identically to every other node.",
    sBody))

story += callout(
    "Rule: Whenever your algorithm needs to potentially modify the HEAD of the list "
    "(delete it, insert before it, merge into it), use a dummy node. "
    "Set dummy.next = head, run your algorithm, and return dummy.next at the end. "
    "This single habit eliminates 90% of linked list edge case bugs.",
    C_GREEN, icon="✅")

story.append(P("<b>Before vs. After: The Logic</b>", sH2))

# Side-by-side comparison
story += code_block([
    "## ─── ❌ WITHOUT dummy: head deletion needs a special case ───────",
    "def delete_val_v1(head, val):",
    "    if head and head.val == val: return head.next   ## special case!",
    "    curr = head",
    "    while curr and curr.next:",
    "        if curr.next.val == val:",
    "            curr.next = curr.next.next",
    "            return head",
    "        curr = curr.next",
    "    return head",
    "",
    "## ─── ✅ WITH dummy: head is treated identically to all others ────",
    "def delete_val_v2(head, val):",
    "    dummy      = ListNode(0)",
    "    dummy.next = head",
    "    curr       = dummy    ## start before head — no special case needed",
    "    while curr.next:",
    "        if curr.next.val == val:",
    "            curr.next = curr.next.next",
    "            break",
    "        curr = curr.next",
    "    return dummy.next     ## always correct, even if head was deleted",
])
story.append(Spacer(1,8))

story.append(P("<b>Visual: Dummy Node During a Merge Operation</b>", sH3))
story.append(P("Merging [1→3→5] and [2→4→6] using a dummy head. The dummy acts as a guaranteed 'prev' for the first real node:", sBody))

# Visualise the dummy at start
story.append(P("Initial state:", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=3)))
story += node_chain([0,1,3,5], highlight=[0], pointer_labels={0:"dummy/curr",1:"p1",2:"",3:""})
story += node_chain([2,4,6],   highlight=[],  pointer_labels={0:"p2"})

story.append(P("After first comparison (1 &lt; 2, take 1):", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=3)))
story += node_chain([0,1,2,3,4,5,6], highlight=[0,1], pointer_labels={0:"dummy",1:"",2:"p2/curr",3:"p1"})

story.append(P("Final result — return dummy.next:", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=3)))
story += node_chain([1,2,3,4,5,6], pointer_labels={0:"head (dummy.next)"})

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3 — FAST & SLOW POINTERS
# ════════════════════════════════════════════════════════
story += section_divider(3, "Fast & Slow Pointers")

story.append(P("<b>Finding the Middle Node</b>", sH2))
story.append(P(
    "Move <b>slow</b> one step and <b>fast</b> two steps simultaneously. "
    "When fast reaches the end (or can no longer take two steps), "
    "slow is at the middle. For even-length lists, slow lands on "
    "the second of the two middle nodes — use <b>fast and fast.next</b> "
    "as the loop condition to get the first middle instead.",
    sBody))

story += code_block([
    "## ─── Find middle of linked list ───────────────────────────────",
    "def find_middle(head):",
    "    slow = head",
    "    fast = head",
    "    ## fast moves 2 steps; slow moves 1 step",
    "    ## When fast can't take 2 more steps, slow is at middle",
    "    while fast and fast.next:",
    "        slow = slow.next        ## 1 step",
    "        fast = fast.next.next   ## 2 steps",
    "    return slow   ## middle node",
    "",
    "## For ODD list [1,2,3,4,5]:  slow lands on 3 ✓",
    "## For EVEN list [1,2,3,4]:   slow lands on 3 (second middle)",
    "## To get first middle of even list: while fast.next and fast.next.next",
])

story.append(P("Visual trace on [1 → 2 → 3 → 4 → 5]:", sH3))
steps_mid = [
    ([1,2,3,4,5], {0:"slow/fast"}, "Start: both at head"),
    ([1,2,3,4,5], {1:"slow",2:"fast"}, "Step 1: slow→2, fast→3"),
    ([1,2,3,4,5], {2:"slow",4:"fast"}, "Step 2: slow→3, fast→5. fast.next=None → stop. MIDDLE = 3"),
]
for vals, ptrs, desc in steps_mid:
    story += node_chain(vals, pointer_labels=ptrs)
    story.append(P(f"<b>{desc}</b>", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW, spaceAfter=6)))

story.append(P("<b>Floyd's Cycle Detection (Tortoise and Hare)</b>", sH2))
story.append(P(
    "If a cycle exists, the fast pointer will eventually lap the slow pointer "
    "and they will meet <i>inside</i> the cycle. If there is no cycle, fast "
    "will reach None first. The algorithm is O(n) time and O(1) space — "
    "no visited set required.",
    sBody))

story += code_block([
    "## ─── Phase 1: Detect if cycle exists ──────────────────────────",
    "def has_cycle(head):",
    "    slow = fast = head",
    "    while fast and fast.next:",
    "        slow = slow.next",
    "        fast = fast.next.next",
    "        if slow is fast:     ## identity check, not equality",
    "            return True      ## they met → cycle confirmed",
    "    return False             ## fast fell off end → no cycle",
    "",
    "## ─── Phase 2: Find cycle ENTRY POINT ──────────────────────────",
    "def detect_cycle(head):",
    "    slow = fast = head",
    "",
    "    ## Phase 1: find meeting point",
    "    while fast and fast.next:",
    "        slow = slow.next",
    "        fast = fast.next.next",
    "        if slow is fast: break",
    "    else:",
    "        return None          ## no cycle",
    "",
    "    ## Phase 2: find entry node",
    "    ## Mathematical proof: distance(head→entry) == distance(meet→entry via cycle)",
    "    slow = head              ## reset slow to head",
    "    while slow is not fast:",
    "        slow = slow.next     ## both move 1 step",
    "        fast = fast.next",
    "    return slow              ## cycle entry node",
])

# Cycle visualization
story.append(P("<b>Visual: Cycle Structure</b>", sH3))
story.append(P("List where node 4 points back to node 2 (cycle entry):", sBody))

cycle_data = [[
    P("head", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_ACCENT, alignment=TA_CENTER)),
    P("", sCaption), P("", sCaption), P("", sCaption), P("", sCaption), P("", sCaption),
]]
cycle_vals = [[
    P("[1]", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_HEADING, alignment=TA_CENTER)),
    P("→", S("_", fontName="Helvetica-Bold", fontSize=14, textColor=C_ACCENT, alignment=TA_CENTER)),
    P("[2]", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_GREEN, alignment=TA_CENTER)),
    P("→", S("_", fontName="Helvetica-Bold", fontSize=14, textColor=C_ACCENT, alignment=TA_CENTER)),
    P("[3]", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_HEADING, alignment=TA_CENTER)),
    P("→", S("_", fontName="Helvetica-Bold", fontSize=14, textColor=C_ACCENT, alignment=TA_CENTER)),
    P("[4]", S("_", fontName="Courier-Bold", fontSize=11, textColor=C_HEADING, alignment=TA_CENTER)),
    P("→ back to [2]", S("_", fontName="Courier-Bold", fontSize=9, textColor=C_RED, alignment=TA_CENTER)),
]]
entry_row = [[
    P("", sCaption), P("", sCaption),
    P("entry", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_GREEN, alignment=TA_CENTER)),
    P("", sCaption), P("", sCaption), P("", sCaption),
    P("meet", S("_", fontName="Helvetica-Bold", fontSize=8, textColor=C_YELLOW, alignment=TA_CENTER)),
    P("", sCaption),
]]
cw8 = [40, 28, 40, 28, 40, 28, 40, 80]
story.append(Table([cycle_data[0], cycle_vals[0], entry_row[0]], colWidths=cw8, style=TableStyle([
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("BOX",(0,1),(0,1),1,C_BORDER),("BOX",(2,1),(2,1),1,colors.HexColor("#0A2E1A")),
    ("BOX",(4,1),(4,1),1,C_BORDER),("BOX",(6,1),(6,1),1,colors.HexColor("#2E2A0A")),
    ("BACKGROUND",(2,1),(2,1),colors.HexColor("#0A2E1A")),
    ("BACKGROUND",(6,1),(6,1),colors.HexColor("#2E2A0A")),
    ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
    ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2),
    ("TOPPADDING",(0,2),(-1,2),2),("BOTTOMPADDING",(0,2),(-1,2),2),
])))
story.append(Spacer(1, 8))

story += callout(
    "Why does Phase 2 work? Let F = distance(head → entry), C = cycle length, "
    "k = steps taken. When they meet: slow took F+a steps; fast took F+a+nC steps. "
    "Since fast = 2×slow: 2(F+a) = F+a+nC → F = nC-a. "
    "So from head and meeting point, both pointers travel F steps to reach entry.",
    C_ACCENT2, icon="📐")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4 — DISTANCE MAINTENANCE
# ════════════════════════════════════════════════════════
story += section_divider(4, "Distance Maintenance")

story.append(P("<b>Fixed-Gap Two Pointers</b>", sH2))
story.append(P(
    "Create a fixed <b>gap of n nodes</b> between two pointers by advancing "
    "the first pointer n steps ahead. Then move both at the same speed. "
    "When the front pointer reaches the end, the rear pointer is exactly "
    "n positions from the end — without knowing the list length in advance.",
    sBody))

story += code_block([
    "## ─── Remove N-th Node from End ────────────────────────────────",
    "def remove_nth_from_end(head, n):",
    "    dummy = ListNode(0)",
    "    dummy.next = head",
    "    front = dummy",
    "    back  = dummy",
    "",
    "    ## Advance front by n+1 steps (extra 1 so back lands on prev node)",
    "    for _ in range(n + 1):",
    "        front = front.next",
    "",
    "    ## Move both until front falls off the end",
    "    while front is not None:",
    "        front = front.next",
    "        back  = back.next",
    "",
    "    ## back is now the node BEFORE the target",
    "    back.next = back.next.next   ## skip the target node",
    "    return dummy.next",
])

story.append(P("Visual trace: remove 2nd from end of [1→2→3→4→5], n=2", sH3))
trace_steps = [
    ([0,1,2,3,4,5], {0:"dummy/back",3:"front"}, "After advancing front by n+1=3 steps (gap=3)"),
    ([0,1,2,3,4,5], {1:"back",4:"front"},        "Step 1: both advance"),
    ([0,1,2,3,4,5], {2:"back",5:"front"},        "Step 2: front at tail"),
    ([0,1,2,3,4,5], {3:"back",},                 "Step 3: front=None → back.next (node 4) is the target → skip it"),
]
for vals, ptrs, desc in trace_steps:
    story += node_chain(vals, highlight=[0], pointer_labels=ptrs)
    story.append(P(f"<b>{desc}</b>", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW, spaceAfter=6)))

story.append(P("Result after back.next = back.next.next:", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=3)))
story += node_chain([1,2,3,5], pointer_labels={0:"head"})

story += callout(
    "The dummy node is crucial here: when n equals the list length (deleting "
    "the head), back would otherwise have no valid starting position. "
    "With dummy, back starts at dummy and the deletion of the real head "
    "becomes a normal back.next = back.next.next operation.",
    C_PURPLE, icon="🎯")

story.append(P("<b>Gap Technique Summary</b>", sH3))
gap_data = [
    [th("Goal"),                              th("Gap Size"),    th("Loop Until"),       th("back Points To")],
    [td("N-th node from end (find it)",C_BODY),tdc("n steps"),   tdc("front is None"),  td("The target node",    C_BODY)],
    [td("Remove N-th from end",        C_BODY),tdc("n+1 steps"),  tdc("front is None"),  td("Node BEFORE target", C_BODY)],
    [td("Check if list has ≥ k nodes", C_BODY),tdc("k steps"),   tdc("front is None"),  td("(not needed)",       C_MUTED)],
    [td("Find node k from beginning",  C_BODY),tdc("k steps (just walk)",C_MUTED),tdc("—"),td("Node k",          C_BODY)],
]
story.append(std_table(gap_data, [160, 90, 130, 100]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5 — STRUCTURAL REVERSAL
# ════════════════════════════════════════════════════════
story += section_divider(5, "Structural Reversal Patterns")

story.append(P("<b>The Three-Pointer Iterative Reversal</b>", sH2))
story.append(P(
    "Reversing a linked list requires three pointers: <b>prev</b> (the reversed portion), "
    "<b>curr</b> (the node being processed), and <b>next_node</b> (saved before unlinking). "
    "The operation on each step is identical: save next, redirect curr back, advance both.",
    sBody))

story.append(P("At every step: (1) save next, (2) redirect curr.next → prev, (3) advance prev = curr, (4) advance curr = saved next", sFormula))

story += code_block([
    "## ─── Iterative Linked List Reversal ────────────────────────────",
    "def reverse_list(head):",
    "    prev = None    ## the 'reversed so far' tail (starts as None = new tail)",
    "    curr = head",
    "",
    "    while curr is not None:",
    "        next_node  = curr.next    ## Step 1: SAVE next before breaking link",
    "        curr.next  = prev         ## Step 2: REDIRECT curr backward",
    "        prev       = curr         ## Step 3: advance prev (prev is new head-so-far)",
    "        curr       = next_node    ## Step 4: advance curr to saved next",
    "",
    "    return prev   ## when curr is None, prev is the new head",
])

story.append(P("Visual trace: reversing [1 → 2 → 3 → None]", sH3))
rev_steps = [
    ([1,2,3], {0:"curr"}, "Initial: prev=None, curr=head"),
    ([1,2,3], {1:"curr",0:"prev"}, "After step 1: [1].next = None, prev=1, curr=2"),
    ([1,2,3], {2:"curr",1:"prev"}, "After step 2: [2].next = 1, prev=2, curr=3"),
    ([1,2,3], {2:"prev"},          "After step 3: [3].next = 2, prev=3, curr=None → DONE"),
]
for vals, ptrs, desc in rev_steps:
    story += node_chain(vals, pointer_labels=ptrs)
    story.append(P(f"<b>{desc}</b>", S("_", fontName="Helvetica", fontSize=9, textColor=C_YELLOW, spaceAfter=6)))

story.append(P("New list after reversal:", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_MUTED, spaceAfter=3)))
story += node_chain([3,2,1], pointer_labels={0:"head (prev)"})

story.append(P("<b>Reversing a Sublist (Positions m to n)</b>", sH2))
story.append(P(
    "To reverse only part of a list, we need to: (1) walk to the node before "
    "position m, (2) reverse exactly (n−m+1) nodes, and (3) reconnect the "
    "reversed segment back to the surrounding nodes. A dummy head handles m=1 "
    "(reversing from the very start).",
    sBody))
story += code_block([
    "## ─── Reverse Sublist from position m to n (1-indexed) ──────────",
    "def reverse_between(head, m, n):",
    "    dummy      = ListNode(0)",
    "    dummy.next = head",
    "    pre        = dummy          ## node just before the reversal starts",
    "",
    "    ## Walk pre to position m-1",
    "    for _ in range(m - 1):",
    "        pre = pre.next",
    "",
    "    ## Now reverse (n - m + 1) nodes starting at pre.next",
    "    curr = pre.next             ## first node of sublist",
    "    prev = None",
    "    for _ in range(n - m + 1):",
    "        next_node = curr.next",
    "        curr.next = prev",
    "        prev      = curr",
    "        curr      = next_node",
    "",
    "    ## Reconnect: pre → [reversed head] and [original m] → curr",
    "    pre.next.next = curr        ## original m-th node (now tail) → node after n",
    "    pre.next      = prev        ## pre → reversed head (original n-th node)",
    "    return dummy.next",
])

story.append(P("<b>K-Group Reversal: Reverse Nodes in K-Group</b>", sH2))
story.append(P(
    "Reverse every k consecutive nodes. For each group: (1) check k nodes exist "
    "ahead, (2) reverse the k-node segment, (3) reconnect and move to the next group. "
    "The 'check k nodes exist' step prevents reversing a final partial group.",
    sBody))
story += code_block([
    "## ─── Helper: check if at least k nodes remain ───────────────────",
    "def has_k_nodes(node, k):",
    "    count = 0",
    "    while node and count < k:",
    "        node  = node.next",
    "        count += 1",
    "    return count == k",
    "",
    "## ─── Reverse K-Group ────────────────────────────────────────────",
    "def reverse_k_group(head, k):",
    "    dummy      = ListNode(0)",
    "    dummy.next = head",
    "    group_prev = dummy          ## tail of already-processed portion",
    "",
    "    while has_k_nodes(group_prev.next, k):",
    "        ## Identify group: [group_start ... group_end]",
    "        group_start = group_prev.next",
    "        group_end   = group_prev",
    "        for _ in range(k):",
    "            group_end = group_end.next",
    "",
    "        ## Save the node after this group",
    "        next_group = group_end.next",
    "",
    "        ## Reverse the k nodes",
    "        prev, curr = None, group_start",
    "        for _ in range(k):",
    "            nxt = curr.next; curr.next = prev; prev = curr; curr = nxt",
    "",
    "        ## Reconnect: group_prev → new head (prev), old head → next group",
    "        group_prev.next      = prev          ## connect to reversed head",
    "        group_start.next     = next_group    ## original start is now tail",
    "        group_prev           = group_start   ## advance group_prev",
    "",
    "    return dummy.next",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6 — MULTI-LIST COORDINATION
# ════════════════════════════════════════════════════════
story += section_divider(6, "Multi-List Coordination")

story.append(P("<b>Merging Two Sorted Lists</b>", sH2))
story.append(P(
    "Use a dummy node as the result list head. Compare the front elements of "
    "both lists, attach the smaller one to the result, and advance that pointer. "
    "After one list is exhausted, attach the remaining portion directly.",
    sBody))
story += code_block([
    "## ─── Merge Two Sorted Linked Lists ─────────────────────────────",
    "def merge_two_lists(l1, l2):",
    "    dummy = ListNode(0)",
    "    curr  = dummy",
    "",
    "    while l1 and l2:",
    "        if l1.val <= l2.val:",
    "            curr.next = l1          ## attach smaller node",
    "            l1        = l1.next     ## advance that list's pointer",
    "        else:",
    "            curr.next = l2",
    "            l2        = l2.next",
    "        curr = curr.next            ## advance result pointer",
    "",
    "    ## Attach remaining nodes (at most one list still has nodes)",
    "    curr.next = l1 if l1 else l2    ## one pointer assignment, not a loop",
    "    return dummy.next",
])

story.append(P("<b>Merge K Sorted Lists</b>", sH2))
story.append(P(
    "Extending merge to K lists. Divide and conquer beats the naive approach:",
    sBody))
mk_data = [
    [th("Approach"),               th("Time"),            th("Space"),   th("Notes")],
    [td("Merge one by one",  C_BODY), tdc("O(nK)",   C_RED),    tdc("O(1)"),  td("Merge result with each next list. Slow for large K.",   C_MUTED)],
    [td("Min-Heap (Priority Queue)",C_BODY),tdc("O(n log K)",C_GREEN),tdc("O(K)"),td("Push head of each list. Pop min, push its next. Optimal.",C_MUTED)],
    [td("Divide and Conquer",C_BODY),tdc("O(n log K)",C_GREEN),tdc("O(log K)"),td("Pair lists, merge pairs, repeat. Same time as heap.",C_MUTED)],
]
story.append(std_table(mk_data, [130, 80, 70, 200]))
story.append(Spacer(1, 8))

story.append(P("<b>Finding the Intersection of Two Lists</b>", sH2))
story.append(P(
    "Given two singly linked lists that may share a tail segment, find the "
    "first shared node. The elegant O(n+m) / O(1) space solution: "
    "run two pointers, one per list. When a pointer reaches the end of its list, "
    "redirect it to the <b>head of the other list</b>. Both pointers traverse "
    "the same total distance and meet at the intersection node (or both hit None if no intersection).",
    sBody))

story += code_block([
    "## ─── Intersection: Switching Heads Trick ────────────────────────",
    "def get_intersection(headA, headB):",
    "    pA, pB = headA, headB",
    "",
    "    ## Each pointer traverses both lists exactly once.",
    "    ## After at most len(A) + len(B) steps, they meet.",
    "    while pA is not pB:",
    "        pA = pA.next if pA else headB  ## switch to headB at end of A",
    "        pB = pB.next if pB else headA  ## switch to headA at end of B",
    "",
    "    return pA  ## None if no intersection",
    "",
    "## Why this works:",
    "## pA travels: [len_A + shared + len_B_unique] total",
    "## pB travels: [len_B + shared + len_A_unique] total",
    "## Both travel len_A + len_B total → they arrive at intersection simultaneously",
])

story.append(P("<b>Visual: Switching Heads</b>", sH3))
story.append(P("List A: [1→3→5→7→8→None] | List B: [2→4→7→8→None] | Intersection at node 7:", sBody))

inter_data = [
    [td("List A",C_ACCENT,"Helvetica-Bold"),
     P("1 → 3 → 5 →", S("_", fontName="Courier", fontSize=10, textColor=C_ACCENT)),
     P("[7] → 8 → None", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_GREEN))],
    [td("List B",C_TEAL,"Helvetica-Bold"),
     P("2 → 4 →", S("_", fontName="Courier", fontSize=10, textColor=C_TEAL)),
     P("[7] → 8 → None (shared)", S("_", fontName="Courier-Bold", fontSize=10, textColor=C_GREEN))],
    [td("pA path",C_ACCENT2),
     P("1,3,5,7,8,None→2,4,[7]", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("← meets pB here", S("_", fontName="Helvetica-Oblique", fontSize=9, textColor=C_GREEN))],
    [td("pB path",C_ACCENT2),
     P("2,4,7,8,None→1,3,5,[7]", S("_", fontName="Courier", fontSize=9, textColor=C_BODY)),
     P("← meets pA here", S("_", fontName="Helvetica-Oblique", fontSize=9, textColor=C_GREEN))],
]
story.append(Table(inter_data, colWidths=[60, 200, 220], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),C_CARD),
    ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),("LEFTPADDING",(0,0),(-1,-1),8)])))
story.append(Spacer(1,8))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7 — ADVANCED VARIATIONS
# ════════════════════════════════════════════════════════
story += section_divider(7, "Advanced Variations")

story.append(P("<b>Doubly Linked List</b>", sH2))
story.append(P(
    "A doubly linked list adds a <b>prev pointer</b> to each node, enabling "
    "O(1) backward traversal. This doubles pointer overhead but unlocks "
    "bidirectional movement — crucial for certain patterns and real-world "
    "data structures.",
    sBody))

story += code_block([
    "## ─── Doubly Linked List Node ────────────────────────────────────",
    "class DListNode:",
    "    def __init__(self, val=0):",
    "        self.val  = val",
    "        self.prev = None   ## ← extra pointer backward",
    "        self.next = None",
    "",
    "## ─── O(1) Delete a Node Given Its Pointer ────────────────────────",
    "## This is impossible in O(1) with a singly linked list without prev!",
    "def delete_node(node):",
    "    node.prev.next = node.next    ## bypass node going forward",
    "    if node.next:                 ## node is not tail",
    "        node.next.prev = node.prev ## bypass node going backward",
    "    ## node is now unreachable — garbage collected",
])

story.append(P("<b>LRU Cache: The Classic Doubly-Linked List Application</b>", sH3))
story.append(P(
    "An LRU (Least Recently Used) Cache requires O(1) get and O(1) put. "
    "The solution combines a <b>HashMap</b> (for O(1) key lookup) with a "
    "<b>Doubly Linked List</b> (for O(1) move-to-front and evict-from-back). "
    "A dummy head and dummy tail eliminate boundary checks on insert/delete.",
    sBody))

story += code_block([
    "## ─── LRU Cache Structure (Conceptual) ──────────────────────────",
    "class LRUCache:",
    "    def __init__(self, capacity):",
    "        self.cap   = capacity",
    "        self.cache = {}           ## key → DListNode",
    "        ## Dummy sentinels: head = MRU side, tail = LRU side",
    "        self.head  = DListNode()  ## most recently used",
    "        self.tail  = DListNode()  ## least recently used",
    "        self.head.next = self.tail",
    "        self.tail.prev = self.head",
    "",
    "    def get(self, key):",
    "        if key not in self.cache: return -1",
    "        node = self.cache[key]",
    "        self._move_to_front(node) ## accessing = recently used",
    "        return node.val",
    "",
    "    def put(self, key, value):",
    "        if key in self.cache:",
    "            node = self.cache[key]",
    "            node.val = value",
    "            self._move_to_front(node)",
    "        else:",
    "            if len(self.cache) == self.cap:",
    "                lru = self.tail.prev  ## node just before dummy tail",
    "                self._remove(lru)",
    "                del self.cache[lru.key]",
    "            new_node = DListNode(key, value)",
    "            self._insert_at_front(new_node)",
    "            self.cache[key] = new_node",
    "",
    "    ## O(1) because we have prev pointers:",
    "    def _remove(self, node):",
    "        node.prev.next = node.next",
    "        node.next.prev = node.prev",
    "",
    "    def _insert_at_front(self, node):",
    "        node.next = self.head.next",
    "        node.prev = self.head",
    "        self.head.next.prev = node",
    "        self.head.next = node",
    "",
    "    def _move_to_front(self, node):",
    "        self._remove(node)",
    "        self._insert_at_front(node)",
])

story.append(P("<b>Circular Linked List</b>", sH2))
story.append(P(
    "In a circular list, the tail node's <b>next</b> pointer points back to the "
    "head instead of None. This is useful for round-robin scheduling and "
    "music playlist loops. The key challenge: detecting the end of a traversal "
    "without hitting None (which never comes).",
    sBody))
story += code_block([
    "## ─── Traversing a Circular List Safely ──────────────────────────",
    "def traverse_circular(head):",
    "    if head is None: return",
    "    curr = head",
    "    while True:",
    "        process(curr.val)",
    "        curr = curr.next",
    "        if curr is head: break   ## 'is' identity check, not equality",
    "",
    "## ─── Convert singly linked to circular ──────────────────────────",
    "def make_circular(head):",
    "    if head is None: return None",
    "    tail = head",
    "    while tail.next:       ## find tail",
    "        tail = tail.next",
    "    tail.next = head       ## point tail back to head",
    "    return head",
])

story += callout(
    "Always use identity comparison (is) not equality (==) when checking "
    "for the head node in circular traversal. Two different nodes with the "
    "same value would incorrectly terminate the loop with ==.",
    C_RED, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8 — COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(8, "Comparison & Decision Making")

story.append(P("<b>Linked List vs. Array: The Full Picture</b>", sH2))

la_data = [
    [th("Dimension"),          th("Linked List"),                         th("Array / Dynamic Array")],
    [td("Memory layout",C_BODY),td("Non-contiguous; nodes scattered in heap",C_BODY), td("Contiguous block; predictable offsets",C_BODY)],
    [td("Access by index",C_BODY),td("O(n) — must traverse from head",C_RED),         td("O(1) — direct address computation",C_GREEN)],
    [td("Insert at head",C_BODY), td("O(1) — just rewire pointer",C_GREEN),            td("O(n) — shift all elements right",C_RED)],
    [td("Insert at tail",C_BODY), td("O(1) with tail pointer",C_GREEN),                td("O(1) amortised (dynamic array)",C_GREEN)],
    [td("Insert at middle",C_BODY),td("O(1) given pointer; O(n) to find node",C_YELLOW),td("O(n) — shift half the array",C_RED)],
    [td("Delete head",C_BODY),    td("O(1)",C_GREEN),                                  td("O(n)",C_RED)],
    [td("Delete by value",C_BODY),td("O(n) search + O(1) delete",C_YELLOW),            td("O(n) search + O(n) shift",C_RED)],
    [td("Memory overhead",C_BODY),td("8 bytes extra per node (pointer)",C_RED),         td("No pointer overhead",C_GREEN)],
    [td("Cache performance",C_BODY),td("Poor — scattered memory = cache misses",C_RED), td("Excellent — sequential = cache friendly",C_GREEN)],
    [td("Size flexibility",C_BODY),td("Dynamic by nature",C_GREEN),                    td("Fixed (array) or amortised O(1) (dynamic)",C_YELLOW)],
    [td("Binary search",C_BODY),  td("❌ Not possible",C_RED),                          td("✅ O(log n) if sorted",C_GREEN)],
    [td("Reverse iteration",C_BODY),td("O(n) singly; O(1) doubly",C_YELLOW),           td("O(1) — use negative index",C_GREEN)],
]
story.append(std_table(la_data, [140, 200, 140]))
story.append(Spacer(1, 10))

story.append(P("<b>Backend Engineering Decision Guide</b>", sH2))
be_data = [
    [th("Use Case"),                                         th("Best Choice"),   th("Reason")],
    [td("Implement a Queue (FIFO)",                C_BODY),  td("Linked List", C_GREEN), td("O(1) enqueue at tail, O(1) dequeue at head",C_MUTED)],
    [td("Implement a Stack (LIFO)",                C_BODY),  td("Array",       C_YELLOW),td("Python list.append/pop are O(1) amortised + better cache",C_MUTED)],
    [td("LRU / LFU Cache",                         C_BODY),  td("DLL + HashMap",C_GREEN),td("O(1) move-to-front requires prev pointer",C_MUTED)],
    [td("Frequent mid-sequence inserts/deletes",   C_BODY),  td("Linked List", C_GREEN), td("O(1) with pointer; array needs O(n) shift",C_MUTED)],
    [td("Random access / binary search",           C_BODY),  td("Array",       C_GREEN), td("O(1) vs O(n) — no contest",C_MUTED)],
    [td("Memory-constrained small elements",       C_BODY),  td("Array",       C_GREEN), td("No 8-byte pointer overhead per element",C_MUTED)],
    [td("Large heterogeneous elements",            C_BODY),  td("Either",      C_YELLOW),td("Pointer overhead is proportionally smaller",C_MUTED)],
    [td("Undo/Redo history",                       C_BODY),  td("DLL",         C_GREEN), td("O(1) forward/backward navigation",C_MUTED)],
    [td("Text editor (cursor operations)",         C_BODY),  td("DLL (rope)",  C_GREEN), td("Efficient split/join at cursor position",C_MUTED)],
    [td("Graph adjacency list",                    C_BODY),  td("Array/HashMap",C_GREEN),td("Python list for adj[u]; HashMap for node-labelled graphs",C_MUTED)],
]
story.append(std_table(be_data, [175, 95, 210]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9 — PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(9, "LeetCode Problem Roadmap")
story.append(P("Solve in sequence — each problem introduces one new pointer technique.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("206",C_GREEN), td("Reverse Linked List",                 C_BODY), td("3-Pointer Reversal",  C_ACCENT),  td("prev=None, curr=head; 4-step loop. Return prev.", C_MUTED)],
    [tdc("21", C_GREEN), td("Merge Two Sorted Lists",              C_BODY), td("Dummy Node + Merge",  C_ACCENT2), td("Dummy head; compare front elements, attach smaller.", C_MUTED)],
    [tdc("141",C_GREEN), td("Linked List Cycle",                   C_BODY), td("Fast & Slow",         C_GREEN),   td("Floyd Phase 1 only: return slow is fast.", C_MUTED)],
    [tdc("876",C_GREEN), td("Middle of the Linked List",           C_BODY), td("Fast & Slow",         C_GREEN),   td("while fast and fast.next: slow lands at mid.", C_MUTED)],
    [tdc("83", C_GREEN), td("Remove Duplicates from Sorted List",  C_BODY), td("Single Pointer",      C_TEAL),    td("if curr.val == curr.next.val: skip next.", C_MUTED)],
    [tdc("203",C_GREEN), td("Remove Linked List Elements",         C_BODY), td("Dummy Node",          C_PURPLE),  td("Dummy handles head deletion uniformly.", C_MUTED)],
    [tdc("234",C_GREEN), td("Palindrome Linked List",              C_BODY), td("Fast/Slow + Reverse", C_ACCENT2), td("Find mid, reverse second half, compare.", C_MUTED)],
    [tdc("160",C_GREEN), td("Intersection of Two Linked Lists",    C_BODY), td("Switching Heads",     C_ORANGE),  td("Redirect to other list head on None; they meet at intersection.", C_MUTED)],
]
story.append(std_table(easy_data, [38, 190, 120, 132]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("2",  C_YELLOW), td("Add Two Numbers",                  C_BODY), td("Dummy + Traversal",   C_ACCENT),  td("Carry digit; handle different lengths and final carry.", C_MUTED)],
    [tdc("19", C_YELLOW), td("Remove N-th Node from End",        C_BODY), td("Distance Gap",        C_ACCENT2), td("Advance front n+1 steps; back lands at predecessor.", C_MUTED)],
    [tdc("24", C_YELLOW), td("Swap Nodes in Pairs",              C_BODY), td("Dummy + 4 Pointers",  C_GREEN),   td("Dummy → A → B → rest; rewire: dummy→B→A→rest.", C_MUTED)],
    [tdc("92", C_YELLOW), td("Reverse Linked List II (m to n)",  C_BODY), td("Sublist Reversal",    C_PURPLE),  td("Walk to pre; reverse n-m+1 nodes; reconnect four links.", C_MUTED)],
    [tdc("142",C_YELLOW), td("Linked List Cycle II",             C_BODY), td("Floyd Phase 1+2",     C_GREEN),   td("Phase 2: reset slow to head; both advance 1 step.", C_MUTED)],
    [tdc("143",C_YELLOW), td("Reorder List",                     C_BODY), td("Mid + Reverse + Merge",C_ORANGE), td("Split at mid, reverse second half, interleave.", C_MUTED)],
    [tdc("328",C_YELLOW), td("Odd Even Linked List",             C_BODY), td("Two Sublists",        C_TEAL),    td("Separate odd/even index nodes; concatenate.", C_MUTED)],
    [tdc("148",C_YELLOW), td("Sort List",                        C_BODY), td("MergeSort on List",   C_ACCENT2), td("Find mid (fast/slow), sort halves, merge. O(n log n).", C_MUTED)],
    [tdc("138",C_YELLOW), td("Copy List with Random Pointer",    C_BODY), td("HashMap + Traversal", C_ACCENT2), td("Map: old→new; two passes for next and random.", C_MUTED)],
]
story.append(std_table(med_data, [38, 190, 130, 122]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("25",  C_RED), td("Reverse Nodes in K-Group",          C_BODY), td("K-Group Reversal",    C_PURPLE),
     td("has_k_nodes check; reverse in-place; reconnect group_prev and group_start.", C_MUTED)],
    [tdc("23",  C_RED), td("Merge K Sorted Lists",              C_BODY), td("Min-Heap / D&C",      C_RED),
     td("Min-heap of (val, idx, node); pop min, push next. O(n log K).", C_MUTED)],
    [tdc("146", C_RED), td("LRU Cache",                         C_BODY), td("DLL + HashMap",       C_ORANGE),
     td("Dummy head/tail; HashMap for O(1) lookup; DLL for O(1) move-to-front.", C_MUTED)],
    [tdc("432", C_RED), td("All O(1) Data Structure",           C_BODY), td("DLL + HashMap",       C_ORANGE),
     td("Frequency buckets as DLL nodes; each bucket holds a set of keys.", C_MUTED)],
]
story.append(std_table(hard_data, [38, 185, 120, 137]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 10 — EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(10, "The Edge Case Checklist")

story.append(P(
    "Linked list problems fail almost exclusively on edge cases. "
    "Memorise these patterns — they account for the majority of "
    "Wrong Answer verdicts even when the main logic is correct.",
    sBody))

story.append(P("<b>Edge Case 1: Empty List (head is None)</b>", sH2))
story += code_block([
    "## ALWAYS guard at the top for algorithms that dereference head",
    "def my_algo(head):",
    "    if head is None: return None   ## or 0, or False — depends on problem",
    "    ## ...rest of algorithm...",
    "",
    "## Fast/Slow pointer: guard against None before .next",
    "while fast and fast.next:         ## NOT: while fast.next.next",
    "    ## If fast is None, fast.next crashes. Check fast first.",
])

story.append(P("<b>Edge Case 2: Single-Node List</b>", sH2))
story += code_block([
    "## Reversal: single node — prev=None, curr=head, first iteration:",
    "## next_node = None, curr.next = None (was already), prev = node, curr = None",
    "## Result: prev = original node with .next = None ✓ (correct)",
    "",
    "## Cycle detection: head.next = None → fast.next check fails immediately → False ✓",
    "",
    "## Palindrome check: middle = head → reversed second half = empty → always True ✓",
    "",
    "## Remove N-th from end: if n=1 and list has 1 node:",
    "## dummy → [1] → None. front advances n+1=2 steps → None. back stays at dummy.",
    "## dummy.next = dummy.next.next = None → returns dummy.next = None ✓",
])

story.append(P("<b>Edge Case 3: Losing the Head Reference</b>", sH2))
story.append(P(
    "The most catastrophic linked list bug: overwriting the only reference to "
    "the head node before saving it. Once lost, the original list is "
    "unrecoverable — the nodes exist in memory but are permanently inaccessible.",
    sBody))
story += code_block([
    "## WRONG — head reference lost during reversal!",
    "## def broken_reverse(head):",
    "##     head.next = None    ## ← DESTROYS the link to rest of list",
    "##     # Now we can never reach nodes 2, 3, 4, ...",
    "",
    "## CORRECT — always save next BEFORE breaking any link",
    "def safe_reverse(head):",
    "    prev = None",
    "    curr = head",
    "    while curr:",
    "        next_node  = curr.next    ## SAVE first",
    "        curr.next  = prev         ## BREAK link second",
    "        prev       = curr",
    "        curr       = next_node    ## use saved reference",
    "    return prev",
    "",
    "## General rule: in any pointer rewiring, follow this order:",
    "## 1. Save all references you will need AFTER the rewiring",
    "## 2. Perform the rewiring",
    "## 3. Advance pointers using saved references",
])

story += callout(
    "Mental model: treat pointer rewiring like moving furniture in a small room. "
    "Before moving any piece, figure out what you'll stand on AFTER it moves. "
    "The 'next_node = curr.next' line is your foothold — never skip it.",
    C_ACCENT, icon="🪑")

story.append(P("<b>Edge Case 4: Cycle Causing Infinite Loops</b>", sH2))
story += code_block([
    "## DANGER: traversal algorithm on a cyclic list loops forever",
    "## def find_length(head):  ## BROKEN if cycle exists",
    "##     count = 0",
    "##     curr  = head",
    "##     while curr:          ## Never terminates if curr.next = head",
    "##         count += 1",
    "##         curr  = curr.next",
    "",
    "## SAFE: detect cycle first if input may be cyclic",
    "def safe_traverse(head):",
    "    if has_cycle(head):   ## check before any traversal",
    "        handle_cycle()",
    "        return",
    "    ## Safe to traverse normally",
    "    curr = head",
    "    while curr:",
    "        process(curr.val)",
    "        curr = curr.next",
])

story.append(P("<b>Edge Case 5: Off-By-One in Gap Calculations</b>", sH3))
story += code_block([
    "## Removing N-th from end: advance front n+1 NOT n steps",
    "## Why n+1? We need back to stop at the PREVIOUS node, not the target.",
    "## With n steps: back lands ON the target → can't modify prev.next",
    "## With n+1 steps: back lands BEFORE target → back.next = back.next.next ✓",
    "",
    "## Reversing sublist from m to n:",
    "## Loop range(m-1) to walk pre to position m-1, NOT range(m)",
    "## Loop range(n-m+1) to reverse exactly n-m+1 nodes",
    "## Reconnect: pre.next.next = curr  (original m-th is now tail → link to curr)",
    "##            pre.next = prev       (pre → new head of reversed segment)",
])

story.append(P("<b>Master Edge Case Checklist</b>", sH2))
checks = [
    ("head is None",          "Guard at top of every function. Return None, 0, or appropriate sentinel."),
    ("Single node list",      "Test mentally: does your algorithm handle head.next = None correctly?"),
    ("Save next before rewire","Always: next_node = curr.next BEFORE curr.next = prev."),
    ("Dummy node when needed","Modifying head? Insert before head? Use dummy. Return dummy.next."),
    ("Cycle check",           "If problem doesn't guarantee acyclic, detect cycle before traversal."),
    ("Gap = n+1 for deletion","N-th from end deletion: advance n+1 steps, not n."),
    ("Identity vs equality",  "Cycle detection and circular traversal: use 'is' not '=='."),
    ("Even-length middle",    "Fast/slow for mid: 'while fast and fast.next' gives second middle."),
    ("Reconnect BOTH ends",   "Sublist reversal: reconnect pre→new_head AND old_head→remainder."),
    ("K-group completeness",  "K-group: check k nodes remain BEFORE each reversal, not after."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ] {q}</font></b>",
          S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[160, CW-160], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

# ── CHEAT SHEET ────────────────────────────────────────────────────────────────
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")
story.append(P("One-page reference for all patterns, templates, and pointer rules.", sBody))

cheat = [
    [th("Pattern"),              th("Pointers Used"),          th("Core Operation"),                    th("Classic Problem")],
    [td("Dummy Node",  C_ACCENT), tdc("dummy, curr"),           td("dummy.next=head; return dummy.next",  C_BODY), td("Merge Lists, Delete Node", C_MUTED)],
    [td("Find Middle", C_ACCENT2),tdc("slow(×1), fast(×2)"),   td("while fast and fast.next: advance",   C_BODY), td("Middle Node, Palindrome",  C_MUTED)],
    [td("Cycle Detect",C_GREEN),  tdc("slow(×1), fast(×2)"),   td("Phase 1: meet. Phase 2: reset slow", C_BODY), td("Cycle II, Find Duplicate",  C_MUTED)],
    [td("Gap / N-th",  C_PURPLE), tdc("front, back"),          td("Advance front n+1; sync-move both",   C_BODY), td("Remove Nth from End",      C_MUTED)],
    [td("3-Ptr Reversal",C_YELLOW),tdc("prev,curr,next_node"), td("Save,redirect,advance,advance",       C_BODY), td("Reverse List, Reverse m→n",C_MUTED)],
    [td("Merge Sorted",C_TEAL),   tdc("dummy,p1,p2,curr"),     td("Compare vals, attach min, advance",   C_BODY), td("Merge Two/K Sorted Lists", C_MUTED)],
    [td("Intersect",   C_ORANGE), tdc("pA, pB"),               td("Redirect to other head on None",     C_BODY), td("Intersection of Two Lists", C_MUTED)],
    [td("DLL + HashMap",C_ROSE),  tdc("head,tail,prev,next"),  td("Remove+InsertFront in O(1)",          C_BODY), td("LRU Cache",                C_MUTED)],
]
story.append(std_table(cheat, [95, 120, 185, 80]))
story.append(Spacer(1, 12))

story.append(Table([[
    P("<b>You now have the complete Linked List mental model.</b><br/><br/>"
      "Every linked list algorithm reduces to three primitives: "
      "<b>save a reference</b> before you need it, <b>rewire a pointer</b> "
      "to change structure, and <b>advance a pointer</b> along the chain. "
      "The dummy node, fast/slow, and gap techniques are just disciplined "
      "applications of these three moves.<br/><br/>"
      "Recommended path: LC 206 → LC 21 → LC 141 → LC 19 → LC 142 → LC 25 → LC 146. "
      "After these seven problems you will handle every pointer manipulation "
      "variant with confidence.",
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
        f"Linked List Patterns — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")