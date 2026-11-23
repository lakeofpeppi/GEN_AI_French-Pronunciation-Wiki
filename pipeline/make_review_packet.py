"""prepares node N6: a packet for an AI reviewer in a NEW chat.

the reviewer gets only the finished slides and the wiki pages they cite, nothing from the
chat that wrote them (lecture 10 p.22: don't let the writer grade its own work).
usage: python3 pipeline/make_review_packet.py topic-pronunciation
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
topic = os.path.abspath(sys.argv[1])
rows = {}
for line in open(os.path.join(topic, "outline.md"), encoding="utf-8"):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 4 and cells[0].isdigit():
        rows[cells[0]] = [c.strip() for c in cells[3].split(",")]

parts = [open(os.path.join(ROOT, "pipeline", "review_prompt.md"), encoding="utf-8").read(), "\n# THE SLIDES\n"]
used = []
for path in sorted(glob.glob(os.path.join(topic, "drafts", "*.md"))):
    n = os.path.basename(path)[:2]
    text = open(path, encoding="utf-8").read().split("Notes:")[0].strip()  # teacher notes aren't shown to students, skip them
    parts.append(f"\n## Slide {n}  (wiki pages: {', '.join(rows[n])})\n{text}\n")
    used += [c for c in rows[n] if c not in used]
parts.append("\n# THE WIKI PAGES (the only allowed knowledge source)\n")
for c in used:
    parts.append("\n---\n" + open(os.path.join(ROOT, "wiki", "concepts", c + ".md"), encoding="utf-8").read())
open(os.path.join(topic, "review-packet.md"), "w", encoding="utf-8").write("".join(parts))
print(f"packet: {len(rows)} slides, {len(used)} wiki pages")
