# Checks (verification)

**One line:** how a loop or graph knows work is really done, by script or by a fresh reviewer.

## Explanation
"Looks good to me" from the AI that did the work proves nothing. Program checks are
scripts with a clear pass/fail (tests, broken links, missing sources). AI review handles what
scripts can't (is it faithful to the source? is a claim reversed?), but must run in a new
conversation that only sees the output and the sources.

## Key points
- "Done" is decided by the script, not by the AI saying so [L10 p.14]
- Program checks: tests pass, no broken links, every slide has a source [L10 p.22]
- AI review: faithfulness to sources, run in a fresh conversation with only the output and sources [L10 p.22]
- Saying "check it" is not verification; write the definition of done first [L10 p.51]

## Example
```python
assert all(slide.sources for slide in deck)   # program check, no opinions involved
```

## Related
[[loop]] · [[graph]] · [[reflection]]
