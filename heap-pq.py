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

PAGE_W, PAGE_H = letter
OUT = "/mnt/user-data/outputs/Heap_Priority_Queue_Zero_To_Hero.pdf"

doc = SimpleDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)
CW = PAGE_W - 1.3 * inch   # ≈ 518 pt

# ── Style helpers ──────────────────────────────────────────────────────────────
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
              textColor=C_GREEN,  alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
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


# ── Heap diagram (text-art table, guaranteed to fit in CW) ─────────────────────
def heap_diagram(rows_spec):
    """
    rows_spec: list of row dicts with keys:
      'cells': list of (text, bg_color | None) — empty string = spacer
      'widths': list of int (must sum <= CW)
    Returns a list of flowables.
    """
    result = []
    for row in rows_spec:
        cells  = []
        widths = []
        style_cmds = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),6),
            ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ]
        for ci, ((txt, bg), w) in enumerate(zip(row['cells'], row['widths'])):
            cells.append(P(txt,
                           S("_", fontName="Courier-Bold" if txt else "Courier",
                             fontSize=10, textColor=C_HEADING, alignment=TA_CENTER)))
            widths.append(w)
            if bg:
                style_cmds.append(("BACKGROUND",(ci,0),(ci,0), bg))
                style_cmds.append(("BOX",(ci,0),(ci,0), 1, C_BORDER))
        result.append(Table([cells], colWidths=widths,
                            style=TableStyle(style_cmds)))
    result.append(Spacer(1, 4))
    return result


def array_bar(vals, highlights=None, labels=None):
    """
    Compact horizontal array visualisation. Always CW wide.
    highlights: set of indices
    labels: dict {idx: str}
    """
    highlights = highlights or set()
    labels     = labels     or {}
    n          = len(vals)
    cell_w     = int(CW / (n + 0.5))  # leave a little margin

    idx_row = [P(f"<b>[{i}]</b>",
                 S("_", fontName="Courier-Bold", fontSize=8,
                   textColor=C_MUTED, alignment=TA_CENTER))
               for i in range(n)]
    val_row = []
    lbl_row = []
    style_cmds = [
        ("BOX",(0,1),(-1,1),1,C_BORDER),
        ("INNERGRID",(0,1),(-1,1),0.5,C_BORDER),
        ("BACKGROUND",(0,1),(-1,1),C_CARD),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,1),(-1,1),7),("BOTTOMPADDING",(0,1),(-1,1),7),
        ("TOPPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,0),(-1,0),2),
        ("TOPPADDING",(0,2),(-1,2),2),("BOTTOMPADDING",(0,2),(-1,2),2),
    ]
    for i, v in enumerate(vals):
        fg = C_TEAL if i in highlights else C_HEADING
        val_row.append(P(f"<b>{v}</b>",
                         S("_", fontName="Courier-Bold", fontSize=10,
                           textColor=fg, alignment=TA_CENTER)))
        lbl_row.append(P(labels.get(i, ""),
                         S("_", fontName="Helvetica", fontSize=7,
                           textColor=C_ACCENT2, alignment=TA_CENTER)))
        if i in highlights:
            style_cmds.append(("BACKGROUND",(i,1),(i,1),
                                colors.HexColor("#0A2E3A")))
    tbl = Table([idx_row, val_row, lbl_row],
                colWidths=[cell_w]*n,
                style=TableStyle(style_cmds))
    return [tbl, Spacer(1, 6)]


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
        f"Heap & Priority Queue Patterns — Zero to Hero  ·  Page {doc.page}")
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

story.append(P("HEAP &amp; PRIORITY QUEUE", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubT))
story.append(Spacer(1, 0.12*inch))
story.append(P("Partial Ordering · O(log n) Efficiency · Top-K · Merge K · Two-Heap Median", sAuthor))
story.append(Spacer(1, 0.18*inch))

story.append(Table([[
    P("<b>What You Will Master</b>",
      S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· Min-Heap and Max-Heap: the partial-order guarantee and why O(1) min/max matters\n"
       "· Array representation: parent/child index formulas and the complete-tree invariant\n"
       "· Top-K pattern: O(n log k) with a size-K min-heap — beating O(n log n) sort\n"
       "· Merge K Sorted Lists/Arrays: pointer-state tuples inside the heap\n"
       "· Two-Heap Median Finder: balancing a max-heap and min-heap for O(log n) inserts\n"
       "· Lazy Removal: marking deleted elements without breaking the heap invariant\n"
       "· Custom objects and tuples: comparison ordering and the unique-ID trick\n"
       "· Heapify O(n) vs successive insertions O(n log n) — why the math works\n"
       "· Heap vs Sorted Array vs BST decision table\n"
       "· 25+ categorised LeetCode problems with pattern labels and key insights",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))
]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CARD),
                      ("BOX",(0,0),(-1,-1),1,C_BORDER),
                      ("TOPPADDING",(0,0),(-1,-1),12),
                      ("BOTTOMPADDING",(0,0),(-1,-1),12),
                      ("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.22*inch))

# Quick-ref complexity card on cover
cx_data = [
    [th("Operation"),           th("Min/Max-Heap"),        th("Sorted Array"),           th("BST (balanced)"),     th("Unsorted Array")],
    [td("Find min or max"),     td("O(1)", C_GREEN),        td("O(1) endpoint", C_GREEN), td("O(log n)",C_YELLOW),  td("O(n)", C_RED)],
    [td("Insert"),              td("O(log n)", C_GREEN),    td("O(n) shift", C_RED),      td("O(log n)", C_GREEN),  td("O(1) amort.", C_GREEN)],
    [td("Delete min/max"),      td("O(log n)", C_GREEN),    td("O(1)+shift O(n)",C_RED),  td("O(log n)", C_GREEN),  td("O(n)", C_RED)],
    [td("Delete arbitrary"),    td("O(log n) lazy",C_YELLOW), td("O(n)", C_RED),          td("O(log n)", C_GREEN),  td("O(n)", C_RED)],
    [td("Build from n items"),  td("O(n) heapify",C_GREEN), td("O(n log n) sort",C_RED),  td("O(n log n)", C_RED),  td("O(1) as-is", C_GREEN)],
    [td("Kth element"),         td("O(n+k log n)",C_YELLOW), td("O(1) by index",C_GREEN), td("O(log n+k)",C_GREEN), td("O(n) scan", C_YELLOW)],
]
story.append(std_table(cx_data, [120, 90, 108, 108, 92]))
story.append(Spacer(1, 0.24*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),
                      ("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ────────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",
     ["Min-Heap vs Max-Heap","O(1) Find / O(log n) Insert+Delete",
      "Array Representation and Index Formulas"]),
    ("02","The Top-K Pattern",
     ["Min-Heap of Size K for Top-K Largest","O(n log k) vs O(n log n)",
      "Top-K Frequent Elements"]),
    ("03","Merge K Sorted Pattern",
     ["Priority Queue with Pointer State","Tuple Ordering in heapq",
      "Merge K Sorted Linked Lists"]),
    ("04","Two-Heap Median Finder",
     ["Max-Heap + Min-Heap Structure","Balance Invariant",
      "Add Number and Find Median"]),
    ("05","Lazy Removal & Custom Objects",
     ["Custom Comparison with Tuples","Lazy Deletion with a Validity Map",
      "The Removal Counter Pattern"]),
    ("06","Heapify O(n) vs Successive Insertions",
     ["Why Bottom-Up Heapify Wins","Sift-Down vs Sift-Up","When to Use Each"]),
    ("07","Comparison & Decision Making",
     ["Heap vs Sorted Array vs BST","Heap Sort vs Quick Sort",
      "Decision Flowchart"]),
    ("08","Problem Roadmap",
     ["Easy Problems","Medium Problems","Hard Problems"]),
    ("09","Edge Case Checklist",
     ["Empty Heap","K Greater than Array Size","Duplicates and Tie-breaking"]),
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

story.append(P("<b>Min-Heap and Max-Heap: Partial Ordering</b>", sH2))
story.append(P(
    "A <b>heap</b> is a complete binary tree that obeys the <b>heap property</b>. "
    "In a <b>min-heap</b>, every parent is less than or equal to its children — "
    "the global minimum always sits at the root and can be read in O(1). "
    "In a <b>max-heap</b>, every parent is greater than or equal to its children, "
    "placing the maximum at the root. "
    "This is <i>partial ordering</i>: sibling nodes carry no ordering guarantee "
    "relative to each other, only the parent-child axis is constrained. "
    "That relaxation is precisely why insertions and deletions cost O(log n) "
    "instead of O(n) — we only need to restore one path, not sort the whole tree.",
    sBody))

# ── Two heap diagrams side by side ────────────────────────────────────────────
# Min-heap [1, 3, 5, 7, 8, 9, 11]  — stored as text-art in two columns
LEFT  = int(CW * 0.49)
RIGHT = int(CW * 0.49)
GAP   = int(CW - LEFT - RIGHT)

N_BG  = colors.HexColor("#0D2035")   # generic node bg
R_BG  = colors.HexColor("#0A3A1A")   # root node bg (green tint)
MX_BG = colors.HexColor("#2E1A0A")   # max-heap root (orange tint)

def side_tree(label, rows, col_w):
    """
    rows: list of (text, bg_color | None, cell_pct_of_col_w)
    Flattened into a single-column card with centred ASCII art.
    """
    lines = [P(f"<b>{label}</b>",
               S("_", fontName="Helvetica-Bold", fontSize=10,
                 textColor=C_MUTED, alignment=TA_CENTER))]
    for row in rows:
        lines.append(P(row,
                       S("_", fontName="Courier", fontSize=9.5, leading=14,
                         textColor=C_BODY, alignment=TA_CENTER)))
    inner = [[l] for l in lines]
    return Table(inner, colWidths=[col_w],
                 style=TableStyle([
                     ("BACKGROUND",(0,0),(-1,-1),C_CARD),
                     ("BOX",(0,0),(-1,-1),1,C_BORDER),
                     ("TOPPADDING",(0,0),(-1,-1),5),
                     ("BOTTOMPADDING",(0,0),(-1,-1),5),
                     ("LEFTPADDING",(0,0),(-1,-1),8),
                     ("RIGHTPADDING",(0,0),(-1,-1),8),
                 ]))

min_tree = side_tree("MIN-HEAP  (root = global minimum)", [
    "        [ 1 ]",
    "       /     \\",
    "    [ 3 ]   [ 5 ]",
    "   /   \\   /   \\",
    " [7]  [8] [9] [11]",
    "",
    "Heap array: [1, 3, 5, 7, 8, 9, 11]",
    "heap[0] = 1  (minimum, O(1) access)",
], LEFT)

max_tree = side_tree("MAX-HEAP  (root = global maximum)", [
    "       [ 11 ]",
    "       /     \\",
    "    [ 8 ]   [ 9 ]",
    "   /   \\   /   \\",
    " [3]  [7] [5]  [1]",
    "",
    "Heap array: [11, 8, 9, 3, 7, 5, 1]",
    "heap[0] = 11  (maximum, O(1) access)",
], RIGHT)

story.append(Table([[min_tree, "", max_tree]],
                   colWidths=[LEFT, GAP, RIGHT],
                   style=TableStyle([
                       ("VALIGN",(0,0),(-1,-1),"TOP"),
                       ("TOPPADDING",(0,0),(-1,-1),0),
                       ("BOTTOMPADDING",(0,0),(-1,-1),0),
                       ("LEFTPADDING",(0,0),(-1,-1),0),
                       ("RIGHTPADDING",(0,0),(-1,-1),0),
                   ])))
story.append(Spacer(1, 10))

story += callout(
    "Partial ordering is the key insight: we only need the extreme value, not a "
    "fully sorted structure. By relaxing the sort requirement to just "
    "parent <= child (or >=), we unlock O(log n) insert/delete while keeping "
    "O(1) access to the one element we care about.",
    C_ACCENT, icon="💡")

story.append(P("<b>Array Representation and Index Formulas</b>", sH2))
story.append(P(
    "A heap is stored as a <b>flat array</b> — no pointer overhead, "
    "excellent cache locality. This works because a heap is a <b>complete binary tree</b>: "
    "all levels are fully filled except possibly the last, which fills left-to-right. "
    "That regularity lets us compute every parent-child relationship from indices alone.",
    sBody))

idx_data = [
    [th("Relationship"),  th("Formula (0-indexed)"), th("Example: i=1"), th("Intuition")],
    [td("Left child",  C_BODY), tdc("2*i + 1", C_GREEN),  tdc("2*1+1 = 3", C_TEAL),
     td("Each level doubles in size; left child opens next block",C_MUTED)],
    [td("Right child", C_BODY), tdc("2*i + 2", C_GREEN),  tdc("2*1+2 = 4", C_TEAL),
     td("Immediately follows left child in the array",C_MUTED)],
    [td("Parent",      C_BODY), tdc("(i-1)//2", C_ORANGE),tdc("(1-1)//2=0",C_TEAL),
     td("Integer division always truncates to the parent index",C_MUTED)],
    [td("Root",        C_BODY), tdc("index 0",  C_ACCENT), tdc("arr[0]",    C_TEAL),
     td("Always position 0; the only node with no parent",C_MUTED)],
    [td("Last internal node",C_BODY),tdc("n//2 - 1",C_ACCENT),tdc("7//2-1=2",C_TEAL),
     td("Start of heapify loop; leaves are indices n//2 through n-1",C_MUTED)],
]
story.append(std_table(idx_data, [105, 120, 90, 203]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Index arithmetic ───────────────────────────────────────────",
    "parent      = (i - 1) // 2",
    "left_child  = 2 * i + 1",
    "right_child = 2 * i + 2",
    "",
    "## ─── Sift-Up: restore heap after insertion ──────────────────────",
    "def sift_up(heap, i):          ## min-heap",
    "    while i > 0:",
    "        p = (i - 1) // 2",
    "        if heap[p] > heap[i]:  ## parent too large",
    "            heap[p], heap[i] = heap[i], heap[p]",
    "            i = p",
    "        else: break            ## heap property restored",
    "",
    "## ─── Sift-Down: restore heap after extraction ───────────────────",
    "def sift_down(heap, i, n):     ## min-heap",
    "    while True:",
    "        smallest, l, r = i, 2*i+1, 2*i+2",
    "        if l < n and heap[l] < heap[smallest]: smallest = l",
    "        if r < n and heap[r] < heap[smallest]: smallest = r",
    "        if smallest == i: break",
    "        heap[i], heap[smallest] = heap[smallest], heap[i]",
    "        i = smallest",
    "",
    "## ─── Python heapq: built-in min-heap API ────────────────────────",
    "import heapq",
    "heap = []",
    "heapq.heappush(heap, val)       ## O(log n) — insert, sift-up",
    "min_val = heapq.heappop(heap)   ## O(log n) — remove root, sift-down",
    "min_val = heap[0]               ## O(1)     — peek without removing",
    "",
    "## Max-heap: negate values on push, re-negate on pop",
    "heapq.heappush(max_heap, -val)",
    "max_val = -heapq.heappop(max_heap)",
    "max_val = -max_heap[0]          ## O(1) peek",
    "",
    "## Build from existing list in O(n)",
    "heapq.heapify(data)             ## in-place; see Section 06",
])
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §2  TOP-K PATTERN
# ════════════════════════════════════════════════════════
story += section_divider(2, "The Top-K Pattern")

story.append(P("<b>The Counterintuitive Insight: Min-Heap for Top-K Largest</b>", sH2))
story.append(P(
    "To find the <b>K largest</b> elements, maintain a <b>min-heap of size K</b>. "
    "This seems backwards — why a min-heap? Because the heap's root is the "
    "<i>smallest element currently in the top-K set</i>. "
    "When a new element arrives: if it is larger than the root (the current "
    "weakest qualifier), it deserves a spot in the top-K — pop the root and "
    "push the newcomer. The heap naturally evicts the weakest candidate.",
    sBody))

story += callout(
    "Memory hook: 'A min-heap of size K is a bouncer for the top-K club.' "
    "The root is the minimum qualifying score. Any new arrival must beat that score "
    "to enter. If they do, the current weakest member is evicted.",
    C_TEAL, icon="🏆")

story += code_block([
    "import heapq",
    "",
    "## ─── Top-K Largest — O(n log k) ────────────────────────────────",
    "def top_k_largest(nums, k):",
    "    heap = []                    ## min-heap, capped at size k",
    "    for num in nums:",
    "        heapq.heappush(heap, num)",
    "        if len(heap) > k:",
    "            heapq.heappop(heap)  ## evict the smallest (no longer top-k)",
    "    return list(heap)            ## the k largest (unordered)",
    "",
    "## ─── Kth Largest Element ────────────────────────────────────────",
    "def find_kth_largest(nums, k):",
    "    heap = []",
    "    for num in nums:",
    "        heapq.heappush(heap, num)",
    "        if len(heap) > k:",
    "            heapq.heappop(heap)",
    "    return heap[0]               ## root = kth largest",
    "",
    "## ─── Top-K Frequent Elements — O(n log k) ───────────────────────",
    "from collections import Counter",
    "def top_k_frequent(nums, k):",
    "    freq = Counter(nums)         ## {value: count}",
    "    heap = []",
    "    for val, cnt in freq.items():",
    "        heapq.heappush(heap, (cnt, val))  ## sort key = frequency",
    "        if len(heap) > k:",
    "            heapq.heappop(heap)           ## evict least frequent",
    "    return [val for cnt, val in heap]",
])

story.append(P("<b>Complexity: O(n log k) vs O(n log n)</b>", sH3))
cmp_data = [
    [th("Approach"),               th("Time"),            th("Space"),     th("Best when")],
    [td("Sort + slice"),           td("O(n log n)",C_YELLOW), td("O(n)",C_YELLOW),
     td("k is close to n; entire order needed",C_MUTED)],
    [td("Min-heap size K"),        td("O(n log k)",C_GREEN),  td("O(k)",C_GREEN),
     td("k << n; streaming data; memory constrained",C_MUTED)],
    [td("Quickselect (single Kth)"),  td("O(n) avg",C_GREEN),    td("O(1)",C_GREEN),
     td("Only the Kth element needed; not a set",C_MUTED)],
    [td("heapq.nlargest(k,data)"), td("O(n log k)",C_GREEN),  td("O(k)",C_GREEN),
     td("Convenience wrapper; same as manual heap approach",C_MUTED)],
]
story.append(std_table(cmp_data, [140, 85, 60, 233]))
story.append(Spacer(1, 8))

story.append(P("<b>Step-by-Step Trace: Top-3 Largest from [5, 3, 8, 1, 9, 2, 7]</b>", sH3))
trace_rows = [
    [th("Step"), th("Element"), th("Heap after (sorted)"), th("Action")],
    [tdc("push 5"),  tdc("5",C_HEADING), tdc("[5]",         C_ACCENT), td("size=1 < k=3; no eviction",C_MUTED)],
    [tdc("push 3"),  tdc("3",C_HEADING), tdc("[3, 5]",      C_ACCENT), td("size=2 < k=3; no eviction",C_MUTED)],
    [tdc("push 8"),  tdc("8",C_HEADING), tdc("[3, 5, 8]",   C_ACCENT), td("size=k=3; no eviction",C_MUTED)],
    [tdc("push 1"),  tdc("1",C_HEADING), tdc("[3, 5, 8]",   C_ACCENT), td("1 < heap[0]=3; skip (stays outside)",C_MUTED)],
    [tdc("push 9"),  tdc("9",C_GREEN),   tdc("[5, 8, 9]",   C_ACCENT), td("9 > heap[0]=3; push 9, pop 3",C_MUTED)],
    [tdc("push 2"),  tdc("2",C_HEADING), tdc("[5, 8, 9]",   C_ACCENT), td("2 < heap[0]=5; skip",C_MUTED)],
    [tdc("push 7"),  tdc("7",C_GREEN),   tdc("[7, 8, 9]",   C_ACCENT), td("7 > heap[0]=5; push 7, pop 5",C_MUTED)],
]
story.append(std_table(trace_rows, [75, 65, 135, 243]))
story.append(P("Final heap [7, 8, 9] — top-3 largest. heap[0]=7 is the 3rd largest.", sCaption))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §3  MERGE K SORTED
# ════════════════════════════════════════════════════════
story += section_divider(3, "Merge K Sorted Pattern")

story.append(P("<b>The Core Insight</b>", sH2))
story.append(P(
    "Given K sorted arrays (or linked lists) with N total elements, "
    "the naive approach concatenates all and re-sorts: O(N log N). "
    "The heap approach exploits existing order: at any moment, the next output "
    "element must be the minimum among all K current front elements. "
    "A min-heap of size K tracks exactly these K candidates — we pop the "
    "global minimum, then push the next element from that same source.",
    sBody))

story += code_block([
    "import heapq",
    "",
    "## ─── Merge K Sorted Arrays — O(N log K) ─────────────────────────",
    "## Heap tuple: (value, array_index, element_index)",
    "## Python compares tuples left-to-right; value drives the sort.",
    "## array_index and element_index are the 'pointer state'.",
    "",
    "def merge_k_arrays(arrays):",
    "    heap, result = [], []",
    "",
    "    ## Seed: push the first element of every non-empty array",
    "    for arr_i, arr in enumerate(arrays):",
    "        if arr:",
    "            heapq.heappush(heap, (arr[0], arr_i, 0))",
    "",
    "    while heap:",
    "        val, arr_i, elem_i = heapq.heappop(heap)   ## smallest front",
    "        result.append(val)",
    "        nxt = elem_i + 1",
    "        if nxt < len(arrays[arr_i]):                ## advance pointer",
    "            heapq.heappush(heap, (arrays[arr_i][nxt], arr_i, nxt))",
    "",
    "    return result",
    "## Time: O(N log K)  — N elements total, heap holds K items at once",
    "## Space: O(K)       — at most one entry per source array in the heap",
])

story.append(P("<b>Tuple Pointer State</b>", sH3))
state_data = [
    [th("Tuple Field"),    th("Role"),                            th("Why it's needed")],
    [tdc("value",C_ACCENT),td("Sort key — governs heap order",C_BODY),
     td("The actual value being merged into output",C_MUTED)],
    [tdc("arr_i", C_GREEN),td("Source array index",C_BODY),
     td("Tells us which array to advance after popping",C_MUTED)],
    [tdc("elem_i",C_YELLOW),td("Position within that source array",C_BODY),
     td("Lets us compute next_index = elem_i + 1",C_MUTED)],
]
story.append(std_table(state_data, [90, 215, 213]))
story.append(Spacer(1, 8))

story.append(P("<b>Trace: Merge 3 Arrays  A=[1,4,7]  B=[2,5,8]  C=[3,6,9]</b>", sH3))
mt_rows = [
    [th("Action"), th("Heap (values)"), th("Output so far"), th("Next push")],
    [td("Seed"),           tdc("[1,2,3]",  C_ACCENT), tdc("[]",C_MUTED),   td("first of each array",C_MUTED)],
    [td("Pop 1 (A,idx=0)"),tdc("[2,3,4]",  C_ACCENT), tdc("[1]",C_GREEN),  td("push A[1]=4",C_MUTED)],
    [td("Pop 2 (B,idx=0)"),tdc("[3,4,5]",  C_ACCENT), tdc("[1,2]",C_GREEN),td("push B[1]=5",C_MUTED)],
    [td("Pop 3 (C,idx=0)"),tdc("[4,5,6]",  C_ACCENT), tdc("[1,2,3]",C_GREEN),td("push C[1]=6",C_MUTED)],
    [td("Pop 4 (A,idx=1)"),tdc("[5,6,7]",  C_ACCENT), tdc("[1..4]",C_GREEN),td("push A[2]=7",C_MUTED)],
    [td("... continues"), tdc("...",       C_MUTED),  tdc("[1..9]",C_GREEN),td("all sources exhausted",C_MUTED)],
]
story.append(std_table(mt_rows, [145, 110, 110, 153]))
story.append(P("Result: [1,2,3,4,5,6,7,8,9]  — O(N log K) where K=3, N=9", sCaption))
story.append(Spacer(1, 8))

story.append(P("<b>Merge K Sorted Linked Lists</b>", sH3))
story += code_block([
    "## Problem: if two ListNodes have equal .val, Python tries to compare",
    "## the nodes themselves — raising TypeError if __lt__ is not defined.",
    "## Fix: include a unique counter (uid) as a tie-breaker.",
    "",
    "def merge_k_lists(lists):",
    "    heap = []",
    "    dummy = result = ListNode(0)",
    "    uid = 0",
    "",
    "    for node in lists:",
    "        if node:",
    "            heapq.heappush(heap, (node.val, uid, node))",
    "            uid += 1",
    "",
    "    while heap:",
    "        val, _, node = heapq.heappop(heap)",
    "        result.next = node",
    "        result = result.next",
    "        if node.next:",
    "            heapq.heappush(heap, (node.next.val, uid, node.next))",
    "            uid += 1",
    "",
    "    return dummy.next",
    "## The uid counter guarantees Python never reaches the ListNode comparison.",
])
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §4  TWO-HEAP MEDIAN
# ════════════════════════════════════════════════════════
story += section_divider(4, "Two-Heap Median Finder")

story.append(P("<b>The Challenge and the Structure</b>", sH2))
story.append(P(
    "Find the median of a dynamically growing data stream. "
    "Sorting after each insertion costs O(n log n) per query. "
    "The two-heap approach keeps O(log n) per insertion and O(1) median "
    "by splitting the data at the midpoint: "
    "the <b>smaller half</b> lives in a max-heap (so we instantly know the "
    "largest of the small numbers) and the <b>larger half</b> in a min-heap "
    "(so we instantly know the smallest of the large numbers). "
    "The median always lives at this boundary.",
    sBody))

inv_data = [
    [th("Property"),                    th("Rule")],
    [td("lo  = max-heap",  C_ACCENT),
     td("Stores the smaller half. Root = max of smaller half.  Negate for Python.", C_BODY)],
    [td("hi  = min-heap",  C_GREEN),
     td("Stores the larger half.  Root = min of larger half.", C_BODY)],
    [td("Balance invariant", C_YELLOW),
     td("len(lo) == len(hi)  OR  len(lo) == len(hi) + 1  (lo may hold the extra)", C_BODY)],
    [td("Cross invariant",  C_PURPLE),
     td("Every element in lo must be <= every element in hi.", C_BODY)],
    [td("Median — even total", C_BODY),
     tdc("(-lo[0] + hi[0]) / 2", C_GREEN)],
    [td("Median — odd total",  C_BODY),
     tdc("-lo[0]   (lo holds the middle element)", C_GREEN)],
]
story.append(std_table(inv_data, [150, 368]))
story.append(Spacer(1, 8))

story.append(P("<b>Stream [5, 15, 1, 3] — State After Each Insertion</b>", sH3))
th_rows = [
    [th("Add"), th("lo (max-heap, negated)"), th("hi (min-heap)"), th("Median"), th("Note")],
    [tdc("5",C_HEADING), tdc("[-5]",C_ACCENT),    tdc("[]",C_MUTED),    tdc("5.0",C_PURPLE),
     td("5 to lo; hi empty",C_MUTED)],
    [tdc("15",C_HEADING),tdc("[-5]",C_ACCENT),    tdc("[15]",C_GREEN),  tdc("10.0",C_PURPLE),
     td("15 > lo.top=5; push to hi",C_MUTED)],
    [tdc("1",C_HEADING), tdc("[-5,-1]",C_ACCENT), tdc("[15]",C_GREEN),  tdc("5.0",C_PURPLE),
     td("1 <= lo.top; push to lo; lo has extra",C_MUTED)],
    [tdc("3",C_HEADING), tdc("[-3,-1]",C_ACCENT), tdc("[5,15]",C_GREEN),tdc("4.0",C_PURPLE),
     td("3 to lo; lo overflows; move lo.top=5 to hi",C_MUTED)],
]
story.append(std_table(th_rows, [45, 140, 120, 75, 138]))
story.append(Spacer(1, 8))

story += code_block([
    "import heapq",
    "",
    "class MedianFinder:",
    "    def __init__(self):",
    "        self.lo = []   ## max-heap (negate): holds smaller half",
    "        self.hi = []   ## min-heap: holds larger half",
    "",
    "    def add_num(self, num):",
    "        ## Step 1: always push to lo first",
    "        heapq.heappush(self.lo, -num)",
    "",
    "        ## Step 2: enforce cross-invariant (all lo <= all hi)",
    "        if self.hi and (-self.lo[0]) > self.hi[0]:",
    "            heapq.heappush(self.hi, -heapq.heappop(self.lo))",
    "",
    "        ## Step 3: rebalance sizes",
    "        if len(self.lo) > len(self.hi) + 1:",
    "            heapq.heappush(self.hi, -heapq.heappop(self.lo))",
    "        elif len(self.hi) > len(self.lo):",
    "            heapq.heappush(self.lo, -heapq.heappop(self.hi))",
    "",
    "    def find_median(self):",
    "        if len(self.lo) > len(self.hi):",
    "            return float(-self.lo[0])          ## odd: lo holds middle",
    "        return (-self.lo[0] + self.hi[0]) / 2  ## even: average of two middles",
    "",
    "## add_num: O(log n)    find_median: O(1)",
])
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §5  LAZY REMOVAL & CUSTOM OBJECTS
# ════════════════════════════════════════════════════════
story += section_divider(5, "Lazy Removal & Custom Objects")

story.append(P("<b>Custom Objects: The Comparison Problem</b>", sH2))
story.append(P(
    "Python's heapq compares heap elements directly. "
    "For integers this is trivial. For custom objects or classes without "
    "<b>__lt__</b>, Python raises a TypeError when two elements tie on "
    "their first comparison field. "
    "The safest pattern: always store <b>(priority, uid, object)</b> tuples — "
    "the uid (an auto-incrementing counter) breaks every tie before Python "
    "reaches the object comparison.",
    sBody))

story += code_block([
    "import heapq",
    "",
    "## ─── Safe tuple pattern: (priority, uid, object) ───────────────",
    "uid_counter = 0",
    "",
    "def push_task(heap, priority, task):",
    "    global uid_counter",
    "    heapq.heappush(heap, (priority, uid_counter, task))",
    "    uid_counter += 1",
    "",
    "def pop_task(heap):",
    "    priority, uid, task = heapq.heappop(heap)",
    "    return task",
    "",
    "## ─── dataclass with order=True (alternative) ────────────────────",
    "from dataclasses import dataclass, field",
    "",
    "@dataclass(order=True)",
    "class HeapItem:",
    "    priority: int",
    "    item: object = field(compare=False)  ## excluded from comparison",
    "",
    "## WRONG: heapq.heappush(heap, -(freq, val))  -> TypeError on tuple negation",
    "## RIGHT: heapq.heappush(heap, (-freq, val))  -> negate the sort key only",
])

story.append(P("<b>Lazy Removal: Deleting Non-Root Elements</b>", sH2))
story.append(P(
    "Heaps give O(log n) delete-min but O(n) arbitrary deletion "
    "(you must find the element first). "
    "<b>Lazy removal</b> defers the work: mark an element as deleted in a "
    "separate structure, and skip it the next time it surfaces at the top. "
    "The true deletion happens at the cost of the next pop — amortised O(log n).",
    sBody))

story += code_block([
    "import heapq",
    "from collections import defaultdict",
    "",
    "## ─── Lazy Removal with a removal-count map ──────────────────────",
    "class LazyHeap:",
    "    def __init__(self):",
    "        self.heap   = []",
    "        self.dead   = defaultdict(int)  ## {value: count marked removed}",
    "        self.size   = 0",
    "",
    "    def push(self, val):",
    "        heapq.heappush(self.heap, val)",
    "        self.size += 1",
    "",
    "    def remove(self, val):",
    "        self.dead[val] += 1   ## mark; does not touch the heap",
    "        self.size -= 1",
    "",
    "    def _clean(self):",
    "        ## Discard dead elements sitting at the top",
    "        while self.heap and self.dead[self.heap[0]] > 0:",
    "            self.dead[self.heap[0]] -= 1",
    "            heapq.heappop(self.heap)",
    "",
    "    def top(self):",
    "        self._clean()",
    "        return self.heap[0] if self.heap else None",
    "",
    "    def pop(self):",
    "        self._clean()",
    "        self.size -= 1",
    "        return heapq.heappop(self.heap)",
    "",
    "## Uses: Sliding Window Median (LC 480), Task Scheduler variants,",
    "## Dijkstra's algorithm (stale distance entries are 'lazy removed').",
])

story += callout(
    "Lazy removal trades memory for time. The heap may accumulate O(n) stale entries, "
    "but each is cleaned at the next real pop — amortised O(log n). "
    "Use defaultdict(int) counts (not a set) when duplicate values exist.",
    C_PURPLE, icon="🗑️")
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §6  HEAPIFY O(n) vs INSERTIONS
# ════════════════════════════════════════════════════════
story += section_divider(6, "Heapify O(n) vs. Successive Insertions")

story.append(P("<b>Why Building a Heap is Faster Than Inserting One by One</b>", sH2))
story.append(P(
    "Given n elements, there are two ways to build a heap. "
    "The naive method calls heappush n times: each costs O(log n), "
    "giving <b>O(n log n)</b> total. "
    "Floyd's <b>heapify</b> algorithm runs in <b>O(n)</b> by processing the array "
    "bottom-up, calling sift-down only on internal nodes. "
    "The key: most nodes are near the bottom where sift-down is very cheap — "
    "half the nodes are leaves (zero swaps), a quarter need at most one swap, "
    "an eighth at most two, and so on. The costs form a geometric series.",
    sBody))

story.append(P(
    "Total work  =  n/2 x 0  +  n/4 x 1  +  n/8 x 2  +  n/16 x 3  +  ...  =  O(n)",
    sFormula))
story.append(Spacer(1, 4))

story += code_block([
    "## ─── Floyd's Heapify — O(n) ─────────────────────────────────────",
    "def heapify(arr):",
    "    n = len(arr)",
    "    ## Start from the last internal node; leaves are already valid heaps",
    "    for i in range(n // 2 - 1, -1, -1):  ## n//2-1 down to 0",
    "        sift_down(arr, i, n)",
    "",
    "## Why n//2-1?  Last leaf = index n-1.",
    "## Its parent = (n-1-1)//2 = (n-2)//2 = n//2-1.",
    "## All nodes at index >= n//2 are leaves — trivially valid.",
    "",
    "## Python shortcut (identical algorithm, built-in):",
    "heapq.heapify(data)   ## O(n), in-place",
    "",
    "## Verify: heapq.heapify([5,3,8,1,9,2]) -> [1,3,2,5,9,8]",
    "## Array satisfies heap property without being fully sorted.",
])

hfy_data = [
    [th("Method"),                    th("Algorithm"),                    th("Time"),          th("Best when")],
    [td("heapq.heapify"),             td("Bottom-up sift-down, n//2 calls",C_BODY),  td("O(n)",C_GREEN),
     td("All data available upfront; single batch build",C_MUTED)],
    [td("n x heappush"),              td("One insert per element, sift-up each",C_BODY),td("O(n log n)",C_YELLOW),
     td("Streaming data; elements arrive one by one",C_MUTED)],
    [td("heapq.nsmallest(k, data)"),  td("heapify then k pops",         C_BODY),    td("O(n + k log n)",C_GREEN),
     td("Convenience wrapper for Top-K from a static list",C_MUTED)],
]
story.append(std_table(hfy_data, [130, 200, 90, 98]))
story.append(Spacer(1, 8))

story.append(P("<b>Sift-Down vs Sift-Up: When Each Is Used</b>", sH3))
sv_data = [
    [th("Operation"),        th("Uses"),     th("Direction"),         th("Cost"),     th("Why")],
    [td("heappush"),         td("Sift-Up",C_ACCENT),   td("child to root"),  tdc("O(log n)"),
     td("New element inserted at end; may violate with parent",C_MUTED)],
    [td("heappop"),          td("Sift-Down",C_GREEN),  td("root to leaf"),   tdc("O(log n)"),
     td("Root replaced by last element; may violate with children",C_MUTED)],
    [td("heapify"),          td("Sift-Down x n/2",C_GREEN),td("each internal"), tdc("O(n)"),
     td("Bottom-up; nodes near bottom have short paths",C_MUTED)],
    [td("decrease-key"),     td("Sift-Up",C_ACCENT),   td("node to root"),   tdc("O(log n)"),
     td("Priority lowered; node may now be smaller than parent",C_MUTED)],
]
story.append(std_table(sv_data, [90, 100, 110, 70, 148]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §7  COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(7, "Comparison & Decision Making")

story.append(P("<b>Heap vs Sorted Array vs BST</b>", sH2))
full_cmp = [
    [th("Dimension"),          th("Heap"),                        th("Sorted Array"),             th("BST (balanced)")],
    [td("Find min/max"),       td("O(1) — root",C_GREEN),          td("O(1) — endpoint",C_GREEN),  td("O(log n)",C_YELLOW)],
    [td("Insert"),             td("O(log n)",C_GREEN),              td("O(n) — shift",C_RED),       td("O(log n)",C_GREEN)],
    [td("Delete min/max"),     td("O(log n)",C_GREEN),              td("O(n) — shift after",C_RED), td("O(log n)",C_GREEN)],
    [td("Delete arbitrary"),   td("O(log n) lazy / O(n) naive",C_YELLOW),td("O(n)",C_RED),         td("O(log n)",C_GREEN)],
    [td("Search by value"),    td("O(n)",C_RED),                    td("O(log n) binary search",C_GREEN),td("O(log n)",C_GREEN)],
    [td("Kth element"),        td("O(k log n)",C_YELLOW),           td("O(1) by index",C_GREEN),    td("O(log n + k)",C_GREEN)],
    [td("Build from n items"), td("O(n) heapify",C_GREEN),          td("O(n log n) sort",C_RED),    td("O(n log n)",C_RED)],
    [td("Memory overhead"),    td("O(n) array, no pointers",C_GREEN),td("O(n) array",C_GREEN),      td("O(n) + pointer overhead",C_YELLOW)],
    [td("Cache performance"),  td("Good — array-backed",C_GREEN),   td("Excellent — sequential",C_GREEN),td("Poor — pointer chasing",C_RED)],
    [td("Best for"),
     td("Streaming min/max, priority queues, Top-K, task scheduling",C_MUTED),
     td("Static sorted data, range queries, O(1) index access",C_MUTED),
     td("Dynamic sorted data, predecessor/successor, rank queries",C_MUTED)],
]
story.append(std_table(full_cmp, [130, 155, 125, 108]))
story.append(Spacer(1, 10))

story.append(P("<b>Heap Sort vs Quick Sort</b>", sH2))
sort_cmp = [
    [th("Dimension"),          th("Heap Sort"),                                th("Quick Sort")],
    [td("Time — worst case"),  td("O(n log n) guaranteed",C_GREEN),             td("O(n^2) — bad pivot choice",C_RED)],
    [td("Time — average"),     td("O(n log n)",C_GREEN),                        td("O(n log n)",C_GREEN)],
    [td("Extra space"),        td("O(1) — in-place",C_GREEN),                   td("O(log n) — stack frames",C_YELLOW)],
    [td("Stable?"),            td("No — swaps disrupt original order",C_RED),   td("No — typical implementations",C_RED)],
    [td("Cache behaviour"),    td("Poor — accesses scattered heap positions",C_RED),td("Good — sequential partition scans",C_GREEN)],
    [td("Practical speed"),    td("2-3x slower in practice (cache misses)",C_YELLOW),td("Fastest in practice",C_GREEN)],
    [td("Use when"),
     td("Worst-case O(n log n) required; O(1) extra space needed",C_MUTED),
     td("Average-case performance; data fits in cache; typical production use",C_MUTED)],
]
story.append(std_table(sort_cmp, [125, 195, 198]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow_rows = [
    ("Q1", "Do you need to repeatedly access the minimum OR maximum?",        C_ACCENT,  False),
    (" YES", "Use a Heap. O(1) access, O(log n) insert/delete.",               C_GREEN,   True),
    (" NO",  "Continue to Q2.",                                                C_MUTED,   True),
    ("Q2", "Do you need the TOP-K elements from a stream or large array?",    C_ACCENT,  False),
    (" YES", "Min-heap of size K. O(n log k) beats O(n log n) sort.",         C_GREEN,   True),
    (" NO",  "Continue to Q3.",                                                C_MUTED,   True),
    ("Q3", "Do you need to merge K sorted sequences?",                        C_ACCENT,  False),
    (" YES", "Heap with (value, source_id, index) tuples. O(N log K).",       C_TEAL,    True),
    (" NO",  "Continue to Q4.",                                                C_MUTED,   True),
    ("Q4", "Do you need a running median from a data stream?",                C_ACCENT,  False),
    (" YES", "Two Heaps (lo max-heap + hi min-heap). O(log n) add, O(1) median.",C_PURPLE,True),
    (" NO",  "Continue to Q5.",                                                C_MUTED,   True),
    ("Q5", "Do you need O(log n) search or predecessor/successor queries?",   C_ACCENT,  False),
    (" YES", "BST (Python: sortedcontainers.SortedList).",                    C_YELLOW,  True),
    (" NO",  "Sorted Array if data is static; Heap if dynamic min/max is the goal.",C_MUTED,True),
]
for label, text, clr, is_branch in flow_rows:
    bg = C_DARK2 if is_branch else C_CARD
    story.append(Table([[
        P(f"<b>{label}</b>",
          S("_", fontName="Courier-Bold" if not is_branch else "Courier",
            fontSize=9, textColor=clr)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[55, CW-55],
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
story.append(P("Solve in order — each problem exercises exactly one new heap technique.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy = [
    [th("#"), th("Problem"),                                  th("Pattern"),         th("Key Insight")],
    [tdc("703", C_GREEN),  td("Kth Largest in a Stream",     C_BODY),
     td("Min-heap size K", C_ACCENT),  td("heap[0] is always the Kth largest after each push.",C_MUTED)],
    [tdc("1046",C_GREEN),  td("Last Stone Weight",           C_BODY),
     td("Max-heap",        C_ACCENT2), td("Negate values. Pop two; push |diff| if nonzero.",C_MUTED)],
    [tdc("1337",C_GREEN),  td("K Weakest Rows in a Matrix",  C_BODY),
     td("Min-heap",        C_ACCENT),  td("Heap of (soldier_count, row_idx); pop K times.",C_MUTED)],
    [tdc("2099",C_GREEN),  td("Find Subseq of Length K with Largest Sum",C_BODY),
     td("Min-heap size K", C_ACCENT),  td("Keep top-K by value; return sorted positions.",C_MUTED)],
]
story.append(std_table(easy, [38, 215, 125, 140]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med = [
    [th("#"), th("Problem"),                                      th("Pattern"),             th("Key Insight")],
    [tdc("215", C_YELLOW), td("Kth Largest in an Array",         C_BODY),
     td("Min-heap size K",    C_ACCENT),    td("Classic top-K. heap[0] after n inserts = answer.",C_MUTED)],
    [tdc("347", C_YELLOW), td("Top K Frequent Elements",         C_BODY),
     td("Min-heap by freq",   C_ACCENT),    td("Counter + heap of (freq, val); evict least frequent.",C_MUTED)],
    [tdc("973", C_YELLOW), td("K Closest Points to Origin",      C_BODY),
     td("Max-heap size K",    C_ACCENT2),   td("Negate distance; heap of (-dist, x, y).",C_MUTED)],
    [tdc("378", C_YELLOW), td("Kth Smallest in Sorted Matrix",   C_BODY),
     td("Min-heap + pointer", C_TEAL),      td("Seed first column; pop, push next in same row.",C_MUTED)],
    [tdc("621", C_YELLOW), td("Task Scheduler",                  C_BODY),
     td("Max-heap + cooldown",C_PURPLE),    td("Always schedule most frequent available task.",C_MUTED)],
    [tdc("1642",C_YELLOW), td("Furthest Building You Can Reach", C_BODY),
     td("Min-heap (ladders)", C_ACCENT),    td("Swap smallest ladder use for bricks retroactively.",C_MUTED)],
    [tdc("295", C_YELLOW), td("Find Median from Data Stream",    C_BODY),
     td("Two Heaps",          C_ORANGE),    td("lo=max-heap + hi=min-heap; balance after each add.",C_MUTED)],
    [tdc("767", C_YELLOW), td("Reorganize String",               C_BODY),
     td("Max-heap greedy",    C_ACCENT2),   td("Place most-frequent char that isn't last placed.",C_MUTED)],
    [tdc("355", C_YELLOW), td("Design Twitter",                  C_BODY),
     td("Merge K sorted",     C_TEAL),      td("Heap over per-user tweet lists; top-10 feed.",C_MUTED)],
]
story.append(std_table(med, [38, 210, 130, 140]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard = [
    [th("#"), th("Problem"),                                   th("Pattern"),             th("Key Insight")],
    [tdc("23",  C_RED),  td("Merge K Sorted Lists",           C_BODY),
     td("Merge K + uid",          C_TEAL),   td("(val, uid, node); push node.next after each pop.",C_MUTED)],
    [tdc("632", C_RED),  td("Smallest Range Covering K Lists",C_BODY),
     td("Min-heap + global max",  C_ORANGE),  td("Heap of (val, list_i, elem_i); range=max-heap[0].",C_MUTED)],
    [tdc("480", C_RED),  td("Sliding Window Median",           C_BODY),
     td("Two Heaps + lazy remove",C_PURPLE),  td("Two-heap median + lazy-delete expired elements.",C_MUTED)],
    [tdc("857", C_RED),  td("Minimum Cost to Hire K Workers",  C_BODY),
     td("Max-heap + sort",        C_ACCENT2), td("Sort by wage/quality; max-heap of size K on quality.",C_MUTED)],
    [tdc("1675",C_RED),  td("Minimize Deviation in Array",     C_BODY),
     td("Max-heap + transform",   C_RED),     td("Make all even; halve max; track global min.",C_MUTED)],
]
story.append(std_table(hard, [38, 200, 140, 140]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §9  EDGE CASE CHECKLIST
# ════════════════════════════════════════════════════════
story += section_divider(9, "Edge Case Checklist")

story.append(P(
    "Heap problems share a predictable set of failure modes. "
    "Test every solution mentally against each item below before submitting.",
    sBody))

story.append(P("<b>Edge Case 1: Empty Heap Operations</b>", sH2))
story += code_block([
    "## heapq.heappop([]) raises IndexError — always guard:",
    "if heap:",
    "    val = heapq.heappop(heap)",
    "",
    "## heap[0] on empty list also raises IndexError:",
    "top = heap[0] if heap else None",
    "",
    "## Two-Heap median on an empty stream:",
    "def find_median(lo, hi):",
    "    if not lo and not hi: return None",
    "    if len(lo) > len(hi): return float(-lo[0])",
    "    return (-lo[0] + hi[0]) / 2.0",
    "",
    "## Merge K: guard against empty source arrays during seeding:",
    "for arr_i, arr in enumerate(arrays):",
    "    if arr:             ## <- critical: skip empty arrays",
    "        heapq.heappush(heap, (arr[0], arr_i, 0))",
])

story.append(P("<b>Edge Case 2: K Greater than or Equal to Array Size</b>", sH2))
story += code_block([
    "## 'Kth largest' when k > len(nums) — clamp or return all:",
    "def find_kth_largest(nums, k):",
    "    k = min(k, len(nums))        ## clamp: return the smallest element",
    "    ## ... rest of algorithm",
    "",
    "## 'Top-K' when k == 0 — return immediately:",
    "def top_k_largest(nums, k):",
    "    if k <= 0: return []",
    "    if k >= len(nums): return nums   ## entire array qualifies",
    "    ## ... heap algorithm",
    "",
    "## 'Top-K Frequent' when k == total unique elements:",
    "## Counter produces exactly len(freq) items; heap never over-evicts.",
    "## No special guard needed as long as k <= len(Counter(nums)).",
])

story.append(P("<b>Edge Case 3: Duplicate Values and Tie-breaking</b>", sH2))
story += code_block([
    "## heapq handles duplicate integer values correctly.",
    "## Duplicates may appear in any relative order (heapq is not stable).",
    "",
    "## Duplicates in custom tuple heaps:",
    "## (priority, uid, obj) — uid guarantees Python never compares obj.",
    "## WITHOUT uid: (1, task_A) vs (1, task_B) -> Python compares task_A",
    "## If task objects lack __lt__, this raises TypeError.",
    "",
    "## Lazy removal with DUPLICATE values — use a count map, not a set:",
    "from collections import defaultdict",
    "dead = defaultdict(int)",
    "",
    "def lazy_remove(val):",
    "    dead[val] += 1           ## one more copy is logically deleted",
    "",
    "def clean_pop(heap):",
    "    while heap and dead[heap[0]] > 0:",
    "        dead[heap[0]] -= 1",
    "        heapq.heappop(heap)",
    "    return heapq.heappop(heap) if heap else None",
    "",
    "## Two-heap with duplicates: balance logic is unaffected.",
    "## If lo.top == hi.top, the median is simply that shared value.",
])

story.append(P("<b>Edge Case 4: Negating Non-Integer Types</b>", sH3))
story += code_block([
    "## Negate ONLY the sort-key field of a tuple:",
    "## WRONG: heapq.heappush(heap, -(freq, val))  -> TypeError",
    "## RIGHT: heapq.heappush(heap, (-freq, val))  -> correct",
    "",
    "## Float negation works fine in Python (no overflow):",
    "heapq.heappush(max_heap, -3.14)          ## OK",
    "heapq.heappush(max_heap, -float('inf'))  ## represents +inf on pop",
    "",
    "## Consistent negation in the Two-Heap pattern:",
    "heapq.heappush(self.lo, -num)            ## lo stores negated values",
    "top_of_lo = -self.lo[0]                  ## un-negate when reading",
])

story += callout(
    "Quick reminder: -self.lo[0] un-negates the max-heap root. "
    "Always re-negate when moving from lo to hi: "
    "heapq.heappush(hi, -heapq.heappop(lo)).",
    C_RED, icon="⚠️")

# ── MASTER CHEAT SHEET ─────────────────────────────────────────────────────────
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")

cheat = [
    [th("Pattern"),             th("Heap Type"),         th("Key Operation"),                th("Classic Problem")],
    [td("Find min/max",C_ACCENT),  tdc("min or max heap"), td("heap[0] — O(1)",C_BODY),       td("Kth Largest, Scheduler",C_MUTED)],
    [td("Top-K Largest",C_ACCENT), tdc("min-heap size K"), td("evict if len > K",C_BODY),     td("LC 215, 347, 973",C_MUTED)],
    [td("Top-K Smallest",C_ACCENT2),tdc("max-heap size K"),td("negate + evict if len > K",C_BODY),td("LC 378, K Closest",C_MUTED)],
    [td("Merge K Sorted",C_TEAL),  tdc("min-heap"),        td("(val, arr_i, elem_i) tuples",C_BODY),td("LC 23, 632",C_MUTED)],
    [td("Two-Heap Median",C_ORANGE),tdc("lo=max, hi=min"), td("balance sizes after every add",C_BODY),td("LC 295, 480",C_MUTED)],
    [td("Lazy Removal",C_PURPLE),  tdc("any heap"),        td("defaultdict(int) count map",C_BODY),td("LC 480, Dijkstra",C_MUTED)],
    [td("Custom objects",C_ROSE),  tdc("any heap"),        td("(priority, uid, obj) tuple",C_BODY),td("LC 23, 355",C_MUTED)],
    [td("Heapify",C_GREEN),        tdc("any heap"),        td("heapq.heapify(arr) — O(n)",C_BODY),  td("Batch heap build",C_MUTED)],
    [td("Heap Sort",C_YELLOW),     tdc("max-heap"),        td("heapify + n x sift-down",C_BODY),    td("In-place O(1) space sort",C_MUTED)],
]
story.append(std_table(cheat, [135, 110, 165, 108]))
story.append(Spacer(1, 10))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
checks = [
    ("Min or Max heap?",       "Python heapq is min-heap only. For max: negate on push, re-negate on pop."),
    ("Negate tuple correctly?","(-freq, val) — negate the sort key field only, never the whole tuple."),
    ("K > array size?",        "Clamp k = min(k, len(nums)) or return all elements if k >= n."),
    ("Empty heap guard?",      "Check 'if heap:' before heappop() or heap[0]. heapq never self-guards."),
    ("Custom object tie-break?","Always use (priority, uid, obj). uid counter prevents TypeError."),
    ("Lazy removal duplicates?","Use defaultdict(int) count map, not a set, when values repeat."),
    ("Top-K largest vs smallest?","Largest -> min-heap size K. Smallest -> max-heap size K (negate)."),
    ("Two-heap balance?",      "After every add: len(lo) == len(hi) or len(lo) == len(hi) + 1."),
    ("Merge K seed guard?",    "'if arr:' before pushing first element of each source array."),
    ("Heapify available?",     "If all data is upfront: heapq.heapify(arr) in O(n), not n pushes."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ]  {q}</font></b>",
          S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[180, CW-180],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_CARD),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

story.append(Table([[P(
    "<b>You now have the complete Heap &amp; Priority Queue mental model.</b><br/><br/>"
    "Every heap problem reduces to one question: "
    "<i>which extreme value do I need, and how often does it change?</i><br/><br/>"
    "Repeated min/max on a dynamic set — that is a heap.  "
    "The K-th extreme — that is a size-K heap acting as a filter.  "
    "Two extremes simultaneously (median) — that is two heaps balanced "
    "around a boundary.<br/><br/>"
    "Recommended path: LC 703 → LC 215 → LC 347 → LC 23 → LC 295 → LC 480 → LC 632. "
    "These seven problems exercise every major pattern: "
    "basic heap, top-K, top-K frequent, merge-K, two-heap, lazy removal, "
    "and the hardest merge-K variant.",
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