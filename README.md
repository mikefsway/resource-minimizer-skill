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

**Empirical Effectiveness:** ⚠️ **Not yet** - The skill includes theoretical predictions of ~50-60% energy reduction, but these have NOT been verified with actual empirical testing.

### Want to Test It Yourself?

We've created a comprehensive testing framework in the `testing/` folder:

**Start here:** `testing/START_HERE.md`

The testing folder includes:
- Step-by-step testing guide
- 10 test scenarios
- Energy assessment tool (Python)
- Results templates
- Analysis scripts

**Time required:** 30-60 minutes for meaningful results

### Predicted Effectiveness (Theoretical)

Based on design analysis, the skill should:
- Reduce token usage by 40-60%
- Reduce energy consumption by 40-60%
- Maintain quality above 90%
- Reduce API costs by 40-60%

**⚠️ These are predictions, not proven results.** Run the tests in `testing/` to verify!

### Share Your Results

If you run empirical tests, please share your findings:
1. Follow the guide in `testing/RUN_TESTS.md`
2. Generate your report
3. Open a GitHub issue with results
4. Help validate (or refute) the predictions!

## Project Structure

```
resource-minimizer-skill/
├── resource-minimizer/          # The actual skill
│   ├── SKILL.md                 # Core skill definition
│   └── references/              # Deep-dive documentation
│       ├── efficiency-principles.md
│       └── expansion-patterns.md
├── testing/                     # Testing framework
│   ├── START_HERE.md           # Begin testing here
│   ├── RUN_TESTS.md            # Detailed guide
│   ├── test_scenarios.json     # Test prompts
│   ├── energy_assessment.py    # Analysis tool
│   └── ...                     # Templates and examples
└── README.md                    # This file
```

## Contributing

Contributions welcome! Especially:
- Empirical test results
- Additional test scenarios
- Improvements to efficiency patterns
- Bug reports

## License

MIT - see LICENSE file