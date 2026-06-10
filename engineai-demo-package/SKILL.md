---
name: engineai-demo-package
description: Interactive session that designs AND auto-scaffolds a full synthetic client demo, then emits a filled runbook. Drives the whole arc — business analysis → stakeholder roles → use-case design → synthetic-first data → HYBRID AUTO-SCAFFOLD (Playwright scrapers + MCP server + mocks + report-build PDF + email send) → branded PDF into the client inbox → Telegram + a PORTABLE agent (Leo or a personal Hermes via a config switch) → reliability hardening → real-path rehearsal → emitted runbook. Same spine for every client. No slides. They drive. Use when building, scaffolding, rehearsing, or hardening an EngineAI client demo, or when someone says "build a demo for [client]", "spin up a synthetic demo", "demo package", "hand them the phone".
type: procedural
title: EngineAI Demo Package — Interactive Synthetic Demo Builder
tags: [engineai, demo, sales, mcp, hermes, playwright, pdf, email, telegram, runbook, portability, client-facing, interactive, scaffold]
---

# EngineAI Demo Package

## The Core Principle

You don't pitch. You hand them the phone.

Every minute spent talking is a minute they could have spent *using the future of their business.* By the end of the meeting the client has typed questions, received answers, watched a branded PDF land in their own inbox, seen data update live, and had an automated alert fire — all against data that looks like theirs, in a channel that feels like their team's.

They don't ask "could this work for us?" They ask "when can we go live?"

## How to use this skill

This is an **interactive creation session**, not a document you read once. You (the agent) drive the build conversationally — ask one focused question at a time, scaffold artefacts as you go, verify each piece, and finish by emitting a filled runbook anyone can follow to re-run the demo cold. Work the stages in order; each ends with a go/no-go.

**Start at Stage 0 every time.** The detail for the heavy stages lives in four companion references (read them when you reach the stage that points to them):

- `references/scaffold-manifest.md` — the manifest schema, the file tree the auto-scaffold emits, generalized skeletons, the portable `target_agent` switch, and the runbook-emission step. **This is the source of truth for file layout and tool names.**
- `references/report-pdf-email-pattern.md` — HTML→PDF branded report, brand-scrape, and the email-with-attachment send path.
- `references/demo-reliability-hardening.md` — the reliability playbook the in-room experience depends on.
- `references/browser-automation-demo-pattern.md` — the Playwright scraper pipeline + mock→live switching (CDS worked example).

## The workflow spine

```
Stage 0  Interactive driver        → you, asking, building, confirming
Stage 1  Business analysis         → who they are, what hurts
Stage 2  Stakeholder roles         → personas + the question each will ask
Stage 3  Use-case design           → the demo moments, mapped to people
Stage 4  Data strategy             → synthetic-first (mock), real optional
Stage 5  HYBRID AUTO-SCAFFOLD      → scrapers + MCP + mocks + PDF + email, generated
Stage 6  Delivery wiring           → branded PDF lands in the client inbox
Stage 7  Channel + portable agent  → Telegram + Leo / personal Hermes via target_agent
Stage 8  Reliability hardening     → make the real (message→tool) path bulletproof
Stage 9  Rehearse the real path    → dry-run end to end, on the target you'll demo on
Stage 10 Emit the runbook          → fill the engine-ai-os template, write to disk
```

First full build: 4–6 hours. Repeat builds: 2–3 hours, because the scaffold is generated, not hand-written. All artefacts live under `~/.hermes/demos/{{slug}}/`.

---

## Stage 0: The interactive driver

You run this session. Behave like a build partner, not a form.

**Rules of the room:**
1. Ask **one question at a time.** Wait for the answer.
2. After each stage, **show the artefact** and ask "lock this and move on?"
3. **Scaffold as you go** — build incrementally so each piece is verifiable (Stage 5d).
4. **Default to synthetic.** Real data is opt-in (Stage 4).
5. **Track the spine.** Keep a running done/pending checklist so the human always knows where you are.
6. **Confirm the portability target early** (Stage 7): is this demo driven by **Leo** (EngineAI's shared Chief-of-Staff Hermes) or a **personal Hermes** (e.g. Gilfoyle)? It changes config bindings, not architecture.

Open with:

> "Let's build a demo. Who's the client, and have you met them or are we going in cold? I'll take it one step at a time, scaffold as we go, and hand you a runbook at the end. First: which agent runs it — Leo, or a personal Hermes?"

---

## Stage 1: Business analysis

Gather just enough to make the data feel lived-in (website, LinkedIn, CRM, meeting notes).

| Data point | Source | Why |
|---|---|---|
| Company, industry, size | Website, LinkedIn | Shapes data realism |
| Key people + roles | LinkedIn, CRM, notes | Defines stakeholder personas |
| Core processes | Website, industry knowledge | Defines tools needed |
| Pain points | Notes, industry patterns | Defines demo triggers |
| Tools they already use | Research | Don't rebuild what they have |
| Their language / terminology | Website, proposals | Makes data feel authentic |
| The **"no-API" website** | Direct question | Your highest-leverage demo moment |

Always ask: **"What website does someone on their team copy-paste from every day?"** That answer becomes a Playwright scraper target (Stage 5). Produce a short research summary (see Appendix A for the shape), confirm, move on.

---

## Stage 2: Stakeholder roles

One persona per person in the room. Each persona exists to own a demo moment.

```yaml
persona:
  name: "[Name]"
  role: "[Title]"
  concerns: ["[what keeps them up at night]", "[what metrics they track]"]
  language: "[how they talk about their work]"
  demo_moment: "[the question that makes them lean forward]"
  agent_tone: "[how the agent should talk to them]"
```

Map top-down: Director (big picture) → Operator (detail) → Decision Maker (power / the email moment) → Field person (authenticity) → Specialist (depth / the browser moment). Fit personas to who's actually attending.

---

## Stage 3: Use-case design

For each persona, design the exchange: a question + the tool that answers it + the visible payoff. Use the canonical tool names (`{{slug}}_brief`, `{{slug}}_email_report`, plus any client-specific tools) — see `scaffold-manifest.md`.

| Moment | Persona | Question they type | Tool called | Visible payoff |
|---|---|---|---|---|
| Big picture | Director | "Status on everything?" | `{{slug}}_status` | Whole business in 30s |
| Detail | Operator | "What's expiring?" | `{{slug}}_check` | Specific, actionable |
| Power (finale) | Decision Maker | "Email [person] the [project] brief" | `{{slug}}_email_report` | **Branded PDF in their inbox** |
| Depth | Specialist | "[Deliverable] for [project]" | `{{slug}}_brief` | Screenshots from "no-API" portals |
| Unprompted | All | (cron fires) | scheduled job | "I didn't ask for that" |

**Golden rule:** every datum you create later must map to a moment here. If it doesn't serve a question someone will ask, cut it. The **Power moment is the centrepiece** — it ends with a branded PDF landing in the client's real inbox (Stages 5c/6).

---

## Stage 4: Data strategy — synthetic first

**Default: 100% synthetic, mock mode.** Faster, safer, zero credential/PII risk, and you control the tension. The scaffold runs **`PLAYWRIGHT_MODE=mock`** against generated mock-HTML portals — no logins. The real path is a config flip, not a rebuild: **`PLAYWRIGHT_MODE=live`** + credentials (see `report-pdf-email-pattern.md` and `browser-automation-demo-pattern.md`). Only go real when the client hands you a file in the room or post-sale.

Map synthetic content to the client's actual business and **build in tension** — expired permits, over-budget jobs, looming deadlines. Perfect data is boring. Pre-seed a week of history so it feels lived-in. (If a richer demo needs a backing database, a Supabase schema `{{slug}}_demo` is an optional extension — but the proven spine is mock-HTML portals scraped by Playwright.)

| Category | What to create | Construction e.g. | Rugby e.g. | Retail e.g. |
|---|---|---|---|---|
| Entities | 4–6 current | Active jobs | Season matches | Product lines |
| Pipeline | 4–6 upcoming | Tenders | Recruitment targets | Launches |
| Compliance | 10–15, status mix | H&S docs | Injury reports | Quality checks |
| Flags | 2–3 issues | Expired permits | Injury risks | Stockouts |

---

## Stage 5: Hybrid auto-scaffold

The heart of the upgrade. You **generate the demo from a manifest** instead of hand-writing files; the human fills the parts that carry the client's specific tension.

> **Read `references/scaffold-manifest.md` first.** It owns the manifest schema, the exact file tree, every file skeleton, and the generation checklist. The summary below is orientation only.

### The split

| Auto-generated from manifest | Hand-tuned per client |
|---|---|
| `playwright-utils.mjs` sentinel lib | per-source `extract*()` logic |
| scraper scaffolds (one per source) | mock-HTML look & feel |
| `{{slug}}-brief.mjs` orchestrator | which portals to mock |
| `report-build.mjs` → PDF | report layout / branding |
| MCP `server.py` + tool stubs | tool business logic |
| email-send path | recipient + copy |
| `agent-config/target.json` | persona prompts |

### The file tree it produces (canonical — matches `scaffold-manifest.md` §1)

```
~/.hermes/demos/{{slug}}/
├── playwright-scripts/
│   ├── lib/playwright-utils.mjs       # sentinel contract + extract* TODOs
│   ├── {{source}}-scrape.mjs   (×N)   # one scraper per source
│   ├── {{slug}}-brief.mjs             # orchestrator (execFileAsync + Promise.all)
│   ├── report-build.mjs               # HTML→PDF branded report
│   ├── brand-scrape.mjs               # brand harvester (run once at scaffold time)
│   ├── mocks/{{source}}-mock.html (×N)# offline demo data, zero credentials
│   ├── output/ · briefs/ · reports/ · assets/
│   └── package.json
├── mcp-server/server.py               # tool defs + sentinel parsing + email send
├── agent-config/target.json           # PORTABLE switch payload (Stage 7)
└── RUNBOOK.md                         # local copy; canonical in engine-ai-os/Runbooks

~/.hermes/scripts/demo-model.sh        # SHARED model toggle (created once per host)
```

### 5a. MCP server + tools

The scaffold stubs the MCP `server.py`; you fill the logic. Tool names follow `{{slug}}_{{tool}}` (e.g. `{{slug}}_brief`, `{{slug}}_email_report`, plus client-specific `{{slug}}_status` / `{{slug}}_check`). The exact `server.py` skeleton, sentinel parsing, and the node-binary resolution live in `scaffold-manifest.md` — use it as the authority rather than typing boilerplate from memory.

### 5b. Browser automation (the "no-API" moment)

For each copy-paste website from Stage 1, generate a mock HTML page (mock mode) and a Playwright scraper (retina @2× DPR, headless Chromium, DOM→JSON + full-page screenshot). The orchestrator runs all scrapers **truly in parallel** (`execFileAsync` + `Promise.all` — not sync `execSync`, which serialises) and compiles a structured brief. Flip real with `PLAYWRIGHT_MODE=live`. See `references/browser-automation-demo-pattern.md`.

### 5c. Report → PDF → email (the finale, one tool)

The closer: a single `{{slug}}_email_report` tool that **builds a branded PDF and sends it**, so the client watches it land in their inbox.

```
Decision Maker types: "Email Daniel the Westgate site brief."
  → agent calls {{slug}}_email_report
      → runs the brief orchestrator (data + Playwright screenshots)
      → renders client-branded HTML → prints to PDF (report-build.mjs)
      → emails the PDF as an attachment from clientdemo.engineai@gmail.com / AgentMail
  → client's phone buzzes. Branded PDF. Their logo. Their data. Real inbox.
```

> **Read `references/report-pdf-email-pattern.md`** for the HTML→PDF technique, brand-scrape, and the attachment send. **Load-bearing gotcha:** attachments must go through the Gmail **Python client** (`messages().send(body={'raw':…})`), never a `gws --attach` argv path — a PDF-sized payload blows the OS arg-length limit. The `{{slug}}_email_report` tool description must be **directive** ("ALWAYS use this when asked to email/send a report; do NOT hand-compose") or weaker models freelance a plain-text email instead.

### 5d. Verify each piece as it's generated

Don't generate the whole tree then test. After each module: run it once, confirm output. Tools → call each against mock data. Scrapers → run with an arg, check JSON + screenshot. Report → build one PDF, open it. Email → send one **test to yourself**, confirm delivery. Incremental verification is what makes Stage 9 a formality.

---

## Stage 6: Delivery wiring

Wire the finale so the branded PDF reliably reaches an inbox.

- **Demo mailbox:** `clientdemo.engineai@gmail.com`, one label per client (`CDS_Demo`, `NHR_Demo`); pre-seed 3–5 realistic emails so it looks lived-in. (Cleaner option: an AgentMail inbox per client.)
- **Safe-recipient rule:** the `email_report` tool's `default_recipients` is an **internal address** (e.g. `joe@engineai.co.nz`) — it **NEVER** sends to the client until explicitly told. Test sends go to you.
- **The reveal:** have the inbox open on a second screen. "Look — the agent built that PDF and sent it. Real build, real send, real email."

Confirm delivery end-to-end before moving on. A PDF that doesn't arrive is the worst possible demo failure (Stage 8).

---

## Stage 7: Channel + portable agent

### Telegram channels

| Channel | Purpose | Who sees it |
|---|---|---|
| `[Client] Ops` | Main — Q&A, status, pipeline | All stakeholders |
| `[Client] [Domain]` | Secondary — HSE / analytics / compliance | Subset |

### Portability switch — `target_agent` (canonical)

The same demo runs on either host. Decide once in Stage 0; the scaffold writes `agent-config/target.json`:

```json
{ "target_agent": "leo" }      // "leo" | "gilfoyle"  (any personal Hermes id)
```

| Concern | **leo** (shared / managed) | **gilfoyle** (personal Hermes) |
|---|---|---|
| When | EngineAI-run demos, shared infra | Personal instance, offline-safe, travel |
| MCP registration | Leo's `mcp_config_path` | local Hermes config |
| Channel + persona | "Leo — EngineAI Chief of Staff" | "Gilfoyle" (personal voice) |
| Secrets | Leo's managed store | local `.env` |
| Model toggle | Leo's gateway label | local `demo-model.sh` + local launchd label |

**Architecture is identical across targets** — only MCP registration path, channel, persona, and secret store change. The wiring step reads `target_agent` and binds those four. Migrating personal→Leo for delivery: flip `target_agent`, re-register the MCP server at Leo's path, repoint the channel, move credentials, then re-run the real-path test on Leo. See `scaffold-manifest.md` §8.

### Model switching for the demo (in-chat, session-scoped)

The demo runs on a **stronger, more obedient model** than the daily driver (see Stage 8). Switch it **in the chat** — never at the shell:

```
/model {{DEMO_MODEL}}     ← before the demo (e.g. /model deepseek/deepseek-v4-pro)
/model {{DAILY_MODEL}}    ← after (e.g. /model deepseek/deepseek-v4-flash)
```

A shared `~/.hermes/scripts/demo-model.sh {pro|flash|status}` exists as a **terminal-only** fallback — but **never paste it into the demo chat**: it restarts the gateway and kills the live session.

---

## Stage 8: Reliability hardening

A demo that breaks in the room costs the deal. Harden the **real path** (a chat message → the model firing the right tool) before you rehearse.

> **Read `references/demo-reliability-hardening.md`** for the why behind each item (grounded in real CDS failures). The playbook is these six, in order of impact:

1. **Switch the model in-chat, session-scoped — never at the shell.** `/model {{DEMO_MODEL}}` before, `/model {{DAILY_MODEL}}` after. Never paste `launchctl`/`hermes`/gateway-restart commands into the demo chat — that reboots the gateway and kills the session.
2. **Add the behaviour guardrail** to the agent's standing instructions, verbatim: *"For a demo request, call the matching tool, present the result, and STOP — no terminal commands, no file edits, no offering extra engineering. This is a client-facing path."* (Stops over-eager models freelancing on stage.)
3. **Point the fallback model at something sane** (e.g. Flash) — never a free/over-eager model, or a mid-demo hiccup degrades into chaos.
4. **Test the REAL path.** Send an actual chat message and confirm the model fires the right tool ("give me the GeoTech brief" → `{{slug}}_brief`). Calling the MCP tool directly proves nothing about message→tool routing — this is the true failure point.
5. **Pre-warm dependencies.** Install/prime browsers, auth, and caches *before* the room, so there's nothing for the agent to "helpfully fix" mid-demo. Run one dummy query 15 min before.
6. **Put the wow in an emailed PDF, not inline chat media.** Inline images are unreliable on weaker models (they silently drop or mangle the attach directive). Deliver the branded artifact via `{{slug}}_email_report`.

---

## Stage 9: Rehearse the real path

Dry-run the entire demo end-to-end, **on the agent target you'll actually use** (Leo or personal Hermes), as the client will experience it — typing into Telegram, watching the inbox, waiting for the cron. Confirm the demo session is on `{{DEMO_MODEL}}` first (`/model …`).

- **Part 0 — Handover:** "Here's the phone. We loaded a demo of your business — synthetic data, real tools. Ask it anything." Then stop talking.
- **Part 1 — Director:** "Status on everything?" / "Pipeline?" / "Red flags?"
- **Part 2 — Operator:** "Who's on [project]?" / "What's expiring?"
- **Part 3 — Decision Maker (the finale):** "Email [person] the [project] brief." → branded PDF builds → lands in inbox → phone buzzes. *Rehearse this until flawless; re-run it twice — the PDF-email path is the one that must never miss.*
- **Part 4 — Field person:** field input accepted, escalated.
- **Part 5 — Specialist (depth):** "[Deliverable] for [project]." → parallel browser sessions → screenshots land. "That ran N browser sessions in parallel. No API. Just the browser."
- **Part 6 — Unprompted:** cron fires. "I didn't send that. It checks every morning."
- **Part 7 — Secondary channel:** a second cron fires in the domain channel.
- **Part 8 — Bring your data:** "That was synthetic. Everything you used is real — real tools, real email, real PDF. Give me one spreadsheet and 10 minutes."

Run the Stage 8 checks first (real-path test green, deps warm, on the correct target). Fix anything amber before the room.

---

## Stage 10: Emit the runbook

Close the session by **filling the engine-ai-os runbook template** and writing it both locally (`~/.hermes/demos/{{slug}}/RUNBOOK.md`) and to the canonical repo. This is the deliverable that lets anyone — Joe, Leo, a future teammate — re-run the demo cold.

- **Template:** `engine-ai-os/Runbooks/live-agent-demo-template.md` (gold-standard worked example: `live-agent-demo-cds-example.md`).
- **Emit target:** `engine-ai-os/Runbooks/{{skill-folder-or-client-slug}}.md`, then link it from `Runbooks/README.md`. (Naming convention: runbook filename = the demo's slug.)
- **Placeholder → data mapping** and the commit step are spelled out in `scaffold-manifest.md` §9.

Fill it with the concrete values you gathered: client + attendees + goal; personas + their demo-moment questions; the data/mock map; the scaffold inventory (from the manifest); the finale wiring (report template, recipient, expected PDF); channels + `target_agent`; crons; the exact in-chat model commands (`/model {{DEMO_MODEL}}` ↔ `/model {{DAILY_MODEL}}`); the Stage 8 reliability checklist; and the Parts 0–8 script verbatim. Show it to the human, confirm, commit. That ends the session.

### Pre-demo checklist (goes into the runbook)

**T-24h**
- [ ] Business analysis, personas, synthetic data with tension
- [ ] Scaffold generated; each module verified (5d)
- [ ] Playwright mocks + scrapers run clean, screenshots sharp
- [ ] `{{slug}}_brief` and **`{{slug}}_email_report` tested** — one branded PDF built, opened, and **delivered to the test inbox**
- [ ] Demo Gmail labelled + pre-seeded; two Telegram channels created
- [ ] `agent-config/target.json` set; MCP server registered at the target
- [ ] Crons tested (run once, verify format)
- [ ] Behaviour guardrail in the agent's standing instructions; fallback model sane

**T-15min**
- [ ] Demo session switched to `{{DEMO_MODEL}}` in-chat (`/model …`)
- [ ] **Real-path test passed** (a chat message fired the right tool)
- [ ] Deps warm — browsers primed, one dummy query run
- [ ] Demo Gmail open on a second screen (for the inbox reveal)
- [ ] Phone charged, Telegram open, channels visible
- [ ] Demoing on the correct `target_agent`

---

## The engagement model

The demo framework is also the pricing ladder:

| Stage | What happens | Price |
|---|---|---|
| **Demo** | Full synthetic demo. 2-hour meeting. Hand them the phone. | Free (lead gen) |
| **Build** | 2–3 days: real MCP server + agent, real data wired. | $5k–10k |
| **Run** | Monthly: runtime, crons, email, support, iteration. | $500–2k/mo |
| **Scale** | Dedicated instance, SLA, custom integrations, fleet. | $3k+/mo |

The demo is the only upfront investment. They've used the product before they've paid a cent.

---

## Appendix A: CDS worked example

### Research summary

```
Company:   CDS Civil — trenchless construction (directional drilling, pipe jacking, micro-tunnelling, sliplining)
Location:  Auckland (Albany, Pakuranga, Hobsonville, Whenuapai, Silverdale)   Size: Tier-2 civil contractor
Key people:
- Daniel — Director/Owner (big picture, profit, clients)
- Anthony Clough — Director (ops, risk, compliance)
- Lisa Souter — Ops Manager (daily ops, HSE, crew scheduling)
- Scuff — Site Supervisor (field, crew safety, plant)
- Mark Carmody — Head Engineer (specs, method statements, geotech)
Pain: multiple Auckland projects; H&S compliance (permits, RAMS, SWMS); tender pipeline; crew allocation; budget; field↔office.
No-API websites: NZ Geotechnical Database + Auckland Council GIS + supplier portals.
```

### Stakeholder personas

```yaml
daniel:  {role: Director/Owner,  demo_moment: "Three messages = his entire business", tone: "Strategic, flag risks"}
anthony: {role: Director (Ops),  demo_moment: "Email Daniel a branded site brief",    tone: "Operational, action-oriented"}
lisa:    {role: Ops Manager,     demo_moment: "Toolbox briefing appears automatically", tone: "Supportive, checklist-friendly"}
scuff:   {role: Site Supervisor, demo_moment: "Site update → ops board reflects it",    tone: "Blunt, field-level"}
mark:    {role: Head Engineer,   demo_moment: "GeoTech brief from no-API portals",      tone: "Technical, precise"}
```

### Synthetic data (6 projects, with tension)

| Project | Type | Status | Tension |
|---|---|---|---|
| Albany Main Trunk | Directional drilling | Active | RAMS expiring June 14 |
| Pakuranga Rising Main | Pipe jacking | Active | Healthy — on schedule |
| Hobsonville Stormwater | Micro-tunnelling | Active | 8% over + expired permit |
| Whenuapai Water Main | Sliplining | Mobilising | Drafts pending |
| Silverdale Sewer Upgrade | Open cut + trenchless | Pending | Tender won, signing imminent |
| Kumeu Water Reticulation | Directional drilling | Completed | Closed |

### Wiring (the real build)

- **Tools:** `cds_geotech_brief`, `cds_consent_status`, `cds_supplier_check`, `cds_email_report` (the canonical `{{slug}}_…` pattern).
- **Browser:** parallel headless Chromium against synthetic NZGD / Council GIS / supplier portals, retina screenshots, ~2–3.5s.
- **Finale:** "Email Daniel the Westgate site brief" → `cds_email_report` renders a CDS-branded PDF → delivered to the demo inbox → phone buzzes. Artifact: `~/.hermes/demos/cds/reports/CDS-GeoTech-Brief-westgate-trunk-sewer.pdf`.
- **Model commands:** `/model deepseek/deepseek-v4-pro` (demo) ↔ `/model deepseek/deepseek-v4-flash` (daily).
- **Channels:** CDS Operations (all 5 + agent) · CDS HSE & Compliance (Lisa, Anthony, Mark + agent).
- **Backup repo:** `github.com/Tradie-AI-2000/wardo-hermes`. **Runbook:** `engine-ai-os/Runbooks/live-agent-demo-cds-example.md`.

---

## Appendix B: Blank demo template

Use this to kick off any build; Stage 0 walks you through filling it conversationally.

```
Research:   Company [name] · Industry [x] · Location [x] · Size [x]
            Key people: [Name] — [Role]. [Concerns].
            Pain points: [...]   No-API website: [the copy-paste site]
Data map:   Entities [...] · Pipeline [...] · Compliance [...] · Flags [...]
Personas:   [persona]: {role, demo_moment}
Finale:     trigger "[Email X the Y brief]" → {{slug}}_email_report
            report contents [...] · branding [logo/colours] · recipient [internal until told]
Channels:   [Client] Ops · [Client] [Domain]      target_agent: [leo | gilfoyle]
Crons:      [time] [briefing] → [channel] for [persona]
Models:     demo /model [DEMO_MODEL]  ·  daily /model [DAILY_MODEL]
Build:      [ ] manifest filled  [ ] scaffold generated + each module verified
            [ ] {{slug}}_email_report delivers PDF to test inbox
            [ ] channels created  [ ] target.json + MCP registered  [ ] crons tested
            [ ] guardrail + sane fallback set  [ ] real-path test green  [ ] runbook emitted
```

---

## Companion references

- `references/scaffold-manifest.md` — manifest schema, file tree, skeletons, `target_agent` switch, runbook emission. **Source of truth for layout + tool names.**
- `references/report-pdf-email-pattern.md` — HTML→PDF branded report, brand-scrape, attachment send (+ the `gws --attach` gotcha).
- `references/demo-reliability-hardening.md` — the six-item reliability playbook.
- `references/browser-automation-demo-pattern.md` — Playwright scraper pipeline, mock→live switching, CDS worked example.
