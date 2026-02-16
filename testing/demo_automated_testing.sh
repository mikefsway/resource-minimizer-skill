#!/bin/bash
# Demo script to showcase automated testing framework

set -e

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║  AUTOMATED TESTING FRAMEWORK - DEMONSTRATION                               ║"
echo "║  Resource Minimizer Skill                                                  ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY is not set!"
    echo ""
    echo "To run automated tests, you need an Anthropic API key."
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-...'"
    echo ""
    echo "Or create a .env file:"
    echo "  echo \"ANTHROPIC_API_KEY=sk-ant-...\" > .env"
    echo ""
    exit 1
fi

echo "✓ API key detected"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "⚠️  anthropic package not installed"
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "✓ Dependencies installed"
echo ""

echo "────────────────────────────────────────────────────────────────────────────"
echo "What this demo will do:"
echo "────────────────────────────────────────────────────────────────────────────"
echo ""
echo "1. Run 2 test scenarios through a BASELINE agent (no skill)"
echo "2. Run the SAME 2 scenarios through an OPTIMIZED agent (with skill)"
echo "3. Capture full transcripts and API logs for transparency"
echo "4. Generate a comparison report showing:"
echo "   - Token reduction %"
echo "   - Energy savings"
echo "   - Cost savings"
echo "   - Quality comparison"
echo ""
echo "All logs and transcripts will be saved for your verification."
echo ""
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Press Enter to start the demo (Ctrl+C to cancel)..."

echo ""
echo "Starting automated test run..."
echo ""

# Run a minimal test with 2 scenarios for demo purposes
python3 automated_test_runner.py --scenarios 3,5

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║  DEMO COMPLETE!                                                            ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Find the latest run directory
LATEST_RUN=$(ls -td automated_test_runs/run_* 2>/dev/null | head -1)

if [ -z "$LATEST_RUN" ]; then
    echo "No test run found. Something went wrong."
    exit 1
fi

echo "Test run directory: $LATEST_RUN"
echo ""
echo "Files generated:"
echo "  📊 $LATEST_RUN/comparison_report.txt"
echo "  📝 $LATEST_RUN/baseline_results.json"
echo "  📝 $LATEST_RUN/optimized_results.json"
echo "  📁 $LATEST_RUN/logs/ (full transparency)"
echo ""

echo "────────────────────────────────────────────────────────────────────────────"
echo "VERIFY TRANSPARENCY:"
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

echo "1. View comparison report:"
echo "   cat $LATEST_RUN/comparison_report.txt"
echo ""

echo "2. Check baseline transcript:"
echo "   cat $LATEST_RUN/baseline_scenario_003_transcript.txt"
echo ""

echo "3. Check optimized transcript:"
echo "   cat $LATEST_RUN/optimized_scenario_003_transcript.txt"
echo ""

echo "4. Verify baseline had NO skill:"
echo "   cat $LATEST_RUN/logs/baseline_scenario_003_request.json | grep -i 'resource-minimizer' || echo '✓ No skill in baseline'"
echo ""

echo "5. Verify optimized HAD skill:"
echo "   cat $LATEST_RUN/logs/optimized_scenario_003_request.json | grep -i 'resource-minimizer' && echo '✓ Skill present in optimized'"
echo ""

echo "6. See actual token counts from API:"
echo "   echo 'Baseline:' && cat $LATEST_RUN/logs/baseline_scenario_003_response.json | jq '.response.usage'"
echo "   echo 'Optimized:' && cat $LATEST_RUN/logs/optimized_scenario_003_response.json | jq '.response.usage'"
echo ""

echo "────────────────────────────────────────────────────────────────────────────"
echo "NEXT STEPS:"
echo "────────────────────────────────────────────────────────────────────────────"
echo ""
echo "Run a full test:"
echo "  python3 automated_test_runner.py --quick  # 5 scenarios"
echo "  python3 automated_test_runner.py --all    # All scenarios"
echo ""

echo "Read the guide:"
echo "  cat AUTOMATED_TESTING_GUIDE.md"
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  This framework gives you REPRODUCIBLE, TRANSPARENT, AUTOMATED testing     ║"
echo "║  No manual counting. No estimation. Just run, verify, and report.          ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
