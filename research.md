# What the research says

Collected 2026-10-28. Numbers are from the linked sources; our own measurements are in `case-study.md`.

## 1. How many agents

- **Diversity, not count.** Identical agents (same model, prompt, setup) saturate fast: extra ones add
  correlated, redundant answers. "2 diverse agents can match or exceed the performance of 16
  homogeneous agents" across seven benchmarks. What matters is the number of *effective channels*
  (non-redundant reasoning paths). [Understanding Agent Scaling via Diversity](https://arxiv.org/html/2602.03794v1)
- **No universal best size; fit matters more.** 180 configurations: "architecture-task alignment, not
  number of agents, determines collaborative success". Multi-agent setups hurt sequential planning
  (-39% to -70%) and give diminishing or negative returns once one agent already does well (~45%+
  accuracy). [Towards a Science of Scaling Agent Systems](https://arxiv.org/html/2512.08296v1)
- **Keep fan-out small.** Practice reports: teams of ~3-4 agents, fan-out capped at 3-5, overflow run
  in sequence. [Zylos: token-efficient multi-agent communication](https://zylos.ai/research/2026-06-05-token-efficient-multi-agent-communication/)
- **Personas collapse.** LLM personas cluster into a few kinds of answers; "sampling more personas cannot
  mitigate the collapse". So give each agent a different *job and evidence* (files, tools, running the
  app), not just a different character. [The Chameleon's Limit](https://www.alphaxiv.org/abs/2604.24698)

**Rule we use:** roster of 8-10 distinct lenses; 3-5 act per round, chosen for the change; each lens
has a "do not cover" list so two agents never review the same thing.

## 2. Who checks the work

- **Central checking.** Independent agents amplified errors 17.2x over one agent; with an orchestrator
  validating outputs before merging, 4.4x. [Towards a Science of Scaling Agent Systems](https://arxiv.org/html/2512.08296v1)
- **A chooser saves the most.** In a blackboard system, an LLM control unit picks which agents act
  each round. Removing it raised tokens 3.7-4.5x (MMLU 5.07M to 18.83M, GPQA 2.98M to 13.33M) for about
  the same accuracy. [LbMAS, arXiv 2507.01701](https://arxiv.org/pdf/2507.01701)

## 3. How they communicate

- **Shared board (blackboard).** Agents talk only through a shared space; it replaces each agent's own
  memory. On MATH the blackboard system scored highest (72.6%) and used fewer tokens than 5 of 6
  compared systems. [LbMAS](https://arxiv.org/pdf/2507.01701)
- **Digests first, details on demand.** Each entry has a digest of at most 200 tokens; agents pass
  addresses instead of copies and open only what they need. A fresh agent's cost stayed flat at ~2.7k
  tokens for boards of 10k to 887k tokens. [blackboard context store](https://github.com/TapanManu/blackboard)
- **Sparse topology.** In debate rounds, each agent seeing only some peers cut input tokens 9-53%
  with equal or better accuracy (best around 2 of 5 peers). [Sparse Communication Topology, arXiv 2406.11776](https://arxiv.org/html/2406.11776v1)
- **Shared memory vs messages.** Shared memory risks conflicting writes; fix with one writer per file
  or a single moderator. Messages avoid that but fragment context. Common choice: a hybrid.
  [Shared memory vs message passing](https://blckalpaca.at/en/knowledge-base/ai-agents/multi-agent-systems-fundamentals/shared-memory-vs-message-passing)

## 4. A scout that reads for everyone (is it worth it?)

Idea: one agent reads the repo once and writes a context pack; the reviewers wait for it and read only
the pack. Slower (one extra step), fewer tokens. What the evidence says:

- **Yes on tokens.** Anthropic's research system has subagents "condense their most important findings"
  before returning, and pass references instead of copies. In our runs >90% of each reviewer's cost
  was reading the repo. Estimate: 10 reviewers x ~70k = ~700k, vs a scout ~100k + 10 x ~12k = ~220k
  (about 70% less); with 5 reviewers ~350k vs ~160k (about 55% less).
  [Anthropic multi-agent research system, via ZenML](https://zenml.io/llmops-database/building-production-multi-agent-research-systems-with-claude)
- **But summaries lose details.** In a two-agent relay, a narrative summary kept the task feasible only
  0.48 of the time, uncompressed 0.88, structured JSON 0.96. "Small omissions can break strict
  constraints." [State Compression in Two-Agent LLM Relays](https://www.alphaxiv.org/abs/2607.18265)
  Compression cut 26-54% of tokens while performance "largely" held, but with "no guarantee" key
  details survive. [ACON, arXiv 2510.00615](https://arxiv.org/html/2510.00615v1)
- **And tokens buy quality.** On BrowseComp, token usage alone explained 80% of performance variance.
  Cutting reading everywhere can cut findings too. [same ZenML source]
- **Independence matters for review.** Our best catches came from evidence a scout can't pass on: the
  persona that really clicked found the broken menu that code readers missed.

**Verdict:** worth it, with three conditions: (1) the scout writes a *structured* pack with verbatim
code excerpts and checked facts, never prose summaries of code; (2) each reviewer may still open up to
2 files to verify; (3) personas whose evidence is running things (design, qa-mutation) still run the
app or tests themselves. See `.claude/agents/scout.md`.

## 5. Spending fewer tokens

| Technique | Reported saving | Source |
|---|---|---|
| Send each agent only the context it needs | 60-80% of the handoff | Zylos |
| Prompt caching of a stable shared prefix | 41-90% on cached parts | Zylos |
| Typed / structured messages instead of prose | 10-30% | Zylos |
| Smaller model for simple steps | 50-83% | Zylos |
| Drop redundant agents and links each round | ~20% | Zylos (AgentDropout) |
| Forked sub-agents sharing the parent's cache | ~90% on the shared prefix | [finisky](https://finisky.github.io/en/claude-code-fork-cache/) |

Forks share the parent's view, so they are cheap but not independent: good for parallel work, poor for
review, where independent eyes are the point.

## 6. Open questions, second pass (2026-10-28)

What we had not checked: is the scout's saving real, are reply rounds worth it, does a cheaper model
save what the price says, and how often do review findings turn out false.

- **A digest pass saves about what we estimated, quality unmeasured.** Five reviewers on one 16k-token
  diff: naive 80k input tokens ($1.32); a "librarian" pass writing a JSON digest first, 21k ($0.49);
  caching the diff as a shared system prefix, $0.45, but only on a warm series (cold: $1.32 again).
  The author did not check whether the digest lost findings. Single PR.
  [Stop paying for the same tokens twice](https://dev.to/andreagriffiths11/stop-paying-for-the-same-tokens-twice-geh)
- **Cost is prefix x turns, not just files read.** 24 reviewers on a 28-file PR: a purpose-built agent
  type with a small tool allowlist cut each reviewer's prefix from ~81k to ~23k tokens (unused skill
  catalogs and tool schemas), total cost -45%. A cheaper model, priced 2.5x lower, saved 9%: it took
  ~2.2x the turns. A newer model cost 2.7x but caught a blocker the cheap run missed. The same setup
  three days later cost 3.5x. "Anything that grows the carried context has to remove turns to break
  even." [What an AI code review costs](https://blog.traderspost.io/article/what-an-ai-code-review-costs)
- **A second review round adds noise.** 30 artifacts, 150 injected errors: single-pass review F1 0.376
  beat every multi-turn variant (best 0.303, p < 0.001). Extra rounds raised recall by 0.08 but
  false positives by 62% (8.5 vs 5.2; precision 0.30 to 0.20): reviewers invent findings once the real
  ones are found, and drift to critiquing the conversation instead of the artifact.
  [More Rounds, More Noise, arXiv 2603.16244](https://arxiv.org/abs/2603.16244)
- **Split finding from checking.** Practice reports keep generation and verification in separate
  passes, with the checker able to read the whole codebase; a finder-plus-verifier setup cut one
  pipeline's false positives 560 to 64. Missing visibility into other files caused ~10% of false
  positives in one field study. Vendor and single-case numbers, not benchmarks.
  [Reviewate](https://reviewate-website.pages.dev/blog/reduce-false-positives-ai-code-review),
  [Augment](https://www.augmentcode.com/guides/ai-code-review-accuracy)
- **Caching across our reviewers is unlikely.** Prompt caches match a byte-exact prefix. Each persona
  has its own system prompt, so the pack, sent after it, is not shared. Forks share the parent's cache
  but not its independence (section 5). Resuming a subagent can miss the cache on the first message.
  Unofficial sources only. [finisky](https://finisky.github.io/en/claude-code-fork-cache/),
  [cache miss on resume](https://claudeissues.com/issue/44724-subagent-cache-miss-on-first-sendmessage-resume-cache-read-0)

**What this means for the protocol (not yet applied, owner decides):**
1. The scout is supported on tokens; whether the pack loses findings is still untested anywhere. Our
   next round should measure it: same change, same personas, with and without the pack, count
   checked findings.
2. Count turns, not just tokens read. Personas already have small tool lists; keep them small.
3. "Use a small model" for replies may not save much if it takes more turns. Measure before adopting.
4. Reply rounds (protocol step 7) risk invented findings. Keep them to co-signs and votes on existing
   entries; no new findings in a reply round, or drop the step. Our own data agree: "more rounds on
   the same code find less" (case-study.md).
