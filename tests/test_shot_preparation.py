import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_shot import load_json, load_profile, prepare
from run_benchmark import run


class ShotPreparationTests(unittest.TestCase):
    def setUp(self):
        self.shot = load_json(ROOT / "assets/shot-spec-template.json")
        self.profile = load_profile("seedance-2.0-ark")

    def codes(self, report):
        return {error["code"] for error in report["errors"]}

    def test_all_six_reference_profile_drafts_prepare(self):
        previous = None
        for path in sorted((ROOT / "benchmarks/shots").glob("*.json")):
            shot = load_json(path)
            report = prepare(shot, self.profile, draft=True, previous=previous if shot.get("preserve") else None)
            self.assertTrue(report["local_pass"], report["errors"])
            self.assertFalse(report["submission_ready"])
            self.assertEqual(report["generation_status"], "not_run")
            self.assertFalse(report["video_verified"])
            previous = shot

    def test_planned_asset_fails_strict_preparation(self):
        self.assertIn("ASSET_MISSING", self.codes(prepare(self.shot, self.profile)))

    def test_existing_asset_checked_relative_to_spec(self):
        with tempfile.TemporaryDirectory() as directory:
            # File existence is the tested contract; media decoding is separate.
            Path(directory, "frame.png").write_bytes(b"fixture")
            self.shot["assets"][0]["source"] = "frame.png"
            report = prepare(self.shot, self.profile, directory)
            self.assertTrue(report["local_pass"], report["errors"])
            self.assertEqual(report["bindings"][0]["label"], "@图片1")
            self.assertFalse(report["video_verified"])

    def test_remote_reference_not_claimed_verified(self):
        self.shot["assets"][0]["source"] = "https://example.test/frame.png"
        self.assertIn("REMOTE_ASSET_UNVERIFIED", self.codes(prepare(self.shot, self.profile)))

    def test_wrong_asset_role_and_duplicates_fail(self):
        self.shot["assets"].append(copy.deepcopy(self.shot["assets"][0]))
        self.shot["assets"][0]["kind"] = "video"
        codes = self.codes(prepare(self.shot, self.profile, draft=True))
        self.assertTrue({"ASSET_ROLE", "ASSET_ID", "ASSET_BINDING"}.issubset(codes))

    def test_known_unsupported_task_not_bypassed_by_draft(self):
        shot = load_json(ROOT / "benchmarks/shots/S03.json")
        report = prepare(shot, load_profile("minimax-hailuo-2.3"), draft=True)
        self.assertIn("UNSUPPORTED_TASK", self.codes(report))
        self.assertNotIn("prompt", report)

    def test_unknown_version_needs_draft(self):
        profile = load_profile("kling-configure-version")
        self.assertIn("MODEL_VERSION", self.codes(prepare(self.shot, profile)))
        report = prepare(self.shot, profile, draft=True)
        self.assertTrue(report["local_pass"])
        self.assertFalse(report["submission_ready"])
        self.assertTrue(report["warnings"])

    def test_omni_does_not_inherit_veo_limits(self):
        shot = load_json(ROOT / "benchmarks/shots/S01.json")
        profile = load_profile("google-omni-1.1-flash")
        self.assertEqual(profile["model_id"], "gemini-omni-1.1-flash")
        self.assertIn("UNVERIFIED_DURATION", self.codes(prepare(shot, profile)))

    def test_duration_resolution_coupling(self):
        self.shot.update(duration_seconds=10, resolution="1080P")
        report = prepare(self.shot, load_profile("minimax-hailuo-2.3"), draft=True)
        self.assertIn("DURATION_RESOLUTION", self.codes(report))

    def test_hailuo_02_keyframe_pair_excludes_512p(self):
        shot = load_json(ROOT / "benchmarks/shots/S03.json")
        shot["resolution"] = "512P"
        self.assertIn("TASK_RESOLUTION", self.codes(prepare(shot, load_profile("minimax-hailuo-02"), draft=True)))

    def test_invalid_duration_and_overlapping_beats(self):
        for value in (True, -1, float("nan"), 16, 6.5):
            shot = copy.deepcopy(self.shot)
            shot["duration_seconds"] = value
            self.assertIn("DURATION", self.codes(prepare(shot, self.profile, draft=True)), value)
        self.shot["beats"] = [{"start": 0, "end": 4, "description": "推信封"},
                              {"start": 3, "end": 7, "description": "停住"}]
        self.assertIn("TIMELINE", self.codes(prepare(self.shot, self.profile, draft=True)))

    def test_timeline_overlap_within_duration_fails(self):
        self.shot["beats"] = [{"start": 0, "end": 4, "description": "推信封"},
                              {"start": 3, "end": 6, "description": "停住"}]
        self.assertIn("TIMELINE", self.codes(prepare(self.shot, self.profile, draft=True)))

    def test_declared_continuity_compares_selected_keys(self):
        previous = load_json(ROOT / "benchmarks/shots/S05.json")
        shot = load_json(ROOT / "benchmarks/shots/S06.json")
        shot["start_state"]["PR-02.owner"] = "乙右手"
        self.assertIn("CONTINUITY", self.codes(prepare(shot, self.profile, draft=True, previous=previous)))

    def test_bad_previous_record_is_an_input_error(self):
        self.assertIn("CONTINUITY", self.codes(prepare(self.shot, self.profile, draft=True, previous=[])))

    def test_native_audio_unknown_is_not_silently_accepted(self):
        self.shot["audio"]["mode"] = "native"
        report = prepare(self.shot, load_profile("minimax-hailuo-2.3"))
        self.assertIn("AUDIO_CAPABILITY", self.codes(report))

    def test_post_audio_and_internal_intent_not_sent_to_model(self):
        self.shot["intent"] = "INTERNAL-INTENT-SENTINEL"
        self.shot["audio"]["dialogue"] = "POST-AUDIO-SENTINEL"
        report = prepare(self.shot, self.profile, draft=True)
        self.assertNotIn("INTERNAL-INTENT-SENTINEL", report["prompt"])
        self.assertNotIn("POST-AUDIO-SENTINEL", report["prompt"])
        self.assertIn("POST-AUDIO-SENTINEL", report["editorial"]["audio"]["dialogue"])

    def test_image_to_video_does_not_restate_full_starting_appearance(self):
        self.shot["start_state"]["character"] = "ALREADY-IN-IMAGE-SENTINEL"
        self.shot["end_state"]["character"] = "坐姿不变"
        report = prepare(self.shot, self.profile, draft=True)
        self.assertNotIn("ALREADY-IN-IMAGE-SENTINEL", report["prompt"])

    def test_still_end_frame_does_not_receive_motion_sequence(self):
        self.shot["task"] = "end_frame_image"
        self.shot["action"] = "MOTION-SEQUENCE-SENTINEL"
        report = prepare(self.shot, load_profile("image-configure-model"), draft=True)
        self.assertTrue(report["local_pass"], report["errors"])
        self.assertNotIn("MOTION-SEQUENCE-SENTINEL", report["prompt"])
        self.assertIn(self.shot["end_state"]["envelope"], report["prompt"])

    def test_edit_uses_source_not_reference_task(self):
        self.shot["task"] = "video_edit"
        self.shot["assets"] = [{"id": "V1", "kind": "video", "role": "base_video", "source": ""}]
        report = prepare(self.shot, self.profile, draft=True)
        self.assertTrue(report["prompt"].startswith("严格编辑@视频1"))

    def test_english_boilerplate_does_not_translate_authored_prose(self):
        self.shot["prompt_language"] = "en"
        self.shot["action"] = "She slides the envelope and holds it in place."
        report = prepare(self.shot, self.profile, draft=True)
        self.assertIn("Start from", report["prompt"])
        self.assertIn(self.shot["action"], report["prompt"])
        self.assertNotIn("必须实现：", report["prompt"])

    def test_style_conflict_is_deterministic(self):
        self.shot["avoid"] = ["no anime"]
        self.assertIn("STYLE_CONFLICT", self.codes(prepare(self.shot, self.profile, draft=True)))

    def test_prompt_endpoint_limit_is_not_silently_truncated(self):
        self.shot["action"] = "长" * 2100
        report = prepare(self.shot, load_profile("minimax-hailuo-2.3"), draft=True)
        self.assertIn("PROMPT_LENGTH", self.codes(report))
        self.assertIn("长" * 2100, report["prompt"])

    def test_invalid_top_level_or_state_fails_cleanly(self):
        self.assertIn("SCHEMA", self.codes(prepare([], self.profile)))
        self.shot["start_state"] = "not a map"
        self.assertIn("SCHEMA", self.codes(prepare(self.shot, self.profile, draft=True)))

    def test_malformed_optional_values_are_input_errors(self):
        for key, value in (("lighting", []), ("audio", {"mode": "post", "dialogue": []})):
            shot = copy.deepcopy(self.shot)
            shot[key] = value
            self.assertIn("SCHEMA", self.codes(prepare(shot, self.profile, draft=True)))
        self.shot["assets"][0]["kind"] = []
        self.assertIn("ASSET_ROLE", self.codes(prepare(self.shot, self.profile, draft=True)))

    def test_benchmark_keeps_visual_scores_empty_and_real_records(self):
        with tempfile.TemporaryDirectory() as directory:
            summary, valid = run(directory)
            self.assertTrue(valid)
            self.assertEqual((summary["cases"], summary["profiles"]), (6, 5))
            self.assertEqual(summary["generation_status"], "not_run")
            ledger_path = Path(directory, "trial-template.json")
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            self.assertTrue(all(v is None for row in ledger for v in row["scores"].values()))
            ledger_path.write_text('[{"real_record": true}]', encoding="utf-8")
            run(directory)
            self.assertEqual(json.loads(ledger_path.read_text()), [{"real_record": True}])

    def test_benchmark_cannot_overwrite_fixtures(self):
        with self.assertRaises(ValueError):
            run(ROOT / "benchmarks/shots")


if __name__ == "__main__":
    unittest.main()
