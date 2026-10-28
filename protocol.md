# Protocol

## Roles

- **Owner:** decides. Nothing is applied without a yes.
- **Main agent (chooser + checker):** picks 3-5 personas per round, briefs them, checks every finding
  against the code, writes the index and a plain-words summary.
- **Scout:** reads the repo once per round and writes `pack.md` (structured: verbatim code excerpts
  with file:line and checked facts, no prose summaries). Reviewers wait for it.
- **Personas:** one lens each, report only (never edit code), write only their own board file.

## Board layout

```
board/
  pack.md          context for the round (main agent): repo map, excerpts, open questions, FGL card
  INDEX.md         one line per entry, <= 20 tokens, with an address (main agent only)
  R1/security.md   one file per persona per round, in FGL (that persona only)
  decisions.md     the owner's decisions (main agent)
```

## A round

1. **Choose.** Pick 3-5 personas whose lens fits the change. Skip the rest this round.
2. **Scout.** Run the scout with the change and the chosen personas; it writes `pack.md` (< 8k tokens).
   Reviewers start only when it's done.
3. **Brief.** Each persona gets `templates/brief.md`: its lens, its "do not cover" list, the pack, at
   most 2 extra files it may open, the output format. A mid-size model is enough.
4. **Write.** Each persona writes `R<n>/<name>.md` in FGL, max 6 lines.
5. **Check.** The main agent verifies each finding in the code. False ones are marked, not deleted.
   Findings two personas reached independently get high confidence.
6. **Index.** One line per entry in `INDEX.md`, plus a plain-words summary for the owner.
7. **Reply round (optional).** Continue the same personas (they keep what they read); each sees only
   the INDEX lines of 2-3 peers. Use a small model. Costs ~1-5k tokens per persona.

## FGL (compact finding language)

ASCII only (other symbols cost more tokens). One line per item, max 6 lines, sign last.

| Code | Means |
|---|---|
| `F!!` `F!` `F.` | finding: blocker / major / minor |
| `P<n>` | pitch to the owner |
| `+P7` `-P3` `~P9:cond` | vote for / against / for with a condition |
| `^R4/it#F2` | agree with that item (co-sign) |
| `xR4/kiss#K1:why` | disagree with that item |
| `K<n>` | removal proposal |
| `=` | area checked, no finding |
| `->` | fix |
| `~N` | about N lines of code |
| `?` | unsure, needs a real test |

Files get short aliases in the pack (for example `A` = app.py, `R` = README.md). Line: `A:310`.

```
F! A:310 GET/ serves token without auth -> one-time key in launch link ~15
+P9:keep table+test
^R4/it#F3
-- security
```

## Rules

- Report only. Never edit code or other personas' files.
- Point to file:line. No finding without evidence; say `=` when an area is fine.
- Stay in your lens. If you see something in another lens, one line `Q:` for the main agent.
- Personas may contest the owner's rules in one `P<n>` line; the owner decides.
- The main agent never relays a finding it hasn't checked.
