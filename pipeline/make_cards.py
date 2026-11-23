"""node N2: one evidence card per relevant wiki page, copied from its checked key points.

usage: python3 pipeline/make_cards.py topic-pronunciation
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
topic = os.path.abspath(sys.argv[1])
POINT = re.compile(r"^- (.*?)\s*\[(S[1-6]) §([^\]]+)\]\s*«([^»]+)»", re.M)  # re.M or ^ only matches the very first line, that was the bug

retrieval = open(os.path.join(topic, "retrieval.md"), encoding="utf-8").read()
wanted = re.findall(r"\[\[([a-z0-9-]+)\]\]", retrieval.split("## Skipped")[0])  # skipped pages don't get cards

for name in wanted:
    text = open(os.path.join(ROOT, "wiki", "concepts", name + ".md"), encoding="utf-8").read()
    block = re.search(r"## Key points\n(.*?)(\n## |\Z)", text, re.S).group(1)
    lines = [f"# card: {name}   (copied from wiki/concepts/{name}.md, this node may only see that page)"]
    for claim, src, sec, quote in POINT.findall(block):
        lines += [f"- claim: {claim}", f"  cite: {src} §{sec}", f"  quote: {quote}"]
    open(os.path.join(topic, "cards", name + ".md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{name}: {len(lines) // 3} items")
