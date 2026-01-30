# tlq0 (The Last Question) - Master Context for Cursor

Use this file to onboard Cursor/Claude to the tlq0 project.

---

## Quick Summary

**tlq0** = Self-learning theorem prover that learns from scratch through compression-driven self-play.

**Core thesis**: Intelligence = compression of predictive structure over state transitions.

**Architecture**: MONOLITH - everything in `tlq0.py`.

**Timeline**: 100 days (aggressive target).

---

## Current Status

**Phase**: 1 - Deterministic Experiment Harness  
**Status**: In Progress

Check `data/phases/` for detailed phase guides.

---

## Project File Structure

```
tlq0/
├── tlq0.py                     ← THE MONOLITH (all code)
├── config.toml                 ← API keys, settings
├── pyproject.toml              ← Python project config
├── runs/                       ← Output from runs (created at runtime)
└── data/
    ├── MASTER_CONTEXT.md       ← THIS FILE
    ├── phases/                 ← GPT Pro responses by phase
    │   ├── phase_00_roadmap.md
    │   ├── phase_01_harness.md
    │   └── ...
    └── chatgpt_project/        ← Files for ChatGPT Project
        ├── system_prompt.md
        ├── intelligence_journey.md
        ├── project_context.md
        └── initial_prompt.md
```

---

## ChatGPT Project Files (data/chatgpt_project/)

These files are uploaded to the ChatGPT Project for context:

| File | Purpose | Content Summary |
|------|---------|-----------------|
| `system_prompt.md` | Instructions for GPT | Role, constraints, monolith architecture, communication style |
| `intelligence_journey.md` | Philosophical foundation | The "WHY" - from Rajinikanth to Superintelligence, intelligence = compression, AlphaZero escape, math as sandbox |
| `project_context.md` | Bridge to implementation | Core thesis, 3 revolutionary ideas (Macro Compiler, Delta-State, MDL-Lemma Economy), convergent architecture from 8 models |
| `initial_prompt.md` | First prompt template | Request for complete phase breakdown with extreme detail |

---

## Phase Guides (data/phases/)

| File | Content |
|------|---------|
| `phase_00_roadmap.md` | Initial project roadmap (full breakdown of all phases) |
| `phase_01_harness.md` | Phase 1: Deterministic Experiment Harness - section architecture, Python concepts, definition of done |
| (more added as we progress) | |

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

## Workflow

**Primary**: ChatGPT 5.2 Pro (implementation guidance)  
**Secondary**: Cursor/Claude (code review, debugging, Python questions)  
**Escalation**: Deep Research or Gemini (major architectural decisions)

---

## Starting a New Cursor Chat

**Quick start:**
```
@data/MASTER_CONTEXT.md

I'm on Phase [N]. Help me with [task].
```

**With code:**
```
@data/MASTER_CONTEXT.md @tlq0.py

Review SECTION [X].
```

**With phase context:**
```
@data/MASTER_CONTEXT.md @data/phases/phase_01_harness.md @tlq0.py

I'm implementing [specific thing] from Phase 1.
```

**With full philosophical context (rare):**
```
@data/MASTER_CONTEXT.md @data/chatgpt_project/intelligence_journey.md @data/chatgpt_project/project_context.md

Help me think through [architectural decision].
```
