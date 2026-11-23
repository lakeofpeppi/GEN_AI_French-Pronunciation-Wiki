# workflow: topic → teaching HTML deck (graph)

Based on Lecture 10 p.43–47. The **graph** decides the order of nodes; small **loops**
live inside nodes. Every gate is a **script** in `pipeline/`. Every node writes a
**file** into `topic-<name>/`, so each stage can be opened, committed and re-run alone.

```
 [N1 retrieve wiki] ──► (G1 coverage gate) ──fail: < 3 pages──► STOP, ingest more
          ▲                     │ pass
          │                     ▼
          │            [N2 evidence cards] ◄──────────────┐
          │                     │                         │ fail: re-extract that card
          │                     ▼                         │
          │              (G2 card check) ─────────────────┘
          │                     │ pass
          │                     ▼
          │               [N3 outline] ◄──────────────────┐
          │                     │                         │ fail: fix outline
          └── missing topic ── (G3 outline check) ────────┘
                                │ pass
                                ▼
                        {H  human looks at outline}
                                │
                                ▼
                     [N4 draft each slide] ◄──────────────┐
                                │                         │ fail: redraft ONLY that slide
                                ▼                         │ (max 2 rounds per slide)
                        (G4 slide check) ─────────────────┘
                                │ pass
                                ▼
                       [N5 render HTML] ◄─────────────────┐
                                │                         │ fail: fix layout only
                                ▼                         │
                       (G5 render check) ─────────────────┘
                                │ pass
                                ▼
                    [N6 AI review, fresh context] ── fail: back to N4 for listed slides
                                │ pass
                                ▼
                         deliver + report.md
```

## Nodes: what each one may see and change (Lecture 10 p.44)

| Node | Reads | Writes | Must not |
|---|---|---|---|
| N1 retrieve | `wiki/index.md`, concept pages | `retrieval.md` | read `raw/` |
| N2 evidence cards | ONE wiki page + the raw pages it cites | `cards/<concept>.md` | mix sources |
| N3 outline | cards | `outline.md` | add facts not in a card |
| N4 draft | the outline row + its cards | `drafts/NN.md` | touch other slides |
| N5 render | passed drafts | `deck.html` | change any words |
| N6 review | `deck.html` + cited wiki pages only | `review.md` | see the drafting chat |

## Gates (scripts)

| Gate | Command | Passes when |
|---|---|---|
| G1 | `check.py coverage` | ≥ 3 relevant wiki pages |
| G2 | `check.py cards` | every card quote is really on the cited raw page; the cite also appears in the wiki page |
| G3 | `check.py outline` | 8–15 slides; teaching sections present; every slide uses ≥ 1 existing card |
| G4 | `check.py slides` | every slide has a Sources line; its citations come from its own cards; ≤ 60 words |
| G5 | `node render_check.js` | slide count matches, no text overflows, every slide shows its source |

## Five things this loop defines (Lecture 10 p.21–22)

- **Goal:** a deck that teaches CS students what an AI agent is and how loops/graphs make it reliable.
- **Limits:** wiki only; English; 8–15 slides.
- **Done:** G1–G5 pass and N6 finds no unfaithful slide.
- **Stop:** 3 rounds max per loop; < 3 relevant pages → stop before drafting.
- **Trigger:** I ask for a deck on a topic (`/topic-slides <topic>`).

## Which parts repeat

- **Small loops (fast, frequent):** G2 → N2 for one card, G4 → N4 for one slide, G5 → N5 for layout.
- **Big loops (should be rare):** G3 → N1 (missing topic), N6 → N4 (unfaithful slide).
  If a big loop keeps happening, the check belongs earlier (Lecture 10 p.26).
