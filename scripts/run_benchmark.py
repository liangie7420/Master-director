#!/usr/bin/env python3
"""Reproduce local preparation/lint comparisons. Never calls a video model."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from check_prompt import scan_text
from prepare_shot import ROOT, load_json, load_profile, prepare


def legacy_prompt(shot):
    """A labelled reconstruction of the pre-refactor skeleton, not a real old run."""
    refs = "\n".join("[Image %d] %s" % (i, asset.get("description", asset["role"]))
                     for i, asset in enumerate(shot.get("assets", []), 1))
    return ("[Reference Images]\n" + refs + "\n[Core Rules]\n"
            "Frame continues from first frame; character pose, position and light stay unchanged.\n"
            "Keep character identity, clothing and environment unchanged. Follow real physics.\n"
            "[Video Style]\n" + shot["style"] + "\n[Camera & Narrative]\n"
            + "；".join(shot["start_state"].values()) + "\n" + shot["action"] + "\n"
            + shot["camera"]["description"] + "\n" + shot.get("lighting", "")
            + "\n[Signature]\n85mm, shallow depth of field, half-face lighting, Kodak Vision3 500T.\n"
            "[Negative]\nNo facial deformation, no clothing drift, no text, no watermark, no anime, no cartoon.\n")


def run(out_dir):
    out_dir = Path(out_dir).resolve()
    # Do not let generated artifacts replace fixtures, baseline or source files.
    for protected in (ROOT / "scripts", ROOT / "assets", ROOT / "references", ROOT / "tests",
                      ROOT / "benchmarks/shots", ROOT / "benchmarks/baseline"):
        if out_dir == protected.resolve() or protected.resolve() in out_dir.parents:
            raise ValueError("输出目录不能位于输入或源码目录")
    if out_dir == ROOT or out_dir in ROOT.parents:
        raise ValueError("请选择独立的结果目录")
    out_dir.mkdir(parents=True, exist_ok=True)
    baseline = load_json(ROOT / "benchmarks/baseline/manifest.json")
    lint_rows = []
    for case in baseline["scanner_cases"]:
        # Explicitly request references only in the case that tests that contract.
        task = "image_to_video" if case["id"] == "reference_word_only" else "auto"
        errors, warnings, _ = scan_text(case["text"], task=task)
        lint_rows.append({"id": case["id"], "before_errors": case["errors"], "after_errors": errors,
                          "after_warnings": warnings, "after_task": task})
    profile_names = ["seedance-2.0-ark", "minimax-hailuo-2.3", "minimax-hailuo-02",
                     "google-omni-1.1-flash", "kling-configure-version"]
    rows, previous = [], None
    paths = sorted((ROOT / "benchmarks/shots").glob("*.json"))
    for path in paths:
        shot = load_json(path)
        sid = shot["id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", sid):
            raise ValueError("镜头 ID 不能用作安全文件名: " + sid)
        legacy = legacy_prompt(shot)
        (out_dir / (sid + "-legacy-reconstructed.txt")).write_text(legacy, encoding="utf-8")
        for name in profile_names:
            report = prepare(shot, load_profile(name), path.parent, draft=True,
                             previous=previous if shot.get("preserve") else None)
            (out_dir / (sid + "-" + name + ".json")).write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            rows.append({"shot_id": sid, "profile": name, "task": shot["task"],
                         "local_pass": report["local_pass"], "submission_ready": report["submission_ready"],
                         "errors": report["errors"], "warnings": report["warnings"],
                         "prompt_sha256": hashlib.sha256(report.get("prompt", "").encode()).hexdigest() if "prompt" in report else None,
                         "generation_status": "not_run", "video_verified": False})
        previous = shot
    summary = {"scope": "offline input/lint evaluation only", "generation_status": "not_run",
               "video_verified": False, "cases": len(paths), "profiles": len(profile_names),
               "matrix": rows, "lint_comparison": lint_rows}
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger = []
    for row in rows:
        for variant in ("legacy_reconstructed", "candidate"):
            ledger.append({"shot_id": row["shot_id"], "profile": row["profile"], "variant": variant,
                           "trial_id": None, "result_path": None, "cost": None, "latency_seconds": None,
                           "scores": {k: None for k in ("core_event", "identity", "spatial_contact", "continuity", "performance", "aesthetics", "adherence")},
                           "evidence": [], "status": "not_run"})
    # Preserve manually recorded trials across reruns.
    ledger_path = out_dir / "trial-template.json"
    if not ledger_path.exists():
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seedance = [row for row in rows if row["profile"] == "seedance-2.0-ark"]
    passed = sum(row["local_pass"] for row in rows)
    note = ("# Local experiment report\n\n"
            "Offline preparation only. No video was generated or visually reviewed.\n\n"
            "- Cases: %d; profiles: %d; combinations: %d.\n"
            "- Structurally prepared drafts: %d; incompatible combinations: %d.\n"
            "- Seedance reference profile: %d/%d drafts prepared.\n"
            "- All outputs are drafts; actual assets and provider-specific submission checks remain required.\n"
            "- Legacy texts reconstruct the old skeleton; they are not historical model outputs.\n"
            "- Visual scores and costs remain null until real trials are recorded.\n"
            % (len(paths), len(profile_names), len(rows), passed, len(rows)-passed,
               sum(row["local_pass"] for row in seedance), len(seedance)))
    (out_dir / "REPORT.md").write_text(note, encoding="utf-8")
    return summary, all(row["local_pass"] for row in seedance) and len(paths) == 6


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="manju-director 离线对照；不会生成视频或填写虚构评分")
    ap.add_argument("--out", default=str(ROOT / "benchmarks/results/local"))
    args = ap.parse_args()
    try:
        summary, valid = run(args.out)
        print("离线对照：%d 类镜头 × %d 个配置；生成状态 not_run；报告 %s" %
              (summary["cases"], summary["profiles"], Path(args.out).resolve() / "REPORT.md"))
        return 0 if valid else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
