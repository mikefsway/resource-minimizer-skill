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

## License

MIT - see LICENSE file