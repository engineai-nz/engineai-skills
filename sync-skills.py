#!/usr/bin/env python3
"""Read-only named-skill drift/proposals from immutable Git source objects.

This tool is not an installer. Apply requests fail closed, without writes.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).absolute().parent

SKILLS = {
    # GEO suite
    "geo": "geo",
    "geo-audit": "geo",
    "geo-brand-mentions": "geo",
    "geo-citability": "geo",
    "geo-compare": "geo",
    "geo-content": "geo",
    "geo-crawlers": "geo",
    "geo-llmstxt": "geo",
    "geo-platform-optimizer": "geo",
    "geo-proposal": "geo",
    "geo-prospect": "geo",
    "geo-report": "geo",
    "geo-report-pdf": "geo",
    "geo-schema": "geo",
    "geo-technical": "geo",
    # Review
    "adversarial-review": "review",
    "code-combat": "review",
    # Engine AI delivery / general-purpose operator skills (standalone at repo root)
    "autonomous-development-environment": None,
    "brand": None,
    "humaniser": None,
    "project-sweep": None,
    "solution-template-factory": None,
    # June 2026: personal/session/meta/infra skills moved to benduchateau/dotclaude.
    # This repo holds Engine AI product skills only.
    # July 2026: runbook-paired skills (engineai-demo-package, project-workflow) live in
    # engineai-nz/engine-ai-os under Skills/, where lifecycle_audit --strict enforces the
    # Offer->Service->Playbook->Runbook->Skill chain. Syncing them from a laptop let a
    # stale copy overwrite canon. Do not re-add them here.
    # Sep 2026: project-sweep, solution-template-factory, and autonomous-development-environment
    # are general-purpose operator skills (not Offer-chain). They live here as standalone
    # roots, same as brand/humaniser. Offer-chain runbook skills stay in engine-ai-os.
}



SKIP_FILES = {".DS_Store", "Zone.Identifier", "Thumbs.db"}
SKIP_DIRS = {".venv", "venv", "node_modules", "__pycache__", ".git"}


class Conflict(RuntimeError):
    """A read precondition failed, or a write was requested."""


def safe_path(path):
    path = Path(os.path.abspath(path))
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise Conflict(f"Symlink is not a supported inspection path: {item}")
    return path


def snapshot(root):
    """Observe local files for a proposal; never an installation source."""
    root = safe_path(root)
    if not root.exists():
        return None
    if not root.is_dir():
        raise Conflict(f"Expected a skill directory: {root}")
    files = {}
    for base, dirs, names in os.walk(root):
        for name in dirs + names:
            if (Path(base) / name).is_symlink():
                raise Conflict(f"Symlink inside skill: {Path(base) / name}")
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if name in SKIP_FILES or name.endswith(".pyc"):
                continue
            path = Path(base) / name
            if not path.is_file():
                raise Conflict(f"Unsupported skill entry: {path}")
            files[path.relative_to(root).as_posix()] = (
                path.read_bytes(), path.stat().st_mode & 0o777)
    return files


def fingerprint(files):
    if files is None:
        return "absent"
    digest = hashlib.sha256()
    for name, (data, mode) in sorted(files.items()):
        digest.update(json.dumps([name, mode, hashlib.sha256(data).hexdigest()],
                                 separators=(",", ":")).encode() + b"\n")
    return digest.hexdigest()


def committed_snapshot(repo, relative, revision=None):
    """Read every source byte/mode from a commit tree, regardless of index flags."""
    def git(*args):
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, check=True).stdout
    if revision is None:
        revision = git("rev-parse", "HEAD").decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision):
        raise Conflict("Source revision must be a full commit SHA")
    git("cat-file", "-e", revision + "^{commit}")
    files = {}
    for entry in git("ls-tree", "-r", "-z", revision, "--", relative).split(b"\0"):
        if not entry:
            continue
        metadata, path_bytes = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        path = path_bytes.decode("utf-8")
        prefix = relative + "/"
        if not path.startswith(prefix):
            raise Conflict("Git tree entry escaped the named skill")
        name = path[len(prefix):]
        parts = Path(name).parts
        if not parts or any(part in [".", ".."] for part in parts) or Path(name).is_absolute():
            raise Conflict("Unsupported Git tree path")
        if kind != "blob" or mode not in ["100644", "100755"]:
            raise Conflict(f"Unsupported committed entry (symlink/submodule): {path}")
        if any(part in SKIP_DIRS for part in parts[:-1]) or parts[-1] in SKIP_FILES or name.endswith(".pyc"):
            continue
        files[name] = (git("cat-file", "blob", oid), 0o755 if mode == "100755" else 0o644)
    if "SKILL.md" not in files:
        raise Conflict(f"Missing committed SKILL.md at {revision}:{relative}")
    return revision, files


def paths(repo, live, name):
    if name not in SKILLS:
        raise Conflict(f"Skill is outside the repository allowlist: {name}")
    repo, live = safe_path(repo), safe_path(live)
    relative = str(Path(SKILLS[name] or "") / name)
    source, target = safe_path(repo / relative), safe_path(live / name)
    for left, right in [(repo, live), (live, repo)]:
        if left == right or left in right.parents:
            raise Conflict("Repository and installation roots must not overlap")
    return repo, source, target, relative


def proposal(src, dst):
    diffs = []
    for name, (data, mode) in sorted(src.items()):
        before, old_mode = (dst or {}).get(name, (b"", 0))
        if old_mode != mode:
            diffs.append(f"Mode proposal {name}: {oct(old_mode)} -> {oct(mode)}\n")
        if before == data:
            continue
        try:
            old, new = before.decode("utf-8"), data.decode("utf-8")
            diffs.append("".join(difflib.unified_diff(
                old.splitlines(keepends=True), new.splitlines(keepends=True),
                fromfile="repository/" + name, tofile="local-proposal/" + name)))
        except UnicodeDecodeError:
            diffs.append(f"Binary content differs: {name} (review separately)\n")
    return "".join(diffs)


def install(*args, **kwargs):
    # No precheck + path-based replace can promise atomic protection from an
    # uncooperative concurrent writer. Keep this boundary unconditionally closed.
    raise Conflict("Installation is unavailable: this is a read-only drift/proposal tool. "
                   "Use a separately reviewed, supported install route with verified "
                   "target custody, no-follow traversal and durable recovery.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True, choices=sorted(SKILLS))
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--live-dir", type=Path, default=Path.home() / ".claude/skills")
    parser.add_argument("--direction", choices=["repo-to-local", "local-to-repo"], default="repo-to-local")
    parser.add_argument("--source-revision", help="Full commit SHA; default resolves and reports local HEAD")
    parser.add_argument("--apply", action="store_true", help="Unsupported; always fails without writes")
    # Parse prior callers explicitly instead of silently accepting unsafe apply.
    parser.add_argument("--expect-target", help=argparse.SUPPRESS)
    parser.add_argument("--backup-dir", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.apply:
            install()
        if args.expect_target or args.backup_dir:
            raise Conflict("Installation options are unsupported; no files were changed")
        repo, source, target, relative = paths(args.repo_root, args.live_dir, args.skill)
        revision, committed = committed_snapshot(repo, relative, args.source_revision)
        local = snapshot(target)
        src, dst = committed, local
        if args.direction == "local-to-repo":
            if local is None or "SKILL.md" not in local:
                raise Conflict(f"Missing local proposal SKILL.md: {target}")
            src, dst = local, committed
        changes = [name for name, value in sorted(src.items()) if (dst or {}).get(name) != value]
        extras = sorted(set(dst or {}) - set(src))
        result = {"result": "drift" if changes or extras else "unchanged", "direction": args.direction,
                  "repository_commit": revision, "repository_source": "immutable Git tree/blob bytes and modes",
                  "local_path": str(target), "source_fingerprint": fingerprint(src),
                  "target_fingerprint": fingerprint(dst), "changed_files": changes,
                  "preserved_extras": extras, "installation_available": False}
        if args.direction == "local-to-repo":
            result["review_only_diff"] = proposal(src, dst)
        print(json.dumps(result, indent=2))
        return 0
    except (Conflict, OSError, ValueError, UnicodeError, subprocess.CalledProcessError) as error:
        print(json.dumps({"result": "blocked", "reason": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
