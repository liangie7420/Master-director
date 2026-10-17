#!/usr/bin/env python3
"""Validate an authored shot specification and prepare task-specific model text.

No model calls, translation, uploads or automatic quality verdicts. Python 3.8+.
"""
import argparse
import json
import math
from pathlib import Path
import sys
from urllib.parse import urlparse

from check_prompt import TASKS, scan_text

ROOT = Path(__file__).resolve().parents[1]
IMAGE_TASKS = {"asset_image", "first_frame_image", "end_frame_image"}
ASSET_ROLES = {"first_frame": "image", "last_frame": "image", "identity": "image",
               "scene": "image", "prop": "image", "style": "image", "motion": "video",
               "base_video": "video", "voice": "audio", "music": "audio"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def load_profile(name, registry=None):
    data = load_json(registry or ROOT / "references/model-adapters/profiles.json")
    if name not in data["profiles"]:
        raise ValueError("未知 profile: %s；可选 %s" % (name, ", ".join(data["profiles"])))
    return data["profiles"][name]


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_shot(shot, profile, base_dir=None, draft=False, previous=None):
    errors, warnings = [], []
    base_dir = Path(base_dir or ".")

    def error(code, message):
        errors.append({"code": code, "message": message})

    def warning(code, message):
        warnings.append({"code": code, "message": message})

    if not isinstance(shot, dict):
        return [{"code": "SCHEMA", "message": "镜头说明必须是 JSON 对象"}], []
    for key in ("id", "task", "intent", "visible_evidence", "focus", "action", "style"):
        if not isinstance(shot.get(key), str) or not shot[key].strip():
            error("SCHEMA", "%s 必须是非空字符串" % key)
    task = shot.get("task")
    if task not in TASKS or task == "auto":
        error("TASK", "需要明确生成任务")
    for key in ("start_state", "end_state"):
        if not isinstance(shot.get(key), dict) or not shot[key] or any(
                not isinstance(k, str) or not isinstance(v, str) or not v.strip() for k, v in shot.get(key, {}).items()):
            error("SCHEMA", "%s 必须包含非空的对象状态" % key)
    if not isinstance(shot.get("camera"), dict) or not isinstance(shot.get("camera", {}).get("description"), str) or not shot["camera"]["description"].strip():
        error("SCHEMA", "camera.description 必须是字符串")
    for key in ("preserve", "must", "prefer", "avoid"):
        if not isinstance(shot.get(key, []), list) or any(not isinstance(v, str) or not v.strip() for v in shot.get(key, [])):
            error("SCHEMA", "%s 必须是字符串列表" % key)
    for key in ("lighting",):
        if key in shot and not isinstance(shot[key], str):
            error("SCHEMA", "%s 必须是字符串" % key)
    audio_shape = shot.get("audio", {})
    if isinstance(audio_shape, dict):
        for key in ("description", "dialogue"):
            if key in audio_shape and not isinstance(audio_shape[key], str):
                error("SCHEMA", "audio.%s 必须是字符串" % key)
    if shot.get("prompt_language", "zh") not in ("zh", "en"):
        error("SCHEMA", "prompt_language 当前支持 zh/en；正文需由作者写成目标语言")
    if errors:
        return errors, warnings

    support = profile.get("tasks", {}).get(task)
    if support is False:
        error("UNSUPPORTED_TASK", "该版本不支持任务 " + task)
    elif support is not True:
        (warning if draft else error)("UNVERIFIED_CAPABILITY", "该版本的任务能力未核实：" + task)
    if not profile.get("model_id"):
        (warning if draft else error)("MODEL_VERSION", "需要填写准确的模型版本与入口")

    duration = shot.get("duration_seconds")
    if task not in IMAGE_TASKS:
        if not _number(duration) or duration <= 0:
            error("DURATION", "视频时长必须为正数")
        else:
            rules = profile.get("duration", {})
            if not rules:
                (warning if draft else error)("UNVERIFIED_DURATION", "该入口的时长范围尚未核实")
            if rules.get("integer") and not float(duration).is_integer():
                error("DURATION", "该接口的时长要求整数秒")
            if rules.get("values") and duration not in rules["values"]:
                error("DURATION", "时长不在该版本允许值内")
            if rules.get("min") is not None and duration < rules["min"] or rules.get("max") is not None and duration > rules["max"]:
                error("DURATION", "时长超出该版本范围")
            by_resolution = rules.get("by_resolution", {})
            resolution = shot.get("resolution")
            if by_resolution and resolution not in by_resolution:
                error("RESOLUTION", "需要选择该版本支持的分辨率")
            elif by_resolution and duration not in by_resolution[resolution]:
                error("DURATION_RESOLUTION", "该分辨率不支持此时长")
            task_resolutions = profile.get("task_resolutions", {}).get(task)
            if task_resolutions and resolution not in task_resolutions:
                error("TASK_RESOLUTION", "该任务不支持此分辨率")

    assets = shot.get("assets", [])
    if not isinstance(assets, list) or any(not isinstance(a, dict) for a in assets):
        error("SCHEMA", "assets 必须是对象列表")
        return errors, warnings
    seen, kinds, roles = set(), {}, {}
    for asset in assets:
        aid, kind, role = asset.get("id"), asset.get("kind"), asset.get("role")
        if not isinstance(kind, str) or not isinstance(role, str):
            error("ASSET_ROLE", "素材类型与职责必须是字符串")
            continue
        if "description" in asset and not isinstance(asset["description"], str):
            error("SCHEMA", "素材描述必须是字符串")
        if not isinstance(aid, str) or not aid.strip() or aid in seen:
            error("ASSET_ID", "素材 ID 缺失或重复")
        else:
            seen.add(aid)
        if kind not in ("image", "video", "audio") or role not in ASSET_ROLES or ASSET_ROLES.get(role) != kind:
            error("ASSET_ROLE", "素材类型与职责不匹配: %s" % aid)
        kinds[kind] = kinds.get(kind, 0) + 1
        roles[role] = roles.get(role, 0) + 1
        source = asset.get("source", "")
        if not isinstance(source, str) or not source.strip():
            (warning if draft else error)("ASSET_MISSING", "素材尚未提供: %s" % aid)
        elif urlparse(source).scheme in ("http", "https"):
            (warning if draft else error)("REMOTE_ASSET_UNVERIFIED", "远程素材需先验证访问和上传: %s" % aid)
        elif not (base_dir / source).is_file():
            (warning if draft else error)("ASSET_MISSING", "本地素材不存在: %s" % aid)
    required = {"image_to_video": ("first_frame",), "keyframe_pair": ("first_frame", "last_frame"),
                "video_edit": ("base_video",), "video_extend": ("base_video",)}.get(task, ())
    for role in required:
        if roles.get(role, 0) != 1:
            error("ASSET_BINDING", "任务要求且只允许一项 %s" % role)
    if task == "multimodal_reference" and not assets:
        error("ASSET_BINDING", "多模态参考任务需要素材")
    if task == "text_to_video" and assets:
        error("TASK_INPUT", "文生视频任务不能隐式携带参考素材，请选择对应模式")
    if task == "multimodal_reference" and profile.get("reference_requires_image") and not kinds.get("image"):
        error("TASK_INPUT", "该入口的参考模式至少需要一张图片")
    if task == "image_to_video" and (len(assets) != 1 or roles.get("first_frame") != 1):
        error("TASK_INPUT", "首帧图生视频只接收一张首帧；其他参考需选择多模态模式")
    if task == "keyframe_pair" and (len(assets) != 2 or roles.get("first_frame") != 1 or roles.get("last_frame") != 1):
        error("TASK_INPUT", "严格首尾帧模式只接收一对帧")
    for kind, limit in profile.get("max_assets", {}).items():
        if limit is not None and kinds.get(kind, 0) > limit:
            error("ASSET_LIMIT", "%s 素材超过该版本上限" % kind)
    if profile.get("audio_requires_visual") and kinds.get("audio") and not (kinds.get("image") or kinds.get("video")):
        error("TASK_INPUT", "该版本的音频参考需要搭配图片或视频")

    audio = shot.get("audio", {"mode": "none"})
    if not isinstance(audio, dict) or audio.get("mode") not in ("none", "native", "post"):
        error("AUDIO", "audio.mode 必须是 none/native/post")
    elif audio.get("mode") == "native" and profile.get("native_audio") is not True:
        (warning if draft and profile.get("native_audio") is None else error)("AUDIO_CAPABILITY", "该版本原生声音能力不支持或未核实")

    beats = shot.get("beats", [])
    if not isinstance(beats, list):
        error("TIMELINE", "beats 必须为列表")
        beats = []
    last_end = 0
    for beat in beats:
        if not isinstance(beat, dict):
            error("TIMELINE", "时间段必须为对象")
            continue
        start, end = beat.get("start"), beat.get("end")
        if not (_number(start) and _number(end) and 0 <= start < end and _number(duration) and end <= duration):
            error("TIMELINE", "时间段越界或顺序错误")
        elif start < last_end:
            error("TIMELINE", "时间段重叠")
        else:
            last_end = end
        if not isinstance(beat.get("description"), str) or not beat["description"].strip():
            error("TIMELINE", "时间段描述缺失")
    if previous is not None:
        if not isinstance(previous, dict) or not isinstance(previous.get("end_state"), dict):
            error("CONTINUITY", "前镜记录缺少 end_state 对象")
            return errors, warnings
        for key in shot.get("preserve", []):
            if key not in previous.get("end_state", {}) or key not in shot["start_state"]:
                error("CONTINUITY", "承接状态缺失: " + key)
            elif previous["end_state"][key] != shot["start_state"][key]:
                error("CONTINUITY", "声明承接的状态不一致: " + key)
    style = shot["style"].lower()
    avoid = " ".join(shot.get("avoid", [])).lower()
    if any(word in style for word in ("二维", "anime", "2d", "漫画")) and any(word in avoid for word in ("no anime", "no cartoon", "禁止动画", "禁止漫画")):
        error("STYLE_CONFLICT", "目标动画画风与负面约束冲突")
    if not shot.get("must"):
        warning("PRIORITY", "建议明确本镜的核心验收事件")
    return errors, warnings


def render_prompt(shot, profile):
    """Project only the task-relevant fields. Does not invent/translate direction."""
    task, bindings = shot["task"], []
    en = shot.get("prompt_language", "zh") == "en"
    counters = {"image": 0, "video": 0, "audio": 0}
    for asset in shot.get("assets", []):
        kind = asset["kind"]
        counters[kind] += 1
        label = (({"image": "@图片", "video": "@视频", "audio": "@音频"}[kind])
                 if profile.get("reference_syntax") == "at_zh" else kind.title() + " ") + str(counters[kind])
        bindings.append(dict(asset, label=label))
    labels = {a["role"]: a["label"] for a in bindings}
    parts = []
    if task in ("video_edit", "video_extend"):
        verb = (("Edit " if task == "video_edit" else "Extend ") if en
                else ("严格编辑" if task == "video_edit" else "向后延长"))
        parts.append(verb + labels["base_video"] + ("." if en else "。"))
        if task == "video_edit":
            parts.append("Preserve everything not requested to change." if en else "保留未指定修改的内容。")
    for asset in bindings:
        purpose = asset.get("description") or asset["role"]
        parts.append(("%s: %s." if en else "%s：%s。") % (asset["label"], purpose))
    if task in IMAGE_TASKS:
        state = shot["end_state"] if task == "end_frame_image" else shot["start_state"]
        parts.extend((shot["style"], "；".join(state.values()), shot["camera"]["description"]))
    else:
        if task == "text_to_video":
            parts.extend((shot["style"], "；".join(shot["start_state"].values())))
        elif task == "image_to_video":
            parts.append(("Start from %s as the first frame." if en else "从%s首帧开始。") % labels["first_frame"])
        elif task == "keyframe_pair":
            parts.append(("Move continuously from the state in %s to the state in %s." if en
                          else "从%s的状态连续运动到%s的状态。") % (labels["first_frame"], labels["last_frame"]))
        elif task == "multimodal_reference":
            parts.extend((shot["style"], "；".join(shot["start_state"].values())))
        if shot.get("beats"):
            for index, beat in enumerate(shot["beats"], 1):
                marker = ("%s–%ss" % (beat["start"], beat["end"])) if profile.get("timing") == "timestamps" else ("Beat %d" if en else "动作段%d") % index
                parts.append(marker + "：" + beat["description"])
        else:
            parts.append(shot["action"])
        parts.append(shot["camera"]["description"])
        parts.append(("End state: " if en else "结束状态：") + "; ".join(shot["end_state"].values()))
    if shot.get("lighting") and (task in IMAGE_TASKS or task in ("text_to_video", "multimodal_reference") or shot.get("lighting_changes")):
        parts.append(shot["lighting"])
    if shot.get("must"):
        parts.append(("Critical: " if en else "必须实现：") + "; ".join(shot["must"]))
    if shot.get("prefer"):
        parts.append(("Optional refinement: " if en else "次要细节：") + "; ".join(shot["prefer"]))
    audio = shot.get("audio", {})
    if task not in IMAGE_TASKS and audio.get("mode") == "native":
        if audio.get("description"):
            parts.append(("Audio: " if en else "声音：") + audio["description"])
        if audio.get("dialogue"):
            parts.append(("Dialogue: " if en else "台词：") + audio["dialogue"])
    if shot.get("avoid") and profile.get("negative_policy") != "positive_only":
        parts.append(("Avoid: " if en else "避免：") + "; ".join(shot["avoid"]))
    return "\n".join(parts) + "\n", bindings


def prepare(shot, profile, base_dir=None, draft=False, previous=None):
    errors, warnings = validate_shot(shot, profile, base_dir, draft, previous)
    report = {"shot_id": shot.get("id") if isinstance(shot, dict) else None,
              "profile": profile.get("model_id"), "errors": errors, "warnings": warnings,
              "local_pass": not errors, "generation_status": "not_run", "video_verified": False,
              "submission_ready": not errors and not draft}
    if not errors:
        prompt, bindings = render_prompt(shot, profile)
        limit = profile.get("max_prompt_characters")
        if limit is not None and len(prompt) > limit:
            report["errors"].append({"code": "PROMPT_LENGTH", "message": "提示词超过该接口字数限制，请按优先级精简"})
            report["local_pass"] = report["submission_ready"] = False
        lint_errors, lint_warnings, _ = scan_text(prompt, task=shot["task"])
        report.update(prompt=prompt, bindings=bindings, lint={"errors": lint_errors, "warnings": lint_warnings},
                      start_state=shot["start_state"], end_state=shot["end_state"],
                      parameters={"duration_seconds": shot.get("duration_seconds"), "resolution": shot.get("resolution")},
                      editorial={k: shot.get(k) for k in ("intent", "visible_evidence", "focus", "audio")})
        if lint_errors:
            report["errors"].extend({"code": code, "message": message} for code, message in lint_errors)
            report["local_pass"] = report["submission_ready"] = False
    return report


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="manju-director 镜头检查与按任务组织提示词；不调用模型")
    ap.add_argument("shot", help="镜头 JSON 文件")
    ap.add_argument("--profile", required=True, help="profiles.json 中的版本键")
    ap.add_argument("--registry", help="自定义模型配置文件")
    ap.add_argument("--previous", help="前镜说明，用于检查声明的状态承接")
    ap.add_argument("--draft", action="store_true", help="允许待提供素材/未核实能力，结果不可提交")
    ap.add_argument("--out", help="保存完整准备报告；不覆盖输入")
    args = ap.parse_args()
    try:
        path = Path(args.shot)
        protected = {path.resolve(), (Path(args.registry) if args.registry else ROOT / "references/model-adapters/profiles.json").resolve()}
        if args.previous:
            protected.add(Path(args.previous).resolve())
        if args.out and Path(args.out).resolve() in protected:
            raise ValueError("输出不能覆盖镜头或模型配置")
        report = prepare(load_json(path), load_profile(args.profile, args.registry), path.parent,
                         args.draft, load_json(args.previous) if args.previous else None)
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text, end="")
        return 0 if report["local_pass"] else 1
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
