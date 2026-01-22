([Past chat][1])([Past chat][1])([Past chat][1])([Past chat][1])([Past chat][1])

Alright — here’s an **extensive “Project Setup + Roadmap” doc** you can paste into a new ChatGPT Project (and also turn into `PROJECT_BRIEF.md` inside the repo). It’s written assuming you’re restarting from **Prompt 1 / Batch 1** and building forward toward the **Batch 10 Nat/Basic slice + delta encoder** plan you pasted.

---

# Proof OS / AlphaProof++ (Python-first) — Project Setup Doc

## 0) One-sentence North Star

Build a **laptop-first** Lean4/mathlib theorem-prover system that improves **proofs per unit compute** via **search + verifier loops + caching + compression-progress**, and eventually via **delta state embeddings** (token-delta → true Expr DAG).

## 1) The thesis (what makes this project different)

We win **not by scaling models**, but by **amortizing compute**:

* **Transition caching** makes verifier calls cheaper.
* **Search allocations (MCTS)** spend compute where it matters.
* **Retrieval + memory** reduces branching factor.
* **Macro mining / proof-program compilation** converts expensive traces into reusable assets.
* **Delta encoders** cut the per-step “span” cost (critical path per transition).

This is “compression-progress” operationalized:

> Don’t just solve more; solve so future solves cost less.

---

# 2) Non-negotiables (project guardrails)

### Determinism

* Stable ordering everywhere (sort keys, tie-break by tactic string, then index).
* Any randomness must be seeded and logged.
* Float comparisons must be stable; when ties happen, enforce deterministic order.

### Unit-test discipline

* Every feature has unit tests.
* Unit tests **must not** require network, LeanDojo downloads, or a full mathlib checkout.
* Real integration tests can exist, but they’re separate and optional.

### Import hygiene

* No heavy work at import time (no loading big indices, no initializing envs).
* CLIs should build configs and call library functions.

### Performance discipline

* Performance changes must be either:

  * clearly asymptotic (e.g., chunked top-k avoids huge allocations), or
  * backed by profiling evidence.

### Build leverage doctrine

* Python is the “highest leverage” substrate early.
* If we ever use Rust later, it’s **only** for proven hotspots (profile-driven).

---

# 3) Your background / learning constraints

* You’re strong in **Java backend** (~1.5 years) + some C/C++.
* You’re building AlphaProof++ while learning Python.
* Goal: reach **Fluency B** (idiomatic Python + pro engineering practices) *while shipping*.

So the workflow must force:

* types, tests, clean module boundaries, profiling-first performance.

---

# 4) Tooling and workflow (PyCharm + Cursor + ChatGPT Project)

### The “separation of powers”

* **PyCharm:** you write code (the reps), run tests, refactor, debug.
* **Cursor (Ask mode):** review + suggestions (optional) — not the source of truth.
* **ChatGPT Project:** architecture, batch planning, rubric review, first-principles explanations.

### The rule of 3 (the learning multiplier)

1. You implement a change in PyCharm.
2. You ask for review (Cursor or ChatGPT).
3. You re-implement the key improvements **from memory** (active recall) and rerun tests.

---



## Code style baseline

* `ruff` for lint+format
* `pyright` for typing
* `pytest` for tests

**Definition of Done for any PR/commit:**

* `ruff` clean
* `pyright` clean (or minimal approved exceptions)
* `pytest -q` passes

---

# 6) What we measure (the scoreboard)

Every eval run must emit:

* `solved / attempted`
* `verifier_attempted` (Lean transitions attempted)
* `transition_cache_hit_rate`
* `search_budget` (sims, depth, max-actions)
* `tactic_bans` (e.g., omega banned)
* proposer token counts (if using an LLM) or local proposer calls

This turns “vibes” into a measurable loop.

---

# 7) How to load context into the ChatGPT Project

### Best practice: upload 3 small files, not one huge dump

1. `PROJECT_BRIEF.md` — 1–2 pages (this doc’s first half)
2. `BATCH_LOG.md` — what changed per batch + metrics
3. `REPO_TREE.txt` — file list (so the project can navigate)

Optional:

* `cursor_raw_transcripts.txt` (appendix only)

Raw dumps are okay, but always include a curated summary.

---

# 8) The Prompting Protocol (what you ask the Project assistant)

## Working session prompt (use daily)

```text
Session goal: <one sentence>
I will paste: (1) file/diff, (2) test output, (3) notes.

Respond with:
1) Minimal patch plan (<= 5 bullets)
2) Exact edits (small blocks) or a precise diff description
3) Tests to add (unit only, no network)
4) Determinism/performance risks
5) First-principles explanation (short)
```

## Code review rubric prompt

```text
Review using this rubric:
- correctness + edge cases
- determinism (ordering, tie-breaks)
- testability (fake env, no heavy imports)
- complexity + hotspots
- pythonic idioms (remove Java-ish patterns)
- API boundaries

Suggest the smallest set of changes that improve quality without changing behavior unless necessary.
Explain from first principles.
```

---

# 9) Batch Roadmap (starting Prompt 1 / Batch 1)

You said you want to restart from the beginning. So here’s a clean “Batch 1 → Batch 10” progression that *naturally leads* into prompts 29–31 and then Stage B/C delta encoder work.

## Batch 1 — Skeleton + determinism foundations

**Prompt 1 — Repo bootstrap + toolchain**

* Add `pyproject.toml`, `ruff`, `pyright`, `pytest`, basic package layout.
* Add `tests/test_smoke_imports.py` that imports key modules (no heavy imports).
  **Done when:** `pytest -q` passes on a clean clone; imports are fast.

**Prompt 2 — Core types + interfaces**

* Define `Action`, `Outcome`, `MCTSConfig`, `ActionGenConfig` in `core/types.py` (dataclasses, typed).
* Define `Verifier` and `Env` interfaces (Protocols).
  **Done when:** types are stable and unit tests validate basic construction.

**Prompt 3 — Fake environment for unit tests**

* Implement `FakeEnv` / `FakeVerifier` that can simulate:

  * no-op transitions
  * error transitions
  * solved transition
    **Done when:** can unit-test MCTS without Lean.

---

## Batch 2 — Minimal MCTS + action generation

**Prompt 4 — Action generator v0**

* Base tactics list + priors.
* Support bans (`ban-exact`, later `ban-prefix`).
  **Done when:** deterministic action list and ban filtering tested.

**Prompt 5 — MCTS core v0**

* Deterministic expansion ordering.
* PUCT selection + backup.
* Stops on solve/error/depth.
  **Done when:** FakeEnv test solves within budget.

**Prompt 6 — CLI “hello world” runner**

* `solve_hello_world_mcts.py` runs MCTS on FakeEnv and prints metrics.
  **Done when:** CLI works and is import-clean.

---

## Batch 3 — Transition cache + metrics plumbing

**Prompt 7 — Transition cache (state_hash, tactic) → outcome**

* Add hit/miss accounting.
* Deterministic keys and serialization for debugging.
  **Done when:** cache hit rate appears in metrics and is unit-tested.

**Prompt 8 — Metrics schema + run artifacts**

* Write `eval/metrics.py` and a `RunReport` JSON schema.
* Always save configs + results.
  **Done when:** every run emits `report.json`.

**Prompt 9 — Determinism harness**

* Unit test that repeated runs on FakeEnv yield identical outputs.
  **Done when:** stable.

---

## Batch 4 — Premise plumbing (stub)

**Prompt 10 — PremiseRecord + storage**

* Define `PremiseRecord`, minimal DB format (jsonl/parquet later).
  **Prompt 11 — Premise embedding stub**
* Start with deterministic hashing → fixed-size vector (so everything works before ML).
  **Prompt 12 — PremiseIndex.search (simple)**
* cosine top-k, stable ordering.
  **Done when:** retrieval is deterministic and tested.

---

## Batch 5 — Memory index (trace memory)

**Prompt 13 — Memory store**

* Store (state_repr, action, outcome, next_state_repr) for successful steps.
  **Prompt 14 — Memory embedding + index**
* Same deterministic embedding approach initially.
  **Prompt 15 — Integrate memory retrieval into proposer**
* “memory-first” suggestions + fallback to base actions.
  **Done when:** you can see behavior changes in FakeEnv and metrics.

---

## Batch 6 — Real verifier integration boundary (integration tests)

**Prompt 16 — VerifierRunner interface + subprocess-safe wrapper**

* timeouts, cleanup, logging
* keep unit tests fake; add optional integration test marker.
  **Prompt 17 — Lean task discovery boundary**
* A CLI that *can* discover tasks from a file when mathlib is present (integration).
  **Prompt 18 — Eval runner (library)**
* `eval/run.py` that runs tasks, collects metrics, saves artifacts.
  **Done when:** you can run a small real slice (even if tiny).

---

## Batch 7 — Make search smarter (still model-free)

**Prompt 19 — Better priors + action templates**

* “simp [..]”, “rw [..]” action families.
  **Prompt 20 — No-op pruning + basic progressive widening**
* (Later refined in prompt 30.)
  **Prompt 21 — Budget controls in configs**
* (Later wired in prompt 31.)
  **Done when:** omega-banned style failure modes are less frequent on small slices.

---

## Batch 8 — Scale and indexing discipline

**Prompt 22 — Index build pipeline**

* build premise DB, build vectors, persist `vecs.npy`, `records.jsonl`.
  **Prompt 23 — Deterministic normalization invariants**
* unit normalization guaranteed; tests enforce.
  **Prompt 24 — Add memory-mapped loading**
* `np.load(..., mmap_mode="r")` groundwork.
  **Done when:** indices load fast and don’t blow RAM.

---

## Batch 9 — Measurement & runbooks

**Prompt 25 — Runbook discipline**

* docs for running a slice, capturing metrics, reproducing.
  **Prompt 26 — Regression harness**
* fixed seed eval suite; compare outputs.
  **Prompt 27 — Trace introspection tools**
* small CLI to inspect failures, top tactics, cache stats.
  **Prompt 28 — Prep for Mathlib Nat/Basic**
* pipeline supports file_path + include_prefix settings.

---

## Batch 10 — The plan you pasted (Prompts 29–31)

These match your “scale + measure” mission for Nat/Basic.

* **Prompt 29:** memmap + chunked cosine top-k (PremiseIndex + MemoryIndex)
* **Prompt 30:** fix omega-banned timeout via action priors + progressive widening + ignore_noop
* **Prompt 31:** make budgets configurable from CLI + write runbook for Nat/Basic

**After Batch 10:** run two evals:

1. omega allowed (maximize solved)
2. omega banned (ablation)

Capture: solved/attempted, verifier_attempted, cache hit rate, proposer tokens.

---

# 10) After Batch 10: Stage B → Stage C encoders

## Stage B (next 1–2 batches): delta without Lean AST

**Delta token-multiset encoder**

* maintain token counts of pretty-printed state
* update counts by diff
* embed via feature hashing / small learned projection
  **Goal:** prove delta-update wins end-to-end without needing Lean internals.

## Stage C (later): True Expr DAG encoder

* extract Lean expressions to structured DAGs
* hash-cons nodes
* message passing / bottom-up embeddings cached by node-hash
* update cost proportional to changed subgraph

This is the “revolutionary” piece that can cut span constants.

---

# 11) Python mastery plan while building (Fluency B track)

You’ll “accidentally” become fluent if you enforce:

### Daily

* Write code + tests in PyCharm
* Run review rubric
* Re-implement key improvements via active recall

### Weekly gates

Every week you must produce:

1. one refactor PR that reduces complexity/LOC
2. one perf note (what was profiled, what changed)
3. one determinism note (what tie-breaks/ordering rules were added)

This is what converts “I can write Python” into “I write clean Python naturally.”

---

# 12) Recommended “Project Instructions” block (paste into ChatGPT Project)

```text
You are the “Proof OS Architect + Python Fluency Coach” for an AlphaProof++-style theorem proving system.

Goal:
- Build a laptop-first Lean4/mathlib prover with search+verifier loops.
- Optimize proofs per unit compute via caching, MCTS allocation, retrieval/memory, and compression-progress.

Constraints:
- Deterministic outputs (stable ordering, tie-breaks).
- Unit tests required; no network/LeanDojo in unit tests.
- No heavy import-time work.
- Performance work must be profiling-driven or clearly asymptotic.
- Use typing (pyright) and enforce invariants (unit normalization, etc.).

Workflow:
- I paste diffs/files/tests.
- You respond with:
  (1) top 3 issues,
  (2) minimal patch plan,
  (3) exact edits or precise diff guidance,
  (4) tests to add,
  (5) determinism/perf risks,
  (6) first-principles explanation.

Roadmap:
- Batch 1–10 as in PROJECT_BRIEF, culminating in Mathlib/Data/Nat/Basic slice (Mathlib/Data/Nat/ prefix).
- After Batch 10 metrics, Stage B delta token-multiset encoder, then Stage C true Expr DAG encoder.

Learning:
- Assume I come from Java; optimize explanations for bridging to Pythonic idioms.
- Favor small, test-backed changes over rewrites.
```

---

We are going to be starting out with a single file monolith structure and lean python along the way. You are my mentor/guide/teacher and will also help me unblock things.