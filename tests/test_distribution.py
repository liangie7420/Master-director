import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_bundle import build
from manage_skill import MARKER, check, destination, install, payload, uninstall
from prepare_example import build_example


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="manju-install-")
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("---\nname: manju-director\ndescription: Test\n---\n", encoding="utf-8")
        (self.source / "scripts").mkdir()
        (self.source / "scripts/check.py").write_text("print('ok')\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_three_host_layouts_install_check_uninstall(self):
        for host, directory in (("codex", ".agents"), ("claude", ".claude"), ("workbuddy", ".workbuddy")):
            target = destination(host, "project", self.root / "创作 workspace")
            self.assertEqual(target, self.root / "创作 workspace" / directory / "skills/manju-director")
            self.assertTrue(install(target, self.source)["ok"])
            self.assertTrue(check(target)["ok"])
            self.assertTrue(uninstall(target)["uninstalled"])
            self.assertFalse(target.exists())

    def test_project_root_must_be_explicit(self):
        with self.assertRaises(ValueError):
            destination("codex", "project")

    def test_unmanaged_old_skill_is_never_overwritten(self):
        target = self.root / "existing"
        target.mkdir()
        (target / "SKILL.md").write_text("user version", encoding="utf-8")
        for update in (False, True):
            with self.assertRaises(ValueError):
                install(target, self.source, update=update)
        self.assertEqual((target / "SKILL.md").read_text(), "user version")

    def test_modified_install_is_preserved_on_update_and_uninstall(self):
        target = self.root / "installed"
        install(target, self.source)
        (target / "SKILL.md").write_text("local edit", encoding="utf-8")
        self.assertFalse(check(target)["ok"])
        with self.assertRaises(ValueError):
            install(target, self.source, update=True)
        with self.assertRaises(ValueError):
            uninstall(target)
        self.assertEqual((target / "SKILL.md").read_text(), "local edit")

    def test_update_removes_only_old_managed_files(self):
        target = self.root / "installed"
        install(target, self.source)
        (target / "my-notes.txt").write_text("keep", encoding="utf-8")
        (self.source / "scripts/check.py").unlink()
        (self.source / "scripts/new.py").write_text("print(2)", encoding="utf-8")
        self.assertTrue(install(target, self.source, update=True)["ok"])
        self.assertFalse((target / "scripts/check.py").exists())
        self.assertEqual((target / "my-notes.txt").read_text(), "keep")

    def test_update_does_not_overwrite_new_user_file(self):
        target = self.root / "installed"
        install(target, self.source)
        (target / "scripts/new.py").write_text("user file", encoding="utf-8")
        (self.source / "scripts/new.py").write_text("package file", encoding="utf-8")
        with self.assertRaises(ValueError):
            install(target, self.source, update=True)
        self.assertEqual((target / "scripts/new.py").read_text(), "user file")

    def test_uninstall_retains_extra_files(self):
        target = self.root / "installed"
        install(target, self.source)
        (target / "my-story.md").write_text("keep", encoding="utf-8")
        self.assertEqual(uninstall(target)["retained"], ["my-story.md"])
        self.assertTrue((target / "my-story.md").exists())

    def test_manifest_escape_is_rejected_before_deletion(self):
        target = self.root / "installed"
        install(target, self.source)
        outside = self.root / "outside.txt"
        outside.write_text("keep", encoding="utf-8")
        marker = json.loads((target / MARKER).read_text())
        marker["files"]["../outside.txt"] = hashlib.sha256(outside.read_bytes()).hexdigest()
        (target / MARKER).write_text(json.dumps(marker), encoding="utf-8")
        with self.assertRaises(ValueError):
            uninstall(target)
        self.assertEqual(outside.read_text(), "keep")
        self.assertTrue((target / "SKILL.md").exists())

    def test_zip_is_reproducible_and_uses_one_top_folder(self):
        first, second = self.root / "one.zip", self.root / "two.zip"
        build(first, self.source)
        build(second, self.source)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertIn("manju-director/SKILL.md", archive.namelist())
            self.assertIn("manju-director/bundle-manifest.json", archive.namelist())
            self.assertTrue(all(name.startswith("manju-director/") for name in archive.namelist()))

    def test_payload_excludes_private_state_and_results(self):
        (self.source / "scripts/.env").write_text("secret", encoding="utf-8")
        (self.source / "benchmarks/results").mkdir(parents=True)
        (self.source / "benchmarks/results/output.json").write_text("{}", encoding="utf-8")
        (self.source / "task_plan.md").write_text("local", encoding="utf-8")
        files = payload(self.source)
        self.assertNotIn("scripts/.env", files)
        self.assertNotIn("task_plan.md", files)
        self.assertNotIn("benchmarks/results/output.json", files)

    def test_installed_scripts_work_from_unrelated_project(self):
        archive_path = self.root / "skill.zip"
        build(archive_path, ROOT)
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(self.root / "unpacked")
        target = self.root / "installed"
        install(target, self.root / "unpacked/manju-director")
        cwd = self.root / "creative"
        cwd.mkdir()
        result = subprocess.run([sys.executable, str(target / "scripts/prepare_shot.py"),
                                 str(target / "assets/shot-spec-template.json"),
                                 "--profile", "seedance-2.0-ark", "--draft"],
                                cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["local_pass"])

    def test_missing_or_reserved_manifest_fields_fail_cleanly(self):
        target = self.root / "installed"
        install(target, self.source)
        marker_path = target / MARKER
        original = json.loads(marker_path.read_text())
        modified = dict(original)
        modified.pop("bundle_id")
        marker_path.write_text(json.dumps(modified), encoding="utf-8")
        with self.assertRaises(ValueError):
            check(target)
        modified = dict(original)
        modified["files"] = {MARKER: "0" * 64}
        marker_path.write_text(json.dumps(modified), encoding="utf-8")
        with self.assertRaises(ValueError):
            uninstall(target)
        modified["files"] = {MARKER + "/": "0" * 64}
        marker_path.write_text(json.dumps(modified), encoding="utf-8")
        with self.assertRaises(ValueError):
            uninstall(target)
        marker_path.write_text("[]", encoding="utf-8")
        with self.assertRaises(ValueError):
            check(target)
        self.assertTrue((target / "SKILL.md").exists())

    def test_complete_example_has_ten_shots_and_no_fictional_generation(self):
        output = self.root / "production"
        result = build_example(output)
        self.assertEqual((result["shots"], result["seconds"]), (10, 60))
        self.assertEqual(len(list((output / "prompts").glob("*.txt"))), 20)
        reviews = json.loads((output / "review.json").read_text(encoding="utf-8"))
        self.assertTrue(all(row["status"] == "not_run" and row["visual_scores"] is None for row in reviews))
        (output / "my-notes.md").write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            build_example(output)
        self.assertEqual((output / "my-notes.md").read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
