# Engine AI skills

This repository contains Engine AI product and operator skills. Joe’s shared
engineering and delivery policy belongs to
[Joe’s Engineering Playbook](https://github.com/engineai-nz/joes-engineering-playbook).
Offering/runbook skills belong to
[engine-ai-os](https://github.com/engineai-nz/engine-ai-os), including
`project-workflow` and `engineai-demo-package`. Pstack and Matt Pocock skills keep
their existing upstream owners and installations; this tool does not manage them.

There is no full-environment installer in this repository. Skills, account
instructions, hooks, security settings and schedulers have different owners.
Filesystem presence does not prove that a harness loaded a skill.

## Verified drift and proposal tool

`sync-skills.py` is read-only. It replaces the former laptop-to-main publisher
without installing files, deleting destination extras, staging, committing or
pushing. Every invocation names one skill from the repository allowlist.
`--apply` always returns a blocked result, even with a revision, fingerprint and
backup path. No installation or backup write occurs.

Compare one installed skill with the committed repository version:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills"
```

The repository source comes from immutable Git tree/blob bytes and executable
modes, rather than the working tree or index. The report records the resolved
commit SHA. Ignored files, untracked files, working-tree edits and index flags
such as `assume-unchanged` cannot silently become repository source. No remote is
fetched; local HEAD does not prove freshness or review approval.

To inspect a particular reviewed commit, supply its full SHA:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills" \
  --source-revision '<full-reviewed-commit-sha>'
```

Missing source entries, symlinks and unsupported paths fail closed.
`preserved_extras` reports destination files absent from the source, never a
deletion request. Volatile caches and dependency folders are excluded. Local
fingerprints are observations, not locks or transaction guarantees; coordinate
custody and repeat inspection if another owner is editing the files.

To propose a local improvement, request a named review diff:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills" \
  --direction local-to-repo --source-revision '<full-reviewed-commit-sha>'
```

Review that diff for private data and obsolete doctrine. Apply any accepted
repository edits on an owned branch through the existing PR, review and CI gates.
This command cannot promote local files or push `main`.

## Installation boundary

A generic installer remains deferred. A supported installation route must prove
source authenticity, exclusive target custody, no-follow filesystem traversal,
protection against intervening custom edits, and durable receipt/recovery through
finalization. A path check followed by replacement does not establish those
properties. This repository adds no installer infrastructure or scheduler.

Bounded direct alignment of named instruction files can still use existing
filesystem tools, reviewed canonical text, backups and immediate conflict checks
under the user’s authority. That is separate from a generic transactional install
claim. Existing security gates, dirty work and explicit pauses remain binding.
There is no rollback procedure for this tool because it performs no writes.

## Validation

Fixture tests use disposable repositories and local observations, with no network:

```sh
python3 -B -m unittest discover -s tests -v
```

They cover stale local doctrine, unrelated staged/unstaged work, ignored private
files, index flags, missing sources, repeated reports, revision validation, path
traversal, symlinks, source changes during Git reads and no-mutation apply refusal.
The no-write boundary prevents the former concurrent-edit, parent-swap and final
receipt failure paths from being entered. These tests do not prove an installer,
a live harness load or an unattended wake path.

## Included skills

The allowlist in `sync-skills.py` defines the reported subset: the GEO suite under
`geo/`, review skills under `review/`, and named standalone operator skills.
Other repository content is not automatically installed or inspected.
