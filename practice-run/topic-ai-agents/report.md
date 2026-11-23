# report.md — run log for topic-ai-agents

Each line: time · node/gate · result · what happened next. Gates are scripts (pipeline/check.py).

- 18:56 · N1 retrieve · 13 relevant pages, 3 skipped · → G1
- 18:56 · G1 coverage · PASS (13 ≥ 3) · → N2
- 18:56 · N2 evidence cards · 13 cards, 31 quotes written · → G2
- 18:56 · G2 cards (round 1) · FAIL 6/31: quotes not on cited page. cause: PDF text layer pulls some characters (一 二 生 行 方 工 用) out of place, e.g. slide shows 第一個 LLM 產生初稿, text has 第 個 LLM 產 初稿 · → N2 re-extract only those 6 quotes
- 18:56 · G2 cards (round 2) · PASS, but the reflection quote had been cut down to 初稿 (2 chars), which proves nothing. Check was too easy to satisfy → added a min 6-character rule to G2 · → rerun
- 18:56 · G2 cards (round 3) · FAIL 5 too-short quotes → re-extracted longer contiguous quotes → PASS (31/31). Hit the 3-round limit exactly; next time this check should happen earlier (see reflection)
- 18:57 · N3 outline · 14 slides, teaching arc hook→quiz · → G3
- 18:57 · G3 outline · PASS (14 slides, all 8 teaching sections, every slide has cards) · → H
- 18:57 · H human check · SKIPPED this run (Angelie asked for a full automatic run; she reviews the finished deck instead) · → N4
