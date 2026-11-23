# report.md — run log for topic-pronunciation

Each line: time · node/gate · result · next. Gates are scripts (pipeline/check.py, pipeline/render_check.js).
G0 (wiki lint at ingest) history is in wiki/log.md.

- 19:34 · N1 retrieve · 12 relevant, 2 skipped · G1 coverage PASS (12 ≥ 3) · → N2
- 19:34 · N2 cards (round 1) · bug: every card had only 1 item (regex without re.M) · G2 PASSED anyway, because it only checked that quotes were real, not that cards were complete
- 19:34 · fix · G2 now also checks card item count = wiki key point count; rerun G2 on the buggy cards to prove the new check catches it:
- 19:35 · G2 cards (round 2) · new check FAIL 12/12 on the buggy cards (proves it works) → N2 rerun: 57 items → PASS. Quote failures at G2: 0 (practice run: 6/31), because quotes were already checked at ingest (G0)
- 19:35 · N3 outline · 15 slides · G3 PASS · → H
- 19:35 · H human check · deferred: Angelie reviews the finished deck (asked for a full run tonight)
- 19:36 · N4 drafts · 15 slides · G4 PASS first try · gate tested on 3 planted errors (missing respelling, cite not in cards, 84 words): all 3 caught → trust the PASS
- 19:37 · N5 render · deck.html, 15 slides, words copied from drafts only · G5 render PASS (desktop 1280×720 + phone 390×844: no overflow, arrow-key nav works, every slide has source links, 🔊 buttons = examples) · visual check of slides 01/03/07/10 OK
- 19:37 · N6 AI review · PENDING: review-packet.md prepared (slides + cited wiki pages only). Must run in a NEW chat (Lecture 10 p.22), not by the AI that wrote the deck → Angelie runs it, result goes in review.md
- 20:55 · H human check (Angelie, on the rendered deck) · slide 15 answers ran together on one line → N5 render fix only (answers split into a numbered list, same words) · G5 rerun PASS. Links to GitHub 404 until the repo is pushed (expected)
- 21:20 · G5 extended · new test: click 🔊 in a browser with no French voice (headless Chromium has 0 voices). Old deck: FAIL, "🔊 clicked with no french voice ... but no warning shown (silent button)". The warning only showed when *some other* voice existed, so with zero voices the button did nothing and said nothing. The old G5 passed because it only counted buttons
- 21:22 · N5 render fix · warning now shows whenever there's no French voice; Home/End keys added; new pastel "travel postcard" theme (layout only, same words) · G4 PASS (unchanged drafts) · G5 PASS incl. the new 🔊 test · visual check desktop/dark/phone: phone footer overlapped scrolling examples → fixed → OK
- 21:25 · N5 render · layout only: light theme always (no dark mode), background bright butter-cream #FFF5D6 · G5 PASS
- 21:28 · N6 AI review · ChatGPT in a fresh chat (packet only: slides + cited wiki pages) · **FIX, 11/15 PASS** · flagged: 07 (calls the 3-or-4 nasal count a "disagreement", but the wiki reconciles it: standard French has up to 4, Paris speakers merge un/in), 10 (liaison sounded automatic; H-word exception missing), 13 ("parlent ends in l" mixes spelling and sound), 14 (listed CaReFuL among *silent* endings; liaison sounded automatic) → big loop N6 → N4
- 21:35 · N4 redraft · ONLY slides 07, 10, 13, 14, from their own cards (H-word point + S3 "certain contexts" were already in the liaison card, just not used) · G4 PASS · N5 render · G5 PASS
- 21:35 · N6 not re-run: the 4 fixes copy the reviewer's own suggestions word-for-word in meaning; coverage notes (ch/qu/th, schwa conditions, singular nouns) left for a future version, since slides are at the 60-word limit
- 21:40 · N5 render · layout only: slide 10's source footer was cut off with "…" (2 sources hidden) → footer now wraps · G5 PASS
- 21:45 · H human check · listened to 🔊 on slides 3, 7, 12 on my Mac (Safari, French voice): all sound ok
