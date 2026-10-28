# Claude Code in this repo

**Read and write only inside this repository.** Never open, list or search anything outside it: not
other drives or network shares, not the user's Documents, not AppData. This holds for you and for every
board agent you start. `.claude/hooks/confine.py` blocks file tools outside the repo and commands that
mention other drives, shares or AppData; if it blocks something you think is needed, ask the user,
never retry another way.

This repo is a method (protocol, research, personas), not a product: it holds no personal data, and
must never get any. Examples use invented names only.

Start with `README.md`, then `protocol.md`. Persona agents are in `.claude/agents/`.
Test the guard: `python tests/confine_test.py`.
