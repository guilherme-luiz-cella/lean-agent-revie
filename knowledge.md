# Knowledge: AI on code, tokens, handoffs, multi-agent

Collected 2026-10-28. Terse on purpose. One fact per line, source after it.
Tags: `[paper]` peer-reviewed or arXiv, `[vendor]` company about own product or field, `[blog]` one
practitioner, `[n=1]` single run, `[2nd]` read via secondary coverage only, primary not opened.
Protocol rules built on this: `protocol.md`. Deeper notes on the board design: `research.md`.

## 1. What AI does to code (the baseline)

- Experienced devs, own large repos, 246 tasks, RCT: AI allowed = 19% slower. They believed 20% faster.
  Gap belief vs measured ~39 points. Early-2025 tools. [paper][2nd]
  [METR via InfoQ](https://www.infoq.com/news/2025/07/ai-productivity)
- DORA 2025: AI adoption now goes with more throughput, and still with more instability (change fail
  rate, rework). ~90% use AI; 30% do not trust its code. AI amplifies a team's strengths and its
  dysfunctions. [vendor][2nd] [DORA via InfoQ](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)
- Security: AI code passes security tests ~56% of the time, flat for a year, 100+ models. Java 30%,
  Python 63%. Coding-tuned models no better (51% vs 52%). [vendor]
  [Veracode 2026](https://www.veracode.com/news/llms-are-getting-smarter-but-not-safer-veracode-2026-genai-code-security-report-finds-ai-generated-code-security-has-stalled-at-56%25-pass-rate/)
- Duplication and churn up, refactoring down in AI-era commit histories. [vendor][2nd] (GitClear 2024)
- Agents add test changes in only 49.6% of PRs that touch code under test.
  [paper] [Test coverage of agentic PRs](https://huggingface.co/papers/2607.18057.md)
- TDD inside the agent loop: no clear quality gain, small sample. Agents skip the red step, write code
  first, over-implement. [blog] [Fowler site, via summary](https://daily.dev/posts/tdd-inside-the-agent-loop---theater-or-actual-value--mytwhkuys.md)

Takeaway: AI code is fast, not safe by default. Speed feels bigger than it is. Check everything.

## 2. Improving code with agents

**Context files (CLAUDE.md / AGENTS.md)**
- LLM-written context files: success -0.5% to -2%, cost +20%. Human-written: +4% success, cost up to
  +19%. Agents with a file explore more, run more tests. Mostly duplicates what the repo already says.
  138 issues, 12 repos. [paper][2nd]
  [Evaluating AGENTS.md, arXiv 2602.11988, via summary](https://arxiviq.substack.com/p/evaluating-agentsmd-are-repository)
- Rule: write it by hand, short, only what the agent cannot find in the code. Never auto-generate.

**Review and false findings**
- AI review false positive claims: 5-15% (vendor), up to 50% (research system). No neutral benchmark.
  [vendor] [CodeAnt](https://www.codeant.ai/blogs/ai-code-review-false-positives)
- Top cause of false warnings: shallow reasoning across functions (37%). Missing view of other files:
  ~10%. [2nd] [Augment](https://www.augmentcode.com/guides/ai-code-review-accuracy)
- Split finder from checker. Checker reads whole codebase. One pipeline: 560 to 64 false positives.
  [vendor][n=1] [Reviewate](https://reviewate-website.pages.dev/blog/reduce-false-positives-ai-code-review)
- Google Tricorder kept an analyzer only while effective false positive rate stayed under 10%. [2nd]
- Second review round: recall +0.08, false positives +62%, F1 0.376 to 0.303. Reviewers invent findings
  once real ones are gone. One pass beats many. [paper]
  [More Rounds, More Noise](https://arxiv.org/abs/2603.16244)
- Models cannot self-correct reasoning without outside feedback. Gains labeled "self-correction" were
  really self-consistency. [paper] [arXiv 2310.01798](https://arxiv.org/pdf/2310.01798)
- Running the thing beats reading it. Our persona that clicked found the dead menu; readers did not.
  [n=1] (`case-study.md`)

**LLM as judge**
- Known biases: position, verbosity, self-preference (models score own outputs higher).
  [paper] [Self-preference bias](https://arxiv.org/abs/2410.21819),
  [Position bias](https://arxiv.org/html/2406.07791v1)
- Position consistency drops when two answers are close in quality. Close calls = least reliable.
- Judge with a rubric, one call, score 0-1 plus pass/fail: closest to humans (Anthropic). Judge the
  end state, not the path. ~20 real cases enough early: big effects show in small samples. [vendor]
  [Anthropic research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Never let a model judge its own output alone. Use tests, a different model, or a human.

## 3. Token usage

**Where tokens go**
- Review reads a lot, writes a little. ChatDev: review = 59.4% of all tokens. [paper][2nd]
  [Tokenomics](https://www.engineerscodex.com/tokenomics-agentic-software-engineering)
- Our reviewers: 67-133k tokens each, >90% reading, reply ~200 words. [n=1] (`case-study.md`)
- Tool observations ~84% of an average SWE-agent turn. [paper]
  [Complexity Trap](https://arxiv.org/abs/2508.21433)
- Cost = prefix x turns x agents. Every turn re-reads the prefix. [blog]
  [TradersPost](https://blog.traderspost.io/article/what-an-ai-code-review-costs)
- Claude Code sends ~33k tokens before your prompt (tools, system). [blog]
  [HN](https://hn.svelte.dev/item/48883275)
- Tokens buy quality: token count explained 80% of variance on BrowseComp; with tool calls and model,
  95%. Cutting blindly cuts results. [vendor] [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)

**What cuts cost (measured)**

| Lever | Saving | Catch | Source |
|---|---|---|---|
| Small tool allowlist per agent | prefix 81k to 23k, cost -45% | none seen | [blog] TradersPost |
| Mask old tool outputs | cost about half, solve rate same or +2.6% | SWE-agent only | [paper] Complexity Trap |
| Mask + summarize hybrid | further -7% to -11% | more parts | [paper] Complexity Trap |
| Digest pass ("librarian", JSON) | 80k to 21k input | quality not checked | [blog][n=1] [DEV](https://dev.to/andreagriffiths11/stop-paying-for-the-same-tokens-twice-geh) |
| Shared cached prefix | $1.32 to $0.45 | warm cache only; cold = no saving | [blog][n=1] same |
| Prompt compression (LLMLingua) | up to 20x, -1.5 points | collapses near 25-30x | [paper] [LLMLingua](https://arxiv.org/abs/2310.05736) |
| Forked subagents share parent cache | ~90% on shared prefix | not independent | [blog] [finisky](https://finisky.github.io/en/claude-code-fork-cache/) |
| Chooser picks who acts | tokens 3.7-4.5x lower | same accuracy | [paper] [LbMAS](https://arxiv.org/abs/2507.01701) |

**Traps**
- Cheaper model: rate card said 2.5x cheaper, measured 9%. It took 2.2x the turns. [blog] TradersPost
- Newer model cost 2.7x, caught a blocker the cheap one missed. Price vs catch: measure both.
- Same setup three days later: 3.5x cost. Compare same-day ratios, never absolute dollars.
- Putting the whole diff in one file: tool calls -96%, cost +12%. Bigger context must remove turns to pay.
- Cache matches byte-exact prefix. Different system prompt per agent = no shared cache. Resume of a
  subagent can miss cache on first message. [blog]
  [issue 44724](https://claudeissues.com/issue/44724-subagent-cache-miss-on-first-sendmessage-resume-cache-read-0)
- Static content first, dynamic last. Never edit the prefix mid-session. [2nd]
  [implicator](https://www.implicator.ai/anthropic-says-cache-misses-are-production-incidents-reveals-caching-shaped-claude-code/)

## 4. Transferring information

**Long context rots**
- All 18 models tested got worse as input grew, task difficulty fixed. Even copying repeated words.
  Distractors hurt more at length. [vendor][2nd]
  [Chroma via summary](https://www.morphllm.com/context-rot)
- Coding agents pass 100k tokens routinely. 5k targeted retrieval beat a 100k codebase summary
  (Sourcegraph, unverified). [blog] [morphllm](https://morphllm.com/context-rot)
- Goal: smallest set of high-signal tokens. Long-run tools: compaction, structured notes, subagents
  that return condensed results. [vendor][2nd]
  [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Compaction: tool results are the easiest thing to drop; deciding what to keep is the hard part.

**Handoff format**
- Relay between two agents: narrative summary kept task feasible 0.48, raw 0.88, structured JSON 0.96.
  Small omissions break strict constraints. [paper]
  [State compression in relays](https://www.alphaxiv.org/abs/2607.18265)
- Compression cut 26-54% tokens, performance "largely" held, no guarantee key details survive. [paper]
  [ACON](https://arxiv.org/abs/2510.00615)
- Brief each subagent with: objective, output format, tools and sources, boundaries. Vague briefs =
  duplicated and missing work. [vendor] Anthropic research system
- Subagents return condensed findings and references, not copies. [vendor] same
- Bad tool description fixed by an agent: task time -40%. Tool text is part of the handoff. [vendor] same

**Shared board vs messages**
- Blackboard (shared space, agents read and post): best on MATH 72.6%, fewer tokens than 5 of 6
  systems. [paper] LbMAS
- Digests <= 200 tokens plus addresses: fresh agent cost flat ~2.7k for boards 10k to 887k tokens.
  [blog] [blackboard](https://github.com/TapanManu/blackboard)
- Each debater sees only some peers: input tokens -9% to -53%, same or better accuracy (best ~2 of 5).
  [paper] [Sparse topology](https://arxiv.org/abs/2406.11776)
- Shared memory risks write conflicts. Fix: one writer per file, or one moderator. [blog]
- Our run: free writes to one shared file broke (agent moved others' text). One writer per file fixed
  it. [n=1] (`case-study.md`)

**Protocols**
- MCP = agent to tool. A2A = agent to agent. Complementary. Neither carries prior state for you: what is
  not in the payload is lost. A2A is stateless on memory. [blog]
  [Mem0](https://mem0.ai/blog/how-memory-works-in-agent-to-agent-protocols)
- Dominant handoff failures in practice: format mismatch, information loss, self-reference loops. [blog]

## 5. Multi-agent systems

**When it pays**
- Multi-agent research beat single agent by 90.2% (Opus lead + Sonnet subagents), at ~15x chat tokens.
  Single agent: ~4x. Works for broad, parallel tasks. Coding fits poorly: shared context, many
  dependencies. [vendor] [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- 180 configs: fit of architecture to task decides, not agent count. Sequential planning: -39% to -70%
  with multi-agent. Once one agent scores ~45%+, more agents give little or negative return. [paper]
  [Scaling agent systems](https://arxiv.org/abs/2512.08296)
- 2 diverse agents can match 16 identical ones. Count effective channels, not heads. [paper]
  [Scaling via diversity](https://arxiv.org/abs/2602.03794)
- Personas collapse to a few answer types. More personas do not fix it. Vary job and evidence, not
  character. [paper] [Chameleon's Limit](https://www.alphaxiv.org/abs/2604.24698)

**Why it fails** (MAST, 1,642 traces, 7 frameworks) [paper]
[Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)

| Group | Share | Top modes |
|---|---|---|
| System design | ~44% | step repetition 15.7%, unaware of stop condition 12.4%, disobey task 11.8% |
| Agent misalignment | ~32% | reasoning-action mismatch 13.2%, task derailment 7.4%, no clarifying question 6.8% |
| Verification | ~24% | wrong verification 9.1%, none or partial 8.2%, stops too early 6.2% |

- Failure rates of 6 popular systems: ~41-87%, benchmarks differ.
- Fixes tested: clearer roles +9.4% success; top-level objective check +15.6%. Still low overall.
- Errors: independent agents amplified errors 17.2x; with orchestrator checking, 4.4x. [paper]
  Scaling agent systems

**Debate and voting**
- Debate (3 agents, 2 rounds) lost to plain majority vote at equal compute. Gain was consistency, not
  correction. [paper] arXiv 2310.01798
- Debate can make answers worse; minority agents conform to the majority, right or wrong. [paper]
  [Talk Isn't Always Cheap](https://arxiv.org/abs/2509.05396)
- Independent agreement is the signal. Two agents finding the same bug unseen = always real in our runs.
  [n=1] (`case-study.md`)

**Seen in practice (Anthropic research system)** [vendor]
- 50 subagents spawned for simple queries. Fix: budget in prompt (simple: 1 agent, 3-10 calls;
  compare: 2-4 agents, 10-15 calls each; complex: 10+).
- Endless search for sources that do not exist. Kept going after enough results.
- Subagents distracting each other with updates. Lead blocked waiting on each batch.
- Preferred SEO farms over primary sources. Humans caught it, evals did not.
- Parallel: 3-5 subagents, 3+ tools each, research time down up to 90%.

## 6. Rules that follow

1. Measure turns and prefix, not just reply length. Reading is the bill.
2. Give each agent the fewest tools and only the context it needs. Mask old tool output.
3. Hand off structured: verbatim excerpts, file:line, checked facts. No prose summary of code.
4. Few agents, different evidence each (read, run, test, click). 3-5 per round.
5. One chooser, one checker. Checker sees the whole repo. Nothing reaches the owner unchecked.
6. One review pass per change. Follow-up rounds only co-sign or vote, never add new findings.
7. Stop rule: hard cap plus plateau (findings per round flat or rising = stop).
8. Never let a model grade only its own work. Use tests, a second model, a human.
9. Context files: human-written, short, only what the code cannot tell.
10. Cheaper model is not cheaper until measured. Compare same-day ratios.

## 7. Open, not answered anywhere yet

- Does a scout pack lose findings vs free exploration? No study found. Test it here: same change, same
  personas, with and without pack, count checked findings.
- Code-specific judge bias numbers: none found.
- Tool output truncation in review agents (not SWE-solving): no data found.
