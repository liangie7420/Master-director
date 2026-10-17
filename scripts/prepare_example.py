#!/usr/bin/env python3
"""Copy and prepare the authored 60-second example. No generative model calls."""
import argparse
import json
from pathlib import Path
import shutil
import sys

from prepare_shot import ROOT, load_json, load_profile, prepare

SOURCE = ROOT / "examples/last-letter"


def build_example(output, profile_name="seedance-2.0-ark"):
    output = Path(output).expanduser().resolve()
    if (ROOT / ".manju-install.json").exists() and ROOT in output.parents:
        raise ValueError("创作产物应写到安装目录之外")
    for folder in (ROOT, ROOT / "assets", ROOT / "scripts", ROOT / "references", ROOT / "examples",
                   ROOT / "docs", ROOT / "tests", ROOT / "benchmarks/shots", ROOT / "benchmarks/baseline"):
        if output == folder.resolve() or output in folder.resolve().parents or (
                folder != ROOT and folder.resolve() in output.parents):
            raise ValueError("输出不能覆盖源码或示例输入")
    if output.exists() and any(output.iterdir()):
        raise ValueError("输出目录非空；请选择新目录，以保留已有创作文件")
    profile = load_profile(profile_name)
    shots = [load_json(path) for path in sorted((SOURCE / "shots").glob("*.json"))]
    if len(shots) != 10 or sum(s["duration_seconds"] for s in shots) != 60:
        raise ValueError("内置示例必须为 10 镜、60 秒")
    output.mkdir(parents=True, exist_ok=True)
    for path in SOURCE.rglob("*"):
        if path.is_symlink():
            raise ValueError("示例不接受符号链接")
        if path.is_file():
            dest = output / path.relative_to(SOURCE)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    rows, reviews, previous = [], [], None
    for shot in shots:
        report = prepare(shot, profile, output / "shots", draft=True,
                         previous=previous if shot.get("preserve") else None)
        sid = shot["id"]
        if not report["local_pass"]:
            raise ValueError("%s 未通过输入检查: %s" % (sid, report["errors"]))
        for dirname in ("prompts", "prepared"):
            (output / dirname).mkdir(exist_ok=True)
        (output / "prompts" / (sid + "-video.txt")).write_text(report["prompt"], encoding="utf-8")
        (output / "prepared" / (sid + ".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        first = dict(shot, task="first_frame_image", assets=shot["frame_references"])
        frame_report = prepare(first, load_profile("image-configure-model"), output / "shots", draft=True)
        if not frame_report["local_pass"]:
            raise ValueError("%s 首帧说明未通过检查" % sid)
        (output / "prompts" / (sid + "-first-frame.txt")).write_text(frame_report["prompt"], encoding="utf-8")
        (output / "prepared" / (sid + "-first-frame.json")).write_text(json.dumps(frame_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.append({"shot_id": sid, "seconds": shot["duration_seconds"], "local_pass": True,
                     "submission_ready": False, "generation_status": "not_run"})
        reviews.append({"shot_id": sid, "source_media": None, "job_id": None, "output_media": None,
                        "observed_end_state": None, "visual_scores": None, "evidence": [],
                        "cost": None, "status": "not_run"})
        previous = shot
    (output / "review.json").write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"example": "关门前的来信", "shots": len(shots), "seconds": 60, "profile": profile_name,
              "output": str(output), "local_pass": True, "generation_status": "not_run",
              "creative_approval": "illustrative_only", "matrix": rows}
    (output / "production-status.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="准备内置 60 秒示例生产包；不生成图片或视频")
    ap.add_argument("--out", required=True, help="一个新的创作输出目录")
    ap.add_argument("--profile", default="seedance-2.0-ark")
    args = ap.parse_args()
    try:
        print(json.dumps(build_example(args.out, args.profile), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
