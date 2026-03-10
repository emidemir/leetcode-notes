from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor
import textwrap

# ── Color Palette ──────────────────────────────────────────────────────────────
C_BG_DARK    = HexColor("#0F172A")   # deep navy – page-level accent
C_ACCENT     = HexColor("#6366F1")   # indigo
C_ACCENT2    = HexColor("#10B981")   # emerald
C_ACCENT3    = HexColor("#F59E0B")   # amber
C_DANGER     = HexColor("#EF4444")   # red
C_CODE_BG    = HexColor("#1E293B")   # slate-800
C_CODE_FG    = HexColor("#E2E8F0")   # slate-200
C_BORDER     = HexColor("#334155")   # slate-700
C_LIGHT_BG   = HexColor("#F1F5F9")   # slate-100
C_TEXT       = HexColor("#1E293B")
C_MUTED      = HexColor("#64748B")
C_WHITE      = colors.white
C_YELLOW_BG  = HexColor("#FFFBEB")
C_GREEN_BG   = HexColor("#ECFDF5")
C_BLUE_BG    = HexColor("#EFF6FF")
C_RED_BG     = HexColor("#FEF2F2")

# ── Styles ─────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def add(name, **kw):
        if name not in base:
            base.add(ParagraphStyle(name=name, **kw))
        return base[name]

    # Cover
    add("CoverTitle",    fontName="Helvetica-Bold",   fontSize=36, textColor=C_WHITE,
        alignment=TA_CENTER, spaceAfter=8, leading=44)
    add("CoverSub",      fontName="Helvetica",        fontSize=14, textColor=HexColor("#94A3B8"),
        alignment=TA_CENTER, spaceAfter=6)
    add("CoverTag",      fontName="Helvetica-Bold",   fontSize=11, textColor=C_ACCENT,
        alignment=TA_CENTER, spaceAfter=4)

    # Section headers
    add("H1",  fontName="Helvetica-Bold", fontSize=22, textColor=C_ACCENT,
        spaceAfter=6, spaceBefore=18, leading=28, borderPad=2)
    add("H2",  fontName="Helvetica-Bold", fontSize=15, textColor=C_TEXT,
        spaceAfter=4, spaceBefore=12, leading=20)
    add("H3",  fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT2,
        spaceAfter=3, spaceBefore=8, leading=16)

    # Body
    add("Body", fontName="Helvetica", fontSize=10, textColor=C_TEXT,
        spaceAfter=6, leading=15, alignment=TA_JUSTIFY)
    add("BodyBold", fontName="Helvetica-Bold", fontSize=10, textColor=C_TEXT,
        spaceAfter=6, leading=15)
    add("Bullet", fontName="Helvetica", fontSize=10, textColor=C_TEXT,
        spaceAfter=4, leading=14, leftIndent=16, firstLineIndent=-10)
    add("SubBullet", fontName="Helvetica", fontSize=9.5, textColor=C_MUTED,
        spaceAfter=3, leading=13, leftIndent=30, firstLineIndent=-10)

    # Code
    add("Code", fontName="Courier", fontSize=8.8, textColor=C_CODE_FG,
        backColor=C_CODE_BG, spaceAfter=2, leading=13,
        leftIndent=8, rightIndent=8, spaceBefore=2)
    add("CodeComment", fontName="Courier", fontSize=8.8, textColor=HexColor("#94A3B8"),
        backColor=C_CODE_BG, spaceAfter=2, leading=13,
        leftIndent=8, rightIndent=8)
    add("CodeHL", fontName="Courier-Bold", fontSize=8.8, textColor=HexColor("#FCD34D"),
        backColor=C_CODE_BG, spaceAfter=2, leading=13, leftIndent=8, rightIndent=8)

    # Callouts
    add("Note",    fontName="Helvetica", fontSize=9.5, textColor=HexColor("#1D4ED8"),
        backColor=C_BLUE_BG,  spaceAfter=6, leading=14, leftIndent=10, rightIndent=10)
    add("Warning", fontName="Helvetica", fontSize=9.5, textColor=HexColor("#92400E"),
        backColor=C_YELLOW_BG, spaceAfter=6, leading=14, leftIndent=10, rightIndent=10)
    add("Success", fontName="Helvetica", fontSize=9.5, textColor=HexColor("#065F46"),
        backColor=C_GREEN_BG,  spaceAfter=6, leading=14, leftIndent=10, rightIndent=10)
    add("Danger",  fontName="Helvetica", fontSize=9.5, textColor=HexColor("#991B1B"),
        backColor=C_RED_BG,   spaceAfter=6, leading=14, leftIndent=10, rightIndent=10)

    add("Caption", fontName="Helvetica-Oblique", fontSize=8.5, textColor=C_MUTED,
        alignment=TA_CENTER, spaceAfter=8)
    add("PageNum", fontName="Helvetica", fontSize=9, textColor=C_MUTED, alignment=TA_CENTER)

    return base

S = build_styles()


# ── Helper Flowables ───────────────────────────────────────────────────────────
def hr(color=C_BORDER, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

def sp(h=6):
    return Spacer(1, h)

def h1(txt):  return Paragraph(txt, S["H1"])
def h2(txt):  return Paragraph(txt, S["H2"])
def h3(txt):  return Paragraph(txt, S["H3"])
def body(txt): return Paragraph(txt, S["Body"])
def bold(txt): return Paragraph(txt, S["BodyBold"])
def bullet(txt, sub=False):
    prefix = "• " if not sub else "◦ "
    style  = S["SubBullet"] if sub else S["Bullet"]
    return Paragraph(prefix + txt, style)
def note(txt):    return Paragraph("ℹ  " + txt, S["Note"])
def warn(txt):    return Paragraph("⚠  " + txt, S["Warning"])
def success(txt): return Paragraph("✓  " + txt, S["Success"])
def danger(txt):  return Paragraph("✗  " + txt, S["Danger"])
def caption(txt): return Paragraph(txt, S["Caption"])


class ColorBox(Flowable):
    """Solid-color banner used for the cover."""
    def __init__(self, w, h, color):
        super().__init__()
        self.w, self.h, self.color = w, h, color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)
    def wrap(self, *_): return self.w, self.h


def code_block(lines):
    """Return a list of Paragraph flowables that look like a code block."""
    items = []
    for raw in lines:
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)
        txt = "&nbsp;" * (indent * 2) + stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if stripped.startswith("#") or stripped.startswith("//"):
            items.append(Paragraph(txt, S["CodeComment"]))
        elif stripped.startswith("# HL:"):
            items.append(Paragraph(txt[5:], S["CodeHL"]))
        else:
            items.append(Paragraph(txt, S["Code"]))
    return items


def section_banner(title, subtitle=""):
    """Indigo banner for major section headings."""
    data = [[Paragraph(f'<font color="white"><b>{title}</b></font>', ParagraphStyle(
                "BannerTitle", fontName="Helvetica-Bold", fontSize=15, textColor=C_WHITE,
                leading=20)),
             Paragraph(f'<font color="#A5B4FC">{subtitle}</font>', ParagraphStyle(
                "BannerSub", fontName="Helvetica", fontSize=9, textColor=HexColor("#A5B4FC"),
                leading=13))]]
    t = Table(data, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), C_ACCENT),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0), (-1,-1), 12),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[C_ACCENT]),
    ]))
    return [sp(10), t, sp(6)]


def info_table(headers, rows, col_widths=None):
    data = [[Paragraph(f"<b>{h}</b>", ParagraphStyle(
                "TH", fontName="Helvetica-Bold", fontSize=9, textColor=C_WHITE,
                leading=12)) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), ParagraphStyle(
                "TD", fontName="Helvetica", fontSize=9, textColor=C_TEXT,
                leading=13)) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  C_BG_DARK),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C_WHITE, C_LIGHT_BG]),
        ("GRID",         (0,0), (-1,-1), 0.4, C_BORDER),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]))
    return t


def two_col(left_items, right_items, widths=(3.2*inch, 3.2*inch)):
    """Render two lists of flowables side-by-side."""
    def pack(items):
        return [i for i in items]
    data = [[pack(left_items), pack(right_items)]]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1),4),
        ("RIGHTPADDING", (0,0),(-1,-1),4),
        ("TOPPADDING",   (0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    return t


# ── Page template (header / footer) ───────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    # top rule
    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(0.6*inch, h-0.5*inch, w-0.6*inch, h-0.5*inch)
    # header text
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(C_ACCENT)
    canvas.drawString(0.6*inch, h-0.42*inch, "Monotonic Stack — Zero to Hero")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_MUTED)
    canvas.drawRightString(w-0.6*inch, h-0.42*inch, "Senior DSA Guide")
    # footer
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(C_BORDER)
    canvas.line(0.6*inch, 0.5*inch, w-0.6*inch, 0.5*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_MUTED)
    canvas.drawCentredString(w/2, 0.33*inch, f"Page {doc.page}")
    canvas.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
#  DOCUMENT BUILD
# ══════════════════════════════════════════════════════════════════════════════
def build():
    out = "/mnt/user-data/outputs/Monotonic_Stack_Zero_to_Hero.pdf"
    doc = SimpleDocTemplate(
        out,
        pagesize=letter,
        leftMargin=0.65*inch, rightMargin=0.65*inch,
        topMargin=0.8*inch,   bottomMargin=0.7*inch,
        title="Monotonic Stack — Zero to Hero",
        author="Senior DSA Instructor",
    )

    story = []
    W = letter[0] - 1.3*inch   # usable width

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(ColorBox(W, 2.8*inch, C_BG_DARK))
    story.append(sp(-2.5*inch))
    story.append(Paragraph("MONOTONIC STACK", S["CoverTitle"]))
    story.append(Paragraph("Zero  ▸  Hero", S["CoverSub"]))
    story.append(sp(0.15*inch))
    story.append(Paragraph("A Comprehensive DSA Tutorial Guide", S["CoverTag"]))
    story.append(sp(2.0*inch))

    # tag pills
    tags = ["Core Philosophy", "Element Life-Cycle", "Linear-Time Proof",
            "Range Problems", "Circular Arrays", "Edge Cases"]
    pill_data = [[Paragraph(f'<font color="white"><b>  {t}  </b></font>',
                            ParagraphStyle("pill", fontName="Helvetica-Bold", fontSize=8,
                                           textColor=C_WHITE, alignment=TA_CENTER)) for t in tags]]
    pill_t = Table([pill_data[0]], colWidths=[W/6]*6)
    pill_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), C_ACCENT),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),[3,3,3,3]),
        ("GRID",         (0,0),(-1,-1), 0.5, C_WHITE),
    ]))
    story.append(pill_t)
    story.append(sp(12))
    story.append(hr(C_ACCENT, 1.5))
    story.append(body(
        "Covers: Monotonic Increasing & Decreasing Stacks • Amortized O(n) Proof • "
        "Element Life-Cycle Template • Histogram / Rain-Water Patterns • Circular Arrays • "
        "Dual-Stack Techniques • Strictly vs Non-Strictly Monotonic • Edge-Case Checklist"
    ))

    story.append(PageBreak())

    # ── TABLE OF CONTENTS ─────────────────────────────────────────────────────
    story += section_banner("Table of Contents", "Eight chapters from definition to mastery")
    toc = [
        ("1", "The Core Philosophy",            "Core definition, discarding logic, O(n) proof"),
        ("2", "Monotonic Increasing Stack",      "Previous/Next smaller element patterns"),
        ("3", "Monotonic Decreasing Stack",      "Next greater element — the classic problem"),
        ("4", "The Element Life-Cycle Template", "Universal 3-step implementation template"),
        ("5", "Range-Based 'Area' Problems",     "Histogram, rain water, boundary concepts"),
        ("6", "Comparison & Decision Making",    "vs Sliding Window • strict vs non-strict"),
        ("7", "Advanced Variations",             "Circular arrays, dual monotonic stacks"),
        ("8", "Edge-Case Checklist",             "Empty input, sentinels, identical elements"),
    ]
    toc_data = [["Ch", "Title", "Topics Covered"]]
    for ch, title, topics in toc:
        toc_data.append([ch, title, topics])
    story.append(info_table(
        ["Ch", "Title", "Topics Covered"],
        [[r[0], r[1], r[2]] for r in toc],
        col_widths=[0.35*inch, 2.2*inch, W - 0.35*inch - 2.2*inch]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 1 — CORE PHILOSOPHY
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 1", "The Core Philosophy")

    story.append(h1("1.1  What Is a Monotonic Stack?"))
    story.append(body(
        "A <b>Monotonic Stack</b> is a standard stack data structure augmented with one "
        "invariant: elements stored in the stack are always maintained in a "
        "<b>sorted order</b> — either strictly increasing or strictly decreasing from "
        "bottom to top. This invariant is enforced every time a new element is pushed: "
        "any element that violates the order is <i>popped</i> first."
    ))
    story.append(sp(4))

    variants = [
        ["Variant", "Stack order (bottom → top)", "Invariant rule on push", "Primary use"],
        ["Increasing", "Small … Large", "Pop while top ≥ current", "Next/Prev Smaller"],
        ["Decreasing", "Large … Small", "Pop while top ≤ current", "Next/Prev Greater"],
    ]
    story.append(info_table(variants[0], variants[1:],
        col_widths=[1.3*inch, 1.9*inch, 1.9*inch, W-5.1*inch]))
    story.append(caption("Table 1.1 — Monotonic Stack variants at a glance"))
    story.append(sp(4))

    story.append(note(
        "Think of a monotonic stack as a VIP bouncer: every new guest (element) that "
        "arrives causes shorter/taller guests to leave so the line stays sorted."
    ))

    story.append(h2("1.2  Visualising the Invariant"))
    story.append(body(
        "Consider the array <b>[3, 1, 4, 1, 5, 9, 2, 6]</b>. "
        "Trace through building a <b>Monotonic Increasing</b> stack:"
    ))
    story += code_block([
        "Array:  [3, 1, 4, 1, 5, 9, 2, 6]",
        "",
        "Step 1  push 3     →  stack: [3]",
        "Step 2  1 < 3,  pop 3   →  stack: [1]      # 3 is discarded",
        "Step 3  4 > 1,  push 4  →  stack: [1, 4]",
        "Step 4  1 < 4,  pop 4   →  stack: [1]",
        "        1 == 1, pop 1   →  stack: []",
        "        push 1          →  stack: [1]",
        "Step 5  5 > 1,  push 5  →  stack: [1, 5]",
        "Step 6  9 > 5,  push 9  →  stack: [1, 5, 9]",
        "Step 7  2 < 9,  pop 9   →  stack: [1, 5]",
        "        2 < 5,  pop 5   →  stack: [1]",
        "        2 > 1,  push 2  →  stack: [1, 2]",
        "Step 8  6 > 2,  push 6  →  stack: [1, 2, 6]",
    ])
    story.append(caption("Trace 1.1 — Building a Monotonic Increasing Stack"))

    story.append(h1("1.3  The Discarding Logic — Why Is It Safe?"))
    story.append(body(
        "When we pop element <b>A</b> because incoming element <b>B</b> is smaller (for an "
        "increasing stack), we are implicitly recording: <i>\"B is the first element to the "
        "right that is smaller than A.\"</i>  A can never be the answer to any future query "
        "about 'nearest smaller' for elements processed after B. Its useful information has "
        "been captured at the moment of popping — so discarding it is correct and permanent."
    ))
    story.append(sp(4))
    story.append(warn(
        "Each pop is not a loss — it is a <b>computation</b>. "
        "The act of popping encodes the relationship between the popped element and the "
        "element that triggered the pop (the current element)."
    ))

    story.append(h1("1.4  Amortised O(n) Complexity Proof"))
    story.append(body(
        "At first glance, the nested <b>while</b> loop inside the outer <b>for</b> loop "
        "looks like O(n²). The amortised argument shows it is O(n):"
    ))
    story.append(bullet("<b>Each element is pushed exactly once.</b>"))
    story.append(bullet("<b>Each element is popped at most once.</b>"))
    story.append(bullet(
        "Therefore the total number of push + pop operations across the entire algorithm "
        "is bounded by <b>2n</b>."
    ))
    story.append(bullet(
        "The while loop, <i>summed across all iterations of the outer for loop</i>, "
        "performs at most <b>n</b> total pops, not n per iteration."
    ))
    story.append(sp(4))
    story.append(success(
        "Amortised Complexity = O(n) pushes + O(n) pops = O(n) total.  "
        "Space complexity = O(n) for the stack in the worst case (strictly increasing input)."
    ))
    story += code_block([
        "# Amortised complexity demo — count operations",
        "def count_ops(arr):",
        "    stack, push_count, pop_count = [], 0, 0",
        "    for x in arr:",
        "        while stack and stack[-1] >= x:",
        "            stack.pop()",
        "            pop_count += 1",
        "        stack.append(x)",
        "        push_count += 1",
        "    # Invariant: push_count <= n, pop_count <= n",
        "    return push_count, pop_count   # Both are always <= len(arr)",
    ])
    story.append(caption("Snippet 1.1 — Each element pushed once, popped at most once"))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 2 — INCREASING STACK
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 2", "Monotonic Increasing Stack")

    story.append(h1("2.1  The Invariant"))
    story.append(body(
        "A <b>Monotonic Increasing Stack</b> stores elements such that, reading from "
        "bottom to top, values are non-decreasing. On each push, we first pop every "
        "element that is <b>greater than or equal to</b> the current value (strict) "
        "or just <b>greater than</b> (non-strict / allowing duplicates)."
    ))
    story.append(sp(4))

    story.append(two_col(
        [h3("Strict Increasing (no duplicates)"),
         *code_block([
             "while stack and stack[-1] >= current:",
             "    stack.pop()",
             "stack.append(current)",
         ])],
        [h3("Non-Strict (duplicates allowed)"),
         *code_block([
             "while stack and stack[-1] > current:",
             "    stack.pop()",
             "stack.append(current)",
         ])],
        widths=[W/2 - 4, W/2 - 4]
    ))
    story.append(sp(6))

    story.append(h1("2.2  Key Use Case: Previous Smaller Element (PSE)"))
    story.append(body(
        "For each element in the array, find the index of the nearest element to its "
        "<b>left</b> that is strictly smaller. If none exists, record <b>-1</b>."
    ))
    story += code_block([
        "def previous_smaller_element(arr):",
        "    n = len(arr)",
        "    result = [-1] * n     # default: no smaller element on the left",
        "    stack  = []           # monotonic increasing stack (stores indices)",
        "",
        "    for i in range(n):",
        "        # Pop elements that are >= current (they can't be PSE for arr[i])",
        "        while stack and arr[stack[-1]] >= arr[i]:",
        "            stack.pop()",
        "",
        "        # Whatever remains on top is the nearest smaller to the left",
        "        if stack:",
        "            result[i] = stack[-1]   # index of previous smaller",
        "",
        "        stack.append(i)             # push current index",
        "",
        "    return result",
        "",
        "# Example",
        "# arr    = [4, 5, 2, 10, 8]",
        "# result = [-1, 0, -1, 2, 2]",
        "# arr[2]=2 is the PSE for indices 3 and 4",
    ])
    story.append(caption("Snippet 2.1 — Previous Smaller Element using a Monotonic Increasing Stack"))

    story.append(h1("2.3  Key Use Case: Next Smaller Element (NSE)"))
    story.append(body(
        "Process left-to-right. When we <b>pop</b> an element (because the current "
        "element is smaller), the current element is the NSE for the popped element."
    ))
    story += code_block([
        "def next_smaller_element(arr):",
        "    n      = len(arr)",
        "    result = [-1] * n     # default: no smaller element to the right",
        "    stack  = []           # stores indices",
        "",
        "    for i in range(n):",
        "        # Current element is smaller → it IS the NSE for stack top",
        "        while stack and arr[stack[-1]] > arr[i]:",
        "            idx = stack.pop()",
        "            result[idx] = i   # i is the next smaller index for idx",
        "",
        "        stack.append(i)",
        "",
        "    # Elements still in stack have no NSE (result stays -1)",
        "    return result",
        "",
        "# Example",
        "# arr    = [4, 5, 2, 10, 8]",
        "# result = [2, 2, -1, 4, -1]",
        "# index 2 (value 2) is NSE for indices 0 and 1",
    ])
    story.append(caption("Snippet 2.2 — Next Smaller Element: pop event records the answer"))
    story.append(note(
        "Storing <b>indices</b> instead of values is almost always preferred. "
        "You can always retrieve the value with arr[idx], but the index "
        "gives you positional information (distance, span, etc.) for free."
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 3 — DECREASING STACK
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 3", "Monotonic Decreasing Stack")

    story.append(h1("3.1  The Invariant"))
    story.append(body(
        "A <b>Monotonic Decreasing Stack</b> stores elements from bottom (largest) "
        "to top (smallest). On each push, pop every element that is "
        "<b>smaller than or equal to</b> the current value."
    ))
    story += code_block([
        "# Decreasing stack maintenance",
        "while stack and stack[-1] <= current:",
        "    stack.pop()",
        "stack.append(current)",
    ])

    story.append(h1("3.2  The Classic Problem: Next Greater Element (NGE)"))
    story.append(body(
        "For each position, find the first element to the <b>right</b> that is strictly "
        "greater. This is the canonical interview problem solved elegantly with a "
        "Monotonic Decreasing Stack."
    ))
    story += code_block([
        "def next_greater_element(arr):",
        "    n      = len(arr)",
        "    result = [-1] * n     # -1 means no greater element exists to the right",
        "    stack  = []           # monotonic decreasing stack (indices)",
        "",
        "    for i in range(n):",
        "        # arr[i] is greater than stack top → it IS the NGE for that top",
        "        while stack and arr[stack[-1]] < arr[i]:",
        "            idx       = stack.pop()",
        "            result[idx] = arr[i]   # or store index i if needed",
        "",
        "        stack.append(i)",
        "",
        "    # Remaining elements in stack have no NGE → result[idx] stays -1",
        "    return result",
        "",
        "# Example",
        "# arr    = [2, 1, 5, 3, 4]",
        "# result = [5, 5, -1, 4, -1]",
    ])
    story.append(caption("Snippet 3.1 — Next Greater Element: the canonical Monotonic Decreasing Stack problem"))
    story.append(sp(6))

    # Dry-run trace table
    story.append(h2("Dry-Run Trace — arr = [2, 1, 5, 3, 4]"))
    trace_data = [
        ["i", "arr[i]", "Action", "Stack (indices)", "result"],
        ["0", "2",  "Push 0",            "[0]",     "[-1,-1,-1,-1,-1]"],
        ["1", "1",  "Push 1 (1<2)",       "[0,1]",   "[-1,-1,-1,-1,-1]"],
        ["2", "5",  "Pop 1→NGE=5, Pop 0→NGE=5, Push 2", "[2]", "[5,5,-1,-1,-1]"],
        ["3", "3",  "Push 3 (3<5)",       "[2,3]",   "[5,5,-1,-1,-1]"],
        ["4", "4",  "Pop 3→NGE=4, Push 4","[2,4]",   "[5,5,-1,4,-1]"],
        ["—", "—",  "End: idx 2,4 remain → -1","[ ]","[5,5,-1,4,-1]"],
    ]
    story.append(info_table(trace_data[0], trace_data[1:],
        col_widths=[0.3*inch, 0.5*inch, 2.4*inch, 1.5*inch, W-4.7*inch]))
    story.append(caption("Table 3.1 — Step-by-step NGE trace"))

    story.append(h1("3.3  Previous Greater Element (PGE)"))
    story.append(body(
        "Mirror of NGE: process left-to-right, but instead of recording during pop, "
        "record the stack top (if it exists) just before pushing — that top is the PGE."
    ))
    story += code_block([
        "def previous_greater_element(arr):",
        "    n      = len(arr)",
        "    result = [-1] * n",
        "    stack  = []           # decreasing stack",
        "",
        "    for i in range(n):",
        "        while stack and arr[stack[-1]] <= arr[i]:",
        "            stack.pop()",
        "",
        "        # Stack top (if any) is the first greater element to the LEFT",
        "        if stack:",
        "            result[i] = stack[-1]",
        "",
        "        stack.append(i)",
        "",
        "    return result",
    ])
    story.append(caption("Snippet 3.2 — Previous Greater Element"))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 4 — ELEMENT LIFE-CYCLE TEMPLATE
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 4", "The Element Life-Cycle Template")

    story.append(h1("4.1  The Universal Three-Step Template"))
    story.append(body(
        "Every Monotonic Stack problem, regardless of direction or type, follows the "
        "same three-step life-cycle for each element. Master this template and you can "
        "adapt it to any variant in under two minutes."
    ))
    story.append(sp(4))

    steps = [
        ["Step", "Name", "Action", "What it computes"],
        ["1", "POP & PROCESS",
         "while stack not empty AND current breaks monotonic property → pop",
         "The popped element's NEAREST NEIGHBOR in the direction of traversal "
         "is the current element that triggered the pop."],
        ["2", "READ NEIGHBOR",
         "After the while loop, check if stack is non-empty",
         "stack.top() is the NEAREST NEIGHBOR in the opposite direction "
         "(the one that survived)."],
        ["3", "PUSH",
         "Append current element (usually its index) to the stack",
         "The element becomes a candidate for future comparisons."],
    ]
    story.append(info_table(steps[0], steps[1:],
        col_widths=[0.4*inch, 1.1*inch, 2.1*inch, W-3.6*inch]))
    story.append(caption("Table 4.1 — The three-step Element Life-Cycle"))
    story.append(sp(6))

    story.append(h1("4.2  Annotated Generic Template"))
    story += code_block([
        "def monotonic_stack_template(arr, problem_type='NGE'):",
        "    \"\"\"",
        "    Generic template — adapt condition and result-recording per problem.",
        "    problem_type: 'NGE' | 'NSE' | 'PGE' | 'PSE'",
        "    \"\"\"",
        "    n      = len(arr)",
        "    result = [-1] * n",
        "    stack  = []   # stores indices",
        "",
        "    for i in range(n):",
        "",
        "        # ── STEP 1: POP & PROCESS ──────────────────────────────────",
        "        # Adjust the condition to match the monotonic property you need.",
        "        # For NGE (decreasing stack): pop while top < current",
        "        # For NSE (increasing stack): pop while top > current",
        "        while stack and breaks_property(arr, stack[-1], i, problem_type):",
        "            popped      = stack.pop()",
        "            # >>> Record the answer for the popped element <<<",
        "            result[popped] = i   # or arr[i] depending on what is asked",
        "",
        "        # ── STEP 2: READ NEAREST NEIGHBOR ──────────────────────────",
        "        # The current stack top is the nearest neighbor in the OPPOSITE",
        "        # direction — use this for PSE / PGE style problems.",
        "        if stack:",
        "            pass   # result[i] = stack[-1]  (uncomment if needed)",
        "",
        "        # ── STEP 3: PUSH CURRENT ────────────────────────────────────",
        "        stack.append(i)",
        "",
        "    return result",
        "",
        "def breaks_property(arr, top_idx, cur_idx, ptype):",
        "    \"\"\"Returns True if arr[top_idx] violates the invariant given arr[cur_idx].\"\"\"",
        "    if ptype in ('NGE', 'PGE'):",
        "        return arr[top_idx] < arr[cur_idx]   # decreasing stack",
        "    else:                                    # NSE, PSE",
        "        return arr[top_idx] > arr[cur_idx]   # increasing stack",
    ])
    story.append(caption("Snippet 4.1 — Fully annotated generic template with life-cycle comments"))

    story.append(h1("4.3  Decision Map"))
    story.append(body(
        "Use this map to instantly select the correct template configuration:"
    ))
    dm = [
        ["Problem", "Stack type", "Pop condition", "Answer recorded at"],
        ["Next Greater Element",   "Decreasing", "top < current", "Pop time (for popped)"],
        ["Previous Greater Element","Decreasing","top < current", "Push time (check top)"],
        ["Next Smaller Element",   "Increasing", "top > current", "Pop time (for popped)"],
        ["Previous Smaller Element","Increasing","top > current", "Push time (check top)"],
    ]
    story.append(info_table(dm[0], dm[1:],
        col_widths=[2.0*inch, 1.2*inch, 1.4*inch, W-4.6*inch]))
    story.append(caption("Table 4.2 — Decision map for all four nearest-neighbor problems"))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 5 — RANGE / AREA PROBLEMS
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 5", "Range-Based 'Area' Problems")

    story.append(h1("5.1  The Left-Boundary / Right-Boundary Concept"))
    story.append(body(
        "Many 2-D range problems reduce to: <i>\"For each bar/element, how far left and "
        "right can we extend before hitting something taller/shorter?\"</i>  "
        "The Monotonic Stack provides both boundaries in a single O(n) pass."
    ))
    story.append(bullet(
        "<b>Left boundary</b> (lb[i]) = index of the nearest element to the LEFT that "
        "would invalidate the extension. Found when the element is <i>pushed</i>: "
        "lb[i] = stack.top() at push time."
    ))
    story.append(bullet(
        "<b>Right boundary</b> (rb[i]) = index of the nearest element to the RIGHT that "
        "invalidates. Found when the element is <i>popped</i>: rb[popped] = current index."
    ))
    story.append(bullet(
        "<b>Span / width</b> = rb[i] - lb[i] - 1 gives the number of positions the "
        "element 'owns' as the minimum/maximum in that range."
    ))
    story.append(sp(4))

    story.append(h1("5.2  Largest Rectangle in Histogram"))
    story.append(body(
        "Given an array of bar heights, find the area of the largest rectangle that can "
        "be formed using consecutive bars. Each bar's contribution = "
        "<b>height[i] × width</b>, where width = (next smaller to right) − (prev smaller to left) − 1."
    ))
    story += code_block([
        "def largest_rectangle_histogram(heights):",
        "    n      = len(heights)",
        "    stack  = []          # increasing stack (stores indices)",
        "    max_area = 0",
        "",
        "    # Append sentinel 0 so every element is eventually popped",
        "    heights = heights + [0]",
        "",
        "    for i in range(n + 1):",
        "        while stack and heights[stack[-1]] >= heights[i]:",
        "            h = heights[stack.pop()]   # height of rectangle",
        "",
        "            # Width: from previous smaller (stack top) to current smaller (i)",
        "            if stack:",
        "                w = i - stack[-1] - 1  # left boundary is stack top",
        "            else:",
        "                w = i                  # no left boundary → extends to index 0",
        "",
        "            max_area = max(max_area, h * w)",
        "",
        "        stack.append(i)",
        "",
        "    return max_area",
        "",
        "# Example: heights = [2, 1, 5, 6, 2, 3]  →  max_area = 10",
        "# The rectangle of height 5 spans indices 2-3 (width=2), area = 10",
    ])
    story.append(caption("Snippet 5.1 — Largest Rectangle in Histogram with sentinel trick"))
    story.append(sp(4))

    story.append(h1("5.3  Trapping Rain Water"))
    story.append(body(
        "For each column, the water it can hold = "
        "<b>min(max_left, max_right) − height[i]</b>. "
        "A Monotonic Decreasing Stack offers an elegant online solution: when a taller "
        "bar is found, the popped bar forms the 'valley' floor and the boundaries are "
        "readily available."
    ))
    story += code_block([
        "def trap_rain_water(height):",
        "    stack    = []    # decreasing stack (stores indices)",
        "    water    = 0",
        "",
        "    for i in range(len(height)):",
        "        while stack and height[stack[-1]] < height[i]:",
        "            floor_idx = stack.pop()       # valley bottom",
        "            if not stack:",
        "                break                     # no left wall → no water",
        "",
        "            left_wall  = stack[-1]",
        "            right_wall = i",
        "            bounded_h  = min(height[left_wall], height[right_wall])",
        "            width      = right_wall - left_wall - 1",
        "            water     += (bounded_h - height[floor_idx]) * width",
        "",
        "        stack.append(i)",
        "",
        "    return water",
        "",
        "# Example: height = [0,1,0,2,1,0,1,3,2,1,2,1]  →  water = 6",
    ])
    story.append(caption("Snippet 5.2 — Trapping Rain Water with Monotonic Decreasing Stack"))
    story.append(sp(4))
    story.append(success(
        "Both problems share the same structural insight: the stack maintains potential "
        "'candidate' bars, and a pop event always computes a concrete area or volume "
        "contribution in O(1) per pop."
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 6 — COMPARISON & DECISION MAKING
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 6", "Comparison & Decision Making")

    story.append(h1("6.1  Monotonic Stack vs. Sliding Window"))
    story.append(body(
        "Both are O(n) techniques for range queries, but they answer different "
        "questions. Understanding the distinction prevents costly mis-applications."
    ))
    vs_data = [
        ["Dimension", "Monotonic Stack", "Sliding Window"],
        ["Core question",
         "What is the nearest element satisfying a condition?",
         "What is the aggregate (max/min/sum) over a fixed-size window?"],
        ["Window size",
         "Variable — determined by the data itself",
         "Fixed k, or bounded by a constraint"],
        ["Direction",
         "Can look both left and right in a single pass",
         "Typically one direction (left → right)"],
        ["What it stores",
         "Candidate elements maintaining monotonic order",
         "Elements within the current window"],
        ["Eviction rule",
         "Violates monotonic property (value-based)",
         "Falls outside the window (index-based)"],
        ["Typical problems",
         "NGE, NSE, Histogram, Rain Water",
         "Max in window, Longest subarray with constraint"],
        ["Can it handle NGE?", "Yes — natively", "No — not designed for it"],
        ["Can it do sliding max?",
         "Yes — use a deque variant (monotonic deque)",
         "Yes — with deque"],
        ["Space complexity",
         "O(n) worst case",
         "O(k) where k = window size"],
    ]
    story.append(info_table(vs_data[0], vs_data[1:],
        col_widths=[1.5*inch, 2.5*inch, W-4.0*inch]))
    story.append(caption("Table 6.1 — Monotonic Stack vs. Sliding Window"))
    story.append(sp(6))

    story.append(h1("6.2  Strictly vs. Non-Strictly Monotonic"))
    story.append(body(
        "Handling <b>duplicate values</b> is a common source of bugs. "
        "The difference between strict and non-strict monotonicity determines "
        "which duplicate 'wins' as the answer."
    ))
    dup_data = [
        ["Variant", "Pop condition (increasing)", "Effect on duplicates", "Use when…"],
        ["Strict Increasing",     "top >= current", "Only one of equal elements stays",
         "Answer must be strictly smaller (strict inequality required)"],
        ["Non-Strict Increasing", "top > current",  "All equal elements stay",
         "Duplicates should share the same answer (≤ comparison)"],
    ]
    story.append(info_table(dup_data[0], dup_data[1:],
        col_widths=[1.4*inch, 1.5*inch, 1.8*inch, W-4.7*inch]))
    story.append(caption("Table 6.2 — Strict vs non-strict handling"))
    story.append(sp(4))
    story += code_block([
        "# Example: arr = [3, 3, 3]",
        "",
        "# Strict Increasing Stack (pop when top >= current)",
        "# Each 3 pops the previous 3 → only last 3 survives",
        "# PSE of every index = -1 (nothing strictly smaller to the left)",
        "",
        "# Non-Strict Increasing Stack (pop when top > current)",
        "# Equal elements coexist → stack = [3, 3, 3]",
        "# PSE of index 1 = 0 (arr[0] == arr[1], but not strictly smaller — handle carefully)",
    ])
    story.append(caption("Snippet 6.1 — Duplicate value behaviour comparison"))
    story.append(warn(
        "Always re-read the problem statement for 'strictly greater/smaller' vs "
        "'greater/smaller or equal' — one word changes the pop condition and the results."
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 7 — ADVANCED VARIATIONS
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 7", "Advanced Variations")

    story.append(h1("7.1  Circular Arrays — The Double-Pass Trick"))
    story.append(body(
        "For circular arrays, every element may have a 'next greater' that wraps around. "
        "The classic trick: <b>simulate two full passes</b> by iterating from "
        "<b>0 to 2n − 1</b> and using <b>index mod n</b> to access elements. "
        "Only push during the first pass (i < n) to avoid double-counting."
    ))
    story += code_block([
        "def next_greater_circular(arr):",
        "    n      = len(arr)",
        "    result = [-1] * n",
        "    stack  = []           # decreasing stack (stores real indices 0..n-1)",
        "",
        "    for i in range(2 * n):          # double pass",
        "        real_i = i % n",
        "",
        "        # Pop and record NGE as usual",
        "        while stack and arr[stack[-1]] < arr[real_i]:",
        "            idx         = stack.pop()",
        "            result[idx] = arr[real_i]",
        "",
        "        # Only push during the first full pass to avoid re-visiting",
        "        if i < n:",
        "            stack.append(real_i)",
        "",
        "    # Elements still in stack have no NGE in the circular array → -1",
        "    return result",
        "",
        "# Example",
        "# arr    = [1, 2, 1]",
        "# result = [2, -1, 2]    (index 2 wraps around to find 2 at index 1)",
    ])
    story.append(caption("Snippet 7.1 — Circular NGE using index mod n with a single stack"))
    story.append(sp(4))
    story.append(note(
        "The double-pass trick works because: any element that still has no NGE after "
        "seeing every element in the array twice genuinely has no NGE in the circle."
    ))

    story.append(h1("7.2  Dual Monotonic Stacks — Computing Both Boundaries Simultaneously"))
    story.append(body(
        "Some problems require, for each element, both its "
        "<b>previous greater</b> and <b>next greater</b> simultaneously "
        "(e.g., 'sum of subarray minimums', 'maximum sum with bounded contribution'). "
        "Two approaches:"
    ))
    story.append(bullet(
        "<b>Two separate passes:</b> first pass (left → right) builds PSE/PGE; "
        "second pass (right → left or another left → right) builds NSE/NGE."
    ))
    story.append(bullet(
        "<b>Single pass with index recording:</b> at pop time, record both "
        "the left boundary (new stack top after pop) and the right boundary "
        "(current element triggering pop)."
    ))
    story.append(sp(4))
    story += code_block([
        "def both_boundaries_single_pass(arr):",
        "    \"\"\"",
        "    For each index, find (prev_smaller_idx, next_smaller_idx) in one pass.",
        "    Uses an increasing stack; at pop time both boundaries are known.",
        "    \"\"\"",
        "    n    = len(arr)",
        "    left = [-1] * n   # index of previous smaller",
        "    right= [ n] * n   # index of next smaller (n = 'no boundary')",
        "    stack = []",
        "",
        "    for i in range(n):",
        "        while stack and arr[stack[-1]] > arr[i]:",
        "            popped   = stack.pop()",
        "            right[popped] = i              # RIGHT boundary recorded at pop",
        "",
        "        # LEFT boundary: whatever is now on top of the stack",
        "        left[i] = stack[-1] if stack else -1",
        "",
        "        stack.append(i)",
        "",
        "    return left, right",
        "",
        "# Span owned by element i (as the minimum) = right[i] - left[i] - 1",
        "# Contribution to 'sum of subarray mins' = arr[i] * (i-left[i]) * (right[i]-i)",
    ])
    story.append(caption("Snippet 7.2 — Single-pass dual-boundary collection"))
    story.append(sp(4))

    story.append(h2("Deduplication for 'Sum of Subarray Minimums'"))
    story.append(body(
        "When duplicates exist, the 'sum of subarray minimums' problem can double-count "
        "contributions. The fix: use <b>strict inequality on one side</b>:"
    ))
    story += code_block([
        "# To avoid double-counting duplicates:",
        "# Left side:  pop while arr[top] >= arr[i]   (strict — pops duplicates left)",
        "# Right side: pop while arr[top] >  arr[i]   (non-strict — keeps right duplicate)",
        "#",
        "# This asymmetric treatment ensures each duplicate subarray",
        "# is counted exactly once.",
    ])
    story.append(caption("Snippet 7.3 — Asymmetric duplicate handling"))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════════
    # CHAPTER 8 — EDGE CASES CHECKLIST
    # ════════════════════════════════════════════════════════════════════════════
    story += section_banner("Chapter 8", "The Edge-Case Checklist")

    story.append(h1("8.1  The Pre-Flight Checklist"))
    story.append(body(
        "Before submitting any Monotonic Stack solution, run through these eight checks. "
        "Each has caused wrong answers in competitive programming and technical interviews."
    ))

    checks = [
        ("Empty Input Array",
         "if not arr: return []",
         "Always guard with an early return. An empty array is valid input."),
        ("Single-Element Array",
         "len(arr) == 1 → result is trivially [-1] or [arr[0]]",
         "No previous or next element exists; stack will push once and loop ends."),
        ("All Identical Elements",
         "[5, 5, 5, 5] — strict stack pops all; non-strict keeps all",
         "Re-check whether your pop condition handles equality correctly."),
        ("Strictly Increasing Input",
         "[1, 2, 3, 4, 5] — increasing stack never pops during build",
         "Worst-case O(n) space. Stack will be filled after the loop. Always drain."),
        ("Strictly Decreasing Input",
         "[5, 4, 3, 2, 1] — decreasing stack never pops during build",
         "Same stack-full scenario in the opposite direction."),
        ("Sentinel Value (∞ / −1) to Drain the Stack",
         "Append float('inf') or -1 to the array to force all remaining pops",
         "Prevents writing a separate post-loop drain. Clean and idiomatic."),
        ("Index vs. Value in Stack",
         "Storing values loses position info; store indices and derive values",
         "Use arr[stack[-1]] to get value; use stack[-1] for position math."),
        ("Overflow in Area Calculations",
         "h * w can overflow in 32-bit languages for large inputs",
         "Use 64-bit integers or language-specific big integers."),
    ]

    for num, (title, code_ex, explanation) in enumerate(checks, 1):
        ck_data = [[
            Paragraph(f"<b>{num}. {title}</b>", ParagraphStyle(
                "CKTitle", fontName="Helvetica-Bold", fontSize=10, textColor=C_WHITE,
                leading=14)),
            Paragraph(explanation, ParagraphStyle(
                "CKExp", fontName="Helvetica", fontSize=9, textColor=C_TEXT, leading=13)),
        ]]
        ck_code = [[
            Paragraph("", S["Body"]),
            Paragraph(f'<font face="Courier" size="8.5" color="#059669">{code_ex}</font>',
                      ParagraphStyle("CKCode", fontName="Courier", fontSize=8.5,
                                     textColor=HexColor("#059669"), leading=12)),
        ]]
        bg = C_ACCENT if num % 2 == 1 else C_BG_DARK
        t = Table(ck_data, colWidths=[2.4*inch, W-2.4*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(0,0), bg),
            ("BACKGROUND",   (1,0),(1,0), C_LIGHT_BG),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
            ("RIGHTPADDING", (0,0),(-1,-1), 8),
            ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
        ]))
        story.append(t)
        story.append(sp(2))

    story.append(sp(8))
    story.append(h1("8.2  Sentinel Value Pattern"))
    story += code_block([
        "# Pattern A: Append sentinel to the array",
        "def nse_with_sentinel(arr):",
        "    result = [-1] * len(arr)",
        "    stack  = []",
        "    for i, val in enumerate(arr + [float('-inf')]):  # sentinel drains stack",
        "        while stack and arr[stack[-1]] > val:",
        "            result[stack.pop()] = i",
        "        if i < len(arr):",
        "            stack.append(i)",
        "    return result",
        "",
        "# Pattern B: Sentinel index (-1 or n) as a virtual boundary bar",
        "def histogram_with_sentinel(heights):",
        "    heights = [0] + heights + [0]   # sentinels on both sides",
        "    stack   = [0]                   # push left sentinel index",
        "    max_area = 0",
        "    for i in range(1, len(heights)):",
        "        while heights[stack[-1]] > heights[i]:",
        "            h = heights[stack.pop()]",
        "            w = i - stack[-1] - 1",
        "            max_area = max(max_area, h * w)",
        "        stack.append(i)",
        "    return max_area",
    ])
    story.append(caption("Snippet 8.1 — Two sentinel patterns for clean stack drainage"))

    story.append(sp(8))
    story.append(h1("8.3  Quick-Reference Summary"))
    summary = [
        ["Concept", "One-Line Summary"],
        ["Monotonic Increasing Stack", "Bottom-to-top: small→large. Pop when top ≥ current."],
        ["Monotonic Decreasing Stack", "Bottom-to-top: large→small. Pop when top ≤ current."],
        ["Why O(n)?", "Each element is pushed once and popped at most once → 2n ops total."],
        ["Pop = Computation", "When popped, current element IS the nearest neighbor for popped."],
        ["Push = Record",     "Stack top at push time IS the opposite nearest neighbor."],
        ["Store indices",     "Prefer arr[stack[-1]] over raw values for positional math."],
        ["Sentinel trick",    "Append ∞ or 0 to drain remaining elements without post-loop."],
        ["Circular array",    "Iterate 2n times with index % n; only push in first n iterations."],
        ["Dual boundaries",   "At pop time: left=new_stack_top, right=current. One pass."],
        ["Duplicate safety",  "Use asymmetric conditions: strict on one side, non-strict other."],
    ]
    story.append(info_table(summary[0], summary[1:],
        col_widths=[2.2*inch, W-2.2*inch]))
    story.append(caption("Table 8.1 — Master summary of all Monotonic Stack concepts"))

    story.append(sp(10))
    story.append(hr(C_ACCENT, 1.5))
    story.append(Paragraph(
        "End of Tutorial  ·  Monotonic Stack: Zero to Hero",
        ParagraphStyle("Footer", fontName="Helvetica-Oblique", fontSize=10,
                       textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=4)
    ))
    story.append(Paragraph(
        "Practise on: Next Greater Element II · Largest Rectangle in Histogram · "
        "Trapping Rain Water · Sum of Subarray Minimums · Buildings with an Ocean View",
        ParagraphStyle("Footer2", fontName="Helvetica", fontSize=8.5,
                       textColor=C_ACCENT, alignment=TA_CENTER)
    ))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written to {out}")


if __name__ == "__main__":
    build()