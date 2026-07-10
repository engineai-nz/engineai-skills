# Engine AI Claude Skills

Engine AI's shared Claude Code setup — skills, statusline, hooks, scripts, and settings templates. Used by the Engine AI team to keep their Claude Code environments consistent.

## Quick install (full setup)

```bash
git clone https://github.com/engineai-nz/engineai-skills.git ~/engineai-dotclaude
cd ~/engineai-dotclaude
./install.sh
```

The installer copies skills into `~/.claude/skills/`, scripts into `~/.claude/scripts/`, hooks into `~/.claude/hooks/`, and drops in `CLAUDE.md` + `settings.json` templates. Existing files are backed up to `~/.claude/backups/dotclaude-<timestamp>/`.

After install: restart Claude Code and edit `~/.claude/CLAUDE.md` to personalise.

## What's included

- **Skills** — GEO suite, session lifecycle, review, infra, standalone (see below)
- **Statusline** — Engine AI gold branded Python statusline with model, context %, duration, project, git branch, rate limits
- **Scripts** — session hooks (home hygiene, git status across projects, wiki sync check, wrap reminder)
- **Hooks** — auto-format on Edit/Write, bash command audit log, Next.js image cache clear
- **Templates** — sanitised `CLAUDE.md` and `settings.json` you can personalise

## What is not here

Skills paired with an Engine AI service offering and its runbook live in
[`engineai-nz/engine-ai-os`](https://github.com/engineai-nz/engine-ai-os) under `Skills/`, where
`lifecycle_audit --strict` enforces the Offer → Service → Playbook → Runbook → Skill chain in CI.
That includes `project-workflow` and `engineai-demo-package`. This repo holds general-purpose
tooling only.

## Skills-only install

Drop any skill folder into `~/.claude/skills/` to use it individually. See the category tables below.

---

## GEO -- Generative Engine Optimisation

Full suite for optimising websites for AI-powered search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews).

| Skill | What it does |
|---|---|
| `geo/geo` | Core GEO analysis with citability scoring, crawler checks, and schema audit |
| `geo/geo-audit` | Full website audit with parallel subagent delegation across all GEO dimensions |
| `geo/geo-brand-mentions` | Brand mention and authority scanning across AI-referenced platforms |
| `geo/geo-citability` | Score how likely AI systems are to cite or quote page content (0-100) |
| `geo/geo-compare` | Monthly delta tracking between baseline and current GEO audits |
| `geo/geo-content` | Content quality and E-E-A-T assessment for AI citability |
| `geo/geo-crawlers` | AI crawler access analysis via robots.txt, meta tags, and HTTP headers |
| `geo/geo-llmstxt` | Generate and validate llms.txt files for AI system discoverability |
| `geo/geo-platform-optimizer` | Platform-specific optimisation for individual AI search engines |
| `geo/geo-proposal` | Auto-generate client-ready GEO service proposals from audit data |
| `geo/geo-prospect` | CRM-lite for managing GEO prospects through the sales pipeline |
| `geo/geo-report` | Professional client-facing report combining all audit results |
| `geo/geo-report-pdf` | PDF report generation with score gauges, charts, and action plans |
| `geo/geo-schema` | Schema.org structured data audit and JSON-LD generation |
| `geo/geo-technical` | Technical SEO audit with GEO-specific crawlability and SSR checks |

## Session

Session lifecycle management for Claude Code.

| Skill | What it does |
|---|---|
| `session/load-project` | Guided walkthrough for opening a project and getting it running locally |
| `session/resume` | Start-of-session briefing: memory, git state, next actions |
| `session/resume-deep` | Comprehensive briefing with full memory review and cross-project scan |
| `session/wrap` | End-of-session cleanup: update todos, lessons, decisions, check for stray files |

## Review

| Skill | What it does |
|---|---|
| `review/adversarial-review` | Dual-agent adversarial review of PRDs, specs, and architecture docs |
| `review/code-combat` | Multi-round adversarial negotiation between AI agents over build docs |

## Meta

Skills about skills.

| Skill | What it does |
|---|---|
| `meta/autoresearch` | Autonomously optimise skills by running, scoring, and mutating prompts |
| `meta/skill-creator` | Guide for creating and packaging new Claude Code skills |

## Infrastructure

| Skill | What it does |
|---|---|
| `infra/openclaw-audit` | Audit OpenClaw VM against security, health, Docker, and app standards |
| `infra/unraid-troubleshooter` | Unraid server diagnostics: array, parity, Docker, VMs, plugins |

## Standalone Skills

| Skill | What it does |
|---|---|
| `brainstorming` | Pre-build exploration of intent, requirements, and design before implementation |
| `brand` | Engine AI visual identity: colours, typography, spacing, components, tone of voice |
| `file-organizer` | Intelligent file/folder organisation with duplicate detection |
| `humaniser` | Strip AI writing patterns, apply natural direct voice |
| `notebooklm` | Query Google NotebookLM for source-grounded, citation-backed answers |
| `senior-architect` | System architecture design with diagrams for React, Node, Postgres, Go, Python |
| `Stellar-Immigration-Agent-Skill` | NZ immigration process for recruiting Filipino skilled workers (AEWV) |

---

## Installation

Full setup (recommended): `./install.sh` — see top of this README.

Single skill, manual: `cp -r geo/geo-audit ~/.claude/skills/geo-audit`

## Config bundle layout

```
config/
├── scripts/       # ~/.claude/scripts/  — statusline.py, session-start hooks
├── hooks/         # ~/.claude/hooks/    — PostToolUse hooks
└── templates/     # CLAUDE.md + settings.json starter templates
```

## Opt-in env vars

| Var | What it does |
|---|---|
| `OPENCLAW_HOST` | If set (e.g. `user@10.0.0.2`), session-start hook pings an OpenClaw server over SSH. Skipped silently when unset. |
| `HYGIENE_ALLOWED_DIRS` | Space-separated list of directories expected in `~/`. Defaults to `projects`. |

## Built by

[Engine AI](https://engineai.co.nz) -- AI orchestration consultancy, Auckland, New Zealand.
