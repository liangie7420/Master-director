import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("prompt_lint", Path(__file__).resolve().parents[1] / "scripts/check_prompt.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class PromptLintTests(unittest.TestCase):
    def test_temporal_and_subject_scopes_are_not_hard_conflicts(self):
        for text in ("起幅闭眼，随后睁眼。", "甲闭眼，乙睁眼。", "先静止然后冲刺"):
            with self.subTest(text=text):
                self.assertEqual(lint.check_conflicts(text), [])
                self.assertEqual(lint.scan_text(text)[0], [])

    def test_same_clause_opposites_are_advisory(self):
        errors, warnings, _ = lint.scan_text("角色同时闭眼并睁眼。")
        self.assertEqual(errors, [])
        self.assertTrue(any(code == "POSSIBLE-CONFLICT" for code, _ in warnings))

    def test_english_substrings_and_camera_are_not_actor_actions(self):
        self.assertEqual(lint.check_action_overload(
            "The vase stands still; the camera returns to a medium shot with a push in."), [])
        self.assertEqual(lint.check_action_overload("She returns home. The flower stands in a vase."), [])

    def test_chinese_actions_not_double_counted(self):
        self.assertEqual(lint.check_action_overload("她转身抓起茶杯。"), [])

    def test_actions_are_advisory(self):
        errors, warnings, _ = lint.scan_text("She runs, jumps, throws a ball. Anime style.")
        self.assertEqual(errors, [])
        self.assertTrue(any(code == "ACTION-LOAD" for code, _ in warnings))

    def test_native_and_english_reference_syntax(self):
        for ref in ("@图片1", "@图像2", "@视频1", "@音频1", "Image 1", "Reference image 1", "首帧"):
            with self.subTest(ref=ref):
                self.assertEqual(lint.scan_text(ref, task="multimodal_reference")[0], [])

    def test_reference_word_does_not_satisfy_required_binding(self):
        self.assertTrue(lint.scan_text("reference", task="image_to_video")[0])

    def test_text_only_asset_needs_no_reference_or_negative(self):
        self.assertEqual(lint.scan_text("二维线稿风格，黑色短发，深蓝外套。", task="asset_image")[:2], ([], []))

    def test_input_image_can_provide_style(self):
        self.assertEqual(lint.scan_text("Image 1. She slowly smiles.", task="image_to_video")[:2], ([], []))

    def test_empty_fails(self):
        self.assertTrue(lint.scan_text("  \n")[0])

    def test_negation_does_not_leak_into_another_sentence(self):
        risks = lint.check_risks("No subtitles. A crowd enters.")
        self.assertEqual(len(risks), 1)
        self.assertIn("crowd", risks[0][0])

    def test_negated_risks_not_reported(self):
        self.assertEqual(lint.check_risks("No subtitles, no watermark, no crowd."), [])


if __name__ == "__main__":
    unittest.main()
