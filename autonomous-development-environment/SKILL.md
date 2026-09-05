---
name: autonomous-development-environment
description: >
  Audit and raise an EngineAI workstation or agent runtime toward a fully autonomous
  development environment. Use for "ADE", "autonomous development environment", "agent
  workstation audit", "can agents ship unattended", or when hardening local tooling,
  permissions, loops, and guardrails so coding agents can build, verify, and remediate
  with minimal human intervention.
---

# Build the Ultimate Autonomous Development Environment for EngineAI

## Mission

The theme of this session is to build the **ultimate autonomous software development environment for Joe Ward and EngineAI**.

The desired end state is not merely “AI-assisted development.” It is an operating environment where, once Joe or Ben has defined and approved what should be built, an autonomous development agent can take ownership of delivery and continue working until the agreed scope is complete, tested, deployed, and operational.

Do not stop at recommendations.

**Audit the actual environment, identify anything that prevents this operating model, and implement every safe improvement you have sufficient authority to implement.**

The governing principle is:

> Once a project has been handed from humans to the development agent, Joe and Ben should not be required to babysit execution.

---

# Desired EngineAI Delivery Model

The ideal workflow is:

1. **Joe and Ben talk to clients**
   - discovery
   - requirements
   - strategy
   - commercial decisions
   - product direction

2. **Fireflies captures meetings**
   - transcripts
   - requirements
   - decisions
   - actions
   - constraints

3. **AI converts discovery into delivery artefacts**
   - opportunity brief where appropriate
   - project specification
   - architecture/design
   - PRD
   - acceptance criteria

4. **PRD becomes structured Linear work**
   - projects
   - milestones
   - issues
   - dependencies
   - priorities
   - acceptance criteria

5. **Project is handed to an autonomous development agent**
   - agent understands the PRD
   - reads Linear
   - works through issues
   - writes code
   - runs tests
   - fixes failures
   - opens/reviews/merges PRs
   - updates Linear
   - handles dependencies
   - deploys
   - verifies production
   - communicates progress
   - continues until project completion

6. **Agents operate and maintain the product**
   - deployment
   - monitoring
   - bug remediation
   - dependency maintenance
   - CI failures
   - routine operational fixes
   - incremental improvements where authorised

Once Step 5 begins, Joe and Ben should be able to:

- go on holiday;
- meet other clients;
- work on strategy;
- start another project;

without delivery stopping because an agent needs a routine human action.

---

# Core Requirement

Find every realistic point in the EngineAI development lifecycle where an agent could currently be forced to say something equivalent to:

- “Joe, I need you to approve this.”
- “Joe, you need to merge this PR.”
- “Joe, only an admin can do this.”
- “Joe, I don't have access to this service.”
- “Joe, I need this API key.”
- “Joe, you need to create this environment variable.”
- “Joe, you need to approve this deployment.”
- “Joe, you need to configure this integration.”
- “Joe, GitHub won't allow me to merge this.”
- “Joe, I can't access Linear/Fireflies/Supabase/Vercel/etc.”
- “Joe, I need permission to run this command.”
- “Joe, CI failed so I stopped.”
- “Joe, another issue is blocking this one so I'm waiting.”
- “Joe, the PR has review comments so I'm waiting.”
- “Joe, deployment failed so I'm waiting.”
- “Joe, my context reset and I don't know what to do next.”

For each such scenario, determine whether it can be eliminated through:

- configuration;
- authentication;
- credentials;
- permissions;
- GitHub settings;
- repository configuration;
- Codex configuration;
- local development environment setup;
- CI/CD;
- secrets management;
- service accounts;
- agent instructions;
- automation;
- tooling;
- repository architecture;
- EngineAI OS;
- process changes;
- recovery mechanisms.

The target is **human-on-the-loop, not human-in-the-loop**, once implementation begins.

Humans should intervene only for genuinely human decisions.

---

# Important Context

A global `AGENTS.md` autonomy audit has already been performed or is being performed as part of this broader initiative.

Do not limit this audit to `AGENTS.md`.

Treat `AGENTS.md` as only one component of the autonomous development system.

We now need to determine whether the surrounding environment actually enables the behaviour those instructions describe.

---

# Audit Scope

Perform a comprehensive audit of the actual environment available to you.

Do not assume configuration is correct because a README says it is.

Where possible, inspect the real configuration and test the capability.

## 1. Codex / Agent Runtime

Audit the Codex environment itself.

Determine:

- what permissions agents have;
- what filesystem restrictions exist;
- what commands require approval;
- what network restrictions exist;
- what integrations are available;
- what MCP servers are configured;
- what authentication is available;
- whether credentials persist correctly;
- whether agents can execute long multi-step development workflows;
- what happens across context/session resets;
- whether agents can recover project state;
- whether agents can run tests and development servers;
- whether agents can create branches;
- whether agents can commit;
- whether agents can push;
- whether agents can create PRs;
- whether agents can review PR feedback;
- whether agents can merge;
- whether agents can deploy;
- whether agents can observe deployment status;
- whether agents can diagnose failed deployments;
- whether agents can update Linear autonomously.

Identify runtime behaviours that unnecessarily force approval or manual interaction.

Where configuration can safely remove these constraints, change it.

---

# 2. Joe's Local MacBook Development Environment

Audit the local development environment available to the agent.

Inspect relevant tooling such as:

- Git
- GitHub CLI
- Node
- npm / pnpm / yarn / bun as applicable
- Python
- package managers
- Docker
- local databases
- Supabase tooling
- Vercel tooling
- cloud CLIs
- shell configuration
- credential helpers
- SSH
- environment management
- secrets tooling
- Bitwarden tooling
- development certificates
- required build tooling
- repository checkout conventions
- PATH/configuration problems
- any other tools EngineAI projects depend upon

Look for:

- missing dependencies;
- expired authentication;
- inconsistent versions;
- manual login requirements;
- interactive commands that break autonomous execution;
- credentials only available in Joe's interactive shell;
- secrets stored insecurely;
- tools requiring GUI interaction;
- tooling that agents cannot invoke;
- machine-specific assumptions;
- fragile local state.

The environment should be reproducible and agent-operable.

---

# 3. GitHub Organisation and Repository Controls

This is a critical audit area.

Inspect actual EngineAI GitHub configuration wherever your permissions allow.

Audit organisation-level and repository-level:

- permissions;
- roles;
- branch protection;
- rulesets;
- required reviews;
- CODEOWNERS;
- required status checks;
- merge queues;
- merge methods;
- signed commit requirements;
- workflow permissions;
- GitHub Actions permissions;
- Actions secrets;
- environments;
- environment protection;
- deployment approvals;
- repository access;
- GitHub App permissions;
- bot/service-account permissions;
- Dependabot;
- security scanning;
- required conversations;
- force-push restrictions;
- admin bypass policies;
- default branch rules;
- PR creation/merge restrictions.

Find anything that could cause a completed agent change to sit waiting indefinitely for Joe or Ben.

We still require appropriate engineering safeguards.

The objective is **not to remove quality controls**.

The objective is to replace unnecessary human controls with **automated evidence-based controls**, for example:

PR → automated tests → lint → typecheck → security checks → preview/deployment verification → autonomous review/remediation → merge → deploy

instead of:

PR → Joe manually reviews → Joe clicks merge → Joe approves deployment.

Where human approval provides no meaningful risk reduction, determine whether it should be automated or removed.

Where genuine human approval remains necessary, clearly explain why.

---

# 4. EngineAI Repository Standards

Audit the standards and operating instructions used across EngineAI repositories.

At minimum inspect:

https://github.com/engineai-nz/engine-ai-starter/blob/main/HOW_WE_BUILD.md

and:

https://github.com/engineai-nz/engine-ai-os

Also locate any other relevant sources of delivery instructions, including:

- repository `AGENTS.md` files;
- global instructions;
- README files;
- CONTRIBUTING documents;
- architecture documents;
- CI configuration;
- GitHub workflows;
- templates;
- scripts;
- bootstrap tooling;
- EngineAI starter templates;
- project scaffolding;
- deployment conventions;
- issue conventions;
- Linear integration instructions.

Look for contradictions between these systems.

Examples:

- global `AGENTS.md` encourages autonomous merging while repository rules prohibit it;
- EngineAI OS says agents should continue autonomously but CI requires manual deployment approval;
- HOW_WE_BUILD requires processes that no longer serve a purpose;
- different repositories use incompatible development conventions;
- documentation assumes credentials that agents do not actually have.

There should ultimately be **one coherent operating model**.

---

# 5. Third-Party Integrations and Credentials

Identify every external service involved in the EngineAI development lifecycle.

Do not restrict yourself to this list, but explicitly investigate relevant tools such as:

- GitHub
- Linear
- Fireflies
- Vercel
- Supabase
- Bitwarden
- Atomic / Automic or whatever EngineAI currently uses under that name
- Slack
- Gmail
- Google Workspace
- Notion
- OpenAI
- Anthropic or other model providers
- DNS providers
- hosting/cloud providers
- database providers
- observability platforms
- error tracking
- analytics
- payment providers where relevant
- client APIs
- MCP servers
- internal EngineAI Brain services

For each service determine:

1. Is it connected?
2. Is authentication valid?
3. Can the agent access it?
4. Can the agent perform required read operations?
5. Can the agent perform required write operations?
6. Can the agent perform required administrative/deployment operations?
7. Are permissions appropriately scoped?
8. Are credentials stored securely?
9. Can credentials be accessed non-interactively?
10. What happens when credentials expire?
11. Is there a refresh/rotation strategy?
12. Is Joe personally the only account capable of an essential operation?

Search specifically for **Joe-as-single-point-of-failure scenarios**.

Do the same for Ben.

---

# 6. Secrets and Identity Architecture

Determine whether EngineAI has the right identity model for autonomous agents.

Audit whether agents currently depend on:

- Joe's personal credentials;
- Joe's browser session;
- Joe's SSH keys;
- Joe manually copying secrets;
- Joe approving OAuth;
- Joe unlocking Bitwarden;
- Joe creating API keys.

Where appropriate, recommend or implement a better model using:

- machine/service identities;
- GitHub Apps;
- service accounts;
- workload identity;
- scoped tokens;
- secrets managers;
- Bitwarden machine accounts/service accounts;
- CI identities;
- environment-specific credentials;
- automatic rotation.

The desired model is:

**persistent machine-authorised access with least privilege**, not “an agent pretending to be Joe.”

---

# 7. CI/CD and Deployment Autonomy

Audit the complete path:

code → commit → PR → validation → merge → deployment → production verification.

Agents should be capable of handling the normal path and common failure paths.

Inspect whether they can autonomously:

- run local validation;
- run unit tests;
- run integration tests;
- run E2E tests;
- interpret CI failures;
- patch failures;
- push fixes;
- monitor CI;
- merge once gates pass;
- deploy preview environments;
- deploy staging;
- deploy production where policy permits;
- inspect deployment logs;
- roll back;
- fix deployment failures;
- verify production health.

Identify any deployment systems requiring humans to click buttons.

---

# 8. Autonomous PR Lifecycle

Design for a world where Joe does **not babysit PRs**.

Determine whether an agent can:

1. create its own branch;
2. implement the issue;
3. test locally;
4. commit;
5. push;
6. create PR;
7. monitor CI;
8. fix CI;
9. inspect review comments;
10. resolve legitimate comments;
11. reject/clarify incorrect automated review comments where appropriate;
12. rerun checks;
13. merge after required evidence passes;
14. remove branch;
15. update Linear;
16. continue to the next issue.

Audit every step.

Where the process currently pauses for a human, determine why.

---

# 9. Linear → Autonomous Execution

Audit how agents consume Linear work.

The preferred behaviour is not:

> implement one issue → stop → ask Joe what next.

The preferred behaviour is:

> understand project → select next eligible issue → implement → validate → merge → update Linear → select next eligible issue → continue.

Determine whether the environment supports:

- project-level context;
- issue prioritisation;
- dependency awareness;
- status updates;
- issue creation when implementation reveals legitimate missing work;
- blocker creation;
- issue completion;
- parent/sub-issue management;
- milestone progression;
- automatic continuation.

Agents should be able to work through an entire project backlog.

---

# 10. Failure Recovery

A truly autonomous system must be resilient when something goes wrong.

Audit behaviour for:

- failed tests;
- failed builds;
- broken dependencies;
- rate limits;
- temporary API failures;
- Git conflicts;
- stale branches;
- CI failures;
- deployment failures;
- database migration failures;
- flaky tests;
- package registry failures;
- unavailable third-party APIs;
- context exhaustion;
- session termination;
- machine restart;
- partially completed issues.

For recoverable failures, the expected behaviour should be:

diagnose → fix/retry → validate → continue

not:

diagnose → tell Joe → stop.

---

# 11. State Persistence and Agent Handoffs

A session ending must not mean project delivery ends intellectually.

Determine how an agent can reconstruct:

- project goal;
- approved PRD;
- architecture decisions;
- completed work;
- current issue;
- current branch/PR;
- known blockers;
- deployment state;
- next actions.

Evaluate whether state should live in:

- Linear;
- GitHub;
- EngineAI Brain;
- repository documentation;
- structured agent traces;
- EngineAI OS;
- another durable system.

Avoid creating unnecessary duplicate systems.

There should be a clear source of truth.

---

# 12. Observability and Maintenance

Deployment is not completion if nobody knows the application is broken.

Audit whether agents can observe:

- production errors;
- logs;
- uptime;
- failed jobs;
- failed deployments;
- database health;
- queue health;
- integration failures;
- security alerts;
- dependency alerts.

Determine whether common operational problems can automatically become agent work.

Longer term, the model should support:

signal → issue → diagnosis → fix → PR → validation → deployment → verification.

---

# 13. Human Escalation Policy

Define precisely what still deserves Joe or Ben's involvement.

Human escalation should generally be restricted to categories such as:

- material financial commitments outside pre-approved limits;
- contracts/legal commitments;
- destructive irreversible production operations with material business risk;
- significant product decisions not covered by the PRD;
- major architecture changes that fundamentally alter approved scope;
- security incidents requiring executive judgement;
- unavailable credentials that cannot safely be provisioned any other way;
- actions legally requiring a human;
- communications or commitments that require founder authority.

Do **not** treat routine software engineering judgement as a human escalation.

Agents should make reasonable implementation decisions themselves.

---

# Audit Method

Do not perform a theoretical review only.

For every major capability:

1. inspect configuration;
2. inspect documentation;
3. inspect permissions where possible;
4. test the actual capability where safe;
5. compare declared behaviour against real behaviour;
6. identify the blocker;
7. determine the root cause;
8. implement the fix if authorised and safe;
9. verify the fix.

Examples:

Do not merely check that GitHub CLI is installed.

Verify authentication and what repositories/actions it can perform.

Do not merely see that Vercel configuration exists.

Determine whether the agent can actually deploy and inspect the deployment.

Do not merely see a Linear MCP configuration.

Verify the development agent can read and update project issues.

---

# Implementation Mandate

This is an **audit + remediation session**, not an advisory report.

When you identify an issue:

### Fix it immediately when:
- you have sufficient access;
- the change is reversible or low risk;
- it clearly moves the environment toward the stated target;
- it does not require a genuine founder/business decision.

Examples:

- broken configuration;
- missing local tooling;
- inconsistent repository instructions;
- CI problems;
- automation gaps;
- scripts;
- agent configuration;
- outdated documentation;
- missing safe permissions;
- workflow configuration.

Do not ask Joe for permission for ordinary remediation work already implied by this mission.

### Escalate only when:
you literally cannot proceed safely or technically without Joe/Ben.

When escalation is necessary, explain:

- exact blocker;
- why the agent cannot solve it itself;
- exact one-time human action required;
- how we prevent that human dependency from recurring.

The important part is the final point.

A human intervention should ideally be a **one-time bootstrap action**, not a permanent part of the development workflow.

---

# Security Constraint

Autonomy does not mean unlimited credentials.

Optimise simultaneously for:

**maximum useful autonomy + least privilege + auditability + recoverability.**

Do not weaken controls indiscriminately.

Prefer:

- scoped credentials;
- machine identities;
- automated policy;
- automated tests;
- reversible actions;
- logged operations;
- protected high-risk resources;

over unrestricted admin credentials.

The goal is eliminating **unnecessary human intervention**, not eliminating security.

---

# Anti-Patterns to Identify

Actively search for:

- Joe being the only GitHub admin able to complete routine work;
- mandatory founder PR approval;
- mandatory deployment approval;
- personal API tokens;
- secrets stored only in `.env` on Joe's Mac;
- undocumented credentials;
- browser-only authentication;
- CLI tools requiring repeated interactive login;
- disconnected MCP integrations;
- credentials agents cannot access;
- CI checks agents cannot rerun;
- repositories agents cannot push to;
- environments agents cannot deploy to;
- Linear projects agents cannot update;
- infrastructure requiring console clicks;
- manual DNS changes;
- manual migration execution;
- manual version releases;
- undocumented bootstrap procedures;
- inconsistent repo setup;
- local-only configuration;
- stale credentials;
- expiring tokens with no renewal process;
- review bots that block instead of assist;
- branch rules that prevent autonomous merges;
- excessive approval gates;
- missing automated quality gates;
- agents completing one issue and stopping;
- agents failing once and stopping;
- agents losing context and stopping.

---

# Desired Architecture

At the end of this work, we should be moving toward an EngineAI delivery pipeline roughly equivalent to:

**Client conversation**

↓  
Fireflies

↓  
AI discovery analysis

↓  
PRD / approved scope

↓  
Linear project + sequenced issues

↓  
Autonomous development agent

↓  
Implementation

↓  
Automated tests / lint / typecheck / security / acceptance validation

↓  
PR

↓  
Automated review + remediation

↓  
Autonomous merge when gates pass

↓  
Deployment

↓  
Production verification

↓  
Linear/project state updated

↓  
Agent continues to next issue

↓  
Project complete

↓  
Monitoring / maintenance loop

Joe and Ben remain **above the execution layer**, not inside it.

---

# Deliverables

Maintain a working audit as you progress, but prioritise implementing improvements over writing about them.

At the end provide:

## 1. Autonomy Scorecard

Rate major areas such as:

- Codex/runtime
- local development environment
- GitHub
- repository standards
- credentials/secrets
- third-party integrations
- Linear
- CI
- PR lifecycle
- deployment
- state persistence
- failure recovery
- observability
- maintenance

Use a simple status:

- GREEN — autonomous
- AMBER — partially autonomous
- RED — requires human intervention

## 2. Human Intervention Register

List every remaining situation in which Joe or Ben could still need to intervene.

For each include:

- trigger;
- current reason;
- whether it is legitimate;
- proposed long-term elimination/mitigation.

The ideal result is a very short register.

## 3. Changes Implemented

Show what you actually changed during this session.

Include:

- files;
- configurations;
- GitHub settings;
- workflows;
- scripts;
- permissions;
- integrations;
- documentation;
- tooling.

## 4. Remaining Blockers

Separate these into:

**Agent-solvable**

Continue solving these rather than merely listing them.

**Requires one-time human bootstrap**

Only include items you genuinely cannot perform.

**Intentionally human-controlled**

Explain why these should remain human-controlled.

## 5. Ultimate Autonomous Development Architecture

Produce the recommended final operating architecture for EngineAI showing how:

Fireflies → PRD → Linear → Agent → GitHub → CI → Deployment → Monitoring → Maintenance

works without routine founder involvement.

---

# Definition of Done

Do not consider this task complete because you have produced a good audit document.

Completion means you have:

- inspected the real environment available to you;
- audited the major autonomy surfaces;
- identified human dependencies;
- implemented all safe changes possible within your authority;
- verified those changes where possible;
- reduced unnecessary approval points;
- established clear automated quality gates;
- established or designed reliable agent identity/secrets access;
- established an autonomous PR-to-deployment path;
- ensured agents can continue through Linear work rather than stopping after one issue;
- established failure-recovery expectations;
- established state/handoff mechanisms;
- documented the very small number of legitimate remaining human escalation cases.

Continue iterating until no additional material autonomy blockers can be found within the accessible environment.

Do not stop after discovering problems.

**Discover → fix → test → continue auditing.**

The ultimate test is:

> Could Joe and Ben approve a PRD today, hand the project over, close their laptops, and reasonably expect the development system to continue progressing toward a tested production deployment without routine human intervention?

Anything that makes the answer **no** is within scope for this audit.
