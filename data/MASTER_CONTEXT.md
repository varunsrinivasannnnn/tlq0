# tlq0 (The Last Question) - Master Context for Cursor

Use this file to onboard Cursor/Claude to the tlq0 project.

---

## Quick Summary

**tlq0** = Self-learning theorem prover that learns from scratch through compression-driven self-play.

**Core thesis**: Intelligence = compression of predictive structure over state transitions.

**Architecture**: MONOLITH - everything in `tlq0.py`.

**Timeline**: 100 days to beat AlphaProof (aggressive target, that's the mindset).

---

## Project Files

All files for ChatGPT Project are in `data/chatgpt_project/`:

| File | Purpose |
|------|---------|
| `system_prompt.md` | Copy to ChatGPT Instructions field |
| `intelligence_journey.md` | Upload - philosophical foundation |
| `project_context.md` | Upload - bridge to implementation |
| `initial_prompt.md` | First message to send |

---

## The Philosophy (Summary)

1. **Intelligence = compressed pattern matching** for prediction
2. **Human Data Ceiling**: LLMs trained on human data can't exceed human intelligence
3. **AlphaZero Escape**: Self-play with perfect verifier > human data
4. **Math = cleanest sandbox**: Binary verifier, no sensors, faster than real-time
5. **Compression as objective**: MDL drives everything

---

## The Three Revolutionary Ideas

1. **Macro Compiler**: Compress proof traces into reusable macros
2. **Delta-State Reasoning**: Update embeddings incrementally, not full reprocess
3. **MDL-Lemma Economy**: Taste through compression pressure

---

## The Convergent Architecture

8 frontier models agreed on:
- Hash-consed DAG + De Bruijn indices
- Small GNN (1-10M params), NOT transformers
- Tiny typed bytecode DSL (~15 primitives)
- Forward theorem generation (self-play)
- MDL learning objective
- Wake/Sleep learning loop

---

## 100-Day Timeline (Private - Not Shared with GPT)

| Day | Milestone |
|-----|-----------|
| 1-15 | M0: Foundation |
| 16-35 | M1: DSL + search |
| 36-55 | M2: Forward gen + data |
| 56-80 | M3: First learning |
| 81-100 | M4+: GNN + delta |

---

## Starting a New Cursor Chat

Tag this file and say:

> "Read the master context. I'm on Day X of 100. Help me with [task]."

For code context: `@tlq0.py`

---

## Workflow

- **Primary**: ChatGPT UI (has full context)
- **Secondary**: Cursor/Claude (for code reviews, debugging)
- **Escalation**: GPT API (for major decisions)
