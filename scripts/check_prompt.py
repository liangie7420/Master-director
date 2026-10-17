#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task-aware prompt linting; use prepare_shot.py for asset/capability checks.

Python 3.8+, standard library only. Exit 0 = local pass, 1 = error (or --strict warning).
Lexical hints do not certify generated-video quality.
"""
import argparse
import json
from pathlib import Path
import re
import sys

TASKS = ("auto", "asset_image", "first_frame_image", "end_frame_image", "text_to_video",
         "image_to_video", "keyframe_pair", "multimodal_reference", "video_edit", "video_extend")
REFERENCE_TASKS = {"image_to_video", "keyframe_pair", "multimodal_reference", "video_edit", "video_extend"}
REF_RE = re.compile(
    r"(?:@?(?:图片|图像|视频|音频)\s*\d+|\b(?:image|video|audio)\s*\d+\b|"
    r"\breference\s+(?:image\s*)?\d+\b|(?:首帧|尾帧|定妆图|上一镜|first frame|last frame))", re.I)
ABSTRACT_WORDS = ["唯美", "氛围感", "高级感", "很有质感", "精致感", "科技感",
                  "大片感", "电影感", "很科幻", "未来感", "压迫感", "感觉不对"]
CONFLICT_PAIRS = [("静止", "冲刺"), ("固定机位", "推镜头"), ("固定机位", "跟拍"),
                  ("面无表情", "微笑"), ("闭眼", "睁眼"), ("静止", "旋转")]
ACTION_VERBS = ["推门", "转身", "抬手", "放下", "拿起", "抓起", "坐下", "站起", "走近",
                "冲刺", "奔跑", "跳跃", "挥剑", "握紧", "掏出", "按下", "抬眸", "低头",
                "抬头", "摇头", "点头", "后退", "前倾", "跌倒", "push", "pushes", "grab",
                "grabs", "sits down", "stands up", "walks", "runs", "jumps", "throws", "turns",
                "raises", "lowers", "presses", "swipes", "picks up", "puts down", "leans", "steps back"]
RISK_PATTERNS = [
    (r"\bhand close-up\b|手部特写|指尖特写", "手部近景：检查接触关系、动作幅度与样片"),
    (r"字幕|\bsubtitles?\b|\bwatermarks?\b|水印|屏幕文字|\btext on screen\b", "画面文字：按目标模型验证可读性和字幕要求"),
    (r"一群人|\bcrowd\b|群众|路人|\bbystanders?\b", "多人入镜：明确主体绑定和前后景位置"),
    (r"水花|瀑布|溅|\bfluid\b|\bliquid\b|\bsplash\b", "流体交互：核验接触与遮挡"),
    (r"快速|高速|\bfast\b|\brapid\b", "高速运动：核验轨迹、清晰度与镜头目的"),
    (r"180°|180度|全景旋转|\bfull rotation\b", "大角度运镜：核验空间关系与身份保持"),
]


def _clauses(text):
    return re.split(r"[。；;！!？?\n,.，]+", text)


def _is_negated(text, span_start):
    prefix = re.split(r"[。；;！!？?\n,.，]+", text[:span_start])[-1].lower()
    return bool(re.search(r"\b(?:no|not|without|avoid|never)\b|禁止|不要|避免|勿|无", prefix))


def check_abstract(text):
    return [(w, "建议用可见行为、构图或材质说明含义；有充分上下文时可保留")
            for w in ABSTRACT_WORDS if w in text]


def check_conflicts(text):
    out = []
    for clause in _clauses(text):
        if re.search(r"随后|然后|再|先|接着|之前|之后|从.*到|→|\b(?:then|before|after)\b", clause, re.I):
            continue
        for a, b in CONFLICT_PAIRS:
            if a in clause and b in clause:
                out.append((a + " + " + b, "同一短句含相反状态；请核对主体、时间与作用范围"))
    return list(dict.fromkeys(out))


def check_action_overload(text):
    verbs = sorted(set(ACTION_VERBS), key=len, reverse=True)
    pattern = "|".join((r"\b" + re.escape(v) + r"\b") if v.isascii() else re.escape(v) for v in verbs)
    hits = []
    for clause in _clauses(text):
        if re.search(r"\bcamera\b|镜头|运镜|机位", clause, re.I):
            continue
        for match in re.finditer(pattern, clause, re.I):
            if not _is_negated(clause, match.start()):
                hits.append(match.group(0).lower())
    hits = list(dict.fromkeys(hits))
    if len(hits) >= 3:
        return [(", ".join(hits), "动作词较多；核对因果步骤和不同主体，必要时拆镜")]
    return []


def check_risks(text):
    out = []
    for pattern, advice in RISK_PATTERNS:
        for match in re.finditer(pattern, text, re.I):
            if not _is_negated(text, match.start()):
                out.append((pattern, advice))
                break
    return out


def check_missing(text, task="auto"):
    out = []
    if task in REFERENCE_TASKS and not REF_RE.search(text):
        out.append(("ref", "参考素材声明缺失", "error", "当前任务需要带编号或角色的素材声明；实际文件由 prepare_shot.py 核验"))
    if task in ("auto", "asset_image", "first_frame_image", "end_frame_image", "text_to_video"):
        if not re.search(r"风格|画风|质感|电影|\b(?:style|cinematic|comic|anime|ink)\b", text, re.I):
            out.append(("style", "画风锚点缺失", "warning", "确认画风由文本、素材或参数中的哪一项提供"))
    return out


def scan_text(text, strict=False, task="auto"):
    if not text.strip():
        return [("EMPTY", "提示词为空")], [], []
    errors, warnings, infos = [], [], []
    for word, advice in check_abstract(text):
        warnings.append(("ABSTRACT", word + " — " + advice))
    for pair, advice in check_conflicts(text):
        warnings.append(("POSSIBLE-CONFLICT", pair + " — " + advice))
    for verbs, advice in check_action_overload(text):
        warnings.append(("ACTION-LOAD", verbs + " — " + advice))
    for _, advice in check_risks(text):
        warnings.append(("RISK", advice))
    for code, name, level, advice in check_missing(text, task):
        (errors if level == "error" else warnings).append(("MISSING", "[%s] %s — %s" % (code, name, advice)))
    return errors, warnings, infos


def format_result(name, text, strict=False, task="auto"):
    errors, warnings, infos = scan_text(text, strict, task)
    lines = ["🔍 提示词本地检查：%s" % name]
    for label, items in (("ERROR", errors), ("WARNING", warnings), ("INFO", infos)):
        for code, message in items:
            lines.append("%s [%s] %s" % (label, code, message))
    failed = bool(errors) or (strict and bool(warnings))
    lines.append("❌ 本地检查未通过" if failed else "✅ 本地检查通过；成片效果仍需样片验证")
    return "\n".join(lines), failed


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="manju-director 提示词本地检查（词法提示不等于成片质量）")
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="单个 UTF-8 prompt 文件")
    source.add_argument("--dir", help="目录内的 .txt/.md 文件")
    source.add_argument("--text", help="直接传入提示词")
    ap.add_argument("--task", choices=TASKS, default="auto")
    ap.add_argument("--strict", action="store_true", help="warning 也计入本地检查失败")
    ap.add_argument("--json", action="store_true", help="输出结构化检查结果")
    args = ap.parse_args()
    try:
        if args.file:
            paths = [Path(args.file)]
        elif args.dir:
            directory = Path(args.dir)
            if not directory.is_dir():
                raise ValueError("目录不存在: " + args.dir)
            paths = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in (".txt", ".md"))
            if not paths:
                raise ValueError("目录内未找到 .txt/.md 文件")
        else:
            paths = []
        inputs = [(p.name, p.read_text(encoding="utf-8-sig")) for p in paths] if paths else [("inline prompt", args.text)]
        reports, failed = [], False
        for name, prompt in inputs:
            errors, warnings, infos = scan_text(prompt, args.strict, args.task)
            message, bad = format_result(name, prompt, args.strict, args.task)
            failed = failed or bad
            reports.append({"name": name, "errors": errors, "warnings": warnings, "infos": infos,
                            "local_pass": not bad, "video_verified": False})
            if not args.json:
                print(message)
        if args.json:
            print(json.dumps(reports, ensure_ascii=False, indent=2))
        return 1 if failed else 0
    except (OSError, UnicodeError, ValueError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
