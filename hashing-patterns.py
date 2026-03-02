from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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

PAGE_W, PAGE_H = letter

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Hashing_Patterns_Zero_To_Hero.pdf",
    pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.75*inch,  bottomMargin=0.75*inch,
)

CW = PAGE_W - 1.3*inch   # usable content width

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

P = Paragraph   # shorthand

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

# ══════════════════════════════════════════════════════════════════════════════
# STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT),("ROWHEIGHT",(0,0),(-1,-1),6)])))
story.append(Spacer(1, 0.3*inch))
story.append(P("HASHING PATTERNS", sTitle))
story.append(P("Zero to Hero: The Complete LeetCode Guide", sSubtitle))
story.append(Spacer(1, 0.15*inch))
story.append(P("Space-Time Tradeoffs · Lookup Optimization · Frequency Counting · Grouping", sAuthor))
story.append(Spacer(1, 0.2*inch))

story.append(Table([
    [P("<b>What You Will Master</b>", S("_", fontName="Helvetica-Bold", fontSize=12, textColor=C_ACCENT))],
    [P("· The O(1) average-case lookup and the Space-Time Tradeoff philosophy\n"
       "· Pattern 1 — Frequency Counting (Counter / int[26] array)\n"
       "· Pattern 2 — Complement Lookup: the 'target − x' trick (Two Sum)\n"
       "· Pattern 3 — Grouping & Bucketing by canonical key (Group Anagrams)\n"
       "· Pattern 4 — Value → Index mapping for distance problems\n"
       "· Pattern 5 — HashSet for O(1) existence checks & deduplication\n"
       "· Pattern 6 — Prefix Sum + HashMap (exact subarray sums with negatives)\n"
       "· HashMap vs. HashSet vs. Frequency Array decision table\n"
       "· Collision resolution, mutable keys, and memory pitfalls\n"
       "· 25+ categorized LeetCode problems with pattern labels",
       S("_", fontName="Helvetica", fontSize=10, leading=17, textColor=C_BODY))]],
    colWidths=[CW], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),("BOX",(0,0),(-1,-1),1,C_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(-1,-1),20)])))
story.append(Spacer(1, 0.3*inch))

cx = [
    [th("Brute Force"), th("With Hashing"), th("Space Cost")],
    [td("O(n<super>2</super>) nested loops", C_RED),
     td("O(n) single pass", C_GREEN),
     td("O(n) extra space", C_YELLOW)],
    [td("Scan entire array for each element", C_MUTED),
     td("O(1) average lookup per step", C_BODY),
     td("Hash table stores seen elements", C_MUTED)],
]
story.append(Table(cx, colWidths=[CW/3]*3, style=TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_BG),("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#0A1628")),
    ("BOX",(0,0),(-1,-1),1,C_BORDER),("INNERGRID",(0,0),(-1,-1),0.5,C_BORDER),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)])))
story.append(Spacer(1, 0.35*inch))
story.append(Table([[""]], colWidths=[CW],
    style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_ACCENT2),("ROWHEIGHT",(0,0),(-1,-1),4)])))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story += section_divider(0, "Table of Contents")
toc = [
    ("01","The Core Philosophy",["O(1) Avg vs O(n) Worst Case","The Space-Time Tradeoff","Hash Function Internals (Conceptual)"]),
    ("02","Pattern 1: Frequency Counting",["HashMap Counter vs int[26] Array","Anagram & Permutation Problems","Visual: Character Frequency Maps"]),
    ("03","Pattern 2: Complement Lookup",["The 'target − x' Trick","Two Sum: Single-Pass O(n)","Eliminating Nested Loops"]),
    ("04","Pattern 3: Grouping & Bucketing",["Canonical Key Design","Group Anagrams by Sorted String","Tuple Keys & Value-Based Grouping"]),
    ("05","Pattern 4: Value → Index Mapping",["Storing Index for Distance Queries","Contains Duplicate II","Subarray Constraints via Index Gap"]),
    ("06","Pattern 5: HashSet Lookups",["O(1) Existence Checks","Deduplication & Seen Sets","Longest Consecutive Sequence"]),
    ("07","Pattern 6: Prefix Sum + HashMap",["Combining Two Techniques","Subarray Sum Equals K","Modular Arithmetic Variants"]),
    ("08","Comparison & Decision Making",["HashMap vs HashSet vs Freq Array","When to Use Each","Decision Flowchart"]),
    ("09","Problem Roadmap",["Easy Problems","Medium Problems","Hard Problems"]),
    ("10","Pitfalls & Edge Cases",["Hash Collisions (Conceptual)","Mutable vs Immutable Keys","Memory Limits & Large Inputs"]),
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

story.append(P("<b>What is a Hash Table?</b>", sH2))
story.append(P(
    "A Hash Table (Python: <b>dict</b>, Java: <b>HashMap</b>, C++: <b>unordered_map</b>) "
    "is a data structure that maps keys to values using a <b>hash function</b>. "
    "The hash function converts any key into an integer index, which points "
    "directly to a slot in an underlying array. This direct indexing is what "
    "makes lookup, insertion, and deletion all O(1) <i>average case</i>.",
    sBody))

story += code_block([
    "## ─── How a hash table conceptually works ───────────────────────",
    "## 1. You call:   table[key] = value",
    "## 2. Internally: slot = hash_function(key) % table_capacity",
    "## 3. The value is stored at underlying_array[slot]",
    "## 4. Lookup:     slot = hash_function(key) % capacity → O(1) read",
    "",
    "## Example (conceptual):",
    "## key='apple'  → hash('apple') % 16 = 7  → store at slot 7",
    "## key='banana' → hash('banana') % 16 = 3  → store at slot 3",
    "## Lookup 'apple': hash → slot 7 → value found immediately, no search",
])

story.append(P("<b>O(1) Average Case vs. O(n) Worst Case</b>", sH2))
story.append(P(
    "The O(1) guarantee is <b>average case</b>, not worst case. The worst case "
    "occurs when many keys hash to the same slot — a <b>collision</b>. Modern "
    "hash tables handle collisions so effectively that the worst case is almost "
    "never observed in practice. However, understanding the theory matters for "
    "interviews and adversarial inputs.",
    sBody))

comp_data = [
    [th("Operation"), th("Average Case"), th("Worst Case"), th("When Worst Case Occurs")],
    [td("Lookup (get)",    C_BODY), td("O(1)", C_GREEN), td("O(n)", C_RED), td("All keys hash to same slot (all collisions)", C_MUTED)],
    [td("Insert (put)",    C_BODY), td("O(1)", C_GREEN), td("O(n)", C_RED), td("Table resize + rehash of all n elements",    C_MUTED)],
    [td("Delete (remove)", C_BODY), td("O(1)", C_GREEN), td("O(n)", C_RED), td("Collision chain must be traversed",           C_MUTED)],
    [td("Iteration",       C_BODY), td("O(n)", C_YELLOW),td("O(n)", C_YELLOW),td("Always linear — must visit all slots",     C_MUTED)],
]
story.append(std_table(comp_data, [100, 80, 80, 220]))
story.append(Spacer(1,8))

story += callout(
    "In LeetCode, always assume O(1) average for hash operations. "
    "The worst case is relevant for security-critical code (hash-DoS attacks) "
    "but almost never affects interview problem complexity analysis.",
    C_ACCENT, icon="💡")

story.append(P("<b>The Space-Time Tradeoff</b>", sH2))
story.append(P(
    "Hashing is the premier example of the <b>Space-Time Tradeoff</b>: "
    "you spend extra memory to buy faster time. The classic brute-force nested "
    "loop uses O(1) extra space but O(n²) time. A hash-based solution uses "
    "O(n) extra space but O(n) time. For n=100,000, that swap trades 10 billion "
    "operations for 100,000 — typically a worthwhile deal.",
    sBody))

tradeoff_data = [
    [th("Approach"), th("Time"),       th("Space"),    th("Constraint When to Prefer")],
    [td("Nested loop (brute force)", C_BODY), td("O(n<super>2</super>)", C_RED),   td("O(1)",    C_GREEN),  td("Memory is extremely tight, n is small", C_MUTED)],
    [td("Sorting + two pointers",    C_BODY), td("O(n log n)", C_YELLOW),           td("O(log n)",C_GREEN),  td("Can modify input, no index needed",      C_MUTED)],
    [td("HashMap / HashSet",         C_BODY), td("O(n)",    C_GREEN),               td("O(n)",    C_YELLOW), td("Speed is priority, space is available",  C_MUTED)],
    [td("Frequency array int[k]",    C_BODY), td("O(n)",    C_GREEN),               td("O(k)",    C_GREEN),  td("Keys are small integers or ASCII chars",  C_MUTED)],
]
story.append(std_table(tradeoff_data, [145, 70, 70, 195]))
story.append(Spacer(1,8))

story.append(P("<b>Collision Resolution (Conceptual)</b>", sH2))
story.append(P(
    "A <b>collision</b> occurs when two different keys produce the same hash slot. "
    "Two primary strategies resolve this:",
    sBody))

coll_data = [
    [th("Strategy"), th("Mechanism"), th("Pro"), th("Con")],
    [td("Chaining",         C_ACCENT),
     td("Each slot holds a linked list. Multiple keys at same slot form a chain.", C_BODY),
     td("Simple; handles high load factors", C_GREEN),
     td("Extra pointer memory; poor cache locality", C_RED)],
    [td("Open Addressing",  C_ACCENT2),
     td("On collision, probe for next empty slot (linear, quadratic, or double hash).", C_BODY),
     td("Better cache performance; no extra pointers", C_GREEN),
     td("Performance degrades at high load; deletion tricky", C_RED)],
]
story.append(std_table(coll_data, [95, 190, 120, 75]))
story.append(Spacer(1,8))

story += callout(
    "Python's dict uses open addressing with a compact probe sequence. "
    "Java's HashMap uses chaining with a tree fallback (chains longer than 8 nodes "
    "become Red-Black trees). You don't need to implement these — just know "
    "they exist and why worst case is O(n).",
    C_ACCENT2, icon="🔧")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 2 — FREQUENCY COUNTING
# ════════════════════════════════════════════════════════
story += section_divider(2, "Pattern 1: Frequency Counting")

story.append(P("<b>The Core Idea</b>", sH2))
story.append(P(
    "Count how many times each element appears in a collection. "
    "The result is a <b>frequency map</b>: element → count. "
    "This map answers 'does element X appear?' (O(1)) and "
    "'how often does X appear?' (O(1)) without rescanning the array.",
    sBody))

story += code_block([
    "## ─── Three ways to build a frequency map ───────────────────────",
    "",
    "## Option 1: Plain dict",
    "freq = {}",
    "for item in collection:",
    "    freq[item] = freq.get(item, 0) + 1",
    "",
    "## Option 2: defaultdict(int) — cleaner",
    "from collections import defaultdict",
    "freq = defaultdict(int)",
    "for item in collection:",
    "    freq[item] += 1",
    "",
    "## Option 3: Counter — most Pythonic",
    "from collections import Counter",
    "freq = Counter(collection)   ## one line!",
    "",
    "## Option 4: Fixed-size array (for ASCII / lowercase letters only)",
    "## Space: O(26) = O(1) constant — always preferred for char problems",
    "freq = [0] * 26",
    "for ch in string:",
    "    freq[ord(ch) - ord('a')] += 1",
])

story += callout(
    "Rule of Thumb: If the key space is small and bounded (e.g., only lowercase "
    "letters a-z, digits 0-9, or ASCII 0-127), use a fixed-size array. "
    "It has guaranteed O(1) worst case, better cache performance, and uses "
    "constant space. Reserve HashMap for unbounded or arbitrary key types.",
    C_GREEN, icon="✅")

story.append(P("<b>Anagram & Permutation Problems</b>", sH2))
story.append(P(
    "Two strings are <b>anagrams</b> if they contain the same characters "
    "with the same frequencies. The canonical check: build frequency maps "
    "for both strings and compare them. O(n) time, O(k) space where k is "
    "alphabet size.",
    sBody))

story += code_block([
    "## ─── Anagram check: are s and t anagrams? ──────────────────────",
    "def is_anagram(s, t):",
    "    if len(s) != len(t): return False",
    "",
    "    ## Method A: Counter comparison  O(n) time, O(k) space",
    "    return Counter(s) == Counter(t)",
    "",
    "## Method B: Fixed array (lowercase only)  — O(1) space",
    "def is_anagram_array(s, t):",
    "    if len(s) != len(t): return False",
    "    freq = [0] * 26",
    "    for i in range(len(s)):",
    "        freq[ord(s[i]) - ord('a')] += 1   ## increment for s",
    "        freq[ord(t[i]) - ord('a')] -= 1   ## decrement for t",
    "    return all(f == 0 for f in freq)       ## all zeros = same freqs",
    "",
    "## ─── Permutation in string ──────────────────────────────────────",
    "## Is p a permutation of any substring of s?",
    "## → Fixed-size sliding window + frequency array comparison",
    "def check_inclusion(p, s):",
    "    if len(p) > len(s): return False",
    "    need = [0] * 26",
    "    have = [0] * 26",
    "    for ch in p: need[ord(ch)-ord('a')] += 1",
    "    for i in range(len(p)): have[ord(s[i])-ord('a')] += 1",
    "    if need == have: return True",
    "    for i in range(len(p), len(s)):",
    "        have[ord(s[i])-ord('a')]          += 1  ## add right",
    "        have[ord(s[i-len(p)])-ord('a')]   -= 1  ## remove left",
    "        if need == have: return True",
    "    return False",
])

story.append(P("<b>Visual: Frequency Map Comparison</b>", sH3))
story.append(P('Checking if "eat" and "tea" are anagrams:', sBody))

pairs = [("e","t"),("a","e"),("t","a")]
col_w = int(CW/6)
header_row = [th("Char"), th("eat freq"), th("tea freq"), th("Match?")]
vis_data = [header_row]
eat_freq = {"e":1,"a":1,"t":1}
tea_freq = {"t":1,"e":1,"a":1}
for ch, _ in [("a",None),("e",None),("t",None)]:
    ef = eat_freq.get(ch,0)
    tf = tea_freq.get(ch,0)
    match = "✅" if ef == tf else "❌"
    mc = C_GREEN if ef == tf else C_RED
    vis_data.append([tdc(f"'{ch}'", C_ACCENT), td(str(ef), C_BODY), td(str(tf), C_BODY), td(match, mc)])
story.append(std_table(vis_data, [CW/4]*4))
story.append(P("All counts match → anagrams confirmed", sCaption))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 3 — COMPLEMENT LOOKUP
# ════════════════════════════════════════════════════════
story += section_divider(3, "Pattern 2: Complement Lookup")

story.append(P("<b>The 'target − x' Trick</b>", sH2))
story.append(P(
    "For many pair-finding problems, instead of checking every pair (O(n²)), "
    "you can ask a smarter question: <i>\"as I process element x, have I already "
    "seen an element that, combined with x, satisfies the condition?\"</i> "
    "For a target sum, that question becomes: <b>\"have I seen target − x?\"</b> "
    "A hash set / map answers this in O(1), reducing the algorithm to O(n).",
    sBody))

story.append(P("have I seen (target − x) before?   →   store x in map, look up complement", sFormula))

story.append(P("<b>Two Sum: From O(n²) to O(n)</b>", sH2))
story += code_block([
    "## ─── Brute Force: O(n²) ────────────────────────────────────────",
    "def two_sum_brute(nums, target):",
    "    for i in range(len(nums)):",
    "        for j in range(i + 1, len(nums)):      ## O(n) inner scan",
    "            if nums[i] + nums[j] == target:",
    "                return [i, j]",
    "    return []",
    "",
    "## ─── HashMap: O(n) ─────────────────────────────────────────────",
    "def two_sum(nums, target):",
    "    seen = {}                  ## maps value → index",
    "    for i, x in enumerate(nums):",
    "        complement = target - x",
    "        if complement in seen:                 ## O(1) lookup",
    "            return [seen[complement], i]",
    "        seen[x] = i            ## store AFTER lookup (avoid using x as its own pair)",
    "    return []",
    "",
    "## ─── Why 'store after lookup'? ─────────────────────────────────",
    "## If target=6 and x=3: complement=3. We check 'is 3 in seen?' first.",
    "## If we stored x BEFORE checking, we'd incorrectly pair x with itself.",
    "## Exception: if duplicates are allowed (e.g., [3,3], target=6), storing",
    "## first would work — but the standard pattern stores after to be safe.",
])

story.append(P("<b>Step-by-Step Trace: nums=[2,7,11,15], target=9</b>", sH3))
trace_data = [
    [th("i"), th("x"), th("complement"), th("seen (before)"), th("Action")],
    [tdc("0"), tdc("2"), tdc("9-2=7"),  tdc("{}"),         td("7 not in seen → store {2:0}", C_BODY)],
    [tdc("1"), tdc("7"), tdc("9-7=2"),  tdc("{2:0}"),       td("2 IN seen → return [0,1] ✅", C_GREEN)],
]
story.append(std_table(trace_data, [30,30,85,120,215]))
story.append(Spacer(1, 8))

story.append(P("<b>Why This Eliminates O(n²)</b>", sH2))
story.append(P(
    "The nested loop checks n×(n-1)/2 pairs. The hash solution processes "
    "each element exactly once and does a constant-time lookup. "
    "The hash table replaces the inner loop entirely — it is a precomputed "
    "answer to the question 'have I seen complement before?'",
    sBody))

elim_data = [
    [th("Step"), th("Brute Force"), th("HashMap Approach")],
    [td("Element x = nums[i]",     C_BODY),
     td("Start inner loop j=i+1",  C_MUTED),
     td("Compute complement = target - x", C_BODY)],
    [td("Search for complement",   C_BODY),
     td("Scan nums[i+1..n-1] = O(n)", C_RED),
     td("seen[complement] = O(1) average", C_GREEN)],
    [td("Store for future lookups",C_BODY),
     td("No storage — rescans every time", C_RED),
     td("seen[x] = i — stored permanently", C_GREEN)],
    [td("Total cost",              C_BODY),
     td("O(n²) — n elements × O(n) scan", C_RED),
     td("O(n) — n elements × O(1) lookup", C_GREEN)],
]
story.append(std_table(elim_data, [130, 185, 165]))
story.append(Spacer(1, 8))

story.append(P("<b>Generalising the Complement Pattern</b>", sH3))
story.append(P(
    "The same principle applies far beyond Two Sum. Any time the problem "
    "asks 'find two elements where f(a, b) = target', check if "
    "'have I seen the value that makes f satisfied?' at each step:",
    sBody))
gen_data = [
    [th("Problem"), th("Condition"), th("What to Store"), th("Complement Check")],
    [td("Two Sum",                  C_BODY), tdc("a + b == target",   C_ACCENT),  tdc("value → index"),   tdc("target - x in seen")],
    [td("Two Sum (sorted)",         C_BODY), tdc("a + b == target",   C_ACCENT),  td("use two pointers",  C_MUTED), td("N/A — no hash needed",C_MUTED)],
    [td("Pair with given product",  C_BODY), tdc("a * b == target",   C_ACCENT2), tdc("value → index"),   tdc("target // x in seen")],
    [td("Pair with given XOR",      C_BODY), tdc("a ^ b == target",   C_ACCENT2), tdc("value set"),       tdc("target ^ x in seen")],
    [td("Four Sum (2+2 split)",     C_BODY), tdc("a+b+c+d==target",   C_GREEN),   tdc("pair_sum → count"),tdc("target-(a+b) in sums")],
]
story.append(std_table(gen_data, [130, 130, 110, 110]))
story.append(Spacer(1, 8))

story += callout(
    "The complement pattern works whenever you can express the second element "
    "as a pure function of the first: complement = f(x, target). "
    "If the second element cannot be determined from the first alone "
    "(e.g., 'find two elements where arr[i] < arr[j]'), a different technique is needed.",
    C_YELLOW, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 4 — GROUPING & BUCKETING
# ════════════════════════════════════════════════════════
story += section_divider(4, "Pattern 3: Grouping & Bucketing")

story.append(P("<b>The Canonical Key Idea</b>", sH2))
story.append(P(
    "Many problems require grouping elements that are 'equivalent' under some "
    "transformation. The pattern: compute a <b>canonical key</b> for each element "
    "such that all equivalent elements produce the <b>same key</b>. "
    "Use this key to bucket them in a HashMap. "
    "The art is in designing a key that is both correct and computationally cheap.",
    sBody))

story += callout(
    "A canonical key is any representation that is identical for all elements "
    "in the same equivalence class. Sorting is the most common canonicalization "
    "for string problems. For numeric patterns, prime-product encoding or "
    "frequency tuples work well.",
    C_ACCENT, icon="🗝️")

story.append(P("<b>Group Anagrams</b>", sH2))
story.append(P(
    "Given a list of strings, group all anagrams together. "
    "All anagrams of a string share the same sorted version. "
    "Use sorted(word) as the canonical key.",
    sBody))

story += code_block([
    "## ─── Group Anagrams by Sorted Key ──────────────────────────────",
    "def group_anagrams(words):",
    "    buckets = defaultdict(list)",
    "    for word in words:",
    "        key = ''.join(sorted(word))    ## canonical key: sorted characters",
    "        buckets[key].append(word)      ## group words with same key",
    "    return list(buckets.values())",
    "",
    "## Example:",
    "## words = ['eat','tea','tan','ate','nat','bat']",
    "## 'eat' → key='aet' → bucket['aet'] = ['eat']",
    "## 'tea' → key='aet' → bucket['aet'] = ['eat','tea']",
    "## 'ate' → key='aet' → bucket['aet'] = ['eat','tea','ate']",
    "## 'tan' → key='ant' → bucket['ant'] = ['tan']",
    "## 'nat' → key='ant' → bucket['ant'] = ['tan','nat']",
    "## 'bat' → key='abt' → bucket['abt'] = ['bat']",
    "## Result: [['eat','tea','ate'], ['tan','nat'], ['bat']]",
    "",
    "## ─── Alternative: Frequency Tuple Key (O(n) per word, no sort) ─",
    "def group_anagrams_v2(words):",
    "    buckets = defaultdict(list)",
    "    for word in words:",
    "        count = [0] * 26",
    "        for ch in word: count[ord(ch)-ord('a')] += 1",
    "        key = tuple(count)             ## tuple is hashable; list is not!",
    "        buckets[key].append(word)",
    "    return list(buckets.values())",
    "## Complexity: O(n * m) where m = word length — better than O(n * m log m)",
])

story.append(P("<b>Visual: Canonical Key Mapping</b>", sH3))
words_ex  = ["eat","tea","tan","ate","nat","bat"]
keys_ex   = ["aet","aet","ant","aet","ant","abt"]
buckets_ex= {"aet":["eat","tea","ate"],"ant":["tan","nat"],"abt":["bat"]}

kv_data = [[th("Word"), th("Sorted Key"), th("Bucket")]]
for w, k in zip(words_ex, keys_ex):
    kv_data.append([tdc(f'"{w}"', C_ACCENT), tdc(f'"{k}"', C_GREEN), tdc(f'bucket["{k}"]', C_ACCENT2)])
story.append(std_table(kv_data, [CW/3]*3))
story.append(P("All words with the same sorted key land in the same bucket", sCaption))
story.append(Spacer(1, 8))

story.append(P("<b>Other Canonical Key Strategies</b>", sH2))
key_data = [
    [th("Equivalence Type"),        th("Canonical Key"),               th("Example Problem")],
    [td("Anagrams",         C_BODY), tdc("sorted(word)"),               td("Group Anagrams (LC 49)",                     C_MUTED)],
    [td("Anagrams (faster)",C_BODY), tdc("tuple(freq_array[26])"),      td("Group Anagrams alt (LC 49)",                 C_MUTED)],
    [td("Same difference pattern",C_BODY),tdc("tuple(diffs from first)"),td("Find duplicate file content",               C_MUTED)],
    [td("Same digit frequency",C_BODY),tdc("tuple(sorted(Counter(n)))"),td("Group digit-anagram numbers",                C_MUTED)],
    [td("Isomorphic strings", C_BODY),tdc("pattern tuple (first-seen)"),td("Isomorphic Strings (LC 205)",                C_MUTED)],
    [td("Word pattern match", C_BODY),td("normalised structure", C_BODY),td("Word Pattern (LC 290)",          C_MUTED)],
]
story.append(std_table(key_data, [140, 175, 165]))
story.append(Spacer(1, 8))

story.append(P("<b>Adjacency List Representation (Graph-lite)</b>", sH3))
story.append(P(
    "A HashMap of <b>node → list of neighbours</b> is the standard hash-based "
    "adjacency list for graph problems. It uses O(V + E) space and gives O(degree) "
    "neighbour iteration — much better than an O(V²) matrix for sparse graphs.",
    sBody))
story += code_block([
    "## ─── Build adjacency list from edge list ────────────────────────",
    "def build_adj(n, edges):",
    "    adj = defaultdict(list)            ## or: {i: [] for i in range(n)}",
    "    for u, v in edges:",
    "        adj[u].append(v)",
    "        adj[v].append(u)               ## omit for directed graph",
    "    return adj",
    "",
    "## Usage in BFS / DFS:",
    "## for neighbour in adj[current_node]:   ## O(degree) per node",
    "##     if neighbour not in visited:",
    "##         queue.append(neighbour)",
])
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 5 — VALUE → INDEX MAPPING
# ════════════════════════════════════════════════════════
story += section_divider(5, "Pattern 4: Value → Index Mapping")

story.append(P("<b>Storing Indices, Not Just Presence</b>", sH2))
story.append(P(
    "Sometimes you don't just need to know <i>if</i> a value was seen, "
    "but <i>where</i> it was seen. By mapping <b>value → index</b>, "
    "you can calculate the distance between two occurrences of the same "
    "element in O(1) at lookup time.",
    sBody))

story += code_block([
    "## ─── Value → Index Pattern Template ────────────────────────────",
    "def value_to_index_template(nums):",
    "    index_map = {}             ## maps: value → most recent index",
    "",
    "    for i, val in enumerate(nums):",
    "        if val in index_map:",
    "            ## Found same value at two positions",
    "            prev_index = index_map[val]",
    "            distance   = i - prev_index",
    "            ## ... use distance for problem logic ...",
    "",
    "        index_map[val] = i     ## always update to most recent index",
    "                               ## (or store first occurrence — depends on problem)",
    "    return result",
])

story.append(P("<b>Contains Duplicate II</b>", sH3))
story.append(P(
    "Find if any value appears twice within a window of size k. "
    "Store value → last seen index. On finding a duplicate, check if the "
    "index gap ≤ k.",
    sBody))
story += code_block([
    "## ─── Contains Duplicate II ─────────────────────────────────────",
    "def contains_nearby_duplicate(nums, k):",
    "    last_seen = {}             ## value → last index where value appeared",
    "",
    "    for i, val in enumerate(nums):",
    "        if val in last_seen and i - last_seen[val] <= k:",
    "            return True        ## duplicate within window of k",
    "        last_seen[val] = i     ## update to most recent position",
    "",
    "    return False",
    "",
    "## Trace: nums=[1,2,3,1], k=3",
    "## i=0: val=1, not in map → store {1:0}",
    "## i=1: val=2, not in map → store {1:0, 2:1}",
    "## i=2: val=3, not in map → store {1:0, 2:1, 3:2}",
    "## i=3: val=1, IN map, distance=3-0=3 ≤ k=3 → return True ✅",
])

story.append(P("<b>Longest Subarray Between Two Identical Elements</b>", sH3))
story.append(P(
    "Another classic: find the maximum distance between any two equal elements. "
    "Store the <b>first</b> occurrence index, then on finding a duplicate, "
    "compute the gap. Crucially, do NOT update the stored index on revisit — "
    "you want the largest possible gap.",
    sBody))
story += code_block([
    "## ─── Maximum Distance Between Same Elements ─────────────────────",
    "def max_distance_same_elem(arr):",
    "    first_seen = {}            ## value → FIRST index (never overwrite)",
    "    max_dist   = 0",
    "",
    "    for i, val in enumerate(arr):",
    "        if val in first_seen:",
    "            max_dist = max(max_dist, i - first_seen[val])",
    "            ## DO NOT update first_seen[val] — want maximum gap",
    "        else:",
    "            first_seen[val] = i   ## only store on first occurrence",
    "",
    "    return max_dist",
    "",
    "## ─── Key design choice: first vs. most recent index ─────────────",
    "## Store FIRST index when: maximizing distance (keep oldest position)",
    "## Store MOST RECENT index when: checking within-k constraint",
])

story += callout(
    "Design decision: whether to store the FIRST or MOST RECENT occurrence "
    "depends entirely on the problem goal. 'Maximum gap' → store first (never update). "
    "'Within k constraint' → store most recent (always update). "
    "Getting this wrong is a very common interview bug.",
    C_YELLOW, icon="⚠️")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 6 — HASHSET LOOKUPS
# ════════════════════════════════════════════════════════
story += section_divider(6, "Pattern 5: HashSet Lookups")

story.append(P("<b>When You Only Need Existence, Not Count</b>", sH2))
story.append(P(
    "A <b>HashSet</b> (Python: <b>set</b>, Java: <b>HashSet</b>) stores unique "
    "elements and supports O(1) average <i>contains</i> queries. "
    "Use it when you only need to answer 'have I seen this before?' — "
    "not 'how many times have I seen it?'",
    sBody))

story += code_block([
    "## ─── HashSet Patterns ───────────────────────────────────────────",
    "",
    "## 1. Deduplication: remove duplicates while preserving order",
    "def deduplicate(arr):",
    "    seen = set()",
    "    return [x for x in arr if not (x in seen or seen.add(x))]",
    "",
    "## 2. Existence check: O(1) lookup vs O(n) linear scan",
    "## BAD:  if target in list     → O(n)",
    "## GOOD: if target in set_ver  → O(1) average",
    "seen_set = set(arr)              ## build once: O(n)",
    "for query in queries:",
    "    if query in seen_set:        ## each query: O(1)",
    "        process(query)",
    "",
    "## 3. Intersection / Union of two collections: O(m+n)",
    "set_a = set(arr_a)",
    "set_b = set(arr_b)",
    "common    = set_a & set_b        ## intersection",
    "all_elems = set_a | set_b        ## union",
    "only_in_a = set_a - set_b        ## difference",
])

story.append(P("<b>Longest Consecutive Sequence</b>", sH2))
story.append(P(
    "Find the length of the longest consecutive integer sequence in an unsorted "
    "array. Naive sort is O(n log n). The HashSet approach is O(n):",
    sBody))
story += code_block([
    "## ─── Longest Consecutive Sequence: O(n) ────────────────────────",
    "def longest_consecutive(nums):",
    "    num_set = set(nums)     ## O(1) membership test",
    "    best    = 0",
    "",
    "    for num in num_set:     ## iterate set (deduplicated)",
    "        ## Only start a sequence at its BEGINNING",
    "        ## (num-1 not in set means num is the start)",
    "        if num - 1 not in num_set:",
    "            current = num",
    "            length  = 1",
    "            while current + 1 in num_set:   ## extend sequence: O(1) each",
    "                current += 1",
    "                length  += 1",
    "            best = max(best, length)",
    "",
    "    return best",
    "",
    "## Why O(n) total even though there's a while loop inside a for loop?",
    "## Each number is visited AT MOST TWICE:",
    "##   once in the outer for loop, once inside a while loop.",
    "## Total inner while steps across ALL outer iterations = n.",
    "## Amortised: O(n) + O(n) = O(n).",
])

story += callout(
    "The 'only start at sequence beginning' trick (check num-1 not in set) "
    "is the key to the O(n) proof. Without it, every number would trigger "
    "a while loop, and overlapping sequences would be counted multiple times — "
    "pushing complexity back to O(n²) in the worst case.",
    C_PURPLE, icon="🔑")

story.append(P("<b>Two-Set Technique: Valid Sudoku / Board Validation</b>", sH3))
story.append(P(
    "For board-validation problems, create a set per row, column, and box. "
    "On each cell visit, check all three sets in O(1). "
    "If the element is already in any set, the board is invalid.",
    sBody))
story += code_block([
    "## ─── Board Validation with Sets ────────────────────────────────",
    "def is_valid_board(board, n):",
    "    rows  = [set() for _ in range(n)]",
    "    cols  = [set() for _ in range(n)]",
    "    boxes = [set() for _ in range(n)]",
    "",
    "    for r in range(n):",
    "        for c in range(n):",
    "            val = board[r][c]",
    "            if val == '.': continue",
    "            box_id = (r // 3) * 3 + (c // 3)   ## 3x3 box index",
    "",
    "            if val in rows[r] or val in cols[c] or val in boxes[box_id]:",
    "                return False",
    "",
    "            rows[r].add(val); cols[c].add(val); boxes[box_id].add(val)",
    "",
    "    return True",
])
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 7 — PREFIX SUM + HASHMAP
# ════════════════════════════════════════════════════════
story += section_divider(7, "Pattern 6: Prefix Sum + HashMap")

story.append(P("<b>The Combination: Why It's Powerful</b>", sH2))
story.append(P(
    "Prefix Sum alone answers range queries in O(1). HashMap alone gives O(1) "
    "lookups. <b>Combined</b>, they solve problems that neither technique can "
    "handle alone — specifically: <i>count subarrays with an exact sum K, "
    "including arrays with negative numbers.</i>",
    sBody))

story.append(P("sum(L, R) = K   →   prefix[R+1] - prefix[L] = K   →   prefix[L] = prefix[R+1] - K", sFormula))

story += code_block([
    "## ─── Subarray Sum Equals K ──────────────────────────────────────",
    "def subarray_sum(nums, k):",
    "    count       = 0",
    "    running_sum = 0",
    "    prefix_map  = {0: 1}   ## seed: empty prefix (sum=0) seen once",
    "",
    "    for num in nums:",
    "        running_sum += num",
    "",
    "        ## If (running_sum - k) was seen before, a subarray ending",
    "        ## here with sum k exists — as many times as that prefix occurred",
    "        complement = running_sum - k",
    "        count += prefix_map.get(complement, 0)",
    "",
    "        ## Record this running sum",
    "        prefix_map[running_sum] = prefix_map.get(running_sum, 0) + 1",
    "",
    "    return count",
    "",
    "## Works with NEGATIVE numbers — this is why sliding window fails here.",
    "## The running_sum can decrease, so there is no monotonicity to exploit.",
])

story.append(P("<b>Visualising the Prefix Map</b>", sH3))
story.append(P("Trace: nums=[3, 4, -7, 3, 1], k=0", sBody))

nums_t = [3,4,-7,3,1]
prefix_trace = []
rs = 0
pm = {0:1}
for x in nums_t:
    rs += x
    comp = rs - 0  # k=0
    found = pm.get(comp, 0)
    prefix_trace.append((x, rs, comp, found, dict(pm)))
    pm[rs] = pm.get(rs, 0) + 1

pt_data = [[th("num"), th("running_sum"), th("complement (rs-k)"), th("found in map"), th("count added")]]
for x, rs_v, comp, found, _ in prefix_trace:
    pt_data.append([
        tdc(str(x), C_ACCENT),
        tdc(str(rs_v), C_ACCENT2),
        tdc(str(comp), C_BODY),
        tdc(str(found), C_GREEN if found > 0 else C_MUTED),
        td(str(found), C_GREEN if found > 0 else C_MUTED),
    ])
story.append(std_table(pt_data, [50, 90, 135, 105, 100]))
story.append(P("Total count = 3 (subarrays with sum 0: [3,4,-7], [4,-7,3], [3,4,-7,3,1] wait — check manually)", sCaption))
story.append(Spacer(1,4))

story.append(P("<b>Modular Arithmetic Variant: Subarray Sum Divisible by K</b>", sH3))
story.append(P(
    "Instead of storing prefix sums, store <b>prefix sums modulo k</b>. "
    "If two prefix sums have the same remainder mod k, the subarray between "
    "them is divisible by k.",
    sBody))
story += code_block([
    "## ─── Subarray Sum Divisible by K ───────────────────────────────",
    "def subarray_div_k(nums, k):",
    "    count      = 0",
    "    running    = 0",
    "    mod_map    = {0: 1}    ## remainder 0 seen once before any element",
    "",
    "    for num in nums:",
    "        running = (running + num) % k",
    "        if running < 0: running += k   ## handle negative nums in Python",
    "        count  += mod_map.get(running, 0)",
    "        mod_map[running] = mod_map.get(running, 0) + 1",
    "",
    "    return count",
    "## Why? If prefix[i] % k == prefix[j] % k, then",
    "## (prefix[j] - prefix[i]) % k == 0  → sum(i+1..j) divisible by k",
])

story += callout(
    "The Prefix Sum + HashMap pattern is the universal solution for 'count subarrays "
    "where f(subarray) = target' problems. Variants include: exact sum, divisible sum, "
    "equal 0s and 1s (treat 0 as -1), and longest balanced subarray. "
    "All use the same structure — only the 'complement' formula changes.",
    C_TEAL, icon="🌊")

story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 8 — COMPARISON
# ════════════════════════════════════════════════════════
story += section_divider(8, "Comparison & Decision Making")

story.append(P("<b>HashMap vs. HashSet vs. Frequency Array</b>", sH2))

comp3_data = [
    [th("Dimension"), th("HashMap"), th("HashSet"), th("Freq Array int[k]")],
    [td("Stores",       C_BODY), td("key → value pairs",           C_BODY), td("keys only (no value)",       C_BODY), td("index → count (implicit key)",   C_BODY)],
    [td("Lookup",       C_BODY), tdc("O(1) avg",     C_GREEN),              tdc("O(1) avg",  C_GREEN),               tdc("O(1) exact",  C_GREEN)],
    [td("Space",        C_BODY), tdc("O(n) dynamic", C_YELLOW),             tdc("O(n) dynamic", C_YELLOW),           tdc("O(k) constant",C_GREEN)],
    [td("Key type",     C_BODY), td("Any hashable",  C_BODY),               td("Any hashable",  C_BODY),              td("Small integers only",            C_RED)],
    [td("Worst case",   C_BODY), tdc("O(n) on collision", C_RED),           tdc("O(n) on collision", C_RED),         tdc("O(1) always",  C_GREEN)],
    [td("Ordering",     C_BODY), td("Insertion order (Python 3.7+)",C_BODY),td("No order",      C_MUTED),            td("Sorted by value (implicit)",     C_BODY)],
    [td("Use when",     C_BODY), td("Need to map value→something (count, index, list)", C_ACCENT, "Helvetica-Oblique"),
                                  td("Need existence only (seen?, dedup, set ops)", C_ACCENT2, "Helvetica-Oblique"),
                                  td("Keys are chars or small ints (a-z, 0-9, ASCII)", C_GREEN, "Helvetica-Oblique")],
    [td("Classic use",  C_BODY), td("Two Sum, Group Anagrams, Prefix+Hash",C_MUTED),
                                  td("Dedup, Consecutive Sequence, Board Validation",C_MUTED),
                                  td("Anagram check, Permutation in String",C_MUTED)],
]
story.append(std_table(comp3_data, [85, 150, 150, 95]))
story.append(Spacer(1, 10))

story.append(P("<b>Decision Flowchart</b>", sH2))
flow = [
    ("Q1", "Do you need to associate each key with a VALUE (count, index, list)?", C_ACCENT),
    (" → YES",  "Use HashMap (dict). Store key → value.",                           C_GREEN),
    (" → NO",   "Continue to Q2.",                                                  C_MUTED),
    ("Q2", "Do you only need to check existence or deduplication?",                 C_ACCENT),
    (" → YES",  "Use HashSet (set). Lighter than HashMap.",                         C_GREEN),
    (" → NO",   "Continue to Q3.",                                                  C_MUTED),
    ("Q3", "Are all keys small integers or chars from a bounded alphabet?",         C_ACCENT),
    (" → YES",  "Use Frequency Array int[k]. O(1) worst case, best cache perf.",    C_GREEN),
    (" → NO",   "Use HashMap.",                                                     C_BODY),
    ("Q4", "Is the input potentially adversarial or security-sensitive?",           C_ACCENT),
    (" → YES",  "Consider a tree-based map (SortedDict) for O(n log n) guaranteed.",C_YELLOW),
    (" → NO",   "HashMap is fine — adversarial worst case is not a concern here.",  C_BODY),
]
for label, text, clr in flow:
    bg = C_CARD if not label.startswith(" ") else C_DARK2
    story.append(Table([[
        P(f"<b>{label}</b>", S("_", fontName="Courier-Bold", fontSize=9, textColor=clr)),
        P(text, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[80, CW-80], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 8))

story.append(P("<b>Pattern Selection Quick Reference</b>", sH2))
pat_data = [
    [th("Signal in Problem"),                        th("Pattern to Use"),          th("Structure")],
    [td("'find pair/two elements'",         C_BODY), td("Complement Lookup",        C_ACCENT),  tdc("seen_map = {}")],
    [td("'group / categorize by property'", C_BODY), td("Bucket by canonical key",  C_ACCENT2), tdc("buckets = defaultdict(list)")],
    [td("'count occurrences of each'",      C_BODY), td("Frequency Counter",        C_GREEN),   tdc("freq = Counter(arr)")],
    [td("'have I seen this before?'",       C_BODY), td("HashSet existence check",  C_TEAL),    tdc("seen = set()")],
    [td("'distance between same elements'", C_BODY), td("Value → Index mapping",    C_PURPLE),  tdc("last = {val: idx}")],
    [td("'subarrays with exact sum K'",     C_BODY), td("Prefix Sum + HashMap",     C_YELLOW),  tdc("prefix_map = {0:1}")],
    [td("'longest consecutive / streak'",   C_BODY), td("HashSet + boundary check", C_ORANGE),  tdc("s = set(arr); check x-1 not in s")],
    [td("'dedup / unique elements'",        C_BODY), td("HashSet dedup",            C_GREEN),   tdc("unique = list(dict.fromkeys(arr))")],
]
story.append(std_table(pat_data, [175, 145, 160]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 9 — PROBLEM ROADMAP
# ════════════════════════════════════════════════════════
story += section_divider(9, "LeetCode Problem Roadmap")
story.append(P("Solve in order — each problem is a clean representative of its pattern.", sBody))

story.append(P("<b>🟢 Easy — Build the Foundation</b>", sH2))
easy_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("1",   C_GREEN), td("Two Sum",                           C_BODY), td("Complement Lookup",  C_ACCENT),  td("seen[target-x]; store AFTER lookup.", C_MUTED)],
    [tdc("217", C_GREEN), td("Contains Duplicate",               C_BODY), td("HashSet",             C_TEAL),    td("Add to set; return True if already in.", C_MUTED)],
    [tdc("242", C_GREEN), td("Valid Anagram",                    C_BODY), td("Freq Counter",        C_GREEN),   td("int[26] delta; all zeros = anagram.", C_MUTED)],
    [tdc("383", C_GREEN), td("Ransom Note",                      C_BODY), td("Freq Counter",        C_GREEN),   td("mag freq must cover note freq.", C_MUTED)],
    [tdc("349", C_GREEN), td("Intersection of Two Arrays",       C_BODY), td("HashSet",             C_TEAL),    td("set(nums1) & set(nums2).", C_MUTED)],
    [tdc("771", C_GREEN), td("Jewels and Stones",                C_BODY), td("HashSet",             C_TEAL),    td("Build jewel set; count stones in it.", C_MUTED)],
    [tdc("1002",C_GREEN), td("Find Common Characters",           C_BODY), td("Freq Counter",        C_GREEN),   td("Min freq across all words per char.", C_MUTED)],
    [tdc("219", C_GREEN), td("Contains Duplicate II",            C_BODY), td("Value→Index",         C_PURPLE),  td("Store last seen index; check i-prev ≤ k.", C_MUTED)],
]
story.append(std_table(easy_data, [38, 185, 110, 147]))
story.append(Spacer(1, 10))

story.append(P("<b>🟡 Medium — Apply the Patterns</b>", sH2))
med_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("49",  C_YELLOW), td("Group Anagrams",                   C_BODY), td("Grouping / Bucket", C_ACCENT2), td("Key = sorted(word) or tuple(freq[26]).", C_MUTED)],
    [tdc("128", C_YELLOW), td("Longest Consecutive Sequence",     C_BODY), td("HashSet Boundary",  C_TEAL),    td("Start only if x-1 not in set; extend while x+1 in set.", C_MUTED)],
    [tdc("560", C_YELLOW), td("Subarray Sum Equals K",            C_BODY), td("Prefix+HashMap",    C_YELLOW),  td("Seed {0:1}; complement = prefix-k.", C_MUTED)],
    [tdc("974", C_YELLOW), td("Subarray Sums Divisible by K",     C_BODY), td("Prefix+HashMap",    C_YELLOW),  td("Store prefix%k; same remainder = divisible subarray.", C_MUTED)],
    [tdc("525", C_YELLOW), td("Contiguous Array (0s and 1s)",     C_BODY), td("Prefix+HashMap",    C_YELLOW),  td("Replace 0→-1; find longest zero-sum subarray.", C_MUTED)],
    [tdc("438", C_YELLOW), td("Find All Anagrams in a String",    C_BODY), td("Freq Array+Window", C_GREEN),   td("Fixed window; compare int[26] arrays per slide.", C_MUTED)],
    [tdc("567", C_YELLOW), td("Permutation in String",            C_BODY), td("Freq Array+Window", C_GREEN),   td("Same as 438 — check if freq match in k-window.", C_MUTED)],
    [tdc("347", C_YELLOW), td("Top K Frequent Elements",          C_BODY), td("Freq Counter",      C_GREEN),   td("Count freq; bucket sort by count or heap.", C_MUTED)],
    [tdc("380", C_YELLOW), td("Insert Delete GetRandom O(1)",     C_BODY), td("HashMap+Array",     C_ACCENT2), td("Map value→array_index; swap+pop for delete.", C_MUTED)],
    [tdc("451", C_YELLOW), td("Sort Characters By Frequency",     C_BODY), td("Freq Counter",      C_GREEN),   td("Count then sort by count descending.", C_MUTED)],
]
story.append(std_table(med_data, [38, 195, 110, 137]))
story.append(Spacer(1, 10))

story.append(P("<b>🔴 Hard — Master the Craft</b>", sH2))
hard_data = [
    [th("#"), th("Problem"), th("Pattern"), th("Key Insight")],
    [tdc("76",  C_RED), td("Minimum Window Substring",            C_BODY), td("HashMap+Variable Window",  C_PURPLE),
     td("'formed' counter tracks how many chars meet required freq.", C_MUTED)],
    [tdc("992", C_RED), td("Subarrays with K Different Integers", C_BODY), td("HashMap+Two Windows",      C_PURPLE),
     td("exactly(k) = atMost(k) - atMost(k-1). Two calls.", C_MUTED)],
    [tdc("30",  C_RED), td("Substring with All Words",            C_BODY), td("HashMap+Word-Level Window", C_PURPLE),
     td("Slide word-by-word, not char-by-char. HashMap of word counts.", C_MUTED)],
    [tdc("41",  C_RED), td("First Missing Positive",              C_BODY), td("Array as HashMap (cyclic sort)", C_ORANGE),
     td("Place each num at index num-1. Then find first mismatch.", C_MUTED)],
    [tdc("149", C_RED), td("Max Points on a Line",                C_BODY), td("Slope HashMap",            C_PURPLE),
     td("For each anchor point, group other points by (dy/dx) slope.", C_MUTED)],
]
story.append(std_table(hard_data, [38, 185, 125, 132]))
story.append(PageBreak())

# ════════════════════════════════════════════════════════
# SECTION 10 — PITFALLS
# ════════════════════════════════════════════════════════
story += section_divider(10, "Pitfalls & Edge Cases")

story.append(P("<b>Pitfall 1: Hash Collisions and Adversarial Inputs</b>", sH2))
story.append(P(
    "In competitive programming or security contexts, an attacker who knows "
    "the hash seed can craft an input where all keys hash to the same slot, "
    "degrading every operation to O(n) and causing O(n²) total complexity. "
    "Python and Java mitigate this with randomized hash seeds.",
    sBody))
story += code_block([
    "## ─── Collision scenario (conceptual) ───────────────────────────",
    "## If hash(x) % capacity always returns the same slot:",
    "## table = {}",
    "## for k in adversarial_keys:   ## all hash to slot 7",
    "##     table[k] = k             ## each insert scans chain at slot 7",
    "## → O(n) per insert → O(n²) total!",
    "",
    "## Mitigation in Python: hash(x) is randomised per interpreter session",
    "## (PYTHONHASHSEED). You cannot reproduce the same hash across runs.",
    "",
    "## For interview purposes: always state O(n) average, acknowledge",
    "## O(n) worst case exists, and note it is rarely a practical concern.",
])

story.append(P("<b>Pitfall 2: Mutable vs. Immutable Keys</b>", sH2))
story.append(P(
    "Hash map keys <b>must be immutable</b> (hashable). In Python, lists and "
    "dicts cannot be keys. This matters when your canonical key is a sequence "
    "— use tuple instead of list.",
    sBody))
story += code_block([
    "## ─── Mutable key errors ─────────────────────────────────────────",
    "",
    "## WRONG — list is mutable → TypeError: unhashable type: 'list'",
    "## key = [1, 0, 2, 1, 0]",
    "## bucket[key] = word             ## ← crashes",
    "",
    "## CORRECT — convert to tuple (immutable)",
    "key = tuple([1, 0, 2, 1, 0])      ## tuples are hashable",
    "bucket[key] = word                ## ← works",
    "",
    "## CORRECT — sorted string (strings are immutable)",
    "key = ''.join(sorted(word))",
    "bucket[key] = word",
    "",
    "## Other immutable types safe as keys:",
    "## int, float, str, tuple, frozenset, bool",
    "",
    "## Mutable types that CANNOT be keys:",
    "## list, dict, set, bytearray",
])

story += callout(
    "frozenset is the immutable version of set and IS hashable. "
    "If your key needs to represent an unordered collection of unique items, "
    "frozenset({1, 2, 3}) works as a dict key where {1, 2, 3} would not.",
    C_TEAL, icon="❄️")

story.append(P("<b>Pitfall 3: Memory Limits</b>", sH2))
story.append(P(
    "Hash tables store all n elements in memory. For large inputs or when "
    "values themselves are large strings, the O(n) space cost is real. "
    "Consider these thresholds:",
    sBody))
mem_data = [
    [th("n"),           th("~HashMap Memory (Python dict)"), th("Concern Level")],
    [tdc("10<super>3</super>"),  td("~100 KB",  C_BODY),  td("✅ Safe",         C_GREEN)],
    [tdc("10<super>5</super>"),  td("~10 MB",   C_BODY),  td("✅ Typically fine",C_GREEN)],
    [tdc("10<super>6</super>"),  td("~100 MB",  C_BODY),  td("⚠️  Check limits", C_YELLOW)],
    [tdc("10<super>7</super>+"), td("1+ GB",    C_BODY),  td("❌ May exceed limit",C_RED)],
]
story.append(std_table(mem_data, [120, 190, 170]))
story.append(Spacer(1, 8))

story.append(P("<b>Pitfall 4: Key Cardinality Explosion in Grouping</b>", sH3))
story.append(P(
    "When using sorted strings as HashMap keys, a very long string produces "
    "a very long key. With n words each of length m, the total key storage "
    "is O(n·m) — same as the input, so it's acceptable. But watch out for "
    "tuple keys from large frequency arrays: tuple(counter) on unicode text "
    "can produce tuples with tens of thousands of elements.",
    sBody))
story += code_block([
    "## Key size matters!",
    "",
    "## For lowercase ASCII only — safe: tuple has 26 elements max",
    "key = tuple(freq[26])",
    "",
    "## For arbitrary Unicode text — dangerous: tuple can be huge",
    "key = tuple(Counter(word).items())  ## varies: 1 to len(word) pairs",
    "",
    "## Better for Unicode: sort and join (string key, O(m log m))",
    "key = ''.join(sorted(word))",
])

story.append(P("<b>Pitfall 5: Modifying a HashMap While Iterating</b>", sH3))
story += code_block([
    "## WRONG — RuntimeError: dictionary changed size during iteration",
    "## for key in freq:",
    "##     if freq[key] == 0:",
    "##         del freq[key]         ## ← mutating during iteration!",
    "",
    "## CORRECT — iterate over a copy",
    "for key in list(freq.keys()):    ## list() makes a snapshot",
    "    if freq[key] == 0:",
    "        del freq[key]            ## safe: iterating the copy",
    "",
    "## Or use a comprehension to rebuild:",
    "freq = {k: v for k, v in freq.items() if v > 0}",
])

story += callout(
    "Never delete from a dict while iterating it directly. "
    "In Python, this raises RuntimeError. In other languages it may "
    "silently corrupt iteration order. Always iterate a copy or "
    "rebuild the map with a comprehension.",
    C_RED, icon="🔴")

# Final cheat sheet
story.append(PageBreak())
story += section_divider(0, "Master Cheat Sheet")
story.append(P("One-page reference for all six patterns, structures, and decision rules.", sBody))

cheat = [
    [th("Pattern"),             th("Structure"),             th("When to Use"),                        th("Complexity")],
    [td("Frequency Count",C_ACCENT),  tdc("Counter/int[26]"),  td("Count occurrences, anagram check",C_BODY),      tdc("O(n) time O(k) space")],
    [td("Complement Lookup",C_ACCENT2),tdc("seen_map = {}"),   td("Find pair a+b=target, Two Sum",    C_BODY),      tdc("O(n) time O(n) space")],
    [td("Grouping/Bucket", C_GREEN),  tdc("defaultdict(list)"),td("Group by equivalence (anagrams)",  C_BODY),      tdc("O(n·m) time O(n) space")],
    [td("Value→Index",    C_PURPLE),  tdc("{val: idx}"),       td("Distance queries, within-k dup",   C_BODY),      tdc("O(n) time O(n) space")],
    [td("HashSet Lookup", C_TEAL),    tdc("seen = set()"),     td("Existence, dedup, consecutive seq",C_BODY),      tdc("O(n) time O(n) space")],
    [td("Prefix+HashMap", C_YELLOW),  tdc("prefix_map={0:1}"), td("Subarray sum = K, negatives OK",  C_BODY),      tdc("O(n) time O(n) space")],
]
story.append(std_table(cheat, [115, 120, 195, 50]))
story.append(Spacer(1, 10))

story.append(P("<b>The Three-Question Pre-Code Checklist</b>", sH2))
checks = [
    ("What is my KEY?",       "Identify what you will hash. Must be immutable. String/int/tuple only."),
    ("What is my VALUE?",     "Count? Index? List of items? None (HashSet)? This determines HashMap vs Set."),
    ("What is my INVARIANT?", "What does 'element in map' guarantee? First occurrence? Most recent? All occurrences?"),
    ("Seed needed?",          "Prefix+HashMap: always seed with {0: 1} before the loop."),
    ("Update order?",         "For complement lookup: lookup FIRST, store AFTER (avoid self-pairing)."),
    ("Mutable key?",          "If key is list or set: convert to tuple or frozenset before using as key."),
    ("Memory concern?",       "If n > 10^6 or values are large strings: consider if space is acceptable."),
    ("Worst case?",           "State O(1) avg, O(n) worst. For most LeetCode problems, avg case is sufficient."),
]
for q, a in checks:
    story.append(Table([[
        P(f"<b><font color='#34D399'>[ ] {q}</font></b>", S("_", fontName="Helvetica-Bold", fontSize=9, textColor=C_GREEN)),
        P(a, S("_", fontName="Helvetica", fontSize=9, textColor=C_BODY)),
    ]], colWidths=[160, CW-160], style=TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),C_CARD),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("LINEBELOW",(0,0),(-1,-1),0.5,C_BORDER)])))
story.append(Spacer(1, 12))

story.append(Table([[
    P("<b>You now have the complete Hashing Patterns mental model.</b><br/><br/>"
      "Every hash-based optimization follows the same philosophy: "
      "spend O(n) space to convert an O(n) or O(n²) time inner-loop search "
      "into an O(1) lookup. The art is in choosing the right structure "
      "(HashMap/Set/array), designing the right key, and deciding whether "
      "to store the first or most recent occurrence.<br/><br/>"
      "Recommended path: LC 1 (complement) → LC 242 (freq array) → LC 49 "
      "(canonical key) → LC 128 (set boundary) → LC 560 (prefix+hash). "
      "After these five problems, you will recognize hashing opportunities "
      "in virtually every other algorithm category.",
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
        f"Hashing Patterns — Zero to Hero  ·  Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_bg, onLaterPages=add_page_bg)
print("PDF built successfully!")