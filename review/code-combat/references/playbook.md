# Code Combat playbook
# Code Combat

Multi-round adversarial negotiation protocol between AI agents. Takes over after
`/adversarial-review` produces findings. Runs structured debate rounds until the
execution model is locked and all critical findings are resolved.

The goal is better build docs, not winning arguments.

---

## Step 1: Detect and Confirm

### Auto-Detection

Code Combat should be suggested (not auto-started) when ALL of these are true:
- An adversarial review exists in the project (`docs/adversarial-review-*.json`)
- The user pastes or receives (via Telegram/Discord) a response from another AI agent
- The response references or responds to review findings

### Confirmation

Always ask before engaging:

```
Looks like a rebuttal from {opponent}. Want me to run Code Combat?
I'll load the prior findings, fact-check their claims with Codex, and draft a response.
```

Do NOT auto-engage. The user may want to read the response themselves first or handle
it outside the skill.

### Session Initialisation

On first round, create the combat workspace:
- `docs/code-combat/` directory
- `docs/code-combat/ledger.json` (resolution ledger)
- Round responses will be numbered: `round-{N}-response.md`

---

## Step 2: Load Context

### From Adversarial Review

Load the most recent adversarial review JSON (`docs/adversarial-review-*.json`).
Extract:
- All findings with their IDs, severity, category, and status
- Questions for author
- Coverage map
- Reviewer disagreements

### From Resolution Ledger

If `docs/code-combat/ledger.json` exists (not the first round), load it to see:
- Which findings are already resolved
- Which are contested
- What was agreed in prior rounds
- What's still open

### From Prior Rounds

Read any existing `docs/code-combat/round-{N}-response.md` files to maintain
continuity. Do not re-argue settled points.

---

## Step 3: Parse the Rebuttal

Read the opponent's response and classify every distinct point into one of:

| Classification | Description | How to Handle |
|---|---|---|
| **Concession** | Opponent accepts a finding | Mark finding as resolved in ledger |
| **Defence** | Opponent argues a finding is wrong | Evaluate the evidence. Concede or counter. |
| **Counter-proposal** | Opponent offers an alternative solution | Evaluate technical merit. Accept, modify, or reject. |
| **New information** | Context we didn't have (e.g., a deliberate constraint) | Evaluate whether it changes our findings. Update if valid. |
| **New question** | Opponent asks for specific implementation guidance | Answer concretely with schemas, code, or patterns. |
| **Deflection** | Opponent restates the claim without new evidence | Hold firm. Re-state the specific evidence they haven't addressed. |
| **Scope shift** | Opponent changes the subject or introduces new topics | Acknowledge but redirect to open findings first. |

Build a structured map of: `finding_id -> classification -> evidence`.

---

## Step 4: Fire Codex as Fact-Checker

For each round, fire Codex via the codex companion to independently verify the
opponent's factual claims.

Use this command pattern:

```
node "/home/duchats/.claude/plugins/cache/openai-codex/codex/1.0.0/scripts/codex-companion.mjs" task "YOUR_PROMPT_HERE"
```

### What Codex Checks

- **Technical claims:** "Vercel Edge has a 25s limit" -- verify against actual docs
- **API capabilities:** "Supabase Management API supports X" -- verify
- **Framework features:** "Vercel AI SDK v6 supports Y" -- verify
- **Counter-proposals:** Is the proposed solution technically sound?
- **New information:** Are the constraints the opponent cites real?

### Codex Prompt Template

The prompt must include:
1. The opponent's specific claims (quoted, with attribution)
2. Instruction to verify each claim against official documentation
3. Instruction to flag any claims that are incorrect, outdated, or misleading
4. Instruction to be concise: one verdict per claim (confirmed/incorrect/partially correct)

### Independence

Do NOT share Claude's evaluation with Codex. Codex fact-checks the opponent's claims
independently. Claude evaluates the strategic merit. Merge during synthesis.

Run Codex in the background while Claude evaluates the response.

---

## Step 5: Evaluate and Draft Response

### Evaluation Principles

1. **Concede fast.** If they're right, say so in one line. Don't dig in on weak positions.
2. **Propose, don't just critique.** Every "this is missing" must come with a concrete
   suggestion: a schema, a pattern, a code sample, a specific recommendation.
3. **Hold with evidence.** When holding firm, cite the specific evidence they haven't
   addressed. "You've restated the claim but haven't addressed [specific gap]."
4. **Accept new context.** If the opponent provides legitimate project context we didn't
   have (e.g., a deliberate constraint), update our position. Note: context changes
   the finding, but doesn't automatically resolve it.
5. **Answer implementation questions directly.** When the opponent asks "how should we
   do X?", give a concrete answer with code. This is where the debate becomes productive.

### Tone Calibration

- **Early rounds (open P0s):** Direct, evidence-based, push for specifics. Not aggressive,
  but firm. The goal is to surface real gaps.
- **Middle rounds (P0s resolving, P1s in progress):** Collaborative. Build on their
  proposals. Offer refinements rather than rejections.
- **Late rounds (convergence):** Constructive. Focus on minor refinements and verification.
  Signal when we're close to done.

The user may explicitly request a tone shift at any point. Follow their lead.

### Opponent Model Awareness

Note which model the opponent is running. Different models have characteristic patterns:

| Model | Common Pattern | Calibration |
|---|---|---|
| **Gemini** | Confident, self-validating output. Marketing language. Symmetrical structure. | Push harder on evidence. Ask for specifics behind claims. |
| **GPT** | Over-qualified, hedging. May add unnecessary caveats. | Can accept broader statements. Watch for buried concessions. |
| **Claude** | Structured, thorough. May over-engineer solutions. | Focus on whether the proposed solution matches the actual need. |

This is a heuristic, not a rule. Evaluate the content, not the model.

---

## Step 6: Generate Round Response

### File Format

Write to `docs/code-combat/round-{N}-response.md`.

### Response Structure

```markdown
# Code Combat: Round {N}
**Date:** {date}
**From:** Claude (Opus) + Codex (GPT)
**To:** {opponent name} ({opponent model})
**Project:** {project name}

## Status Dashboard
| Metric | Count |
|---|---|
| Total findings | {N} |
| Resolved | {N} |
| In progress | {N} |
| Open | {N} |
| P0s remaining | {N} |

## Concessions (What We Accept)
{Points where the opponent is right or provides valid new context}

## Holds (What Stands)
{Points where the evidence hasn't been addressed, with specific citations}

## Counters (Where We Disagree)
{Points where we push back, with evidence and rationale}

## Proposals (Concrete Solutions)
{Schemas, code, patterns, protocols offered in response to their questions
or to resolve contested findings}

## Codex Fact-Check Results
{Independent verification of opponent's technical claims}

## What's Left
{Ordered list of remaining open items before convergence}
```

### Length

Round responses should be comprehensive but not padded. If a finding is resolved,
one line is enough. If a new schema is needed, include the full schema. Let the
content dictate the length.

---

## Step 7: Update Resolution Ledger

After each round, update `docs/code-combat/ledger.json`.

### Ledger Schema

```json
{
  "project": "",
  "opponent": { "name": "", "model": "" },
  "source_review": "docs/adversarial-review-{type}-v{N}.json",
  "rounds_completed": 0,
  "status": "active",
  "findings": [
    {
      "id": "F001",
      "title": "",
      "severity": "P0",
      "status": "open",
      "resolution_round": null,
      "resolution_type": null,
      "resolution_summary": "",
      "history": [
        {
          "round": 1,
          "action": "opponent_conceded",
          "detail": "Accepted provisioning chain needs saga pattern"
        }
      ]
    }
  ],
  "new_agreements": [
    {
      "round": 2,
      "topic": "task_ledger schema",
      "detail": "Schema agreed with tool_cache, effects_log, checkpoint fields",
      "artifacts": ["task_ledger SQL", "HandoffEnvelopeSchema Zod"]
    }
  ],
  "open_questions": [],
  "convergence": {
    "reached": false,
    "round": null,
    "summary": ""
  }
}
```

### Status Values for Findings

| Status | Meaning |
|---|---|
| `open` | Not yet addressed by opponent |
| `contested` | Opponent disagrees, debate ongoing |
| `in_progress` | Opponent is working on a fix/response |
| `resolved` | Addressed with concrete evidence or implementation |
| `conceded_by_us` | We accepted the opponent's defence |
| `superseded` | Replaced by a different approach agreed in debate |
| `deferred` | Both sides agree to address later (with rationale) |

---

## Step 8: Deliver via Telegram

After generating the round response and updating the ledger, send via Telegram.

### Delivery Format

Use the `mcp__plugin_telegram_telegram__reply` tool with:
- `chat_id`: `7706509046`
- `text`: Short summary (3-5 lines: what was conceded, what's held, what's proposed,
  how many findings remain)
- `files`: Attach the round response `.md` file

### Summary Template

```
Code Combat Round {N} response attached.

Conceded: {N items}. Held: {N items}. Proposed: {list}.
Findings: {resolved}/{total} resolved. {P0s remaining} P0s left.
{One line on what's needed next from the opponent.}
```

### If Telegram Delivery Fails

Note the failure. Files are in `docs/code-combat/` regardless. User can send manually.

---

## Step 9: Detect Convergence

### Convergence Criteria

The combat is complete when ALL of the following are true:
- All P0 findings are resolved or have concrete implementation plans with schemas/code
- All P1 findings are resolved, deferred with rationale, or have clear owners
- The opponent has produced updated documentation reflecting agreements
- A verification pass confirms the updated doc accurately captures what was agreed

### Convergence Actions

When convergence is detected:

1. **Generate debate summary.** Write to `docs/code-combat/summary.md`:

```markdown
# Code Combat Summary: {Project}
**Date:** {date}
**Rounds:** {N}
**Participants:** Claude (Opus) + Codex (GPT) vs {opponent} ({model})

## What Changed
| Finding | Original Issue | Resolution | Round |
|---|---|---|---|
| F001 | No ADR | 5 ADRs written with trade-offs | Round 3 |
| F002 | ... | ... | ... |

## New Agreements (Not in Original Review)
{Things that emerged from the debate that weren't in the original findings}

## Deferred Items
{Items both sides agreed to address later, with rationale and target phase}

## Key Patterns Established
{Reusable patterns that emerged: saga, outbox, sealed envelope, etc.}

## Process Notes
{What worked, what didn't, how many rounds each severity level took}
```

2. **Update the resolution ledger** with `convergence.reached = true`.

3. **Notify via Telegram** with summary attached.

4. **Suggest next steps:** "Architecture locked. Ready for epics/stories/implementation."

---

## Step 10: Time-Boxing

### Round Limits

If a specific finding has been contested for **3+ rounds** without progress:
- Flag it as a **taste decision** that needs human judgement
- Present both positions clearly
- Ask the user to make the call
- Do not continue arguing. Three rounds of the same argument means the AIs disagree
  on something that requires human context.

### Session Limits

If the overall combat exceeds **7 rounds** without convergence:
- Generate a progress report showing what's resolved and what's stuck
- Recommend the user schedule a sync with the opponent's operator
- The AIs have done their job. Remaining items are likely judgement calls.

---

## Principles

- **The goal is convergence, not victory.** Better docs win. Ego doesn't.
- **Concede fast, propose faster.** Every critique should come with a solution.
- **Track everything.** The ledger is the source of truth. Chat is ephemeral.
- **Independence matters.** Codex fact-checks independently every round.
- **Tone follows progress.** Adversarial early, collaborative late.
- **Time-box disagreements.** Three rounds on the same point means humans need to decide.
- **The opponent is a collaborator with different biases.** Their model sees things ours doesn't. That's the point.
- **Deliver as files.** Responses are too long for inline messages. Always `.md` via Telegram.
