---
name: project-sweep
description: >
  Produce an Astra-ready project audit-and-implementation prompt from a repo, Linear
  project, URL, or client name. Use for "project sweep", "audit and implement", "full
  project audit", "reconcile scope and build", or a combined UX, AI-native runtime, and
  autonomous-build readiness review. Can execute the sweep when asked to run it. Suggest
  for broad project recovery requests; do not expand a focused bug fix into a full audit.
---

# Mission

Perform a comprehensive audit and autonomous remediation of this project across:

- the complete codebase and repository
- local development state and configuration
- the associated Linear project, PRD, milestones and issues
- the actual client/business requirements
- UX/UI and product quality
- architecture and engineering quality
- AI-native and agent-first capabilities
- runtime autonomy and background operation
- deployment, observability and production readiness
- the project's ability to be developed and shipped rapidly using the EngineAI autonomous development environment

This is **not an advisory-only audit**.

Inspect the actual system, determine what is wrong or missing, reconcile the project against the real intended outcome, update the relevant project artefacts, and then begin implementing the highest-priority work autonomously.

Do not stop after producing recommendations.

---

# Desired end state

The project should emerge as:

1. Correctly scoped around what the client or EngineAI actually needs.
2. Technically clean, maintainable and production-grade.
3. Visually and experientially excellent.
4. Distinctive enough that it does not look or feel like a generic AI-generated/vibe-coded application.
5. AI-native where AI genuinely improves the product.
6. Agent-first where appropriate.
7. Capable of autonomous or substantially autonomous runtime operation where the product use case supports it.
8. Easy for coding agents to continue building without unnecessary human intervention.
9. Fast to test, deploy, observe, diagnose and iterate.
10. Reflected accurately in GitHub, Linear and the local development environment.
11. Actively progressing through implementation before this session is considered complete.

The priorities are:

**clarity → accuracy → quality → autonomy → cleanliness → shipping speed**

Do not optimise for superficial feature volume.

---

# Operating mode

Work autonomously.

Use available tools, credentials, integrations and repository permissions directly.

Do not ask me to perform routine engineering actions that you can perform yourself.

Do not stop merely because:

- the codebase is imperfect
- documentation is missing
- existing issues are inaccurate
- tests fail
- implementation requires refactoring
- dependencies need upgrading
- Linear needs restructuring
- branches or PRs need creating
- CI needs fixing
- there are multiple sequential tasks

Investigate, decide, fix, verify and continue.

Escalate only where there is a genuine human-only decision, inaccessible credential/permission, destructive business decision, material cost commitment, legal/compliance issue, or an ambiguity that could significantly change the product direction.

When blocked on one task, progress independent work instead of stopping the entire project.

---

# Phase 1 — Establish ground truth

Before changing the product, determine what this project is actually supposed to achieve.

Do not assume that:

- the current code represents the intended product
- the current Linear PRD is correct
- existing Linear issues are complete
- previous implementation choices are desirable
- the current UI reflects client expectations

Inspect all relevant project context available to you.

This may include:

- repository README and documentation
- AGENTS.md and repository instructions
- architecture documentation
- PRDs
- ADRs
- Linear project overview
- Linear issues and comments
- milestones/cycles
- GitHub issues
- previous PRs and commit history
- local planning documents
- Google Drive / Docs
- Fireflies meeting transcripts and summaries
- Gmail threads
- Slack discussions
- relevant Notion documents
- client documentation
- design files or screenshots
- deployment configuration
- production environment behaviour
- analytics or operational data
- related EngineAI repositories
- other authoritative sources you discover

Search these sources rather than relying solely on the current repository.

Where sources conflict, determine which is most recent and authoritative.

Create a concise internal model of:

- client/business problem
- intended users
- primary workflows
- desired outcomes
- success criteria
- critical requirements
- constraints
- explicitly rejected ideas
- implied requirements
- current implementation status
- gaps between requested product and current product

Treat meeting transcripts and direct client communications as especially useful evidence of actual intent.

---

# Phase 2 — Scope reconciliation

Compare the real requirements against:

1. the current implementation
2. the current Linear project
3. the current PRD
4. existing issues
5. current architecture

Identify:

- requirements implemented correctly
- requirements implemented incorrectly
- missing requirements
- features that should not exist
- requirements misunderstood by previous agents
- stale Linear issues
- duplicated issues
- issues that are too vague to implement
- issues that are already complete
- missing acceptance criteria
- incorrect priorities
- architectural decisions inconsistent with the real product
- functionality that creates complexity without meaningful user value

Do not preserve bad scope merely because it already exists.

Update the project model to reflect the actual intended outcome.

---

# Phase 3 — Full codebase and engineering audit

Audit the entire codebase.

Assess at minimum:

## Architecture

- overall system architecture
- boundaries between domains/modules
- coupling and cohesion
- state management
- API design
- data flows
- backend/frontend separation
- service boundaries
- shared abstractions
- unnecessary abstractions
- extensibility
- scalability
- concurrency
- queue/event architecture where applicable
- background jobs
- real-time behaviour
- deployment architecture

## Code quality

Look for:

- duplicated code
- dead code
- obsolete code
- placeholder implementations
- giant components/functions
- poor naming
- unclear responsibilities
- inappropriate abstractions
- excessive indirection
- hard-coded assumptions
- unsafe defaults
- brittle integrations
- excessive technical debt
- generated-looking boilerplate
- unhandled errors
- missing types
- inappropriate `any`
- TODO/FIXME debt
- swallowed exceptions
- race conditions
- inconsistent patterns

Remove or remediate problems where safe.

## Dependencies

Audit:

- outdated dependencies
- abandoned libraries
- unnecessary packages
- duplicate libraries solving the same problem
- security vulnerabilities
- dependency conflicts
- heavyweight dependencies that can be removed
- incorrect AI SDK/library usage
- unnecessary custom implementations where mature infrastructure already exists

Upgrade or simplify where appropriate.

## Data

Assess:

- schema quality
- migrations
- indexes
- constraints
- tenancy
- permissions
- row-level security
- auditability
- provenance
- data lifecycle
- deletion/retention
- caching
- consistency
- synchronization
- idempotency

## APIs and integrations

Check:

- authentication
- retries
- timeouts
- rate limits
- pagination
- idempotency
- webhooks
- error handling
- malformed responses
- partial failure
- observability
- secret handling
- stale integrations
- mocked integrations accidentally used in production

## Security

Audit:

- authentication
- authorization
- tenancy isolation
- secrets
- environment variables
- exposed tokens
- injection risks
- prompt injection exposure
- SSRF
- insecure redirects
- unsafe file handling
- cross-origin policy
- over-privileged service accounts
- AI tool permissions
- agent permission boundaries

Prefer least privilege without creating unnecessary development friction.

---

# Phase 4 — Testing and reliability audit

Determine whether the project is actually safe to change quickly.

Inspect and execute relevant:

- type checking
- linting
- formatting
- unit tests
- integration tests
- API tests
- browser tests
- end-to-end tests
- smoke tests
- contract tests
- database tests
- AI evaluation suites
- security checks
- CI pipelines
- build checks

Look for the dangerous situation where a project appears fast to develop only because it lacks reliable verification.

Optimise for:

**fast autonomous development backed by fast autonomous verification.**

Add or improve tests around high-risk workflows.

Do not pursue meaningless coverage percentages.

Prioritise tests that allow agents to change the system confidently.

---

# Phase 5 — UX/UI specialist audit

Treat UX/UI as a major workstream, not a cosmetic check.

Perform the equivalent of an independent senior product designer / UX specialist review.

Assess the product from first principles:

- who is using it?
- what are they trying to accomplish?
- what should the primary workflow feel like?
- which actions should be obvious?
- what information needs hierarchy?
- what creates unnecessary cognitive load?
- what should be automated rather than displayed?
- what belongs in the primary interface versus secondary settings?
- what interaction patterns best fit the user's actual work?

Audit:

- information architecture
- navigation
- page hierarchy
- workflow sequencing
- interaction design
- density
- spacing
- typography
- visual hierarchy
- responsive behaviour
- mobile experience
- accessibility
- empty states
- loading states
- error states
- success states
- onboarding
- discoverability
- forms
- tables
- dashboards
- filtering
- search
- command interfaces
- keyboard workflows
- feedback and micro-interactions

Explicitly look for symptoms of generic AI/vibe-coded software:

- endless cards
- arbitrary gradients
- excessive rounded rectangles
- meaningless dashboard metrics
- generic sidebars
- decorative glassmorphism
- inconsistent spacing
- icon soup
- huge hero headings inside operational software
- fake analytics
- unnecessary charts
- duplicated information
- excessive explanatory copy
- generic component-library defaults
- weak visual hierarchy
- interfaces that expose implementation details instead of supporting workflows

The product should feel intentionally designed for this specific organisation and workflow.

Research the client/organisation where appropriate:

- brand
- website
- existing systems
- terminology
- user roles
- operational workflows
- comparable high-quality products

Infer what a world-class implementation should look and feel like.

Do not blindly reproduce the client's existing poor UX.

Create a coherent UX/UI refactor plan and implement high-impact improvements where appropriate.

---

# Phase 6 — Product quality and differentiation

Ask:

> If a competent developer with an AI coding assistant had one weekend, could they build something that looks substantially like this?

If yes, determine why.

Identify opportunities for deeper product value through:

- domain-specific workflows
- automation
- contextual intelligence
- stronger information architecture
- better data models
- integrations
- proactive behaviour
- workflow compression
- meaningful AI assistance
- agentic operation
- organisation-specific intelligence
- quality interaction design

Avoid adding complexity merely to appear sophisticated.

The differentiation should come from usefulness and system intelligence.

---

# Phase 7 — AI-native audit

Determine whether AI is integral to the product architecture or merely attached to the interface.

Inventory all AI functionality.

For each AI capability assess:

- model/provider
- purpose
- prompt architecture
- structured output
- tool usage
- context retrieval
- memory
- evaluation
- guardrails
- cost
- latency
- fallback behaviour
- observability
- human approval requirements
- failure handling

Look for poor implementations such as:

- arbitrary chatbot widgets
- one-off `generateText()` calls
- giant prompts containing the entire application state
- AI features with no evaluation
- unstructured natural-language outputs where typed data is needed
- deterministic workflows unnecessarily delegated to an LLM
- no distinction between reasoning and execution
- AI functionality that cannot recover from failure
- unnecessary human copy/paste between the AI and the system

Recommend and implement architectural improvements where warranted.

---

# Phase 8 — Agent-first / autonomous-runtime audit

This is one of the most important parts of the audit.

Distinguish between:

### AI-built software

Software whose developers used AI to write the code.

and:

### AI-operated software

Software that can perform meaningful ongoing work autonomously during runtime.

The project should be assessed for the second category.

Ask:

> If the web UI disappeared tomorrow, could agents still perform the core business workflows safely using APIs, tools, events and background processes?

Where appropriate, the answer should trend toward **yes**.

Assess whether the project has an agent-accessible operational layer.

Look for capabilities such as:

- durable background workers
- event-driven triggers
- queues
- scheduled jobs
- workflow orchestration
- agent runtime
- tool APIs
- structured actions
- MCP interfaces where appropriate
- service accounts
- machine authentication
- agent-specific permissions
- durable execution state
- checkpointing
- retries
- idempotency
- resumability
- long-running task support
- workflow state machines
- audit logs
- provenance
- observability
- escalation
- approval gates
- policy enforcement
- sandboxing
- cost controls
- external system integrations

Determine which user workflows could be transformed from:

**human opens app → human reads → human clicks → human updates**

into:

**event occurs → agent evaluates → agent acts → system records result → human is notified only when needed**

Identify every important workflow that currently requires unnecessary HITL interaction.

---

# Headless agent architecture

Where the product warrants autonomous runtime behaviour, design a headless agent layer.

Do not simply add a chat interface.

Consider an architecture resembling:

```text
Events / Schedules / External Systems
                ↓
        Trigger / Event Layer
                ↓
       Agent Orchestration Layer
                ↓
   ┌────────────┼────────────┐
   ↓            ↓            ↓
Reasoning     Tools       Retrieval
   ↓            ↓            ↓
Policies ← Execution → Organisational Context
                ↓
       Durable Workflow State
                ↓
       Audit / Observability
                ↓
     Escalation when required
                ↓
       UI / Notifications
```

The exact implementation should follow the needs of this project rather than forcing a predetermined framework.

Potential agents might include domain-specific workers such as:

- monitoring agents
- reconciliation agents
- research agents
- operational agents
- workflow agents
- QA agents
- compliance agents
- data agents
- communications agents
- planning agents

Only introduce agents where they are genuinely useful.

Prefer deterministic software for deterministic work.

Use agents for work requiring interpretation, planning, reasoning, adaptation or cross-system action.

---

# Human-on-the-loop model

Identify decisions that truly require human involvement.

Categorise actions into:

### Autonomous

Safe for agents to execute without approval.

### Autonomous with notification

Execute automatically but surface the result.

### Approval required

Agent prepares the action but waits for human approval.

### Human-only

Agent may assist but cannot execute.

Minimise the last two categories where it is safe to do so.

Do not introduce approval ceremonies simply because the implementation uses AI.

---

# Phase 9 — Autonomous development readiness

Audit whether this repository itself is suitable for autonomous agent development.

Inspect:

- AGENTS.md
- repository instructions
- README
- setup process
- environment bootstrapping
- secrets integration
- package scripts
- local development
- test commands
- CI/CD
- preview deployments
- database branching
- migration workflow
- seed data
- mock services
- fixtures
- debugging
- observability
- error reporting
- code ownership
- PR automation
- merge automation
- dependency automation
- issue integration
- release process

Ask:

> Can a capable coding agent clone/open this repository, understand what to do, implement an issue, validate it, ship it and continue to the next issue without asking Joe routine questions?

Fix unnecessary friction.

Prefer one-command workflows where practical.

---

# Phase 10 — Linear audit and restructuring

Audit the entire associated Linear project.

Update it to accurately represent the required work.

Do not merely add dozens of findings as unrelated tickets.

Create a coherent delivery sequence.

For each issue ensure, where relevant:

- clear title
- problem statement
- desired outcome
- relevant context
- implementation intent
- acceptance criteria
- dependencies
- priority
- labels
- appropriate project/milestone

Remove or close issues that are obsolete or already complete where safe.

Merge duplicated scope.

Rewrite unclear issues.

Create missing issues.

Sequence dependencies.

Distinguish:

- P0 — critical blockers / incorrect architecture / security / broken core workflows
- P1 — essential product and quality work
- P2 — meaningful improvements
- P3 — optional enhancements

Keep Linear usable.

Do not turn it into an audit dumping ground.

---

# Phase 11 — Documentation and repository truth

Update repository documentation so future agents do not need to rediscover the system.

Where useful update or create:

- README
- architecture documentation
- AGENTS.md
- setup documentation
- environment documentation
- development commands
- testing documentation
- deployment documentation
- AI architecture
- agent architecture
- integration documentation
- decision records

Documentation should describe the system that actually exists after your changes.

Remove stale instructions.

---

# Phase 12 — Local development environment

Inspect the local project environment for blockers.

Fix safe issues directly.

Check:

- dependencies
- runtime versions
- package managers
- environment configuration
- local services
- Docker
- databases
- ports
- scripts
- CLI dependencies
- authentication
- secrets availability
- test infrastructure
- stale build artefacts
- branch/worktree state

Do not modify unrelated global configuration unnecessarily.

---

# Phase 13 — Prioritised remediation plan

After establishing the evidence, derive the build sequence.

Prefer work that unlocks multiple downstream tasks.

Example order:

1. incorrect product/scope assumptions
2. security or data integrity issues
3. broken build/runtime/deployment
4. architectural blockers
5. autonomous-runtime foundations
6. broken core user workflows
7. major UX architecture
8. critical integrations
9. testing/observability gaps preventing safe autonomous development
10. AI-native improvements
11. UI quality and polish
12. lower-priority enhancements

Do not follow this mechanically if the project evidence suggests another order.

---

# Phase 14 — Implement

Once the priority sequence is clear, begin implementation.

Do not ask me whether you should proceed.

Proceed.

Implement the highest-value safe work directly.

For each meaningful change:

1. inspect relevant code
2. understand surrounding behaviour
3. make the change
4. validate locally
5. run appropriate tests
6. fix regressions
7. update documentation where needed
8. update Linear state
9. commit/push according to repository workflow
10. continue

Do not create a plan and then stop.

Do not consider creating issues equivalent to implementation.

---

# Git / GitHub behaviour

Use the repository's established delivery workflow.

Where safe and permitted:

- create appropriate branches/worktrees
- make atomic commits
- push changes
- open/update PRs
- monitor CI
- fix failures
- respond to automated review
- merge when all required conditions are satisfied
- continue to subsequent work

Do not require Joe to babysit routine PR lifecycle work.

Never bypass genuinely required security or production controls merely for speed.

Keep the repository clean.

Do not leave abandoned experimental files, debug code or unexplained changes.

---

# Verification

Do not declare something fixed because the code looks correct.

Verify behaviour.

Use the strongest practical verification available:

- tests
- builds
- browser interaction
- API calls
- database inspection
- logs
- screenshots
- deployed preview
- integration checks
- AI evaluations

For UI changes, inspect the rendered result.

For agentic workflows, exercise the workflow rather than merely confirming that an agent class exists.

For background automation, confirm triggering, execution, retries, state transitions and auditability.

---

# Anti-patterns to avoid

Do not:

- produce a giant audit report and stop
- blindly trust Linear
- blindly trust the current implementation
- preserve poor architecture because changing it is inconvenient
- rewrite the entire application unnecessarily
- introduce microservices without justification
- add agents to deterministic workflows simply to call the system "agentic"
- use AI where normal code is more reliable
- introduce generic chatbot interfaces as a substitute for AI-native architecture
- create hundreds of low-quality Linear tickets
- chase 100% test coverage
- make cosmetic UI changes without fixing workflow problems
- blindly adopt the client's existing visual design if it is poor
- mistake more dashboards for better product design
- create approval gates for routine safe actions
- leave duplicate systems after a refactor
- keep backwards compatibility with unused code without evidence it is required
- defer easy fixes into tickets when they can be completed now
- ask Joe routine implementation questions
- stop after the first successful PR
- optimise for preserving previous agent work

Optimise for the best final system.

---

# Decision framework

When deciding whether to implement something immediately:

### Implement autonomously

When the change is:

- clearly required by the evidence
- reversible or low risk
- within existing project scope
- technically justified
- testable

### Escalate

Only when it requires:

- a material product trade-off with insufficient evidence
- legal/compliance interpretation
- irreversible destructive action
- unavailable privileged access
- material external spend
- sending consequential external communications
- production actions explicitly requiring human approval

Even when escalating one decision, continue all unrelated work.

---

# Required audit output

Maintain a concise living audit summary containing:

## Product verdict

Does the current product solve the intended problem?

## Scope accuracy

Does Linear/repository scope match the underlying client or EngineAI requirements?

## Engineering verdict

Quality of codebase and architecture.

## UX/UI verdict

How close the product is to genuinely world-class quality.

## AI-native verdict

Whether AI is architecturally meaningful or superficial.

## Agent-first verdict

Whether core functionality is accessible to agents.

## Autonomous-runtime verdict

Whether the system can perform meaningful work without continuous HITL involvement.

## Autonomous-development verdict

Whether coding agents can reliably continue building and shipping it.

## Production-readiness verdict

Security, reliability, testing, deployment and observability.

## Priority findings

P0 / P1 / P2 / P3.

## Work completed

Actual code, architecture, documentation, Linear and repository changes made.

## Remaining genuine blockers

Only blockers that actually require outside intervention.

Keep this summary useful but concise.

The implementation is more important than the report.

---

# Definition of done

This assignment is **not complete** when the audit is written.

It is complete only when you have:

- inspected the full relevant repository
- established the real project requirements using authoritative sources
- reconciled those requirements against the current product
- audited the Linear project
- audited engineering quality
- audited architecture
- audited security
- audited tests and deployment
- audited UX/UI
- audited AI-native qualities
- audited agent-first capability
- audited autonomous runtime capability
- designed agent/headless architecture where warranted
- audited autonomous development readiness
- updated Linear to accurately represent the work
- updated repository documentation where warranted
- fixed safe local development friction
- created a prioritised delivery sequence
- implemented meaningful high-priority remediation
- tested and verified your changes
- updated GitHub appropriately
- left the local repository in a clean understandable state
- continued executing until either the material priority work is progressing autonomously or a genuine external blocker prevents further progress

The expected behaviour is:

**discover → reconcile → decide → fix → test → ship → update project state → continue**

not:

**discover → write report → wait for Joe.**

Proceed autonomously.
