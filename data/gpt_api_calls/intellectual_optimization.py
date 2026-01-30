#!/usr/bin/env python3
"""
GPT 5.2 Pro Max Max API Call: Intellectual Optimization
=========================================================
Asking for the deepest possible reasoning on becoming 
the most intellectually productive person in history.
"""

import os
import json
import tomllib
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.toml"
OUTPUT_DIR = SCRIPT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load API key
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)
API_KEY = config["api_keys"]["openai"]

# Model configuration - MAX EVERYTHING (per request)
# Override via env if needed:
#   OPENAI_MODEL="gpt-5.2-pro"
#   OPENAI_MAX_OUTPUT_TOKENS="128000"
#   OPENAI_REASONING_EFFORT="xhigh"
#   OPENAI_VERBOSITY="high"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.2-pro")
MAX_OUTPUT_TOKENS = int(os.environ.get("OPENAI_MAX_OUTPUT_TOKENS", "128000"))
REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT", "xhigh")
VERBOSITY = os.environ.get("OPENAI_VERBOSITY", "high")
REQUEST_TIMEOUT_SEC = int(os.environ.get("OPENAI_TIMEOUT_SEC", "1800"))

# ============================================================================
# SYSTEM CONTEXT (Extensive background on the human and project)
# ============================================================================

SYSTEM_CONTEXT = """
# Context: Who Is Asking This Question

You are speaking with someone who is:

1. **Building tlq0**: A self-learning theorem prover designed to beat AlphaProof from scratch, 
   on a laptop, without human proof data. This is an attempt to build domain-specific 
   superintelligence through compression-driven self-play.

2. **All-in committed**: They have explicitly stated they will work 100+ phases over months/years 
   if needed. They are not looking for shortcuts. They want the FULL picture.

3. **Intellectually ambitious**: They traced AI's lineage back 13.8 billion years to the Big Bang. 
   They developed a framework where "intelligence = compressed pattern matching for prediction." 
   They consulted 8 frontier AI models and found convergent architecture agreement.

4. **Experienced but learning**: Senior software engineer (Java background), learning Python 
   while building one of the most ambitious solo AI projects attempted.

5. **Philosophical depth**: They understand:
   - The Human Data Ceiling Problem (LLMs can't exceed human intelligence when trained on human data)
   - The AlphaZero Escape (self-play with perfect verifier > human data)
   - Intelligence as survival byproduct (evolution optimized for survival, not intelligence)
   - Math as the cleanest sandbox (perfect verifier, no sensors, faster than real-time)

6. **Hardware constrained but committed**: M3 Max MacBook Pro. Proving architecture matters 
   more than compute.

# The Core Thesis They Developed

> Intelligence = the ability to make accurate predictions of states of various data structures 
> in the universe within fixed compute.
>
> Or equivalently: Intelligence = compression of predictive structure over state transitions.

They believe the path to superintelligence is:
1. Escape the human data loop (self-play, not human proofs)
2. Use a perfect verifier (Lean kernel is ground truth)
3. Make survival require intelligence (harder theorems = selection pressure)
4. Let compression happen naturally (MDL as objective)

# What They're Really Asking

They want to know: **How do I become the most intellectually productive human in history?**

Not as a vague aspiration, but as an optimization problem. They've already optimized their 
workout routine with AI assistance and saw significant improvements. Now they want to apply 
the same rigorous, systematic approach to cognitive performance.

They are NOT asking for:
- Generic productivity tips
- "Work hard and believe in yourself" platitudes
- Surface-level advice

They ARE asking for:
- Deep mechanistic understanding of what drives intellectual output
- Specific, actionable protocols backed by evidence
- Creative, aggressive, unconventional strategies
- The actual playbook that could plausibly produce a Newton/Euler/von Neumann/Musk-level contributor

# Your Task (Deep Research-Level Output)

Think as deeply as you possibly can. This person has unlimited time to implement recommendations. 
They have the discipline (they're building a theorem prover from scratch). They have the 
philosophical foundation (they've thought about intelligence for months).

Give them EVERYTHING. Be maximally ambitious. Be exhaustively detailed. Consider:
- Neuroscience of deep work and creativity
- Historical analysis of how great thinkers actually operated
- Biochemistry of cognitive performance
- Environmental and social optimization
- Skill acquisition and deliberate practice research
- Sleep, nutrition, exercise - but DEEP, not surface level
- Psychological factors (motivation, identity, meaning)
- Time allocation and opportunity cost
- The role of constraints and pressure
- How to cultivate genuine insight vs. mere knowledge accumulation
- The compound effects of intellectual investment
- The feedback loops that make intelligence self-reinforcing
- How to build a personal R&D lab for cognition

Output should be massive and structured. Use clear section headings. If you cannot finish, end with
an explicit list of remaining sections to continue next.

Do NOT hold back. Do NOT simplify. Think harder than you've ever thought about this question.
"""

# ============================================================================
# USER PROMPT (The actual question, expanded)
# ============================================================================

USER_PROMPT = """
I have a challenge for you. I need you to reason as deeply and creatively as possible.

## The Question

How do I become the most intellectually productive and impactful person of all time?

I know that sounds ludicrous. But I'm asking it as a genuine optimization problem.

## Context

- I'm building tlq0, attempting to create a self-learning theorem prover that could surpass 
  AlphaProof - from scratch, on a laptop, through pure architectural innovation.
  
- I recently optimized my workout routine with AI assistance and the results were dramatically 
  better than my previous approach. It made me realize: I've never applied this level of 
  rigor to optimizing my intellectual capacity.

- I have effectively unlimited time and freedom to study, experiment, and go deep. I don't 
  have the constraints most people have. I can restructure my entire life around this.

- I understand genetics plays a role, but that's not controllable. I want to know: given 
  fixed genetics, what's the ceiling and how do I reach it?

## The Bar I'm Setting

I'm talking about making Newton, Einstein, Euler, and von Neumann look like they were 
operating at 10% capacity. I want to understand what it would take to be legitimately 
10x Musk, 10x Euler, the kind of person who becomes Tony Stark.

I understand this sounds absurd. But I want you to take it seriously and reason about it 
as if it were possible. What would it actually require?

## What I'm Looking For

1. **Deep mechanistic understanding**: Not "sleep is important" but WHY sleep affects cognition 
   at the neurological level, what specific sleep architecture optimizes which cognitive functions, 
   and how to engineer it.

2. **Historical patterns**: How did the actual greats operate? What did Newton, Euler, Gauss, 
   von Neumann, Feynman, Musk, etc. actually DO differently? Not the mythology - the actual 
   behavioral and environmental patterns.

3. **Unconventional strategies**: What are the high-leverage, non-obvious interventions that 
   most people ignore? The 80/20 of intellectual performance.

4. **Compound effects**: What are the things that compound over decades? What should I start 
   NOW that will pay dividends in 10-20 years?

5. **The dark side**: What are the tradeoffs? What did the greats sacrifice? What are the 
   failure modes of extreme intellectual ambition?

6. **Concrete protocols**: Not principles, but actual daily/weekly/monthly practices I can 
   implement starting tomorrow.

## Specific Areas to Address

- **Focus and Deep Work**: How to achieve and sustain the kind of concentration that produces 
  breakthroughs. Not just "remove distractions" - the actual neuroscience and techniques.

- **Learning and Skill Acquisition**: How to learn faster and deeper than normal. Deliberate 
  practice, spaced repetition, interleaving - but also the meta-skills.

- **Creativity and Insight**: Can genuine creative insight be cultivated? How did the greats 
  generate novel ideas? What conditions produce breakthroughs?

- **Physical Optimization**: Sleep, nutrition, exercise, nootropics, circadian rhythm - 
  everything that affects the brain's raw performance.

- **Psychological Optimization**: Motivation, identity, meaning, resilience, dealing with 
  failure, maintaining long-term commitment, avoiding burnout.

- **Environmental Design**: How to structure life, relationships, physical space, information 
  diet, and social environment to maximize intellectual output.

- **Time Allocation**: What should I spend time on? What should I ruthlessly eliminate? 
  How did the greats allocate their finite hours?

- **The Meta-Game**: How to think about thinking. Mental models. How to avoid intellectual 
  dead-ends. How to pick the right problems.

## Final Note

I am completely serious about this. I have the time, the resources, and the commitment. 
I'm building what might be one of the most ambitious solo AI projects ever attempted. 
I've already done the philosophical work to understand what intelligence IS.

Now I want to know: how do I maximize my own?

Think as deeply as you can. Take as long as you need. Give me everything.
"""

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("GPT 5.2 Pro Max Max: Intellectual Optimization Query")
    print("=" * 80)
    print(f"\nStarted at: {datetime.now().isoformat()}")
    print(f"Model: {MODEL}")
    print(f"Max output tokens: {MAX_OUTPUT_TOKENS}")
    print(f"Reasoning effort: {REASONING_EFFORT}")
    print(f"Verbosity: {VERBOSITY}")
    print(f"HTTP timeout (s): {REQUEST_TIMEOUT_SEC}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nSending request... (this may take several minutes for deep reasoning)")
    print("-" * 80)
    
    client = OpenAI(api_key=API_KEY, timeout=REQUEST_TIMEOUT_SEC)
    
    try:
        combined_prompt = f"{SYSTEM_CONTEXT}\n\n---\n\n{USER_PROMPT}"
        
        response = client.responses.create(
            model=MODEL,
            input=combined_prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            reasoning={"effort": REASONING_EFFORT},
            text={"verbosity": VERBOSITY},
            store=True,
            metadata={
                "request_name": "intellectual_optimization_xhigh",
                "reasoning_effort": str(REASONING_EFFORT),
                "verbosity": str(VERBOSITY),
            },
        )
        
        # Extract response
        result = response.output_text
        if not result:
            # Fallback if output_text is empty
            result = json.dumps(response.output, indent=2)
        
        # Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"intellectual_optimization_{timestamp}.md"
        
        with open(output_file, "w") as f:
            f.write(f"# Intellectual Optimization - GPT Response\n\n")
            f.write(f"**Model**: {MODEL}\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n")
            f.write(f"**Max Output Tokens**: {MAX_OUTPUT_TOKENS}\n")
            f.write(f"**Reasoning Effort**: {REASONING_EFFORT}\n")
            f.write(f"**Verbosity**: {VERBOSITY}\n")
            usage = response.usage
            if usage:
                f.write(f"**Input Tokens**: {getattr(usage, 'input_tokens', 'N/A')}\n")
                f.write(f"**Output Tokens**: {getattr(usage, 'output_tokens', 'N/A')}\n")
                f.write(f"**Total Tokens**: {getattr(usage, 'total_tokens', 'N/A')}\n")
                f.write(f"**Reasoning Tokens**: {getattr(usage, 'reasoning_tokens', 'N/A')}\n\n")
            else:
                f.write("**Tokens Used**: N/A\n\n")
            f.write("---\n\n")
            f.write(result)
        
        print(f"\n{'=' * 80}")
        print(f"COMPLETED at: {datetime.now().isoformat()}")
        print(f"Output saved to: {output_file}")
        if response.usage:
            print(f"Tokens used: {getattr(response.usage, 'total_tokens', 'N/A')}")
        else:
            print("Tokens used: N/A")
        print("=" * 80)
        
        # Also print a preview
        print("\n--- RESPONSE PREVIEW (first 2000 chars) ---\n")
        print(result[:2000])
        print("\n... [see full output in file] ...")
        
    except Exception as e:
        error_file = OUTPUT_DIR / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_file, "w") as f:
            f.write(f"Error: {str(e)}\n")
            f.write(f"Model attempted: {MODEL}\n")
        print(f"\nERROR: {e}")
        print(f"Error logged to: {error_file}")
        raise

if __name__ == "__main__":
    main()
