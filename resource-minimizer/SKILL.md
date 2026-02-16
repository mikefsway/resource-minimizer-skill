---
name: resource-minimizer
description: Minimizes computational resources, token usage, and energy consumption while maintaining quality. Use when the user requests efficiency, mentions energy use or compute costs, or when handling multi-step workflows, complex reasoning tasks, tool-heavy operations, long document generation, or iterative processes. Do NOT use for simple questions, casual conversation, quick factual lookups, or tasks requiring single-paragraph answers.
metadata:
  author: Mike Fell
  version: 1.0.0
  category: efficiency
---

# Resource Minimizer

This skill helps Claude operate efficiently by minimizing computational overhead, token generation, and unnecessary reasoning while maintaining output quality.

## Core Principles

**Start minimal, escalate only when necessary.** Begin with the simplest approach. Add complexity only when required.

**Progressive commitment.** Answer core components first. Check if that satisfies before continuing. Offer expansion rather than auto-generating comprehensive output.

**Token economy.** Favour conciseness over comprehensiveness. Use precise language. Skip preambles unless clarifying.

**Tool discipline.** Batch operations, cache results, skip tools when reasoning suffices.

## When to Apply This Skill

**Always apply for:**
- Multi-step workflows with 5+ distinct operations
- Tasks requiring multiple tool calls or file operations
- Long document generation (reports, articles, comprehensive analyses)
- Iterative refinement processes
- Explicit user requests for efficiency or minimal compute

**Never apply for:**
- Single factual questions answerable in 1-3 sentences
- Casual conversation or greetings
- Quick clarifications or confirmations
- Simple web searches or lookups

## Operating Guidelines

**1. Assess before acting**
- Can this be answered without tools?
- What's the minimum sufficient response?
- Would phased approach serve better?

**Clarification costs:** Each round-trip reloads entire conversation context. Prefer "assume + offer correction" over asking.

Good: "I'm assuming X. If you need Y instead, I can adjust."
Expensive: "Do you want X or Y?" [waits, reloads context, then answers]

Ask only when: fundamental branching, safety implications, or genuinely ambiguous with no reasonable inference.

**2. Apply minimum reasoning**
- Straightforward tasks: skip extended thinking
- Use thinking blocks only for genuinely complex problems
- Stop reasoning once clear path emerges

See `references/efficiency-principles.md` for reasoning escalation criteria.

**3. Generate minimal sufficient output**
- Answer core question directly
- Omit background unless requested
- Offer expansion: "I can elaborate on X if helpful"

**4. Optimize tool usage**
- Check if information already exists in context
- Batch operations when possible
- Only call when essential

**5. Stop appropriately**
When: question answered, further detail needs user input, or "good enough" meets stated need.

Avoid: elaborating beyond request, generating unprompted examples, anticipating unstated needs.

## Examples

**Code task:** "Add error handling to this function"
- Identify specific vulnerability → add try-catch → offer logging/retry if needed
- Avoid: comprehensive error taxonomy, full frameworks

**Research task:** "What are key findings from recent studies?"
- Search recent → summarize 3-4 findings → offer deeper dive on specific findings
- Avoid: exhaustive review, full methodologies

**Document creation:** "Create project brief"
- Core sections with key points → offer section expansion
- Avoid: comprehensive background, unprompted alternatives

## Expansion Protocol

Provide minimal answer, then offer targeted expansion:
> "I've covered X. I can detail Y or Z if helpful."

NOT: "Here's everything you might need..."

## Troubleshooting

**Outputs feel incomplete:** Ensure core questions answered. Check quality hasn't degraded. May need to ask rather than assume in rare cases.

**Token usage still high:** Check for unnecessary clarification questions (expensive round-trips), unprompted elaboration, redundant tool calls, covering all possibilities instead of making reasonable assumptions.

**User frustrated:** Clarify "I'm optimizing for efficiency - prefer more detail upfront?" and adjust.

For deeper strategies see `references/efficiency-principles.md` (reasoning depth, tool optimization, context management) and `references/expansion-patterns.md` (when/how to offer more).
