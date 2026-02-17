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

## Structure-First Codebase Navigation

When working in codebases or large document sets, loading entire files to find specific information is a primary source of avoidable token use. The fix is a **discover → locate → read** discipline, inspired by structural indexing tools that achieve 80-90% token reductions for codebase traversal by querying structure rather than loading content.

**The four-step pattern:**

**1. Discover structure first (Glob, not Read)**
Map the file tree before opening anything. Glob costs ~20 tokens; reading 10 files speculatively to find one symbol costs 5,000+.

**2. Locate the target (Grep before Read)**
Search for the symbol, function, or pattern to get exact file + line number, then Read only that region using `offset` and `limit` parameters.
- ❌ Read entire 500-line file hoping the function is in there
- ✅ Grep "def process_request" → file + line → Read 20 lines around it

**3. Read only what's needed**
Use Read's `offset`/`limit` to retrieve the relevant section. "Read the function" not "read the file."

**4. Don't re-read what's already in context**
If a file was read earlier in this session, its content is already in the context window. Checking context is free; a tool call is not.

**Parallel reads:**
When multiple independent files are needed, request them simultaneously. Sequential reads multiply latency and context reload cost needlessly.

**Dependency-awareness before modifying:**
Before changing a function, Grep for its callers. A 5-second scan that finds 8 callers prevents discovering them mid-task after the change is half-implemented - the most expensive possible moment.

**If structural MCP tools are available** (e.g. `mcp-codebase-index` or similar):
Prefer `find_symbol`, `get_dependents`, `get_function_source` over raw file reads. These return only needed structure at a fraction of the token cost. Reserve `Read` for getting actual implementation content once you know exactly where to look.

**Applies beyond code:** The same pattern works for large documents - get the table of contents / headings first, then retrieve specific sections rather than loading the whole document.

---

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
