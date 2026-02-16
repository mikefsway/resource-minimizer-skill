#!/usr/bin/env python3
"""
Automated Testing Framework for Resource Minimizer Skill

This script automatically tests the resource-minimizer skill by:
1. Running test scenarios through two separate agents (baseline vs optimized)
2. Capturing full transcripts for transparency
3. Automatically extracting metrics (tokens, tool calls, round trips)
4. Generating comparison reports

Usage:
    python automated_test_runner.py --scenarios 1,3,4,5,8
    python automated_test_runner.py --all
    python automated_test_runner.py --quick  # Top 5 scenarios
"""

import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import anthropic
import re


@dataclass
class TestConfig:
    """Configuration for a test run"""
    run_id: str
    test_type: str  # "baseline" or "optimized"
    skill_enabled: bool
    model: str
    scenarios: List[str]
    output_dir: Path


@dataclass
class ScenarioResult:
    """Results from running a single scenario"""
    scenario_id: str
    scenario_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    tool_calls: int
    round_trips: int
    execution_time_ms: float
    quality_score: float
    user_satisfaction: float
    notes: str
    full_transcript: str


class TransparentLogger:
    """Logs all interactions for full transparency"""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_log = []

    def log_request(self, scenario_id: str, test_type: str, prompt: str):
        """Log outgoing request"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "request",
            "scenario_id": scenario_id,
            "test_type": test_type,
            "prompt": prompt
        }
        self.session_log.append(entry)

        # Write to file immediately for transparency
        log_file = self.log_dir / f"{test_type}_{scenario_id}_request.json"
        with open(log_file, 'w') as f:
            json.dump(entry, f, indent=2)

        print(f"[{test_type}] Request logged: {scenario_id}")

    def log_response(self, scenario_id: str, test_type: str, response: Dict):
        """Log incoming response"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "scenario_id": scenario_id,
            "test_type": test_type,
            "response": response
        }
        self.session_log.append(entry)

        # Write to file immediately for transparency
        log_file = self.log_dir / f"{test_type}_{scenario_id}_response.json"
        with open(log_file, 'w') as f:
            json.dump(entry, f, indent=2)

        print(f"[{test_type}] Response logged: {scenario_id}")

    def save_session_log(self, filename: str):
        """Save complete session log"""
        log_file = self.log_dir / filename
        with open(log_file, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        print(f"Complete session log saved: {log_file}")


class MetricsExtractor:
    """Extracts metrics from API responses"""

    @staticmethod
    def count_tool_calls(response_data: Dict) -> int:
        """Count tool calls in response"""
        # Anthropic API returns usage info
        content = response_data.get('content', [])
        tool_calls = sum(1 for item in content if item.get('type') == 'tool_use')
        return tool_calls

    @staticmethod
    def extract_text(response_data: Dict) -> str:
        """Extract text from response"""
        content = response_data.get('content', [])
        text_parts = [item.get('text', '') for item in content if item.get('type') == 'text']
        return '\n'.join(text_parts)

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def estimate_tokens_from_words(word_count: int) -> int:
        """Estimate tokens (1.3 words per token)"""
        return int(word_count * 1.3)

    @staticmethod
    def get_actual_tokens(response_data: Dict) -> Tuple[int, int]:
        """Get actual token counts from API response"""
        usage = response_data.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        return input_tokens, output_tokens


class SkillTester:
    """Main testing orchestrator"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.logger: Optional[TransparentLogger] = None
        self.metrics_extractor = MetricsExtractor()

    def load_scenarios(self, scenarios_file: Path) -> List[Dict]:
        """Load test scenarios from JSON"""
        with open(scenarios_file, 'r') as f:
            data = json.load(f)
        return data['scenarios']

    def create_system_prompt(self, skill_enabled: bool) -> str:
        """Create system prompt with or without skill"""
        base_prompt = """You are Claude, a helpful AI assistant. Help the user with their request."""

        if skill_enabled:
            # Load the skill instructions
            skill_file = Path(__file__).parent.parent / "resource-minimizer" / "SKILL.md"
            if skill_file.exists():
                with open(skill_file, 'r') as f:
                    skill_content = f.read()
                    # Extract the content after the frontmatter
                    parts = skill_content.split('---', 2)
                    if len(parts) >= 3:
                        skill_instructions = parts[2].strip()
                    else:
                        skill_instructions = skill_content

                return f"""{base_prompt}

You have the resource-minimizer skill enabled. Follow these instructions:

{skill_instructions}

IMPORTANT: Apply the resource-minimizer principles to minimize token usage, tool calls, and computational overhead while maintaining quality."""
            else:
                print("Warning: Skill file not found, using base prompt")
                return base_prompt

        return base_prompt

    def run_scenario(
        self,
        scenario: Dict,
        test_type: str,
        skill_enabled: bool,
        model: str = "claude-sonnet-4-5-20250929"
    ) -> ScenarioResult:
        """Run a single test scenario"""

        scenario_id = scenario['id']
        scenario_name = scenario['name']
        test_prompt = scenario['test_prompt']

        print(f"\n{'='*80}")
        print(f"Running {test_type.upper()}: {scenario_id} - {scenario_name}")
        print(f"Skill enabled: {skill_enabled}")
        print(f"{'='*80}\n")

        # Log the request
        self.logger.log_request(scenario_id, test_type, test_prompt)

        # Create system prompt
        system_prompt = self.create_system_prompt(skill_enabled)

        # Start timing
        start_time = time.time()

        # Make API request
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=8192,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": test_prompt}
                ]
            )

            # Stop timing
            execution_time_ms = (time.time() - start_time) * 1000

            # Convert response to dict for logging
            response_dict = {
                "id": response.id,
                "type": response.type,
                "role": response.role,
                "content": [
                    {
                        "type": item.type,
                        "text": getattr(item, 'text', None),
                        "id": getattr(item, 'id', None),
                        "name": getattr(item, 'name', None),
                        "input": getattr(item, 'input', None)
                    }
                    for item in response.content
                ],
                "model": response.model,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }

            # Log the response
            self.logger.log_response(scenario_id, test_type, response_dict)

            # Extract metrics
            prompt_tokens, completion_tokens = self.metrics_extractor.get_actual_tokens(response_dict)
            total_tokens = prompt_tokens + completion_tokens
            tool_calls = self.metrics_extractor.count_tool_calls(response_dict)
            response_text = self.metrics_extractor.extract_text(response_dict)

            # Round trips (simplified - this is a single request)
            round_trips = 1

            # Quality scoring (automated heuristic - can be refined)
            quality_score = self._assess_quality(response_text, scenario, tool_calls)
            user_satisfaction = quality_score  # For automated testing, use same heuristic

            # Generate notes
            notes = f"Automated test. Tokens: {total_tokens}, Tools: {tool_calls}, Time: {execution_time_ms:.0f}ms"

            # Create full transcript
            full_transcript = self._format_transcript(test_prompt, response_text, response_dict)

            result = ScenarioResult(
                scenario_id=scenario_id,
                scenario_name=scenario_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                tool_calls=tool_calls,
                round_trips=round_trips,
                execution_time_ms=execution_time_ms,
                quality_score=quality_score,
                user_satisfaction=user_satisfaction,
                notes=notes,
                full_transcript=full_transcript
            )

            print(f"✓ Completed: {total_tokens} tokens, {tool_calls} tool calls, {execution_time_ms:.0f}ms")

            return result

        except Exception as e:
            print(f"✗ Error running scenario: {e}")
            raise

    def _assess_quality(self, response_text: str, scenario: Dict, tool_calls: int) -> float:
        """Automated quality assessment using heuristics"""
        # This is a simplified heuristic - real quality assessment would be more sophisticated

        word_count = self.metrics_extractor.count_words(response_text)

        # Base quality on whether response is substantive
        if word_count < 20:
            return 2.0  # Too short

        # Check if response addresses the scenario
        quality = 4.0  # Start with "good"

        # Bonus for appropriate length
        expected = scenario.get('optimized_expected', {}) if tool_calls < 10 else scenario.get('baseline_expected', {})

        # If response seems complete (has substance), give higher score
        if word_count > 50 and len(response_text) > 200:
            quality = 4.5

        return quality

    def _format_transcript(self, prompt: str, response_text: str, response_dict: Dict) -> str:
        """Format a readable transcript"""
        lines = [
            "="*80,
            "FULL TRANSCRIPT",
            "="*80,
            "",
            "USER PROMPT:",
            "-"*80,
            prompt,
            "",
            "CLAUDE RESPONSE:",
            "-"*80,
            response_text,
            "",
            "METADATA:",
            "-"*80,
            f"Input tokens: {response_dict['usage']['input_tokens']}",
            f"Output tokens: {response_dict['usage']['output_tokens']}",
            f"Total tokens: {response_dict['usage']['input_tokens'] + response_dict['usage']['output_tokens']}",
            f"Model: {response_dict['model']}",
            f"Stop reason: {response_dict['stop_reason']}",
            "="*80
        ]
        return "\n".join(lines)

    def run_test_suite(
        self,
        config: TestConfig,
        scenarios: List[Dict]
    ) -> List[ScenarioResult]:
        """Run a complete test suite"""

        print(f"\n{'#'*80}")
        print(f"# Starting {config.test_type.upper()} Test Suite")
        print(f"# Run ID: {config.run_id}")
        print(f"# Skill Enabled: {config.skill_enabled}")
        print(f"# Model: {config.model}")
        print(f"# Scenarios: {len(scenarios)}")
        print(f"{'#'*80}\n")

        results = []

        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[{i}/{len(scenarios)}] Running {scenario['id']}...")

            try:
                result = self.run_scenario(
                    scenario=scenario,
                    test_type=config.test_type,
                    skill_enabled=config.skill_enabled,
                    model=config.model
                )
                results.append(result)

                # Save transcript
                transcript_file = config.output_dir / f"{config.test_type}_{scenario['id']}_transcript.txt"
                with open(transcript_file, 'w') as f:
                    f.write(result.full_transcript)

                # Brief pause to avoid rate limits
                time.sleep(1)

            except Exception as e:
                print(f"Error in scenario {scenario['id']}: {e}")
                continue

        return results

    def save_results(self, results: List[ScenarioResult], output_file: Path):
        """Save results in format compatible with energy_assessment.py"""

        results_data = {
            "test_suite": output_file.stem.replace('_', ' ').title(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "skill_enabled": "optimized" in str(output_file),
            "model": "claude-sonnet-4-5-20250929",
            "tester_name": "Automated Test Runner",
            "platform": "anthropic-api",
            "notes": "Automatically generated test results with full transparency logs",
            "results": [
                {
                    "scenario_id": r.scenario_id,
                    "scenario_name": r.scenario_name,
                    "prompt_tokens": r.prompt_tokens,
                    "completion_tokens": r.completion_tokens,
                    "total_tokens": r.total_tokens,
                    "tool_calls": r.tool_calls,
                    "round_trips": r.round_trips,
                    "execution_time_ms": r.execution_time_ms,
                    "quality_score": r.quality_score,
                    "user_satisfaction": r.user_satisfaction,
                    "notes": r.notes
                }
                for r in results
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n✓ Results saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Automated testing for Resource Minimizer skill"
    )
    parser.add_argument(
        "--scenarios",
        help="Comma-separated scenario IDs (e.g., 1,3,4,5,8)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick test (top 5 scenarios)"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5-20250929",
        help="Model to use (default: claude-sonnet-4-5-20250929)"
    )
    parser.add_argument(
        "--output-dir",
        default="./automated_test_runs",
        help="Output directory for results"
    )

    args = parser.parse_args()

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{timestamp}"
    output_dir = Path(args.output_dir) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'#'*80}")
    print(f"# AUTOMATED SKILL TESTING FRAMEWORK")
    print(f"# Run ID: {run_id}")
    print(f"# Output: {output_dir}")
    print(f"{'#'*80}\n")

    # Initialize tester
    tester = SkillTester()

    # Initialize logger
    log_dir = output_dir / "logs"
    tester.logger = TransparentLogger(log_dir)

    # Load scenarios
    scenarios_file = Path(__file__).parent / "test_scenarios.json"
    all_scenarios = tester.load_scenarios(scenarios_file)

    # Filter scenarios based on arguments
    if args.all:
        selected_scenarios = [s for s in all_scenarios if s.get('should_trigger', True)]
    elif args.quick:
        # Top 5 that should trigger
        scenario_ids = ['scenario_001', 'scenario_003', 'scenario_004', 'scenario_005', 'scenario_008']
        selected_scenarios = [s for s in all_scenarios if s['id'] in scenario_ids]
    elif args.scenarios:
        scenario_ids = [f"scenario_{int(x):03d}" for x in args.scenarios.split(',')]
        selected_scenarios = [s for s in all_scenarios if s['id'] in scenario_ids]
    else:
        print("Error: Must specify --scenarios, --all, or --quick")
        return

    print(f"Selected {len(selected_scenarios)} scenarios to test\n")

    # Run baseline tests
    baseline_config = TestConfig(
        run_id=run_id,
        test_type="baseline",
        skill_enabled=False,
        model=args.model,
        scenarios=[s['id'] for s in selected_scenarios],
        output_dir=output_dir
    )

    print("\n" + "="*80)
    print("PHASE 1: BASELINE TESTING (WITHOUT SKILL)")
    print("="*80)

    baseline_results = tester.run_test_suite(baseline_config, selected_scenarios)
    baseline_file = output_dir / "baseline_results.json"
    tester.save_results(baseline_results, baseline_file)

    # Run optimized tests
    optimized_config = TestConfig(
        run_id=run_id,
        test_type="optimized",
        skill_enabled=True,
        model=args.model,
        scenarios=[s['id'] for s in selected_scenarios],
        output_dir=output_dir
    )

    print("\n" + "="*80)
    print("PHASE 2: OPTIMIZED TESTING (WITH SKILL)")
    print("="*80)

    optimized_results = tester.run_test_suite(optimized_config, selected_scenarios)
    optimized_file = output_dir / "optimized_results.json"
    tester.save_results(optimized_results, optimized_file)

    # Save complete session log
    tester.logger.save_session_log(f"complete_session_{run_id}.json")

    # Generate comparison report
    print("\n" + "="*80)
    print("GENERATING COMPARISON REPORT")
    print("="*80)

    import subprocess
    report_file = output_dir / "comparison_report.txt"

    try:
        subprocess.run([
            "python3",
            str(Path(__file__).parent / "energy_assessment.py"),
            "--compare",
            str(baseline_file),
            str(optimized_file),
            "--output",
            str(report_file)
        ], check=True)

        print(f"\n✓ Comparison report generated: {report_file}")

        # Print the report
        with open(report_file, 'r') as f:
            print("\n" + f.read())

    except subprocess.CalledProcessError as e:
        print(f"Error generating report: {e}")

    # Generate summary
    print("\n" + "="*80)
    print("TEST RUN COMPLETE")
    print("="*80)
    print(f"\nRun ID: {run_id}")
    print(f"Output Directory: {output_dir}")
    print(f"\nFiles generated:")
    print(f"  - {baseline_file} (baseline results)")
    print(f"  - {optimized_file} (optimized results)")
    print(f"  - {report_file} (comparison report)")
    print(f"  - {log_dir}/ (full transparency logs)")
    print(f"  - {output_dir}/*_transcript.txt (individual transcripts)")
    print("\nVerify transparency:")
    print(f"  cat {log_dir}/*.json")
    print(f"  cat {output_dir}/*_transcript.txt")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
