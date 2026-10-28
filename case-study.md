# Case study: four rounds on a small local tool

The project: a local Windows tool (Python stdlib server + plain-JS viewer, ~3.5k lines) that shows a
folder as a graph. Runs on 2026-10-27/28. Every finding below was checked in the code.

## Rounds

| Round | Setup | Cost per agent | What it found |
|---|---|---|---|
| 1 | 3 plain task briefs ("stress test", "build", "editors + delete") | 47-86k tokens | A real data-loss bug (two same-name deleted items overwrote each other), from the narrowest brief |
| 2 | 5 strict personas (design, structure, modularity, folders, ux), free exploration | 87-133k | 3 blockers: private data written to a shared drive, a test that could hit the real app, a menu that never opened (found only by the persona that really clicked) |
| 3 | Same 5, after a change, ~250-word replies | 71-80k | 6 real bugs in new code; 2 found twice independently |
| 4 | 5 new personas (security, domain expert, IT, minimalist, newcomer), Sonnet, narrow file list, 150-word format | 67-80k | An auth hole (token handed out by an unauthenticated page), undocumented data locations, the domain feature users wanted most |

## What worked

- **Running the app beat reading code.** Two code readers saw only a "listener leak"; the persona that
  right-clicked saw the menu never opens.
- **Independent agreement = confidence.** When two personas found the same bug without seeing each
  other, it was always real.
- **New lenses found new things.** Round 4's security and domain personas found what five earlier
  personas missed. Diversity, not more of the same.
- **The minimalist persona** gave the clearest owner decisions (remove X, saves N lines, loses Y).

## What didn't

- **The compact format barely moved cost.** Replies shrank, but each agent still spent ~70k reading.
  The fix is the context pack (see `protocol.md`), not shorter replies.
- **A shared file with free writes broke.** One agent wrote above others and moved text. Fixed by one
  writer per file.
- **Personas can be confidently wrong** (one said no file used some globals; the test suite did).
  Every finding needs checking before acting.
- **A popular pitch failed in practice.** "Let the editor type-check the JS" got 4 signatures; tried,
  it gave 87 warnings and 0 real ones. Replaced by a 25-line script that does only the useful part.
- **Overlap.** Two personas (structure, modularity) found the same things twice; one could go.

## Numbers to plan with

- Fresh persona, free exploration: ~70-130k tokens. With a narrow file list: ~67-80k. Target with a
  context pack: ~10-15k.
- Continued persona, reply round: ~2-5k.
- Real findings per persona per round: 1-3 (after checking). More rounds on the same code find less.
