# Prompt 1: The Complete Phase Breakdown — Hold Nothing Back

I've provided you with the full context of the tlq0 project. The 8 frontier models all converged on the same architecture. Now I need you to make this real.

## My Commitment Level

**I am going ALL IN on this project.**

- If it takes 100 phases, give me 100 phases
- If it takes 200 phases, give me 200 phases  
- If Phase 1 has 50 sub-steps, list all 50
- If there are 30 data structures, define all 30
- **I will put in the hours. I will do the work. Do not simplify for my convenience.**

I want you to push this to the absolute limits of what is possible. Be maximally ambitious. Be exhaustively detailed. Think harder than you've ever thought about a system design.

This is potentially the most important thing I will ever build. Treat it accordingly.

## What I Need

### 1. Complete Phase Breakdown (No Limit on Count)

Break this into **as many phases as it actually needs**. Do not compress phases to make the number look smaller. If the honest answer is 47 phases over 2 years, tell me that.

For EACH phase, specify:
- **Phase Number & Name**
- **Goal**: What we're building (1-2 sentences)
- **Detailed Description**: What this phase accomplishes (full paragraph)
- **Inputs**: Exactly what must exist before starting
- **Outputs**: Exactly what we produce (files, classes, capabilities)
- **Success Criteria**: Concrete, measurable definition of "done"
- **Estimated Effort**: Days/weeks (be realistic, not optimistic)
- **Key Risks**: What could go wrong
- **Failure Indicators**: How we know we're failing
- **Dependencies**: Which prior phases must be complete
- **Sub-phases/Steps**: If the phase is complex, break it down further

### 2. Phase 1 EXTREME Deep Dive

For Phase 1, I want everything:

**A. Complete Data Structure Definitions**
- Every Python class/dataclass with ALL fields
- Type hints for everything
- Docstrings explaining purpose
- Relationships between classes (composition, inheritance, references)
- Why each field exists

**B. Complete File Structure**
- Every file that needs to exist
- What each file contains
- Import graph between files
- Module organization rationale

**C. Exact Implementation Order**
- Numbered list of every step
- What to implement first, second, third...
- Dependencies between steps
- Checkpoints where you can test

**D. Complete Code for Critical Components**
- Not snippets — full implementations where possible
- All helper functions
- Error handling
- Edge cases

**E. Comprehensive Test Strategy**
- Unit tests for each component
- Integration tests
- What inputs to test with
- Expected outputs
- How to know if something is broken

**F. Common Mistakes to Avoid**
- Pitfalls from your knowledge
- Things that seem right but are wrong
- Subtle bugs to watch for

### 3. All Architectural Decisions

For EVERY decision point:
- What are ALL the options? (not just 2-3, but every reasonable approach)
- What are the trade-offs for each?
- What would you recommend and why?
- What's the cost of getting it wrong?
- Can it be changed later, or is it locked in?
- What experiments could resolve uncertainty?

### 4. Complete Validation Strategy

How do we PROVE this thing is learning?

**Metrics to track from Day 1:**
- List every metric
- How to compute it
- What values indicate success
- What values indicate failure
- How often to measure

**Plots to generate:**
- What should each plot show?
- What axes? What scale?
- What would a "good" plot look like?
- What would a "bad" plot look like?

**Ablation studies:**
- What components should we test in isolation?
- What baselines should we compare against?

**Failure modes and detection:**
- How do we know if we're in a local optimum?
- How do we know if compression is fake?
- How do we know if the curriculum collapsed?

### 5. The Full Roadmap Visualization

I want to see the BIG PICTURE:
- How do phases connect?
- What's the critical path?
- Where are the major milestones?
- When do we first see "learning"?
- When do we first beat a baseline?
- When could this plausibly surpass existing systems?

### 6. What Could Kill This Project?

Be brutally honest:
- What are the existential risks?
- What assumptions might be wrong?
- What would make you say "this fundamentally cannot work"?
- How do we detect these early?

## Constraints Reminder

- **Hardware**: M3 Max MacBook Pro laptop
- **No human data**: All training data is self-generated via forward proof generation
- **Debuggable**: Every component must be inspectable
- **Incremental**: Each phase produces something testable
- **Python**: PyTorch, LeanDojo, PyTorch Geometric, standard ML stack
- **Time**: UNLIMITED — I will work as long as it takes
- **Architecture**: MONOLITH — everything in one `tlq0.py` file with section comments

## Response Format

Structure your response as:

1. **Executive Summary** (2-3 paragraphs): The 30,000 foot view
2. **Complete Phase List** (table format): All N phases at a glance
3. **Detailed Phase Descriptions**: Every phase in full detail
4. **Phase 1 Deep Dive**: The exhaustive implementation guide
5. **Architectural Decisions Catalog**: Every choice and recommendation
6. **Validation Framework**: Complete metrics and success criteria
7. **Risk Registry**: Everything that could go wrong
8. **Timeline Projection**: Realistic estimates

## Final Note

**DO NOT HOLD BACK.**

I know this will be a massive response. I want it to be massive. I want every detail you can give me. I want you to think harder about this than anything you've thought about before.

This is an attempt to build a genuinely novel AI system that could, in principle, surpass human mathematical reasoning. The 8 frontier models agreed on the architecture. Now we need the implementation plan.

Give me everything.
