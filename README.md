# Lean agent review

A way to run a board of AI review agents (personas) on a codebase while spending few tokens,
without agents repeating each other. Built from real runs on a small project and from published
research. Plain Markdown: nothing to install.

## The short version

1. **Most of the cost is reading, not talking.** A reviewer cost 67-133k tokens; over 90% was reading
   the repo. Its reply was ~150-250 words. So cut what agents read first (a shared context pack).
2. **Diversity beats headcount.** 2 agents with different lenses can match 16 identical ones. Keep a
   roster of ~8-10 distinct lenses, but let only 3-5 act per round.
3. **One chooser, one checker.** A main agent picks who acts each round, gives each a narrow brief,
   and verifies every finding against the code before it reaches you. Central checking cut error
   amplification from 17x to 4x in research; choosing who acts cut tokens 3.7-4.5x.
4. **A scout reads once for everyone.** It writes a structured pack (verbatim code, checked facts);
   reviewers read that instead of the repo: an estimated ~55-70% fewer tokens (not yet measured), at
   the cost of one extra step.
5. **A shared board, one writer per file.** Agents write only their own file; the main agent writes the
   index. No overwrites, and newcomers read short digests instead of everything.
6. **A compact language (FGL)** for findings and votes: easy to pass around and to check. It halves
   the reply, but replies are a small part of the cost; it barely moved the total (`case-study.md`).
7. **A judge checks every entry** against the code with a fixed rubric, on a different model than the
   reviewers. **No repeating** (co-sign instead), and **debate**: anyone may contradict the owner or a
   peer, with proof.

## Files

| File | What it is |
|---|---|
| `protocol.md` | How a round runs: roles, board layout, the FGL card, rules |
| `research.md` | What the research says, with numbers and links |
| `knowledge.md` | Terse knowledge base: AI on code, token usage, handoffs, multi-agent; tagged by source strength |
| `case-study.md` | Four real rounds: cost, findings, what worked and what didn't |
| `.claude/agents/` | 10 reviewer personas + the scout + the judge, as Claude Code agent types (own model, own tools) |
| `personas/README.md` | The lens table: which persona to pick for which change |
| `templates/` | The context pack, an agent brief and the board index, ready to copy |
| `CLAUDE.md` + `.claude/hooks/confine.py` | Keeps Claude and every board agent inside the repo (no other drives, shares or AppData); `tests/confine_test.py` proves it |

## How to use it (Claude Code or any agent tool)

1. Copy `.claude/agents/`, `templates/` and `protocol.md` into your repo. Claude Code then offers each
   persona as its own agent type (`security`, `design`, ...) instead of a general-purpose agent.
2. Pick 3-5 personas whose lens fits the change (see the lens table in `personas/README.md`).
3. Run `scout` first: it reads the repo once and writes `board/pack.md`.
4. Start the chosen personas with the round number and what changed; they read the pack.
5. Run `judge`: it checks every entry in the code and writes `board/R<n>/judge.md`.
   Spot-check it, write `INDEX.md` and decide.
6. For replies, continue the same agents (they keep what they read) instead of starting new ones.
