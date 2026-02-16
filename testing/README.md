# Resource Minimizer Testing

This folder contains automated tools to test the effectiveness of the resource-minimizer skill.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your API Key
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run Tests
```bash
# Quick test (5 scenarios, ~5 minutes)
python3 automated_test_runner.py --quick

# Try the demo first (2 scenarios)
./demo_automated_testing.sh

# Run all scenarios
python3 automated_test_runner.py --all

# Run specific scenarios
python3 automated_test_runner.py --scenarios 1,3,5
```

### 4. View Results
```bash
cat automated_test_runs/run_*/comparison_report.txt
```

## What Gets Tested

The automated testing framework:
- Runs test scenarios through two separate agents (baseline without skill, optimized with skill)
- Captures actual token counts from the Anthropic API
- Measures tool usage, quality, and efficiency
- Generates comparison reports automatically

## Test Results

See `empirical_test_results.md` for actual test results showing **41.4% token reduction** across complex scenarios.

## Files Overview

| File | Purpose |
|------|---------|
| `automated_test_runner.py` | Main automated testing script |
| `demo_automated_testing.sh` | Quick demo (try this first) |
| `test_scenarios.json` | Test scenarios used by the runner |
| `energy_assessment.py` | Analysis tool (auto-run by test runner) |
| `requirements.txt` | Python dependencies |
| `test_results_template.json` | Template for manual testing (optional) |
| `empirical_test_results.md` | Actual test results |
| `AUTOMATED_TESTING_GUIDE.md` | Detailed guide for automated testing |
| `CLAUDE_CODE_NATIVE_TESTING.md` | Alternative: test within Claude Code sessions |
| `claude_code_test_runner.py` | Claude Code native test runner |

## How It Works

```
1. Load test scenarios from test_scenarios.json
2. Create baseline agent (API calls without skill)
3. Create optimized agent (API calls with skill)
4. Run same scenarios through both agents
5. Extract metrics from API responses (actual token counts)
6. Generate comparison report
7. Save full logs for transparency
```

## Output

After running tests, you'll get:

```
automated_test_runs/run_TIMESTAMP/
├── baseline_results.json         # Baseline metrics
├── optimized_results.json        # Optimized metrics
├── comparison_report.txt         # Human-readable report
├── logs/                         # Full API request/response logs
└── transcripts/                  # Readable conversation logs
```

## Success Criteria

The skill is effective if tests show:
- ✅ Token reduction > 30%
- ✅ Quality maintained > 90% of baseline
- ✅ User satisfaction maintained or improved

## Alternative: Claude Code Native Testing

You can also test directly within a Claude Code session without needing an API key. See `CLAUDE_CODE_NATIVE_TESTING.md` for details.

## Need More Details?

- **Automated testing setup and usage**: `AUTOMATED_TESTING_GUIDE.md`
- **Claude Code native testing**: `CLAUDE_CODE_NATIVE_TESTING.md`
- **Test scenarios**: Open `test_scenarios.json`
- **Actual results**: `empirical_test_results.md`

## Manual Testing (Optional)

If you prefer to test manually:
1. Copy `test_results_template.json` to create your results files
2. Run test scenarios manually with and without the skill
3. Record metrics using the template
4. Run `python3 energy_assessment.py --compare baseline.json optimized.json`

## Questions?

- Check `AUTOMATED_TESTING_GUIDE.md` for comprehensive documentation
- Review `test_scenarios.json` to understand what gets tested
- See `empirical_test_results.md` for example results
- Open a GitHub issue if you need help
