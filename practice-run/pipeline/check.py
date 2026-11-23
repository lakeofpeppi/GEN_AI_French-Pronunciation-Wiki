"""program checks for the wiki and the deck graph.

usage:
  python3 pipeline/check.py wiki                  # lint the whole wiki
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
SOURCES = ["L07", "L08", "L09", "L10", "TA07"]

# matches things like [L10 p.21] or [TA07 p.5], the two groups are the source id and page
CITE = re.compile(r"\[(L07|L08|L09|L10|TA07) p\.(\d+)\]")
# matches wiki links like [[tool-use]]
LINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")


def raw_page(src, page):
    """text of one slide, or None if we don't have that page."""
    path = os.path.join(ROOT, "raw", "text", src, f"p{int(page):02d}.txt")
    if not os.path.exists(path):
        return None
    return open(path, encoding="utf-8").read()


def squash(text):
    # pdf text has random spaces and line breaks, so drop all whitespace before comparing
    return re.sub(r"\s+", "", text)


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
        name = os.path.splitext(os.path.basename(path))[0]
        pages[name] = (path, open(path, encoding="utf-8").read())

    # only sources that wiki/log.md says were ingested can be cited
    log = open(os.path.join(ROOT, "wiki", "log.md"), encoding="utf-8").read()
    ingested = set(re.findall(r"\| ingest \| (L07|L08|L09|L10|TA07) \|", log))

    linked = set()
    for name, (path, text) in pages.items():
        rel = os.path.relpath(path, ROOT)
        # every cite has to point at a slide we actually have
        for src, page in CITE.findall(text):
            if raw_page(src, page) is None:
                problems.append(f"{rel}: cites [{src} p.{page}] but that page doesn't exist")
            elif src not in ingested:
                # this catches citing a lecture from memory before we actually read it in
                problems.append(f"{rel}: cites [{src} p.{page}] but {src} hasn't been ingested yet")
        # every [[link]] has to point at a real page
        for target in LINK.findall(text):
            linked.add(target)
            if target not in pages:
                problems.append(f"{rel}: broken link [[{target}]]")
        # bullets under "key points" must each end with a citation
        section = re.search(r"## Key points\n(.*?)(\n## |\Z)", text, re.S)
        if section:
            for line in section.group(1).splitlines():
                if line.startswith("- ") and not CITE.search(line):
                    problems.append(f"{rel}: key point without citation -> {line[:60]}")

    # a concept nobody links to is an orphan, the wiki can't reach it
    for name, (path, _) in pages.items():
        if "/concepts/" in path.replace(os.sep, "/") and name not in linked:
            problems.append(f"orphan concept page: {name}")

    index = open(os.path.join(ROOT, "wiki", "index.md"), encoding="utf-8").read()
    for name in pages:
        if f"[[{name}]]" not in index:
            problems.append(f"{name} is missing from wiki/index.md")
    return report("wiki lint", problems)


# ---------- deck gates ----------

def read_cards(topic):
    """cards/<name>.md -> {name: [ {claim, cite, quote}, ... ]}"""
    cards = {}
    for path in sorted(glob.glob(os.path.join(topic, "cards", "*.md"))):
        name = os.path.splitext(os.path.basename(path))[0]
        items, cur = [], None
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if line.startswith("- claim:"):
                cur = {"claim": line[8:].strip()}  # start a new evidence item
                items.append(cur)
            elif cur is not None and line.strip().startswith("cite:"):
                cur["cite"] = line.split("cite:", 1)[1].strip()
            elif cur is not None and line.strip().startswith("quote:"):
                cur["quote"] = line.split("quote:", 1)[1].strip()
        cards[name] = items
    return cards


def check_coverage(topic):
    text = open(os.path.join(topic, "retrieval.md"), encoding="utf-8").read()
    found = [t for t in LINK.findall(text) if os.path.exists(os.path.join(ROOT, "wiki", "concepts", t + ".md"))]
    problems = [] if len(set(found)) >= 3 else [f"only {len(set(found))} relevant wiki pages, need at least 3 -> stop and ingest more"]
    return report("G1 coverage", problems)


def check_cards(topic):
    problems = []
    for name, items in read_cards(topic).items():
        wiki_path = os.path.join(ROOT, "wiki", "concepts", name + ".md")
        wiki_text = open(wiki_path, encoding="utf-8").read() if os.path.exists(wiki_path) else ""
        if not items:
            problems.append(f"card {name}: empty")
        for i, it in enumerate(items, 1):
            m = CITE.search(f"[{it.get('cite', '')}]")
            if not m:
                problems.append(f"card {name} #{i}: bad cite '{it.get('cite')}'")
                continue
            page = raw_page(*m.groups())
            # the cite must also be in the wiki page, cards can't bring in new sources
            if f"[{it['cite']}]" not in wiki_text:
                problems.append(f"card {name} #{i}: [{it['cite']}] is not cited in wiki/concepts/{name}.md")
            # tiny quotes like "初稿" match almost anything, so they prove nothing
            if len(squash(it.get("quote", ""))) < 6:
                problems.append(f"card {name} #{i}: quote '{it.get('quote')}' is too short to be evidence (min 6 chars)")
            # this is the real faithfulness test: the quote has to literally be on that slide
            elif page is None or squash(it.get("quote", "")) not in squash(page):
                problems.append(f"card {name} #{i}: quote '{it.get('quote')}' not found on [{it['cite']}]")
    return report("G2 cards", problems)


REQUIRED_SECTIONS = ["hook", "definition", "how-it-works", "patterns", "example", "reliability", "summary", "quiz"]


def read_outline(topic):
    """outline rows look like: | 03 | definition | AI agent = model + harness | ai-agent, harness |"""
    rows = []
    for line in open(os.path.join(topic, "outline.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].isdigit():
            rows.append({"n": cells[0], "section": cells[1], "title": cells[2],
                         "cards": [c.strip() for c in cells[3].split(",") if c.strip()]})
    return rows


def check_outline(topic):
    problems = []
    rows = read_outline(topic)
    cards = read_cards(topic)
    if not 8 <= len(rows) <= 15:
        problems.append(f"{len(rows)} slides, need 8-15")
    sections = {r["section"] for r in rows}
    for s in REQUIRED_SECTIONS:
        if s not in sections:
            problems.append(f"teaching section missing: {s}")  # this one sends us back to retrieval if the wiki lacks it
    for r in rows:
        if not r["cards"]:
            problems.append(f"slide {r['n']}: no evidence card")
        for c in r["cards"]:
            if c not in cards:
                problems.append(f"slide {r['n']}: card '{c}' doesn't exist")
    return report("G3 outline", problems)


def check_slides(topic):
    problems = []
    rows = {r["n"]: r for r in read_outline(topic)}
    cards = read_cards(topic)
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
        # every cite on the slide must come from THIS slide's cards, not from memory
        allowed = {it.get("cite") for c in row["cards"] for it in cards.get(c, [])}
        for s, p in CITE.findall(text):
            if f"{s} p.{p}" not in allowed:
                problems.append(f"slide {n}: cites [{s} p.{p}] which none of its cards ({', '.join(row['cards'])}) has")
        # count words in the visible part only (skip the notes and the sources line)
        body = text.split("Notes:")[0]
        body = re.sub(r"^Sources:.*$", "", body, flags=re.M)
        body = re.sub(r"```.*?```", "", body, flags=re.S)  # code blocks don't count, they're examples
        words = len(re.findall(r"[A-Za-z0-9'’\-]+", body))
        if words > 60:
            problems.append(f"slide {n}: {words} words, max 60 -> shorten this slide")
    return report("G4 slides", problems)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    topic = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else ""
    fn = {"wiki": lambda: check_wiki(), "coverage": lambda: check_coverage(topic),
          "cards": lambda: check_cards(topic), "outline": lambda: check_outline(topic),
          "slides": lambda: check_slides(topic)}.get(cmd)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    sys.exit(fn())
