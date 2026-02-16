# Step-by-Step Testing Procedure

This guide walks you through running empirical tests to measure the actual effectiveness of the resource-minimizer skill.

## Time Required

- **Quick Test (5 scenarios):** ~30 minutes
- **Comprehensive Test (10 scenarios):** ~60 minutes

## What You'll Measure

1. **Token usage** - How many tokens Claude generates
2. **Tool calls** - How many tools Claude uses
3. **Round trips** - How many back-and-forth exchanges
4. **Quality** - How good the answers are (your rating)
5. **Satisfaction** - How satisfied you are with the response (your rating)

From these, we calculate:
- Energy consumption (estimated)
- API costs (estimated)
- CO2 emissions (estimated)

## Preparation

### 1. Set Up Your Environment

Choose your platform:

**Option A: Claude.ai (Web)**
1. Go to https://claude.ai
2. Go to Settings → Capabilities → Skills
3. Click "Upload Skill"
4. Upload `resource-minimizer.zip` (create it: `zip -r resource-minimizer.zip ../resource-minimizer/`)

**Option B: Claude Code CLI**
```bash
# macOS/Linux
cp -r ../resource-minimizer ~/.config/claude-code/skills/

# Windows
copy ..\resource-minimizer %APPDATA%\claude-code\skills\

# Verify installation
ls ~/.config/claude-code/skills/resource-minimizer/
```

### 2. Prepare Your Results Files

```bash
# Copy the template twice
cp test_results_template.json my_baseline_results.json
cp test_results_template.json my_optimized_results.json
```

Edit the headers:
- `my_baseline_results.json`: Set `"skill_enabled": false`
- `my_optimized_results.json`: Set `"skill_enabled": true`

### 3. Choose Your Test Scenarios

Open `test_scenarios.json` and select scenarios to test.

**Recommended starting set (5 scenarios):**
- scenario_001: Multi-Step Code Refactoring
- scenario_003: Research Task - Security Practices
- scenario_004: Long Document Generation
- scenario_005: Ambiguous Database Setup
- scenario_008: Complex Data Analysis Pipeline

**Why these?** They should trigger the skill and show measurable differences.

**Don't test these yet:**
- scenario_002, 007, 010 (should NOT trigger skill - useful for validation)

## Phase 1: Baseline Testing (WITHOUT Skill)

### For Each Scenario:

#### Step 1: Start Fresh
- Open a NEW Claude conversation/session
- Make sure skill is NOT active
- Clear any previous context

#### Step 2: Send the Test Prompt
- Copy the exact `test_prompt` from `test_scenarios.json`
- Paste into Claude
- Send

Example for scenario_001:
```
I have a Python application with authentication logic scattered across
multiple files. Help me refactor it to be more maintainable with proper
error handling, logging, and tests.
```

#### Step 3: Observe Claude's Response
Watch for:
- How comprehensive is the response?
- Does Claude ask clarifying questions?
- How many tools does Claude use?
- Does Claude generate everything upfront or progressively?

#### Step 4: Record Metrics

Open `my_baseline_results.json` and add an entry:

```json
{
  "scenario_id": "scenario_001",
  "scenario_name": "Multi-Step Code Refactoring",
  "prompt_tokens": ESTIMATE_HERE,
  "completion_tokens": ESTIMATE_HERE,
  "total_tokens": PROMPT + COMPLETION,
  "tool_calls": COUNT_HERE,
  "round_trips": COUNT_HERE,
  "execution_time_ms": ESTIMATE_HERE,
  "quality_score": RATE_1_TO_5,
  "user_satisfaction": RATE_1_TO_5,
  "notes": "Your observations"
}
```

**How to fill in each field:**

##### prompt_tokens
Count words in your prompt, multiply by 1.3
```
Example: "I have a Python application..." = 24 words
24 × 1.3 = 31 tokens (round to nearest integer)
```

##### completion_tokens
Count words in Claude's response, multiply by 1.3
```
Example: Claude wrote 800 words
800 × 1.3 = 1040 tokens
```

##### total_tokens
Add prompt_tokens + completion_tokens

##### tool_calls
Count each tool Claude used:
```
Read file: 1
Edit file: 1
Grep search: 1
Bash command: 1
Total: 4 tool calls
```

##### round_trips
Count exchanges:
```
You send prompt: 1
Claude asks clarifying question: 1 (round trip 2 started)
You answer: 1
Claude responds: 1 (total: 2 round trips)
```

##### execution_time_ms
Estimate time from send to response completion in milliseconds:
```
~5 seconds = 5000
~10 seconds = 10000
~30 seconds = 30000
```

##### quality_score
Rate answer quality 1-5:
- 5 = Excellent, comprehensive, correct
- 4 = Good, mostly correct, minor issues
- 3 = Adequate, some issues
- 2 = Poor, significant issues
- 1 = Unusable

##### user_satisfaction
Rate your satisfaction 1-5:
- 5 = Very satisfied, exactly what I needed
- 4 = Satisfied, mostly what I needed
- 3 = Neutral, acceptable
- 2 = Unsatisfied, not quite right
- 1 = Very unsatisfied

##### notes
Write observations:
```
"Claude generated complete refactoring upfront with comprehensive
error handling. Created 5 new files. Included detailed documentation."
```

#### Step 5: Repeat for All Scenarios

Complete all chosen scenarios before moving to Phase 2.

**IMPORTANT:** Don't rush. Quality data > speed.

### Baseline Phase Complete

You should now have `my_baseline_results.json` with all scenarios recorded.

## Phase 2: Optimized Testing (WITH Skill)

### Enable the Skill

**Claude.ai:**
- Make sure skill is uploaded and enabled in settings
- OR invoke with `/resource-minimizer` at start of session

**Claude Code:**
- Skill should be auto-detected if installed correctly
- Verify: Look for skill activation in responses

### For Each Scenario:

#### Step 1: Start Fresh
- Open a NEW Claude conversation/session
- VERIFY skill is active
- Clear any previous context

#### Step 2: Send IDENTICAL Test Prompt
- Use the EXACT SAME prompt as baseline
- Copy from `test_scenarios.json` (not from memory)
- This ensures fair comparison

#### Step 3: Observe DIFFERENT Behavior
Watch for differences:
- Is response more concise?
- Does Claude offer expansions instead of full content?
- Fewer clarifying questions?
- More assumptions with correction offers?
- Fewer tool calls?
- Progressive approach vs upfront?

Example differences:
```
BASELINE:
"I'll refactor your authentication system. [Generates complete
solution with all files, tests, docs]"

OPTIMIZED WITH SKILL:
"I'll refactor the core authentication logic first. [Shows main
refactoring]. I can add error handling, logging, or tests if needed."
```

#### Step 4: Record Metrics
Add to `my_optimized_results.json` with same fields as baseline.

**CRITICAL:** Use same scenario_id to enable comparison.

#### Step 5: Compare As You Go
Notice differences in real-time:
- Token count lower? (shorter responses)
- Fewer tool calls?
- Single round trip vs multiple?
- Still high quality?

### Optimized Phase Complete

You should now have `my_optimized_results.json` with all scenarios recorded.

## Phase 3: Analysis

### Run the Assessment Tool

```bash
python3 energy_assessment.py \
  --compare my_baseline_results.json my_optimized_results.json \
  > my_test_report.txt
```

This generates a report showing:
- Token reduction percentage
- Energy savings
- Cost savings
- CO2 reduction
- Quality comparison
- Whether skill meets targets

### Generate JSON Report (Optional)

```bash
python3 energy_assessment.py \
  --compare my_baseline_results.json my_optimized_results.json \
  --format json \
  --output my_test_report.json
```

### Review Results

Open `my_test_report.txt` and check:

#### Success Indicators ✅
- Token reduction > 30%
- Energy reduction > 30%
- Quality maintained > 90%
- Satisfaction maintained > 90%

#### Concern Indicators ⚠️
- Token reduction < 20%
- Quality drops > 10%
- Satisfaction decreases
- Skill didn't seem to activate

### Interpret Your Results

**If skill is effective:**
- Significant token/energy reduction
- Quality maintained
- Satisfaction same or better
- Clear behavioral differences observed

**If results unclear:**
- Try more scenarios
- Verify skill was actually active
- Check if scenarios were complex enough to trigger
- Review notes for patterns

**If skill seems ineffective:**
- Verify installation
- Check trigger conditions
- Review which scenarios should/shouldn't trigger
- Document findings - this is valuable feedback!

## Phase 4: Validation (Optional)

### Test Non-Triggering Scenarios

Test scenarios that should NOT trigger the skill:
- scenario_002: Simple Factual Question
- scenario_007: Quick Clarification
- scenario_010: Casual Greeting

**Expected:** Baseline and optimized results should be nearly identical.

**Why?** Validates that skill correctly identifies when NOT to activate.

### Calculate Trigger Accuracy

```
Accuracy = (Correct activations + Correct non-activations) / Total tests
Should be > 85%
```

## Common Pitfalls

### ❌ Different prompts for baseline vs optimized
**Solution:** Copy exact prompt from JSON, use for both tests

### ❌ Testing in same conversation
**Solution:** Always start fresh session for each test

### ❌ Skill not actually enabled
**Solution:** Verify installation, look for behavioral changes

### ❌ Estimating tokens too loosely
**Solution:** Use word count × 1.3, be consistent

### ❌ Rating quality/satisfaction inconsistently
**Solution:** Define your scale upfront, apply consistently

### ❌ Not recording observations
**Solution:** Write notes immediately, details fade quickly

## Quick Reference

### Baseline Test Checklist
- [ ] Fresh session
- [ ] Skill NOT active
- [ ] Copy exact prompt
- [ ] Observe behavior
- [ ] Count tool calls
- [ ] Count round trips
- [ ] Estimate tokens
- [ ] Rate quality (1-5)
- [ ] Rate satisfaction (1-5)
- [ ] Write notes
- [ ] Record in JSON

### Optimized Test Checklist
- [ ] Fresh session
- [ ] Skill IS active
- [ ] Use SAME prompt
- [ ] Observe DIFFERENT behavior
- [ ] Count tool calls
- [ ] Count round trips
- [ ] Estimate tokens
- [ ] Rate quality (1-5)
- [ ] Rate satisfaction (1-5)
- [ ] Write notes
- [ ] Record in JSON

### Analysis Checklist
- [ ] Run energy_assessment.py
- [ ] Review token reduction %
- [ ] Check quality maintained
- [ ] Check satisfaction maintained
- [ ] Verify meets targets (>30% reduction, >90% quality)
- [ ] Document findings

## Example Session

Here's what a complete test session looks like:

### Baseline (scenario_003: Security Research)

**Prompt:**
```
What are the current best practices for securing REST APIs?
I'm building a financial services application.
```

**Claude Response (excerpt):**
```
For securing REST APIs in financial services, here are comprehensive
best practices:

1. Authentication & Authorization
   [500 words of detailed explanation]

2. Encryption
   [400 words of detailed explanation]

3. Input Validation
   [350 words...]

[Continues with full comprehensive coverage]
```

**Metrics:**
- Prompt: 17 words × 1.3 = 22 tokens
- Response: 1200 words × 1.3 = 1560 tokens
- Tool calls: 2 (web search, read docs)
- Round trips: 1
- Quality: 5/5
- Satisfaction: 4/5
- Notes: "Very comprehensive, maybe more than needed"

### Optimized (SAME scenario)

**Prompt:** (identical)
```
What are the current best practices for securing REST APIs?
I'm building a financial services application.
```

**Claude Response (excerpt):**
```
For financial APIs, key security practices:

1. Authentication: OAuth 2.0 + JWT tokens
2. Encryption: TLS 1.3, encrypt sensitive data at rest
3. Input validation: Whitelist, parameterized queries
4. Rate limiting: Prevent abuse

I can detail implementation, discuss compliance (PCI DSS),
or explain specific vulnerabilities if helpful.
```

**Metrics:**
- Prompt: 22 tokens (same)
- Response: 380 words × 1.3 = 494 tokens
- Tool calls: 1 (single web search)
- Round trips: 1
- Quality: 4.5/5
- Satisfaction: 5/5
- Notes: "Concise, actionable, financial context applied. Offers more if needed."

### Comparison
- Token reduction: (1560 - 494) / 1560 = 68.3%
- Quality maintained: 4.5/5.0 = 90% ✅
- Satisfaction improved: 5/4 = 125% ✅
- Behavioral difference: Clear progressive disclosure

## Sharing Your Results

If you run empirical tests, please share!

### What to Share
1. Your test report (`my_test_report.txt`)
2. Your methodology notes
3. Number of scenarios tested
4. Key findings
5. Any surprises or unexpected results

### Where to Share
- GitHub Issue: "Empirical Test Results - [Date]"
- Include: Platform (Claude.ai/CLI), model, date, # scenarios
- Attach your report file

### Why Share?
- Validates (or refutes) theoretical predictions
- Helps improve the skill
- Benefits other users
- Contributes to AI efficiency research

## Need Help?

- **Questions about procedure:** Re-read this guide
- **Questions about scenarios:** Check `test_scenarios.json`
- **Technical issues:** Check README.md
- **Skill not working:** Verify installation
- **Results seem wrong:** Review your methodology

Still stuck? Open a GitHub issue with:
- What you're trying to do
- What's happening
- What you expected
- Your setup (platform, model)

---

**Good luck with your testing! Real-world empirical data is incredibly valuable.**
