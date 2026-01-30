# Phase 1: Deterministic Experiment Harness

**Source**: GPT 5.2 Pro  
**Date**: 2026-01-22  
**Type**: Implementation guide

---

## Goal

Build a **deterministic, inspectable, structured experiment shell** that every future phase can plug into.

---

## Section Architecture

| Section | Capability |
|---------|------------|
| SECTION 0 | Imports + Version + Global Constants |
| SECTION 1 | Typed IDs + Hashing Utilities |
| SECTION 2 | Error Taxonomy + Preconditions |
| SECTION 3 | Config System |
| SECTION 4 | Run Directory + Atomic Writes + Environment Snapshot |
| SECTION 5 | RNG Discipline + Determinism Layer |
| SECTION 6 | Structured Event Logging + Streaming Metrics |
| SECTION 7 | Core Shell Types (Stubs) |
| SECTION 8 | CLI Contract |
| SECTION 9 | Built-in Test Harness |

---

## Definition of Done

1. `python tlq0.py init --seed 0` creates run dir with config, env, events.jsonl, artifacts/
2. `python tlq0.py selfcheck --seed 123` logs RNG samples and verifies determinism
3. Two selfcheck runs with same seed produce **identical** RNG sample payloads
4. Internal test command passes

---

## Full GPT Pro Response

Alright. Phase 1 is where tlq0 becomes an **experiment OS**: deterministic runs, structured logs, stable IDs, and a CLI that makes every later phase testable and falsifiable. This is non-negotiable if we’re serious about “prove it’s learning” later (solve-rate + MDL curves that actually mean something) . And it directly matches the philosophy: if intelligence is *compression over state transitions*, then your system must record those transitions precisely, reproducibly, and queryably from day 1 .

You asked: **monolith only**, high-level design (not literal code), explain **functionalities** (not functions), and teach Python concepts as needed. Perfect.

---

## Phase 1 Goal in One Sentence

Build a **reproducible run harness** that (1) creates a run directory, (2) snapshots config + environment, (3) logs structured events + metrics, (4) enforces deterministic RNG discipline, and (5) exposes a CLI to execute these reliably.

If Phase 1 is good, you can later say:

> “This solve-rate improvement is real, because the run is reproducible, the budgets are pinned, and the evidence is logged.”

If Phase 1 is sloppy, tlq0 will eventually turn into:

> “It feels like it’s learning?”
> which is death for this project.

---

## The Monolith Mental Model

Since everything must live in `tlq0.py`, you need “fake modularity” via **sections**. Think of each section as a module with a strict dependency direction: later sections can import names from earlier sections, but never the reverse.

### Rule (hard):

**No symbol defined in Section N may depend on anything defined in Section > N.**

This keeps the monolith from turning into spaghetti.

---

## Phase 1 Section Blueprint

Below is the exact “section architecture” I recommend for Phase 1. For each section, I’ll tell you:

* **What capability it provides**
* **Why it exists** (what future pain it prevents)
* **Python concepts** you’ll practice

### SECTION 0: Imports + Version + Global Constants

**Capability**

* Centralize imports, version string, global constants like default paths.

**Why**

* You’ll want every run to record **code version** and key constants so you can diff results across time.

**Python concepts**

* `from __future__ import annotations` (optional but helpful): lets you write type hints referencing classes defined later.
* Optional imports pattern: try-import torch/numpy but don’t hard-fail in Phase 1 (so core harness works even if ML deps aren’t installed yet).

---

### SECTION 1: Typed IDs + Hashing Utilities

**Capability**

* Create stable identifiers (run IDs, theorem IDs, state IDs later).
* Provide deterministic hashing and stable JSON serialization.

**Why**

* You are building a system where the central object is a sequence of transitions (state → action → next_state). If you can’t assign stable IDs and hash reliably, you can’t:

  * deduplicate,
  * cache,
  * join logs across runs,
  * or compute novelty later.
* Also: MDL accounting later depends on stable encodings .

**What to design (high level)**

* “ID types”:

  * `RunId`, `TheoremId`, `StateId`, `NodeId`, `MacroId`, `LemmaId`
* “Hash primitives”:

  * fast hash for keys (64-bit)
  * integrity hash (sha256 hex)
* “Stable JSON dumps”:

  * same dict → same string always (sorted keys, compact separators)

**Python concepts**

* `typing.NewType`: creates “stronger” types for IDs so you don’t accidentally pass a theorem id where a run id is expected.
* `hashlib` for hashing.
* Deterministic JSON: `json.dumps(sort_keys=True, separators=(",", ":"))`.

**Aggressive challenge**

* Make a tiny property test: same structured object → identical stable JSON string across runs.
* Ensure hash of stable JSON is identical across runs.

---

### SECTION 2: Error Taxonomy + Preconditions

**Capability**

* Define custom exception classes (`TLQ0Error`, `ConfigError`, `IOError` variants).
* Define a `require`/`check` style assertion helper that raises your domain errors.

**Why**

* You want failures to be:

  * **typed** (easy to detect in logs),
  * **actionable** (include context),
  * not random `KeyError`/`IndexError` deep inside.
* Later phases will have lots of “expected failures” (tactic failed, timeout, etc.). Start disciplined now.

**Python concepts**

* Custom exceptions: subclassing `Exception`.
* Raising with context: `raise X("...") from e` preserves traceback.

**Aggressive challenge**

* Every “cannot proceed” condition in Phase 1 should raise a `TLQ0Error` subtype, not a raw exception.

---

### SECTION 3: Config System (Dataclasses + Validation + Serialization)

**Capability**

* Define a top-level config object with sub-configs.
* Validate invariants.
* Serialize/deserialize to JSON deterministically.

**Why**

* If your config isn’t structured and snapshotted, you will *never* be sure what changed between runs.
* In later phases, you’ll be tuning search budgets, curriculum settings, retriever settings, etc. Config drift is the #1 silent bug in research codebases.

**What to design**

* `EnvConfig`: Lean-related settings (timeouts, project path, safety flags).
* `SearchConfig`: budgets (max nodes, max depth, max seconds).
* `TrainConfig`: seed, device, batch size (even if training isn’t in Phase 1).
* `TLQ0Config`: schema version + subconfigs.

**Validation philosophy**

* Validation should be strict and loud.
* Keep a `schema_version` so you can evolve configs without breaking old runs.

**Python concepts**

* `@dataclass(frozen=True)`:

  * Frozen = immutable. You can’t accidentally mutate config mid-run.
* `field(default_factory=...)`:

  * Avoid mutable defaults traps.
* JSON roundtrip:

  * dataclasses → dict → JSON
  * JSON → dict → dataclasses

**Aggressive challenge**

* Implement **config “diff printing”**: given two config dicts, print changed keys. This will become one of your most-used debug tools.

---

### SECTION 4: Run Directory Contract + Atomic Writes + Environment Snapshot

**Capability**

* Create a unique run directory.
* Write:

  * `config.json` (snapshotted config)
  * `env.json` (snapshot of environment: python version, platform, git commit if you add it)
  * `events.jsonl` (structured log stream)
  * `artifacts/` directory

**Why**

* Runs are your evidence. Your entire research program is “replay runs and compare curves.”
* Atomic writes prevent corrupt files if your process dies mid-write.

**Run directory layout (contract)**

* `runs/<run_id>/`

  * `config.json`
  * `env.json`
  * `events.jsonl`
  * `artifacts/`

    * (later: checkpoints, plots, dataset shards, macro library snapshots)

**Python concepts**

* `pathlib.Path` is your friend. Use it everywhere instead of string path concatenation.
* Atomic write pattern:

  * write to `file.tmp`
  * rename/replace to `file`
* Environment snapshot:

  * `sys.version`
  * `platform.platform()`
  * optional: versions of torch/numpy if installed

**Aggressive challenge**

* Guarantee: **no two runs ever collide**.
* Guarantee: a run dir always has enough info to “explain itself” even months later.

---

### SECTION 5: RNG Discipline + Determinism Layer

**Capability**

* A single place to seed:

  * Python `random`
  * NumPy RNG
  * PyTorch RNG (CPU and optionally MPS later)
* A local RNG object you pass around (instead of using globals).

**Why**

* Determinism is a spectrum:

  * CPU-only + single-thread can be very deterministic.
  * GPU/MPS + parallelism will introduce nondeterminism.
* You still want best-effort determinism and, crucially, **recorded seeds** so you can replay as closely as possible.

**Design**

* `seed_everything(seed)` sets global seeds.
* `RNG` object contains:

  * a Python `random.Random(seed)` instance
  * a NumPy generator if available
  * a Torch generator if available
* All randomness in tlq0 must go through the `RNG` object (discipline).

**Python concepts**

* Why global RNG is dangerous: hidden state shared across modules.
* `random.Random(seed)` creates an isolated RNG instance (very important).

**Aggressive challenge**

* Write a selfcheck that logs the first 10 RNG samples. With same seed, this must be identical across runs.

---

### SECTION 6: Structured Event Logging + Streaming Metrics

**Capability**

* Write a JSONL event log where each line is a dict containing:

  * timestamp
  * event kind
  * payload
  * optional step counter
* Provide basic meters: mean, min, max, last, counts.

**Why**

* This is your internal “flight recorder.”
* Later, when MDL goes down but solve-rate doesn’t, you’ll need logs to answer: *what actually happened?*
* JSONL is ideal because:

  * append-only
  * streamable
  * easy to load into pandas later

**Event design (contract)**

* An event is:

  * `ts_utc`: ISO timestamp
  * `kind`: string tag like `"run_start"`, `"metric"`, `"selfcheck_rng_sample"`
  * `payload`: JSON-serializable dict
  * `step`: optional int

**Metrics design**

* Meters: e.g. `loss`, `solve_rate`, `backend_latency_s`
* Each meter stores streaming stats.

**Python concepts**

* File handling with context managers:

  * `with open(...) as f:` auto-closes even on errors.
* Why JSONL is better than “print debugging.”

**Aggressive challenge**

* Implement `log_once`: emit some events only once (like environment snapshot) even if called multiple times.

---

### SECTION 7: Core Shell Types for Proof/Search (Stubs Only in Phase 1)

**Capability**

* Define the types that every later phase will use:

  * Action representation
  * ProofState representation
  * Trajectory/Transition representation

**Why**

* These are the “data structures of intelligence” for tlq0.
* The project context explicitly frames intelligence as compression over **state transitions** . So Phase 1 should already define the shapes of those transitions, even if they’re not populated from Lean yet.

**What to define**

* `ActionOp` (Enum): INTRO, EXACT, APPLY, etc. (the convergent minimal DSL) 
* `Action`: `{ op, args }`
* `Hypothesis`: `{ name, type_str }`
* `ProofState`: `{ state_id, goals, hypotheses, raw_backend_metadata }`
* `Transition`: `{ state, action, next_state, ok, error, elapsed_s }`
* `Trajectory`: `{ theorem_id, transitions, success, stats }`

**Python concepts**

* `Enum`: clean, serializable opcodes. Don’t use magic strings.
* `@dataclass(frozen=True)` for immutable records (trajectories shouldn’t mutate).
* Type hints for tuples vs lists:

  * tuple = immutable and hashable-ish (useful for logs/artifacts)

**Aggressive challenge**

* Add `encode()/decode()` for Action so actions can be serialized deterministically.
* Even in Phase 1, prove you can roundtrip.

---

### SECTION 8: CLI (Command-Line Interface) Contract

**Capability**

* Run tlq0 in different modes from the terminal or PyCharm Run Configurations:

  * `init`: create a run dir, snapshot config/env
  * `selfcheck`: run determinism checks + log results
  * optional: `doctor`: verify environment assumptions (torch present, lean path later)

**Why**

* Your CLI is your “kernel syscall interface.”
* Every phase should introduce at least one command or option that makes it testable.

**Python concepts**

* `argparse`: standard CLI parser.
* Subcommands: either manual parsing or `argparse` subparsers.

**PyCharm tip**

* Create Run Configurations:

  * Script path: `tlq0.py`
  * Parameters: `selfcheck --seed 0`
  * Working directory: your repo root
* You’ll iterate much faster than running terminal commands repeatedly.

**Aggressive challenge**

* Every command must create a run directory and write logs; no “naked mode” runs.

---

### SECTION 9: Built-in Test Harness (Inside tlq0.py)

Because you want *everything* in `tlq0.py`, treat tests as another CLI command, like `python tlq0.py test`.

**Capability**

* Run a battery of assertions:

  * config roundtrip
  * stable JSON determinism
  * RNG determinism
  * run dir structure correctness
  * event log validity

**Why**

* You need red/green feedback loops.
* This prevents “Phase 3 broke Phase 1” regressions.

**Python concepts**

* Simple testing without pytest:

  * `assert` statements
  * collecting failures
* (Optional later) you can integrate pytest, but monolith-first is fine.

**Aggressive challenge**

* Tests must run fast (<1s ideally) and must be runnable from PyCharm.

---

## Phase 1 “Definition of Done” Checklist

You are done with Phase 1 when all of these are true:

1. Running `python tlq0.py init --seed 0` creates a fresh run dir with:

   * config snapshot
   * env snapshot
   * events.jsonl
   * artifacts dir

2. Running `python tlq0.py selfcheck --seed 123` logs:

   * first N RNG samples
   * hash of those samples
   * verifies required files exist
   * ends cleanly

3. Running `python tlq0.py selfcheck --seed 123` twice produces **identical** RNG sample event payloads.

4. Your internal test command passes.

If you can’t meet (3), you’re not allowed to proceed. That’s the discipline.

---

## Python Concepts You’ll Be Forced to Learn (and Why They Matter)

### 1) `@dataclass`

Dataclasses are like “Java POJOs generated for free”:

* auto-creates `__init__`, `__repr__`, equality, etc.
* With `frozen=True`, you get immutability (like making fields `final`).

**Why it matters**
Your system is a pipeline of records (states, actions, transitions). Dataclasses make those clean and inspectable.

### 2) Type hints (`typing`)

Python won’t enforce types at runtime by default, but type hints:

* document intent,
* reduce bugs,
* and PyCharm will give you autocomplete + warnings.

**Why it matters**
tlq0 will become a large system in one file. Types will save you.

### 3) `pathlib.Path`

Stop using string paths. Seriously.

* safer joins
* easier existence checks
* cross-platform

### 4) Context managers (`with open(...)`)

Prevents file descriptor leaks and ensures logs flush correctly even on exceptions.

### 5) JSONL logging

Not “print debugging.” JSONL becomes your dataset and your evidence chain.

---

## PyCharm Workflow (Do This Now)

1. **Create a virtual environment** in PyCharm (Settings → Project → Python Interpreter).
2. Add a Run Configuration:

   * Script: `tlq0.py`
   * Params: `selfcheck --seed 0`
3. Turn on:

   * “Show Python Console”
   * “Emulate terminal in output console” (helps with CLI output)
4. Use PyCharm’s “Structure” panel to navigate your sections fast.
5. Use “TODO” comments aggressively:

   * `# TODO(PHASE1): ...` so PyCharm can list them.

---

## Resources (No fluff, just the ones that matter)

* Python official docs:

  * “dataclasses”
  * “typing”
  * “argparse”
  * “pathlib”
* Real Python (site): great practical deep dives (especially argparse + dataclasses)
* “Effective Python” (book) — particularly for idioms and gotchas
* For debugging: learn `pdb` basics (PyCharm debugger is great, but understanding stack frames matters)

---

## Your Phase 1 Assignment (Aggressive)

Implement Phase 1 in `tlq0.py` with the section architecture above, then produce:

1. A run directory from `init`.
2. Two `selfcheck` runs with the same seed whose RNG sample logs are identical.
3. A `test` command that asserts the invariants.

**When you’re done, paste:**

* your section headers (just the section titles, not full code),
* the run directory tree output,
* and one or two example JSONL lines.

Then I’ll review the architecture and we move to Phase 2 (Lean toolchain pinning + smoke checks), which is where the “environment is physics” step begins .

Let’s build the proof OS.


