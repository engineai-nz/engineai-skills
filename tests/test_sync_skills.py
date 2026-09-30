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

    def test_default_stale_local_is_read_only_and_never_stages_unrelated_dirty_work(self):
        self.local()
        (self.repo / 'notes.txt').write_text('unrelated dirty work')
        before_repo = sync.snapshot(self.repo)
        before_local = sync.snapshot(self.live)
        status = self.git('status', '--porcelain')
        code, report = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(report['result'], 'drift')
        self.assertEqual(sync.snapshot(self.repo), before_repo)
        self.assertEqual(sync.snapshot(self.live), before_local)
        self.assertEqual(self.git('status', '--porcelain'), status)
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
        with self.assertRaises(sync.Conflict):
            sync.install(self.repo, self.source, self.target, 'brand', None, 'absent', self.backup)
        with self.assertRaises(sync.Conflict):
            sync.install(self.repo, self.source, self.target, 'brand', 'f' * 40, 'absent', self.backup)
        self.assertFalse(self.target.exists())

    def test_fingerprint_conflict_preserves_custom_work(self):
        self.local()
        before = sync.snapshot(self.target)
        with self.assertRaises(sync.Conflict):
            self.apply('absent')
        self.assertEqual(sync.snapshot(self.target), before)
        self.assertFalse(self.backup.exists())

    def test_missing_source_never_deletes_target(self):
        self.local()
        (self.source / 'SKILL.md').unlink()
        before = sync.snapshot(self.target)
        code, _ = self.run_cli()
        self.assertEqual(code, 2)
        with self.assertRaises(sync.Conflict):
            self.apply()
        self.assertEqual(sync.snapshot(self.target), before)

    def test_missing_local_source_never_deletes_canon(self):
        before = sync.snapshot(self.repo)
        code, _ = self.run_cli('--direction', 'local-to-repo')
        self.assertEqual(code, 2)
        self.assertEqual(sync.snapshot(self.repo), before)

    def test_install_backups_extras_and_preserves_unrelated_dirty_files(self):
        self.local()
        before = sync.snapshot(self.target)
        (self.repo / 'dirty.txt').write_text('keep')
        status = self.git('status', '--porcelain')
        result = self.apply()
        self.assertEqual(result['result'], 'installed')
        self.assertEqual(sync.snapshot(self.backup / 'original'), before)
        self.assertEqual((self.target / 'extra.txt').read_text(), 'keep local custom work\n')
        self.assertEqual(self.git('status', '--porcelain'), status)

    def test_repeated_install_is_noop_without_new_backup(self):
        self.apply()
        second = self.root / 'second-backup'
        result = self.apply(backup=second)
        self.assertEqual(result['result'], 'unchanged')
        self.assertFalse(second.exists())

    def test_path_traversal_outside_allowlist_rejected(self):
        for name in ['../brand', '/brand', 'brand/../../outside']:
            with self.assertRaises(sync.Conflict):
                sync.paths(self.repo, self.live, name)

    def test_symlinked_parent_target_source_and_backup_rejected(self):
        link = self.root / 'link'
        link.symlink_to(self.live, target_is_directory=True)
        with self.assertRaises(sync.Conflict):
            sync.paths(self.repo, link / 'nested', 'brand')
        self.target.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(sync.Conflict):
            sync.paths(self.repo, self.live, 'brand')
        self.target.unlink()
        (self.source / 'link.txt').symlink_to(self.source / 'a.txt')
        with self.assertRaises(sync.Conflict):
            sync.snapshot(self.source)
        (self.source / 'link.txt').unlink()
        self.backup.symlink_to(self.live, target_is_directory=True)
        with self.assertRaises(sync.Conflict):
            self.apply()

    def test_backup_overlap_or_existing_backup_rejected(self):
        for backup in [self.repo / 'backups', self.live / 'backups', self.root,
                       self.target / 'backup']:
            with self.assertRaises(sync.Conflict):
                self.apply(backup=backup)
        self.backup.mkdir()
        with self.assertRaises(sync.Conflict):
            self.apply()
        self.assertFalse(self.target.exists())

    def test_dirty_selected_source_rejected(self):
        (self.source / 'a.txt').write_text('unreviewed change')
        with self.assertRaises(sync.Conflict):
            self.apply()
        self.assertFalse(self.backup.exists())

    def test_untracked_selected_source_rejected(self):
        (self.source / 'untracked.txt').write_text('unreviewed')
        with self.assertRaises(sync.Conflict):
            self.apply()

    def test_source_changed_after_preflight_rolls_back_prior_copy(self):
        self.local()
        before = sync.snapshot(self.target)
        original = sync.check_revision
        calls = 0
        def change_later(*args):
            nonlocal calls
            calls += 1
            if calls == 4:
                (self.source / 'a.txt').write_text('changed during installation')
            return original(*args)
        with patch.object(sync, 'check_revision', side_effect=change_later):
            with self.assertRaises(sync.Conflict):
                self.apply()
        self.assertEqual(sync.snapshot(self.target), before)
        self.assertEqual(json.loads((self.backup / 'receipt.json').read_text())['status'], 'rolled-back')

    def test_mid_copy_failure_rolls_back_existing_and_created_target(self):
        for existing in [False, True]:
            with self.subTest(existing=existing):
                if existing:
                    self.local()
                before = sync.snapshot(self.target)
                original = os.replace
                calls = 0
                def fail_second(*args):
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError('fixture disk error')
                    return original(*args)
                backup = self.root / f'backup-{existing}'
                with patch.object(sync.os, 'replace', side_effect=fail_second):
                    with self.assertRaises(OSError):
                        self.apply(backup=backup)
                self.assertEqual(sync.snapshot(self.target), before)
                self.assertEqual(json.loads((backup / 'receipt.json').read_text())['status'], 'rolled-back')

    def test_rollback_preserves_concurrent_edits_and_records_conflict(self):
        self.local()
        original = os.replace
        calls = 0
        def compete_then_fail(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.target / 'SKILL.md').write_text('another owner edited this')
                raise OSError('fixture failure')
            return original(*args)
        with patch.object(sync.os, 'replace', side_effect=compete_then_fail):
            with self.assertRaises(OSError):
                self.apply()
        self.assertEqual((self.target / 'SKILL.md').read_text(), 'another owner edited this')
        receipt = json.loads((self.backup / 'receipt.json').read_text())
        self.assertEqual(receipt['status'], 'rollback-conflict')
        self.assertEqual(receipt['rollback_conflicts'], ['SKILL.md'])

    def test_target_file_directory_collision_fails_before_backup(self):
        self.local()
        (self.target / 'a.txt').mkdir()
        with self.assertRaises(sync.Conflict):
            self.apply()
        self.assertFalse(self.backup.exists())


if __name__ == '__main__':
    unittest.main()
