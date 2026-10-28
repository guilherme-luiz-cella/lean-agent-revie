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
   reviewers read that instead of the repo: ~55-70% fewer tokens, at the cost of one extra step.
5. **A shared board, one writer per file.** Agents write only their own file; the main agent writes the
   index. No overwrites, and newcomers read short digests instead of everything.
6. **A compact language (FGL)** for findings and votes: about half the words, easy to pass around.

## Files

| File | What it is |
|---|---|
| `protocol.md` | How a round runs: roles, board layout, the FGL card, rules |
| `research.md` | What the research says, with numbers and links |
| `case-study.md` | Four real rounds: cost, findings, what worked and what didn't |
| `.claude/agents/` | 10 reviewer personas + the scout, as Claude Code agent types (own model, own tools) |
| `personas/README.md` | The lens table: which persona to pick for which change |
| `templates/` | The context pack, an agent brief and the board index, ready to copy |

## How to use it (Claude Code or any agent tool)

1. Copy `.claude/agents/`, `templates/` and `protocol.md` into your repo. Claude Code then offers each
   persona as its own agent type (`security`, `design`, ...) instead of a general-purpose agent.
2. Pick 3-5 personas whose lens fits the change (see the lens table in `personas/README.md`).
3. Run `scout` first: it reads the repo once and writes `board/pack.md`.
4. Start the chosen personas with the round number and what changed; they read the pack.
5. Read their files, check each finding in the code, write `INDEX.md` and decide.
6. For replies, continue the same agents (they keep what they read) instead of starting new ones.
