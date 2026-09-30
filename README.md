# Engine AI skills

This repository contains Engine AI product and operator skills. Joe’s shared
engineering and delivery policy belongs to
[Joe’s Engineering Playbook](https://github.com/engineai-nz/joes-engineering-playbook).
Offering/runbook skills belong to
[engine-ai-os](https://github.com/engineai-nz/engine-ai-os), including
`project-workflow` and `engineai-demo-package`. Pstack and Matt Pocock skills keep
their existing upstream owners and installations; this tool does not manage them.

There is no full-environment installer in this repository. Skills, account
instructions, hooks, security settings and schedulers have different owners;
copying one does not establish a working runtime or authorize a product build.

## Inspect drift first

`sync-skills.py` replaces the former laptop-to-main publisher. It never stages,
commits, pushes, removes destination extras or edits account configuration.
Every invocation names one skill from the repository allowlist. Missing sources,
symlinks and unsupported paths fail closed. With no `--apply`, it only reports
file drift and fingerprints, without creating backups or directories:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills"
```

The default direction is repository to installation. Local custom changes remain
intact. `preserved_extras` lists destination files absent from the source; they
are never treated as deletion requests. Volatile caches and dependency folders
are excluded from drift comparison.

To propose a local improvement, request a named review diff:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills" \
  --direction local-to-repo
```

This direction is always read-only. Review the diff for private data and obsolete
doctrine, then apply any accepted edits on an owned branch through existing PR,
review and CI gates. It cannot promote local files or push `main`.

## Install an explicitly reviewed revision

After reviewing the exact repository commit and target drift, installation
requires all of:

- The full reviewed commit SHA, matching the checkout’s HEAD. The selected skill
  must be tracked and free of staged, unstaged and untracked changes.
- The target fingerprint from the drift report (or `absent` for a new skill).
- A new backup directory outside both repository and installation trees. Existing
  backup directories, overlapping trees and symlinked paths are rejected.

For example, replace both placeholders with the values actually reviewed:

```sh
python3 sync-skills.py --skill brand --live-dir "$HOME/.claude/skills" --apply \
  --source-revision '<full-reviewed-commit-sha>' \
  --expect-target '<target-fingerprint-from-drift-report>' \
  --backup-dir '<new-external-backup-directory>'
```

There is no default approved SHA, automatic update, model preference change or
scheduler. Unrelated dirty repository files are untouched. Source changes during
installation invalidate the operation. Destination writes replace each file
atomically. Changed target files block overwrites. A failed copy restores files
written by this invocation when they still match its installed content; competing
edits are retained and marked `rollback-conflict`.

A successful install emits the backup location and new target fingerprint. An
already aligned target is a no-op and needs no new backup. Restart or explicitly
reload the consuming harness and verify the skill appears in its actual catalogue;
filesystem presence is not loading evidence.

## Recovery and validation

The backup contains `original/` for a pre-existing target plus `receipt.json`,
which records the source revision, before fingerprint, changed/created file names
and result. Keep backups private; local skills can contain private references.

For manual rollback, stop competing edits, compare current files with the reviewed
installed source, restore only receipt-listed changed files from `original/`
with their modes, and remove only receipt-listed newly created files after
confirming they are still this installation’s content. Preserve all destination
extras and later local edits. If the receipt says `rollback-conflict`, inspect
those files before restoration. Do not blindly replace the whole installation.

Fixture tests use disposable repositories and installations, with no network:

```sh
python3 -m unittest discover -s tests -v
```

They cover stale local doctrine, unrelated dirty work, absent sources, no
implicit deletion, repeated installs, reviewed revision and fingerprint checks,
path traversal, symlinks, backup overlap, source changes during installation and
mid-copy recovery. Passing fixtures prove these code paths; they do not prove
that any live Mac installation or scheduler was exercised.

## Included skills

The allowlist in `sync-skills.py` defines the managed subset: the GEO suite under
`geo/`, review skills under `review/`, and named standalone operator skills.
Other content in this repository is not automatically installed. Existing PR
holds, including the human skim on PR #6 and draft AI-news cron PR #1, remain
binding; this tool neither activates them nor releases those holds.
