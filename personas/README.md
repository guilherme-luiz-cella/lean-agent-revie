# Personas: one lens each, no overlap

The agent definitions live in `../.claude/agents/` (one file per persona, plus `scout`, which reads
for everyone, and `judge`, which checks every entry; neither is a lens).

Research: diverse lenses beat more of the same (2 diverse agents can match 16 identical ones), and
personas drift toward the same answers unless their *job and evidence* differ. So each persona below
has its own evidence source and a "do not cover" list. Keep 8-10 in the roster; pick 3-5 per round.

| Persona | Evidence it uses | Pick it when the change touches |
|---|---|---|
| design | runs the app, screenshots, keyboard, contrast | screens, layout, interaction |
| ux | timed tasks as 3-4 user types | flows, discoverability, defaults |
| structure | reads code against docs and standards | logic, threads, errors, resources |
| security | reads trust boundaries and data paths | servers, files, auth, personal data |
| deploy | reads build and install scripts, OS policies | packaging, install, update, uninstall |
| domain | the users' daily work in that field | features, data the users care about |
| kiss | measures size, argues for removal | anything that adds settings or code |
| newcomer | follows the README literally | docs, setup, first run |
| qa-mutation | breaks code on purpose, reruns tests | tests, before a release |
| repo | layout, docs drift, what ships where | folders, build output, docs |

Dropped after use: a separate "modularity" persona overlapped "structure" twice; fold boundary
questions (shared globals, API surface) into structure.
