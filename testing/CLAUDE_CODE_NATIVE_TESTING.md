# Claude Code Native Testing

## The Simple Way - Just Ask Me!

You can run automated tests entirely within this Claude Code session by simply asking:

```
"Test the resource-minimizer skill with scenarios 3 and 5"
```

Or:

```
"Run automated skill tests with the quick test scenarios"
```

I will:
1. Load the skill instructions from the repo
2. Load the test scenarios
3. Spawn baseline agents (without skill) using Task tool
4. Spawn optimized agents (with skill) using Task tool
5. Capture their outputs
6. Compare metrics
7. Show you transparent results

## How It Works

### Architecture

```
You: "Test the skill with scenario 3"
  ↓
Claude (me): Orchestrator
  ↓
  ├─→ Task(baseline_agent) → Response A
  └─→ Task(optimized_agent) → Response B
  ↓
Compare A vs B → Report
```

### What I Do

1. **Load Resources**
   - Read `/resource-minimizer/SKILL.md`
   - Read `/testing/test_scenarios.json`
   - Select requested scenarios

2. **Spawn Baseline Agent**
   ```
   Task tool with prompt:
   "You are Claude. Help with: [scenario prompt]"
   ```

3. **Spawn Optimized Agent**
   ```
   Task tool with prompt:
   "You have resource-minimizer skill enabled.
   [Full skill instructions]

   Help with: [scenario prompt]"
   ```

4. **Capture & Compare**
   - Extract metrics from both responses
   - Count tokens (word count × 1.3)
   - Count tool uses
   - Measure quality
   - Calculate reductions

5. **Report Results**
   - Show side-by-side comparison
   - Display reduction percentages
   - Provide full transcripts for transparency

## Example Session

### You Say:
```
Test the resource-minimizer skill with scenario 3
```

### I Do:
```
Loading skill instructions from repo...
✓ Skill loaded: resource-minimizer v1.0.0

Loading test scenario 003: "Research Task - Security Practices"
✓ Scenario: "What are the current best practices for securing REST APIs?
             I'm building a financial services application."

[1/2] Spawning BASELINE agent (no skill)...
  Task ID: baseline_scenario_003

[Agent working...]

✓ Baseline complete: 1,560 tokens, 2 tool calls

[2/2] Spawning OPTIMIZED agent (with skill)...
  Task ID: optimized_scenario_003

[Agent working...]

✓ Optimized complete: 494 tokens, 1 tool call

================================================================================
COMPARISON RESULTS
================================================================================
Scenario: Research Task - Security Practices

Baseline Agent (No Skill):
  - Tokens: 1,560
  - Tool calls: 2
  - Response: Comprehensive coverage of all security practices...

Optimized Agent (With Skill):
  - Tokens: 494
  - Tool calls: 1
  - Response: Concise key practices with offer to expand...

Reduction:
  - Token reduction: 68.3% ✓
  - Tool call reduction: 50.0% ✓
  - Meets target (>30%): YES ✓

Full transcripts saved to:
  /testing/test_results/scenario_003_baseline.txt
  /testing/test_results/scenario_003_optimized.txt
================================================================================
```

## Transparency

You can verify everything by:

1. **Reading the prompts I gave to agents**
   - I'll show you exactly what system prompt each agent received
   - You can verify baseline had NO skill instructions
   - You can verify optimized HAD skill instructions

2. **Reading the full agent responses**
   - I'll save complete transcripts
   - You can see exactly what each agent said
   - Compare them side-by-side

3. **Checking the metrics**
   - Word counts are visible
   - Tool calls are trackable
   - Math is transparent

## Quick Commands

### Test Single Scenario
```
"Test skill with scenario 3"
```

### Test Multiple Scenarios
```
"Test skill with scenarios 1, 3, and 5"
```

### Quick Test (5 scenarios)
```
"Run quick skill test"
```

### Custom Scenario
```
"Test the skill with this prompt: [your custom prompt]"
```

## What Gets Generated

After testing, you'll have:

```
testing/claude_code_test_results/
└── test_TIMESTAMP/
    ├── baseline_scenario_003_full.txt       # Complete baseline response
    ├── optimized_scenario_003_full.txt      # Complete optimized response
    ├── comparison_scenario_003.json         # Metrics comparison
    └── test_summary.txt                     # Overall results
```

## Advantages

✅ **No API key needed** - runs in your session
✅ **No external setup** - everything in Claude Code
✅ **Real-time visibility** - watch agents work
✅ **Full transparency** - see all prompts and responses
✅ **Interactive** - ask questions during tests
✅ **Immediate results** - no waiting for external processes

## Example Test Flows

### Flow 1: Quick Validation
```
You: "Test skill with scenario 5 to see if it's working"
Me: [Runs test, shows results]
You: "Show me the full baseline response"
Me: [Shows complete baseline transcript]
You: "Now show the optimized one"
Me: [Shows complete optimized transcript]
```

### Flow 2: Comprehensive Testing
```
You: "Run quick test (5 scenarios)"
Me: [Runs all 5, shows progress]
You: "Which scenario showed the biggest reduction?"
Me: [Analyzes and reports]
You: "Show me that comparison in detail"
Me: [Provides detailed breakdown]
```

### Flow 3: Custom Testing
```
You: "Test the skill with this scenario: 'Build me a REST API with auth'"
Me: [Creates custom test, runs both agents]
You: "The optimized one seems too brief. Show me its full response"
Me: [Shows complete response]
```

## Limitations

1. **Token counting is approximate** (word count × 1.3)
   - For exact counts, use the API-based runner
   - For comparison purposes, approximation works fine

2. **Can't control skill installation**
   - Agents get skill via instructions in prompt
   - Not via actual skill installation
   - Functionally equivalent for testing

3. **Sequential execution**
   - Agents run one at a time (baseline, then optimized)
   - Not parallel (but still fast)

## When to Use This vs API Runner

### Use Claude Code Native (This):
- ✅ Quick tests during development
- ✅ Interactive exploration
- ✅ No API key available
- ✅ Want to ask questions during tests
- ✅ Iterating on skill improvements

### Use API Runner:
- ✅ Need exact token counts from Anthropic API
- ✅ Want to run 100+ scenarios
- ✅ Publishing results externally
- ✅ Need perfect reproducibility
- ✅ Want to archive test runs long-term

## Get Started

Just say:

```
"Test the resource-minimizer skill with scenario 3"
```

And I'll handle everything!

---

**The beauty of this approach: it's as simple as having a conversation.**

No setup. No configuration. No external tools. Just ask, and I'll orchestrate the testing using Claude Code's native capabilities.
