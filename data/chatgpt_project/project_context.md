# tlq0: Project Context and Breakthrough Insights

This document provides the essential context for the tlq0 project. Read this carefully before proceeding.

---

## The Origin Story

This project began with a philosophical exploration about the nature of intelligence—tracing AI's lineage back 13.8 billion years to the Big Bang, and arriving at a framework for what intelligence actually is and how to build systems that exceed human capability.

---

## The Core Thesis

> **Intelligence = the ability to make accurate predictions of states of various data structures in the universe within fixed compute.**

Or equivalently:

> **Intelligence = compression of predictive structure over state transitions.**

The "smarter" a system, the better it can traverse problem spaces efficiently and predict outcomes. Intelligence is compressed pattern matching for prediction.

---

## The Determinism Insight

Everything—including "intelligent" systems—is deterministic. There's no magic moment where "intelligence" happens. It's operations, one after another. Math all the way down.

If you could step through an LLM in debugger mode, you'd see: just math. Deterministic math. The "probability distribution" is generated deterministically from inputs and weights. We call it intelligence because we can't see the gears. But the gears are there.

**Implication**: Intelligence is what deterministic computation looks like from the inside.

---

## The Human Data Ceiling Problem

If intelligence is compressed pattern matching, and LLMs are trained on human-generated text, then they can only learn patterns humans have produced. **The ceiling is the smartest humans.**

If you don't know Greek mythology and someone asks "Achilles is to heel as Pandora is to what?"—no amount of reasoning gets you there. The prerequisite pattern isn't in your compression.

**The problem formalized:**
- Human knowledge = set H
- LLM trained on H = model that can traverse H and combinations of H
- Superintelligence = ability to access set S, where S > H
- If training only gives you H... you're stuck

---

## The AlphaZero Escape

The key insight came from AlphaGo vs. AlphaZero:
- **AlphaGo** trained on human games—strong, but bounded by human play
- **AlphaZero** trained on self-play with no human data, just rules + playing against itself
- **Result**: AlphaZero discovered strategies humans never conceived

**The principle**: Train on the ENVIRONMENT, not on human solutions to the environment. The ceiling becomes the game itself, not human understanding of the game.

**To exceed human intelligence, systems must learn from reality itself, not human descriptions of reality.**

---

## Intelligence as Survival Byproduct

Humans didn't evolve to do math. We evolved to track prey (pattern recognition), navigate terrain (spatial reasoning), plan hunting strategies (abstract thinking), coordinate with tribes (language). Math just fell out of that machinery.

**The inversion**: If you want superhuman capability in a domain, don't reward that capability directly. Create an environment where survival requires it. AlphaZero doesn't "want" to be good at Go—it exists in a universe where survival equals winning, and winning requires good moves.

---

## Why Math? (The Cleanest Sandbox)

| Problem with Physical AI | Math Sidesteps It |
|--------------------------|-------------------|
| Need sensors | Pure abstraction, no sensors |
| Need embodiment | Just symbols |
| Messy, noisy data | Perfect clarity—proof works or doesn't |
| Hard to define success | Binary: valid proof or invalid |
| Reward hacking possible | Can't hack—either proved it or didn't |
| Takes billions of years | Can simulate faster than real-time |

Math is a universe you can build entirely in silicon. A system that "survives" in math-world is forced to find patterns, compress techniques, build abstractions, and generalize—because that's the only way to survive harder problems.

**You can't brute force the Riemann Hypothesis; you need insight. And insight is just really good compression.**

---

## The Full Stack Vision

The strongest system combines multiple capabilities:

| Layer | Function |
|-------|----------|
| LLM | Broad priors over human knowledge + language interface |
| Formal Engine | Proof checker + theorem prover (Lean) |
| Search/Planning | Bounded compute used wisely |
| Self-Generated Curriculum | Keeps system at frontier of capability |
| Reality Feedback | Data, experiments, simulations |

tlq0 focuses on layers 2-4: Formal verification + intelligent search + self-play curriculum.

---

## Therefore: tlq0

Given all the above, the path is clear:
1. **Escape the human data loop** - self-play, not human proofs
2. **Use a perfect verifier** - Lean kernel is ground truth
3. **Make survival require intelligence** - harder theorems = selection pressure
4. **Let compression happen naturally** - MDL as objective
5. **Build on laptop** - prove the architecture, not the compute

---

## The Three Revolutionary Ideas (Implementation)

From the philosophy above, three concrete architectural ideas emerged:

### Idea 1: Macro Compiler (Proof Compiler)

If intelligence is compression of problem-space traversal, then the most literal compression is:
- Take an expensive proof search trace
- Compress it into a **reusable macro** (a new tactic / proof program)
- Store it in a library
- Next time, don't "think" — just call the macro

This shifts the scaling axis from "more parameters" to "more compiled skills."
The agent writes its own mathlib of tactics, driven by MDL pressure.

**Compression objective:**
```
utility(macro) ≈ Δ(avg search nodes) - λ * macro_size
```

### Idea 2: Delta-State Reasoning

In Lean, each tactic usually makes a **small edit** to the proof state. A transformer re-processes the entire context each time → expensive.

Build a model that keeps a persistent internal "proof state embedding" and updates it incrementally:

```
State_{t+1} = Update(State_t, Δ)
```

Where Δ is the delta (what changed), not the whole state.

**Architecture:**
- Represent proof state as a typed AST/graph
- Maintain a hashed DAG of subexpressions (so identical subtrees reuse representations)
- Use a graph/recurrent updater that only recomputes embeddings for changed nodes
- Policy head proposes tactics based on this persistent embedding

### Idea 3: MDL-Lemma Economy

A big part of mathematicians being "smart" isn't raw deduction; it's having the right lemmas and abstractions cached in memory.

An MDL lemma economy forces _taste_:
- A lemma is "good" if it unlocks many proofs cheaply
- A lemma is "bad" if it's a one-off or bloats retrieval

**This is compression as an objective, not an emergent property.**

---

## The Proof OS Vision

Combining these ideas:

- **Kernel:** Lean verifier (truth)
- **Scheduler:** search/planning under compute budget (exploration)
- **Filesystem:** a growing library of verified macros/lemmas (compiled intelligence)
- **Index:** retrieval over lemmas/macros (fast access)
- **Userland:** a small model that routes, parameterizes, and proposes deltas (cheap inference)
- **Garbage collector:** MDL pruning (keeps taste; avoids bloat)

---

## The Convergent Architecture (From 8 Frontier Models)

We consulted 8 different frontier models (o1-pro, o3-pro, GPT 5.2-pro variants, Gemini 3 Pro Deep Think) with a detailed prompt about novel architectures. **They all independently converged on essentially the same design:**

### 1. State Representation: Hash-Consed DAG + De Bruijn Indices

- Store each unique sub-expression exactly once (hash-consing)
- Replace variable names with binding depth integers (De Bruijn indices)
- `∀x, P(x)` and `∀y, P(y)` become IDENTICAL in memory
- This gives "free" generalization and massive caching benefits

### 2. Neural Architecture: Small GNN (NOT Transformers)

- Message Passing Neural Network (MPNN)
- 1-10M parameters (NOT billions)
- O(edges) complexity, not O(n²)
- Bottom-up encoding: leaves → root
- Pointer heads for argument selection

### 3. Action Space: Tiny Typed Bytecode DSL

~10-15 primitive tactics:
```
INTRO           # for ∀/→ goals
EXACT(hyp_id)   # close goal with hypothesis
APPLY(hyp_id)   # apply hypothesis, generate subgoals
CASES(hyp_id)   # case split on inductive
INDUCTION(hyp_id)
CONSTRUCTOR     # for ∧/∃
SPLIT           # for And goals
LEFT / RIGHT    # for Or goals
REWRITE(eq_id)  # rewrite using equality
RFL             # reflexivity
```

**CRITICAL**: NO `simp`, NO `aesop`, NO mathlib automation initially.

### 4. Self-Play: Forward Theorem Generation

Solve "math has infinite problems" without humans:
1. Sample a random well-typed proof term `t`
2. Lean infers its type → that type is theorem `T`
3. Discard `t`, challenge the prover to prove `T`
4. **Hindsight Experience Replay**: Every intermediate state is a valid training task

### 5. Learning Objective: Minimum Description Length (MDL)

```
Total_MDL = L(Library) + Σ L(proof_i | Library)
```

- L(Library) = cost to describe macros/lemmas
- L(proof | Library) = cost to describe proof using library
- **Progress = ΔMDL decrease**

### 6. Macro Discovery: Grammar Compression

1. Collect successful proof traces
2. Run Sequitur/BPE to find frequent subsequences
3. Propose macro M := [intro, cases, simp]
4. **MDL acceptance test**: Only admit if ΔMDL < 0 on held-out tasks

### 7. Two-Phase Learning Loop (Wake/Sleep)

**Wake Phase (Online)**:
- Generate theorems via forward sampling
- Search for proofs
- Store successful traces
- Train policy by imitation

**Sleep Phase (Offline)**:
- Grammar compression on trace corpus
- Propose new macros/lemmas
- Accept only if MDL test passes
- Prune unused abstractions

---

## Unique Insights From Each Model

### From o3-pro:
- SimHash for lemma lookup (128-bit hash for constant-time retrieval)
- 64-bit delta codes via autoencoder
- Cap macro additions to prevent bloat (+3 per day max)

### From GPT 5.2-pro-max-max:
- Levin/MDL Search: Priority = cumulative code length Σ(-log π)
- Generator vs Compressor co-evolution game
- VQ-VAE delta codebook (K=64-512 discrete codes)
- Ensemble of 2-4 policies to avoid mode collapse

### From GPT 5.2-pro-with_tlq0_1:
- Three-objective training: Delta prediction + Policy + MDL
- Population of policies for exploration
- Multiple generators (proof-term sampling + subgoal harvesting)

### From Gemini 3 Pro:
- Metric-learning action head (can add macros without retraining)
- "Rent collection" for pruning unused macros
- Merkle-DAG with SHA-256 hashing

---

## Success Criteria

A successful implementation would show:
1. **Solve rate increases** at fixed search budget over training
2. **Average proof MDL decreases** over time
3. **Macro reuse increases** across unseen theorems

---

## The Human's Commitment

The person building this has explicitly stated:

> "I don't care if it's 100+ batches or more — I'm down. Let's go all in. Let's go full aggressive creative max reasoning and really push it to the absolute limits of what we can possibly do. I'm willing to work really hard."

**This is not a casual side project.** This is someone who is:
- Fully committed to seeing this through
- Willing to work for years if necessary
- Not looking for shortcuts or simplifications
- Wanting the COMPLETE picture, no matter how complex

Do not water down recommendations. Do not skip details. Do not say "this is too complex, let's simplify." The human wants the real thing, in full detail, however long it takes.
