# Automated Testing Framework - Quick Reference

## What Is This?

An automated, transparent testing system that uses the Claude API to empirically test the resource-minimizer skill by running the same scenarios through two separate "agents" - one with the skill, one without.

## Key Innovation

**Before:** Manual testing required ~40 minutes per 5 scenarios, manual token counting, and could introduce human bias.

**Now:** Fully automated testing runs 5 scenarios in ~5 minutes, extracts actual token counts from API, and provides complete transparency logs.

## How It Works

```
1. Load test scenarios from test_scenarios.json
2. Spawn "baseline agent" (API calls without skill in system prompt)
3. Spawn "optimized agent" (API calls with skill in system prompt)
4. Run identical scenarios through both
5. Capture full request/response logs
6. Extract metrics from API responses (actual token counts)
7. Generate comparison report using energy_assessment.py
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Run demo (2 scenarios)
./demo_automated_testing.sh

# 4. Run quick test (5 scenarios)
python3 automated_test_runner.py --quick

# 5. View results
cat automated_test_runs/run_*/comparison_report.txt
```

## What Gets Generated

For each test run:

```
automated_test_runs/run_TIMESTAMP/
├── baseline_results.json          # Metrics for baseline
├── optimized_results.json         # Metrics for optimized
├── comparison_report.txt          # Human-readable comparison
├── logs/                          # FULL TRANSPARENCY
│   ├── baseline_scenario_001_request.json
│   ├── baseline_scenario_001_response.json
│   ├── optimized_scenario_001_request.json
│   ├── optimized_scenario_001_response.json
│   └── complete_session_*.json
└── *_transcript.txt files         # Readable conversation logs
```

## Transparency & Verification

### Verify the skill was included in optimized agent:
```bash
cat automated_test_runs/run_*/logs/optimized_*_request.json | grep "resource-minimizer"
```

### Verify the skill was NOT in baseline agent:
```bash
cat automated_test_runs/run_*/logs/baseline_*_request.json | grep "resource-minimizer" || echo "✓ Clean baseline"
```

### Check actual token counts from API:
```bash
cat automated_test_runs/run_*/logs/baseline_scenario_003_response.json | jq '.response.usage'
cat automated_test_runs/run_*/logs/optimized_scenario_003_response.json | jq '.response.usage'
```

### Read what agents actually said:
```bash
cat automated_test_runs/run_*/baseline_scenario_003_transcript.txt
cat automated_test_runs/run_*/optimized_scenario_003_transcript.txt
```

## Files Created

| File | Purpose |
|------|---------|
| `automated_test_runner.py` | Main orchestrator - runs tests, logs everything |
| `requirements.txt` | Python dependencies (anthropic SDK) |
| `demo_automated_testing.sh` | Demo script to showcase the system |
| `AUTOMATED_TESTING_GUIDE.md` | Comprehensive documentation |
| `AUTOMATED_TESTING_README.md` | This quick reference |

## Architecture

```
┌──────────────────────────────────────┐
│   automated_test_runner.py          │
│   ┌──────────────────────────────┐  │
│   │ TransparentLogger            │  │  Logs every request/response
│   │ - log_request()              │  │
│   │ - log_response()             │  │
│   └──────────────────────────────┘  │
│   ┌──────────────────────────────┐  │
│   │ MetricsExtractor             │  │  Extracts metrics from API
│   │ - get_actual_tokens()        │  │
│   │ - count_tool_calls()         │  │
│   └──────────────────────────────┘  │
│   ┌──────────────────────────────┐  │
│   │ SkillTester                  │  │  Main orchestrator
│   │ - run_scenario()             │  │
│   │ - run_test_suite()           │  │
│   │ - create_system_prompt()     │  │
│   └──────────────────────────────┘  │
└──────────────────────────────────────┘
           │
           ├─────> Anthropic API (baseline calls)
           └─────> Anthropic API (optimized calls)
```

## Key Features

### 1. True Isolation
- Separate API sessions for baseline vs optimized
- Different system prompts
- No cross-contamination

### 2. Actual Metrics
- Token counts from API `usage` field
- Not estimates (word count × 1.3)
- Accurate tool call counting
- Real execution timing

### 3. Full Transparency
- Every request logged to JSON
- Every response logged to JSON
- Human-readable transcripts
- Complete session audit trail

### 4. Reproducibility
- Same scenarios, same order
- Deterministic process
- Results can be replicated
- Version controlled

### 5. Automation
- No manual intervention
- Batch processing
- Automatic report generation
- Error handling built-in

## Usage Examples

### Quick test (recommended first):
```bash
python3 automated_test_runner.py --quick
```
Runs scenarios: 1, 3, 4, 5, 8 (~5-10 minutes)

### Specific scenarios:
```bash
python3 automated_test_runner.py --scenarios 1,3,8
```

### All scenarios:
```bash
python3 automated_test_runner.py --all
```
Runs all "should_trigger" scenarios (~20-30 minutes)

### Custom model:
```bash
python3 automated_test_runner.py --quick --model claude-opus-4-6
```

## Understanding Results

### Example Report Output:

```
================================================================================
SAVINGS ANALYSIS
================================================================================
Token Reduction: 58.0%          ← Should be >30%
Energy Reduction: 58.0%         ← Should be >30%
Cost Reduction: 58.0%           ← Direct cost impact
CO2 Reduction: 58.0%            ← Environmental impact
Tool Call Reduction: 50.0%      ← Fewer operations
Round Trip Reduction: 33.0%     ← Less context loading

================================================================================
QUALITY ASSESSMENT
================================================================================
Quality Maintained (>90%): ✓ YES        ← Quality threshold
Satisfaction Maintained (>90%): ✓ YES   ← User satisfaction
Quality: 4.50 → 4.50                    ← No degradation
Satisfaction: 4.50 → 4.50               ← Maintained or improved

================================================================================
CONCLUSION
================================================================================
Effective: ✓ YES                        ← Meets effectiveness criteria
Meets All Targets: ✓ YES                ← Passes all thresholds
Recommendation: APPROVED                 ← Ready for use
```

## Advantages Over Manual Testing

| Aspect | Manual | Automated |
|--------|--------|-----------|
| Time (5 scenarios) | 40 min | 5 min |
| Token accuracy | Estimate (±20%) | Actual (<1%) |
| Tool call counting | Manual observation | API extraction |
| Transparency | Notes only | Full logs |
| Reproducibility | Difficult | Perfect |
| Human bias | Possible | Eliminated |
| Scale | Hard >10 | Easy 100+ |

## Verification Checklist

After running automated tests:

- [ ] Review comparison_report.txt
- [ ] Spot-check 2-3 transcripts
- [ ] Verify skill in optimized request logs
- [ ] Verify no skill in baseline request logs
- [ ] Compare token counts between baseline/optimized
- [ ] Check quality scores are acceptable
- [ ] Review any error logs
- [ ] Archive successful runs

## Common Issues

### API Key Not Set
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Rate Limiting
Script includes 1-second delays. If still hitting limits:
- Run fewer scenarios
- Wait between runs
- Request limit increase

### Dependencies Missing
```bash
pip install -r requirements.txt
```

## Extending the Framework

Want to test a different skill?

1. Modify `create_system_prompt()` in `automated_test_runner.py`
2. Point to different skill file:
   ```python
   skill_file = Path("path/to/other-skill/SKILL.md")
   ```

Want custom scenarios?

1. Edit `test_scenarios.json`
2. Add new scenario with:
   - id: "scenario_011"
   - name: "Descriptive name"
   - test_prompt: "Your test prompt"
   - should_trigger: true/false

Want different quality metrics?

1. Edit `_assess_quality()` in `automated_test_runner.py`
2. Add domain-specific checks
3. Implement custom scoring logic

## Cost Estimate

Approximate API costs:

- Demo (2 scenarios): ~$0.05-0.10
- Quick test (5 scenarios): ~$0.10-0.30
- Full test (10 scenarios): ~$0.30-0.60

Actual cost depends on:
- Scenario complexity
- Response length
- Model used (Sonnet vs Opus)

## Next Steps

1. **Run the demo**: `./demo_automated_testing.sh`
2. **Review the guide**: `cat AUTOMATED_TESTING_GUIDE.md`
3. **Run quick test**: `python3 automated_test_runner.py --quick`
4. **Verify results**: Check logs and transcripts
5. **Share findings**: Document and publish results

## Support

**Documentation:**
- `AUTOMATED_TESTING_GUIDE.md` - Comprehensive guide
- `START_HERE.md` - Overview of testing options
- `RUN_TESTS.md` - Manual testing (reference)

**Debugging:**
- Check `automated_test_runs/run_*/logs/` for details
- Review error messages in console output
- Verify API key is set correctly

**Contributing:**
- Report issues with logs attached
- Share successful test results
- Suggest improvements to framework

---

**The automated framework provides scientific rigor with full transparency.**

No more manual work. No more estimation. Just run, verify, and report.
