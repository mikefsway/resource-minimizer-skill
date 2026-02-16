# Quick Reference - Testing Checklist

## Files at a Glance

| File | Type | Use It For |
|------|------|------------|
| `START_HERE.md` | Guide | First-time orientation |
| `RUN_TESTS.md` | Guide | Detailed step-by-step instructions |
| `QUICK_REFERENCE.md` | Cheat Sheet | This file - quick lookups |
| `README.md` | Overview | Context and FAQ |
| `test_scenarios.json` | Data | Copy test prompts from here |
| `test_results_template.json` | Template | Copy to record your results |
| `energy_assessment.py` | Tool | Run to analyze results |
| `THEORETICAL_*.md` | Analysis | Predictions (NOT real data) |
| `THEORETICAL_*.json` | Example | Format examples (NOT real data) |

## Testing Workflow

```
Setup (5 min)
  → Install skill
  → Copy template to my_baseline_results.json
  → Copy template to my_optimized_results.json

Baseline Tests (15 min)
  → Disable skill
  → Run 5 scenarios
  → Record metrics in my_baseline_results.json

Optimized Tests (15 min)
  → Enable skill
  → Run SAME 5 scenarios
  → Record metrics in my_optimized_results.json

Analysis (5 min)
  → python3 energy_assessment.py --compare my_baseline_results.json my_optimized_results.json
  → Review results
  → Done!
```

## Recording Metrics Cheat Sheet

### Token Counts
```
Prompt tokens = word count × 1.3
Claude response tokens = word count × 1.3
Total = prompt + response
```

### Tool Calls
```
Count each tool use:
- Read file: 1
- Edit file: 1
- Bash command: 1
- Grep search: 1
Total = sum of all
```

### Round Trips
```
You send → Claude responds: 1 round trip
Claude asks question → You answer → Claude responds: 2 round trips
Each exchange adds 1
```

### Quality Rating (1-5)
```
5 = Excellent, comprehensive, perfect
4 = Good, minor issues
3 = Adequate, acceptable
2 = Poor, significant problems
1 = Unusable
```

### Satisfaction Rating (1-5)
```
5 = Very satisfied, exactly what I needed
4 = Satisfied, mostly what I needed
3 = Neutral
2 = Unsatisfied
1 = Very unsatisfied
```

## Test Scenarios Quick Pick

### Must Test (High Trigger Probability)
- `scenario_001`: Multi-Step Code Refactoring
- `scenario_003`: Research Task
- `scenario_004`: Long Document Generation
- `scenario_005`: Ambiguous Database Setup
- `scenario_008`: Complex Data Pipeline

### Validation Tests (Should NOT Trigger)
- `scenario_002`: Simple Factual Question
- `scenario_007`: Quick Clarification
- `scenario_010`: Casual Greeting

### Optional Deep Tests
- `scenario_006`: Iterative Code Debugging
- `scenario_009`: Exploratory Architecture Discussion

## Command Quick Reference

### Setup
```bash
# Install skill (macOS/Linux)
cp -r ../resource-minimizer ~/.config/claude-code/skills/

# Create result files
cp test_results_template.json my_baseline_results.json
cp test_results_template.json my_optimized_results.json
```

### Edit Your Files
```bash
# Edit baseline header
# Set: "skill_enabled": false

# Edit optimized header
# Set: "skill_enabled": true
```

### Run Analysis
```bash
# Text report to screen
python3 energy_assessment.py --compare my_baseline_results.json my_optimized_results.json

# Save to file
python3 energy_assessment.py --compare my_baseline_results.json my_optimized_results.json > my_report.txt

# JSON format
python3 energy_assessment.py --compare my_baseline_results.json my_optimized_results.json --format json --output my_report.json
```

## JSON Template Quick Copy

```json
{
  "scenario_id": "scenario_XXX",
  "scenario_name": "Name from test_scenarios.json",
  "prompt_tokens": 0,
  "completion_tokens": 0,
  "total_tokens": 0,
  "tool_calls": 0,
  "round_trips": 1,
  "execution_time_ms": 0,
  "quality_score": 0.0,
  "user_satisfaction": 0.0,
  "notes": "Your observations"
}
```

## Success Criteria

Your test shows skill is effective if:
- ✅ Token reduction > 30%
- ✅ Quality maintained > 90% (quality score ≥ 90% of baseline)
- ✅ Satisfaction maintained ≥ 90% of baseline
- ✅ Behavioral differences observed

## Common Calculations

### Token Reduction %
```
((baseline_tokens - optimized_tokens) / baseline_tokens) × 100
Example: ((4000 - 2000) / 4000) × 100 = 50%
```

### Quality Maintained?
```
(optimized_quality / baseline_quality) × 100 ≥ 90%
Example: (4.5 / 5.0) × 100 = 90% ✓
```

### Expected Ranges (Theoretical)
```
Token reduction: 40-60%
Quality: 95-100% maintained
Satisfaction: 100-110% (might improve!)
Tool calls: 40-60% fewer
Round trips: 40-60% fewer
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Can't count tokens exactly | Use word count × 1.3 |
| Skill doesn't activate | Verify installation, use complex scenario |
| Results seem identical | Check skill is actually enabled |
| Don't have Python | Install Python 3.7+ or calculate manually |
| Prompts different | Copy exact prompt from test_scenarios.json |
| Forgot to record something | Estimate best you can, note in "notes" field |

## Time Estimates

| Task | Time |
|------|------|
| Read START_HERE.md | 5 min |
| Read RUN_TESTS.md | 10 min |
| Install skill | 2 min |
| Setup files | 3 min |
| Run 1 scenario | 5 min |
| Run 5 scenarios baseline | 15 min |
| Run 5 scenarios optimized | 15 min |
| Run analysis | 2 min |
| Review results | 5 min |
| **Total (5 scenarios)** | **~40 min** |
| **Total (10 scenarios)** | **~70 min** |

## Quick Example

**Baseline Test:**
```
Prompt: "What are best practices for REST API security?" (10 words)
Response: 1200 words of comprehensive explanation
Tokens: 13 prompt + 1560 response = 1573 total
Tools: 2
Round trips: 1
Quality: 5/5
Satisfaction: 4/5
```

**Optimized Test (same prompt):**
```
Response: 380 words, concise with expansion offer
Tokens: 13 prompt + 494 response = 507 total
Tools: 1
Round trips: 1
Quality: 4.5/5
Satisfaction: 5/5
```

**Result:**
```
Token reduction: (1573 - 507) / 1573 = 67.8% ✅
Quality: 4.5/5.0 = 90% ✅
Satisfaction: 5/4 = 125% ✅
EFFECTIVE!
```

## Need More Detail?

- **Setup questions:** → `START_HERE.md`
- **Step-by-step process:** → `RUN_TESTS.md`
- **Scenario details:** → `test_scenarios.json`
- **General info:** → `README.md`
- **Can't find answer:** → GitHub Issues

---

**Tip:** Print this page as a reference while testing!
