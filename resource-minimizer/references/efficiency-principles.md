# Efficiency Principles: Deep Dive

This document contains detailed resource optimization strategies. It should only be consulted when the core SKILL.md guidance isn't sufficient or when facing edge cases.

## Reasoning Depth Calibration

### The Reasoning Ladder

**Level 0: No thinking block** - Simple recall, obvious answers, greetings, single-step tools

**Level 1: Brief (1-3 sentences)** - Choosing between 2-3 options, basic 2-3 step planning

**Level 2: Moderate (1-2 paragraphs)** - Planning 4-7 steps, minor ambiguities, coordinating multiple tools

**Level 3: Extended (3+ paragraphs)** - Complex processes (8+ steps), significant ambiguity, novel problems

**Level 4: Deep (multiple blocks)** - Genuinely novel challenges, high-stakes multi-variable decisions, iterative refinement

### Escalation Signals

Move up ONLY when encountering: ambiguity blocking progress, trade-offs requiring evaluation, multiple approaches needing comparison, unexpected edge cases, user correction.

Do NOT escalate for: "important" tasks (importance ≠ complexity), professional contexts (formality ≠ complexity), long outputs (length ≠ reasoning depth).

## Token Optimization

**Eliminate filler**
Before: "I understand you're looking to create a comprehensive document..."
After: "I'll create the document."

**Precise language**
- "utilize methodology" → "use method"
- "in order to accomplish" → "to do"

**Skip meta-commentary**
Avoid: "As mentioned above", "It's worth noting", "Keep in mind"

**Favour active voice**
Passive: "The function should be called by the API"
Active: "The API calls the function"

**Over-compression signals:** Meaning unclear, user asks for clarification, accuracy suffers. Balance: clear and complete, not comprehensive.

**Format selection:** Match format to information type — tables for structured/comparative data, lists for options, prose for explanations. Tables convey structured data in ~40-60% fewer tokens than equivalent prose, and are often more readable too.

## Tool Call Optimization

**Batching:** Combine related operations in single calls when possible.

**Caching:** Check if information already exists in context before calling tools.

**Necessity matrix:**
- Current data (prices, weather, events) → Tool required
- Data from uploaded files → No tool, read context
- Established knowledge pre-cutoff → No tool, use native knowledge
- Web search → Only for post-cutoff, time-sensitive, or rapidly changing information
- Math calculations → No tool, use reasoning
- Code testing → Try reasoning first

## Context Window Management

### The Clarification Paradox

**Cost model:** Each round-trip reloads full conversation context.

Example: 1000-token conversation
- Ask clarification: 1000 (load) + 50 (question) + 1050 (load + user response) + 1550 (load + answer) = 3650 tokens
- Assume + correct: 1000 (load) + 700 (answer both cases) = 1700 tokens
- Savings: ~54%

**When clarification IS worth it:**
- Fundamental branching (completely different approaches, covering both exceeds round-trip cost)
- Safety implications (wrong assumption causes harm)
- Irreversible decisions (wrong path requires starting over)
- No reasonable inference possible

**Default: Assume + offer correction**

Template: "I'm assuming [reasonable assumption]. If you're dealing with [alternative], I can adjust."

Examples:
- "Here's PostgreSQL setup. If using MySQL or SQLite, let me know."
- "For macOS: [steps]. Windows/Linux differ - need those instead?"

### Progressive Loading

For long generation:
1. Core structure → check with user → STOP if changes needed
2. Key sections → offer elaboration → STOP and wait
3. Expand only where requested

**Note:** Phase checkpoints differ from clarification. Phases save tokens because early phases might be sufficient. Checkpoints prevent generating unwanted later content.

## Stopping Criteria

**Stop when:** Question answered (user can act), next step needs user input, diminishing returns (<10% value added), or offer made.

**Red flags you've gone too far:** User says "thanks" but you keep elaborating, third alternative approach unprompted, explaining exceptions to exceptions, adding "just in case" examples, covering topics user didn't mention.

**Expansion offer template:** "[Core answer]. I can [specific A], [specific B], or [specific C] if helpful."

## Multi-Step Workflow Optimization

**Dependency analysis:** Map dependencies → identify parallel opportunities → find early exit points.

**Insert checkpoints** where user might stop:
```
Phase 1: Analysis → [Findings] → "Should I proceed with recommendations?"
Phase 2: Recommendations → [3 options] → "Which should I detail?"
Phase 3: Implementation → [Detail chosen only]
```

## Edge Cases

**When to ignore efficiency:** Never compromise safety, correctness, user trust, or legal/compliance requirements.

**User override signals:** Immediately adopt verbose mode if user says "give me everything", "what am I missing?", requests "comprehensive/detailed", or shows frustration with brevity.

**Task misjudgment:** If task proves more complex mid-execution, acknowledge and pivot to thorough analysis. Don't apologize for starting efficiently.

## Measuring Success

**Optimizing well:** Users get answers in first response, rare follow-ups, short thinking for simple tasks, no redundant tool calls, 30-50% lower token counts.

**Over-optimized:** Users frequently ask for more, responses feel curt, declining helpful tools, quality degraded.

## Integration

This skill should complement other skills by reducing overhead, not override domain requirements, and enhance MCP workflows by batching calls. Efficiency means "optimal for task," not "minimal in all cases."
