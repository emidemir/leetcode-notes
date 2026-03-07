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
C_INDIGO  = colors.HexColor("#6366F1")

PAGE_W, PAGE_H = letter

doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Binary_Tree_Patterns_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)
CW = PAGE_W - 1.3*inch

# ── Style factory ──────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("T",  fontName="Helvetica-Bold",   fontSize=30, leading=38, textColor=C_HEADING, alignment=TA_CENTER, spaceAfter=6)
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
sNodeLbl = S("NL", fontName="Courier-Bold",     fontSize=9,  textColor=C_HEADING, alignment=TA_CENTER)

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

# ── Tree diagram builder ───────────────────────────────────────────────────────
def tree_diagram(node_rows, edge_rows=None, caption=""):
    """
    node_rows: list of lists of (label, color, width) or None for empty slots.
    Renders a text-art tree using a table grid.
    """
    all_rows = []
    for row in node_rows:
        cells = []
        widths = []
        for item in row:
            if item is None:
                cells.append(P("", sCaption))
                widths.append(30)
            else:
                lbl, clr, w = item
                cells.append(P(f"<b>{lbl}</b>",
                    S("_", fontName="Courier-Bold", fontSize=10,
                      textColor=C_HEADING, alignment=TA_CENTER)))
                widths.append(w)
        all_rows.append((cells, widths))

    # All rows must share column widths — use first row's widths
    if not all_rows:
        return [Spacer(1,4)]
    col_ws = all_rows[0][1]
    tbl_data = [r[0] for r in all_rows]

    style_cmds = [
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]
    # Colour node cells based on item color
    col_idx = 0
    for ri, row in enumerate(node_rows):
        ci = 0
        for item in row:
            if item is not None:
                lbl, clr, w = item
                if clr:
                    style_cmds.append(("BACKGROUND",(ci,ri),(ci,ri), clr))
                    style_cmds.append(("BOX",(ci,ri),(ci,ri),1,C_BORDER))
            ci += 1

    tbl = Table(tbl_data, colWidths=col_ws, style=TableStyle(style_cmds))
    out = [tbl]
    if caption:
        out.append(P(caption, sCaption))
    out.append(Spacer(1,4))
    return out

def simple_tree(vals_by_level, highlight=None, node_w=44):
    """
    vals_by_level: list of lists, e.g. [[1],[2,3],[4,5,6,7]]
    Draws a compact tree with arrows between levels.
    """
    highlight = highlight or {}
    result = []
    levels = len(vals_by_level)
    # Total columns = 2^(levels-1) * node_w for spacing
    max_nodes = 2**(levels-1)
    total_w = max_nodes * (node_w + 8)

    for li, level in enumerate(vals_by_level):
        n_nodes = len(level)
        # Build a single row with padding
        spacing = total_w / n_nodes
        cells = []
        col_ws = []
        for i, v in enumerate(level):
            pad = max(4, int(spacing/2 - node_w/2))
            if i == 0 and pad > 0:
                cells.append(P("", sCaption))
                col_ws.append(pad)
            if v is None:
                cells.append(P("", sCaption))
            else:
                clr = highlight.get(v, None)
                fg  = C_HEADING
                bg  = clr if clr else colors.HexColor("#152030")
                cells.append(P(f"<b>{v}</b>",
                    S("_", fontName="Courier-Bold", fontSize=10,
                      textColor=fg, alignment=TA_CENTER)))
            col_ws.append(node_w)
            if i < n_nodes - 1:
                gap = max(4, int(spacing - node_w))
                cells.append(P("", sCaption))
                col_ws.append(gap)

        style_cmds = [
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]
        # Colour + box each node cell
        ci = 0
        for i, v in enumerate(level):
            if i == 0:
                ci += 1  # skip initial pad
            if v is not None:
                clr = highlight.get(v, colors.HexColor("#152030"))
                style_cmds.append(("BACKGROUND",(ci,0),(ci,0), clr))
                style_cmds.append(("BOX",(ci,0),(ci,0),1,C_BORDER))
            ci += 1
            if i < n_nodes - 1:
                ci += 1  # skip gap

        if cells:
            row_tbl = Table([cells], colWidths=col_ws, style=TableStyle(style_cmds))
            result.append(row_tbl)

        # Arrow row between levels
        if li < levels - 1:
            arrow_cells = [P("↙  ↘" * min(n_nodes, 4),
                S("_", fontName="Helvetica", fontSize=10,
                  textColor=C_ACCENT, alignment=TA_CENTER))]
            result.append(Table([arrow_cells], colWidths=[total_w + 10],
                style=TableStyle([("TOPPADDING",(0,0),(-1,-1),1),
                    ("BOTTOMPADDING",(0,0),(-1,-1),1)])))

    return result + [Spacer(1,6)]


# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.45*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),("ROWHEIGHT",(0,0),(-1,-1),6)])))
story.append(Spacer(1, 0.3*inch))
story.append(P("BINARY TREE PATTERNS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Recursive Thinking · Traversal Strategies · Tree Properties · LCA", sAuthor))
story.append(Spacer(1, 0.2*inch))

story.append(Table([[P("<b>What You Will Master</b>",
    S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· Binary Tree anatomy: Node, Root, Leaf, Height, Depth — and the BST property\n"
       "· The 3 DFS Traversal Pillars: Pre-order, In-order, Post-order (recursive + iterative)\n"
       "· Level-Order BFS: layer-by-layer processing and minimum depth\n"
       "· Top-Down vs. Bottom-Up recursive thinking: which to use and when\n"
       "· Path Sum patterns: tracking running state root-to-leaf\n"
       "· Lowest Common Ancestor (LCA): the divergence-point algorithm\n"
       "· Tree Transformation: invert, serialize, reconstruct, BST conversion\n"
       "· Tree types: Balanced, Complete, Full, Perfect — and their guarantees\n"
       "· DFS vs BFS, Recursive vs Iterative decision tables\n"
       "· 25+ categorized LeetCode problems with traversal pattern labels",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))]],
    colWidths=[CW], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.28*inch))

# Quick-ref complexity card
cx = [
    [th("Operation"),          th("BST (balanced)"),  th("BST (skewed)"), th("General Binary Tree")],
    [td("Search",    C_BODY),  td("O(log n)",C_GREEN),td("O(n)",C_RED),   td("O(n) — must traverse all",C_MUTED)],
    [td("Insert",    C_BODY),  td("O(log n)",C_GREEN),td("O(n)",C_RED),   td("O(1) given parent pointer",C_GREEN)],
    [td("Delete",    C_BODY),  td("O(log n)",C_GREEN),td("O(n)",C_RED),   td("O(n) to find + O(1) to remove",C_MUTED)],
    [td("DFS Traversal",C_BODY),td("O(n)",C_YELLOW),  td("O(n)",C_YELLOW),td("O(n) — visit every node",C_YELLOW)],
    [td("Height",    C_BODY),  td("O(log n)",C_GREEN),td("O(n)",C_RED),   td("O(n) — must traverse all paths",C_MUTED)],
]
story.append(Table(cx, colWidths=[120,110,100,150], style=TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_BG),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD,C_DARK2]),
    ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ("LEFTPADDING",(0,0),(-1,-1),8)])))
story.append(Spacer(1, 0.3*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",["Binary Tree Anatomy","Binary Tree vs BST","Memory Representation"]),
    ("02","The 3 DFS Traversal Pillars",["Pre-order: Root-Left-Right","In-order: Left-Root-Right","Post-order: Left-Right-Root"]),
    ("03","Level-Order Traversal (BFS)",["Queue-based Layer Processing","Minimum Depth","Zigzag & Right Side View"]),
    ("04","Recursive Thinking & Templates",["Base Case & Recursive Step","Top-Down Approach","Bottom-Up Approach"]),
    ("05","Common Patterns & Tricks",["Path Sum Tracking","Lowest Common Ancestor (LCA)","Tree Transformation"]),
    ("06","Special Tree Types",["Balanced vs Unbalanced","Complete, Full & Perfect Trees","BST Operations"]),
    ("07","Comparison & Decision Making",["DFS vs BFS","Recursive vs Iterative","Decision Flowchart"]),
    ("08","Problem Roadmap",["Easy Problems","Medium Problems","Hard Problems"]),
    ("09","Edge Case Checklist",["Empty Tree & Single Node","Skewed Trees","Duplicate Values & Overflow"]),
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

story.append(P("<b>Binary Tree Anatomy</b>", sH2))
story.append(P(
    "A <b>binary tree</b> is a hierarchical data structure where each node has "
    "at most two children, called the <b>left child</b> and <b>right child</b>. "
    "Every non-trivial tree problem reduces to understanding five concepts: "
    "Node, Root, Leaf, Height, and Depth.",
    sBody))

# Anatomy diagram — ASCII art style using table
anat_data = [
    [th("Term"),      th("Definition"),                                    th("Property")],
    [td("Node",  C_ACCENT),  td("Basic unit storing a value and pointers to children",C_BODY),
     td("Every element in the tree is a node",C_MUTED)],
    [td("Root",  C_GREEN),   td("The topmost node — has no parent",C_BODY),
     td("Exactly one root per tree (or zero for empty tree)",C_MUTED)],
    [td("Leaf",  C_YELLOW),  td("A node with no children (left=None, right=None)",C_BODY),
     td("Base case for most recursive algorithms",C_MUTED)],
    [td("Height",C_PURPLE),  td("Longest path from this node down to any leaf",C_BODY),
     td("Height of leaf = 0. Height of tree = height of root.",C_MUTED)],
    [td("Depth", C_TEAL),    td("Distance from root down to this node",C_BODY),
     td("Depth of root = 0. Depth increases going down.",C_MUTED)],
    [td("Level", C_ORANGE),  td("Depth + 1 (some definitions use depth directly)",C_BODY),
     td("Nodes at the same depth form a 'level'",C_MUTED)],
]
story.append(std_table(anat_data, [60, 235, 185]))
story.append(Spacer(1,8))

# Tree visual
story.append(P("<b>Visual: height vs depth on the same tree</b>", sH3))

tree_rows = [
    [P("", sCaption), P("", sCaption), P("",sCaption),
     P("<b>10</b>", S("_",fontName="Courier-Bold",fontSize=11,textColor=C_GREEN,alignment=TA_CENTER)),
     P("",sCaption), P("",sCaption), P("",sCaption)],
    [P("",sCaption),
     P("<b>5</b>",  S("_",fontName="Courier-Bold",fontSize=11,textColor=C_ACCENT,alignment=TA_CENTER)),
     P("",sCaption), P("  ↙  ↘  ",S("_",fontName="Helvetica",fontSize=10,textColor=C_MUTED,alignment=TA_CENTER)),
     P("",sCaption),
     P("<b>15</b>", S("_",fontName="Courier-Bold",fontSize=11,textColor=C_ACCENT,alignment=TA_CENTER)),
     P("",sCaption)],
    [P("<b>3</b>",  S("_",fontName="Courier-Bold",fontSize=11,textColor=C_YELLOW,alignment=TA_CENTER)),
     P("↙↘",S("_",fontName="Helvetica",fontSize=10,textColor=C_MUTED,alignment=TA_CENTER)),
     P("<b>7</b>",  S("_",fontName="Courier-Bold",fontSize=11,textColor=C_YELLOW,alignment=TA_CENTER)),
     P("",sCaption),
     P("<b>12</b>", S("_",fontName="Courier-Bold",fontSize=11,textColor=C_YELLOW,alignment=TA_CENTER)),
     P("↙↘",S("_",fontName="Helvetica",fontSize=10,textColor=C_MUTED,alignment=TA_CENTER)),
     P("<b>20</b>", S("_",fontName="Courier-Bold",fontSize=11,textColor=C_YELLOW,alignment=TA_CENTER))],
]
ann_row = [
    P("leaf",   S("_",fontName="Helvetica",fontSize=7.5,textColor=C_YELLOW,alignment=TA_CENTER)),
    P("",sCaption),
    P("leaf",   S("_",fontName="Helvetica",fontSize=7.5,textColor=C_YELLOW,alignment=TA_CENTER)),
    P("",sCaption),
    P("leaf",   S("_",fontName="Helvetica",fontSize=7.5,textColor=C_YELLOW,alignment=TA_CENTER)),
    P("",sCaption),
    P("leaf",   S("_",fontName="Helvetica",fontSize=7.5,textColor=C_YELLOW,alignment=TA_CENTER)),
]
dep_row = [
    P("depth=2",S("_",fontName="Helvetica",fontSize=7,textColor=C_TEAL,alignment=TA_CENTER)),
    P("",sCaption),
    P("depth=2",S("_",fontName="Helvetica",fontSize=7,textColor=C_TEAL,alignment=TA_CENTER)),
    P("depth=0 (root) height=2",S("_",fontName="Helvetica",fontSize=7,textColor=C_GREEN,alignment=TA_CENTER)),
    P("depth=2",S("_",fontName="Helvetica",fontSize=7,textColor=C_TEAL,alignment=TA_CENTER)),
    P("",sCaption),
    P("depth=2",S("_",fontName="Helvetica",fontSize=7,textColor=C_TEAL,alignment=TA_CENTER)),
]
story.append(Table(tree_rows + [ann_row, dep_row],
    colWidths=[50,40,50,120,50,40,50+30],
    style=TableStyle([
        ("BOX",(0,0),(0,0),1,C_BORDER),("BACKGROUND",(0,0),(0,0),colors.HexColor("#152030")),
        ("BOX",(2,0),(2,0),1,C_BORDER),("BACKGROUND",(2,0),(2,0),colors.HexColor("#152030")),
        ("BOX",(3,0),(3,0),1,colors.HexColor("#0A3A1A")),("BACKGROUND",(3,0),(3,0),colors.HexColor("#0A3A1A")),
        ("BOX",(1,1),(1,1),1,C_BORDER),("BACKGROUND",(1,1),(1,1),colors.HexColor("#0A1E3A")),
        ("BOX",(5,1),(5,1),1,C_BORDER),("BACKGROUND",(5,1),(5,1),colors.HexColor("#0A1E3A")),
        ("BOX",(0,2),(0,2),1,colors.HexColor("#2E2A0A")),("BACKGROUND",(0,2),(0,2),colors.HexColor("#1A1600")),
        ("BOX",(2,2),(2,2),1,colors.HexColor("#2E2A0A")),("BACKGROUND",(2,2),(2,2),colors.HexColor("#1A1600")),
        ("BOX",(4,2),(4,2),1,colors.HexColor("#2E2A0A")),("BACKGROUND",(4,2),(4,2),colors.HexColor("#1A1600")),
        ("BOX",(6,2),(6,2),1,colors.HexColor("#2E2A0A")),("BACKGROUND",(6,2),(6,2),colors.HexColor("#1A1600")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ])))
story.append(Spacer(1,8))

story.append(P("<b>Binary Tree vs. Binary Search Tree (BST)</b>", sH2))
story.append(P(
    "A <b>Binary Search Tree</b> is a binary tree with an additional ordering property: "
    "for every node N, all values in N's <b>left subtree are strictly less than N.val</b>, "
    "and all values in N's <b>right subtree are strictly greater</b>. "
    "This single invariant enables O(log n) search, insert, and delete on balanced BSTs.",
    sBody))

bst_data = [
    [th("Property"),            th("Binary Tree"),                        th("BST")],
    [td("Ordering",   C_BODY),  td("None — any arrangement valid",C_MUTED),td("left &lt; root &lt; right (recursively)",C_GREEN)],
    [td("Search",     C_BODY),  td("O(n) — must visit all nodes",C_RED),  td("O(log n) balanced / O(n) skewed",C_YELLOW)],
    [td("In-order",   C_BODY),  td("Any order",C_MUTED),                  td("Always yields sorted ascending order",C_GREEN)],
    [td("Validation", C_BODY),  td("N/A",C_MUTED),                        td("Validate with min/max bounds per node",C_BODY)],
    [td("Use case",   C_BODY),  td("Hierarchy, expression trees, heaps",C_MUTED), td("Dictionary, set, sorted data structure",C_MUTED)],
]
story.append(std_table(bst_data, [90, 195, 195]))
story.append(Spacer(1,8))

story += code_block([
    "## ─── TreeNode definition ────────────────────────────────────────",
    "class TreeNode:",
    "    def __init__(self, val=0, left=None, right=None):",
    "        self.val   = val",
    "        self.left  = left    ## pointer to left child (or None)",
    "        self.right = right   ## pointer to right child (or None)",
    "",
    "## Building: [10, 5, 15, 3, 7, 12, 20]",
    "root       = TreeNode(10)",
    "root.left  = TreeNode(5)",
    "root.right = TreeNode(15)",
    "## ... each pointer assignment is O(1)",
])

story += callout(
    "The BST invariant must hold for the ENTIRE subtree, not just immediate children. "
    "A common mistake: node 5 with left=3, right=7 where root=4 — "
    "this violates BST because 5 > 4 (5 is in left subtree of 4). "
    "Always validate with min/max bounds passed down recursively.",
    C_RED, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2 — DFS TRAVERSALS
# ════════════════════════════════════════════════════════
story += section_divider(2, "The 3 DFS Traversal Pillars")

story.append(P(
    "All three DFS traversals visit every node exactly once — O(n) time, O(h) space "
    "where h = tree height. The only difference is <b>when the current node is processed</b> "
    "relative to its children.",
    sBody))

# Traversal order summary
trav_data = [
    [th("Traversal"),   th("Order"),           th("Processing Moment"),         th("Classic Use Case")],
    [td("Pre-order", C_ACCENT),  tdc("Root → L → R"), td("Process node BEFORE children",C_BODY),  td("Clone/copy tree, serialize tree, prefix expressions",C_MUTED)],
    [td("In-order",  C_GREEN),   tdc("L → Root → R"), td("Process node BETWEEN children",C_BODY), td("Sorted output from BST, BST validation, kth smallest",C_MUTED)],
    [td("Post-order",C_PURPLE),  tdc("L → R → Root"), td("Process node AFTER children",C_BODY),   td("Delete tree, height calculation, subtree aggregation",C_MUTED)],
]
story.append(std_table(trav_data, [80, 90, 165, 145]))
story.append(Spacer(1,10))

story.append(P("<b>Pre-order: Root → Left → Right</b>", sH2))
story.append(P(
    "Pre-order visits the root <i>before</i> descending. "
    "This means we see parent context before children — "
    "ideal for serializing structure (the root must be written "
    "before children to reconstruct), copying (create parent before children), "
    "or printing hierarchies.",
    sBody))
story += code_block([
    "## ─── Pre-order Recursive ───────────────────────────────────────",
    "def preorder(root, result=[]):",
    "    if root is None: return         ## base case: nothing to do",
    "    result.append(root.val)         ## PROCESS: root first",
    "    preorder(root.left,  result)    ## then left subtree",
    "    preorder(root.right, result)    ## then right subtree",
    "    return result",
    "",
    "## ─── Pre-order Iterative (explicit stack) ───────────────────────",
    "def preorder_iterative(root):",
    "    if not root: return []",
    "    stack, result = [root], []",
    "    while stack:",
    "        node = stack.pop()          ## process current",
    "        result.append(node.val)",
    "        if node.right: stack.append(node.right)  ## push RIGHT first",
    "        if node.left:  stack.append(node.left)   ## LEFT popped first (LIFO)",
    "    return result",
    "## On tree [10,5,15,3,7,12,20]: output = [10, 5, 3, 7, 15, 12, 20]",
])

story.append(P("<b>In-order: Left → Root → Right</b>", sH2))
story.append(P(
    "In-order visits the left subtree completely, then the root, then right. "
    "For a BST, this produces elements in <b>strictly ascending order</b> — "
    "the entire tree is a nested structure that unrolls to a sorted sequence. "
    "This is the most frequently tested traversal in BST problems.",
    sBody))
story += code_block([
    "## ─── In-order Recursive ────────────────────────────────────────",
    "def inorder(root, result=[]):",
    "    if root is None: return",
    "    inorder(root.left,  result)     ## left subtree first",
    "    result.append(root.val)         ## PROCESS: root between children",
    "    inorder(root.right, result)     ## right subtree last",
    "    return result",
    "## On BST [10,5,15,3,7,12,20]: output = [3, 5, 7, 10, 12, 15, 20] ← sorted!",
    "",
    "## ─── In-order Iterative (Morris-style simplified) ───────────────",
    "def inorder_iterative(root):",
    "    stack, result, curr = [], [], root",
    "    while curr or stack:",
    "        while curr:                 ## go as far left as possible",
    "            stack.append(curr)",
    "            curr = curr.left",
    "        curr = stack.pop()          ## backtrack: process node",
    "        result.append(curr.val)",
    "        curr = curr.right           ## now explore right subtree",
    "    return result",
])

story.append(P("<b>Post-order: Left → Right → Root</b>", sH2))
story.append(P(
    "Post-order processes both children <i>before</i> the parent. "
    "This bottom-up evaluation is essential whenever the parent's computation "
    "depends on children's results: calculating subtree height, "
    "counting nodes, summing subtree values, or safely deleting nodes "
    "(children must be freed before parent).",
    sBody))
story += code_block([
    "## ─── Post-order Recursive ───────────────────────────────────────",
    "def postorder(root, result=[]):",
    "    if root is None: return",
    "    postorder(root.left,  result)   ## left subtree first",
    "    postorder(root.right, result)   ## right subtree second",
    "    result.append(root.val)         ## PROCESS: root last (bottom-up)",
    "    return result",
    "## On tree [10,5,15,3,7,12,20]: output = [3, 7, 5, 12, 20, 15, 10]",
    "",
    "## ─── Post-order classic: compute height bottom-up ─────────────",
    "def height(root):",
    "    if root is None: return -1      ## base: empty tree has height -1",
    "    left_h  = height(root.left)     ## get left subtree height first",
    "    right_h = height(root.right)    ## get right subtree height",
    "    return 1 + max(left_h, right_h) ## parent height = max child + 1",
    "## The '+1' and 'max' happen AFTER both children return — pure post-order.",
])

# Traversal trace on same tree
story.append(P("<b>Visual: All Three Traversals on the Same Tree</b>", sH3))
trace_tbl = [
    [th("Tree"), th("Pre-order"), th("In-order"), th("Post-order")],
    [P(
        "      [1]\n"
        "     /   \\\n"
        "   [2]   [3]\n"
        "   / \\\n"
        " [4] [5]",
        S("_",fontName="Courier",fontSize=9,textColor=C_BODY,leading=13)),
     tdc("[1,2,4,5,3]", C_ACCENT),
     tdc("[4,2,5,1,3]", C_GREEN),
     tdc("[4,5,2,3,1]", C_PURPLE)],
]
story.append(std_table(trace_tbl, [160, 110, 110, 100]))
story.append(Spacer(1,6))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3 — LEVEL ORDER BFS
# ════════════════════════════════════════════════════════
story += section_divider(3, "Level-Order Traversal (BFS)")

story.append(P("<b>Queue-Based Layer Processing</b>", sH2))
story.append(P(
    "Level-order traversal visits nodes level by level, left to right. "
    "A queue's FIFO property ensures that nodes discovered at level d "
    "are all processed before any node at level d+1. "
    "The critical technique: <b>snapshot len(queue) at the start of each level</b> "
    "to know exactly how many nodes belong to that level.",
    sBody))

story += code_block([
    "## ─── Level-Order BFS Template ──────────────────────────────────",
    "from collections import deque",
    "",
    "def level_order(root):",
    "    if not root: return []",
    "    queue  = deque([root])",
    "    result = []",
    "",
    "    while queue:",
    "        level_size = len(queue)   ## SNAPSHOT: nodes at this level",
    "        level = []",
    "",
    "        for _ in range(level_size):   ## process EXACTLY this many",
    "            node = queue.popleft()",
    "            level.append(node.val)",
    "            if node.left:  queue.append(node.left)",
    "            if node.right: queue.append(node.right)",
    "",
    "        result.append(level)",
    "",
    "    return result   ## [[root], [l2_left, l2_right], [l3_nodes...], ...]",
])

story.append(P("<b>Minimum Depth (Earliest Leaf via BFS)</b>", sH2))
story.append(P(
    "BFS finds the <b>shallowest</b> leaf because it processes level by level — "
    "the first leaf encountered is guaranteed to be at the minimum depth. "
    "DFS would need to explore all paths and take a minimum, risking O(n) "
    "path exploration on deep trees.",
    sBody))
story += code_block([
    "## ─── Minimum Depth of Binary Tree ─────────────────────────────",
    "def min_depth(root):",
    "    if not root: return 0",
    "    queue = deque([(root, 1)])   ## (node, depth)",
    "",
    "    while queue:",
    "        node, depth = queue.popleft()",
    "",
    "        ## First leaf encountered = minimum depth (BFS guarantee)",
    "        if not node.left and not node.right:",
    "            return depth",
    "",
    "        if node.left:  queue.append((node.left,  depth + 1))",
    "        if node.right: queue.append((node.right, depth + 1))",
    "",
    "    return 0",
    "",
    "## Why BFS beats DFS here:",
    "## DFS: explores entire left subtree (depth 100) before finding",
    "##      a leaf at depth 2 on the right. BFS finds depth-2 leaf first.",
])

story.append(P("<b>Level-Order Variants</b>", sH3))
variants = [
    [th("Variant"),                          th("Modification to Template"),                th("Problem")],
    [td("Zigzag Level Order",    C_BODY),    td("Alternate append direction each level",C_BODY), td("LC 103",C_MUTED)],
    [td("Right Side View",       C_BODY),    td("Record last element of each level",    C_BODY), td("LC 199",C_MUTED)],
    [td("Average of Levels",     C_BODY),    td("sum(level) / len(level) each row",     C_BODY), td("LC 637",C_MUTED)],
    [td("Level Order II (bottom up)",C_BODY),td("Reverse the result list at the end",   C_BODY), td("LC 107",C_MUTED)],
    [td("Deepest Leaves Sum",    C_BODY),    td("Track level; return last level's sum", C_BODY), td("LC 1302",C_MUTED)],
    [td("Max Width of Tree",     C_BODY),    td("Track (node, index) pairs; width = max_idx - min_idx + 1",C_BODY),td("LC 662",C_MUTED)],
]
story.append(std_table(variants, [145, 220, 55]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4 — RECURSIVE THINKING
# ════════════════════════════════════════════════════════
story += section_divider(4, "Recursive Thinking & Templates")

story.append(P("<b>Base Case & Recursive Step</b>", sH2))
story.append(P(
    "Every tree recursion has two components: a <b>base case</b> that handles "
    "the simplest input (usually empty node or leaf), and a <b>recursive step</b> "
    "that expresses the answer in terms of smaller subproblems (left and right subtrees). "
    "Trust the recursion: assume <i>the function works correctly on subtrees</i> "
    "and write only the logic that combines their results.",
    sBody))
story += code_block([
    "## ─── Anatomy of a tree recursive function ───────────────────────",
    "def solve(root):",
    "    ## ── BASE CASE: smallest valid input ─────────────────────────",
    "    if root is None:             ## empty subtree",
    "        return BASE_VALUE        ## 0 for count/sum, True for validity, etc.",
    "",
    "    ## ── RECURSIVE STEP: delegate to subtrees ─────────────────────",
    "    left_result  = solve(root.left)   ## trust: correct answer for left",
    "    right_result = solve(root.right)  ## trust: correct answer for right",
    "",
    "    ## ── COMBINE: merge subtree results at current node ───────────",
    "    return combine(root.val, left_result, right_result)",
    "",
    "## The 'combine' step is what changes between problems.",
    "## Count nodes:  return 1 + left_result + right_result",
    "## Max depth:    return 1 + max(left_result, right_result)",
    "## Is same tree: return root1.val==root2.val and left_result and right_result",
])

story.append(P("<b>Top-Down: Pass Parameters Down (Pre-order style)</b>", sH2))
story.append(P(
    "In the <b>top-down</b> approach, the parent computes information "
    "and <b>passes it as a parameter</b> to children. "
    "The function's return value is often void — the answer is accumulated "
    "in a side-effect variable or the parameter itself. "
    "Works like pre-order: parent context is established before children are called.",
    sBody))
story += code_block([
    "## ─── Top-Down: Has Path Sum? ───────────────────────────────────",
    "def has_path_sum(root, target_sum):",
    "    ## Base: reached a null child — sum didn't reach target",
    "    if root is None: return False",
    "",
    "    ## Base: leaf node — check if remaining sum equals node value",
    "    if not root.left and not root.right:",
    "        return root.val == target_sum",
    "",
    "    ## Pass reduced target DOWN to children",
    "    remaining = target_sum - root.val",
    "    return (has_path_sum(root.left,  remaining) or",
    "            has_path_sum(root.right, remaining))",
    "",
    "## ─── Top-Down: Max Depth (passing depth parameter) ─────────────",
    "def max_depth_td(root, depth=0):",
    "    if root is None: return depth       ## depth passed down, returned at leaf",
    "    return max(max_depth_td(root.left,  depth + 1),",
    "               max_depth_td(root.right, depth + 1))",
])

story.append(P("<b>Bottom-Up: Return Values Up (Post-order style)</b>", sH2))
story.append(P(
    "In the <b>bottom-up</b> approach, children compute their results first "
    "and <b>return them to the parent</b>. The parent combines child results "
    "to produce its own answer. Works like post-order: children are fully "
    "resolved before the parent acts. Most tree optimization problems "
    "(diameter, max path sum, LCA) use bottom-up.",
    sBody))
story += code_block([
    "## ─── Bottom-Up: Diameter of Binary Tree ────────────────────────",
    "def diameter(root):",
    "    max_diam = [0]   ## use list for mutable closure in Python",
    "",
    "    def height(node):",
    "        if node is None: return -1",
    "        left_h  = height(node.left)   ## children compute first",
    "        right_h = height(node.right)",
    "",
    "        ## Diameter through this node = left_height + right_height + 2",
    "        max_diam[0] = max(max_diam[0], left_h + right_h + 2)",
    "",
    "        return 1 + max(left_h, right_h)   ## return height to parent",
    "",
    "    height(root)",
    "    return max_diam[0]",
    "",
    "## ─── Top-Down vs Bottom-Up at a glance ─────────────────────────",
    "## Top-Down:   parent → parameter → children → leaf returns answer",
    "## Bottom-Up:  leaf → return value → parent combines → root returns answer",
])

td_bu_data = [
    [th("Dimension"),          th("Top-Down"),                       th("Bottom-Up")],
    [td("Info flow",  C_BODY), td("Parent → Children (parameter)", C_BODY), td("Children → Parent (return value)",C_BODY)],
    [td("Style",      C_BODY), td("Pre-order-like",C_ACCENT),        td("Post-order-like",C_PURPLE)],
    [td("State",      C_BODY), td("Accumulated parameter (target, depth, path)",C_BODY), td("Returned result (height, sum, bool)",C_BODY)],
    [td("Best for",   C_BODY), td("Path queries, cumulative state",C_MUTED), td("Subtree aggregation, global optimums",C_MUTED)],
    [td("Examples",   C_BODY), td("Path Sum, Good Nodes, Max Depth",C_MUTED), td("Height, Diameter, Max Path Sum, LCA",C_MUTED)],
]
story.append(std_table(td_bu_data, [90, 200, 190]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5 — COMMON PATTERNS
# ════════════════════════════════════════════════════════
story += section_divider(5, "Common Patterns & Tricks")

story.append(P("<b>Path Sum Tracking</b>", sH2))
story.append(P(
    "Path sum problems maintain a <b>running aggregate</b> as recursion "
    "descends from root to leaf. The key insight: instead of summing from scratch "
    "at each leaf, <b>subtract the current node's value from a target</b> as you "
    "descend — reaching 0 at a leaf means a valid path was found.",
    sBody))
story += code_block([
    "## ─── Path Sum II: find all root-to-leaf paths with target sum ───",
    "def path_sum_all(root, target):",
    "    result = []",
    "",
    "    def dfs(node, remaining, path):",
    "        if node is None: return",
    "",
    "        path.append(node.val)           ## add to current path",
    "        remaining -= node.val",
    "",
    "        ## Leaf check: path complete",
    "        if not node.left and not node.right and remaining == 0:",
    "            result.append(list(path))   ## snapshot: list() copies the path",
    "        else:",
    "            dfs(node.left,  remaining, path)",
    "            dfs(node.right, remaining, path)",
    "",
    "        path.pop()                      ## BACKTRACK: restore state",
    "",
    "    dfs(root, target, [])",
    "    return result",
    "",
    "## ─── Maximum Path Sum (any path, not just root-to-leaf) ─────────",
    "def max_path_sum(root):",
    "    max_sum = [float('-inf')]",
    "",
    "    def gain(node):     ## bottom-up: returns max gain from this node downward",
    "        if not node: return 0",
    "        left_gain  = max(gain(node.left),  0)  ## discard negative paths",
    "        right_gain = max(gain(node.right), 0)",
    "        ## Path through this node = left + node + right (global candidate)",
    "        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)",
    "        ## Return to parent: can only use ONE side (path can't fork)",
    "        return node.val + max(left_gain, right_gain)",
    "",
    "    gain(root)",
    "    return max_sum[0]",
])

story.append(P("<b>Lowest Common Ancestor (LCA)</b>", sH2))
story.append(P(
    "Given two nodes p and q, find their LCA — the deepest node that has "
    "both p and q as descendants. The elegant recursive insight: "
    "a node is the LCA if <b>p and q are found in different subtrees</b>, "
    "or if the node itself is p or q (and the other is in its subtree).",
    sBody))
story += code_block([
    "## ─── LCA of Binary Tree (general, not BST) ─────────────────────",
    "def lca(root, p, q):",
    "    ## Base: empty node or found a target",
    "    if root is None: return None",
    "    if root is p or root is q: return root   ## 'is': identity, not equality",
    "",
    "    left  = lca(root.left,  p, q)   ## search left subtree",
    "    right = lca(root.right, p, q)   ## search right subtree",
    "",
    "    ## If both sides found something: THIS node is the LCA",
    "    if left and right: return root",
    "",
    "    ## One side found both (or nothing): propagate result upward",
    "    return left if left else right",
    "",
    "## ─── LCA of BST (exploit ordering property) ─────────────────────",
    "def lca_bst(root, p, q):",
    "    while root:",
    "        if p.val < root.val and q.val < root.val:",
    "            root = root.left    ## both in left subtree",
    "        elif p.val > root.val and q.val > root.val:",
    "            root = root.right   ## both in right subtree",
    "        else:",
    "            return root         ## diverge here: this IS the LCA",
    "    return None",
])

story += callout(
    "LCA insight: when the search finds p in the left subtree and q in the right "
    "(or vice versa), the current node must be the divergence point — it IS the LCA. "
    "If both are on the same side, the LCA is deeper and we propagate upward.",
    C_ACCENT2, icon="🎯")

story.append(P("<b>Tree Transformation</b>", sH2))
story += code_block([
    "## ─── Invert Binary Tree ─────────────────────────────────────────",
    "def invert_tree(root):",
    "    if root is None: return None",
    "    root.left, root.right = invert_tree(root.right), invert_tree(root.left)",
    "    return root",
    "## Post-order: swap children AFTER both sides are inverted.",
    "",
    "## ─── Sorted Array → Balanced BST ───────────────────────────────",
    "def sorted_array_to_bst(nums):",
    "    if not nums: return None",
    "    mid  = len(nums) // 2",
    "    root = TreeNode(nums[mid])             ## middle = root (guarantees balance)",
    "    root.left  = sorted_array_to_bst(nums[:mid])",
    "    root.right = sorted_array_to_bst(nums[mid+1:])",
    "    return root",
    "",
    "## ─── Serialize / Deserialize ─────────────────────────────────────",
    "def serialize(root):",
    "    if not root: return 'N'              ## null marker",
    "    return f'{root.val},{serialize(root.left)},{serialize(root.right)}'",
    "",
    "def deserialize(data):",
    "    vals = iter(data.split(','))",
    "    def build():",
    "        v = next(vals)",
    "        if v == 'N': return None",
    "        node = TreeNode(int(v))",
    "        node.left  = build()",
    "        node.right = build()",
    "        return node",
    "    return build()",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6 — SPECIAL TREE TYPES
# ════════════════════════════════════════════════════════
story += section_divider(6, "Special Types of Trees")

story.append(P("<b>Balanced vs. Unbalanced</b>", sH2))
story.append(P(
    "A tree is <b>height-balanced</b> if, for every node, "
    "the heights of its left and right subtrees differ by at most 1. "
    "Balance is what guarantees O(log n) operations on BSTs. "
    "An unbalanced BST degrades to O(n) — essentially a linked list.",
    sBody))

bal_data = [
    [th("Tree Type"),         th("Height"),      th("Search"), th("Self-Balancing?"), th("Notes")],
    [td("Balanced BST",C_GREEN),  td("O(log n)",C_GREEN),  td("O(log n)",C_GREEN), td("Manual or AVL/RB",C_YELLOW),  td("Ideal for sorted data ops",C_MUTED)],
    [td("AVL Tree",    C_GREEN),  td("O(log n)",C_GREEN),  td("O(log n)",C_GREEN), td("✅ Automatic rotations",C_GREEN),td("Strict balance (|diff|≤1)",C_MUTED)],
    [td("Red-Black",   C_TEAL),   td("O(log n)",C_GREEN),  td("O(log n)",C_GREEN), td("✅ Automatic rotations",C_GREEN),td("Looser balance, faster inserts",C_MUTED)],
    [td("Skewed BST",  C_RED),    td("O(n)",    C_RED),    td("O(n)",    C_RED),   td("❌ No balancing",     C_RED),   td("Worst case: sorted insert order",C_MUTED)],
    [td("Python dict / Java TreeMap",C_MUTED),td("O(log n)",C_GREEN),td("O(log n)",C_GREEN),td("✅ Built-in",C_GREEN),td("Use these in interviews!",C_MUTED)],
]
story.append(std_table(bal_data, [130, 65, 65, 120, 100]))
story.append(Spacer(1,8))

story += callout(
    "For LeetCode: you never implement AVL or Red-Black trees. "
    "Just know they exist, why balance matters (O(log n) guarantee), "
    "and that Python's sortedcontainers.SortedList or Java's TreeMap "
    "give you a balanced BST without manual implementation.",
    C_ACCENT, icon="💡")

story.append(P("<b>Complete, Full, and Perfect Binary Trees</b>", sH2))
types_data = [
    [th("Type"),               th("Definition"),                                          th("Property / Use Case")],
    [td("Full Tree",   C_ACCENT),  td("Every node has 0 or 2 children (never 1)",C_BODY),
     td("Expression trees. Leaf count = internal nodes + 1",C_MUTED)],
    [td("Complete Tree",C_GREEN),  td("All levels filled except possibly last; last level filled left-to-right",C_BODY),
     td("Binary Heap (priority queue). Can store in array with index formula",C_MUTED)],
    [td("Perfect Tree", C_PURPLE), td("All internal nodes have 2 children AND all leaves at same depth",C_BODY),
     td("Exactly 2<super>h+1</super>-1 nodes. All levels fully filled.",C_MUTED)],
    [td("Balanced Tree",C_YELLOW), td("Height of left and right subtrees differ by at most 1 (per node)",C_BODY),
     td("Guarantees O(log n) operations. AVL and Red-Black trees maintain this.",C_MUTED)],
]
story.append(std_table(types_data, [90, 225, 165]))
story.append(Spacer(1,8))

story.append(P("<b>BST Core Operations</b>", sH3))
story += code_block([
    "## ─── BST Search ────────────────────────────────────────────────",
    "def search_bst(root, val):",
    "    if not root or root.val == val: return root",
    "    if val < root.val: return search_bst(root.left,  val)  ## go left",
    "    else:              return search_bst(root.right, val)  ## go right",
    "",
    "## ─── BST Insert ─────────────────────────────────────────────────",
    "def insert_bst(root, val):",
    "    if not root: return TreeNode(val)    ## found insertion point",
    "    if val < root.val: root.left  = insert_bst(root.left,  val)",
    "    else:              root.right = insert_bst(root.right, val)",
    "    return root",
    "",
    "## ─── BST Validate ───────────────────────────────────────────────",
    "def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):",
    "    if not root: return True",
    "    if not (lo < root.val < hi): return False    ## violates bounds",
    "    return (is_valid_bst(root.left,  lo, root.val) and",
    "            is_valid_bst(root.right, root.val, hi))",
    "## Pass BOUNDS down (top-down). Each node must fall within inherited range.",
])

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7 — COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(7, "Comparison & Decision Making")

story.append(P("<b>DFS vs. BFS for Binary Trees</b>", sH2))
dfs_bfs = [
    [th("Dimension"),         th("DFS (Stack / Recursion)"),                   th("BFS (Queue)")],
    [td("Data structure",C_BODY),td("Call stack (recursive) or explicit stack",C_BODY),td("Queue (always explicit deque)",C_BODY)],
    [td("Traversal",      C_BODY),td("Depth-first: one branch fully before sibling",C_BODY),td("Breadth-first: all nodes at level d before d+1",C_BODY)],
    [td("Memory (balanced)",C_BODY),td("O(h) = O(log n) — only current path in memory",C_GREEN),td("O(w) = O(n/2) — entire bottom level in queue",C_YELLOW)],
    [td("Memory (skewed)", C_BODY),td("O(n) — entire tree on call stack",C_RED),td("O(1) for skewed (only 1 node per level)",C_GREEN)],
    [td("Shortest path",  C_BODY),td("❌ Not guaranteed without extra bookkeeping",C_RED),td("✅ Guaranteed shortest path (unweighted)",C_GREEN)],
    [td("Node existence", C_BODY),td("✅ Simple: return True when found",C_GREEN),td("✅ Works but processes more nodes",C_YELLOW)],
    [td("Level grouping", C_BODY),td("⚠️ Needs depth parameter to group levels",C_YELLOW),td("✅ Natural: one loop iteration = one level",C_GREEN)],
    [td("Best for",       C_BODY),
     td("Subtree queries, path sums, LCA, tree transformation, all DFS patterns",C_ACCENT,"Helvetica-Oblique"),
     td("Shortest/min depth, level-order output, layer-by-layer problems",C_GREEN,"Helvetica-Oblique")],
]
story.append(std_table(dfs_bfs, [110, 200, 170]))
story.append(Spacer(1, 10))

story.append(P("<b>Recursive vs. Iterative</b>", sH2))
ri_data = [
    [th("Dimension"),           th("Recursive"),                         th("Iterative")],
    [td("Code length",  C_BODY),td("Usually shorter, mirrors tree structure",C_GREEN),td("More verbose, explicit stack management",C_YELLOW)],
    [td("Readability",  C_BODY),td("Closer to mathematical definition",C_GREEN),td("More explicit, easier to trace",C_YELLOW)],
    [td("Stack frames", C_BODY),td("O(h) implicit call frames — may overflow for h&gt;10k",C_YELLOW),td("O(h) explicit stack — no system limit",C_GREEN)],
    [td("Tail recursion",C_BODY),td("Python does NOT optimise tail calls",C_RED),td("Iterative avoids this entirely",C_GREEN)],
    [td("Debugging",    C_BODY),td("Harder: call stack has many frames",C_YELLOW),td("Easier: inspect explicit stack at any point",C_GREEN)],
    [td("Interview preference",C_BODY),td("✅ Preferred for clarity in most tree problems",C_GREEN),td("Requested for 'no recursion' variant",C_YELLOW)],
    [td("Skewed tree (n=10k)",C_BODY),td("⚠️ RecursionError in Python (default limit 1000)",C_RED),td("✅ Safe — explicit stack has no OS limit",C_GREEN)],
]
story.append(std_table(ri_data, [130, 200, 150]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1", "Does the problem involve processing nodes level by level?",      C_ACCENT),
    (" → YES", "→ BFS with Queue. Level-order, zigzag, right-side view, min depth.",C_GREEN),
    (" → NO",  "→ Continue to Q2.",                                           C_MUTED),
    ("Q2", "Does the answer depend on information from ancestor nodes?",      C_ACCENT),
    (" → YES", "→ Top-Down DFS. Pass parameter down (target sum, bounds).",   C_ACCENT2),
    (" → NO",  "→ Continue to Q3.",                                           C_MUTED),
    ("Q3", "Does the answer aggregate results from subtrees?",                C_ACCENT),
    (" → YES", "→ Bottom-Up DFS. Return values upward (height, diameter, max path).",C_PURPLE),
    (" → NO",  "→ Continue to Q4.",                                           C_MUTED),
    ("Q4", "Is this a BST problem?",                                          C_ACCENT),
    (" → YES", "→ Use BST ordering property: go left if val < root, right otherwise.",C_GREEN),
    (" → NO",  "→ Choose traversal based on processing order needed (pre/in/post).",  C_MUTED),
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
story.append(P("Solve in sequence — each problem introduces exactly one new tree concept.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("104",C_GREEN), td("Maximum Depth of Binary Tree",       C_BODY), td("Bottom-Up DFS",    C_PURPLE),
     td("height(None)=-1; return 1+max(left,right).", C_MUTED)],
    [tdc("226",C_GREEN), td("Invert Binary Tree",                 C_BODY), td("Post-order",       C_PURPLE),
     td("Swap left/right AFTER recursing into both.", C_MUTED)],
    [tdc("100",C_GREEN), td("Same Tree",                          C_BODY), td("Pre-order DFS",    C_ACCENT),
     td("Check root vals equal AND both subtrees same.", C_MUTED)],
    [tdc("101",C_GREEN), td("Symmetric Tree",                     C_BODY), td("Mirror DFS",       C_ACCENT2),
     td("isMirror(left.left, right.right) AND (left.right, right.left).", C_MUTED)],
    [tdc("112",C_GREEN), td("Path Sum",                           C_BODY), td("Top-Down DFS",     C_ACCENT),
     td("Subtract node val; at leaf check remaining==0.", C_MUTED)],
    [tdc("572",C_GREEN), td("Subtree of Another Tree",            C_BODY), td("DFS + Same Tree",  C_TEAL),
     td("At each node: isSameTree(root, subRoot). O(n·m).", C_MUTED)],
    [tdc("543",C_GREEN), td("Diameter of Binary Tree",            C_BODY), td("Bottom-Up DFS",    C_PURPLE),
     td("diam = max(diam, left_h+right_h+2). Return height.", C_MUTED)],
    [tdc("110",C_GREEN), td("Balanced Binary Tree",               C_BODY), td("Bottom-Up DFS",    C_PURPLE),
     td("Return -1 as sentinel for unbalanced; propagate up.", C_MUTED)],
]
story.append(std_table(easy_data, [38, 195, 110, 137]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("102",C_YELLOW), td("Binary Tree Level Order Traversal",  C_BODY), td("BFS Queue",        C_GREEN),
     td("Snapshot len(queue) per level; append entire level.", C_MUTED)],
    [tdc("199",C_YELLOW), td("Binary Tree Right Side View",        C_BODY), td("BFS — last per level",C_GREEN),
     td("Record queue[-1] (or last node) at each level.", C_MUTED)],
    [tdc("113",C_YELLOW), td("Path Sum II",                        C_BODY), td("Top-Down + Backtrack",C_ACCENT),
     td("Append to path, recurse, pop after. Snapshot on valid leaf.", C_MUTED)],
    [tdc("236",C_YELLOW), td("Lowest Common Ancestor",             C_BODY), td("Bottom-Up DFS",    C_PURPLE),
     td("If both sides non-null return root; else propagate non-null side.", C_MUTED)],
    [tdc("105",C_YELLOW), td("Construct Tree from Pre+Inorder",    C_BODY), td("Pre-order + HashMap",C_ACCENT),
     td("preorder[0]=root; find in inorder for split; recurse.", C_MUTED)],
    [tdc("230",C_YELLOW), td("Kth Smallest in BST",               C_BODY), td("In-order DFS",     C_GREEN),
     td("In-order yields sorted; decrement k; return when k==0.", C_MUTED)],
    [tdc("98", C_YELLOW), td("Validate Binary Search Tree",        C_BODY), td("Top-Down + Bounds", C_ACCENT),
     td("Pass (lo, hi) bounds; each node must satisfy lo < val < hi.", C_MUTED)],
    [tdc("297",C_YELLOW), td("Serialize and Deserialize Tree",     C_BODY), td("Pre-order DFS",    C_ACCENT),
     td("Pre-order with 'N' null markers; reconstruct with iterator.", C_MUTED)],
    [tdc("662",C_YELLOW), td("Maximum Width of Binary Tree",       C_BODY), td("BFS + indexing",   C_GREEN),
     td("Track (node, col_index); width = max_idx - min_idx + 1 per level.", C_MUTED)],
]
story.append(std_table(med_data, [38, 195, 125, 122]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("124",C_RED), td("Binary Tree Maximum Path Sum",         C_BODY), td("Bottom-Up + Global",  C_PURPLE),
     td("gain(node) returns best single-side; update global with left+right+node.", C_MUTED)],
    [tdc("297",C_RED), td("Serialize / Deserialize (hard)",       C_BODY), td("BFS or Pre-order",    C_GREEN),
     td("Level-order serialization with null markers. Reconstruct with queue.", C_MUTED)],
    [tdc("99", C_RED), td("Recover BST (two nodes swapped)",      C_BODY), td("In-order + two ptrs", C_GREEN),
     td("In-order; find two inversion points; swap their values.", C_MUTED)],
    [tdc("968",C_RED), td("Binary Tree Cameras",                  C_BODY), td("Bottom-Up Greedy",    C_PURPLE),
     td("States: 0=uncovered, 1=covered, 2=has camera. Post-order decision.", C_MUTED)],
    [tdc("1373",C_RED),td("Maximum Sum BST in Binary Tree",       C_BODY), td("Bottom-Up + BST validate",C_PURPLE),
     td("Return (is_bst, min, max, sum) from each subtree; track global max.", C_MUTED)],
]
story.append(std_table(hard_data, [38, 185, 125, 132]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9 — EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(9, "The Edge Case Checklist")

story.append(P(
    "Binary tree problems have a predictable set of edge cases. "
    "Every algorithm must handle these before submitting — "
    "they account for the vast majority of Wrong Answer verdicts.",
    sBody))

story.append(P("<b>Edge Case 1: Empty Tree (root is None)</b>", sH2))
story += code_block([
    "## ALWAYS guard at the top of tree functions:",
    "def my_tree_algo(root):",
    "    if root is None: return APPROPRIATE_DEFAULT",
    "    ## Appropriate defaults:",
    "    ## Count / Sum → return 0",
    "    ## Height      → return -1 (or 0 depending on definition)",
    "    ## Boolean     → return True (empty tree is vacuously valid)",
    "    ## List        → return []",
    "    ## Node        → return None",
    "",
    "## ALSO guard before accessing .left or .right:",
    "## WRONG: depth = 1 + max(height(root.left), height(root.right))",
    "## if root is None, the call crashes before reaching the if guard",
    "",
    "## CORRECT: base case handles None before any attribute access",
    "def height(root):",
    "    if root is None: return -1    ## guard is the FIRST line",
    "    return 1 + max(height(root.left), height(root.right))",
])

story.append(P("<b>Edge Case 2: Single-Node Tree</b>", sH2))
story += code_block([
    "## Single node: root.left = None, root.right = None",
    "## Test your algorithm mentally on a single node:",
    "",
    "## Height: if root is None return -1 → left_h=-1, right_h=-1",
    "##         return 1 + max(-1,-1) = 0 ✓ (leaf has height 0)",
    "",
    "## Path Sum: if not root.left and not root.right:",
    "##               return root.val == target  ← leaf check fires ✓",
    "",
    "## LCA(root, root, root): root is p → return root immediately ✓",
    "",
    "## Level Order: level_size=1, process root, no children enqueued",
    "##              result = [[root.val]] ✓",
])

story.append(P("<b>Edge Case 3: Skewed Trees (Linked List Shape)</b>", sH2))
story.append(P(
    "A skewed tree has all nodes on one side: every node has only a left child "
    "(left-skewed) or only a right child (right-skewed). "
    "Height = n − 1. Recursive DFS on a left-skewed tree of n=10,000 nodes "
    "requires 10,000 recursive calls — Python's default recursion limit is ~1,000.",
    sBody))
story += code_block([
    "## Skewed tree: 1 → 2 → 3 → ... → 10000 (all right children)",
    "## DFS recursion depth = 10000 → RecursionError in Python!",
    "",
    "## Detection: height(root) == n - 1 (for n nodes)",
    "",
    "## Fix 1: Increase recursion limit (not recommended for production)",
    "import sys",
    "sys.setrecursionlimit(50000)  ## risky: OS may not support deep stacks",
    "",
    "## Fix 2: Convert to iterative DFS with explicit stack (preferred)",
    "def iterative_inorder(root):",
    "    stack, result, curr = [], [], root",
    "    while curr or stack:",
    "        while curr:                 ## go left as deep as possible",
    "            stack.append(curr); curr = curr.left",
    "        curr = stack.pop()          ## backtrack",
    "        result.append(curr.val)",
    "        curr = curr.right           ## explore right",
    "    return result",
])

story.append(P("<b>Edge Case 4: Duplicate Values in BSTs</b>", sH3))
story += code_block([
    "## Standard BST property: left < root < right (strict)",
    "## Many problems state 'all values are unique' — read carefully!",
    "",
    "## If duplicates ARE possible, clarify the convention:",
    "## Convention A: duplicates go LEFT (left <= root < right)",
    "## Convention B: duplicates go RIGHT (left < root <= right)",
    "## Convention C: store count at each node (multiset BST)",
    "",
    "## For LeetCode problems with duplicates, check the constraint note.",
    "## LC 450 Delete Node in BST: states all values unique.",
    "## LC 701 Insert BST: states value not already in tree.",
    "",
    "## BST validation with duplicates (left <= root < right convention):",
    "def is_valid_bst_dup(root, lo=float('-inf'), hi=float('inf')):",
    "    if not root: return True",
    "    if not (lo <= root.val < hi): return False   ## note: <= not <",
    "    return (is_valid_bst_dup(root.left,  lo, root.val + 1) and",
    "            is_valid_bst_dup(root.right, root.val, hi))",
])

story.append(P("<b>Edge Case 5: Integer Overflow in Path Sums</b>", sH3))
story += code_block([
    "## For Maximum Path Sum or Sum problems with large values:",
    "## Python: no integer overflow (arbitrary precision) — safe",
    "## Java / C++: sum of n=1000 nodes each with val=10^4 = 10^7 — fits int",
    "##             but: sum of n=10^4 nodes with val=10^9 → OVERFLOW",
    "",
    "## Python solution: always use float('-inf') for initial max",
    "max_sum = [float('-inf')]   ## NOT max_sum = [0]",
    "## Why not 0? If all nodes are negative, the max path is a single",
    "## negative node — initializing to 0 incorrectly returns 0.",
    "",
    "## In Java/C++: use long instead of int for accumulators.",
])

# Master cheat sheet
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")
story.append(P("One-page reference for all patterns, traversals, and decision rules.", sBody))

cheat = [
    [th("Pattern"),               th("Traversal"),    th("Direction"),    th("Return / State"),        th("Classic Problem")],
    [td("Count / Sum nodes",C_ACCENT), tdc("Post-order"),tdc("Bottom-Up"), tdc("1 + left + right"),   td("Count Nodes, Tree Sum", C_MUTED)],
    [td("Height / Depth",   C_ACCENT), tdc("Post-order"),tdc("Bottom-Up"), tdc("1+max(l,r)"),         td("Max Depth, Diameter",   C_MUTED)],
    [td("Path Sum",         C_GREEN),  tdc("Pre-order"), tdc("Top-Down"),  tdc("target -= node.val"), td("Path Sum I/II",         C_MUTED)],
    [td("BST Search",       C_GREEN),  tdc("Pre-order"), tdc("Top-Down"),  tdc("go left or right"),   td("Search BST, Validate BST",C_MUTED)],
    [td("In-order sorted",  C_TEAL),   tdc("In-order"),  tdc("Bottom-Up"), tdc("yields sorted seq."), td("Kth Smallest, BST ops", C_MUTED)],
    [td("LCA",              C_PURPLE), tdc("Post-order"),tdc("Bottom-Up"), tdc("propagate non-None"), td("LCA Binary Tree / BST", C_MUTED)],
    [td("Level-order",      C_YELLOW), tdc("BFS Queue"), tdc("Level→Level"),tdc("snapshot len(q)"),   td("Level Order, Right View",C_MUTED)],
    [td("Serialize",        C_ORANGE), tdc("Pre-order"), tdc("Top-Down"),  tdc("'N' for None"),       td("Serialize/Deserialize", C_MUTED)],
    [td("Construct from traversals",C_ROSE),tdc("Pre+In"),tdc("Divide"),  tdc("preorder[0]=root"),   td("LC 105, LC 106",        C_MUTED)],
    [td("Transform",        C_INDIGO), tdc("Post-order"),tdc("Bottom-Up"), tdc("return modified root"),td("Invert Tree, Flatten", C_MUTED)],
]
story.append(std_table(cheat, [145, 80, 75, 110, 70]))
story.append(Spacer(1, 10))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
checks = [
    ("root is None?",         "Guard at top: return 0 / [] / None / True as appropriate."),
    ("Single node?",          "Test: left=None, right=None. Leaf check fires correctly?"),
    ("Skewed tree?",          "Deep recursion risk? Convert to iterative if depth > ~1000."),
    ("Bottom-Up or Top-Down?","Need subtree results? Bottom-Up. Need ancestor context? Top-Down."),
    ("Level-by-level?",       "BFS with deque. Snapshot len(queue) at start of each level."),
    ("BST property?",         "Use bounds (lo, hi) passed down, not just parent comparison."),
    ("Float('-inf') for max?","Initialize global max to float('-inf'), not 0 (handles all-negative)."),
    ("Backtrack path?",       "path.pop() after each recursive call in path-finding DFS."),
    ("identity 'is' vs '=='?","LCA and cycle detection: use 'is' (same object), not '==' (same value)."),
    ("Traversal order?",      "Pre = root first. In = sorted BST. Post = subtree aggregation."),
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
    P("<b>You now have the complete Binary Tree mental model.</b><br/><br/>"
      "Every tree problem is a traversal choice (pre/in/post/BFS) combined "
      "with a direction choice (top-down or bottom-up). The Base Case is almost "
      "always 'if root is None: return default', and the recursive step combines "
      "left and right results at the current node.<br/><br/>"
      "Recommended path: LC 104 → LC 226 → LC 543 → LC 102 → LC 112 → LC 236 → LC 124. "
      "After these seven problems you will have exercised every major pattern "
      "(bottom-up, top-down, BFS, path tracking, LCA, and global optimum) "
      "and will recognize them in any tree problem.",
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
        f"Binary Tree Patterns — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")