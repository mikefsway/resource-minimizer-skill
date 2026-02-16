# Automated Testing Guide

## Overview

This automated testing framework eliminates manual testing by using the Claude API to run test scenarios through separate "agents" (API sessions) - one with the skill enabled, one without.

## What Makes This Automated & Transparent

### Automation
- **No manual prompt entry**: Scenarios run automatically
- **No manual counting**: Token counts extracted from API responses
- **No manual comparison**: Reports generated automatically
- **Batch execution**: Run 5-10 scenarios in one command

### Transparency
- **Full request logs**: Every API request saved to JSON
- **Full response logs**: Every API response saved to JSON
- **Complete transcripts**: Human-readable conversation logs
- **Actual metrics**: Real token counts from Anthropic API
- **Audit trail**: Timestamp and track everything

## How It Works

```
┌─────────────────────────────────────────────┐
│  automated_test_runner.py                   │
│  (Orchestrator)                             │
└───┬─────────────────────────────────────┬───┘
    │                                     │
    ▼                                     ▼
┌────────────────────┐          ┌────────────────────┐
│ Baseline Agent     │          │ Optimized Agent    │
│ (No skill)         │          │ (With skill)       │
│                    │          │                    │
│ System prompt:     │          │ System prompt:     │
│ Standard Claude    │          │ + Resource         │
│                    │          │   Minimizer        │
└────────────────────┘          └────────────────────┘
         │                               │
         │                               │
         ▼                               ▼
    [Same Test Scenarios]           [Same Test Scenarios]
         │                               │
         ▼                               ▼
┌────────────────────┐          ┌────────────────────┐
│ Capture & Log      │          │ Capture & Log      │
│ - Requests         │          │ - Requests         │
│ - Responses        │          │ - Responses        │
│ - Token counts     │          │ - Token counts     │
│ - Tool calls       │          │ - Tool calls       │
│ - Timing           │          │ - Timing           │
└────────────────────┘          └────────────────────┘
         │                               │
         └───────────┬───────────────────┘
                     ▼
         ┌────────────────────────┐
         │ Compare & Report       │
         │ (energy_assessment.py) │
         └────────────────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ Results & Proof        │
         │ - Comparison report    │
         │ - Full transcripts     │
         │ - All API logs         │
         └────────────────────────┘
```

## Setup (One-Time)

### 1. Install Dependencies

```bash
cd testing
pip install -r requirements.txt
```

### 2. Set API Key

You need an Anthropic API key to run the automated tests.

**Option A: Environment Variable**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Option B: .env File**
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3. Verify Setup

```bash
python3 automated_test_runner.py --help
```

## Running Tests

### Quick Test (Recommended First)

Run 5 key scenarios (~5-10 minutes):

```bash
python3 automated_test_runner.py --quick
```

This will:
1. Run scenarios 1, 3, 4, 5, 8 through baseline agent
2. Run same scenarios through optimized agent
3. Generate comparison report
4. Save all logs and transcripts

### Specific Scenarios

Run selected scenarios:

```bash
# Run scenarios 1, 3, and 8
python3 automated_test_runner.py --scenarios 1,3,8
```

### All Scenarios

Run all test scenarios that should trigger the skill (~20-30 minutes):

```bash
python3 automated_test_runner.py --all
```

## Output Structure

After running tests, you'll get a timestamped directory:

```
automated_test_runs/
└── run_20260216_143022/
    ├── baseline_results.json           # Baseline metrics
    ├── optimized_results.json          # Optimized metrics
    ├── comparison_report.txt           # Human-readable report
    ├── logs/                           # Full transparency
    │   ├── baseline_scenario_001_request.json
    │   ├── baseline_scenario_001_response.json
    │   ├── optimized_scenario_001_request.json
    │   ├── optimized_scenario_001_response.json
    │   └── complete_session_run_20260216_143022.json
    └── transcripts/
        ├── baseline_scenario_001_transcript.txt
        ├── optimized_scenario_001_transcript.txt
        └── ...
```

## Verifying Transparency

### 1. Check Request Logs

See exactly what was sent to each agent:

```bash
cat automated_test_runs/run_*/logs/baseline_scenario_001_request.json
cat automated_test_runs/run_*/logs/optimized_scenario_001_request.json
```

Compare the system prompts - baseline should NOT have skill instructions, optimized should.

### 2. Check Response Logs

See actual API responses with token counts:

```bash
cat automated_test_runs/run_*/logs/baseline_scenario_001_response.json | jq '.response.usage'
cat automated_test_runs/run_*/logs/optimized_scenario_001_response.json | jq '.response.usage'
```

### 3. Read Transcripts

Human-readable conversation logs:

```bash
cat automated_test_runs/run_*/baseline_scenario_001_transcript.txt
cat automated_test_runs/run_*/optimized_scenario_001_transcript.txt
```

### 4. Verify Complete Session

See everything that happened:

```bash
cat automated_test_runs/run_*/logs/complete_session_*.json
```

## Understanding Results

### Comparison Report

The report shows:

```
================================================================================
RESOURCE MINIMIZER SKILL - ENERGY ASSESSMENT REPORT
================================================================================

Test Date: 2026-02-16T14:30:45
Number of Tests: 5

--------------------------------------------------------------------------------
BASELINE METRICS
--------------------------------------------------------------------------------
Total Tokens: 12,450
Avg Tokens/Test: 2,490
Total Tool Calls: 15
Avg Tool Calls/Test: 3.0
...

--------------------------------------------------------------------------------
OPTIMIZED METRICS (With Resource Minimizer)
--------------------------------------------------------------------------------
Total Tokens: 5,230
Avg Tokens/Test: 1,046
Total Tool Calls: 7
Avg Tool Calls/Test: 1.4
...

================================================================================
SAVINGS ANALYSIS
================================================================================
Token Reduction: 58.0%
Energy Reduction: 58.0%
Cost Reduction: 58.0%
CO2 Reduction: 58.0%
...

================================================================================
CONCLUSION
================================================================================
Effective: ✓ YES
Meets All Targets: ✓ YES
Recommendation: APPROVED
================================================================================
```

### Key Metrics

- **Token Reduction**: Should be >30% for success
- **Quality Maintained**: Should be >90% of baseline
- **Tool Calls Reduced**: Fewer operations = less compute
- **Round Trips**: Fewer back-and-forth exchanges

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

Set your API key:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Rate Limiting

The script includes 1-second delays between scenarios. If you hit rate limits:
- Wait a few minutes
- Run fewer scenarios at once
- Contact Anthropic for rate limit increase

### No Difference Between Baseline and Optimized

Possible causes:
1. Skill instructions not loading correctly
2. Scenarios too simple (should_trigger: false)
3. Model not following skill instructions

Check logs to verify skill was included in system prompt:
```bash
grep -A 20 "resource-minimizer" automated_test_runs/run_*/logs/optimized_*_request.json
```

### Quality Scores Low

Current quality scoring is a simple heuristic. For production use, you'd want:
- Human evaluation
- More sophisticated automated metrics
- Domain-specific quality checks

## Advanced Usage

### Custom Model

Use a different Claude model:

```bash
python3 automated_test_runner.py --quick --model claude-opus-4-6
```

### Custom Output Directory

```bash
python3 automated_test_runner.py --quick --output-dir ./my_tests
```

### Running Specific Test Combinations

```bash
# Test only high-complexity scenarios
python3 automated_test_runner.py --scenarios 1,4,6,8

# Test only medium-complexity
python3 automated_test_runner.py --scenarios 3,5,9
```

## Comparison: Manual vs Automated

| Aspect | Manual Testing | Automated Testing |
|--------|---------------|-------------------|
| Time for 5 scenarios | ~40 minutes | ~5 minutes |
| Token counting | Manual estimation (word count × 1.3) | Actual API counts |
| Tool call counting | Manual observation | Automatic extraction |
| Reproducibility | Hard to replicate exactly | Perfectly reproducible |
| Transparency | Notes + memory | Full logs + transcripts |
| Bias | Possible human bias | Consistent automated |
| Scale | Hard to test >10 scenarios | Easy to test all scenarios |

## Best Practices

### 1. Start Small

Run `--quick` first to verify everything works.

### 2. Review Logs

Don't just trust the summary - spot check the transcripts to ensure quality.

### 3. Multiple Runs

Run tests multiple times to account for API variability:

```bash
# Run 1
python3 automated_test_runner.py --quick

# Wait a few minutes

# Run 2
python3 automated_test_runner.py --quick

# Compare results
```

### 4. Save Important Results

Archive test runs that demonstrate effectiveness:

```bash
cp -r automated_test_runs/run_20260216_143022 ./published_results/
```

### 5. Document Findings

Add notes to the comparison report about observed behaviors.

## Extending the Framework

### Custom Quality Assessment

Edit `_assess_quality()` in `automated_test_runner.py` to add:
- Keyword matching
- Structural analysis
- Domain-specific checks

### Additional Metrics

Edit `MetricsExtractor` to track:
- Response latency patterns
- Specific tool types used
- Response structure characteristics

### Multi-Round Scenarios

Current framework does single-round tests. To add multi-round:
1. Extend `run_scenario()` to support conversation continuations
2. Add follow-up prompts to test_scenarios.json
3. Track context accumulation

## FAQ

### Q: Does this really test the skill objectively?

**A:** Yes, because:
- Uses separate API sessions (true isolation)
- Same scenarios for both (controlled comparison)
- Actual token counts (not estimates)
- Full logs for verification

### Q: How accurate are the token counts?

**A:** Completely accurate - they come directly from Anthropic's API response in the `usage` field.

### Q: Can I see exactly what the agents said?

**A:** Yes! Check the transcript files:
```bash
cat automated_test_runs/run_*/baseline_scenario_001_transcript.txt
```

### Q: How do I know the skill was really enabled?

**A:** Check the request log for the optimized agent:
```bash
cat automated_test_runs/run_*/logs/optimized_scenario_001_request.json | jq '.prompt' | grep -A 10 "resource-minimizer"
```

### Q: Can this test other skills?

**A:** Yes! Modify `create_system_prompt()` to load different skill files.

### Q: How much does automated testing cost?

**A:** Rough estimate:
- 5 scenarios (quick test): ~$0.10-0.30
- 10 scenarios (full test): ~$0.30-0.60
- Depends on scenario complexity and response length

## Next Steps

1. **Run your first automated test**
   ```bash
   python3 automated_test_runner.py --quick
   ```

2. **Review the results**
   ```bash
   cat automated_test_runs/run_*/comparison_report.txt
   ```

3. **Verify transparency**
   ```bash
   ls -la automated_test_runs/run_*/logs/
   cat automated_test_runs/run_*/*_transcript.txt
   ```

4. **Share findings**
   - Archive successful test runs
   - Share reports in GitHub issues
   - Contribute to skill improvement

## Support

- **Issue with the script**: Check error messages, review logs
- **Unexpected results**: Review transcripts, compare request logs
- **Feature requests**: Open GitHub issue with use case

---

**The automated testing framework gives you:**
- ✅ Reproducible results
- ✅ Full transparency
- ✅ Actual token counts
- ✅ Batch testing capability
- ✅ Audit trail
- ✅ Scientific rigor

**No more manual counting. No more estimation. Just run, verify, and report.**
