#!/usr/bin/env python3
"""
Claude Code Native Test Runner

Runs automated tests entirely within Claude Code using agent spawning.
No API key needed - uses Claude Code's Task tool to spawn baseline and optimized agents.

Usage:
    python3 claude_code_test_runner.py --quick
    python3 claude_code_test_runner.py --scenarios 1,3,5
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import tempfile
import re


class ClaudeCodeTester:
    """Orchestrates testing using Claude Code agents"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skill_file = repo_root / "resource-minimizer" / "SKILL.md"
        self.scenarios_file = repo_root / "testing" / "test_scenarios.json"

    def load_skill_instructions(self) -> str:
        """Load skill instructions from repo"""
        with open(self.skill_file, 'r') as f:
            content = f.read()
            # Extract content after frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
            return content

    def load_scenarios(self) -> List[Dict]:
        """Load test scenarios"""
        with open(self.scenarios_file, 'r') as f:
            data = json.load(f)
        return data['scenarios']

    def create_agent_prompt(self, scenario: Dict, use_skill: bool) -> str:
        """Create prompt for agent"""

        scenario_prompt = scenario['test_prompt']

        if use_skill:
            skill_instructions = self.load_skill_instructions()
            return f"""You have the resource-minimizer skill enabled. Follow these instructions carefully:

{skill_instructions}

IMPORTANT: Apply these resource-minimizer principles to the following task.

USER REQUEST:
{scenario_prompt}"""
        else:
            return f"""You are Claude, a helpful AI assistant. Help with the following request:

USER REQUEST:
{scenario_prompt}"""

    def run_agent_task(self, prompt: str, test_type: str, scenario_id: str) -> Dict:
        """
        Run a task using Claude Code agent spawning.

        This creates a temporary file with instructions for spawning an agent,
        then uses the Claude Code CLI to execute it.
        """

        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            temp_file = f.name

        try:
            # Use echo to pipe the prompt to claude-code
            # This simulates spawning an agent and getting its response
            result = subprocess.run(
                ['claude-code', '--session', f'test_{test_type}_{scenario_id}'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout
            error = result.stderr

            if result.returncode != 0:
                print(f"Warning: Agent returned non-zero exit code: {result.returncode}")
                print(f"Error: {error}")

            return {
                'output': output,
                'error': error,
                'returncode': result.returncode,
                'timestamp': datetime.now().isoformat()
            }

        except subprocess.TimeoutExpired:
            print(f"Timeout running {test_type} agent for {scenario_id}")
            return {
                'output': '',
                'error': 'Timeout',
                'returncode': -1,
                'timestamp': datetime.now().isoformat()
            }
        except FileNotFoundError:
            print("Error: claude-code CLI not found. Using fallback method.")
            # Fallback: just note that we can't spawn separate processes
            return {
                'output': f"[Simulated {test_type} response - CLI not available]",
                'error': 'CLI not available',
                'returncode': -1,
                'timestamp': datetime.now().isoformat()
            }
        finally:
            # Cleanup
            try:
                os.unlink(temp_file)
            except:
                pass

    def extract_metrics(self, output: str, scenario: Dict) -> Dict:
        """Extract metrics from agent output"""

        # Count words (approximate tokens)
        word_count = len(output.split())
        estimated_tokens = int(word_count * 1.3)

        # Count tool uses (look for tool patterns in output)
        tool_patterns = [
            r'\[Tool: Read\]',
            r'\[Tool: Write\]',
            r'\[Tool: Edit\]',
            r'\[Tool: Bash\]',
            r'\[Tool: Grep\]',
            r'\[Tool: Glob\]',
        ]
        tool_calls = sum(len(re.findall(pattern, output, re.IGNORECASE)) for pattern in tool_patterns)

        # Assess quality (heuristic)
        quality = 4.0
        if word_count < 50:
            quality = 3.0
        elif word_count > 200:
            quality = 4.5

        return {
            'completion_tokens': estimated_tokens,
            'tool_calls': tool_calls,
            'word_count': word_count,
            'quality_score': quality,
            'character_count': len(output)
        }

    def run_scenario_comparison(self, scenario: Dict) -> Dict:
        """Run a single scenario through both baseline and optimized agents"""

        scenario_id = scenario['id']
        scenario_name = scenario['name']

        print(f"\n{'='*80}")
        print(f"Testing: {scenario_id} - {scenario_name}")
        print(f"{'='*80}")

        # Baseline agent
        print(f"\n[1/2] Running BASELINE agent (no skill)...")
        baseline_prompt = self.create_agent_prompt(scenario, use_skill=False)
        baseline_result = self.run_agent_task(baseline_prompt, 'baseline', scenario_id)
        baseline_metrics = self.extract_metrics(baseline_result['output'], scenario)

        print(f"  ✓ Baseline: ~{baseline_metrics['completion_tokens']} tokens, "
              f"{baseline_metrics['tool_calls']} tools")

        # Small delay
        time.sleep(1)

        # Optimized agent
        print(f"\n[2/2] Running OPTIMIZED agent (with skill)...")
        optimized_prompt = self.create_agent_prompt(scenario, use_skill=True)
        optimized_result = self.run_agent_task(optimized_prompt, 'optimized', scenario_id)
        optimized_metrics = self.extract_metrics(optimized_result['output'], scenario)

        print(f"  ✓ Optimized: ~{optimized_metrics['completion_tokens']} tokens, "
              f"{optimized_metrics['tool_calls']} tools")

        # Calculate reduction
        token_reduction = ((baseline_metrics['completion_tokens'] -
                           optimized_metrics['completion_tokens']) /
                          baseline_metrics['completion_tokens'] * 100)

        print(f"\n  📊 Token reduction: {token_reduction:.1f}%")

        return {
            'scenario_id': scenario_id,
            'scenario_name': scenario_name,
            'baseline': {
                'output': baseline_result['output'],
                'metrics': baseline_metrics,
                'prompt': baseline_prompt
            },
            'optimized': {
                'output': optimized_result['output'],
                'metrics': optimized_metrics,
                'prompt': optimized_prompt
            },
            'comparison': {
                'token_reduction_pct': token_reduction,
                'baseline_tokens': baseline_metrics['completion_tokens'],
                'optimized_tokens': optimized_metrics['completion_tokens']
            }
        }

    def save_results(self, results: List[Dict], output_dir: Path):
        """Save test results"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save individual scenario results
        for result in results:
            scenario_id = result['scenario_id']

            # Save baseline transcript
            baseline_file = output_dir / f"baseline_{scenario_id}_transcript.txt"
            with open(baseline_file, 'w') as f:
                f.write(f"{'='*80}\n")
                f.write(f"BASELINE TEST: {result['scenario_name']}\n")
                f.write(f"{'='*80}\n\n")
                f.write("PROMPT:\n")
                f.write(f"{'-'*80}\n")
                f.write(result['baseline']['prompt'])
                f.write(f"\n{'-'*80}\n\n")
                f.write("RESPONSE:\n")
                f.write(f"{'-'*80}\n")
                f.write(result['baseline']['output'])
                f.write(f"\n{'-'*80}\n\n")
                f.write("METRICS:\n")
                f.write(json.dumps(result['baseline']['metrics'], indent=2))
                f.write("\n")

            # Save optimized transcript
            optimized_file = output_dir / f"optimized_{scenario_id}_transcript.txt"
            with open(optimized_file, 'w') as f:
                f.write(f"{'='*80}\n")
                f.write(f"OPTIMIZED TEST: {result['scenario_name']}\n")
                f.write(f"{'='*80}\n\n")
                f.write("PROMPT:\n")
                f.write(f"{'-'*80}\n")
                f.write(result['optimized']['prompt'])
                f.write(f"\n{'-'*80}\n\n")
                f.write("RESPONSE:\n")
                f.write(f"{'-'*80}\n")
                f.write(result['optimized']['output'])
                f.write(f"\n{'-'*80}\n\n")
                f.write("METRICS:\n")
                f.write(json.dumps(result['optimized']['metrics'], indent=2))
                f.write("\n")

        # Save summary
        summary_file = output_dir / "test_summary.json"
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'num_scenarios': len(results),
                'results': results
            }, f, indent=2)

        print(f"\n✓ Results saved to: {output_dir}")

    def generate_report(self, results: List[Dict]) -> str:
        """Generate comparison report"""

        total_baseline_tokens = sum(r['baseline']['metrics']['completion_tokens']
                                    for r in results)
        total_optimized_tokens = sum(r['optimized']['metrics']['completion_tokens']
                                     for r in results)

        avg_reduction = ((total_baseline_tokens - total_optimized_tokens) /
                        total_baseline_tokens * 100)

        report_lines = [
            "="*80,
            "CLAUDE CODE NATIVE TEST RESULTS",
            "="*80,
            "",
            f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios Tested: {len(results)}",
            "",
            "-"*80,
            "AGGREGATE RESULTS",
            "-"*80,
            f"Baseline Total Tokens: {total_baseline_tokens:,}",
            f"Optimized Total Tokens: {total_optimized_tokens:,}",
            f"Token Reduction: {avg_reduction:.1f}%",
            "",
            "-"*80,
            "INDIVIDUAL SCENARIOS",
            "-"*80,
        ]

        for result in results:
            report_lines.extend([
                "",
                f"Scenario: {result['scenario_name']}",
                f"  Baseline:  {result['baseline']['metrics']['completion_tokens']:,} tokens, "
                f"{result['baseline']['metrics']['tool_calls']} tool calls",
                f"  Optimized: {result['optimized']['metrics']['completion_tokens']:,} tokens, "
                f"{result['optimized']['metrics']['tool_calls']} tool calls",
                f"  Reduction: {result['comparison']['token_reduction_pct']:.1f}%"
            ])

        report_lines.extend([
            "",
            "="*80,
            "CONCLUSION",
            "="*80,
        ])

        if avg_reduction > 30:
            report_lines.append(f"✓ SUCCESS: {avg_reduction:.1f}% token reduction exceeds 30% target")
        else:
            report_lines.append(f"⚠ BELOW TARGET: {avg_reduction:.1f}% reduction (target: >30%)")

        report_lines.append("="*80)

        return "\n".join(report_lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Claude Code native test runner for resource-minimizer skill"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick test (scenarios 1,3,4,5,8)"
    )
    parser.add_argument(
        "--scenarios",
        help="Comma-separated scenario numbers (e.g., 1,3,5)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios that should trigger"
    )

    args = parser.parse_args()

    # Setup
    repo_root = Path(__file__).parent.parent
    tester = ClaudeCodeTester(repo_root)

    # Load scenarios
    all_scenarios = tester.load_scenarios()

    # Select scenarios
    if args.quick:
        scenario_ids = ['scenario_001', 'scenario_003', 'scenario_004',
                       'scenario_005', 'scenario_008']
        selected = [s for s in all_scenarios if s['id'] in scenario_ids]
    elif args.scenarios:
        scenario_ids = [f"scenario_{int(x):03d}" for x in args.scenarios.split(',')]
        selected = [s for s in all_scenarios if s['id'] in scenario_ids]
    elif args.all:
        selected = [s for s in all_scenarios if s.get('should_trigger', True)]
    else:
        print("Error: Specify --quick, --scenarios, or --all")
        return

    print(f"\n{'#'*80}")
    print(f"# CLAUDE CODE NATIVE TEST RUNNER")
    print(f"# Testing {len(selected)} scenarios")
    print(f"{'#'*80}\n")

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = repo_root / "testing" / "claude_code_runs" / f"run_{timestamp}"

    # Run tests
    results = []
    for i, scenario in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}]", end=" ")
        try:
            result = tester.run_scenario_comparison(scenario)
            results.append(result)
        except Exception as e:
            print(f"Error: {e}")
            continue

    # Save results
    tester.save_results(results, output_dir)

    # Generate report
    report = tester.generate_report(results)
    print(f"\n\n{report}")

    # Save report
    report_file = output_dir / "comparison_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n✓ Full report saved to: {report_file}")
    print(f"\n✓ All transcripts available in: {output_dir}")


if __name__ == "__main__":
    main()
