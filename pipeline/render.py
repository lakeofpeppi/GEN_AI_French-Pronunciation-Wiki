"""node N5: turn the checked drafts into one self-contained deck.html.

layout only: every word on a slide comes from drafts/NN.md, this script never writes content.
usage: python3 pipeline/render.py topic-pronunciation
"""
import html
import os
import re
import sys
import glob

topic = os.path.abspath(sys.argv[1])

# short names for the footer, so beginners see where each slide came from
SOURCES = {
    "S1": ("Les bases du français 101 (open textbook)", "https://pressbooks.pub/introductiontofrench1/?p=1416"),
    "S2": ("Duolingo: how French letters sound", "https://blog.duolingo.com/how-to-pronounce-french"),
    "S3": ("Wikipedia: French phonology", "https://en.wikipedia.org/wiki/French_phonology"),
    "S4": ("Wikipedia: Help:IPA/French", "https://en.wikipedia.org/wiki/Help:IPA/French"),
    "S5": ("Wikipedia: French orthography", "https://en.wikipedia.org/wiki/French_orthography"),
    "S6": ("Wikipedia: Liaison (French)", "https://en.wikipedia.org/wiki/Liaison_(French)"),
}


def inline(text):
    """escape first, then turn **bold** and `code` into tags."""
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    # ⚠ is just a marker in the drafts, on the slide it becomes a text label (no emoji on screen)
    return re.sub(r"⚠\s*", '<span class="warn">Heads up</span> ', t)


def render_slide(n, text, total):
    title, items, examples, notes, answers, sources, lead = "", [], [], "", "", "", []
    kind = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            title = s[2:]
        elif s.startswith("🔊"):
            # split "🔊 word ≈ respelling /ipa/" into its three parts
            m = re.match(r"🔊\s*(.+?)\s*≈\s*(.+?)\s*(/[^/]+/)\s*$", s)
            examples.append(m.groups() if m else (s[1:], "", ""))
        elif s.startswith("- "):
            items.append(s[2:]); kind = kind or "ul"
        elif re.match(r"^\d+\. ", s):
            items.append(re.sub(r"^\d+\. ", "", s)); kind = kind or "ol"
        elif s.startswith("Notes:"):
            notes = s[6:].strip()
        elif s.startswith("Answers:"):
            answers = s[8:].strip()
        elif s.startswith("Sources:"):
            sources = s
        elif s:
            lead.append(s)

    out = [f'<section class="slide" data-n="{n}">', f'<p class="count">{n:02d} / {total:02d}</p>',
           f'<div class="title-wrap"><h2>{inline(title)}</h2></div>']  # wrapper so the highlighter follows each line of the title
    out += [f'<p class="lead">{inline(x)}</p>' for x in lead]
    if items:
        out.append(f"<{kind}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{kind}>")
    if examples:
        rows = []
        for word, resp, ipa in examples:
            # the button only needs the french text, data-say keeps it out of the visible layout logic
            rows.append(f'<div class="ex"><button class="say" data-say="{html.escape(word)}" aria-label="hear {html.escape(word)}">🔊</button>'
                        f'<span class="fr">{html.escape(word)}</span><span class="resp">≈ {html.escape(resp)}</span>'
                        f'<span class="ipa">{html.escape(ipa)}</span></div>')
        out.append('<div class="examples">' + "".join(rows) + "</div>")
    if answers:
        # answers come as "1. x · 2. y" on one line, show each one on its own row (layout only, same words)
        parts = [re.sub(r"^\d+\.\s*", "", a.strip()) for a in answers.split("·") if a.strip()]
        items_html = "".join(f"<li>{inline(a)}</li>" for a in parts)
        out.append(f'<details class="answers"><summary>Show answers</summary><ol>{items_html}</ol></details>')
    if notes:
        out.append(f'<aside class="notes"><b>Teacher notes:</b> {inline(notes)}</aside>')
    cites = re.findall(r"\[(S[1-6]) §([^\]]+)\]", sources)
    links = []
    for sid, sec in cites:
        name, url = SOURCES[sid]
        links.append(f'<a href="{url}" target="_blank" rel="noopener" title="{html.escape(name)}">{sid} §{html.escape(sec)}</a>')
    out.append('<footer class="src">Sources: ' + " · ".join(links) + "</footer></section>")
    return "\n".join(out)


drafts = sorted(glob.glob(os.path.join(topic, "drafts", "*.md")))
slides = "\n".join(render_slide(i + 1, open(p, encoding="utf-8").read(), len(drafts)) for i, p in enumerate(drafts))
legend = "".join(f'<li><b>{k}</b> <a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a></li>' for k, (n, u) in SOURCES.items())

page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_template.html"), encoding="utf-8").read()
page = page.replace("{{SLIDES}}", slides).replace("{{LEGEND}}", legend)
open(os.path.join(topic, "deck.html"), "w", encoding="utf-8").write(page)
print(f"rendered {len(drafts)} slides -> {os.path.relpath(os.path.join(topic, 'deck.html'))}")
