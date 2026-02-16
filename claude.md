# Resource Minimizer Skill

## Project Overview

This is a Claude skill that minimizes computational resources, token usage, and energy consumption while maintaining quality. The skill helps Claude operate efficiently by reducing unnecessary reasoning, optimizing tool usage, and generating minimal sufficient output.

## Repository Structure

```
resource-minimizer-skill/
├── resource-minimizer/           # Main skill directory
│   ├── SKILL.md                 # Skill definition and instructions
│   └── references/              # Reference documentation
│       ├── efficiency-principles.md
│       └── expansion-patterns.md
├── README.md                    # User-facing documentation
├── LICENSE                      # MIT License
└── .gitignore
```

## Key Files

- **resource-minimizer/SKILL.md**: The core skill definition file that Claude reads when the skill is invoked. Contains:
  - Skill metadata (name, description, version, author)
  - Core operating principles
  - When to apply/not apply the skill
  - Operating guidelines for resource minimization
  - Examples and troubleshooting

- **resource-minimizer/references/**: Supporting documentation referenced by SKILL.md
  - `efficiency-principles.md`: Detailed reasoning escalation criteria and optimization strategies
  - `expansion-patterns.md`: Patterns for when and how to offer expansions

- **README.md**: Installation and usage instructions for end users

## Core Principles

The skill operates on these principles:

1. **Start minimal, escalate only when necessary** - Begin with simplest approach
2. **Progressive commitment** - Answer core first, check satisfaction, offer expansion
3. **Token economy** - Favor conciseness, use precise language
4. **Tool discipline** - Batch operations, cache results, skip when reasoning suffices

## When This Skill Triggers

**Always apply for:**
- Multi-step workflows (5+ operations)
- Multiple tool calls or file operations
- Long document generation
- Iterative refinement processes
- Explicit efficiency requests

**Never apply for:**
- Simple questions (1-3 sentence answers)
- Casual conversation
- Quick clarifications
- Simple lookups

## Development Guidelines

### Editing the Skill

When modifying SKILL.md:
- Maintain the frontmatter YAML header (name, description, metadata)
- Keep principles concise and actionable
- Examples should be brief and illustrative
- Reference files go in the `references/` directory

### Testing the Skill

1. Zip the `resource-minimizer` folder
2. Upload to Claude.ai or install in Claude Code skills directory:
   - macOS/Linux: `~/.config/claude-code/skills/`
   - Windows: `%APPDATA%\claude-code\skills\`
3. Test with multi-step tasks to verify efficiency improvements

### Documentation Standards

- README.md is user-facing (installation, usage)
- SKILL.md is Claude-facing (behavior, guidelines)
- References are detailed technical documentation
- Keep examples practical and realistic

## Installation Paths

### Claude.ai
Upload zipped `resource-minimizer` folder via Settings → Capabilities → Skills

### Claude Code
Copy `resource-minimizer` folder to:
- macOS/Linux: `~/.config/claude-code/skills/`
- Windows: `%APPDATA%\claude-code\skills\`

## License

MIT License - See LICENSE file for details

## Version

Current version: 1.0.0
Author: Mike Fell
