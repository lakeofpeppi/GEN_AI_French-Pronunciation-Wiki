"""program checks for the french pronunciation wiki and its deck graph.

usage:
  python3 pipeline/check.py wiki                  # lint the wiki (incl. quote check, moved here from G2)
  python3 pipeline/check.py coverage <topic-dir>  # gate G1
  python3 pipeline/check.py cards    <topic-dir>  # gate G2
  python3 pipeline/check.py outline  <topic-dir>  # gate G3
  python3 pipeline/check.py slides   <topic-dir>  # gate G4

exit code 0 = pass, 1 = fail. every failure is printed so the next round
knows exactly what to fix (and only that).
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# matches [S3 §Nasal vowels]: group 1 is the source id, group 2 the section name
CITE = re.compile(r"\[(S[1-6]) §([^\]]+)\]")
# a cite followed by a «quote», the quote is group 3
CITE_QUOTE = re.compile(r"\[(S[1-6]) §([^\]]+)\]\s*«([^»]+)»")
LINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")
MIN_QUOTE = 6

_cache = {}


def source_text(src):
    """full extracted text of one source, or None if we don't have it."""
    if src not in _cache:
        path = os.path.join(ROOT, "raw", "text", src, "full.txt")
        _cache[src] = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    return _cache[src]


# curly quotes and apostrophes are just typography, map them to plain ones before comparing
TYPO = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "«": '"', "»": '"'})


def squash(text):
    # pdf text breaks lines anywhere and adds random spaces, so drop all whitespace and ignore case
    return re.sub(r"\s+", "", text.translate(TYPO)).lower()


def in_source(src, snippet):
    text = source_text(src)
    return text is not None and squash(snippet) in squash(text)


def quote_problems(where, src, section, quote):
    """shared by the wiki lint and the card gate, so both check quotes the same way."""
    out = []
    if not in_source(src, section):
        out.append(f"{where}: section '§{section}' not found in {src}")
    if len(squash(quote)) < MIN_QUOTE:
        out.append(f"{where}: quote «{quote}» too short to be evidence (min {MIN_QUOTE} chars)")
    elif not in_source(src, quote):
        out.append(f"{where}: quote «{quote}» not found in {src}")
    return out


def report(name, problems):
    if problems:
        print(f"FAIL {name}: {len(problems)} problem(s)")
        for p in problems:
            print("  -", p)
        return 1
    print(f"PASS {name}")
    return 0


# ---------- wiki lint ----------

def check_wiki():
    problems = []
    pages = {}
    for path in glob.glob(os.path.join(ROOT, "wiki", "*", "*.md")):
        pages[os.path.splitext(os.path.basename(path))[0]] = (path, open(path, encoding="utf-8").read())

    log = open(os.path.join(ROOT, "wiki", "log.md"), encoding="utf-8").read()
    ingested = set(re.findall(r"\| ingest \| (S[1-6]) \|", log))  # only these can be cited

    linked = set()
    for name, (path, text) in pages.items():
        rel = os.path.relpath(path, ROOT)
        for src, section in CITE.findall(text):
            if src not in ingested:
                problems.append(f"{rel}: cites {src} but {src} hasn't been ingested yet")
        for target in LINK.findall(text):
            linked.add(target)
            if target not in pages:
                problems.append(f"{rel}: broken link [[{target}]]")
        # every key point needs a cite AND a quote, and the quote has to really be in the source
        section = re.search(r"## Key points\n(.*?)(\n## |\Z)", text, re.S)
        if section:
            for line in section.group(1).splitlines():
                if not line.startswith("- "):
                    continue
                found = CITE_QUOTE.findall(line)
                if not found:
                    problems.append(f"{rel}: key point without [S# §section] «quote» -> {line[:60]}")
                for src, sec, quote in found:
                    problems += quote_problems(rel, src, sec, quote)

    for name, (path, _) in pages.items():
        # a concept nobody links to is an orphan, the wiki can't reach it
        if "/concepts/" in path.replace(os.sep, "/") and name not in linked:
            problems.append(f"orphan concept page: {name}")
    index = open(os.path.join(ROOT, "wiki", "index.md"), encoding="utf-8").read()
    for name in pages:
        if f"[[{name}]]" not in index:
            problems.append(f"{name} is missing from wiki/index.md")
    return report("wiki lint", problems)


# ---------- deck gates ----------

def read_cards(topic):
    """cards/<concept>.md -> {concept: [ {claim, cite, quote}, ... ]}"""
    cards = {}
    for path in sorted(glob.glob(os.path.join(topic, "cards", "*.md"))):
        items, cur = [], None
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if line.startswith("- claim:"):
                cur = {"claim": line[8:].strip()}  # start a new evidence item
                items.append(cur)
            elif cur is not None and line.strip().startswith(("cite:", "quote:")):
                key, val = line.strip().split(":", 1)
                cur[key] = val.strip()
        cards[os.path.splitext(os.path.basename(path))[0]] = items
    return cards


def check_coverage(topic):
    text = open(os.path.join(topic, "retrieval.md"), encoding="utf-8").read()
    used = text.split("## Skipped")[0]  # only count pages we actually plan to use
    found = {t for t in LINK.findall(used) if os.path.exists(os.path.join(ROOT, "wiki", "concepts", t + ".md"))}
    problems = [] if len(found) >= 3 else [f"only {len(found)} relevant wiki pages, need 3 -> stop and ingest more"]
    return report("G1 coverage", problems)


def check_cards(topic):
    problems = []
    for name, items in read_cards(topic).items():
        wiki_path = os.path.join(ROOT, "wiki", "concepts", name + ".md")
        wiki_text = open(wiki_path, encoding="utf-8").read() if os.path.exists(wiki_path) else ""
        if not wiki_text:
            problems.append(f"card {name}: no wiki page with that name")
        else:
            # a card that quietly drops points passes every quote check, so count them too
            block = re.search(r"## Key points\n(.*?)(\n## |\Z)", wiki_text, re.S)
            expected = len(CITE_QUOTE.findall(block.group(1))) if block else 0
            if len(items) != expected:
                problems.append(f"card {name}: {len(items)} items but the wiki page has {expected} key points")
        for i, it in enumerate(items, 1):
            m = CITE.search(f"[{it.get('cite', '')}]")
            if not m:
                problems.append(f"card {name} #{i}: bad cite '{it.get('cite')}'")
                continue
            # cards can't bring in new sources, the cite has to be on the wiki page already
            if f"[{it['cite']}]" not in wiki_text:
                problems.append(f"card {name} #{i}: [{it['cite']}] isn't cited in wiki/concepts/{name}.md")
            problems += quote_problems(f"card {name} #{i}", m.group(1), m.group(2), it.get("quote", ""))
    return report("G2 cards", problems)


REQUIRED_SECTIONS = ["hook", "definition", "how-it-works", "rules", "example", "pitfalls", "summary", "quiz"]


def read_outline(topic):
    """rows look like: | 03 | rules | Silent final letters | silent-letters, careful-rule |"""
    rows = []
    for line in open(os.path.join(topic, "outline.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].isdigit():
            rows.append({"n": cells[0], "section": cells[1], "title": cells[2],
                         "cards": [c.strip() for c in cells[3].split(",") if c.strip()]})
    return rows


def check_outline(topic):
    problems = []
    rows, cards = read_outline(topic), read_cards(topic)
    if not 8 <= len(rows) <= 15:
        problems.append(f"{len(rows)} slides, need 8-15")
    for s in REQUIRED_SECTIONS:
        if s not in {r["section"] for r in rows}:
            problems.append(f"teaching section missing: {s}")  # if the wiki can't cover it, go back to retrieval
    for r in rows:
        if not r["cards"]:
            problems.append(f"slide {r['n']}: no evidence card")
        for c in r["cards"]:
            if c not in cards:
                problems.append(f"slide {r['n']}: card '{c}' doesn't exist")
    return report("G3 outline", problems)


def check_slides(topic):
    problems = []
    rows, cards = {r["n"]: r for r in read_outline(topic)}, read_cards(topic)
    drafts = sorted(glob.glob(os.path.join(topic, "drafts", "*.md")))
    if len(drafts) != len(rows):
        problems.append(f"{len(drafts)} drafts but outline has {len(rows)} slides")
    for path in drafts:
        n = os.path.splitext(os.path.basename(path))[0]
        text = open(path, encoding="utf-8").read()
        row = rows.get(n)
        if row is None:
            problems.append(f"slide {n}: not in outline")
            continue
        src = re.search(r"^Sources:(.*)$", text, re.M)
        if not src or not CITE.search(src.group(1)):
            problems.append(f"slide {n}: no Sources line with citations")
            continue
        # every cite on the slide has to come from THIS slide's cards, not from memory
        allowed = {it.get("cite") for c in row["cards"] for it in cards.get(c, [])}
        for s, sec in CITE.findall(text):
            if f"{s} §{sec}" not in allowed:
                problems.append(f"slide {n}: cites [{s} §{sec}] but none of its cards ({', '.join(row['cards'])}) has it")
        # every example word needs all three: respelling, ipa and a sound button (from the interview)
        for ex in re.findall(r"^\s*-?\s*🔊(.*)$", text, re.M):
            if "≈" not in ex or not re.search(r"/[^/]+/", ex):
                problems.append(f"slide {n}: example '{ex.strip()[:30]}' needs '≈ respelling' and '/ipa/'")
        # count only the visible words: skip notes, sources and the example lines
        body = text.split("Notes:")[0]
        body = re.sub(r"^Sources:.*$", "", body, flags=re.M)
        body = re.sub(r"^\s*-?\s*🔊.*$", "", body, flags=re.M)
        words = len(re.findall(r"[A-Za-zÀ-ÿœŒ'’\-]+", body))
        if words > 60:
            problems.append(f"slide {n}: {words} words, max 60 -> shorten this slide")
    return report("G4 slides", problems)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    topic = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else ""
    fn = {"wiki": check_wiki, "coverage": lambda: check_coverage(topic), "cards": lambda: check_cards(topic),
          "outline": lambda: check_outline(topic), "slides": lambda: check_slides(topic)}.get(cmd)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    sys.exit(fn())
