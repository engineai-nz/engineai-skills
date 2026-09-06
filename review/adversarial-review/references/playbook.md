# Adversarial Review playbook
# Adversarial Review

Dual-agent adversarial review system. Claude and Codex independently critique a document,
then findings are synthesised into a single prioritised report with evidence, action types,
and a send-ready author brief.

---

## Step 1: Detect and Classify the Document

Before reviewing, identify what kind of document this is. Read the full document, then classify:

| Doc Type | Review Focus |
|---|---|
| **PRD** | Architecture decisions, scope/MVP boundary, success metrics, user journeys, feasibility |
| **Architecture doc** | Trade-off analysis, missing ADRs, scalability, failure modes, technology fitness |
| **SOW** | Scope clarity, deliverable definitions, acceptance criteria, risk allocation, pricing |
| **Technical spec** | Implementation feasibility, edge cases, API contracts, performance, security |
| **GTM/Strategy doc** | Market assumptions, competitive gaps, metric methodology, execution plan |
| **AI feature spec** | Trust boundaries, eval methodology, fallback paths, cost/latency, data rights |

If the doc type is unclear, ask the user. Do not guess.

### AI-Generated Document Detection

Check for signs the document was AI-generated (Gemini, GPT, Claude). If detected, enable
**Proof Burden Mode** automatically (see Step 3). Signs to check:

- Buzzword density (3+ marketing metaphors that conflict with each other)
- Symmetrical structure (every section has the same number of bullets)
- Metrics without measurement methodology
- No unknowns/assumptions section
- Passive voice on hard problems ("must be implemented", "should be handled")
- Every question answered (greenfield docs should have open questions)
- Referenced input artifacts that don't exist

If AI-generation is detected, note it in the report header with the likely model and evidence.

---

## Step 2: Extract the Structured Model

Before critiquing, normalise the document into a structured model. Extract:

1. **Goals** - what the doc says it will achieve
2. **Assumptions** - stated and unstated
3. **Actors** - humans and systems involved
4. **Constraints** - technical, business, timeline
5. **Metrics** - success criteria and how they're measured
6. **Decisions** - technology, architecture, process choices made
7. **Dependencies** - external systems, teams, APIs, services
8. **Open questions** - things the doc acknowledges it doesn't know

If a category is empty, that's a finding. Flag missing sections explicitly.

---

## Step 3: Run the Review Framework

### Core Review Categories

Apply all seven categories to every document. Weight emphasis based on doc type.

**1. Architecture and Technology Fitness**
- Are technology choices justified with decision records?
- Are tools used for what they're actually designed to do?
- Are separate products/services conflated as one thing?
- Has an alternatives evaluation been done?
- Is the stack appropriate for the stated requirements?

**2. Metrics and Success Criteria**
- Does every metric have a measurement methodology?
- Is there a baseline to improve from?
- Are targets realistic (not 100%, not 0%)?
- Who evaluates success, and is the evaluator independent?
- Are aspirational outcomes separated from committed targets?

**3. Internal Contradictions**
- Do any sections conflict with each other?
- Does the MVP scope match the success criteria?
- Are phase boundaries consistent across sections?
- Do stated constraints conflict with stated goals?

**4. Edge Cases and Failure Modes**
- What happens when the primary path fails?
- Are rollback/compensation mechanisms defined?
- Is there a cost model or budget ceiling?
- Are rate limits, quotas, and resource contention addressed?
- Is there an error budget or acceptable failure rate?

**5. Scope and Phasing**
- Is the MVP actually minimal?
- Are all requirements tagged by phase?
- Could the MVP be split further?
- Are post-MVP features leaking into MVP requirements?

**6. AI-Generated Content Smell**
- Buzzword density and mixed metaphors
- Symmetrical structure (suspicious uniformity)
- Passive voice on hard implementation details
- Generic statements that apply to any project
- Missing unknowns section
- Metrics without methodology

**7. Missing Sections**
- Unknowns and assumptions
- Cost model
- Failure taxonomy
- Rollback strategy
- Measurement plan
- Rollout/migration plan

### Proof Burden Mode (Auto-enabled for AI-generated docs)

When active, force explicit answers for:
- Evaluation methodology for AI/agent components
- Fallback paths when AI components fail
- Human review points and approval gates
- Failure modes and recovery mechanisms
- Trust boundaries between automated and human decisions
- Cost and latency estimates per operation
- Data rights and privacy implications

### Traceability Pass

For each requirement, check:
- Is there a metric that measures whether this requirement is met?
- Is there an owner responsible for delivery?
- Are downstream implementation and test implications clear?

### Coverage Map

Build a coverage map showing which expected sections for this doc type are:
- **Present and strong**
- **Present but weak** (mentioned but underspecified)
- **Missing entirely**

---

## Step 4: Fire Codex as Independent Reviewer

After completing the Claude review, fire Codex via the codex companion for an independent pass.

Use this command pattern:

```
node "/home/duchats/.claude/plugins/cache/openai-codex/codex/1.0.0/scripts/codex-companion.mjs" task "YOUR_PROMPT_HERE"
```

The Codex prompt must include:
1. The full file path to the document
2. The detected doc type
3. All seven review categories (brief description of each)
4. Instruction to cite specific sections and line numbers
5. Instruction to be direct and not pull punches
6. If AI-generation was detected, mention the likely model

Do NOT share Claude's findings with Codex. The reviews must be independent.

Run Codex in the background while preparing the Claude findings for synthesis.

---

## Step 5: Synthesise Findings

Once both reviews are complete, merge into a single report.

### Finding Structure

Every finding must include:

| Field | Required | Description |
|---|---|---|
| **Title** | Yes | One-line summary |
| **Category** | Yes | Which of the 7 review categories |
| **Severity** | Yes | P0 (must fix before next step), P1 (serious gap), P2 (missing section), P3 (cosmetic) |
| **Action type** | Yes | `rewrite` / `add_section` / `resolve_contradiction` / `define_metric` / `narrow_scope` / `decision_needed` / `needs_stakeholder_input` |
| **Evidence** | Yes | Section name, line reference, direct quote |
| **Rationale** | Yes | Why this matters |
| **Suggested fix** | Yes | Specific recommendation |
| **Source** | Yes | `claude` / `codex` / `both` |
| **Confidence** | No | high / medium / low (use when reviewers disagree) |

### Reviewer Disagreement

When Claude and Codex disagree on a finding, surface it explicitly in a **Disagreements**
section. These are often the most valuable discussion points. Include both perspectives
and flag for human judgement.

### Deduplication Rules

- If both reviewers flag the same issue, merge into one finding with source: `both`
- If findings overlap but emphasise different aspects, keep both but cross-reference
- Codex-only findings that Claude missed should be highlighted as additive

### Prioritisation

Order findings: P0 first, then P1, P2, P3. Within each severity, order by action type
(decisions and rewrites before additions).

---

## Step 6: Generate Outputs

### Output 1: Full Internal Report

Write to `docs/adversarial-review-{type}-v{N}.md` in the project directory, where `{type}`
is the doc type slug (e.g., `prd`, `architecture`, `sow`, `spec`). This prevents collisions
when the same project has reviews of different documents.

Format:

```markdown
# Adversarial Review: {Doc Title} v{N}
**Date:** {date}
**Reviewers:** Claude (Opus), Codex (GPT)
**Doc Author:** {author}
**Doc Type:** {detected type}
**AI-Generated:** {Yes/No} ({model if detected}, {evidence})

## Verdict
{2-3 sentence overall assessment}

## Coverage Map
{Table showing present/weak/missing sections}

## P0 - Must Fix Before {Next Step}
{Findings with full evidence}

## P1 - Serious Gaps
{Findings}

## P2 - Missing Sections
{Findings}

## P3 - Cosmetic
{Findings}

## Reviewer Disagreements
{Where Claude and Codex differed}

## Questions for Author
{Separated from findings - these need answers, not fixes}

## Recommended Next Steps
{Ordered action list}
```

### Output 2: Author Brief

Generate a concise, send-ready summary for the document author. This is what gets
fired off via Telegram, Discord, or email. Structure:

```markdown
**{Doc Title} - Adversarial Review Summary**

Ran through Claude and Codex independently. Both converged on {N} core issues.
Full report available in docs/.

**Before you {next action}, these need resolving:**

1. {P0 finding 1 - 2-3 sentences}
2. {P0 finding 2 - 2-3 sentences}
3. {P0 finding 3 - 2-3 sentences}

**Other flags:** {One-line summaries of P1 findings}

{Encouraging closer that's honest about the doc's strengths}
```

Keep the author brief under 300 words. No jargon. No severity labels. Written for the
person who has to act on it, not the person who ran the review.

### Output 3: Structured JSON (Forward-compatible)

Write to `docs/adversarial-review-{type}-v{N}.json` alongside the markdown report.
This is forward-compatible with the future Review Ops Platform database schema.

```json
{
  "document": {
    "title": "",
    "path": "",
    "type": "",
    "author": "",
    "ai_generated": { "detected": false, "model": null, "evidence": [] }
  },
  "review": {
    "version": 1,
    "date": "",
    "reviewers": ["claude", "codex"],
    "verdict": ""
  },
  "findings": [
    {
      "id": "F001",
      "title": "",
      "category": "",
      "severity": "P0",
      "action_type": "",
      "evidence": { "section": "", "line": null, "quote": "" },
      "rationale": "",
      "suggested_fix": "",
      "source": "both",
      "confidence": "high",
      "status": "open"
    }
  ],
  "questions_for_author": [],
  "coverage_map": {},
  "disagreements": []
}
```

---

## Step 7: Re-review Mode

When reviewing a document that has been reviewed before (prior version exists in docs/),
automatically enter re-review mode.

### Re-review Process

1. Load the prior review report and JSON
2. Run the standard review against the updated document
3. Generate a diff report showing:
   - **Fixed** - findings from prior review that are now resolved
   - **Unchanged** - findings that still exist
   - **Regressed** - previously fixed issues that returned
   - **New** - findings not present in prior review
4. Update finding statuses in the JSON output
5. Include a progress summary: "X of Y prior findings resolved, Z new findings"

### Version Numbering

Increment the version number automatically: v1, v2, v3. All versions are kept.

---

## Step 8: Deliver via Telegram

After generating all three outputs, automatically send the author brief to Ben's Telegram
with the report files attached. Do not ask whether to send. Just send it.

**Telegram delivery:**

Use the `mcp__plugin_telegram_telegram__reply` tool with:
- `chat_id`: `7706509046`
- `text`: The author brief (Output 2), written in plain text (no markdownv2 formatting)
- `files`: Attach both report files as documents:
  - The full markdown report (`docs/adversarial-review-{type}-v{N}.md`)
  - The structured JSON (`docs/adversarial-review-{type}-v{N}.json`)

**Brief format for Telegram:**

Keep the same structure as Output 2 but append a file reference line at the end:

```
{Author brief content}

Reports attached: adversarial-review-{type}-v{N}.md + .json
```

**If Telegram delivery fails:**
- Note the failure in the response
- The files are still written to docs/ so the user can send manually
- Do not retry automatically

---

## Principles

- **Independence matters.** Never share Claude's findings with Codex or vice versa before synthesis.
- **Evidence over opinion.** Every finding must cite a specific section, line, or quote.
- **Questions are not findings.** Separate things that need answers from things that need fixes.
- **The author brief is the product.** The full report is for the record. The brief is what drives action.
- **Be direct.** Do not soften findings. Do not use hedge words. State what's wrong and what to do about it.
- **Credit what works.** Note strengths in the verdict. A review that only criticises is less credible.
