# Resource Minimizer Skill for Claude

A Claude skill that minimizes computational resources, token usage, and energy consumption while maintaining quality.

## What It Does

- Starts with minimal reasoning, escalates only when necessary
- Prefers "assume + offer correction" over expensive clarification round-trips
- Generates minimal sufficient output with targeted expansion offers
- Optimizes tool usage through batching and caching

## Installation

### Claude.ai
1. Download the latest release or clone this repo
2. Zip the `resource-minimizer` folder
3. Open Claude.ai → Settings → Capabilities → Skills
4. Upload the zipped skill

### Claude Code
1. Clone this repo: `git clone https://github.com/yourusername/resource-minimizer-skill.git`
2. Copy the skill to Claude Code's skills directory:
   - macOS/Linux: `~/.config/claude-code/skills/`
   - Windows: `%APPDATA%\claude-code\skills\`
3. Restart Claude Code if running

## When It Triggers

The skill activates automatically for:
- Multi-step workflows (5+ operations)
- Complex reasoning tasks
- Tool-heavy operations
- Long document generation
- Explicit efficiency requests

It does NOT trigger for simple questions, casual conversation, or quick lookups.

## Usage Example

**Without skill:**
User: "Help me analyze this data"
Claude: "What format is your data in? What kind of analysis?"
User: "CSV, looking for trends"
Claude: [Comprehensive analysis with everything]

**With skill:**
User: "Help me analyze this data"
Claude: "I'm assuming CSV with time-series data. [Shows key trends] I can detail statistical methods, visualize patterns, or explain outliers if helpful."

## Testing & Effectiveness

### Has This Been Tested?

**Structural & Design:** ✅ Yes - The skill has been validated for correct structure and sound design principles.

**Empirical Effectiveness:** ✅ Yes - Empirical testing was conducted using Claude Code native testing (Task-based agents) against 5 scenarios. See `testing/empirical_test_results.md` for full details.

### Empirical Results (tested 2026-02-16)

| Metric | Result |
|--------|--------|
| Average token reduction (triggered scenarios) | **41.4%** |
| Total token reduction across triggered scenarios | **51.6%** |
| Tool call reduction | **75.0%** |
| Quality maintenance | **~100%** |
| Trigger accuracy | **100%** |

Results across scenario complexity levels:
- **High-complexity tasks**: 29.5% – 74.1% token reduction
- **Medium-complexity tasks**: 9.1% – 16.9% token reduction
- **Simple queries (control)**: 2.3% (skill correctly did not activate)

### Run the Tests Yourself

The `testing/` folder contains an automated testing framework. See `testing/README.md` to get started.

```bash
cd testing
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
python3 automated_test_runner.py --quick
```

### Share Your Results

If you run tests, please share your findings by opening a GitHub issue with your results. Additional data points help validate effectiveness across different use cases.

## Project Structure

```
resource-minimizer-skill/
├── resource-minimizer/          # The actual skill
│   ├── SKILL.md                 # Core skill definition
│   └── references/              # Deep-dive documentation
│       ├── efficiency-principles.md
│       └── expansion-patterns.md
├── testing/                     # Testing framework
│   ├── README.md                # Start here
│   ├── empirical_test_results.md # Actual test results
│   ├── automated_test_runner.py # Main automated test script
│   ├── claude_code_test_runner.py # Claude Code native runner
│   ├── demo_automated_testing.sh  # Quick demo (try first)
│   ├── test_scenarios.json      # Test prompts
│   ├── energy_assessment.py     # Analysis tool
│   ├── requirements.txt         # Python dependencies
│   ├── AUTOMATED_TESTING_GUIDE.md
│   ├── CLAUDE_CODE_NATIVE_TESTING.md
│   └── test_results/            # Saved test run outputs
└── README.md                    # This file
```

## Contributing

Contributions welcome! Especially:
- Empirical test results from different use cases
- Additional test scenarios
- Improvements to efficiency patterns
- Bug reports

## License

MIT - see LICENSE file
