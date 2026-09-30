#!/usr/bin/env python3
"""Report skill drift; install an explicitly reviewed repository skill on request.

Never stage, commit, push, delete destination extras, or promote local files.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
    """A precondition failed without authorising a write."""


def safe_path(path):
    path = Path(os.path.abspath(path))
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise Conflict(f"Symlink is not an owned install path: {item}")
    return path


def snapshot(root):
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


def check_revision(repo, revision, relative):
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision or ""):
        raise Conflict("Install requires the full reviewed --source-revision commit SHA")
    def git(*args):
        result = subprocess.run(["git", "-C", str(repo), *args],
                                text=True, capture_output=True, check=True)
        return result.stdout.strip()
    if git("rev-parse", "HEAD") != revision:
        raise Conflict("Repository HEAD differs from the reviewed source revision")
    if git("status", "--porcelain", "--untracked-files=all", "--", relative):
        raise Conflict("Selected repository skill has local or staged changes")
    if not git("ls-files", "--", relative + "/SKILL.md"):
        raise Conflict("Selected SKILL.md is not tracked at the reviewed revision")


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


def drift(source, target):
    src, dst = snapshot(source), snapshot(target)
    if src is None or "SKILL.md" not in src:
        raise Conflict(f"Missing source SKILL.md: {source}")
    current = dst or {}
    changes = [name for name, value in sorted(src.items()) if current.get(name) != value]
    extras = sorted(set(current) - set(src))
    return src, dst, changes, extras


def proposal(src, dst):
    diffs = []
    for name, (data, _) in sorted(src.items()):
        before = (dst or {}).get(name, (b"", 0))[0]
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


def install(repo, source, target, relative, revision, expected, backup_root):
    backup_root = safe_path(backup_root)
    for root in [repo, target.parent]:
        if backup_root == root or root in backup_root.parents or backup_root in root.parents:
            raise Conflict("Backup root must be external to repository and installation")
    if backup_root.exists():
        raise Conflict("Backup directory already exists; choose a new directory")
    check_revision(repo, revision, relative)
    src, dst, changes, extras = drift(source, target)
    if fingerprint(dst) != expected:
        raise Conflict("Installation changed since review; target fingerprint differs")
    if not changes:
        return {"result": "unchanged", "preserved_extras": extras}
    # Check file/directory collisions before backing up or writing.
    for name in changes:
        path = target / name
        if path.exists() and not path.is_file():
            raise Conflict(f"File conflicts with directory: {path}")
        for parent in path.parents:
            if parent == target.parent:
                break
            if parent.exists() and not parent.is_dir():
                raise Conflict(f"Directory conflicts with file: {parent}")
    check_revision(repo, revision, relative)
    if snapshot(source) != src or snapshot(target) != dst:
        raise Conflict("Source or target changed during preflight")
    backup_root.mkdir(parents=True)
    if target.exists():
        shutil.copytree(target, backup_root / "original", symlinks=True)
    manifest = {"source_revision": revision, "source_fingerprint": fingerprint(src),
                "target": str(target), "target_fingerprint": fingerprint(dst),
                "changed_files": changes, "created_files": [n for n in changes if n not in (dst or {})],
                "status": "prepared"}
    receipt = backup_root / "receipt.json"
    receipt.write_text(json.dumps(manifest, indent=2) + "\n")
    written, made_dirs = [], []
    try:
        for name in changes:
            # Source changes invalidate the approved snapshot; target races fail closed.
            check_revision(repo, revision, relative)
            if snapshot(source) != src:
                raise Conflict("Source changed after preflight")
            path = safe_path(target / name)
            old = (dst or {}).get(name)
            actual = (path.read_bytes(), path.stat().st_mode & 0o777) if path.is_file() else None
            if actual != old:
                raise Conflict(f"Target changed before write: {path}")
            missing = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                made_dirs.append(directory)
            data, mode = src[name]
            # Exclusive temp file inside the owned destination; replace is atomic per file.
            fd, temp_name = tempfile.mkstemp(prefix=".skill-sync-", dir=path.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(data)
                os.chmod(temp_name, mode)
                os.replace(temp_name, path)
            finally:
                if os.path.exists(temp_name):
                    os.unlink(temp_name)
            written.append(name)
        check_revision(repo, revision, relative)
        if snapshot(source) != src:
            raise Conflict("Source changed during installation")
        manifest["status"] = "installed"
    except Exception:
        # Restore only our writes, and do not overwrite another process's later edits.
        conflicts = []
        for name in reversed(written):
            try:
                path = safe_path(target / name)
                actual = (path.read_bytes(), path.stat().st_mode & 0o777) if path.is_file() else None
                if actual != src[name]:
                    conflicts.append(name)
                    continue
                old = (dst or {}).get(name)
                if old is None:
                    path.unlink()
                else:
                    path.write_bytes(old[0])
                    path.chmod(old[1])
            except (Conflict, OSError):
                conflicts.append(name)
        for directory in reversed(made_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        manifest["status"] = "rollback-conflict" if conflicts else "rolled-back"
        manifest["rollback_conflicts"] = conflicts
        receipt.write_text(json.dumps(manifest, indent=2) + "\n")
        raise
    receipt.write_text(json.dumps(manifest, indent=2) + "\n")
    return {"result": "installed", "backup": str(backup_root), "changed_files": changes,
            "preserved_extras": extras, "target_fingerprint": fingerprint(snapshot(target))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True, choices=sorted(SKILLS))
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--live-dir", type=Path, default=Path.home() / ".claude/skills")
    parser.add_argument("--direction", choices=["repo-to-local", "local-to-repo"], default="repo-to-local")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--source-revision")
    parser.add_argument("--expect-target")
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args(argv)
    try:
        repo, source, target, relative = paths(args.repo_root, args.live_dir, args.skill)
        if args.apply:
            if args.direction != "repo-to-local":
                raise Conflict("Local-to-repository is review-only; apply edits through a reviewed branch")
            if not args.expect_target or not args.backup_dir:
                raise Conflict("Install requires --expect-target and --backup-dir")
            result = install(repo, source, target, relative, args.source_revision,
                             args.expect_target, args.backup_dir)
        else:
            if args.direction == "local-to-repo":
                source, target = target, source
            src, dst, changes, extras = drift(source, target)
            result = {"result": "drift" if changes or extras else "unchanged", "direction": args.direction,
                      "source": str(source), "target": str(target),
                      "source_fingerprint": fingerprint(src), "target_fingerprint": fingerprint(dst),
                      "changed_files": changes, "preserved_extras": extras}
            if args.direction == "local-to-repo":
                result["review_only_diff"] = proposal(src, dst)
        print(json.dumps(result, indent=2))
        return 0
    except (Conflict, OSError, subprocess.CalledProcessError) as error:
        print(json.dumps({"result": "blocked", "reason": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
