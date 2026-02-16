# 🧪 Resource Minimizer Testing - START HERE

## What is This?

This folder contains tools to **empirically test** whether the resource-minimizer skill actually reduces energy consumption and computational costs.

## ⚠️ Important Clarification

**THEORETICAL vs EMPIRICAL:**

- Files starting with `THEORETICAL_` contain **predictions**, not real test results
- They show what we *expect* might happen based on the skill's design
- **They are NOT proof the skill works**

**To get REAL results, you need to run your own tests following the guides in this folder.**

## Quick Start (5 minutes)

### 1. Understand What Testing Involves

You'll run the same tasks with Claude twice:
1. **Baseline:** WITHOUT the skill (normal Claude)
2. **Optimized:** WITH the skill enabled

Then compare:
- Token usage (how much Claude generates)
- Tool calls (how many tools Claude uses)
- Quality (is it still good?)
- Your satisfaction (do you prefer it?)

### 2. Choose Your Path

**Path A: Quick Test (30 min) - Recommended First**
- Test 5 scenarios
- Get directional results
- See if it's worth deeper testing

**Path B: Comprehensive Test (60 min)**
- Test all 10 scenarios
- Get statistical significance
- Publishable results

**Path C: Just Read The Theory**
- Read `THEORETICAL_ANALYSIS.md`
- Understand the predictions
- Skip actual testing

### 3. Follow the Guide

📖 **Read:** `RUN_TESTS.md` - Complete step-by-step instructions

This guide covers:
- How to install the skill
- How to run tests
- How to record metrics
- How to analyze results
- What everything means

### 4. Use the Tools

| File | Purpose | When to Use |
|------|---------|-------------|
| `RUN_TESTS.md` | Step-by-step guide | Read first |
| `test_scenarios.json` | Test prompts | Copy prompts from here |
| `test_results_template.json` | Results template | Copy to record your data |
| `energy_assessment.py` | Analysis tool | After collecting data |
| `README.md` | Overview | For reference |

## What You'll Need

- ⏰ 30-60 minutes
- 💻 Claude.ai account OR Claude Code CLI
- 🐍 Python 3.7+ (for analysis)
- 📝 Text editor
- 🧮 Calculator or spreadsheet (for counting)

## Expected Outcomes

### If Skill Works as Designed ✅
- 40-60% fewer tokens generated
- 40-60% less energy used
- Quality stays above 90%
- You prefer the concise responses

### If Skill Doesn't Work ❌
- Similar token usage
- No behavioral difference
- Skill might not be activating
- Something to fix!

### Either Way 📊
**Your empirical data is valuable!** Both positive and negative results help improve the skill.

## The Process (High Level)

```
1. Install skill
   ↓
2. Test WITHOUT skill → Record metrics → Save as baseline
   ↓
3. Test WITH skill → Record metrics → Save as optimized
   ↓
4. Run analysis tool → Compare → Generate report
   ↓
5. Review results → Determine if skill is effective
```

## Files Explained Simply

### Guides (Read These)
- **START_HERE.md** ← You are here
- **RUN_TESTS.md** ← Detailed instructions
- **README.md** ← Overview and FAQ

### Tools (Use These)
- **test_scenarios.json** ← Test prompts to use
- **test_results_template.json** ← Where to record data
- **energy_assessment.py** ← Analyzes your results

### Examples (Reference Only)
- **THEORETICAL_ANALYSIS.md** ← Predicted results (NOT real)
- **THEORETICAL_SUMMARY.md** ← Summary of predictions (NOT real)
- **THEORETICAL_baseline_example.json** ← Example format (NOT real data)
- **THEORETICAL_optimized_example.json** ← Example format (NOT real data)

## Common Questions

### Q: Do I have to test all 10 scenarios?
**A:** No! Start with 5. More is better but 5 gives useful results.

### Q: How do I count tokens if I don't have access to token counts?
**A:** Count words × 1.3. It's an approximation but works fine for comparison.

### Q: What if I get different results than the theoretical predictions?
**A:** Great! That's empirical data. Document what you found - it's valuable.

### Q: Can I just read the theoretical analysis instead of testing?
**A:** You can, but remember it's predictions, not proof. Real testing validates (or refutes) the theory.

### Q: How long does this take?
**A:**
- Setup: 5 min
- 5 scenarios baseline: 15 min
- 5 scenarios optimized: 15 min
- Analysis: 5 min
- **Total: ~40 min**

### Q: What if the skill doesn't seem to work?
**A:** Document it! Negative results are important. Check installation, verify scenarios should trigger, and report findings.

### Q: Do I need to be technical?
**A:** Helpful but not required. If you can:
- Follow step-by-step instructions
- Count things
- Copy/paste prompts
- Run a Python script

...you can do this!

## Success Criteria

The skill is effective if your tests show:
- ✅ 30%+ reduction in token usage
- ✅ Quality stays above 90% of baseline
- ✅ Satisfaction maintained or improved

## Next Steps

### Ready to Test?
1. ✅ Read `RUN_TESTS.md` completely
2. ✅ Install the skill
3. ✅ Copy `test_results_template.json` twice
4. ✅ Start testing!

### Just Want to Understand?
1. ✅ Read `README.md`
2. ✅ Review `test_scenarios.json`
3. ✅ Read `THEORETICAL_ANALYSIS.md` (but remember it's theoretical)

### Want to See Example Output?
1. ✅ Run: `python3 energy_assessment.py --compare THEORETICAL_baseline_example.json THEORETICAL_optimized_example.json`
2. ✅ See what the report looks like
3. ✅ Remember: that's example data, not real results

## Get Help

Stuck? Check:
1. `RUN_TESTS.md` for detailed procedures
2. `README.md` for FAQ
3. GitHub Issues for community help

## Contribute

If you run empirical tests:
1. Generate your report
2. Open a GitHub issue: "Empirical Test Results - [Date]"
3. Share your findings
4. Help validate (or refute) the theoretical predictions!

---

**Ready?** → Open `RUN_TESTS.md` and start testing!

**Not sure?** → Read `README.md` for more context

**Just curious?** → Check `THEORETICAL_ANALYSIS.md` (remembering it's predictions)
