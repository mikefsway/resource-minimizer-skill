# Test Results Directory

This directory contains automated test run results for the resource-minimizer skill.

## Latest Test Run

**Location:** `run_20260216_213931/`
**Date:** 2026-02-16 21:39 UTC
**Summary:** Current version achieves 42.4% token reduction with 83.6% tool call reduction

### Quick Links

- **Detailed Results:** [test_results_2026-02-16.md](run_20260216_213931/test_results_2026-02-16.md)
- **Quick Summary:** [COMPARISON_SUMMARY.txt](run_20260216_213931/COMPARISON_SUMMARY.txt)
- **Previous Results:** [../empirical_test_results.md](../empirical_test_results.md)

## Test Results Summary

| Run Date | Token Reduction | Tool Reduction | Status |
|----------|----------------|----------------|--------|
| 2026-02-16 21:39 | 42.4% | 83.6% | ✓ PASS |
| 2026-02-16 (earlier) | 41.4% | 75.0% | ✓ PASS |

## Directory Structure

```
test_results/
├── README.md                           # This file
└── run_20260216_213931/               # Latest test run
    ├── test_results_2026-02-16.md     # Detailed results & comparison
    └── COMPARISON_SUMMARY.txt         # Quick comparison summary
```

## How to Read Results

1. **Quick Check:** Read `COMPARISON_SUMMARY.txt` for a high-level overview
2. **Detailed Analysis:** Read the full `test_results_*.md` for scenario-by-scenario breakdown
3. **Historical Context:** Compare with `../empirical_test_results.md` for earlier results

## Success Criteria

All test runs must meet these criteria:

- ✓ Token Reduction (triggered scenarios): >30%
- ✓ Quality Maintenance: >90%
- ✓ Trigger Accuracy: >85%
- ✓ Tool Call Reduction: Measured for insight

## Test Scenarios

The automated tests run 5 scenarios:

1. **Scenario 1:** Multi-Step Code Refactoring (should trigger)
2. **Scenario 2:** Simple Factual Question (should NOT trigger - control)
3. **Scenario 3:** Research Task - Security Practices (should trigger)
4. **Scenario 5:** Ambiguous Database Setup (should trigger)
5. **Scenario 8:** Complex Data Analysis Pipeline (should trigger)

## Testing Method

Tests use Claude Code native testing with Task-based agents:
- Baseline agents run without the skill
- Optimized agents run with the skill enabled
- Metrics are extracted from actual API usage data
- Results are compared for token/tool efficiency and quality

For more information on testing methodology, see:
- [../CLAUDE_CODE_NATIVE_TESTING.md](../CLAUDE_CODE_NATIVE_TESTING.md)
- [../AUTOMATED_TESTING_GUIDE.md](../AUTOMATED_TESTING_GUIDE.md)
