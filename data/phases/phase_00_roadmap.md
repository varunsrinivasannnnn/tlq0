# Phase 0: Initial Roadmap

**Source**: GPT 5.2 Pro  
**Date**: 2026-01-22  
**Type**: Project roadmap and architecture overview

---

# Executive Summary

tlq0 is an attempt to **escape the human data loop** by doing for Lean theorem proving what AlphaZero did for Go: learn entirely from self-play against a perfect environment, where “truth” is just the Lean kernel. The philosophical foundation you wrote down is explicit: **intelligence is compression of predictive structure over state transitions** , and math is the cleanest sandbox because verification is binary and unhackable . So tlq0 is not “a big model that knows math”; it’s a **compression engine** that discovers reusable proof programs (macros/lemmas) because MDL pressure makes them pay rent.

The convergent architecture from the 8 frontier models gives you a concrete blueprint: represent proof states as a **hash-consed DAG with De Bruijn indices**, use a **small GNN** to predict actions, constrain the action space to a **tiny typed bytecode DSL** (no `simp`, no `aesop` early), generate tasks via **forward theorem generation**, and drive long-term progress with **MDL** plus a **wake/sleep** loop that alternates between searching/proving and compressing traces into macros . The “Proof OS” metaphor is literal: Lean is the kernel (truth), search is the scheduler (compute allocation), the macro/lemma library is the filesystem (compiled intelligence), retrieval is the index (fast recall), and MDL pruning is garbage collection (taste) .

Implementation reality: you’re building (1) a Lean interaction backend, (2) a state IR + hashing/caching layer, (3) a search engine, (4) a learning pipeline, and (5) a compression/macro economy with an explicit MDL accounting system. The fastest path to “first learning signal” is: **build a brutally simple baseline** (tiny logic fragment + brute search) that produces *some* successful proofs, then iterate: improve representation → improve guided search → improve theorem generation → add macro compression → stabilize MDL improvements. That is the critical path.

---

# Complete Phase List

Below is an **honest “not artificially compressed” roadmap**: **52 phases** (with sub-steps). For a single dedicated engineer, this is roughly **12–24 months** to a robust wake/sleep system showing clean learning curves, with longer tail work for induction-heavy math.

| Phase | Name                             |  Effort | Key Output                                                           |                                |
| ----: | -------------------------------- | ------: | -------------------------------------------------------------------- | ------------------------------ |
|     1 | Reproducible experiment harness  |   1–2 w | Deterministic runs, logging, configs, run dirs                       |                                |
|     2 | Lean toolchain pinning           |   1–2 w | Lean/Lake project + versions + smoke checks                          |                                |
|     3 | Backend interface abstraction    |     1 w | `ProverBackend` API + stub backend                                   |                                |
|     4 | Minimal Lean interaction         |   2–3 w | Can open goal, apply primitive tactics, get new goals                |                                |
|     5 | Tiny action bytecode DSL v0      |   1–2 w | Typed ops + encoding + pretty-print                                  |                                |
|     6 | Baseline search v0               |   2–3 w | BFS/DFS/A* over DSL actions                                          |                                |
|     7 | Toy logic fragment curriculum    |   1–2 w | “Prop-only” or tiny Nat fragment tasks                               |                                |
|     8 | Proof trace logging format       |     1 w | Stable JSONL schema for trajectories                                 |                                |
|     9 | Evaluation harness v0            |     1 w | Fixed benchmark + solve rate + budgets                               |                                |
|    10 | Forward theorem generation v0    |   2–4 w | Generate theorem by sampling well-typed terms (Lean-inferred types)  |                                |
|    11 | Hindsight experience replay      |   1–2 w | Convert intermediate states into training tasks                      |                                |
|    12 | Dataset + replay buffer          |   1–2 w | On-disk shards + sampling + stats                                    |                                |
|    13 | Representation IR scaffolding    |   2–3 w | Lean expr → internal nodes (initially partial)                       |                                |
|    14 | Hash-consing store               |   2–4 w | Interned DAG nodes + Merkle hashes                                   |                                |
|    15 | De Bruijn normalization          |   2–4 w | Alpha-equivalence canonicalization                                   |                                |
|    16 | Graph extraction for proof state |   2–3 w | Local context + goal → graph substructure                            |                                |
|    17 | GNN model v0                     |   2–4 w | Small MPNN policy head                                               |                                |
|    18 | Action heads and pointer args    |   2–4 w | Select op + select hyp/lemma pointers                                |                                |
|    19 | Imitation training loop v0       |   2–3 w | Train on successful traces; eval on held-out                         |                                |
|    20 | Guided search integration        |   2–4 w | Policy-guided expansion + fallback search                            |                                |
|    21 | Levin/MDL search priority        |   2–4 w | Priority = cumulative code length Σ(-log π)                          |                                |
|    22 | Stable curriculum scheduling     |   2–3 w | Frontier selection, avoid collapse                                   |                                |
|    23 | Baselines suite                  |   2–3 w | Random, heuristic, unguided search comparisons                       |                                |
|    24 | Macro representation             |   1–2 w | Macro bytecode, typing, expansion                                    |                                |
|    25 | Trace mining v0                  |   2–3 w | Extract frequent subsequences                                        |                                |
|    26 | Grammar compression engine       |   3–6 w | Sequitur/BPE on traces                                               |                                |
|    27 | MDL accounting system            |   3–6 w | L(Library)+ΣL(proof                                                  | Library) with acceptance test  |
|    28 | Macro acceptance gate            |   2–4 w | Held-out ΔMDL < 0 admission                                          |                                |
|    29 | Macro execution in search        |   2–4 w | Macros as callable ops, inlining/expansion                           |                                |
|    30 | Lemma library v0                 |   2–3 w | Store discovered lemmas/macros with metadata                         |                                |
|    31 | Retrieval index v0               |   2–4 w | SimHash/ANN for lemma lookup                                         |                                |
|    32 | MDL lemma economy pruning        |   2–4 w | Rent collection + pruning unused macros                              |                                |
|    33 | Wake phase pipeline              |   2–4 w | Generate → search → store traces                                     |                                |
|    34 | Sleep phase pipeline             |   2–4 w | Compress → propose macros → MDL gate                                 |                                |
|    35 | Full wake/sleep loop             |   2–6 w | End-to-end iterative improvement                                     |                                |
|    36 | Delta-state embedding v0         |   3–6 w | Incremental updates State_{t+1}=Update(State_t,Δ)                    |                                |
|    37 | Cached message passing           |   2–4 w | Recompute only changed subgraph nodes                                |                                |
|    38 | Delta-code discretization        |   3–8 w | 64-bit codes / VQ-VAE codebook                                       |                                |
|    39 | Multi-policy exploration         |   2–6 w | Ensemble or population policies                                      |                                |
|    40 | Generator improvements           |   4–8 w | Multiple generators; subgoal harvesting                              |                                |
|    41 | Generator–compressor coevolution |  4–10 w | Adversarial curriculum game                                          |                                |
|    42 | Equality + rewrite robustness    |   4–8 w | Strong REWRITE, congruence handling                                  |                                |
|    43 | Induction phase 1                |  4–10 w | Induction tactic + simple Nat theorems                               |                                |
|    44 | Induction phase 2                |  6–12 w | Recursion schemas, stronger invariants                               |                                |
|    45 | Lemma synthesis beyond macros    |  6–12 w | Propose new lemmas, verify, index, reuse                             |                                |
|    46 | Metric-learning retrieval head   |  4–10 w | Add macros without retraining                                        |                                |
|    47 | Robust evaluation and holdouts   |   2–4 w | Hard holdouts, anti-overfit gates                                    |                                |
|    48 | Performance engineering pass     |  4–10 w | Profiling, batching, parallel envs                                   |                                |
|    49 | Long-horizon search stability    |  4–12 w | Better pruning, value head, beam/MCTS                                |                                |
|    50 | Proof artifact compilation       |   2–6 w | Emit Lean code for proofs/macros                                     |                                |
|    51 | Research-grade ablations         |  4–12 w | Full factorial ablations + reports                                   |                                |
|    52 | Scaling milestones               | ongoing | Expand domains, measure ceiling                                      |                                |

---

# Detailed Phase Descriptions

I’m going to be strict about your template. Each phase has the requested fields.

## Phase 1: Reproducible experiment harness

**Goal**
Build the deterministic, inspectable “proof OS shell” so every later component can be run, logged, reproduced, diffed, and profiled.

**Detailed Description**
This phase is about making tlq0 *debuggable by construction*: deterministic RNG seeding across Python/NumPy/PyTorch, a run directory layout, a typed config system, JSONL event logging, artifact saving/loading, basic sanity checks, and a minimal CLI. This is the substrate that prevents “mystery learning” later: every run produces a full record of what happened, which theorem set was used, what budgets were used, and what code version ran.

**Inputs**

* Existing `tlq0.py` skeleton 
* Local Python env

**Outputs**

* Updated `tlq0.py` with Phase 1 sections implemented
* `runs/` directory with structured run outputs
* JSONL logs + config snapshot + environment snapshot
* `tests/` with deterministic/unit tests

**Success Criteria**

* Two consecutive runs with the same seed produce identical config snapshot + identical initial RNG draws + identical “selfcheck” outputs
* A run can be resumed/replayed (at least at the “config + environment + seeds” level)
* Unit tests pass

**Estimated Effort**
1–2 weeks.

**Key Risks**

* “Determinism” is partial (MPS nondeterminism, multithreading) leading to debugging hell later.

**Failure Indicators**

* Seeded runs diverge in first ~100 RNG draws or log events.
* Run directories don’t contain enough info to reproduce.

**Dependencies**
None.

**Sub-phases/Steps**

1. Define configuration dataclasses + validation
2. Deterministic seeding utilities
3. Run directory + artifact store
4. JSONL event logger + metrics stub
5. CLI with `init`, `selfcheck`, `run` modes
6. Unit tests

---

## Phase 2: Lean toolchain pinning

**Goal**
Pin Lean/Lake/LeanDojo versions so the verifier behavior is stable.

**Detailed Description**
You need a stable “physics” for your math universe. This phase sets up a Lean project (Lake) with a pinned toolchain version, plus whichever LeanDojo version you intend to use. It also creates a Lean file that imports only what you allow early (no automation), and runs minimal “hello proof” checks from Python so you know the Lean backend works before you build anything else.

**Inputs**

* Phase 1 harness

**Outputs**

* `lean/` project with pinned toolchain
* Smoke test proving a trivial theorem
* Recorded Lean version + lake manifest in run snapshots

**Success Criteria**

* `python tlq0.py selfcheck` verifies Lean invocation
* CI/local test can compile Lean project deterministically

**Estimated Effort**
1–2 weeks.

**Key Risks**

* LeanDojo install friction on Mac
* Version skew between Lean, mathlib/std, LeanDojo

**Failure Indicators**

* Frequent compilation failures / flaky toolchain
* Python–Lean handshake not stable

**Dependencies**
Phase 1.

**Sub-phases/Steps**

1. Create `lean/` project + minimal imports
2. Write trivial theorems and compile
3. From Python: run Lean compile + capture output
4. Freeze versions in docs/config

---

## Phase 3: Backend interface abstraction

**Goal**
Define the core API boundary between tlq0 and the verifier.

**Detailed Description**
Before implementing LeanDojo specifics, define a clean `ProverBackend` interface: “reset to goal”, “apply primitive tactic/action”, “get proof state”, “is solved”, “extract local hypotheses”, etc. This prevents the whole system from hard-coding LeanDojo quirks and gives you the ability to swap backends (LeanDojo vs direct Lean RPC) without rewriting search/learning.

**Inputs**

* Phase 1 harness
* Phase 2 Lean toolchain

**Outputs**

* `ProverBackend` abstract class
* Stub backend + basic error hierarchy
* Typed `RawState` and `BackendResult`

**Success Criteria**

* Search can be built entirely against the interface with a stub backend.

**Estimated Effort**
1 week.

**Key Risks**

* API too narrow → constant refactors later
* API too wide → premature complexity

**Failure Indicators**

* You keep adding “just one more method” every day.

**Dependencies**
Phase 1–2.

**Sub-phases/Steps**

1. Define “minimum” operations needed by your DSL
2. Define error handling + timeouts
3. Implement stub backend tests

---

## Phase 4: Minimal Lean interaction

**Goal**
Actually execute primitive actions in Lean and observe state transitions.

**Detailed Description**
This is your first “real environment step”: start from a goal, apply an `INTRO` or `EXACT`, and observe how the goal/hypotheses change. You’ll implement the mapping from your bytecode DSL to Lean tactics (or LeanDojo API calls), and a robust state serializer so downstream modules can consume states without scraping fragile strings.

**Inputs**

* Backend interface (Phase 3)

**Outputs**

* Lean backend implementation
* `ProofState` extraction (at least: goal string + hyps list)
* Round-trip: apply → get new state

**Success Criteria**

* Can solve a tiny set of hand-written theorems using only your primitive ops
* No crashes; failures are typed errors with logs

**Estimated Effort**
2–3 weeks.

**Key Risks**

* State parsing instability
* Lean tactic failures not cleanly captured
* Performance (Lean server overhead)

**Failure Indicators**

* Frequent “unknown error” exceptions
* State extraction differs across minor toolchain changes

**Dependencies**
Phases 1–3.

**Sub-phases/Steps**

1. Implement `reset(goal)` and `apply(Action)`
2. Implement robust `ProofState` serialization
3. Add timeout and retry logic
4. Build a micro-benchmark suite

---

## Phase 5: Tiny action bytecode DSL v0

**Goal**
Define the typed action language tlq0 searches over.

**Detailed Description**
The DSL is your “instruction set architecture.” Early on it must be small and analyzable. You’ll implement an enum of opcodes (INTRO, EXACT, APPLY, CASES, …), argument typing rules (which ops require a hypothesis id, which require an equality proof, etc.), compact encoding/decoding (for training and MDL cost), and pretty-printing for debugging. This should reflect the convergent architecture’s minimal primitives .

**Inputs**

* Lean interaction (Phase 4)

**Outputs**

* `ActionOp` enum + `Action` dataclass
* Typechecker for actions against a `ProofState`
* Serialization format (binary or JSON) for actions

**Success Criteria**

* Every action is either (a) statically rejected by the typechecker or (b) executed in Lean with well-defined result
* Action encoding round-trips perfectly

**Estimated Effort**
1–2 weeks.

**Key Risks**

* DSL too expressive → impossible search
* DSL too weak → cannot prove even simple theorems

**Failure Indicators**

* You keep sneaking in “just call simp” to make progress (don’t) .

**Dependencies**
Phases 3–4.

**Sub-phases/Steps**

1. Define opcodes and argument types
2. Implement static validity checks
3. Implement encoding/decoding and logging

---

## Phase 6: Baseline search v0

**Goal**
Prove things without learning.

**Detailed Description**
This phase gives you a floor baseline and a data generator. Implement a search algorithm (start with BFS/DFS with depth limits, then add A* / beam). It expands states using valid actions from the DSL, calls the backend to transition, and detects solved goals. The output is proof traces: sequences of actions that Lean verifies.

**Inputs**

* DSL v0 (Phase 5)
* Lean backend (Phase 4)

**Outputs**

* `SearchEngine` with budgets (nodes/time/depth)
* Proof trace extraction + replayable traces
* Basic heuristics (e.g., prefer INTRO on ∀/→ goals)

**Success Criteria**

* Solves a nontrivial fraction of a small toy benchmark
* Produces reproducible traces with fixed seed

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Combinatorial explosion even on tiny tasks
* Memory blow-up storing visited states

**Failure Indicators**

* Solve rate ~0% after days of tuning
* Search spends most time in backend overhead

**Dependencies**
Phases 4–5.

**Sub-phases/Steps**

1. State hashing and visited set
2. Depth-limited DFS baseline
3. BFS/beam for breadth
4. Budget controls + instrumentation

---

## Phase 7: Toy logic fragment curriculum

**Goal**
Choose the minimal domain where learning is possible.

**Detailed Description**
Pick a “starter theory” where your DSL can be complete enough: propositional logic (And/Or/Imp/False) is ideal. Write a generator of small theorems (or a curated initial set), create train/eval splits, and define “difficulty” (goal size, binder depth, branching). The main job is to ensure tasks are (a) solvable with your ops and (b) diverse enough to learn patterns.

**Inputs**

* Baseline search (Phase 6)

**Outputs**

* `ToyDomain` task suite + splits
* Difficulty metrics
* Curriculum scheduler stub

**Success Criteria**

* Baseline search solves easy tier reliably
* Hard tier exists where baseline fails

**Estimated Effort**
1–2 weeks.

**Key Risks**

* Too easy → nothing to learn
* Too hard → no data, no learning signal

**Failure Indicators**

* Only trivial tautologies; no generalization tests

**Dependencies**
Phase 6.

**Sub-phases/Steps**

1. Define allowed connectives and constructors
2. Build theorem set / generator
3. Build difficulty stratification and splits

---

## Phase 8: Proof trace logging format

**Goal**
Freeze the data schema early.

**Detailed Description**
Every successful proof becomes training data and compression input. Define a stable JSONL (or msgpack) schema for: theorem id, initial state, action sequence, intermediate states, backend metadata, timing, and outcome. Include versioning to handle future changes.

**Inputs**

* Search engine produces traces

**Outputs**

* `Trajectory` schema + serializer
* Backward-compatible versioning rules

**Success Criteria**

* Can load logs from older runs after refactors
* Can replay a saved trace in the backend

**Estimated Effort**
1 week.

**Key Risks**

* Schema churn destroys your dataset
* Missing fields make later analysis impossible

**Failure Indicators**

* You can’t answer “what changed between run A and B?”

**Dependencies**
Phases 1,6.

**Sub-phases/Steps**

1. Define core entities + IDs
2. Add schema versioning
3. Implement replay test

---

## Phase 9: Evaluation harness v0

**Goal**
Make learning measurable from day 1.

**Detailed Description**
Define evaluation as: given a fixed set of theorems and a fixed search budget, measure solve rate, nodes expanded, and proof length. This gives immediate feedback for every subsequent change. Tie this into your run logger so plots are automatic.

**Inputs**

* Benchmark suite (Phase 7)
* Search (Phase 6)

**Outputs**

* `Evaluator` module with metrics
* Hold-out set and reporting

**Success Criteria**

* Every run prints eval metrics
* Metrics are stable across repeats

**Estimated Effort**
1 week.

**Key Risks**

* “Evaluation leakage” (using eval tasks in training)
* Metrics too noisy

**Failure Indicators**

* Eval solve rate varies wildly at same seed/budget

**Dependencies**
Phases 6–8.

**Sub-phases/Steps**

1. Freeze eval split
2. Define budgets and timeouts
3. Implement reporting and log to JSONL

---

## Phase 10: Forward theorem generation v0

**Goal**
Escape fixed datasets by generating infinite tasks.

**Detailed Description**
Implement the core AlphaZero-style trick: sample a random well-typed proof term `t`, let Lean infer its type `T`, discard `t`, and then challenge your prover to prove `T` . Start with tiny term grammars and strong rejection sampling. Track the distribution of theorem sizes and acceptance rates.

**Inputs**

* Lean backend that can typecheck/infers type
* Toy domain definitions

**Outputs**

* `TheoremGenerator` (term sampler)
* Theorem store + de-dup
* Difficulty estimator for generated theorems

**Success Criteria**

* Generates thousands of unique theorems/day
* Nontrivial fraction are solvable by baseline search
* You can stratify by difficulty

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Term sampling almost never produces well-typed terms
* Generated theorems collapse to trivialities

**Failure Indicators**

* Acceptance rate < 0.01% without clear path to improve
* Theorem entropy is low; duplicates dominate

**Dependencies**
Phases 2,4,7.

**Sub-phases/Steps**

1. Define a term grammar aligned to domain
2. Implement rejection sampling with size bounds
3. Cache successful term templates
4. De-dup theorem types via normalization/hashing

---

## Phase 11: Hindsight experience replay

**Goal**
Turn every successful proof into many training tasks.

**Detailed Description**
For each successful trajectory, every intermediate state becomes a valid training example: “from here, the remaining suffix of actions is a valid solution.” This massively amplifies data from scarce successes and is explicitly part of the convergent design .

**Inputs**

* Trajectory logs (Phase 8)

**Outputs**

* `HERBuilder` that yields (state, next_action) pairs
* Optional “subgoal tasks” dataset

**Success Criteria**

* Data volume increases by ~O(proof length)
* Training sets can be regenerated deterministically from raw logs

**Estimated Effort**
1–2 weeks.

**Key Risks**

* Bugs in state identity cause wrong labels
* Data imbalance (too many near-terminal states)

**Failure Indicators**

* Training improves “last-step accuracy” but not solve rate

**Dependencies**
Phase 8.

**Sub-phases/Steps**

1. Define state IDs in logs
2. Build state→action extraction
3. Balance sampling by depth

---

## Phase 12: Dataset and replay buffer

**Goal**
Scalable storage and sampling of training data.

**Detailed Description**
Implement an on-disk dataset format (sharded JSONL, msgpack, or parquet) and a replay buffer sampler that supports: uniform sampling, priority by difficulty, and “recent vs old” mixing. Add dataset statistics for debugging (class imbalance, opcode frequencies).

**Inputs**

* HER data (Phase 11)

**Outputs**

* `ReplayBuffer` + `DatasetIndex`
* Data sampling policies

**Success Criteria**

* Can train without loading entire corpus into RAM
* Sampling reproducible by seed

**Estimated Effort**
1–2 weeks.

**Key Risks**

* IO bottlenecks
* Corrupt shards

**Failure Indicators**

* Training throughput collapses as corpus grows

**Dependencies**
Phases 8,11.

**Sub-phases/Steps**

1. Choose storage format + schema
2. Implement indexing + sampling
3. Add dataset validation tool

---

## Phase 13: Representation IR scaffolding

**Goal**
Stop treating proof states as strings; start building a typed internal IR.

**Detailed Description**
Define an internal representation for Lean expressions/goals: constants, applications, binders, inductives, etc. Initially, accept partial coverage: parse only what your starter domain emits. The output is a graph-friendly IR that can be hash-consed and normalized later.

**Inputs**

* ProofState serializer (Phase 4)

**Outputs**

* `Expr` node types + constructors
* Parser/translator from Lean backend output to IR (partial)

**Success Criteria**

* For the toy domain, 95%+ of states translate successfully
* Translation is deterministic and logged on failure

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Lean syntax complexity
* Parser brittleness

**Failure Indicators**

* Frequent “unparsed state” errors on normal tasks

**Dependencies**
Phases 4,7.

**Sub-phases/Steps**

1. Define IR node taxonomy
2. Implement translator for toy domain shapes
3. Add fallbacks and logging

---

## Phase 14: Hash-consing store

**Goal**
Intern identical subexpressions once to enable caching and reuse.

**Detailed Description**
Implement a hash-consed DAG store: every unique `Expr` node is stored once, keyed by a structural hash (“Merkle DAG”). This matches the convergent architecture’s state representation idea  and enables fast equality, memoization, and cheap delta updates later.

**Inputs**

* IR node types (Phase 13)

**Outputs**

* `ExprStore` (intern table)
* Stable node IDs + hash computation

**Success Criteria**

* Identical expressions across states share node IDs
* Hash collisions are either cryptographically negligible or explicitly checked

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Poor hashing causes collisions and incorrect caching
* Memory growth

**Failure Indicators**

* Store grows ~linearly with steps even on repetitive tasks

**Dependencies**
Phase 13.

**Sub-phases/Steps**

1. Choose hash function + encoding
2. Implement interning + refcounts
3. Add debug “intern stats” metrics

---

## Phase 15: De Bruijn normalization

**Goal**
Canonicalize alpha-equivalent terms.

**Detailed Description**
Implement De Bruijn indices so `∀x, P x` and `∀y, P y` become structurally identical in memory, unlocking generalization and caching benefits . This is delicate: binder depth, variable shifts, and substitution must be correct or everything breaks.

**Inputs**

* Hash-consed IR (Phase 14)

**Outputs**

* `normalize_debruijn(expr)`
* Regression tests for alpha-equivalence

**Success Criteria**

* Alpha-equivalent expressions hash identically
* Unit tests cover tricky binder nesting

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Off-by-one binder bugs
* Variable capture issues

**Failure Indicators**

* “Same theorem” appears as different IDs frequently
* Rewrite/intro correctness issues downstream

**Dependencies**
Phase 14.

**Sub-phases/Steps**

1. Define binder semantics precisely
2. Implement shifting and substitution utilities
3. Add property tests (alpha invariance)

---

## Phase 16: Graph extraction for proof state

**Goal**
Convert a full proof state (context + goals) into a graph for the GNN.

**Detailed Description**
Decide what subgraph to extract around the current goal: include goal expression, hypothesis expressions, and link nodes via “appears-in” edges. Build a graph object with node features (kind, constant ID, binder depth) and edges (child, binder, hypothesis membership).

**Inputs**

* Normalized hash-consed expressions (Phases 14–15)

**Outputs**

* `StateGraph` builder
* Graph statistics logging

**Success Criteria**

* Graph builder is fast and deterministic
* Graph sizes are bounded by configurable cutoffs

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Graphs too large → GNN too slow
* Graph loses key info → policy can’t learn

**Failure Indicators**

* Model accuracy stagnates even on easy tasks
* Huge variance in graph size

**Dependencies**
Phase 15.

**Sub-phases/Steps**

1. Define edge types and node features
2. Implement graph extraction with size limits
3. Add graph visualization/debug dumps

---

## Phase 17: GNN model v0

**Goal**
Build the first learnable policy network from scratch.

**Detailed Description**
Implement a small message-passing network (MPNN) consistent with the convergent architecture . Start minimal: embed node features, run K message-passing steps, pool to a state embedding, and output opcode logits.

**Inputs**

* State graphs (Phase 16)
* Training data (Phase 11–12)

**Outputs**

* `PolicyNetGNN` v0
* Forward pass unit tests and shape checks

**Success Criteria**

* Training loss decreases on a fixed dataset
* Overfits a tiny dataset (sanity check)

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Implementation bugs in PyG
* MPS backend quirks on Mac

**Failure Indicators**

* Cannot overfit a tiny dataset
* NaNs or exploding gradients

**Dependencies**
Phases 12,16.

**Sub-phases/Steps**

1. Implement embeddings and message passing
2. Add pooling and opcode head
3. Add training sanity tests

---

## Phase 18: Action heads and pointer args

**Goal**
Select not just which opcode, but also arguments (hypothesis/lemma pointers).

**Detailed Description**
For ops like EXACT/APPLY/CASES/REWRITE, you must select a target from a set (local hyps, retrieved lemmas). Implement pointer heads: logits over candidate indices. This is essential for realistic proving.

**Inputs**

* GNN v0 (Phase 17)
* ProofState context extraction

**Outputs**

* Multi-head policy: opcode head + pointer heads
* Masking logic for invalid candidates

**Success Criteria**

* Correct masking (no illegal selections)
* Loss decomposes cleanly per head

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Candidate set too large
* Pointer head training unstable

**Failure Indicators**

* Model predicts illegal candidates frequently
* Pointer accuracy near random baseline

**Dependencies**
Phase 17.

**Sub-phases/Steps**

1. Define candidate lists per op
2. Implement masked softmax
3. Add pointer-label generation from traces

---

## Phase 19: Imitation training loop v0

**Goal**
Train policy by imitating successful search traces.

**Detailed Description**
Implement a full training loop: dataloader → forward → loss → optimizer → checkpointing → eval. Track metrics (loss, accuracy, entropy) and tie it into your run logger.

**Inputs**

* Dataset (Phase 12)
* Policy model (Phase 17–18)

**Outputs**

* `Trainer` with checkpointing
* Training curves logged per run

**Success Criteria**

* Training improves action prediction accuracy on held-out transitions
* Checkpoints load and reproduce eval

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Data leakage
* Overfitting to easy states

**Failure Indicators**

* Accuracy up, solve rate unchanged
* Eval metrics unstable

**Dependencies**
Phase 18.

**Sub-phases/Steps**

1. Implement checkpoint format + resume
2. Add eval on held-out transitions
3. Connect to end-to-end evaluation (Phase 9)

---

## Phase 20: Guided search integration

**Goal**
Use the learned policy to guide proof search.

**Detailed Description**
Replace unguided expansions with policy-ranked expansions. Keep a fallback to brute search for exploration. Define a stable search budget and measure solve rate improvements at fixed budget.

**Inputs**

* Search engine (Phase 6)
* Policy model (Phase 19)

**Outputs**

* `GuidedSearchEngine`
* Comparison reports vs unguided baseline

**Success Criteria**

* Solve rate increases at fixed node/time budget
* Search expands fewer nodes for solved theorems

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Policy collapses exploration
* Search becomes brittle (gets stuck)

**Failure Indicators**

* Solve rate decreases relative to unguided baseline
* Search loops or repeats similar states

**Dependencies**
Phases 6,19.

**Sub-phases/Steps**

1. Rank actions by policy logits
2. Add exploration noise/epsilon
3. Add fallback beam/BFS mixture

---

## Phase 21: Levin MDL search priority

**Goal**
Make search cost align with description length.

**Detailed Description**
Implement Levin/MDL search where node priority reflects cumulative code length, e.g., Σ(-log π(action|state)) . This makes search naturally prefer “short explanations” and sets up MDL integration.

**Inputs**

* Guided search framework (Phase 20)

**Outputs**

* Priority queue search using MDL cost
* Logging of cost decomposition

**Success Criteria**

* Search becomes more efficient on average
* Costs correlate with proof length/complexity

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Poor calibration of probabilities
* Cost scaling issues

**Failure Indicators**

* Search degenerates into shallow greedy behavior
* No improvement over plain beam

**Dependencies**
Phase 20.

**Sub-phases/Steps**

1. Define cost function precisely
2. Implement PQ + reopen policy
3. Add calibration diagnostics

---

## Phase 22: Stable curriculum scheduling

**Goal**
Prevent generator collapse and keep tasks near the frontier.

**Detailed Description**
Define a curriculum controller: select theorems whose predicted difficulty yields ~30–70% success probability. If success is too high, increase difficulty; too low, back off. Detect collapse where generator outputs trivial or impossible tasks.

**Inputs**

* Evaluation harness
* Theorem generator v0 (Phase 10)

**Outputs**

* `CurriculumManager`
* Difficulty bins + sampling distributions

**Success Criteria**

* Training stays in a productive regime (nonzero success, nontrivial tasks)
* Difficulty distribution shifts upward over time

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Feedback loop instability
* Difficulty metric is wrong

**Failure Indicators**

* Sudden drop to near-0 success for long periods
* Theorem entropy collapses

**Dependencies**
Phases 9–10,20.

**Sub-phases/Steps**

1. Define difficulty measures
2. Implement success-rate controller
3. Add collapse detectors

---

## Phase 23: Baselines suite

**Goal**
Make “learning” claims falsifiable.

**Detailed Description**
Build baselines: random action policy, heuristic-only (handwritten), unguided BFS/beam, guided but untrained, etc. This prevents self-deception and supports ablations later.

**Inputs**

* Search engine
* Eval harness

**Outputs**

* `BaselineRunner`
* Baseline reports stored per run

**Success Criteria**

* Every eval report includes baseline comparisons
* Baselines are deterministic and reproducible

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Baselines too weak/too strong to be informative

**Failure Indicators**

* You can’t tell whether a change helped

**Dependencies**
Phase 9.

**Sub-phases/Steps**

1. Implement random baseline
2. Implement heuristic baseline
3. Implement unguided and guided-with-random-scores baselines

---

## Phase 24: Macro representation

**Goal**
Represent compiled proof programs as first-class actions.

**Detailed Description**
A macro is a sequence of primitive DSL actions with parameters. Define how macros bind parameters (e.g., “the hypothesis chosen at step 2 is the one introduced at step 1”), how they typecheck, how they expand, and how they are serialized. This is the substrate for the Macro Compiler idea .

**Inputs**

* DSL v0
* Trace logs

**Outputs**

* `Macro` dataclass + typing rules
* Macro expansion engine

**Success Criteria**

* A macro can be executed and replayed reliably
* Macros can be nested (with depth limit)

**Estimated Effort**
1–2 weeks.

**Key Risks**

* Parameter binding is brittle
* Macro expansion explodes search space

**Failure Indicators**

* Macros often fail to replay on similar states

**Dependencies**
Phases 5,8.

**Sub-phases/Steps**

1. Define macro parameterization scheme
2. Implement expansion and static checks
3. Add macro replay tests

---

## Phase 25: Trace mining v0

**Goal**
Extract reusable patterns from successful traces.

**Detailed Description**
Implement mining to find repeated subsequences of actions (and optionally state patterns). Start with simple n-gram frequency over opcode sequences and extend to parameter-aware patterns.

**Inputs**

* Stored trajectories

**Outputs**

* Frequency tables
* Candidate macro proposals

**Success Criteria**

* Finds nontrivial patterns used across many proofs
* Candidates are replayable frequently

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Spurious patterns that don’t generalize
* Ignores parameters and fails

**Failure Indicators**

* Proposed macros rarely pass replay checks

**Dependencies**
Phases 8,24.

**Sub-phases/Steps**

1. Build opcode n-gram miner
2. Add parameter abstraction
3. Build candidate ranking metrics

---

## Phase 26: Grammar compression engine

**Goal**
Compress trace corpora into a macro library.

**Detailed Description**
Implement Sequitur or BPE-style grammar compression on action sequences, exactly as in the convergent plan . The output is a set of macro rules that can re-express traces more compactly.

**Inputs**

* Trace mining (Phase 25)

**Outputs**

* `GrammarCompressor` producing macro candidates
* Compression statistics (bits saved)

**Success Criteria**

* Compression reduces description length of training traces measurably
* Candidate macros are replayable and typed

**Estimated Effort**
3–6 weeks.

**Key Risks**

* Compression optimizes corpus encoding but harms generalization
* Implementation complexity

**Failure Indicators**

* Compression savings exist but solve rate doesn’t improve

**Dependencies**
Phase 25.

**Sub-phases/Steps**

1. Implement Sequitur/BPE core
2. Add parameter-aware tokenization
3. Output macros in your DSL format

---

## Phase 27: MDL accounting system

**Goal**
Make “intelligence = compression” executable.

**Detailed Description**
Implement explicit MDL: `Total_MDL = L(Library) + Σ L(proof_i | Library)` . You need a coding scheme for actions/macros, a cost for adding a macro to the library, and a way to compute proof code length given the library. This becomes the objective used for macro admission and pruning.

**Inputs**

* Macro library format (Phase 24–26)

**Outputs**

* `MDLModel` with encoders/decoders and bit-length computations
* Reports: MDL breakdown per run

**Success Criteria**

* MDL numbers are stable and interpretable
* Adding a useless macro increases MDL; adding a useful macro decreases held-out MDL

**Estimated Effort**
3–6 weeks.

**Key Risks**

* Mis-specified coding scheme → wrong incentives
* Hard to compute MDL efficiently

**Failure Indicators**

* MDL decreases while solve rate stagnates (“fake compression”)

**Dependencies**
Phase 26.

**Sub-phases/Steps**

1. Define coding scheme (actions, pointers, macros)
2. Implement library cost model
3. Implement proof cost model
4. Add held-out MDL evaluation

---

## Phase 28: Macro acceptance gate

**Goal**
Admit macros only if they pay off on held-out tasks.

**Detailed Description**
Implement the admission rule: propose macro → evaluate ΔMDL on a held-out set → admit only if ΔMDL < 0 . This is the key guardrail that prevents library bloat and overfitting.

**Inputs**

* MDL model (Phase 27)

**Outputs**

* `MacroGate` acceptance test
* Macro library versioning

**Success Criteria**

* Macro count grows slowly and only when justified
* Held-out MDL improves over time

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Held-out set not representative
* Too strict gate stalls progress

**Failure Indicators**

* Macro library explodes
* Or macro library never grows at all

**Dependencies**
Phase 27.

**Sub-phases/Steps**

1. Define held-out set strategy
2. Implement ΔMDL evaluator
3. Implement admission + rollback

---

## Phase 29: Macro execution in search

**Goal**
Use macros as atomic actions to accelerate proving.

**Detailed Description**
Integrate macros into the search action generator. Allow search to choose between primitives and macros. Implement expansion strategies: inline fully, or treat as a “program call” with internal stepping for backtracking. Track how many nodes are saved.

**Inputs**

* Search engine
* Macro library

**Outputs**

* `MacroAwareSearch`
* Metrics: macro usage, speedup, failure rate

**Success Criteria**

* Search node expansions drop for tasks where macros apply
* Solve rate improves at fixed budget

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Macro failures waste budget
* Macro application conditions too hard to detect

**Failure Indicators**

* Macros used rarely or harm solve rate

**Dependencies**
Phases 24,28.

**Sub-phases/Steps**

1. Add macro candidates to action list
2. Implement macro “call” semantics
3. Add macro-specific backtracking strategy

---

## Phase 30: Lemma library v0

**Goal**
Turn discovered theorems into reusable lemmas.

**Detailed Description**
Beyond macros (procedural), you will also cache proven theorems (declarative). Store lemma statements, proofs, usage stats, and embeddings/hashes for retrieval. This is the start of the “lemma economy” .

**Inputs**

* Successful proofs and theorem generator

**Outputs**

* `LemmaDB` with metadata + versioning
* Export/import of lemma library

**Success Criteria**

* Lemmas can be applied by APPLY/EXACT
* Library remains consistent across runs

**Estimated Effort**
2–3 weeks.

**Key Risks**

* Library duplicates or near-duplicates
* Lemmas are too specific and not reused

**Failure Indicators**

* Lemma reuse rate near zero

**Dependencies**
Phases 10,20.

**Sub-phases/Steps**

1. Define lemma identity and hashing
2. Store proofs and statements
3. Track reuse stats

---

## Phase 31: Retrieval index v0

**Goal**
Fast lemma/macro lookup at inference time.

**Detailed Description**
Implement an index to retrieve candidate lemmas/macros based on the current goal/hypothesis structure. The convergent plan suggests SimHash for constant-time lookup ; start with a simple embedding + cosine similarity or SimHash on structural features.

**Inputs**

* Lemma DB (Phase 30)
* State representation (Phase 16)

**Outputs**

* `Retriever` interface + index implementation
* Retrieval metrics: hit rate, latency

**Success Criteria**

* Retrieval returns small candidate set with high utility
* Retrieval latency is low compared to backend step

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Retrieval too noisy → search slows
* Retrieval too strict → misses useful lemmas

**Failure Indicators**

* APPLY/EXACT almost never uses retrieved lemmas successfully

**Dependencies**
Phase 30.

**Sub-phases/Steps**

1. Define feature hash for goals
2. Implement SimHash / ANN
3. Evaluate retrieval quality

---

## Phase 32: MDL lemma economy pruning

**Goal**
Keep the library small and high-quality.

**Detailed Description**
Implement “rent collection”: every macro/lemma must justify its existence by continued MDL savings and reuse . If a macro isn’t used (or doesn’t reduce MDL on held-out), prune it. This prevents bloat and forces taste.

**Inputs**

* MDL model (Phase 27)
* Library with usage stats

**Outputs**

* Pruning policy + garbage collector
* Library snapshots per epoch

**Success Criteria**

* Library size stabilizes
* Held-out MDL doesn’t degrade over time

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Pruning removes stepping stones needed later
* Oscillations: add then prune repeatedly

**Failure Indicators**

* Library churn is high
* Solve rate regresses after pruning

**Dependencies**
Phase 28,30.

**Sub-phases/Steps**

1. Define usage and MDL thresholds
2. Implement pruning with rollback
3. Add library-diff tools

---

## Phase 33: Wake phase pipeline

**Goal**
Automate “online life”: generate tasks, search, log traces.

**Detailed Description**
Implement the Wake phase described in the convergent plan : sample/generate theorems, attempt proofs under budget, store successes/failures, and produce data for training and compression.

**Inputs**

* Theorem generator
* Search engine
* Logging/dataset

**Outputs**

* `WakeRunner` orchestrator
* Daily/epoch summaries

**Success Criteria**

* Produces a steady stream of successful proofs
* Logs are stable and complete

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Generator produces mostly unsolved tasks → no data
* Backend becomes bottleneck

**Failure Indicators**

* Success count near zero for long spans

**Dependencies**
Phases 10,20.

**Sub-phases/Steps**

1. Integrate generator with curriculum controller
2. Run search and capture trajectories
3. Export summary stats and checkpoints

---

## Phase 34: Sleep phase pipeline

**Goal**
Automate “offline compression”: mine traces, propose macros, MDL gate, prune.

**Detailed Description**
Implement the Sleep phase : run grammar compression on accumulated traces, propose new macros, evaluate ΔMDL on held-out, admit/prune accordingly, and snapshot the updated library.

**Inputs**

* Trace corpus
* Grammar compressor
* MDL gate

**Outputs**

* `SleepRunner`
* Macro proposal reports + accepted macros

**Success Criteria**

* Sleep step results in net held-out MDL improvement sometimes
* Macro growth is controlled (e.g., cap/day, as suggested) 

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Compression finds patterns that don’t help proving
* Gate mis-specified; admits junk

**Failure Indicators**

* Macro library grows but reuse stays low
* Held-out MDL worsens

**Dependencies**
Phases 26–28.

**Sub-phases/Steps**

1. Implement compression run on recent traces
2. Propose candidates and evaluate
3. Update library and rerun eval

---

## Phase 35: Full wake sleep loop

**Goal**
End-to-end self-improving cycle.

**Detailed Description**
Combine Wake and Sleep into a repeating loop: Wake generates experience and updates the model; Sleep compresses and updates the library; the updated library makes future Wake more efficient; repeat. This is where “learning” should become visible in solve-rate and MDL curves .

**Inputs**

* Wake runner
* Sleep runner
* Trainer

**Outputs**

* `LoopRunner` that executes epochs
* Longitudinal plots

**Success Criteria**

* Solve rate increases at fixed budget across epochs
* Average proof MDL decreases across epochs 
* Macro reuse increases on unseen tasks 

**Estimated Effort**
2–6 weeks.

**Key Risks**

* System oscillates or collapses
* Improvements are not reproducible

**Failure Indicators**

* No monotonic trend after many epochs
* Generalization gap increases

**Dependencies**
Phases 19,33,34.

**Sub-phases/Steps**

1. Define epoch schedule
2. Add checkpointing at each stage
3. Add automatic regression alarms

---

## Phase 36: Delta-state embedding v0

**Goal**
Make inference cheap by updating embeddings incrementally.

**Detailed Description**
Implement the delta-state reasoning idea: maintain a persistent embedding for the proof state and update it from the delta (what changed) rather than re-encoding everything . This requires cacheable graph encoding and a way to identify changed nodes.

**Inputs**

* Hash-consed DAG with stable node IDs
* GNN encoder

**Outputs**

* `DeltaEncoder` interface
* Cache keyed by node hash/version

**Success Criteria**

* Measured speedup in state encoding cost
* Correctness: delta updates match full recompute within tolerance

**Estimated Effort**
3–6 weeks.

**Key Risks**

* Cache invalidation bugs
* Complexity outweighs speed gains

**Failure Indicators**

* Encodings drift; policy performance degrades
* Cache hit rate low

**Dependencies**
Phases 14–17.

**Sub-phases/Steps**

1. Define delta representation
2. Implement cache keys and invalidation
3. Validate against full recompute

---

## Phase 37: Cached message passing

**Goal**
Only recompute embeddings for changed subgraphs.

**Detailed Description**
Implement incremental message passing on the graph: if only a small part of the proof state changed, reuse cached node embeddings for unchanged nodes. This is the concrete “O(changed edges)” benefit promised by delta-state reasoning .

**Inputs**

* Delta encoder v0

**Outputs**

* `IncrementalMPNN` implementation
* Cache statistics and profiling

**Success Criteria**

* High cache hit rate on typical proof steps
* Stable speedups in guided search

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Graph cut selection incorrect
* Memory blow-up from caching too much

**Failure Indicators**

* Cache grows without bound
* No speedup observed

**Dependencies**
Phase 36.

**Sub-phases/Steps**

1. Identify affected nodes via parent pointers
2. Implement recompute frontier
3. Add cache eviction policy

---

## Phase 38: Delta-code discretization

**Goal**
Compress state deltas into discrete codes for MDL and speed.

**Detailed Description**
Implement discrete delta coding: either 64-bit delta codes (autoencoder) or VQ-VAE codebook (K=64–512) as suggested by the convergent insights . The goal is to make deltas compressible and searchable.

**Inputs**

* Delta representation (Phase 36)

**Outputs**

* `DeltaCodec` (encode/decode)
* Codebook training pipeline

**Success Criteria**

* Deltas reconstruct sufficiently for policy performance
* Code distribution has good entropy (not collapsed)

**Estimated Effort**
3–8 weeks.

**Key Risks**

* Codebook collapse
* Reconstruction loses crucial semantics

**Failure Indicators**

* Policy performance drops sharply using codes
* Codes use only a few entries

**Dependencies**
Phase 36.

**Sub-phases/Steps**

1. Implement baseline autoencoder codec
2. Add VQ discretization
3. Evaluate codec vs full delta

---

## Phase 39: Multi-policy exploration

**Goal**
Avoid mode collapse by maintaining diverse policies.

**Detailed Description**
Implement either an ensemble of 2–4 policies or a small population as recommended . Use different seeds, exploration temperatures, and perhaps different inductive biases. Aggregate for search guidance and data generation.

**Inputs**

* Trainer and policy

**Outputs**

* `PolicyPool` + aggregation rules
* Diversity metrics

**Success Criteria**

* Higher solve rate / better coverage than single policy
* Diversity persists (policies don’t converge identically)

**Estimated Effort**
2–6 weeks.

**Key Risks**

* Compute overhead on laptop
* Complexity in orchestration

**Failure Indicators**

* No improvement over single best policy
* Training becomes unstable

**Dependencies**
Phase 20.

**Sub-phases/Steps**

1. Define pool training regimen
2. Implement search-time aggregation
3. Add diversity metrics and alarms

---

## Phase 40: Generator improvements

**Goal**
Make theorem generation robust and frontier-seeking.

**Detailed Description**
Add multiple generators (proof-term sampling + subgoal harvesting), as suggested . Subgoal harvesting means: collect intermediate goals from proofs and mutate them to create new tasks. The aim is to create a rich curriculum without human data.

**Inputs**

* Existing theorem generator
* Trajectory corpus

**Outputs**

* `MultiGenerator`
* Mutation operators and novelty checks

**Success Criteria**

* Task diversity increases
* Difficulty distribution can be controlled

**Estimated Effort**
4–8 weeks.

**Key Risks**

* Mutation creates ill-typed/unprovable theorems
* Generator collapses to easy tasks

**Failure Indicators**

* Acceptance rates crater
* Novelty metrics flatten

**Dependencies**
Phase 10,33.

**Sub-phases/Steps**

1. Implement subgoal harvesting pipeline
2. Implement mutations and filtering
3. Integrate with curriculum controller

---

## Phase 41: Generator–compressor coevolution

**Goal**
Create a self-play game: generator tries to defeat prover, compressor tries to simplify.

**Detailed Description**
Implement an adversarial dynamic: generator is rewarded for producing tasks that are just beyond current capability; prover is rewarded for solving; compressor is rewarded for reducing MDL by compiling useful macros . This prevents stagnation and keeps pressure on abstraction formation.

**Inputs**

* Wake/sleep loop
* Generator improvements

**Outputs**

* `CoevolutionManager`
* Difficulty targeting and anti-collapse safeguards

**Success Criteria**

* Frontier difficulty increases steadily
* Solve-rate on older tiers remains high

**Estimated Effort**
4–10 weeks.

**Key Risks**

* Instability and oscillations
* Generator finds pathological “hard but useless” tasks

**Failure Indicators**

* Prover success collapses for long periods
* MDL improves but eval solve rate doesn’t

**Dependencies**
Phase 35,40.

**Sub-phases/Steps**

1. Define generator reward signal
2. Implement gating by novelty and relevance
3. Stabilize with population/ensembles

---

## Phase 42: Equality and rewrite robustness

**Goal**
Make REWRITE a reliable workhorse.

**Detailed Description**
Equality reasoning is central to real math. Strengthen REWRITE: handle rewriting under binders safely, manage congruence contexts, and build heuristics for selecting rewrite positions. Extend IR to represent equality proofs cleanly.

**Inputs**

* Stable IR + hashing
* DSL with REWRITE

**Outputs**

* Robust rewrite engine and candidate selection
* Tests covering binder edge cases

**Success Criteria**

* Rewrite works reliably on generated equality tasks
* Solve rate increases on equality-heavy tier

**Estimated Effort**
4–8 weeks.

**Key Risks**

* Variable capture bugs
* Explosion in rewrite candidates

**Failure Indicators**

* Frequent backend failures on rewrite
* Search slows dramatically

**Dependencies**
Phase 15,18.

**Sub-phases/Steps**

1. Implement safe rewrite with De Bruijn
2. Add candidate selection heuristics
3. Add rewrite-focused curriculum

---

## Phase 43: Induction phase 1

**Goal**
Introduce induction for simple Nat theorems.

**Detailed Description**
Implement INDUCTION (and supporting primitives) and start proving basic Nat properties. This matches the DSL primitive list . You’ll need a curriculum that generates induction-requiring theorems.

**Inputs**

* Stable search and policy
* Nat fragment definitions

**Outputs**

* Induction-capable backend mapping
* Induction task generator

**Success Criteria**

* Solves a suite of simple induction theorems
* Learns induction patterns (not brute force)

**Estimated Effort**
4–10 weeks.

**Key Risks**

* Search depth explodes
* Induction produces many subgoals

**Failure Indicators**

* Near-zero induction theorem solve rate
* Proof lengths explode without macro help

**Dependencies**
Phase 35.

**Sub-phases/Steps**

1. Implement induction action semantics
2. Generate induction tasks
3. Add induction-specific macros

---

## Phase 44: Induction phase 2

**Goal**
Handle recursion schemas and stronger invariants.

**Detailed Description**
Expand beyond trivial induction: nested induction, induction on structures, and lemmas requiring auxiliary invariants. This is where macros and lemma economy become crucial: you compile recurring induction “skeletons.”

**Inputs**

* Phase 43 induction working

**Outputs**

* Expanded induction DSL patterns
* Macro library that captures induction skeletons

**Success Criteria**

* Solve rate improves on harder induction tasks
* Reuse of induction macros rises

**Estimated Effort**
6–12 weeks.

**Key Risks**

* Curriculum becomes too hard too fast
* Macro bloat

**Failure Indicators**

* Training collapses; generator stuck
* Library size explodes

**Dependencies**
Phase 43.

**Sub-phases/Steps**

1. Add richer induction targets
2. Add lemma synthesis for invariants
3. Tighten MDL gating

---

## Phase 45: Lemma synthesis beyond macros

**Goal**
Actively propose new declarative lemmas.

**Detailed Description**
Move from “discover macros from traces” to “propose new lemmas” via pattern mining, anti-unification, and goal decomposition. Every lemma is verified by Lean, indexed, and subjected to the MDL economy.

**Inputs**

* Lemma DB and retrieval
* Wake/sleep loop

**Outputs**

* `LemmaProposer` + verification pipeline
* Lemma gating by held-out utility

**Success Criteria**

* New lemmas are reused across unrelated theorems
* Held-out solve rate improves with lemma additions

**Estimated Effort**
6–12 weeks.

**Key Risks**

* Lemma proposals are too specific
* Verification cost too high

**Failure Indicators**

* Lemma reuse stays low
* MDL worsens with lemma additions

**Dependencies**
Phase 30–35.

**Sub-phases/Steps**

1. Anti-unify similar goals to propose lemmas
2. Verify and store lemmas
3. Integrate into retrieval and search

---

## Phase 46: Metric-learning retrieval head

**Goal**
Add macros/lemmas without retraining the whole policy.

**Detailed Description**
Implement a metric-learning retrieval head so you can add new library items and immediately retrieve them via embedding similarity, as suggested . This decouples library growth from policy retraining.

**Inputs**

* Retrieval system
* Policy embeddings

**Outputs**

* Learned embedding space for goals and lemmas
* Retrieval quality metrics

**Success Criteria**

* Retrieval adapts to new lemmas quickly
* Solve rate benefits from new library additions faster

**Estimated Effort**
4–10 weeks.

**Key Risks**

* Embedding drift
* Hard negative sampling issues

**Failure Indicators**

* Retrieval quality degrades as library grows

**Dependencies**
Phase 31.

**Sub-phases/Steps**

1. Define contrastive objective
2. Train goal/lemma embeddings
3. Evaluate retrieval and integrate into search

---

## Phase 47: Robust evaluation and holdouts

**Goal**
Prevent “self-play overfitting.”

**Detailed Description**
Create multiple holdouts: (a) fixed hand-written suite, (b) generator-seeded but frozen set, (c) domain shift set (different constructors). Add regression tests: improvements must hold across holdouts.

**Inputs**

* Full training loop

**Outputs**

* Multiple eval suites
* Regression gating (fail build if regress)

**Success Criteria**

* Generalization improvements are demonstrated
* No leakage detected

**Estimated Effort**
2–4 weeks.

**Key Risks**

* Holdouts not truly independent
* Overhead slows iteration

**Failure Indicators**

* Train solve rate rises, holdout flatlines

**Dependencies**
Phase 35.

**Sub-phases/Steps**

1. Freeze holdout generators/seeds
2. Implement eval harness expansions
3. Add regression alarms

---

## Phase 48: Performance engineering pass

**Goal**
Make the whole system fast enough on a laptop.

**Detailed Description**
Profile everything: backend calls, graph building, model inference, search queue operations, IO. Add batching, caching, parallel envs, and careful process management. Consider “N backends in parallel” to amortize Lean overhead.

**Inputs**

* End-to-end loop works

**Outputs**

* Profiling reports
* Optimized hot paths
* Parallel execution capability

**Success Criteria**

* ≥2–10× throughput improvement in proofs/hour
* Stable memory usage

**Estimated Effort**
4–10 weeks.

**Key Risks**

* Concurrency breaks determinism
* Lean backend not parallel-friendly

**Failure Indicators**

* Performance regresses over time
* Frequent deadlocks/timeouts

**Dependencies**
Phase 35.

**Sub-phases/Steps**

1. Add structured profiling instrumentation
2. Optimize graph extraction and caching
3. Add parallel workers for search

---

## Phase 49: Long-horizon search stability

**Goal**
Handle deeper proofs reliably.

**Detailed Description**
Introduce value heads, better pruning, beam re-ranking, and possibly lightweight MCTS. Add cycle detection and subgoal caching. This phase is about avoiding exponential blowups on deeper problems.

**Inputs**

* Guided search and delta-state encoding

**Outputs**

* Value-guided search variants
* Depth-scaled budget policies

**Success Criteria**

* Solve rate improves on deeper tiers without exploding compute
* Proof depth frontier increases over time

**Estimated Effort**
4–12 weeks.

**Key Risks**

* Value learning unstable
* Search heuristics bias incorrectly

**Failure Indicators**

* Search becomes slower with no solve gain
* “Thrashing” among similar subgoals

**Dependencies**
Phases 20,36.

**Sub-phases/Steps**

1. Add value head and training targets
2. Integrate value into search priority
3. Add subgoal caching

---

## Phase 50: Proof artifact compilation

**Goal**
Turn proofs/macros into Lean source artifacts.

**Detailed Description**
Implement compilation: from action traces/macro bytecode to Lean `by` scripts or tactic blocks, plus library export. This makes tlq0’s learned intelligence portable, inspectable, and shareable—literally a growing library.

**Inputs**

* Stable macros/lemmas

**Outputs**

* Lean source emitter
* `lean/Generated/` files with compiled artifacts

**Success Criteria**

* Emitted Lean proofs compile independently
* Macro library export/import works across runs

**Estimated Effort**
2–6 weeks.

**Key Risks**

* Backend tactics don’t correspond 1:1 to Lean syntax
* Compilation brittle under toolchain changes

**Failure Indicators**

* Many proofs only work inside the interactive environment, not as source

**Dependencies**
Phase 30+.

**Sub-phases/Steps**

1. Define canonical emission format
2. Implement emitter for primitives and macros
3. Add compile-check CI

---

## Phase 51: Research-grade ablations

**Goal**
Prove which components matter.

**Detailed Description**
Run systematic ablations: remove macros, remove MDL gate, remove De Bruijn normalization, remove delta-state caching, swap search algorithms, etc. Report effects on solve rate, MDL, proof length, and generalization. This phase produces clarity and prevents cargo-culting.

**Inputs**

* Stable system with learning curves

**Outputs**

* Ablation runner
* Plots and written report

**Success Criteria**

* Each major claim is backed by controlled experiments
* Surprising results are investigated and fixed

**Estimated Effort**
4–12 weeks.

**Key Risks**

* Experiment management overhead
* Nonstationarity makes comparisons hard

**Failure Indicators**

* You can’t reproduce results across weeks

**Dependencies**
Phase 35+.

**Sub-phases/Steps**

1. Define ablation matrix
2. Automate runs and aggregation
3. Write findings and adjust roadmap

---

## Phase 52: Scaling milestones

**Goal**
Expand domains and push toward “real math” steadily.

**Detailed Description**
This is an ongoing phase: increase supported theories, richer datatypes, stronger automation primitives, and larger theorem spaces—without losing the core principle (self-play + verifier + MDL pressure). The work is mostly repeated cycles of: add minimal capability → generate curriculum → learn → compress → stabilize.

**Inputs**

* Everything

**Outputs**

* New domains, new benchmarks, new library growth
* Published-quality results (eventually)

**Success Criteria**

* Clear frontier progression across domains
* Stable improvement curves continue

**Estimated Effort**
Ongoing.

**Key Risks**

* Complexity outruns infrastructure
* You add too much too fast and lose debuggability

**Failure Indicators**

* System becomes a pile of hacks
* Learning curves become uninterpretable

**Dependencies**
All.

**Sub-phases/Steps**

* Repeated domain expansion cycles with regression gates

---

# Phase 1 Deep Dive

You asked for “everything.” I’m going to treat Phase 1 as “**Make tlq0 an experiment OS with typed core objects**.” Your current `tlq0.py` is a blank skeleton ; Phase 1 is where it becomes a real, runnable system.

## Phase 1 Design Principles

1. **Determinism first**: if you can’t reproduce, you can’t debug, and you can’t claim learning.
2. **Typed events + typed configs**: every log line should be parseable and queryable.
3. **Stable IDs everywhere**: theorem ids, state ids, node ids, action ids, run ids.
4. **Schema versioning**: future changes won’t invalidate old runs.
5. **Fail loudly and locally**: structured exceptions with context, never silent corruption.

## Phase 1 Complete Data Structure Definitions

These are the Phase 1 classes you implement *fully*, even if some later components use them more heavily.

### Identity and hashing

* **`RunId`**: stable identifier for a training/eval run.
* **`TheoremId`**: stable identifier for a theorem/task.
* **`StateId`**: stable identifier for a proof state snapshot.
* **`NodeId`**: stable identifier for a hash-consed expression node.
* **`MacroId` / `LemmaId`**: stable library item identifiers.
* **`Hash64` / `Hash256`**: typed wrappers to avoid mixing hash widths.

Why: if you ever put raw strings/ints everywhere, your logs become non-joinable and your caches become untrustworthy.

### Configuration objects

* **`ProjectPaths`**: where things live (project root, runs dir, cache dir).
* **`RunPaths`**: per-run files (config snapshot, events log, artifacts dir).
* **`EnvConfig`**: verifier settings (lean project path, timeouts).
* **`SearchConfig`**: budgets (max nodes, max depth, max seconds).
* **`TrainConfig`**: batch size, lr, device, seed, checkpoint cadence.
* **`TLQ0Config`**: top-level config containing all the above + schema version.

Why: you want a single serializable blob that defines the entire run.

### Logging and metrics

* **`Event`**: typed log record with `ts`, `kind`, `payload`, `step`.
* **`EventLogger`**: JSONL writer, flush policy, and “once-only” event emission.
* **`Meter` / `EMA` / `Histogram`**: metrics accumulators.
* **`RunSummary`**: computed at end; points to artifacts.

Why: you need high-cardinality data (events) and low-cardinality data (metrics).

### Core proof-related shells

Even though Phase 1 won’t fully implement proving, define these *now* to freeze interfaces:

* **`ActionOp` (Enum)**: opcodes (INTRO, EXACT, APPLY, …).
* **`Action`**: (op, args, meta) and serialization.
* **`ProofState`**: (goal, hypotheses, pretty strings, backend metadata).
* **`Transition`**: (state, action, next_state, outcome, cost, timings).
* **`Trajectory`**: theorem id + list of transitions + final result.

Why: all downstream learning, compression, and search depends on these shapes.

## Relationships Between Classes

Textual diagram:

* `TLQ0Config` → owns → `EnvConfig`, `SearchConfig`, `TrainConfig`
* `RunContext` → owns → `TLQ0Config`, `RunPaths`, `EventLogger`, `RNG`
* `Trajectory` → contains → list[`Transition`]
* `Transition` → references → `ProofState` + `Action` + `ProofState`
* `Action` → uses → `ActionOp` + typed args
* `EventLogger` → writes → list[`Event`] to `events.jsonl`

## Phase 1 Complete File Structure

You’re monolith for code, but you still need a repo layout.

### Files that exist by end of Phase 1

* `tlq0.py`
  Contains **all implementation code**, organized by your numbered `# SECTION` dividers.

* `README.md`
  How to set up env, run selfcheck, run tests, and where artifacts go.

* `pyproject.toml` (or `requirements.txt`)
  Dependencies pinned. (I recommend `pyproject.toml` + `uv` or `pip-tools`, but choose one.)

* `.gitignore`
  Ignore `runs/`, `__pycache__/`, large artifacts.

* `tests/test_phase1_core.py`
  Pytest tests for determinism, config roundtrip, logging, hashing.

* `runs/`
  Created at runtime; not committed.

Optional but strongly recommended:

* `scripts/run_selfcheck.sh`
* `scripts/run_tests.sh`

### Import graph

Because code is monolithic, the import graph is “flat” at runtime; but conceptually:

* Section 0 imports standard libs and optional torch/numpy.
* Later sections only depend on earlier section definitions.

Rule: **no section uses a class that appears later in the file**. That’s how you keep “module boundaries” inside a monolith.

## Phase 1 Exact Implementation Order

This is the exact order that minimizes refactors.

1. **Section 0**: imports + `__version__`, constants
2. **Section 1**: typed IDs + hashing utilities
3. **Section 2**: exceptions + validation helpers
4. **Section 3**: config dataclasses + JSON serialization + validation
5. **Section 4**: paths + run directory creation
6. **Section 5**: deterministic RNG + `seed_everything()`
7. **Section 6**: event logging (JSONL) + metrics
8. **Section 7**: core shells (`ActionOp`, `Action`, `ProofState`, `Trajectory`)
9. **Section 8**: CLI (`init`, `selfcheck`)
10. **Section 9**: tests
11. Run: `python tlq0.py selfcheck --seed 123`
12. Run tests: `pytest -q`

### Checkpoints you can test

* After step 5: run dir created correctly, config snapshot saved.
* After step 6: deterministic RNG draws match expected in tests.
* After step 7: event logger writes valid JSONL, reload works.
* After step 8: CLI works.
* After step 10: tests pass.

## Phase 1 Complete Code for Critical Components

You asked for full implementations, not snippets. Below is a **Phase 1-complete `tlq0.py`** you can drop in as a baseline. It does not implement Lean interaction yet; it builds the experiment OS + core shells, consistent with your current file skeleton .

```python
"""
tlq0 (The Last Question) - Mark 0

A self-learning theorem prover that learns from scratch through
compression-driven self-play.

Core thesis: Intelligence = compression of predictive structure over state transitions.

Day 1 of 100. Let's go.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Varun Srinivasan"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 0: IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import dataclasses
from dataclasses import dataclass, field
import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import sys
import time
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union, NewType
import uuid

# Optional deps (Phase 1 should work without torch/numpy; but uses them if present)
try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

try:
    import torch  # type: ignore
except Exception:
    torch = None  # type: ignore


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: TYPED IDS AND HASHING
# ═══════════════════════════════════════════════════════════════════════════════

RunId = NewType("RunId", str)
TheoremId = NewType("TheoremId", str)
StateId = NewType("StateId", str)
NodeId = NewType("NodeId", int)
MacroId = NewType("MacroId", str)
LemmaId = NewType("LemmaId", str)

Hash64 = NewType("Hash64", int)
Hash256 = NewType("Hash256", str)


def utcnow_iso() -> str:
    """UTC timestamp in ISO-8601 (with 'Z')."""
    return _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc).isoformat().replace("+00:00", "Z")


def blake2b_64(data: bytes, person: bytes = b"tlq0") -> Hash64:
    """
    64-bit hash for fast IDs. Not cryptographic integrity; for keys and caching.
    Uses personalization to reduce accidental cross-project collisions.
    """
    h = hashlib.blake2b(data, digest_size=8, person=person)
    return Hash64(int.from_bytes(h.digest(), "little"))


def sha256_hex(data: bytes) -> Hash256:
    """Cryptographic integrity hash."""
    return Hash256(hashlib.sha256(data).hexdigest())


def stable_json_dumps(obj: Any) -> str:
    """Deterministic JSON serialization (important for hashing)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def new_run_id() -> RunId:
    """Generate a unique run id."""
    return RunId(f"run_{_dt.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: ERRORS AND VALIDATION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class TLQ0Error(Exception):
    """Base error for tlq0. Catch this at top-level to produce clean diagnostics."""


class ConfigError(TLQ0Error):
    """Raised when configuration is invalid or cannot be parsed."""


class IOFailure(TLQ0Error):
    """Raised when file IO fails in a tlq0-specific way."""


def require(cond: bool, msg: str) -> None:
    """Raise ConfigError if condition is false."""
    if not cond:
        raise ConfigError(msg)


def as_posix(p: Union[str, Path]) -> str:
    return str(Path(p).expanduser().resolve())


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class EnvConfig:
    """
    Verifier/environment configuration.

    Fields exist to make Lean interaction later reproducible and sandboxed.
    """
    lean_project_dir: str = "lean"          # path to lake project (relative to repo root)
    backend_timeout_s: float = 5.0          # per-step timeout for Lean backend calls
    max_goal_chars: int = 10_000            # guardrail against runaway pretty-prints
    allow_unsafe: bool = False              # if True, allow unsafe Lean tactics (default no)


@dataclass(frozen=True)
class SearchConfig:
    """
    Search budgets and safety limits.

    These must be explicit so solve-rate comparisons are meaningful.
    """
    max_nodes: int = 10_000                 # node expansions per attempt
    max_depth: int = 64                     # max proof length (actions)
    max_seconds: float = 10.0               # wall-clock budget per theorem
    beam_width: int = 32                    # if using beam/A*, how many actions to keep
    dedup_states: bool = True               # maintain visited set keyed by StateId/hash


@dataclass(frozen=True)
class TrainConfig:
    """
    Training configuration.

    Phase 1: defined now; later phases will actually use it.
    """
    seed: int = 0
    device: str = "cpu"                     # "cpu" / "mps" / "cuda"
    batch_size: int = 256
    lr: float = 3e-4
    weight_decay: float = 1e-4
    grad_clip: float = 1.0
    log_every: int = 100
    eval_every: int = 1000
    save_every: int = 5000


@dataclass(frozen=True)
class TLQ0Config:
    """
    Top-level config. This is snapshotted into every run directory.

    schema_version exists to allow backward-compatible parsing later.
    """
    schema_version: int = 1
    env: EnvConfig = field(default_factory=EnvConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    train: TrainConfig = field(default_factory=TrainConfig)

    def validate(self) -> None:
        require(self.schema_version == 1, f"Unsupported schema_version: {self.schema_version}")

        require(self.search.max_nodes > 0, "search.max_nodes must be > 0")
        require(self.search.max_depth > 0, "search.max_depth must be > 0")
        require(self.search.max_seconds > 0, "search.max_seconds must be > 0")
        require(self.search.beam_width > 0, "search.beam_width must be > 0")

        require(self.env.backend_timeout_s > 0, "env.backend_timeout_s must be > 0")
        require(self.env.max_goal_chars > 0, "env.max_goal_chars must be > 0")

        require(self.train.batch_size > 0, "train.batch_size must be > 0")
        require(self.train.lr > 0, "train.lr must be > 0")
        require(self.train.seed >= 0, "train.seed must be >= 0")


def dataclass_to_dict(dc: Any) -> Any:
    """Recursively convert dataclasses to dicts for JSON serialization."""
    if dataclasses.is_dataclass(dc):
        out: Dict[str, Any] = {}
        for f in dataclasses.fields(dc):
            out[f.name] = dataclass_to_dict(getattr(dc, f.name))
        return out
    if isinstance(dc, (list, tuple)):
        return [dataclass_to_dict(x) for x in dc]
    if isinstance(dc, dict):
        return {k: dataclass_to_dict(v) for k, v in dc.items()}
    return dc


def config_to_json(cfg: TLQ0Config) -> str:
    cfg.validate()
    return stable_json_dumps(dataclass_to_dict(cfg))


def config_from_json(s: str) -> TLQ0Config:
    try:
        obj = json.loads(s)
    except Exception as e:
        raise ConfigError(f"Failed to parse config JSON: {e}") from e

    try:
        env = EnvConfig(**obj.get("env", {}))
        search = SearchConfig(**obj.get("search", {}))
        train = TrainConfig(**obj.get("train", {}))
        cfg = TLQ0Config(
            schema_version=int(obj.get("schema_version", 1)),
            env=env,
            search=search,
            train=train,
        )
        cfg.validate()
        return cfg
    except TypeError as e:
        raise ConfigError(f"Config fields mismatch: {e}") from e


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: PATHS AND RUN CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ProjectPaths:
    """
    Defines repo-level paths.

    Keeping this explicit makes it easier to relocate the repo without breaking runs.
    """
    repo_root: str
    runs_dir: str = "runs"
    cache_dir: str = "cache"

    def runs_path(self) -> Path:
        return Path(self.repo_root) / self.runs_dir

    def cache_path(self) -> Path:
        return Path(self.repo_root) / self.cache_dir


@dataclass(frozen=True)
class RunPaths:
    """
    Defines paths inside a run directory.

    Every field exists so you can locate artifacts without guessing filenames.
    """
    run_dir: str
    config_json_path: str
    env_json_path: str
    events_jsonl_path: str
    artifacts_dir: str

    def run_path(self) -> Path:
        return Path(self.run_dir)

    def artifacts_path(self) -> Path:
        return Path(self.artifacts_dir)


@dataclass
class RunContext:
    """
    Runtime context for a run.

    This is mutable only where it makes sense (e.g., meters), but contains
    immutable identifiers and configuration.
    """
    run_id: RunId
    cfg: TLQ0Config
    project: ProjectPaths
    paths: RunPaths
    started_utc: str
    rng: "RNG"
    logger: "EventLogger"

    # Metrics accumulators live here so everything can access them.
    meters: Dict[str, "Meter"] = field(default_factory=dict)


def detect_repo_root() -> str:
    """
    Best-effort repo root detection: directory containing tlq0.py.
    In a monolith project, this is usually correct.
    """
    return as_posix(Path(__file__).parent)


def ensure_dir(p: Union[str, Path]) -> None:
    try:
        Path(p).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise IOFailure(f"Failed to create dir {p}: {e}") from e


def write_text_atomic(path: Union[str, Path], text: str) -> None:
    """
    Atomic-ish write: write to temp then replace.
    Prevents partial writes if the process dies mid-write.
    """
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
    except Exception as e:
        raise IOFailure(f"Failed to write {path}: {e}") from e


def create_run_paths(project: ProjectPaths, run_id: RunId) -> RunPaths:
    run_dir = project.runs_path() / str(run_id)
    ensure_dir(run_dir)
    artifacts = run_dir / "artifacts"
    ensure_dir(artifacts)

    return RunPaths(
        run_dir=as_posix(run_dir),
        config_json_path=as_posix(run_dir / "config.json"),
        env_json_path=as_posix(run_dir / "env.json"),
        events_jsonl_path=as_posix(run_dir / "events.jsonl"),
        artifacts_dir=as_posix(artifacts),
    )


def collect_env_snapshot(cfg: TLQ0Config, project: ProjectPaths) -> Dict[str, Any]:
    """
    Capture enough environment information to debug reproducibility issues.
    """
    snap: Dict[str, Any] = {
        "utc": utcnow_iso(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "repo_root": project.repo_root,
        "lean_project_dir": cfg.env.lean_project_dir,
    }
    if np is not None:
        snap["numpy_version"] = getattr(np, "__version__", "unknown")
    else:
        snap["numpy_version"] = None
    if torch is not None:
        snap["torch_version"] = getattr(torch, "__version__", "unknown")
        snap["torch_mps_available"] = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
    else:
        snap["torch_version"] = None
    return snap


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: RNG AND DETERMINISM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RNG:
    """
    Deterministic random sources across Python, NumPy, and Torch.

    Fields exist so downstream code can use the same generator consistently,
    avoiding hidden global RNG state.
    """
    seed: int
    py: random.Random = field(init=False)
    np: Any = field(init=False)             # np.random.Generator or None
    torch: Any = field(init=False)          # torch.Generator or None

    def __post_init__(self) -> None:
        self.py = random.Random(self.seed)

        if np is not None:
            self.np = np.random.default_rng(self.seed)
        else:
            self.np = None

        if torch is not None:
            g = torch.Generator(device="cpu")
            g.manual_seed(self.seed)
            self.torch = g
        else:
            self.torch = None

    def randint(self, a: int, b: int) -> int:
        """Inclusive randint (like Python's random.randint)."""
        return self.py.randint(a, b)

    def choice(self, xs: Sequence[Any]) -> Any:
        require(len(xs) > 0, "RNG.choice called on empty sequence")
        return xs[self.py.randrange(len(xs))]


def seed_everything(seed: int) -> None:
    """
    Seed global RNGs for best-effort determinism.
    Note: full determinism can still be broken by multithreading/GPU kernels.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    if np is not None:
        np.random.seed(seed)

    if torch is not None:
        torch.manual_seed(seed)
        # Best-effort deterministic flags
        try:
            torch.use_deterministic_algorithms(True)  # may raise on unsupported ops
        except Exception:
            pass
        try:
            torch.backends.cudnn.deterministic = True  # type: ignore[attr-defined]
            torch.backends.cudnn.benchmark = False     # type: ignore[attr-defined]
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: EVENTS, LOGGING, METRICS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Event:
    """
    A structured log event.

    - kind: short string category ("run_start", "metric", "error")
    - payload: JSON-serializable dict
    - step: optional training step or global counter
    """
    ts_utc: str
    kind: str
    payload: Dict[str, Any]
    step: Optional[int] = None


class EventLogger:
    """
    JSONL event logger.

    Each line is one Event as deterministic JSON (sorted keys). This is intentionally
    simple: you can grep it, stream it, or load it into pandas later.
    """
    def __init__(self, path: Union[str, Path], flush_every: int = 1) -> None:
        self.path = Path(path)
        self.flush_every = flush_every
        self._fh = self.path.open("a", encoding="utf-8")
        self._count = 0

    def close(self) -> None:
        try:
            self._fh.flush()
        finally:
            self._fh.close()

    def log(self, kind: str, payload: Dict[str, Any], step: Optional[int] = None) -> None:
        evt = Event(ts_utc=utcnow_iso(), kind=kind, payload=payload, step=step)
        line = stable_json_dumps(dataclass_to_dict(evt))
        self._fh.write(line + "\n")
        self._count += 1
        if self._count % self.flush_every == 0:
            self._fh.flush()

    def log_once(self, kind: str, payload: Dict[str, Any], key: str, _cache: Dict[str, bool]) -> None:
        """
        Emit an event only once per run, keyed by 'key'.
        Caller keeps the cache (simple and explicit).
        """
        if _cache.get(key, False):
            return
        _cache[key] = True
        self.log(kind, payload)


@dataclass
class Meter:
    """
    Streaming scalar meter.

    Useful for tracking loss, solve rate, etc.
    """
    n: int = 0
    total: float = 0.0
    last: float = 0.0
    min: float = float("inf")
    max: float = float("-inf")

    def update(self, x: float) -> None:
        self.n += 1
        self.total += float(x)
        self.last = float(x)
        self.min = min(self.min, float(x))
        self.max = max(self.max, float(x))

    @property
    def mean(self) -> float:
        return self.total / self.n if self.n > 0 else 0.0


class Stopwatch:
    """Simple wall-clock timer for profiling."""
    def __init__(self) -> None:
        self._t0 = time.perf_counter()

    def reset(self) -> None:
        self._t0 = time.perf_counter()

    def elapsed_s(self) -> float:
        return time.perf_counter() - self._t0


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: CORE PROOF SHELL TYPES
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum, auto

class ActionOp(Enum):
    """
    Primitive typed bytecode opcodes (v0).

    Matches the intended minimal action set (expanded later).
    """
    INTRO = auto()
    EXACT = auto()
    APPLY = auto()
    CASES = auto()
    INDUCTION = auto()
    CONSTRUCTOR = auto()
    SPLIT = auto()
    LEFT = auto()
    RIGHT = auto()
    REWRITE = auto()
    RFL = auto()
    FAIL = auto()   # sentinel used internally


@dataclass(frozen=True)
class Action:
    """
    A single action in the proof search DSL.

    args are op-specific and must be JSON-serializable.
    Example:
      Action(ActionOp.EXACT, {"hyp": 3})
    """
    op: ActionOp
    args: Dict[str, Any] = field(default_factory=dict)

    def encode(self) -> Dict[str, Any]:
        return {"op": self.op.name, "args": self.args}

    @staticmethod
    def decode(obj: Mapping[str, Any]) -> "Action":
        op = ActionOp[obj["op"]]
        args = dict(obj.get("args", {}))
        return Action(op=op, args=args)


@dataclass(frozen=True)
class Hypothesis:
    """A local hypothesis in a proof state."""
    name: str
    type_str: str


@dataclass(frozen=True)
class ProofState:
    """
    Minimal proof state shell.

    Phase 1 uses string forms; later phases add IR graphs and hashes.
    """
    state_id: StateId
    goals: Tuple[str, ...]
    hyps: Tuple[Hypothesis, ...]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Transition:
    """One environment step."""
    state: ProofState
    action: Action
    next_state: ProofState
    ok: bool
    error: Optional[str] = None
    elapsed_s: float = 0.0


@dataclass(frozen=True)
class Trajectory:
    """
    A full attempt at proving a theorem: transitions + outcome.
    """
    theorem_id: TheoremId
    success: bool
    transitions: Tuple[Transition, ...]
    stats: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: RUN CREATION AND CLI
# ═══════════════════════════════════════════════════════════════════════════════

def init_run(cfg: TLQ0Config, seed: Optional[int] = None) -> RunContext:
    cfg = dataclasses.replace(cfg, train=dataclasses.replace(cfg.train, seed=(seed if seed is not None else cfg.train.seed)))
    cfg.validate()

    repo_root = detect_repo_root()
    project = ProjectPaths(repo_root=repo_root)
    ensure_dir(project.runs_path())
    ensure_dir(project.cache_path())

    run_id = new_run_id()
    paths = create_run_paths(project, run_id)

    # Determinism
    seed_everything(cfg.train.seed)
    rng = RNG(cfg.train.seed)

    # Save config/env snapshots
    write_text_atomic(paths.config_json_path, config_to_json(cfg))
    env_snap = collect_env_snapshot(cfg, project)
    write_text_atomic(paths.env_json_path, stable_json_dumps(env_snap))

    logger = EventLogger(paths.events_jsonl_path, flush_every=1)
    ctx = RunContext(
        run_id=run_id,
        cfg=cfg,
        project=project,
        paths=paths,
        started_utc=utcnow_iso(),
        rng=rng,
        logger=logger,
    )

    ctx.logger.log("run_start", {
        "run_id": str(ctx.run_id),
        "version": __version__,
        "author": __author__,
        "cfg": dataclass_to_dict(cfg),
    })
    return ctx


def selfcheck(ctx: RunContext) -> None:
    """
    Phase 1 selfcheck: verify determinism basics and run directory health.
    """
    sw = Stopwatch()

    # Deterministic RNG draw sample
    sample = [ctx.rng.randint(0, 10**9) for _ in range(10)]
    ctx.logger.log("selfcheck_rng_sample", {"sample": sample})

    # Hash selfcheck
    h = blake2b_64(stable_json_dumps(sample).encode("utf-8"))
    ctx.logger.log("selfcheck_hash", {"blake2b_64": int(h)})

    # Files exist
    required = [ctx.paths.config_json_path, ctx.paths.env_json_path, ctx.paths.events_jsonl_path]
    ok = True
    missing: List[str] = []
    for p in required:
        if not Path(p).exists():
            ok = False
            missing.append(p)
    ctx.logger.log("selfcheck_files", {"ok": ok, "missing": missing})

    ctx.logger.log("selfcheck_done", {"elapsed_s": sw.elapsed_s()})


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="tlq0: The Last Question")
    p.add_argument("cmd", choices=["init", "selfcheck"], help="Command to run")
    p.add_argument("--seed", type=int, default=0, help="Random seed")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_argparser().parse_args(argv)

    cfg = TLQ0Config(train=dataclasses.replace(TrainConfig(), seed=args.seed))

    if args.cmd == "init":
        ctx = init_run(cfg, seed=args.seed)
        print(f"[tlq0] initialized {ctx.run_id} at {ctx.paths.run_dir}")
        ctx.logger.close()
        return 0

    if args.cmd == "selfcheck":
        ctx = init_run(cfg, seed=args.seed)
        print(f"[tlq0] selfcheck run {ctx.run_id} at {ctx.paths.run_dir}")
        selfcheck(ctx)
        ctx.logger.close()
        print("[tlq0] selfcheck complete")
        return 0

    raise TLQ0Error(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
```

### What this code gives you immediately

* Deterministic seeds (best effort).
* A run directory under `runs/run_YYYYMMDD_HHMMSS_xxxxxxxx/`.
* `config.json`, `env.json`, `events.jsonl`.
* Typed shells for Actions/States/Trajectories to build Phase 2+ against.

## Phase 1 Comprehensive Test Strategy

Create `tests/test_phase1_core.py` with:

### Unit tests

1. **Config roundtrip**

   * Create `TLQ0Config`, serialize to JSON, parse back.
   * Assert equality of dict forms.

2. **Deterministic RNG**

   * Create two RNGs with same seed.
   * Assert same 100 draws.

3. **Stable JSON determinism**

   * Serialize dict with different key orders.
   * Ensure `stable_json_dumps` identical.

4. **Hash determinism**

   * Same input bytes → same `blake2b_64`.

5. **Run directory structure**

   * Call `init_run`.
   * Assert files exist: config/env/events.
   * Assert events file contains `run_start`.

### Integration tests

1. **CLI selfcheck**

   * Run `python tlq0.py selfcheck --seed 123`.
   * Verify exit code 0 and run directory created.

### How to know it’s broken

* Any nondeterminism in RNG tests means your later “learning” results will be suspect.
* Missing log fields means later analysis (MDL, solve rate) will be painful.

## Phase 1 Common Mistakes to Avoid

1. **Using global `random` everywhere** instead of your `RNG` object → hidden nondeterminism.
2. **Logging unstructured strings** instead of JSON payloads → you can’t compute metrics later.
3. **No schema versioning** → old datasets become unreadable.
4. **Letting run dirs overwrite each other** → silent loss of evidence.
5. **Skipping environment snapshots** → you’ll never reproduce toolchain issues.

---

# Architectural Decisions Catalog

I’m listing major decision points as “ADR-style” items. Each includes options, trade-offs, recommendation, cost of wrong choice, reversibility, and experiments.

## ADR 001: Lean interaction method

**Options**

1. LeanDojo environment API (gym-style)
2. Lean language server protocol directly (LSP)
3. Shelling out to `lean` for each step (slow)
4. Custom RPC wrapper around Lean elaborator

**Trade-offs**

* LeanDojo: fastest to build, but you’re tied to its API stability.
* Direct LSP: more control, more engineering.
* Shelling out: simplest, but too slow for learning loops.
* Custom RPC: maximal control, maximal work.

**Recommendation**
Start with LeanDojo if it works reliably on your machine, behind a `ProverBackend` interface. It’s the fastest route to “first learning curve,” and you can swap later because you built Phase 3 correctly.

**Cost of getting it wrong**
Months of sunk time if you implement LSP/RPC prematurely.

**Reversible**
Yes, if the backend interface is clean.

**Experiments**
Implement a minimal prototype of (1) and (2) that can apply `intro` + `exact` and compare step latency.

---

## ADR 002: Starter domain

**Options**

1. Propositional logic only (Prop, And/Or/Imp/False)
2. Equality-only fragment
3. Nat with recursion/induction immediately
4. Mixed fragment (Prop + Eq + Nat)

**Trade-offs**

* Prop-only: easiest to get signal; may overfit to shallow patterns.
* Equality-only: harder but more relevant.
* Nat induction: long horizon; likely sparse signal early.
* Mixed: realistic but complex.

**Recommendation**
Prop-only first, then add equality, then induction. The convergent plan explicitly suggests a tiny DSL and no automation early .

**Cost of wrong choice**
If you start with induction too early, you’ll get 0% solves and no dataset.

**Reversible**
Yes, but switching later is expensive because IR and generators change.

**Experiments**
Measure baseline solve rate of DFS/BFS on each domain with same budget.

---

## ADR 003: State representation source of truth

**Options**

1. Treat Lean states as strings (forever)
2. Parse pretty-printed strings into your IR
3. Extract Lean Expr AST (structured) via backend
4. Hybrid: structured when possible, fallback to strings

**Recommendation**
Hybrid: start with strings for logging and debugging, but build a structured IR ASAP (Phases 13–15). The convergent plan wants hash-consed DAG + De Bruijn , which implies structured.

**Cost of wrong choice**
String-based forever → no reliable hashing, no real delta-state, poor learning.

**Reversible**
Partially; migrating datasets is painful.

**Experiments**
Build IR for toy domain and verify alpha-equivalence collapse improvements.

---

## ADR 004: Hash function for interned DAG

**Options**

1. Non-crypto 64-bit hash (blake2b_64) + collision checks
2. SHA-256 Merkle hashes (slower, safer)
3. Two-tier: 64-bit for table key, SHA for integrity
4. SipHash keyed per run

**Recommendation**
Two-tier: use 64-bit for speed and store also SHA-256 for collision detection in debug builds. Gemini insight mentions Merkle-DAG with SHA-256 .

**Cost of wrong choice**
Hash collisions can silently corrupt learning and “prove” false MDL savings.

**Reversible**
Yes but expensive; affects all stored artifacts.

**Experiments**
Stress-test interner with random expressions; check collision rates and performance.

---

## ADR 005: Search algorithm core

**Options**

1. BFS/DFS with depth limit
2. Beam search
3. A* with heuristic
4. Levin/MDL search (code length priority) 
5. MCTS/PUCT

**Recommendation**
BFS/beam baseline → then Levin/MDL once policy exists. Eventually add MCTS only if needed.

**Cost of wrong choice**
Starting with MCTS adds complexity and debugging pain before you have good priors.

**Reversible**
Yes, search is modular.

**Experiments**
Compare solve rate vs nodes expanded across methods on a fixed suite.

---

## ADR 006: Learning method

**Options**

1. Imitation learning from successful traces
2. Actor-critic RL with sparse reward
3. Offline RL from replay buffer
4. Hybrid: IL pretrain then RL fine-tune

**Recommendation**
Start with imitation from self-generated traces (Phase 19). Sparse RL will be too brittle early.

**Cost**
Going RL too early leads to “no learning signal.”

**Reversible**
Yes.

**Experiments**
Overfit sanity check; then measure solve rate improvements.

---

## ADR 007: Macro discovery algorithm

**Options**

1. Frequent n-grams
2. Sequitur grammar induction 
3. BPE merges 
4. Frequent subtree mining on state/action pairs
5. Neural program induction

**Recommendation**
Sequitur/BPE for action sequences first; then consider parameter-aware mining.

**Cost**
Too complex macro discovery early delays everything.

**Reversible**
Yes.

**Experiments**
Measure compression ratio and macro replay success rate.

---

## ADR 008: Macro admission policy

**Options**

1. Admit if frequency > threshold
2. Admit if training MDL improves
3. Admit if held-out MDL improves (ΔMDL < 0) 
4. Admit but cap/day and prune aggressively 

**Recommendation**
Held-out MDL gate + cap/day. This is your anti-bloat governor.

**Cost**
If you admit freely, the library explodes and you “memorize” instead of generalize.

**Reversible**
Yes, but pruning later may delete stepping stones.

**Experiments**
Simulate admissions on past corpora; measure generalization.

---

## ADR 009: Delta-state representation

**Options**

1. Recompute full graph encoding every step
2. Cache node embeddings by hash-consed node id
3. Maintain delta codes (autoencoder/VQ-VAE) 
4. Maintain recurrent state over action sequence

**Recommendation**
Start with caching embeddings by node id; add delta coding later.

**Cost**
Over-engineering delta codes early.

**Reversible**
Yes.

**Experiments**
Profile encoder time per step; measure cache hit rate.

---

## ADR 010: Retrieval method for lemmas

**Options**

1. Exact matching by hash
2. SimHash on structural features 
3. ANN on learned embeddings
4. Hybrid: SimHash prefilter + ANN rerank

**Recommendation**
Hybrid eventually; SimHash first for simplicity.

**Cost**
Poor retrieval ruins search by flooding with junk candidates.

**Reversible**
Yes.

**Experiments**
Offline retrieval eval: how often retrieved lemma is actually usable.

---

I could keep going (there are ~30+ ADRs in a full build), but the above are the *highest-leverage early locks*. As you progress, treat each as an explicit “ADR file in your head” and log the decision in `events.jsonl` so future-you remembers why.

---

# Validation Framework

You asked: “How do we PROVE it is learning?” Here is the exact framework.

## Metrics to track from Day 1

### Core capability metrics

1. **Solve rate**

   * Compute: `solved / attempted` on fixed eval suite under fixed budget
   * Success: monotonic upward trend across epochs
   * Failure: flatline after many epochs, or regressions after changes

2. **Nodes expanded per solved theorem**

   * Compute: average expansions conditional on solved
   * Success: decreasing trend

3. **Wall-clock time per solved theorem**

   * Compute: median and p90 solve time
   * Success: decreasing or stable while difficulty rises

4. **Proof length**

   * Compute: number of actions (primitive-expanded)
   * Success: decreases for same theorem distribution, or stays stable while theorem difficulty rises

### Compression metrics

5. **Total MDL**

   * Compute: `L(Library) + Σ L(proof_i | Library)` 
   * Success: decreases on held-out corpus
   * Failure: decreases only on training data (“fake compression”)

6. **Library size**

   * Compute: macro count, lemma count, total bytes
   * Success: grows slowly, then stabilizes
   * Failure: unbounded growth with low reuse

7. **Macro reuse rate**

   * Compute: fraction of proofs using at least one macro; average macro calls/proof
   * Success: increases on *held-out* theorems
   * Failure: increases only on seen distributions

8. **ΔMDL per admitted macro**

   * Compute: held-out MDL before/after admitting macro
   * Success: negative on average
   * Failure: near zero or positive

### Learning dynamics metrics

9. **Policy accuracy**

   * Compute: % correct next action on held-out transitions
   * Success: increases, but must correlate with solve rate

10. **Policy entropy**

* Compute: average entropy of opcode distribution
* Success: decreases moderately (more confident) but not to collapse
* Failure: entropy collapses early and solve rate stagnates

11. **Generalization gap**

* Compute: solve_rate(train_like) − solve_rate(holdout)
* Success: small or shrinking
* Failure: widening gap

### Curriculum health metrics

12. **Task difficulty distribution**

* Compute: histogram of AST size, binder depth, baseline hardness
* Success: shifts upward while solve rate stays nonzero
* Failure: collapses to trivial tasks or impossible tasks

13. **Novelty rate**

* Compute: % generated theorems that are new under canonical hash
* Success: high, stable
* Failure: duplicates dominate

### System performance metrics

14. **Backend step latency**
15. **Graph build latency**
16. **Encoder latency**
17. **Cache hit rate** (once delta-state exists)
18. **Samples/sec end-to-end**

## Plots to generate

1. Solve rate vs epoch (train + holdout)
2. Held-out total MDL vs epoch
3. Library size vs epoch
4. Macro reuse rate vs epoch
5. Nodes expanded per solved theorem vs epoch
6. Proof length distribution over time (box plot)
7. Difficulty histogram vs epoch
8. Generalization gap vs epoch
9. Cache hit rate vs epoch (later)
10. Time breakdown stacked area: backend vs search vs model vs IO

Good plot shape: solve rate up, MDL down, macro reuse up, node expansions down, difficulty slowly increasing.
Bad plot shape: MDL down but solve rate flat (fake compression), library size exploding, or curriculum collapsing.

## Ablation studies

Minimum ablations that matter:

1. **No macros** vs macros
2. **No MDL gate** (frequency-only admission) vs MDL gate
3. **No De Bruijn normalization** vs with it
4. **No hash-consing** vs with it
5. **No retrieval** vs retrieval
6. **Unguided search** vs guided search
7. **Full recompute encoding** vs delta-state caching
8. **Single policy** vs ensemble

Baselines to compare against (always):

* Random policy + search
* Handwritten heuristics + search
* Unguided BFS/beam

## Failure modes and detection

### Local optimum in search/policy

* Symptom: solve rate plateaus, entropy low, action distribution repetitive
* Detection: action n-gram diversity drops, novelty drops
* Fix: policy population, exploration noise, generator shifts

### Fake compression

* Symptom: MDL decreases but solve rate doesn’t improve
* Detection: held-out MDL flat, macro reuse only on training-like tasks
* Fix: stronger held-out gate, penalize macro size more, prune aggressively

### Curriculum collapse

* Symptom: generator outputs trivial theorems, success near 100% but no frontier movement
* Detection: theorem size distribution shrinks; novelty drops
* Fix: difficulty controller, adversarial generator, novelty constraints

### Library bloat

* Symptom: macro count grows rapidly, retrieval slows, solve rate flat
* Detection: macro reuse distribution heavy-tailed with most macros unused
* Fix: rent collection + pruning, cap additions/day 

---

# Risk Registry

These are the things that can genuinely kill progress, plus early detection.

## Existential technical risks

1. **Theorem generation doesn’t produce a learnable curriculum**

   * Early detection: <1% solvable rate even at easiest tier
   * Mitigation: start with semi-curated seed tasks + mutate; add subgoal harvesting

2. **Lean interaction throughput too low on laptop**

   * Detection: backend dominates wall time (>80%)
   * Mitigation: parallel backends, caching, reduce interaction granularity

3. **Representation/parsing brittleness**

   * Detection: frequent “unparsed state” events
   * Mitigation: fallback representations; restrict domain; structured extraction

4. **MDL objective mis-specified**

   * Detection: MDL improves while capability doesn’t
   * Mitigation: revise coding scheme, increase library cost, enforce held-out evaluation

5. **Hash-consing / De Bruijn bugs**

   * Detection: same theorem appears with multiple IDs; rewrite errors
   * Mitigation: property tests; cross-check with full recompute; debug dumps

## Existential research risks

6. **Sparse learning signal**

   * Detection: policy cannot beat heuristic baseline after large compute
   * Mitigation: richer HER, better curriculum shaping, auxiliary prediction tasks (delta prediction)

7. **Induction barrier**

   * Detection: induction tasks never cross 1–2% solve rate
   * Mitigation: staged induction curriculum, induction macros, lemma synthesis for invariants

8. **Ceiling effect**

   * Detection: you can’t push frontier despite improvements; search dominates
   * Mitigation: focus on compression (macros/lemmas), better retrieval, better state abstraction

## Project risks

9. **Complexity runaway**

   * Detection: >30% time spent debugging infrastructure
   * Mitigation: regression tests, strict phase gating, never merge without eval

10. **Non-reproducible results**

* Detection: same run config yields different curves
* Mitigation: single-thread determinism mode; locked seeds; log everything

---

# Timeline Projection

Assuming you’re “all in” and moving fast but not recklessly (think ~40–60 hrs/week):

## Months 0–2

* Phases 1–9
* Milestone: deterministic harness + Lean stepping + DSL + baseline search + eval suite.

**First visible “learning” potential**: end of Month 2 (you can at least generate data and see solve-rate baselines).

## Months 2–5

* Phases 10–20
* Milestone: forward theorem generation + HER + dataset + first GNN + guided search.

**First clear learning curve**: somewhere in here if the domain is chosen well (Prop-only).

## Months 5–9

* Phases 21–35
* Milestone: Levin/MDL search + macro discovery + explicit MDL accounting + wake/sleep loop.

**First “compression-driven intelligence” curve**: solve rate up *and* held-out MDL down.

## Months 9–15

* Phases 36–41
* Milestone: delta-state embedding + coevolution + stronger curriculum stability.

**First time you should start feeling “compounding”**: macro reuse accelerates, node expansions drop, frontier moves faster.

## Months 15–24

* Phases 42–52
* Milestone: equality + induction + lemma synthesis + performance + ablations.

**This is where it stops being a toy** and starts approaching research-grade capability.

---

If you want, the very next thing to do is: implement **Phase 1 exactly as above**, run `selfcheck`, and confirm your `runs/` artifacts are clean and reproducible. Then Phase 2 is toolchain pinning and Lean smoke checks—and after that you’re officially “in the environment.”


