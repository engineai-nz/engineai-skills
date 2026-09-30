"""Disposable fixtures only: no user installation or network access."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('sync_skills', Path(__file__).parents[1] / 'sync-skills.py')
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class SyncSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).absolute()
        self.repo = self.root / 'repo'
        self.live = self.root / 'live'
        self.repo.mkdir()
        self.live.mkdir()
        self.source = self.repo / 'brand'
        self.target = self.live / 'brand'
        self.source.mkdir()
        (self.source / 'SKILL.md').write_text('reviewed canon\n')
        (self.source / 'a.txt').write_text('reviewed reference\n')
        self.git('init', '-q')
        self.git('add', 'brand')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'fixture')
        self.revision = self.git('rev-parse', 'HEAD')
        self.backup = self.root / 'backup'

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], check=True,
                              text=True, capture_output=True).stdout.strip()

    def local(self):
        self.target.mkdir()
        (self.target / 'SKILL.md').write_text('local custom version\n')
        (self.target / 'extra.txt').write_text('keep local custom work\n')

    def run_cli(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = sync.main(['--repo-root', str(self.repo), '--live-dir', str(self.live),
                              '--skill', 'brand', *extra])
        return code, json.loads(out.getvalue() or err.getvalue())

    def apply(self, expected=None, backup=None):
        return sync.install(self.repo, self.source, self.target, 'brand', self.revision,
                            expected or sync.fingerprint(sync.snapshot(self.target)),
                            backup or self.backup)

    def test_default_stale_local_is_read_only_and_preserves_dirty_index(self):
        self.local()
        (self.repo / 'notes.txt').write_text('unrelated staged work')
        self.git('add', 'notes.txt')
        (self.repo / 'dirty.txt').write_text('unrelated unstaged work')
        before_repo, before_local = sync.snapshot(self.repo), sync.snapshot(self.live)
        status, staged = self.git('status', '--porcelain'), self.git('diff', '--cached')
        code, report = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(report['result'], 'drift')
        self.assertFalse(report['installation_available'])
        self.assertEqual(report['repository_commit'], self.revision)
        self.assertEqual(sync.snapshot(self.repo), before_repo)
        self.assertEqual(sync.snapshot(self.live), before_local)
        self.assertEqual(self.git('status', '--porcelain'), status)
        self.assertEqual(self.git('diff', '--cached'), staged)
        self.assertFalse(self.backup.exists())

    def test_local_to_canon_only_proposes_named_diff(self):
        self.local()
        before = sync.snapshot(self.repo)
        code, report = self.run_cli('--direction', 'local-to-repo')
        self.assertEqual(code, 0)
        self.assertIn('local custom version', report['review_only_diff'])
        self.assertEqual(sync.snapshot(self.repo), before)
        code, _ = self.run_cli('--direction', 'local-to-repo', '--apply')
        self.assertEqual(code, 2)
        self.assertEqual(sync.snapshot(self.repo), before)

    def test_install_requires_reviewed_full_sha(self):
        # Retain the fixture's entrypoint name for independent baseline repros.
        # No SHA, fingerprint or backup path enables application.
        for revision in [None, self.revision, 'f' * 40]:
            with self.assertRaises(sync.Conflict):
                sync.install(self.repo, self.source, self.target, 'brand', revision, 'absent', self.backup)
        self.assertFalse(self.target.exists())

    def test_git_source_excludes_ignored_private_and_untracked_files(self):
        (self.repo / '.gitignore').write_text('brand/private.txt\n')
        self.git('add', '.gitignore')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'ignore fixture')
        self.revision = self.git('rev-parse', 'HEAD')
        (self.source / 'private.txt').write_text('synthetic private data')
        (self.source / 'untracked.txt').write_text('unreviewed')
        sha, committed = sync.committed_snapshot(self.repo, 'brand', self.revision)
        self.assertEqual(sha, self.revision)
        self.assertNotIn('private.txt', committed)
        self.assertNotIn('untracked.txt', committed)
        self.assertFalse(self.target.exists())

    def test_assume_unchanged_and_skip_worktree_cannot_change_committed_source(self):
        for flag in ['--assume-unchanged', '--skip-worktree']:
            with self.subTest(flag=flag):
                self.git('update-index', flag, 'brand/SKILL.md')
                (self.source / 'SKILL.md').write_text('unreviewed local doctrine')
                _, committed = sync.committed_snapshot(self.repo, 'brand', self.revision)
                self.assertEqual(committed['SKILL.md'][0], b'reviewed canon\n')

    def test_replacement_commit_tree_and_blob_cannot_spoof_requested_sha(self):
        original_commit = self.revision
        original_tree = self.git('rev-parse', original_commit + '^{tree}')
        original_blob = self.git('rev-parse', original_commit + ':brand/SKILL.md')
        (self.source / 'SKILL.md').write_text('replacement unreviewed doctrine')
        self.git('add', 'brand/SKILL.md')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'replacement fixture')
        new_commit = self.git('rev-parse', 'HEAD')
        new_tree = self.git('rev-parse', 'HEAD^{tree}')
        new_blob = self.git('rev-parse', 'HEAD:brand/SKILL.md')
        for original, replacement in [(original_commit, new_commit), (original_tree, new_tree),
                                      (original_blob, new_blob)]:
            with self.subTest(object=original):
                self.git('replace', original, replacement)
                sha, committed = sync.committed_snapshot(self.repo, 'brand', original_commit)
                self.assertEqual(sha, original_commit)
                self.assertEqual(committed['SKILL.md'][0], b'reviewed canon\n')
                self.git('replace', '-d', original)

    def test_source_changes_during_git_read_still_return_committed_blobs(self):
        original = subprocess.run
        def edit_worktree(*args, **kwargs):
            result = original(*args, **kwargs)
            if 'ls-tree' in args[0]:
                (self.source / 'SKILL.md').write_text('changed after tree read')
            return result
        with patch.object(sync.subprocess, 'run', side_effect=edit_worktree):
            _, committed = sync.committed_snapshot(self.repo, 'brand', self.revision)
        self.assertEqual(committed['SKILL.md'][0], b'reviewed canon\n')

    def test_missing_committed_source_never_deletes_target(self):
        self.local()
        self.git('rm', '-q', 'brand/SKILL.md')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'missing source fixture')
        before = sync.snapshot(self.target)
        code, _ = self.run_cli()
        self.assertEqual(code, 2)
        self.assertEqual(sync.snapshot(self.target), before)

    def test_missing_local_source_never_deletes_canon(self):
        before = sync.snapshot(self.repo)
        code, _ = self.run_cli('--direction', 'local-to-repo')
        self.assertEqual(code, 2)
        self.assertEqual(sync.snapshot(self.repo), before)

    def test_repeated_reports_preserve_extras_and_create_nothing(self):
        self.local()
        before = sync.snapshot(self.root)
        first, second = self.run_cli(), self.run_cli()
        self.assertEqual(first, second)
        self.assertIn('extra.txt', first[1]['preserved_extras'])
        self.assertEqual(sync.snapshot(self.root), before)

    def test_path_traversal_outside_allowlist_rejected(self):
        for name in ['../brand', '/brand', 'brand/../../outside']:
            with self.assertRaises(sync.Conflict):
                sync.paths(self.repo, self.live, name)

    def test_symlinked_parent_target_and_committed_symlink_rejected(self):
        link = self.root / 'link'
        link.symlink_to(self.live, target_is_directory=True)
        with self.assertRaises(sync.Conflict):
            sync.paths(self.repo, link / 'nested', 'brand')
        self.target.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(sync.Conflict):
            sync.paths(self.repo, self.live, 'brand')
        self.target.unlink()
        (self.source / 'link.txt').symlink_to('a.txt')
        self.git('add', 'brand/link.txt')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'symlink fixture')
        with self.assertRaises(sync.Conflict):
            sync.committed_snapshot(self.repo, 'brand')

    def test_apply_calls_no_mutation_or_git_api_even_with_all_options(self):
        self.local()
        before = sync.snapshot(self.root)
        with contextlib.ExitStack() as stack:
            mocks = [stack.enter_context(patch.object(Path, name)) for name in
                     ['write_text', 'write_bytes', 'mkdir', 'chmod', 'unlink', 'rmdir', 'rename']]
            mocks += [stack.enter_context(patch.object(os, 'replace')),
                      stack.enter_context(patch.object(tempfile, 'mkstemp')),
                      stack.enter_context(patch.object(sync.subprocess, 'run'))]
            code, report = self.run_cli('--apply', '--source-revision', self.revision,
                '--expect-target', sync.fingerprint(sync.snapshot(self.target)),
                '--backup-dir', str(self.backup))
            self.assertEqual(code, 2)
            self.assertIn('read-only', report['reason'])
            for mock in mocks:
                mock.assert_not_called()
        self.assertEqual(sync.snapshot(self.root), before)

    def test_concurrent_edit_and_parent_swap_hooks_are_never_reached(self):
        self.local()
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'a.txt').write_text('outside owner data')
        before = sync.snapshot(self.root)
        with patch.object(tempfile, 'mkstemp', side_effect=AssertionError('race boundary reached')) as temp:
            with patch.object(os, 'replace', side_effect=AssertionError('replace boundary reached')) as replace:
                with self.assertRaises(sync.Conflict):
                    self.apply()
                temp.assert_not_called()
                replace.assert_not_called()
        self.assertEqual(sync.snapshot(self.root), before)

    def test_prepared_receipt_untouched_when_apply_is_blocked(self):
        self.local()
        self.backup.mkdir()
        receipt = self.backup / 'receipt.json'
        receipt.write_text('{"status":"prepared"}')
        before = sync.snapshot(self.root)
        with patch.object(Path, 'write_text', side_effect=OSError('fixture full disk')) as write:
            with self.assertRaises(sync.Conflict):
                self.apply()
            write.assert_not_called()
        self.assertEqual(sync.snapshot(self.root), before)

    def test_backup_overlap_is_never_created_or_written(self):
        for backup in [self.repo / 'backups', self.live / 'backups', self.root, self.target / 'backup']:
            with self.assertRaises(sync.Conflict):
                self.apply(backup=backup)
        self.assertFalse(self.target.exists())

    def test_invalid_revision_blocked_without_mutation(self):
        before = sync.snapshot(self.root)
        for revision in ['main', 'HEAD', 'bad-sha', 'f' * 40]:
            code, _ = self.run_cli('--source-revision', revision)
            self.assertEqual(code, 2)
        self.assertEqual(sync.snapshot(self.root), before)


if __name__ == '__main__':
    unittest.main()
