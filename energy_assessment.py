#!/usr/bin/env python3
"""
Energy Assessment Tool for Resource Minimizer Skill

This script helps measure the empirical effectiveness of the resource-minimizer
skill in terms of token usage, computational overhead, and estimated energy consumption.

Usage:
    python energy_assessment.py --baseline results_baseline.json
    python energy_assessment.py --optimized results_optimized.json
    python energy_assessment.py --compare results_baseline.json results_optimized.json
"""

import json
import argparse
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    """Represents a single test execution result"""
    scenario_id: str
    scenario_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    tool_calls: int
    round_trips: int
    execution_time_ms: float
    quality_score: float  # 0-5 scale
    user_satisfaction: float  # 0-5 scale
    notes: str = ""


@dataclass
class EnergyMetrics:
    """Energy consumption estimates"""
    total_tokens: int
    estimated_kwh: float
    estimated_cost_usd: float
    estimated_co2_kg: float
    tool_operations: int
    context_loads: int


class EnergyCalculator:
    """Calculate energy consumption based on token usage and operations"""

    # Constants based on research and API pricing
    # Note: These are estimates - actual values may vary
    KWH_PER_MILLION_TOKENS = 0.2  # Conservative estimate for inference
    SONNET_INPUT_COST = 3.0 / 1_000_000  # $3 per MTok
    SONNET_OUTPUT_COST = 15.0 / 1_000_000  # $15 per MTok
    CO2_KG_PER_KWH = 0.43  # US grid average
    CONTEXT_LOAD_MULTIPLIER = 1.5  # Additional cost for context loading
    TOOL_CALL_OVERHEAD_TOKENS = 50  # Estimated overhead per tool call

    @classmethod
    def calculate_energy(cls, result: TestResult) -> EnergyMetrics:
        """Calculate energy metrics for a test result"""

        # Account for context reloading on each round-trip
        effective_input_tokens = result.prompt_tokens * result.round_trips

        # Account for tool call overhead
        tool_overhead_tokens = result.tool_calls * cls.TOOL_CALL_OVERHEAD_TOKENS

        total_tokens = effective_input_tokens + result.completion_tokens + tool_overhead_tokens

        # Energy consumption
        kwh = (total_tokens / 1_000_000) * cls.KWH_PER_MILLION_TOKENS

        # Cost
        cost = (
            result.prompt_tokens * result.round_trips * cls.SONNET_INPUT_COST +
            result.completion_tokens * cls.SONNET_OUTPUT_COST
        )

        # CO2 emissions
        co2_kg = kwh * cls.CO2_KG_PER_KWH

        return EnergyMetrics(
            total_tokens=total_tokens,
            estimated_kwh=kwh,
            estimated_cost_usd=cost,
            estimated_co2_kg=co2_kg,
            tool_operations=result.tool_calls,
            context_loads=result.round_trips
        )

    @classmethod
    def compare_energy(cls, baseline: EnergyMetrics, optimized: EnergyMetrics) -> Dict:
        """Compare energy metrics between baseline and optimized"""

        def pct_reduction(base, opt):
            if base == 0:
                return 0
            return ((base - opt) / base) * 100

        return {
            "token_reduction_pct": pct_reduction(baseline.total_tokens, optimized.total_tokens),
            "energy_reduction_pct": pct_reduction(baseline.estimated_kwh, optimized.estimated_kwh),
            "cost_reduction_pct": pct_reduction(baseline.estimated_cost_usd, optimized.estimated_cost_usd),
            "co2_reduction_pct": pct_reduction(baseline.estimated_co2_kg, optimized.estimated_co2_kg),
            "tool_call_reduction_pct": pct_reduction(baseline.tool_operations, optimized.tool_operations),
            "round_trip_reduction_pct": pct_reduction(baseline.context_loads, optimized.context_loads),
            "absolute_energy_saved_kwh": baseline.estimated_kwh - optimized.estimated_kwh,
            "absolute_cost_saved_usd": baseline.estimated_cost_usd - optimized.estimated_cost_usd,
            "absolute_co2_saved_kg": baseline.estimated_co2_kg - optimized.estimated_co2_kg
        }


class ResultsAnalyzer:
    """Analyze test results and generate reports"""

    @staticmethod
    def load_results(filepath: str) -> List[TestResult]:
        """Load test results from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        results = []
        for item in data.get('results', []):
            results.append(TestResult(**item))

        return results

    @staticmethod
    def aggregate_metrics(results: List[TestResult]) -> Dict:
        """Aggregate metrics across all test results"""
        total_prompt_tokens = sum(r.prompt_tokens for r in results)
        total_completion_tokens = sum(r.completion_tokens for r in results)
        total_tokens = sum(r.total_tokens for r in results)
        total_tool_calls = sum(r.tool_calls for r in results)
        total_round_trips = sum(r.round_trips for r in results)
        avg_quality = sum(r.quality_score for r in results) / len(results) if results else 0
        avg_satisfaction = sum(r.user_satisfaction for r in results) / len(results) if results else 0

        return {
            "num_tests": len(results),
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_tokens,
            "avg_tokens_per_test": total_tokens / len(results) if results else 0,
            "total_tool_calls": total_tool_calls,
            "avg_tool_calls_per_test": total_tool_calls / len(results) if results else 0,
            "total_round_trips": total_round_trips,
            "avg_round_trips_per_test": total_round_trips / len(results) if results else 0,
            "avg_quality_score": avg_quality,
            "avg_user_satisfaction": avg_satisfaction
        }

    @staticmethod
    def generate_report(baseline_results: List[TestResult],
                       optimized_results: List[TestResult]) -> Dict:
        """Generate comprehensive comparison report"""

        baseline_agg = ResultsAnalyzer.aggregate_metrics(baseline_results)
        optimized_agg = ResultsAnalyzer.aggregate_metrics(optimized_results)

        # Calculate energy for all tests
        baseline_energy = [EnergyCalculator.calculate_energy(r) for r in baseline_results]
        optimized_energy = [EnergyCalculator.calculate_energy(r) for r in optimized_results]

        # Aggregate energy metrics
        total_baseline_energy = EnergyMetrics(
            total_tokens=sum(e.total_tokens for e in baseline_energy),
            estimated_kwh=sum(e.estimated_kwh for e in baseline_energy),
            estimated_cost_usd=sum(e.estimated_cost_usd for e in baseline_energy),
            estimated_co2_kg=sum(e.estimated_co2_kg for e in baseline_energy),
            tool_operations=sum(e.tool_operations for e in baseline_energy),
            context_loads=sum(e.context_loads for e in baseline_energy)
        )

        total_optimized_energy = EnergyMetrics(
            total_tokens=sum(e.total_tokens for e in optimized_energy),
            estimated_kwh=sum(e.estimated_kwh for e in optimized_energy),
            estimated_cost_usd=sum(e.estimated_cost_usd for e in optimized_energy),
            estimated_co2_kg=sum(e.estimated_co2_kg for e in optimized_energy),
            tool_operations=sum(e.tool_operations for e in optimized_energy),
            context_loads=sum(e.context_loads for e in optimized_energy)
        )

        comparison = EnergyCalculator.compare_energy(total_baseline_energy, total_optimized_energy)

        # Quality check
        quality_maintained = optimized_agg['avg_quality_score'] >= baseline_agg['avg_quality_score'] * 0.9
        satisfaction_maintained = optimized_agg['avg_user_satisfaction'] >= baseline_agg['avg_user_satisfaction'] * 0.9

        return {
            "test_date": datetime.now().isoformat(),
            "baseline_metrics": baseline_agg,
            "optimized_metrics": optimized_agg,
            "baseline_energy": {
                "total_tokens": total_baseline_energy.total_tokens,
                "estimated_kwh": round(total_baseline_energy.estimated_kwh, 6),
                "estimated_cost_usd": round(total_baseline_energy.estimated_cost_usd, 4),
                "estimated_co2_kg": round(total_baseline_energy.estimated_co2_kg, 4)
            },
            "optimized_energy": {
                "total_tokens": total_optimized_energy.total_tokens,
                "estimated_kwh": round(total_optimized_energy.estimated_kwh, 6),
                "estimated_cost_usd": round(total_optimized_energy.estimated_cost_usd, 4),
                "estimated_co2_kg": round(total_optimized_energy.estimated_co2_kg, 4)
            },
            "savings": {
                "token_reduction_pct": round(comparison['token_reduction_pct'], 2),
                "energy_reduction_pct": round(comparison['energy_reduction_pct'], 2),
                "cost_reduction_pct": round(comparison['cost_reduction_pct'], 2),
                "co2_reduction_pct": round(comparison['co2_reduction_pct'], 2),
                "tool_call_reduction_pct": round(comparison['tool_call_reduction_pct'], 2),
                "round_trip_reduction_pct": round(comparison['round_trip_reduction_pct'], 2),
                "energy_saved_kwh": round(comparison['absolute_energy_saved_kwh'], 6),
                "cost_saved_usd": round(comparison['absolute_cost_saved_usd'], 4),
                "co2_saved_kg": round(comparison['absolute_co2_saved_kg'], 4)
            },
            "quality_assessment": {
                "quality_maintained": quality_maintained,
                "satisfaction_maintained": satisfaction_maintained,
                "baseline_quality": round(baseline_agg['avg_quality_score'], 2),
                "optimized_quality": round(optimized_agg['avg_quality_score'], 2),
                "baseline_satisfaction": round(baseline_agg['avg_user_satisfaction'], 2),
                "optimized_satisfaction": round(optimized_agg['avg_user_satisfaction'], 2)
            },
            "scaled_projections": {
                "per_1000_tasks": {
                    "energy_saved_kwh": round(comparison['absolute_energy_saved_kwh'] * 1000 / len(baseline_results), 3),
                    "cost_saved_usd": round(comparison['absolute_cost_saved_usd'] * 1000 / len(baseline_results), 2),
                    "co2_saved_kg": round(comparison['absolute_co2_saved_kg'] * 1000 / len(baseline_results), 2)
                },
                "per_1_million_tasks": {
                    "energy_saved_kwh": round(comparison['absolute_energy_saved_kwh'] * 1_000_000 / len(baseline_results), 1),
                    "cost_saved_usd": round(comparison['absolute_cost_saved_usd'] * 1_000_000 / len(baseline_results), 2),
                    "co2_saved_kg": round(comparison['absolute_co2_saved_kg'] * 1_000_000 / len(baseline_results), 1),
                    "co2_saved_metric_tons": round(comparison['absolute_co2_saved_kg'] * 1_000_000 / len(baseline_results) / 1000, 2)
                }
            },
            "conclusion": {
                "effective": comparison['energy_reduction_pct'] > 30 and quality_maintained,
                "meets_targets": all([
                    comparison['token_reduction_pct'] > 30,
                    comparison['energy_reduction_pct'] > 30,
                    quality_maintained,
                    satisfaction_maintained
                ]),
                "recommendation": "APPROVED" if (comparison['energy_reduction_pct'] > 30 and quality_maintained) else "NEEDS_IMPROVEMENT"
            }
        }


def format_report(report: Dict) -> str:
    """Format report as human-readable text"""

    lines = [
        "=" * 80,
        "RESOURCE MINIMIZER SKILL - ENERGY ASSESSMENT REPORT",
        "=" * 80,
        f"\nTest Date: {report['test_date']}",
        f"Number of Tests: {report['baseline_metrics']['num_tests']}",
        "\n" + "-" * 80,
        "BASELINE METRICS",
        "-" * 80,
        f"Total Tokens: {report['baseline_metrics']['total_tokens']:,}",
        f"Avg Tokens/Test: {report['baseline_metrics']['avg_tokens_per_test']:.0f}",
        f"Total Tool Calls: {report['baseline_metrics']['total_tool_calls']}",
        f"Avg Tool Calls/Test: {report['baseline_metrics']['avg_tool_calls_per_test']:.1f}",
        f"Total Round Trips: {report['baseline_metrics']['total_round_trips']}",
        f"Avg Round Trips/Test: {report['baseline_metrics']['avg_round_trips_per_test']:.1f}",
        f"Avg Quality Score: {report['baseline_metrics']['avg_quality_score']:.2f}/5.0",
        f"Avg User Satisfaction: {report['baseline_metrics']['avg_user_satisfaction']:.2f}/5.0",
        "",
        f"Estimated Energy: {report['baseline_energy']['estimated_kwh']:.6f} kWh",
        f"Estimated Cost: ${report['baseline_energy']['estimated_cost_usd']:.4f}",
        f"Estimated CO2: {report['baseline_energy']['estimated_co2_kg']:.4f} kg",
        "\n" + "-" * 80,
        "OPTIMIZED METRICS (With Resource Minimizer)",
        "-" * 80,
        f"Total Tokens: {report['optimized_metrics']['total_tokens']:,}",
        f"Avg Tokens/Test: {report['optimized_metrics']['avg_tokens_per_test']:.0f}",
        f"Total Tool Calls: {report['optimized_metrics']['total_tool_calls']}",
        f"Avg Tool Calls/Test: {report['optimized_metrics']['avg_tool_calls_per_test']:.1f}",
        f"Total Round Trips: {report['optimized_metrics']['total_round_trips']}",
        f"Avg Round Trips/Test: {report['optimized_metrics']['avg_round_trips_per_test']:.1f}",
        f"Avg Quality Score: {report['optimized_metrics']['avg_quality_score']:.2f}/5.0",
        f"Avg User Satisfaction: {report['optimized_metrics']['avg_user_satisfaction']:.2f}/5.0",
        "",
        f"Estimated Energy: {report['optimized_energy']['estimated_kwh']:.6f} kWh",
        f"Estimated Cost: ${report['optimized_energy']['estimated_cost_usd']:.4f}",
        f"Estimated CO2: {report['optimized_energy']['estimated_co2_kg']:.4f} kg",
        "\n" + "=" * 80,
        "SAVINGS ANALYSIS",
        "=" * 80,
        f"Token Reduction: {report['savings']['token_reduction_pct']:.1f}%",
        f"Energy Reduction: {report['savings']['energy_reduction_pct']:.1f}%",
        f"Cost Reduction: {report['savings']['cost_reduction_pct']:.1f}%",
        f"CO2 Reduction: {report['savings']['co2_reduction_pct']:.1f}%",
        f"Tool Call Reduction: {report['savings']['tool_call_reduction_pct']:.1f}%",
        f"Round Trip Reduction: {report['savings']['round_trip_reduction_pct']:.1f}%",
        "",
        f"Absolute Energy Saved: {report['savings']['energy_saved_kwh']:.6f} kWh",
        f"Absolute Cost Saved: ${report['savings']['cost_saved_usd']:.4f}",
        f"Absolute CO2 Saved: {report['savings']['co2_saved_kg']:.4f} kg",
        "\n" + "-" * 80,
        "QUALITY ASSESSMENT",
        "-" * 80,
        f"Quality Maintained (>90%): {'✓ YES' if report['quality_assessment']['quality_maintained'] else '✗ NO'}",
        f"Satisfaction Maintained (>90%): {'✓ YES' if report['quality_assessment']['satisfaction_maintained'] else '✗ NO'}",
        f"Quality: {report['quality_assessment']['baseline_quality']:.2f} → {report['quality_assessment']['optimized_quality']:.2f}",
        f"Satisfaction: {report['quality_assessment']['baseline_satisfaction']:.2f} → {report['quality_assessment']['optimized_satisfaction']:.2f}",
        "\n" + "-" * 80,
        "SCALED PROJECTIONS",
        "-" * 80,
        "Per 1,000 Tasks:",
        f"  Energy Saved: {report['scaled_projections']['per_1000_tasks']['energy_saved_kwh']:.3f} kWh",
        f"  Cost Saved: ${report['scaled_projections']['per_1000_tasks']['cost_saved_usd']:.2f}",
        f"  CO2 Saved: {report['scaled_projections']['per_1000_tasks']['co2_saved_kg']:.2f} kg",
        "",
        "Per 1 Million Tasks:",
        f"  Energy Saved: {report['scaled_projections']['per_1_million_tasks']['energy_saved_kwh']:,.1f} kWh",
        f"  Cost Saved: ${report['scaled_projections']['per_1_million_tasks']['cost_saved_usd']:,.2f}",
        f"  CO2 Saved: {report['scaled_projections']['per_1_million_tasks']['co2_saved_metric_tons']:.2f} metric tons",
        "\n" + "=" * 80,
        "CONCLUSION",
        "=" * 80,
        f"Effective: {'✓ YES' if report['conclusion']['effective'] else '✗ NO'}",
        f"Meets All Targets: {'✓ YES' if report['conclusion']['meets_targets'] else '✗ NO'}",
        f"Recommendation: {report['conclusion']['recommendation']}",
        "=" * 80,
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Assess energy effectiveness of Resource Minimizer skill"
    )
    parser.add_argument(
        "--baseline",
        help="Path to baseline test results JSON"
    )
    parser.add_argument(
        "--optimized",
        help="Path to optimized test results JSON"
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("BASELINE", "OPTIMIZED"),
        help="Compare baseline and optimized results"
    )
    parser.add_argument(
        "--output",
        help="Output file for report (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    args = parser.parse_args()

    if args.compare:
        baseline_results = ResultsAnalyzer.load_results(args.compare[0])
        optimized_results = ResultsAnalyzer.load_results(args.compare[1])

        report = ResultsAnalyzer.generate_report(baseline_results, optimized_results)

        if args.format == "json":
            output = json.dumps(report, indent=2)
        else:
            output = format_report(report)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Report written to {args.output}")
        else:
            print(output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
