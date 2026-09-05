---
name: solution-template-factory
description: >
  Build an EngineAI system that turns a solution category or a concrete client problem into
  a reusable solution template, then a first client implementation scaffolded from that
  template. Use when asked for "solution template factory", "solution template", "template
  then implement", "category template", or to industrialise delivery of a repeatable
  solution shape before scaffolding the first client build.
---

Build an EngineAI system for turning either:

1. a real project we have already completed or substantially built, or
2. a new solution/product/agent idea we want to standardise,

into a reusable **solution template + implementation runbook + reference architecture + starter repository** that EngineAI can rapidly reuse for future clients.

The goal is to progressively build a library of high-quality EngineAI solution templates so that when a new client needs something similar, we do not start from zero.

These templates may also become:
- sales/demo environments showing clients what is possible;
- live examples linked from the EngineAI website;
- starting points for client discovery and scoping;
- accelerators for autonomous project delivery;
- internal reference architectures and engineering runbooks.

Do not treat this as merely a questionnaire or documentation generator. Design it as an **EngineAI Solution Template Factory**.

## Core outcome

Create an interactive questionnaire/workflow that guides me through turning a project or concept into a reusable EngineAI template.

The workflow should be intelligent enough that I can provide relatively rough information and the system researches, inspects and infers the rest where safe.

It should support two primary modes:

### Mode A — Extract from an existing project

I identify a completed or substantially completed EngineAI/client project.

The system should inspect the available evidence rather than relying solely on my answers.

Depending on the project, relevant evidence may include:
- GitHub repository/codebase;
- README and technical documentation;
- Linear project, PRD and issues;
- client discovery material;
- Fireflies transcripts;
- Google Drive documentation;
- Slack discussions;
- Gmail threads;
- architecture diagrams;
- deployment configuration;
- external APIs/services;
- Supabase/database schemas;
- agent prompts and tools;
- tests and evaluations;
- UX/UI implementation;
- operating procedures.

Determine what was actually built, why it was built, the problem it solves, which parts are client-specific, and which parts are reusable.

Then abstract the reusable system from the client implementation.

Do **not** blindly clone a client repository and call it a template.

Remove or parameterise:
- client names and branding;
- credentials and secrets;
- client-specific data;
- hard-coded identifiers;
- environment-specific URLs;
- one-off business rules;
- unnecessary technical debt;
- historical implementation artefacts;
- client-specific integrations unless they are fundamental to the template.

Retain and improve:
- proven workflows;
- architecture patterns;
- agent architecture;
- schemas;
- integration patterns;
- evaluation approaches;
- deployment patterns;
- UX patterns;
- governance;
- observability;
- reusable prompts/skills;
- test infrastructure;
- lessons learned.

### Mode B — Create from an idea

I describe an idea, opportunity or solution in plain language.

Use an intelligent questionnaire plus research/discovery to determine:
- the problem;
- target user;
- target industry or industries;
- desired outcome;
- primary workflow;
- system boundaries;
- whether this should be a web application, mobile web application, headless agent, multi-agent system, automation, API/service, knowledge system, integration architecture, or another pattern;
- required integrations;
- required human involvement;
- autonomy requirements;
- UX requirements;
- data model;
- security/governance considerations;
- reusable versus optional modules;
- deployment/runtime expectations.

Do not make me answer questions that can safely be derived from existing EngineAI knowledge, repositories, connected tools or sensible technical investigation.

Ask me only when a decision is genuinely material and cannot safely be inferred.

---

# Interactive questionnaire

Design a polished interactive questionnaire rather than a giant static form.

It should progressively reveal questions based on previous answers.

Start with something like:

**What are we creating a template from?**
- Existing EngineAI/client project
- New idea/concept

From there, dynamically branch.

The questionnaire should feel like an expert EngineAI solution architect interviewing me.

It should capture or derive at minimum:

### 1. Template identity
- working name;
- template category;
- industry applicability;
- core capability;
- one-sentence description.

### 2. Problem
- problem being solved;
- current/manual workflow;
- pain points;
- desired outcome;
- measurable value/ROI where appropriate.

### 3. Users
- primary user;
- secondary users;
- administrators/operators;
- external participants.

### 4. Workflow
Capture the important end-to-end workflow.

Distinguish:
- trigger;
- inputs;
- agent/system actions;
- integrations;
- human checkpoints;
- outputs;
- downstream actions;
- exceptions/failure handling.

### 5. Architecture
Determine the appropriate architecture rather than forcing one.

Examples include:
- web application;
- mobile web application;
- headless agent;
- autonomous agent service;
- multi-agent system;
- AI workflow;
- API/integration service;
- knowledge/Brain architecture;
- dashboard/cockpit;
- hybrid system.

### 6. AI-native characteristics
Determine:
- what should be deterministic;
- what should use models;
- what should be agentic;
- required tools;
- memory/context requirements;
- retrieval requirements;
- autonomy level;
- HITL/HOTL boundaries;
- approval gates;
- evaluation strategy;
- failure recovery.

Prefer **agent-first architectures** where appropriate rather than bolting an LLM onto a conventional CRUD application.

### 7. Integrations
Identify:
- mandatory integrations;
- optional integrations;
- common alternatives;
- authentication model;
- APIs/webhooks/MCP/tools;
- reusable adapters.

### 8. Data
Identify:
- core entities;
- required persistence;
- schemas;
- audit/provenance requirements;
- tenant isolation;
- privacy/security requirements;
- example/demo data.

### 9. UX/UI
For user-facing systems determine:
- primary journeys;
- information hierarchy;
- interaction model;
- mobile requirements;
- dashboard requirements;
- onboarding;
- empty states;
- errors;
- approval/intervention surfaces.

The resulting template should have a **world-class product-quality UX**, not generic AI-generated dashboard UI.

### 10. Reusability
Explicitly classify functionality into:

**Core**
Required for every implementation of this template.

**Modules**
Reusable optional capabilities.

**Adapters**
Client/system-specific integrations.

**Configuration**
Values that vary between deployments.

**Example implementation**
Demonstration configuration/data illustrating the template.

### 11. Deployment and operations
Determine:
- hosting;
- database;
- runtime;
- queues/background workers where relevant;
- secrets;
- monitoring;
- logs;
- traces;
- evals;
- CI/CD;
- rollback/recovery;
- ongoing agent operation.

### 12. Commercial/demo use
Determine whether the template should support:
- internal-only usage;
- client demos;
- public EngineAI website showcase;
- live sandbox;
- sales discovery;
- production deployment.

Public/demo modes must never expose real client information.

---

# Template classification and repository naming

Every generated solution must have a clear **template type**.

Do not create ambiguous repositories such as `client-template` or `ai-template`.

Use a consistent convention based on architecture/capability.

Examples:

- `template-webapp-recruitment-transcriber`
- `template-webapp-compliance-cockpit`
- `template-headless-agent-lead-qualification`
- `template-headless-agent-document-processing`
- `template-agentic-workflow-candidate-onboarding`
- `template-company-brain-professional-services`
- `template-integration-jobadder-ai`
- `template-multi-agent-client-delivery`

You may improve the convention if repository research identifies a stronger EngineAI standard.

The name should tell an engineer immediately:
1. that this is a template;
2. what architectural class it belongs to;
3. what capability it provides.

---

# GitHub implementation

Create the resulting template repository in:

**GitHub organisation:** `engineai-nz`

Use:

https://github.com/engineai-nz/engine-ai-starter

as the required starting point unless inspection demonstrates that doing so would materially conflict with the template architecture.

Inspect the starter repository before implementing anything.

Preserve and use its intended EngineAI development conventions rather than copying files blindly.

Also inspect:

https://github.com/engineai-nz/engine-ai-os

where relevant.

`engine-ai-os` is optional context, not a mandatory dependency.

Use it only where it helps align the generated template with EngineAI's wider delivery methodology, autonomous development lifecycle, project structure or operating standards.

Do not introduce unnecessary coupling to `engine-ai-os`.

---

# Repository output

A generated template repository should be **usable**, not an empty scaffold accompanied by documentation.

Where relevant it should include:

- functioning reference implementation;
- reusable core architecture;
- clean module boundaries;
- sample/demo configuration;
- `.env.example`;
- appropriate schemas/migrations;
- integration interfaces/adapters;
- agent definitions;
- prompts/skills;
- tool contracts;
- representative tests;
- evals where AI behaviour matters;
- fixtures/sample data;
- deployment configuration;
- architecture documentation;
- implementation runbook.

Create an excellent root README that explains:

**What this template is**

**What problem it solves**

**When EngineAI should use it**

**What it demonstrates**

**Reference architecture**

**Core workflow**

**Core / Modules / Adapters / Configuration**

**How to run it**

**How to demo it**

**How to create a new client implementation from it**

**What needs changing for each client**

**What must never be copied from another client**

**Testing and evaluation**

**Deployment**

**Known limitations**

---

# Implementation runbook

Produce a runbook that another autonomous coding agent could use to take this template and build a client implementation with minimal human assistance.

It should cover approximately:

Client requirement
→ template selection
→ discovery
→ configuration
→ integration selection
→ branding/customisation
→ data/schema changes
→ implementation
→ testing/evals
→ security checks
→ deployment
→ acceptance
→ monitoring.

The runbook should identify what an agent can decide autonomously versus the small number of decisions that genuinely require EngineAI/client intervention.

---

# Template manifest

Design a machine-readable manifest for every template.

For example, a `template.yaml`, `template.json` or better equivalent.

It should allow future tooling to understand things such as:

- template ID;
- name;
- type;
- capability;
- industries;
- maturity;
- description;
- architecture;
- runtime;
- AI/agent capabilities;
- integrations;
- modules;
- dependencies;
- configuration;
- deployment options;
- demo availability;
- source project/provenance where applicable;
- required secrets;
- required human approvals;
- tests;
- evals.

Choose the schema carefully.

The longer-term intention is that EngineAI should eventually be able to maintain a catalogue of these templates and allow an agent to discover the closest existing template automatically when a new client project is created.

Design this first implementation so we do not block that future capability.

---

# Provenance and lessons learned

When extracting a template from an existing project, preserve useful provenance without exposing confidential information.

Document:
- what project/pattern the template originated from;
- which design decisions proved successful;
- failures or approaches that should not be repeated;
- important architectural trade-offs;
- reusable lessons;
- known constraints.

Treat completed projects as organisational learning, not merely source code.

---

# Future template catalogue

Architect the solution with a future EngineAI **Template Catalogue / Solution Library** in mind.

Eventually I want to be able to browse something like:

**Recruitment**
- AI Meeting Transcriber
- Candidate Screening Agent
- Workforce Availability Cockpit

**Real Estate**
- Listing Compliance Agent
- Marketing Content Engine

**Professional Services**
- Company Brain
- Client Intake Agent

and select:

**Create client project from this template**

Do not overbuild the catalogue now unless it is naturally required for the first version, but make the generated template metadata compatible with this direction.

---

# Quality bar

Do not create "vibe-coded" template repositories.

A template is more important than a one-off client build because bad architectural decisions will propagate into multiple future projects.

Therefore aggressively remove:
- unnecessary abstraction;
- fragile shortcuts;
- fake/demo-only architecture presented as production ready;
- duplicated logic;
- hard-coded client assumptions;
- generic AI wrappers;
- poor UI;
- placeholder tests;
- dead code;
- speculative complexity.

Prefer:
- strong primitives;
- explicit interfaces;
- composability;
- replaceable adapters;
- sensible defaults;
- autonomous operation;
- observability;
- testability;
- clear documentation.

A future EngineAI developer or agent should be able to understand why the system exists and spin up a new client implementation without reverse-engineering the original project.

---

# Execution approach

Do not stop after proposing an architecture.

Execute the work.

1. Inspect `engine-ai-starter`.
2. Inspect `engine-ai-os` only to the extent relevant.
3. Inspect existing EngineAI conventions/templates if any already exist.
4. Determine how this Template Factory should fit into the ecosystem.
5. Design the interactive questionnaire and template schema.
6. Build the questionnaire/workflow.
7. Implement generation/extraction logic necessary for a useful first version.
8. Establish the repository/template naming convention.
9. Create the appropriate new GitHub repository/repositories in `engineai-nz`.
10. Build at least one end-to-end representative template flow so the architecture is proven.
11. Test it.
12. Review the generated template as though another autonomous agent must use it without additional explanation.
13. Fix deficiencies found during that review.
14. Update documentation.
15. Leave the system in a working, usable state.

Use existing credentials, integrations and permissions where available.

Do not repeatedly ask for approval for routine engineering decisions.

Make safe, reversible implementation decisions autonomously.

Escalate only where:
- credentials/permissions genuinely block execution;
- an irreversible external action is required;
- material commercial/client decisions cannot safely be inferred;
- there is a genuine architectural fork with materially different business outcomes.

If something is blocked, continue all other unblocked work rather than stopping the entire task.

---

# Definition of done

This work is complete when:

- there is a polished interactive questionnaire/workflow;
- it supports both **existing project → reusable template** and **idea → reusable template**;
- the system intelligently derives information rather than forcing the user to manually specify everything;
- templates have a defined taxonomy and naming convention;
- templates have a machine-readable manifest;
- templates distinguish core functionality, modules, adapters and configuration;
- generated output contains a practical implementation runbook;
- an appropriate repository can be created under `engineai-nz` from `engine-ai-starter`;
- generated repositories are usable starter implementations rather than documentation shells;
- architecture supports web apps, headless agents and other EngineAI solution types rather than assuming everything is a web app;
- existing projects can be sanitised and abstracted without leaking client-specific information;
- there is a clear path toward a future EngineAI Template Catalogue;
- at least one complete generation/extraction path has been demonstrated and validated;
- tests/evals appropriate to the implementation pass;
- documentation is sufficient for another autonomous agent to take a generated template and build a client project from it.

At the end, report:

1. what you discovered;
2. architecture chosen;
3. questionnaire/workflow created;
4. repository/repositories created;
5. template taxonomy/naming convention;
6. manifest design;
7. example template produced;
8. tests/evals performed;
9. anything deliberately deferred and why;
10. any genuine blockers remaining.

Continue through implementation and remediation until the definition of done is satisfied rather than stopping after the first successful scaffold.
