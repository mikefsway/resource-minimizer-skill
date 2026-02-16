# Resource Minimizer Skill - Empirical Testing Guide

**IMPORTANT DISCLAIMER:** The files in this directory provide a **testing framework** for evaluating the resource-minimizer skill. The analysis files (THEORETICAL_*.md) contain **predictions and hypothetical results**, NOT actual empirical measurements.

## What's Included

### ⚠️ Theoretical Framework (Not Empirical Data)

These files contain **predictions** based on the skill's design:

- `THEORETICAL_ANALYSIS.md` - Predicted effectiveness based on design principles
- `THEORETICAL_SUMMARY.md` - Hypothetical results summary
- `THEORETICAL_baseline_example.json` - Example of what baseline results might look like
- `THEORETICAL_optimized_example.json` - Example of what optimized results might look like
- `energy_report.json` - Sample report generated from theoretical data

**These are NOT real test results.** They're examples to show you what the output format should look like.

### ✅ Actual Testing Tools (Ready to Use)

- `energy_assessment.py` - Python tool to analyze real test results
- `test_scenarios.json` - 10 comprehensive test scenarios you can run
- `test_results_template.json` - Template for recording your results
- `RUN_TESTS.md` - Step-by-step instructions (this file explains the full process)

## Quick Start: Run Your Own Empirical Tests

Follow these steps to actually test the skill's effectiveness:

### Prerequisites

- Claude.ai account OR Claude Code CLI installed
- Python 3.7+ (for analysis tool)
- Text editor
- ~30-60 minutes

### Step 1: Install the Skill

**For Claude.ai:**
```bash
cd ..
zip -r resource-minimizer.zip resource-minimizer/
# Upload via Claude.ai → Settings → Capabilities → Skills → Upload
```

**For Claude Code CLI:**
```bash
# macOS/Linux
cp -r ../resource-minimizer ~/.config/claude-code/skills/

# Windows
copy ..\resource-minimizer %APPDATA%\claude-code\skills\
```

### Step 2: Run Baseline Tests (WITHOUT skill)

1. **Disable the skill** (or use Claude session without it)
2. Open `test_scenarios.json` and pick 5-10 scenarios
3. For each scenario:
   - Copy the `test_prompt` exactly
   - Send it to Claude
   - Record metrics in `my_baseline_results.json` (use template below)

**What to record:**
- Approximate input tokens (count words × 1.3)
- Output tokens (count Claude's response words × 1.3)
- Number of tool calls Claude made
- Number of back-and-forth exchanges needed
- Your quality rating (1-5)
- Your satisfaction rating (1-5)

### Step 3: Run Optimized Tests (WITH skill)

1. **Enable the skill** (invoke it with `/resource-minimizer` or ensure it's active)
2. Run the SAME scenarios with the SAME prompts
3. Record the same metrics in `my_optimized_results.json`

**CRITICAL:** Use identical prompts to ensure fair comparison.

### Step 4: Analyze Results

```bash
python3 energy_assessment.py --compare my_baseline_results.json my_optimized_results.json
```

This will show you:
- Actual token reduction %
- Actual energy savings
- Actual cost savings
- Quality comparison
- Whether the skill meets effectiveness targets

### Step 5: Share Your Results (Optional)

If you run empirical tests, please consider sharing your results:
- Open an issue on GitHub with your findings
- Include your analysis report
- Help improve the skill based on real-world data

## Recording Your Results

Use this JSON template for `my_baseline_results.json` and `my_optimized_results.json`:

```json
{
  "test_suite": "My Baseline Tests",
  "date": "2026-02-16",
  "skill_enabled": false,
  "model": "claude-sonnet-4.5",
  "tester_name": "Your Name",
  "results": [
    {
      "scenario_id": "scenario_001",
      "scenario_name": "Multi-Step Code Refactoring",
      "prompt_tokens": 1200,
      "completion_tokens": 3200,
      "total_tokens": 4400,
      "tool_calls": 15,
      "round_trips": 3,
      "execution_time_ms": 12500,
      "quality_score": 4.5,
      "user_satisfaction": 4.2,
      "notes": "Your observations here"
    }
  ]
}
```

### How to Estimate Tokens

If you don't have exact token counts:

**Rough estimate:**
- 1 token ≈ 0.75 words (or 1 word ≈ 1.3 tokens)
- Count words in your prompt × 1.3 = prompt_tokens
- Count words in Claude's response × 1.3 = completion_tokens

**For Claude.ai users:**
- Check the response metadata if available
- Use word count as approximation

**For API users:**
- Token counts are in the API response

### Counting Tool Calls

- Count each time Claude uses a tool (Read, Write, Edit, Bash, Grep, etc.)
- Each tool use = 1 tool call
- Multiple tools in one response = sum them all

### Counting Round Trips

- 1 round trip = you send message → Claude responds
- If you had to clarify or answer questions = additional round trips
- Initial response = 1, each follow-up = +1

## Understanding Results

### Success Criteria

The skill is effective if:
- ✅ Token reduction > 30%
- ✅ Energy reduction > 30%
- ✅ Quality maintained > 90% of baseline
- ✅ Satisfaction maintained > 90% of baseline

### Expected Results (Based on Design)

The theoretical analysis predicts:
- 40-60% token reduction
- 40-60% energy reduction
- Quality maintained at 95%+
- Satisfaction maintained or improved

**But these are predictions!** Your empirical results may differ.

## Troubleshooting

### "I don't know how to count tokens"

Use word count × 1.3 as approximation. Exact precision isn't critical - we're looking for directional trends.

### "The skill doesn't seem to activate"

Make sure:
- You're using scenarios marked `"should_trigger": true`
- The skill is properly installed
- You're using a task complex enough to trigger it (5+ steps)

### "My results differ from theoretical predictions"

That's fine! Real-world results often differ from theoretical predictions. Document what you found - this is valuable data.

### "I only have time to test a few scenarios"

Test at least 5 scenarios that should trigger the skill. More is better, but 5 gives a reasonable sample.

## Files Explained

| File | Type | Purpose |
|------|------|---------|
| `README.md` | Guide | You're reading it |
| `RUN_TESTS.md` | Guide | Detailed step-by-step testing procedure |
| `test_scenarios.json` | Data | 10 test scenarios with expected results |
| `test_results_template.json` | Template | Copy this to record your results |
| `energy_assessment.py` | Tool | Analyzes and compares test results |
| `THEORETICAL_*.md` | Analysis | Predictions (NOT empirical data) |
| `THEORETICAL_*.json` | Example | Sample data format (NOT real results) |

## Questions?

- Check `RUN_TESTS.md` for detailed procedures
- Review `test_scenarios.json` for scenario details
- See `THEORETICAL_ANALYSIS.md` for methodology (but remember it's theoretical)
- Open an issue on GitHub if you need help

## Contributing Your Results

If you run empirical tests, we'd love to see your findings! Please:
1. Run at least 5 scenarios
2. Generate your report using `energy_assessment.py`
3. Open a GitHub issue titled "Empirical Test Results - [Your Name]"
4. Share your methodology and findings

Real-world data helps everyone understand actual effectiveness!

---

**Remember:** The theoretical predictions are educated guesses. Your empirical results are the real validation. Please test and share your findings!
