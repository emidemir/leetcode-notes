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
OUT = "/mnt/user-data/outputs/Graph_Patterns_Zero_To_Hero.pdf"

doc = SimpleDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)
CW = PAGE_W - 1.3 * inch   # usable content width

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


# ── ASCII art graph helper ─────────────────────────────────────────────────────
def graph_card(lines, title="", color=C_ACCENT):
    """Render ASCII-art graph diagram inside a dark card."""
    rows = []
    if title:
        rows.append([P(f"<b>{title}</b>",
                       S("_", fontName="Helvetica-Bold", fontSize=9.5,
                         textColor=color, alignment=TA_CENTER))])
    for ln in lines:
        rows.append([P(ln,
                       S("_", fontName="Courier", fontSize=9, leading=14,
                         textColor=C_BODY, alignment=TA_CENTER))])
    style_cmds = [
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
    ]
    if title:
        style_cmds.append(("LINEBELOW",(0,0),(-1,0),0.5,C_BORDER))
    return [Table(rows, colWidths=[CW], style=TableStyle(style_cmds)), Spacer(1,6)]


def two_cards(left_lines, right_lines, left_title, right_title,
              left_color=C_ACCENT, right_color=C_GREEN):
    """Two side-by-side ASCII graph cards."""
    half = int(CW / 2) - 4

    def make_card(lines, title, color, w):
        rows = [[P(f"<b>{title}</b>",
                   S("_", fontName="Helvetica-Bold", fontSize=9.5,
                     textColor=color, alignment=TA_CENTER))]]
        for ln in lines:
            rows.append([P(ln,
                           S("_", fontName="Courier", fontSize=9, leading=13,
                             textColor=C_BODY, alignment=TA_CENTER))])
        return Table(rows, colWidths=[w],
                     style=TableStyle([
                         ("BACKGROUND",(0,0),(-1,-1),C_CARD),
                         ("BOX",(0,0),(-1,-1),1,C_BORDER),
                         ("LINEBELOW",(0,0),(-1,0),0.5,C_BORDER),
                         ("TOPPADDING",(0,0),(-1,-1),4),
                         ("BOTTOMPADDING",(0,0),(-1,-1),4),
                         ("LEFTPADDING",(0,0),(-1,-1),6),
                         ("RIGHTPADDING",(0,0),(-1,-1),6),
                     ]))

    lcard = make_card(left_lines,  left_title,  left_color,  half)
    rcard = make_card(right_lines, right_title, right_color, half)
    return [
        Table([[lcard, rcard]], colWidths=[half+4, half+4],
              style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                                ("TOPPADDING",(0,0),(-1,-1),0),
                                ("BOTTOMPADDING",(0,0),(-1,-1),0),
                                ("LEFTPADDING",(0,0),(-1,-1),0),
                                ("RIGHTPADDING",(0,0),(-1,-1),0)])),
        Spacer(1, 8)
    ]


def matrix_grid(grid, row_labels=None, col_labels=None, highlight=None):
    """Render a small adjacency matrix with coloured cells."""
    highlight = highlight or set()
    n = len(grid)
    cell_w = 28
    extra  = 30  # row label column

    hdr = [P("",sCaption)]
    if col_labels:
        for c in col_labels:
            hdr.append(P(f"<b>{c}</b>",
                         S("_",fontName="Helvetica-Bold",fontSize=8,
                           textColor=C_MUTED,alignment=TA_CENTER)))

    data = [hdr]
    for r in range(n):
        row = [P(row_labels[r] if row_labels else str(r),
                 S("_",fontName="Helvetica-Bold",fontSize=8,
                   textColor=C_MUTED,alignment=TA_CENTER))]
        for c in range(n):
            row.append(P(str(grid[r][c]),
                         S("_",fontName="Courier-Bold",fontSize=9,
                           textColor=C_TEAL if grid[r][c] else C_MUTED,
                           alignment=TA_CENTER)))
        data.append(row)

    style_cmds = [
        ("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
        ("BACKGROUND",(0,0),(-1,0),C_BG),
        ("BACKGROUND",(0,0),(0,-1),C_BG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_CARD,C_DARK2]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]
    for (r,c) in highlight:
        style_cmds.append(("BACKGROUND",(c+1,r+1),(c+1,r+1),
                           colors.HexColor("#0A2E3A")))
    widths = [extra] + [cell_w]*n
    return Table(data, colWidths=widths, style=TableStyle(style_cmds))


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
        f"Graph Patterns — Zero to Hero  ·  Page {doc.page}")
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
story.append(P("GRAPH PATTERNS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubT))
story.append(Spacer(1, 0.12*inch))
story.append(P("Traversal Logic · Connectivity · State Management · Shortest Path · Topology", sAuthor))
story.append(Spacer(1, 0.18*inch))

story.append(Table([[
    P("<b>What You Will Master</b>",
      S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· Graph anatomy: vertices, edges, directed vs undirected, weighted vs unweighted\n"
       "· Adjacency List vs Adjacency Matrix — space, time, and when to use each\n"
       "· BFS: queue-based shortest path in unweighted graphs, layer-by-layer exploration\n"
       "· DFS: recursive and iterative, path finding, exhaustive search, cycle detection\n"
       "· Island Pattern: treating a 2D matrix as a graph with 4/8-directional neighbors\n"
       "· Cycle detection: Three-State DFS for directed; parent-pointer or Union-Find for undirected\n"
       "· Topological Sort: Kahn's in-degree BFS algorithm and its real-world applications\n"
       "· Union-Find (DSU): find, union, path compression, union by rank\n"
       "· Dijkstra's Algorithm: priority queue shortest path for weighted graphs\n"
       "· 30+ categorised LeetCode problems with traversal pattern labels",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))
]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CARD),
                      ("BOX",(0,0),(-1,-1),1,C_BORDER),
                      ("TOPPADDING",(0,0),(-1,-1),12),
                      ("BOTTOMPADDING",(0,0),(-1,-1),12),
                      ("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.22*inch))

# Quick-ref card on cover
qr = [
    [th("Algorithm"),       th("Time"),              th("Space"),     th("Best For")],
    [td("BFS"),             td("O(V+E)",C_GREEN),     td("O(V)",C_GREEN),
     td("Shortest path (unweighted), level-by-level, minimum hops",C_MUTED)],
    [td("DFS"),             td("O(V+E)",C_GREEN),     td("O(V) stack",C_GREEN),
     td("Connectivity, cycle detect, topological order, exhaustive paths",C_MUTED)],
    [td("Union-Find"),      td("O(alpha(V)) per op",C_GREEN),td("O(V)",C_GREEN),
     td("Dynamic connectivity, number of components, cycle in undirected",C_MUTED)],
    [td("Dijkstra"),        td("O((V+E) log V)",C_YELLOW),td("O(V)",C_GREEN),
     td("Shortest path in weighted graphs with non-negative edges",C_MUTED)],
    [td("Topo Sort (Kahn)"),td("O(V+E)",C_GREEN),     td("O(V+E)",C_YELLOW),
     td("Dependency ordering, course schedules, build systems",C_MUTED)],
    [td("Bellman-Ford"),    td("O(VE)",C_RED),         td("O(V)",C_GREEN),
     td("Shortest path with negative edges, negative cycle detection",C_MUTED)],
]
story.append(std_table(qr, [100, 105, 75, 238]))
story.append(Spacer(1, 0.24*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),
                      ("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ────────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc_items = [
    ("01","The Core Philosophy",
     ["Vertices, Edges, and Representations","Adjacency List vs Adjacency Matrix",
      "Directed / Undirected, Weighted / Unweighted"]),
    ("02","The Two Traversal Pillars",
     ["Breadth-First Search (BFS) — Shortest Path",
      "Depth-First Search (DFS) — Connectivity and Paths",
      "BFS vs DFS Decision Guide"]),
    ("03","The Island Pattern (Matrix as a Graph)",
     ["2D Grid Neighbor Logic (4-dir and 8-dir)",
      "Flood Fill and Connected Components",
      "In-place Marking vs Visited Set"]),
    ("04","Cycle Detection and Advanced Connectivity",
     ["Directed Graphs: Three-State DFS (White / Gray / Black)",
      "Undirected Graphs: Parent-Pointer DFS",
      "Union-Find Cycle Detection"]),
    ("05","Topological Sort — The Dependency Pattern",
     ["Kahn's Algorithm (BFS + In-degrees)",
      "DFS Post-Order Topological Sort",
      "Real-World Context: Build Systems"]),
    ("06","Union-Find (Disjoint Set Union)",
     ["Find with Path Compression",
      "Union by Rank / Size",
      "Connected Components and Cycle Detection"]),
    ("07","Shortest Path in Weighted Graphs",
     ["Why BFS Fails for Weighted Graphs",
      "Dijkstra's Algorithm with Priority Queue",
      "Bellman-Ford and When to Use It"]),
    ("08","Comparison and Decision Making",
     ["BFS vs DFS vs Union-Find","Adjacency List vs Matrix","Decision Flowchart"]),
    ("09","Problem Roadmap",
     ["Easy Problems","Medium Problems","Hard Problems"]),
    ("10","Edge Case Checklist",
     ["Disconnected Graphs (Forests)","Self-loops and Parallel Edges","Empty Graphs"]),
]
for num, title, subs in toc_items:
    story.append(P(f"<b>{num} &nbsp; {title}</b>", sTOC))
    for s in subs:
        story.append(P(f"&nbsp;&nbsp;&nbsp;&nbsp;› &nbsp;{s}", sTOCSub))
    story.append(Spacer(1, 3))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §1  CORE PHILOSOPHY
# ════════════════════════════════════════════════════════
story += section_divider(1, "The Core Philosophy")

story.append(P("<b>Vertices, Edges, and What a Graph Actually Is</b>", sH2))
story.append(P(
    "A <b>graph G = (V, E)</b> is a set of <b>vertices</b> (nodes) V and "
    "<b>edges</b> E that connect pairs of vertices. "
    "Unlike trees, graphs have no mandatory root, no parent-child hierarchy, "
    "and edges can form <b>cycles</b>. "
    "Almost every real-world network — road maps, social graphs, dependency chains, "
    "internet routing, circuit boards — is a graph problem in disguise.",
    sBody))

anat_data = [
    [th("Term"),          th("Definition"),                                        th("Example")],
    [td("Vertex / Node",C_ACCENT),  td("Basic unit of the graph, stores a value or ID",C_BODY),
     td("City, web page, user account",C_MUTED)],
    [td("Edge",     C_ACCENT),  td("Connection between two vertices",C_BODY),
     td("Road, hyperlink, friendship",C_MUTED)],
    [td("Degree",   C_BODY),    td("Number of edges incident to a vertex",C_BODY),
     td("In-degree + out-degree for directed graphs",C_MUTED)],
    [td("Path",     C_BODY),    td("Sequence of vertices connected by edges",C_BODY),
     td("Route from city A to city B",C_MUTED)],
    [td("Cycle",    C_YELLOW),  td("Path that starts and ends at the same vertex",C_BODY),
     td("A -> B -> C -> A",C_MUTED)],
    [td("Connected",C_GREEN),   td("Every vertex reachable from every other vertex",C_BODY),
     td("One connected component",C_MUTED)],
    [td("Forest",   C_ORANGE),  td("Acyclic undirected graph (collection of trees)",C_BODY),
     td("Disconnected acyclic graph",C_MUTED)],
    [td("DAG",      C_PURPLE),  td("Directed Acyclic Graph — directed, no cycles",C_BODY),
     td("Dependency graph, course prerequisites",C_MUTED)],
]
story.append(std_table(anat_data, [100, 230, 188]))
story.append(Spacer(1, 8))

story += two_cards(
    ["  (A)---(B)",
     "   |  \\ |",
     "  (C)---(D)",
     "",
     "Undirected: edges go both ways",
     "Degree(A) = 3",
    ],
    ["  (A)-->(B)",
     "   |     |",
     "   v     v",
     "  (C)-->(D)",
     "",
     "Directed: edges have direction",
     "In-degree(B)=1  Out-degree(A)=2",
    ],
    "UNDIRECTED GRAPH", "DIRECTED GRAPH",
    C_ACCENT, C_PURPLE
)

story.append(P("<b>Adjacency List vs Adjacency Matrix</b>", sH2))
story.append(P(
    "Every graph algorithm begins with the question: "
    "<i>how do I store this graph in memory?</i> "
    "The two canonical representations have dramatically different "
    "space and time trade-offs.",
    sBody))

rep_data = [
    [th("Dimension"),          th("Adjacency LIST"),                   th("Adjacency MATRIX")],
    [td("Space",     C_BODY),  td("O(V + E)",C_GREEN),                 td("O(V^2) — always allocates V*V cells",C_RED)],
    [td("Add edge",  C_BODY),  td("O(1) — append to list",C_GREEN),    td("O(1) — set matrix[u][v]=1",C_GREEN)],
    [td("Edge exists?",C_BODY),td("O(degree) — scan neighbour list",C_YELLOW),td("O(1) — matrix[u][v] lookup",C_GREEN)],
    [td("All neighbours",C_BODY),td("O(degree) — iterate list",C_GREEN),td("O(V) — scan entire row",C_RED)],
    [td("Dense graph (E~V^2)",C_BODY),td("OK but wastes list overhead",C_YELLOW),td("Efficient — nearly full anyway",C_GREEN)],
    [td("Sparse graph (E~V)",C_BODY),td("Optimal — O(V+E) storage",C_GREEN),td("Wasteful — mostly zeros",C_RED)],
    [td("Typical LeetCode",C_BODY),td("Almost always the right choice",C_GREEN),td("Only when explicitly asked or V is tiny",C_MUTED)],
]
story.append(std_table(rep_data, [130, 195, 193]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Adjacency List (defaultdict) — preferred ───────────────────",
    "from collections import defaultdict",
    "graph = defaultdict(list)",
    "",
    "## Build undirected graph from edge list",
    "for u, v in edges:",
    "    graph[u].append(v)",
    "    graph[v].append(u)   ## omit for directed graph",
    "",
    "## Build weighted undirected graph",
    "for u, v, w in weighted_edges:",
    "    graph[u].append((v, w))",
    "    graph[v].append((u, w))",
    "",
    "## ─── Adjacency Matrix — when V is small and dense ────────────────",
    "n = num_vertices",
    "matrix = [[0] * n for _ in range(n)]",
    "for u, v in edges:",
    "    matrix[u][v] = 1",
    "    matrix[v][u] = 1   ## omit for directed",
    "",
    "## ─── Why Adjacency Lists dominate in practice ────────────────────",
    "## Real graphs are SPARSE: a social network with 1B users averages",
    "## ~300 friends each — E is O(V), not O(V^2).",
    "## Matrix would need 1B x 1B = 10^18 cells. Impossible.",
    "## List needs 1B + 300B = ~1.3 x 10^11 entries. Feasible.",
])

story.append(P("<b>Directed / Undirected, Weighted / Unweighted</b>", sH3))
duw_data = [
    [th("Type"),                   th("Edge Meaning"),         th("Typical Algorithm")],
    [td("Undirected unweighted",C_BODY), td("Symmetric connection, no cost",C_BODY),
     td("BFS shortest path, DFS connectivity, Union-Find",C_MUTED)],
    [td("Directed unweighted",C_BODY),   td("One-way connection",C_BODY),
     td("Cycle detection (3-state DFS), topological sort",C_MUTED)],
    [td("Undirected weighted",C_BODY),   td("Symmetric connection with cost",C_BODY),
     td("Dijkstra, Prim's MST, Kruskal's MST",C_MUTED)],
    [td("Directed weighted",C_BODY),     td("One-way connection with cost",C_BODY),
     td("Dijkstra, Bellman-Ford, Floyd-Warshall",C_MUTED)],
]
story.append(std_table(duw_data, [150, 170, 198]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §2  TWO TRAVERSAL PILLARS
# ════════════════════════════════════════════════════════
story += section_divider(2, "The Two Traversal Pillars")

story.append(P("<b>Breadth-First Search (BFS) — Shortest Path in Unweighted Graphs</b>", sH2))
story.append(P(
    "BFS explores a graph layer by layer, visiting all vertices at distance d "
    "before any at distance d+1. This FIFO property — enforced by a queue — "
    "guarantees that the first time BFS reaches a vertex, it has found the "
    "<b>shortest path</b> (fewest hops) from the source. "
    "This guarantee holds <i>only</i> for unweighted graphs where every edge "
    "costs exactly 1.",
    sBody))

story += code_block([
    "from collections import deque",
    "",
    "## ─── BFS Template — shortest path, unweighted ────────────────────",
    "def bfs(graph, start):",
    "    visited = {start}",
    "    queue   = deque([(start, 0)])  ## (node, distance)",
    "    result  = []",
    "",
    "    while queue:",
    "        node, dist = queue.popleft()",
    "        result.append((node, dist))",
    "",
    "        for neighbour in graph[node]:",
    "            if neighbour not in visited:",
    "                visited.add(neighbour)",
    "                queue.append((neighbour, dist + 1))",
    "",
    "    return result",
    "",
    "## ─── BFS Shortest Path (with path reconstruction) ───────────────",
    "def shortest_path(graph, start, end):",
    "    parent  = {start: None}",
    "    queue   = deque([start])",
    "",
    "    while queue:",
    "        node = queue.popleft()",
    "        if node == end:",
    "            break",
    "        for nb in graph[node]:",
    "            if nb not in parent:",
    "                parent[nb] = node",
    "                queue.append(nb)",
    "",
    "    ## Reconstruct: walk parent pointers back from end to start",
    "    path, cur = [], end",
    "    while cur is not None:",
    "        path.append(cur); cur = parent.get(cur)",
    "    return path[::-1]   ## reverse to get start -> end",
    "",
    "## ─── Multi-source BFS (start from multiple nodes simultaneously) ─",
    "def multi_source_bfs(graph, sources):",
    "    visited = set(sources)",
    "    queue   = deque((s, 0) for s in sources)   ## seed all sources",
    "    while queue:",
    "        node, dist = queue.popleft()",
    "        for nb in graph[node]:",
    "            if nb not in visited:",
    "                visited.add(nb)",
    "                queue.append((nb, dist + 1))",
])

story += callout(
    "Why BFS guarantees shortest path: each level of BFS represents exactly one "
    "additional hop. Because we process level d before level d+1, the first time "
    "a node is dequeued its distance is minimal. No node is ever visited twice "
    "— the visited set ensures each edge is relaxed at most once.",
    C_ACCENT, icon="💡")

story.append(P("<b>Depth-First Search (DFS) — Connectivity and Path Finding</b>", sH2))
story.append(P(
    "DFS plunges as deep as possible down one branch before backtracking. "
    "It does not find the shortest path but it excels at "
    "<b>existence queries</b> (is there any path?), "
    "<b>connectivity</b> (are two nodes in the same component?), "
    "<b>cycle detection</b>, and <b>exhaustive search</b> (find all paths, "
    "count all valid configurations).",
    sBody))

story += code_block([
    "## ─── DFS Recursive Template ─────────────────────────────────────",
    "def dfs(graph, node, visited):",
    "    visited.add(node)",
    "    process(node)              ## do work at this node",
    "    for nb in graph[node]:",
    "        if nb not in visited:",
    "            dfs(graph, nb, visited)",
    "",
    "## ─── DFS Iterative (explicit stack) ─────────────────────────────",
    "def dfs_iterative(graph, start):",
    "    visited = {start}",
    "    stack   = [start]",
    "    while stack:",
    "        node = stack.pop()",
    "        process(node)",
    "        for nb in graph[node]:",
    "            if nb not in visited:",
    "                visited.add(nb)",
    "                stack.append(nb)",
    "",
    "## ─── DFS over disconnected graph (Forest) ────────────────────────",
    "def dfs_all_components(graph, n):",
    "    visited    = set()",
    "    components = 0",
    "    for node in range(n):      ## try every node as a potential source",
    "        if node not in visited:",
    "            dfs(graph, node, visited)",
    "            components += 1",
    "    return components",
])

story.append(P("<b>BFS vs DFS at a Glance</b>", sH3))
bfs_dfs = [
    [th("Dimension"),          th("BFS (Queue)"),                     th("DFS (Stack / Recursion)")],
    [td("Data structure"),     td("deque — FIFO",C_BODY),             td("call stack or explicit stack — LIFO",C_BODY)],
    [td("Shortest path?"),     td("Yes — in unweighted graphs",C_GREEN),td("No — finds A path, not shortest",C_RED)],
    [td("Memory (wide graph)"),td("O(V) — entire frontier in queue",C_YELLOW),td("O(depth) — only current path",C_GREEN)],
    [td("Memory (deep graph)"),td("O(1) — tiny frontier",C_GREEN),   td("O(V) — entire path on stack",C_RED)],
    [td("Cycle detection"),    td("Track visited; first revisit = cycle",C_BODY),td("Three-state (White/Gray/Black)",C_BODY)],
    [td("All paths"),          td("Possible but inefficient",C_YELLOW),td("Natural with backtracking",C_GREEN)],
    [td("Topological sort"),   td("Yes — Kahn's in-degree method",C_GREEN),td("Yes — post-order DFS",C_GREEN)],
    [td("Use when"),
     td("Shortest hops, level grouping, minimum steps, multi-source spread",C_MUTED),
     td("Connectivity, cycle detect, exhaustive search, DFS tree structure",C_MUTED)],
]
story.append(std_table(bfs_dfs, [125, 195, 198]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §3  ISLAND PATTERN
# ════════════════════════════════════════════════════════
story += section_divider(3, "The Island Pattern (Matrix as a Graph)")

story.append(P("<b>A 2D Grid Is Just a Graph</b>", sH2))
story.append(P(
    "Every cell (r, c) in a 2D grid is a <b>vertex</b>. "
    "Two cells are <b>adjacent</b> if they share an edge (4-directional) "
    "or a corner (8-directional). "
    "\"Island\" problems ask you to count, label, or measure connected regions "
    "of similar cells — which is just counting connected components of a graph "
    "defined over the grid.",
    sBody))

dirs_data = [
    [th("Mode"),         th("Directions"),          th("Delta (dr, dc)"),                th("Use case")],
    [td("4-directional",C_ACCENT),td("Up, Down, Left, Right",C_BODY),
     tdc("(-1,0),(1,0),(0,-1),(0,1)"),
     td("Number of islands, flood fill, shortest path in maze",C_MUTED)],
    [td("8-directional",C_ACCENT2),td("4-dir + all diagonals",C_BODY),
     tdc("all (dr,dc) in {-1,0,1}^2 \\ (0,0)"),
     td("Game of Life, surround regions, diagonal connectivity",C_MUTED)],
]
story.append(std_table(dirs_data, [105, 140, 145, 128]))
story.append(Spacer(1, 8))

# Grid visual
story += graph_card([
    "  Grid:                  After BFS/DFS from (0,0):",
    "  1 1 0 0 0              2 2 0 0 0",
    "  1 1 0 0 0    visit     2 2 0 0 0",
    "  0 0 1 0 0    island    0 0 3 0 0",
    "  0 0 0 1 1              0 0 0 4 4",
    "  0 0 0 1 1              0 0 0 4 4",
    "",
    "  4 islands: label each connected region of 1s.",
], "MATRIX AS GRAPH — Number of Islands", C_TEAL)
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Island Pattern Template (BFS) — O(rows * cols) ────────────",
    "from collections import deque",
    "",
    "def count_islands(grid):",
    "    if not grid: return 0",
    "    rows, cols = len(grid), len(grid[0])",
    "    visited = set()",
    "    count   = 0",
    "    DIRS    = [(-1,0),(1,0),(0,-1),(0,1)]   ## 4-directional",
    "",
    "    def bfs(r, c):",
    "        queue = deque([(r, c)])",
    "        visited.add((r, c))",
    "        while queue:",
    "            cr, cc = queue.popleft()",
    "            for dr, dc in DIRS:",
    "                nr, nc = cr+dr, cc+dc",
    "                if (0 <= nr < rows and 0 <= nc < cols",
    "                        and grid[nr][nc] == '1'",
    "                        and (nr, nc) not in visited):",
    "                    visited.add((nr, nc))",
    "                    queue.append((nr, nc))",
    "",
    "    for r in range(rows):",
    "        for c in range(cols):",
    "            if grid[r][c] == '1' and (r,c) not in visited:",
    "                bfs(r, c)",
    "                count += 1",
    "    return count",
    "",
    "## ─── In-place marking (modifies grid — avoids visited set) ──────",
    "def count_islands_inplace(grid):",
    "    rows, cols = len(grid), len(grid[0])",
    "    count = 0",
    "",
    "    def dfs(r, c):",
    "        if r < 0 or r >= rows or c < 0 or c >= cols: return",
    "        if grid[r][c] != '1': return",
    "        grid[r][c] = '#'   ## mark visited in-place",
    "        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:",
    "            dfs(r+dr, c+dc)",
    "",
    "    for r in range(rows):",
    "        for c in range(cols):",
    "            if grid[r][c] == '1':",
    "                dfs(r, c)",
    "                count += 1",
    "    return count",
])

story += callout(
    "In-place marking (setting visited cells to '#') saves O(rows*cols) space "
    "by avoiding a separate visited set. Only use it if modifying the input is "
    "acceptable. If the grid must stay pristine, use an explicit visited set "
    "or a boolean matrix.",
    C_YELLOW, icon="⚠️")
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §4  CYCLE DETECTION
# ════════════════════════════════════════════════════════
story += section_divider(4, "Cycle Detection & Advanced Connectivity")

story.append(P("<b>Directed Graphs: Three-State DFS</b>", sH2))
story.append(P(
    "In directed graphs, cycle detection requires distinguishing three node states "
    "during DFS: <b>White</b> (unvisited), <b>Gray</b> (in the current recursion "
    "stack — being processed), and <b>Black</b> (fully processed). "
    "If DFS reaches a <b>Gray</b> node, a back-edge exists — a cycle is confirmed. "
    "Reaching a <b>Black</b> node is safe; it was already fully explored.",
    sBody))

state_data = [
    [th("State"),      th("Colour"),   th("Meaning"),                       th("Action on revisit")],
    [td("UNVISITED",C_BODY), tdc("WHITE",C_HEADING), td("Not yet explored in this DFS",C_BODY),
     td("Start DFS from here",C_MUTED)],
    [td("IN STACK", C_BODY), tdc("GRAY", C_YELLOW),  td("Ancestor in current recursion path",C_BODY),
     td("CYCLE DETECTED — back-edge found",C_RED)],
    [td("DONE",     C_BODY), tdc("BLACK",C_GREEN),    td("Fully explored; all descendants processed",C_BODY),
     td("Safe — no new cycle from here",C_MUTED)],
]
story.append(std_table(state_data, [90, 70, 200, 158]))
story.append(Spacer(1, 8))

story += code_block([
    "## ─── Directed Cycle Detection: Three-State DFS ─────────────────",
    "WHITE, GRAY, BLACK = 0, 1, 2",
    "",
    "def has_cycle_directed(graph, n):",
    "    color = [WHITE] * n",
    "",
    "    def dfs(node):",
    "        color[node] = GRAY          ## mark: currently on stack",
    "        for nb in graph[node]:",
    "            if color[nb] == GRAY:   ## back-edge to ancestor",
    "                return True         ## CYCLE FOUND",
    "            if color[nb] == WHITE:  ## unvisited: explore",
    "                if dfs(nb): return True",
    "        color[node] = BLACK         ## fully processed",
    "        return False",
    "",
    "    for node in range(n):",
    "        if color[node] == WHITE:",
    "            if dfs(node): return True",
    "    return False",
])

story.append(P("<b>Undirected Graphs: Parent-Pointer DFS</b>", sH2))
story.append(P(
    "In undirected graphs, every edge appears in both directions — so DFS "
    "would trivially find a 'cycle' by stepping u→v and then v→u back. "
    "The trick: track the <b>parent</b> of each node and skip the edge back "
    "to the parent. Any other revisit is a genuine cycle.",
    sBody))

story += code_block([
    "## ─── Undirected Cycle Detection: Parent-Pointer DFS ──────────────",
    "def has_cycle_undirected(graph, n):",
    "    visited = set()",
    "",
    "    def dfs(node, parent):",
    "        visited.add(node)",
    "        for nb in graph[node]:",
    "            if nb == parent: continue    ## skip the edge we came from",
    "            if nb in visited: return True ## genuine back-edge = cycle",
    "            if dfs(nb, node): return True",
    "        return False",
    "",
    "    for node in range(n):",
    "        if node not in visited:",
    "            if dfs(node, -1): return True  ## -1: no parent for start",
    "    return False",
    "",
    "## Alternative: Union-Find cycle detection (Section 06)",
    "## As you add edges, union the two endpoints.",
    "## If find(u) == find(v) before union, u and v are already connected",
    "## — adding this edge creates a cycle.",
])

story += callout(
    "Rule of thumb: use Three-State DFS for directed graphs (course schedule, "
    "dependency validation) and parent-pointer DFS or Union-Find for undirected "
    "graphs (friend networks, physical connectivity).",
    C_ACCENT2, icon="🎯")
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §5  TOPOLOGICAL SORT
# ════════════════════════════════════════════════════════
story += section_divider(5, "Topological Sort — The Dependency Pattern")

story.append(P("<b>What Is Topological Order?</b>", sH2))
story.append(P(
    "A <b>topological ordering</b> of a DAG is a linear sequence of all vertices "
    "such that for every directed edge u → v, vertex u appears before v. "
    "It does not exist if the graph has a cycle (a cyclic dependency). "
    "Every DAG has at least one valid topological order.",
    sBody))

story += graph_card([
    "  Prerequisite graph:       One valid topological order:",
    "",
    "  Math(0) --> Algo(1)       0  -->  1  -->  3",
    "              |              |              ^",
    "  DB(2)   --> v         (0)  v         (2)|",
    "              CS(3)      Algo --> CS       |",
    "                               DB ---------+",
    "",
    "  Rule: if edge A->B exists, A must appear before B in the order.",
], "DAG — TOPOLOGICAL ORDER", C_PURPLE)
story.append(Spacer(1, 8))

story.append(P("<b>Kahn's Algorithm (BFS + In-degrees)</b>", sH2))
story.append(P(
    "Kahn's algorithm is the most intuitive topological sort: "
    "repeatedly pick a vertex with zero in-degree (no unsatisfied prerequisites), "
    "add it to the output, and reduce the in-degree of all its neighbours. "
    "If the output contains all V vertices, the graph is acyclic. "
    "If not, the remaining vertices form a cycle.",
    sBody))

story += code_block([
    "from collections import deque, defaultdict",
    "",
    "## ─── Kahn's Algorithm — O(V + E) ────────────────────────────────",
    "def topological_sort_kahns(n, prerequisites):",
    "    ## Build adjacency list and compute in-degrees",
    "    graph    = defaultdict(list)",
    "    in_degree = [0] * n",
    "",
    "    for course, prereq in prerequisites:",
    "        graph[prereq].append(course)   ## prereq -> course",
    "        in_degree[course] += 1",
    "",
    "    ## Seed: all nodes with in-degree 0 (no dependencies)",
    "    queue = deque(v for v in range(n) if in_degree[v] == 0)",
    "    order = []",
    "",
    "    while queue:",
    "        node = queue.popleft()",
    "        order.append(node)",
    "        for nb in graph[node]:",
    "            in_degree[nb] -= 1",
    "            if in_degree[nb] == 0:     ## all prerequisites satisfied",
    "                queue.append(nb)",
    "",
    "    ## Cycle check: if not all nodes processed, a cycle exists",
    "    return order if len(order) == n else []",
    "",
    "## ─── DFS Post-Order Topological Sort ─────────────────────────────",
    "def topological_sort_dfs(graph, n):",
    "    visited = set()",
    "    order   = []",
    "",
    "    def dfs(node):",
    "        visited.add(node)",
    "        for nb in graph[node]:",
    "            if nb not in visited:",
    "                dfs(nb)",
    "        order.append(node)   ## POST-ORDER: append after all descendants",
    "",
    "    for node in range(n):",
    "        if node not in visited:",
    "            dfs(node)",
    "",
    "    return order[::-1]   ## reverse post-order = topological order",
])

story.append(P("<b>Real-World Context</b>", sH3))
rw_data = [
    [th("Domain"),         th("Vertices"),          th("Edges"),                    th("Topological Order Means")],
    [td("Package manager",C_BODY), td("npm/pip packages",C_BODY), td("depends-on relationship",C_BODY),
     td("Install dependencies before dependents",C_MUTED)],
    [td("Compiler",C_BODY),       td("Source files / modules",C_BODY),td("import / #include",C_BODY),
     td("Compile imported modules before importer",C_MUTED)],
    [td("University courses",C_BODY),td("Courses",C_BODY),          td("prerequisite edge",C_BODY),
     td("Take Math before Algorithms",C_MUTED)],
    [td("Docker build layers",C_BODY),td("Docker layers",C_BODY),   td("FROM / COPY dependencies",C_BODY),
     td("Build base layers before dependent layers",C_MUTED)],
    [td("Django migrations",C_BODY),  td("Migration files",C_BODY), td("dependencies = [...]",C_BODY),
     td("Apply earlier migrations before later ones",C_MUTED)],
]
story.append(std_table(rw_data, [115, 115, 120, 168]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §6  UNION-FIND
# ════════════════════════════════════════════════════════
story += section_divider(6, "Union-Find (Disjoint Set Union)")

story.append(P("<b>The Core Operations</b>", sH2))
story.append(P(
    "Union-Find (DSU) maintains a collection of disjoint sets. "
    "It supports two operations in near-constant amortised time: "
    "<b>find(x)</b> returns the <i>representative</i> (root) of x's set, "
    "and <b>union(x, y)</b> merges the sets containing x and y. "
    "Two nodes are connected if and only if they share the same representative.",
    sBody))

story += code_block([
    "## ─── Union-Find with Path Compression + Union by Rank ──────────",
    "class UnionFind:",
    "    def __init__(self, n):",
    "        self.parent = list(range(n))  ## each node is its own root",
    "        self.rank   = [0] * n         ## tree height upper bound",
    "        self.count  = n               ## number of connected components",
    "",
    "    def find(self, x):",
    "        ## Path Compression: point every node directly to root",
    "        if self.parent[x] != x:",
    "            self.parent[x] = self.find(self.parent[x])  ## recursive",
    "        return self.parent[x]",
    "",
    "    def union(self, x, y):",
    "        rx, ry = self.find(x), self.find(y)",
    "        if rx == ry: return False     ## already connected — CYCLE if adding edge",
    "",
    "        ## Union by Rank: attach smaller tree under larger",
    "        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx",
    "        self.parent[ry] = rx",
    "        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1",
    "        self.count -= 1",
    "        return True                   ## successfully merged",
    "",
    "    def connected(self, x, y):",
    "        return self.find(x) == self.find(y)",
    "",
    "## ─── Count connected components ─────────────────────────────────",
    "uf = UnionFind(n)",
    "for u, v in edges:",
    "    uf.union(u, v)",
    "print(uf.count)   ## number of remaining distinct components",
    "",
    "## ─── Cycle detection in undirected graph ─────────────────────────",
    "uf = UnionFind(n)",
    "for u, v in edges:",
    "    if not uf.union(u, v):   ## returns False when u,v already connected",
    "        print('CYCLE DETECTED')",
    "        break",
])

story.append(P("<b>The Two Key Optimisations</b>", sH3))
opt_data = [
    [th("Optimisation"),     th("Idea"),                                th("Effect"),               th("Complexity without / with")],
    [td("Path Compression",C_ACCENT),
     td("After finding root, point every visited node directly to root",C_BODY),
     td("Flattens tree — future finds faster",C_GREEN),
     td("O(log n) without / O(alpha(n)) with",C_MUTED)],
    [td("Union by Rank",C_GREEN),
     td("Attach shorter tree under taller tree during union",C_BODY),
     td("Keeps tree height O(log n) max",C_GREEN),
     td("O(n) per op without / O(log n) with rank alone",C_MUTED)],
    [td("Both together",C_PURPLE),
     td("Path compression + union by rank",C_BODY),
     td("Near-constant amortised per operation",C_GREEN),
     td("O(alpha(n)) — essentially O(1) for all practical n",C_MUTED)],
]
story.append(std_table(opt_data, [110, 175, 115, 118]))
story.append(Spacer(1, 8))

# Visual trace of path compression
story += graph_card([
    "  BEFORE path compression:       AFTER find(4):",
    "",
    "       1                              1",
    "       |                            / | \\",
    "       2                           2  3   4",
    "       |",
    "       3",
    "       |",
    "       4      find(4) traces 4->3->2->1, then rewires all to root 1",
], "PATH COMPRESSION — Every Node Points Directly to Root", C_ACCENT)
story.append(Spacer(1, 8))

story += callout(
    "When to use Union-Find vs DFS: Union-Find shines for DYNAMIC connectivity "
    "— when edges arrive one by one and you need to answer 'are x and y connected?' "
    "after each addition. DFS is better for STATIC graphs where you have all edges "
    "upfront and need to traverse structure (paths, cycles, topology).",
    C_TEAL, icon="🎯")
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §7  SHORTEST PATH WEIGHTED GRAPHS
# ════════════════════════════════════════════════════════
story += section_divider(7, "Shortest Path in Weighted Graphs")

story.append(P("<b>Why BFS Fails for Weighted Graphs</b>", sH2))
story.append(P(
    "BFS treats every edge as cost 1. "
    "When edges have different weights, two paths with the same number of hops "
    "can have very different total costs. "
    "BFS would return the minimum-hop path, not the minimum-cost path.",
    sBody))

story += two_cards(
    [" A --1-- B --1-- D",
     " |               ^",
     " +---10------C---+",
     "",
     " BFS says A->B->D = 2 hops",
     " BFS says A->C->D = 2 hops",
     " BFS can't distinguish them!",
     " Actual costs: 2 vs 11",
    ],
    [" A --1-- B --1-- D",
     " |               ^",
     " +---10------C---+",
     "",
     " Dijkstra finds A->B->D = cost 2",
     " (not A->C->D = cost 11)",
     "",
     " Priority queue by dist from A",
    ],
    "WHY BFS FAILS (WEIGHTED)", "WHY DIJKSTRA WORKS",
    C_RED, C_GREEN
)

story.append(P("<b>Dijkstra's Algorithm</b>", sH2))
story.append(P(
    "Dijkstra maintains a <b>distance table</b> dist[v] = shortest known distance "
    "from source to v, initialised to infinity. "
    "It greedily processes the unvisited vertex with the smallest known distance "
    "using a min-heap (priority queue). "
    "When a vertex is popped from the heap, its distance is final — "
    "no future path can be shorter (because all edge weights are non-negative).",
    sBody))

story += code_block([
    "import heapq",
    "",
    "## ─── Dijkstra's Algorithm — O((V + E) log V) ────────────────────",
    "def dijkstra(graph, start, n):",
    "    ## graph: adjacency list of (neighbour, weight) tuples",
    "    dist = [float('inf')] * n",
    "    dist[start] = 0",
    "    heap = [(0, start)]   ## (distance, node)",
    "",
    "    while heap:",
    "        d, node = heapq.heappop(heap)",
    "",
    "        ## Lazy removal: stale entry if a shorter path was found",
    "        if d > dist[node]: continue",
    "",
    "        for nb, weight in graph[node]:",
    "            new_dist = dist[node] + weight",
    "            if new_dist < dist[nb]:       ## found a shorter path",
    "                dist[nb] = new_dist",
    "                heapq.heappush(heap, (new_dist, nb))",
    "",
    "    return dist   ## dist[v] = shortest distance from start to v",
    "",
    "## ─── Dijkstra with path reconstruction ──────────────────────────",
    "def dijkstra_path(graph, start, end, n):",
    "    dist   = [float('inf')] * n",
    "    parent = [-1] * n",
    "    dist[start] = 0",
    "    heap   = [(0, start)]",
    "",
    "    while heap:",
    "        d, node = heapq.heappop(heap)",
    "        if d > dist[node]: continue",
    "        for nb, w in graph[node]:",
    "            if dist[node] + w < dist[nb]:",
    "                dist[nb]   = dist[node] + w",
    "                parent[nb] = node",
    "                heapq.heappush(heap, (dist[nb], nb))",
    "",
    "    path, cur = [], end",
    "    while cur != -1: path.append(cur); cur = parent[cur]",
    "    return path[::-1], dist[end]",
])

story.append(P("<b>Dijkstra vs BFS vs Bellman-Ford</b>", sH3))
sp_data = [
    [th("Algorithm"),       th("Edge weights"),     th("Time"),              th("Use when")],
    [td("BFS"),             td("Unweighted (all=1)",C_GREEN),  td("O(V+E)",C_GREEN),
     td("All edges cost 1; minimum hops; grid problems",C_MUTED)],
    [td("Dijkstra"),        td("Non-negative",C_GREEN),        td("O((V+E) log V)",C_YELLOW),
     td("Weighted graph; no negative edges; road networks",C_MUTED)],
    [td("Bellman-Ford"),    td("Any (incl. negative)",C_YELLOW),td("O(VE)",C_RED),
     td("Negative edges; detect negative-weight cycles",C_MUTED)],
    [td("Floyd-Warshall"),  td("Any",C_YELLOW),                td("O(V^3)",C_RED),
     td("All-pairs shortest path; small V (V <= 500)",C_MUTED)],
    [td("0-1 BFS"),         td("0 or 1 only",C_TEAL),          td("O(V+E)",C_GREEN),
     td("Grid with free and unit-cost moves (deque trick)",C_MUTED)],
]
story.append(std_table(sp_data, [100, 110, 100, 208]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §8  COMPARISON & DECISION
# ════════════════════════════════════════════════════════
story += section_divider(8, "Comparison & Decision Making")

story.append(P("<b>BFS vs DFS vs Union-Find</b>", sH2))
big3 = [
    [th("Dimension"),          th("BFS"),                         th("DFS"),                        th("Union-Find")],
    [td("Data structure"),     td("Queue (deque)",C_BODY),        td("Stack / call stack",C_BODY),  td("parent[] + rank[] arrays",C_BODY)],
    [td("Shortest path"),      td("Yes — unweighted",C_GREEN),    td("No",C_RED),                   td("No",C_RED)],
    [td("Cycle detection"),    td("Possible with visited",C_YELLOW),td("Three-state for directed",C_GREEN),td("Best for undirected",C_GREEN)],
    [td("Connectivity"),       td("Yes",C_GREEN),                 td("Yes",C_GREEN),                td("Yes — dynamic",C_GREEN)],
    [td("Topological sort"),   td("Yes — Kahn's",C_GREEN),        td("Yes — post-order",C_GREEN),   td("No",C_RED)],
    [td("Dynamic edges"),      td("Rebuild graph each time",C_RED),td("Rebuild each time",C_RED),   td("O(alpha) per edge add",C_GREEN)],
    [td("Memory"),             td("O(V) frontier",C_BODY),        td("O(V) stack frames",C_BODY),   td("O(V) arrays",C_GREEN)],
    [td("Code complexity"),    td("Simple — deque template",C_GREEN),td("Simple — recursive",C_GREEN),td("Medium — DSU class",C_YELLOW)],
    [td("Best for"),
     td("Min hops, level order, multi-source spread, 0-1 BFS",C_MUTED),
     td("All paths, cycle detect directed, topo sort, exhaustive",C_MUTED),
     td("Offline connectivity, MST (Kruskal), redundant connections",C_MUTED)],
]
story.append(std_table(big3, [110, 140, 145, 123]))
story.append(Spacer(1, 10))

story.append(P("<b>Adjacency List vs Adjacency Matrix</b>", sH2))
adj_cmp = [
    [th("Dimension"),          th("Adjacency LIST"),                  th("Adjacency MATRIX")],
    [td("Space"),              td("O(V + E)",C_GREEN),                 td("O(V^2)",C_RED)],
    [td("Iterate neighbours"), td("O(degree) — optimal",C_GREEN),     td("O(V) — scan full row",C_RED)],
    [td("Edge existence"),     td("O(degree) — scan list",C_YELLOW),  td("O(1) — index lookup",C_GREEN)],
    [td("Add edge"),           td("O(1) amortised",C_GREEN),           td("O(1)",C_GREEN)],
    [td("Remove edge"),        td("O(degree) — find and remove",C_YELLOW),td("O(1)",C_GREEN)],
    [td("Dense graph (E=V^2)"),td("OK but pointer overhead",C_YELLOW),td("Efficient, no wasted space",C_GREEN)],
    [td("Sparse graph (E&lt;&lt;V^2)"),td("Efficient — only store real edges",C_GREEN),td("Wastes O(V^2) for zeros",C_RED)],
    [td("Typical graph problem"),td("Use this — almost all LeetCode graphs are sparse",C_GREEN),
     td("Only when V is tiny (<= 100) or explicit 'is edge present?' queries",C_MUTED)],
]
story.append(std_table(adj_cmp, [155, 215, 148]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1","Is the graph on a 2D grid/matrix?",                               C_ACCENT, False),
    (" YES","Island Pattern — BFS/DFS with 4-dir DIRS array.",               C_GREEN,  True),
    (" NO", "Continue to Q2.",                                                C_MUTED,  True),
    ("Q2","Do you need the minimum number of hops / steps (unweighted)?",    C_ACCENT, False),
    (" YES","BFS. Process level-by-level with a deque.",                     C_GREEN,  True),
    (" NO", "Continue to Q3.",                                                C_MUTED,  True),
    ("Q3","Do you need shortest path with weighted edges?",                  C_ACCENT, False),
    (" YES","Dijkstra (non-negative weights) or Bellman-Ford (negative ok).",C_YELLOW, True),
    (" NO", "Continue to Q4.",                                                C_MUTED,  True),
    ("Q4","Is this a DAG with dependency / ordering constraint?",            C_ACCENT, False),
    (" YES","Topological Sort — Kahn's BFS or DFS post-order.",              C_PURPLE, True),
    (" NO", "Continue to Q5.",                                                C_MUTED,  True),
    ("Q5","Do edges arrive dynamically? Count components or detect cycles?", C_ACCENT, False),
    (" YES","Union-Find. O(alpha) per union/find after build.",              C_TEAL,   True),
    (" NO", "DFS for static connectivity / exhaustive search / cycle detect.",C_MUTED, True),
]
for label, text, clr, is_branch in flow:
    bg = C_DARK2 if is_branch else C_CARD
    story.append(Table([[
        P(f"<b>{label}</b>",
          S("_", fontName="Courier-Bold", fontSize=9, textColor=clr)),
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
# §9  PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(9, "LeetCode Problem Roadmap")
story.append(P("Solve in order — each problem introduces one new graph concept.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy = [
    [th("#"),  th("Problem"),                              th("Pattern"),          th("Key Insight")],
    [tdc("733", C_GREEN), td("Flood Fill",                C_BODY),
     td("DFS/BFS Matrix",   C_ACCENT),
     td("4-dir DFS; replace old color with new. Guard against same-color start.",C_MUTED)],
    [tdc("463", C_GREEN), td("Island Perimeter",          C_BODY),
     td("Matrix traversal",C_ACCENT),
     td("For each land cell: perimeter += 4 - (land neighbours). No DFS needed.",C_MUTED)],
    [tdc("997", C_GREEN), td("Find the Town Judge",       C_BODY),
     td("In/Out degree",   C_TEAL),
     td("Judge: in-degree = n-1 AND out-degree = 0. Count trust arrays.",C_MUTED)],
    [tdc("1791",C_GREEN), td("Find Center of Star Graph", C_BODY),
     td("Degree",         C_TEAL),
     td("Center appears in both edges[0] and edges[1].",C_MUTED)],
    [tdc("841", C_GREEN), td("Keys and Rooms",            C_BODY),
     td("DFS/BFS",        C_ACCENT),
     td("BFS/DFS from room 0; visited = unlocked rooms; return len==n.",C_MUTED)],
]
story.append(std_table(easy, [38, 200, 115, 165]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med = [
    [th("#"),  th("Problem"),                                  th("Pattern"),              th("Key Insight")],
    [tdc("200", C_YELLOW), td("Number of Islands",            C_BODY),
     td("BFS/DFS Matrix",      C_ACCENT),
     td("Iterate all cells; BFS/DFS from unvisited land. Mark visited.",C_MUTED)],
    [tdc("695", C_YELLOW), td("Max Area of Island",           C_BODY),
     td("DFS Matrix",          C_ACCENT),
     td("DFS returns size; track global max.",C_MUTED)],
    [tdc("994", C_YELLOW), td("Rotting Oranges",              C_BODY),
     td("Multi-source BFS",    C_GREEN),
     td("Seed all rotten oranges; BFS levels = minutes elapsed.",C_MUTED)],
    [tdc("133", C_YELLOW), td("Clone Graph",                  C_BODY),
     td("DFS + HashMap",       C_ACCENT2),
     td("old->new node map; DFS creates clones avoiding revisits.",C_MUTED)],
    [tdc("207", C_YELLOW), td("Course Schedule",              C_BODY),
     td("Cycle detect directed",C_PURPLE),
     td("Three-state DFS or Kahn's. Cycle => impossible.",C_MUTED)],
    [tdc("210", C_YELLOW), td("Course Schedule II",           C_BODY),
     td("Topological Sort",    C_PURPLE),
     td("Kahn's algorithm; return order[] if len == n.",C_MUTED)],
    [tdc("417", C_YELLOW), td("Pacific Atlantic Water Flow",  C_BODY),
     td("Multi-source BFS",    C_GREEN),
     td("Reverse BFS from each ocean; intersection = answer.",C_MUTED)],
    [tdc("323", C_YELLOW), td("Number of Connected Components",C_BODY),
     td("Union-Find / DFS",    C_TEAL),
     td("Union-Find: count after all unions. DFS: count outer calls.",C_MUTED)],
    [tdc("684", C_YELLOW), td("Redundant Connection",         C_BODY),
     td("Union-Find cycle",    C_TEAL),
     td("Process edges; first union() that returns False is redundant.",C_MUTED)],
    [tdc("743", C_YELLOW), td("Network Delay Time",           C_BODY),
     td("Dijkstra",            C_ORANGE),
     td("Dijkstra from source; answer = max(dist[]). INF => impossible.",C_MUTED)],
]
story.append(std_table(med, [38, 200, 130, 150]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard = [
    [th("#"),  th("Problem"),                                      th("Pattern"),              th("Key Insight")],
    [tdc("127", C_RED), td("Word Ladder",                         C_BODY),
     td("BFS — shortest transform",C_GREEN),
     td("BFS on word graph; each level = one transformation. Early exit at target.",C_MUTED)],
    [tdc("212", C_RED), td("Word Search II",                      C_BODY),
     td("DFS + Trie",           C_ACCENT),
     td("Build Trie of words; DFS grid pruning with Trie traversal.",C_MUTED)],
    [tdc("269", C_RED), td("Alien Dictionary",                    C_BODY),
     td("Topological Sort",     C_PURPLE),
     td("Extract ordering from adjacent words; Kahn's on char DAG.",C_MUTED)],
    [tdc("332", C_RED), td("Reconstruct Itinerary",               C_BODY),
     td("Eulerian path DFS",    C_ACCENT2),
     td("Hierholzer's: DFS; push to result after exhausting neighbours.",C_MUTED)],
    [tdc("1192",C_RED), td("Critical Connections in a Network",   C_BODY),
     td("Bridges — Tarjan DFS", C_ROSE),
     td("Track disc/low; edge (u,v) is bridge if low[v] > disc[u].",C_MUTED)],
    [tdc("778", C_RED), td("Swim in Rising Water",                C_BODY),
     td("Dijkstra / Binary Search",C_ORANGE),
     td("Dijkstra: cost = max(path) not sum. Or binary search + BFS.",C_MUTED)],
]
story.append(std_table(hard, [38, 205, 135, 140]))
story.append(PageBreak())


# ════════════════════════════════════════════════════════
# §10  EDGE CASES
# ════════════════════════════════════════════════════════
story += section_divider(10, "Edge Case Checklist")

story.append(P(
    "Graph problems have a predictable set of edge cases that cause "
    "wrong answers or runtime errors. Check every solution against these.",
    sBody))

story.append(P("<b>Edge Case 1: Disconnected Graphs (Forests)</b>", sH2))
story.append(P(
    "A disconnected graph has multiple connected components — "
    "BFS or DFS from one node will not visit all vertices. "
    "Always wrap traversal in an outer loop over all nodes.",
    sBody))
story += code_block([
    "## WRONG: single-source BFS misses disconnected components",
    "def wrong_count_components(graph, n):",
    "    visited = set()",
    "    bfs(graph, 0, visited)   ## only explores component containing 0",
    "    return ???",
    "",
    "## CORRECT: outer loop ensures every unvisited node is a new source",
    "def count_components(graph, n):",
    "    visited = set()",
    "    count   = 0",
    "    for node in range(n):        ## try EVERY node as source",
    "        if node not in visited:",
    "            bfs(graph, node, visited)",
    "            count += 1",
    "    return count",
    "",
    "## Same pattern applies to:",
    "## - Counting islands (outer loop over grid cells)",
    "## - Topological sort (outer loop ensures all nodes in output)",
    "## - DFS post-order topo sort (outer loop for forest case)",
])

story.append(P("<b>Edge Case 2: Self-Loops and Parallel Edges</b>", sH2))
story += code_block([
    "## Self-loop: edge u -> u (node connects to itself)",
    "## Impact: DFS will try to visit u from u — immediately caught by visited set.",
    "## Cycle detection: a self-loop is ALWAYS a cycle in any graph.",
    "",
    "## Parent-pointer DFS for undirected cycle detection:",
    "## WRONG with parallel edges: two edges u-v and u-v will trigger false cycle.",
    "## parent tracking only skips ONE back-edge, not duplicates.",
    "",
    "## Fix for multigraphs (parallel edges) in undirected cycle detection:",
    "## Track parent EDGE INDEX, not parent node:",
    "def dfs_multigraph(node, parent_edge_idx, adj, visited):",
    "    visited.add(node)",
    "    for nb, edge_idx in adj[node]:",
    "        if edge_idx == parent_edge_idx: continue   ## skip exact edge used",
    "        if nb in visited: return True              ## genuine cycle",
    "        if dfs_multigraph(nb, edge_idx, adj, visited): return True",
    "    return False",
    "",
    "## Union-Find handles parallel edges naturally:",
    "## Second edge u-v will find find(u) == find(v) (already unioned) => cycle.",
])

story.append(P("<b>Edge Case 3: Empty Graph or Single Node</b>", sH2))
story += code_block([
    "## Empty graph: n=0 or empty edge list",
    "def process_graph(n, edges):",
    "    if n == 0: return DEFAULT_ANSWER   ## no nodes, no components",
    "    if not edges: return n             ## n isolated nodes = n components",
    "    ## ... rest of algorithm",
    "",
    "## Single node: n=1, no edges",
    "## BFS: queue seeds [0], pops immediately, no neighbours → result=[0]",
    "## DFS: visits node 0, no neighbours, returns → visited={0}",
    "## Union-Find: 1 component from __init__, no unions → count=1",
    "## All handle correctly with standard templates.",
    "",
    "## Empty grid (Island Pattern):",
    "def count_islands(grid):",
    "    if not grid or not grid[0]: return 0   ## guard empty grid",
    "    rows, cols = len(grid), len(grid[0])",
    "    ## ...",
    "",
    "## Dijkstra on single node:",
    "## dist[start] = 0, all others = inf. Heap pops start immediately.",
    "## No neighbours → returns [0, inf, inf, ...]. Correct.",
])

story.append(P("<b>Edge Case 4: Visited Set Placement</b>", sH3))
story += code_block([
    "## WRONG: add to visited when POPPED — may process same node twice",
    "queue = deque([start])",
    "while queue:",
    "    node = queue.popleft()",
    "    visited.add(node)              ## TOO LATE: duplicates already queued",
    "    for nb in graph[node]:",
    "        queue.append(nb)",
    "",
    "## CORRECT: add to visited when ENQUEUED — prevents duplicates",
    "visited = {start}",
    "queue   = deque([start])",
    "while queue:",
    "    node = queue.popleft()",
    "    for nb in graph[node]:",
    "        if nb not in visited:",
    "            visited.add(nb)        ## mark BEFORE enqueuing",
    "            queue.append(nb)",
    "",
    "## Exception: some problems need dequeue-time marking",
    "## (e.g., when state is (node, other_param) and same node can be",
    "## revisited with a different state). Always think about what",
    "## 'visited' means — the NODE or the FULL STATE.",
])

story += callout(
    "The most common graph bug: forgetting to call the traversal on ALL nodes "
    "(missing the outer loop for disconnected graphs). Second most common: "
    "marking visited at pop-time instead of enqueue-time, causing the same "
    "node to be enqueued multiple times and inflating runtime.",
    C_RED, icon="⚠️")

# ── MASTER CHEAT SHEET ─────────────────────────────────────────────────────────
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")

cheat = [
    [th("Pattern"),               th("Algorithm"),      th("Key Data Structure"),    th("Classic Problem")],
    [td("Shortest hops",   C_ACCENT),  td("BFS",         C_GREEN),
     tdc("deque, visited set"),   td("Word Ladder, Rotting Oranges",C_MUTED)],
    [td("All paths / exhaustive",C_ACCENT),td("DFS",    C_GREEN),
     tdc("recursion stack"),       td("All Paths DAG, Permutations",C_MUTED)],
    [td("Island / Flood Fill",C_TEAL),td("BFS or DFS",  C_GREEN),
     tdc("DIRS array, visited set"),td("Number of Islands, Flood Fill",C_MUTED)],
    [td("Cycle — directed", C_YELLOW),td("Three-State DFS",C_PURPLE),
     tdc("color[] WHITE/GRAY/BLACK"),td("Course Schedule I",C_MUTED)],
    [td("Cycle — undirected",C_YELLOW),td("Parent-ptr DFS / UF",C_TEAL),
     tdc("parent node or DSU"),    td("Redundant Connection",C_MUTED)],
    [td("Dependency order",C_PURPLE),td("Kahn's Topo Sort",C_GREEN),
     tdc("in_degree[], BFS queue"),td("Course Schedule II, Alien Dict",C_MUTED)],
    [td("Dynamic connectivity",C_ORANGE),td("Union-Find",C_TEAL),
     tdc("parent[], rank[]"),      td("Number of Components, MST",C_MUTED)],
    [td("Weighted shortest path",C_ROSE),td("Dijkstra",  C_ORANGE),
     tdc("min-heap (dist, node)"), td("Network Delay, Path With Min Effort",C_MUTED)],
    [td("Multi-source spread",C_GREEN),td("Multi-source BFS",C_GREEN),
     tdc("seed all sources in queue"),td("Rotting Oranges, Pacific Atlantic",C_MUTED)],
]
story.append(std_table(cheat, [145, 110, 150, 113]))
story.append(Spacer(1, 10))

story.append(P("<b>Pre-Code Checklist</b>", sH2))
checks = [
    ("Outer loop for all nodes?",   "Wrap BFS/DFS in 'for node in range(n)' to handle disconnected graphs."),
    ("Visited at enqueue time?",    "Add to visited BEFORE appending to queue, not after popping."),
    ("Directed or undirected?",     "Undirected: add both directions. Directed: one direction only."),
    ("Weighted or unweighted?",     "Unweighted -> BFS. Non-neg weights -> Dijkstra. Neg weights -> Bellman-Ford."),
    ("Cycle detection method?",     "Directed: three-state DFS. Undirected: parent-pointer or Union-Find."),
    ("Grid bounds check?",          "0 <= nr < rows AND 0 <= nc < cols before accessing grid[nr][nc]."),
    ("Empty graph guard?",          "if not grid or not grid[0]: return 0 for matrix problems."),
    ("Self-loop / parallel edges?", "Self-loops always a cycle. Parallel edges need edge-index tracking."),
    ("Topological sort cycle?",     "Kahn's: if len(order) < n, cycle exists. DFS: if GRAY node visited."),
    ("Union-Find initialized?",     "parent = list(range(n)); rank = [0]*n; count = n at start."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ]  {q}</font></b>",
          S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[175, CW-175],
        style=TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),C_CARD),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

story.append(Table([[P(
    "<b>You now have the complete Graph Patterns mental model.</b><br/><br/>"
    "Every graph problem reduces to three questions: "
    "<i>What is the graph structure? What traversal guarantees do I need? "
    "What state must I track?</i><br/><br/>"
    "Unweighted shortest path — BFS.  "
    "Connectivity or exhaustive paths — DFS.  "
    "Dynamic connectivity — Union-Find.  "
    "Dependency ordering — Topological Sort.  "
    "Weighted shortest path — Dijkstra.<br/><br/>"
    "Recommended path: LC 733 -> LC 200 -> LC 994 -> LC 207 -> LC 210 -> "
    "LC 684 -> LC 743 -> LC 127. "
    "These eight problems exercise every major pattern: flood fill, "
    "island BFS, multi-source BFS, cycle detection, topological sort, "
    "Union-Find, Dijkstra, and BFS shortest transformation.",
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