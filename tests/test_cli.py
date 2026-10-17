"""Run CLI regressions under the legacy encoding used by Windows pipes."""
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALID_PROMPT = (
    "Reference image 1. Anime style. Soft side light. No text, no watermark."
)


class CliTests(unittest.TestCase):
    def run_cli(self, script, *args):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "gbk"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )

    def test_all_help_output_is_utf8(self):
        for script in ("check_prompt.py", "diagnose.py", "extract_last_frame.py"):
            with self.subTest(script=script):
                result = self.run_cli(script, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("manju-director" if script != "extract_last_frame.py"
                              else "尾帧承接", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_valid_prompt_is_deliverable(self):
        result = self.run_cli("check_prompt.py", "--strict", "--text", VALID_PROMPT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("✅ 本地检查通过", result.stdout)

    def test_missing_reference_fails(self):
        result = self.run_cli("check_prompt.py", "--task", "image_to_video", "--text", "Anime style. No text.")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("参考素材声明缺失", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_strict_mode_rejects_warning_only_prompt(self):
        prompt = "Reference image 1. Soft side light. No text."
        normal = self.run_cli("check_prompt.py", "--text", prompt)
        strict = self.run_cli("check_prompt.py", "--strict", "--text", prompt)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(strict.returncode, 1, strict.stderr)
        self.assertIn("画风锚点缺失", strict.stdout)

    def test_known_symptom_returns_diagnosis(self):
        result = self.run_cli("diagnose.py", "人物变脸")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("🩺 诊断命中", result.stdout)
        self.assertIn("【候选原因】", result.stdout)
        self.assertIn("【止损兜底】", result.stdout)

    def test_unknown_symptom_returns_failure(self):
        result = self.run_cli("diagnose.py", "unknown-symptom-xyz")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("未命中已知症状", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
