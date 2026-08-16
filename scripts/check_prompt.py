#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_prompt.py — 视频/图像 prompt 反模式检测器（manju-director 技能配套）

把 manju-director 的文档规则（R3 单主行动作 / 冲突指令 / 抽象词 /
NON-NEGOTIABLE 要素 / 失败矩阵触发条件）变成可执行检查：
每个 prompt 在交付前必须先过本检测器，agent 没有"略过"选项。

用法：
  python check_prompt.py --file prompt.txt              # 检查单个文件
  python check_prompt.py --dir prompts/                 # 批量扫描目录
  python check_prompt.py --text "prompt 文本"            # 直接传文本
  python check_prompt.py --strict                       # warning 也返回退出码 1

退出码：0 = 无 error；1 = 存在 error（或 --strict 时存在 warning）。
零第三方依赖，Python 3.8+。
"""
import argparse
import os
import re
import sys

# ─────────────────────────────────────────────
# 规则库（可按实战持续扩充）
# ─────────────────────────────────────────────

# 抽象词黑名单：无实指、模型不响应、稀释信息密度
# (词, 豁免复合词列表) —— "高级极简" 不误报，但单独出现的 "高级感" 命中
ABSTRACT_WORDS = [
    ("唯美", []), ("氛围感", []), ("高级感", ["高级感镜头"]),
    ("很有质感", []), ("精致感", []), ("科技感", []), ("大片感", []),
    ("电影感", ["电影感镜头", "电影质感"]), ("很科幻", []), ("未来感", []),
    ("压迫感", []), ("感觉不对", []), ("很有feel", []), ("满满的", []),
]

# 冲突指令对：同一 prompt 内同时出现 = 模型左右为难
CONFLICT_PAIRS = [
    ("静止", "冲刺"), ("静止", "快速奔跑"), ("固定机位", "推镜头"),
    ("固定机位", "跟拍"), ("昏暗", "高亮"), ("特写", "远景"),
    ("全景", "大特写"), ("快速", "极缓慢"), ("高速", "极缓"),
    ("没有风", "衣袂飘动"), ("面无表情", "微笑"), ("闭眼", "睁眼"),
    ("静止", "旋转"), ("室内", "室外"), ("白天", "夜晚"),
]

# R3 主动作动词（中英）：统计命中数，>=3 判定多动作叠加
ACTION_VERBS = [
    # 中文
    "推门", "转身", "抬手", "放下", "拿起", "抓起", "坐下", "站起", "走近",
    "冲", "跑", "跳", "扑", "挥", "踢", "砸", "躲", "闪", "抓", "握紧",
    "掏出", "抽出", "按下", "划开", "点了一下", "拍了拍", "抬眸", "低头",
    "转身", "抬头", "摇头", "点头", "后退", "前倾", "倾斜", "跌倒",
    # 英文
    "push", "grab", "sits", "stands", "walks", "runs", "jumps", "throws",
    "turns", "raises", "lowers", "presses", "swipes", "picks up", "puts down",
    "leans", "steps back", "lunges",
]

# 失败矩阵触发条件（高风险项）：出现即 warning
RISK_PATTERNS = [
    ("hand close-up|手部特写|指尖特写|hands?", "手部特写 —— 模型最高失分区，配合运镜更危险"),
    ("字幕|subtitle|watermark|水印|屏幕文字|text on screen", "文字/字幕入镜 —— 必乱码，应改为模糊字符流或后期合成"),
    ("一群人|crowd|群众|路人|bystand", "多人/群众入镜 —— 后景人物易崩坏"),
    ("水花|瀑布|水流|溅|fluid|liquid|splash", "流体物理 —— 易穿模，建议降低幅度"),
    ("快速|高速|fast|rapid", "高速运动 —— 易糊帧抖动，建议降一档速度"),
    ("180°|180度|全景旋转|full rotation", "大角度旋转 —— 易翻车，建议 <=90°"),
    ("爆炸|explosion|火焰|fire", "爆炸/火焰 —— 高难度特效，建议简化或后期"),
]

# NON-NEGOTIABLE 缺失检测（对应 image/video 引擎的不可省略块）
MISSING_CHECKS = [
    (
        "ref",
        "参考图声明缺失",
        ["reference", "ref:", "@视频", "首帧", "first frame", "上一镜", "定妆", "concept art", "原图"],
        "error",
        "prompt 必须引用参考图（reference/首帧/定妆图/@视频1）——无参考图 = 换脸/漂移风险",
    ),
    (
        "negline",
        "负面提示缺失",
        ["no ", "no.", "without", "avoid", "禁止", "不要", "无", "no text", "no watermark"],
        "warning",
        "负面提示缺失——无负向字段的模型（即梦/Nano Banana）必须把'不要什么'写成负面末行",
    ),
    (
        "light",
        "光影四件套疑似缺失（角色帧）",
        ["光", "light", "光源", "逆光", "侧光", "主光", "shadow", "阴影", "高光", "眼神光"],
        "info",
        "角色帧应有光影四件套：光源方向/半面光/高光点/大光圈背景虚化；无任何光影词 = 平光证件照",
    ),
    (
        "style",
        "画风锚点缺失",
        ["风格", "style", "画风", "质感", "电影", "cinematic", "comic", "anime", "ink"],
        "warning",
        "缺少风格锚点——同角色跨镜会画风漂移",
    ),
]


def _contains_any(text, keywords):
    low = text.lower()
    return any(k.lower() in low for k in keywords)


def check_abstract(text):
    out = []
    for word, exempts in ABSTRACT_WORDS:
        if word.lower() in text.lower():
            if exempts and any(e.lower() in text.lower() for e in exempts):
                continue
            out.append((word, "抽象词 —— 无实指，模型不响应，建议换成具体描写（材质/光线/动作）"))
    return out


def check_conflicts(text):
    out = []
    low = text.lower()
    for a, b in CONFLICT_PAIRS:
        if a.lower() in low and b.lower() in low:
            out.append(("%s + %s" % (a, b), "冲突指令 —— 同一 prompt 内互相矛盾，模型只能随机挑一个执行"))
    return out


def check_action_overload(text):
    hits = [v for v in ACTION_VERBS if v.lower() in text.lower()]
    if len(hits) >= 3:
        return [(", ".join(hits), "多动作叠加（R3 违反）—— 单镜头只允许 1 个主动作 + 至多 2 个微表情变化；堆叠是肢体崩坏头号原因")]
    return []


def _is_negated(text, span_start):
    """检查命中位置前 25 字符内是否有否定词（负面提示里的 'no subtitles' 不误报为风险项）"""
    window = text[max(0, span_start - 25):span_start].lower()
    return any(w in window for w in ("no ", "no.", "not", "without", "avoid", "禁止", "不要", "无 ", "勿"))


def check_risks(text):
    out = []
    for pat, msg in RISK_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if _is_negated(text, m.start()):
                continue
            out.append((pat, msg))
            break
    return out


def check_missing(text):
    out = []
    for code, name, keywords, level, advice in MISSING_CHECKS:
        if not _contains_any(text, keywords):
            out.append((code, name, level, advice))
    return out


def scan_text(text, strict=False):
    errors, warnings, infos = [], [], []

    for word, msg in check_abstract(text):
        warnings.append(("ABSTRACT", "抽象词: %s — %s" % (word, msg)))
    for pair, msg in check_conflicts(text):
        errors.append(("CONFLICT", "冲突指令: %s — %s" % (pair, msg)))
    for verbs, msg in check_action_overload(text):
        errors.append(("R3-OVERLOAD", "%s — %s" % (verbs, msg)))
    for pat, msg in check_risks(text):
        warnings.append(("RISK", "%s — %s" % (pat, msg)))
    for code, name, level, advice in check_missing(text):
        entry = ("MISSING", "[%s] %s — %s" % (code, name, advice))
        if level == "error":
            errors.append(entry)
        elif level == "warning":
            warnings.append(entry)
        else:
            infos.append(entry)

    return errors, warnings, infos


def format_result(name, text, strict=False):
    errors, warnings, infos = scan_text(text, strict)
    lines = ["══════════════════════════════════════",
             "🔍 反模式检测：%s" % name,
             "══════════════════════════════════════"]
    if not errors and not warnings and not infos:
        lines.append("✅ 通过 —— 未检出反模式")
    for level, tag, items in (("❌", "ERROR", errors), ("⚠️", "WARNING", warnings), ("💡", "INFO", infos)):
        if items:
            lines.append("%s %s x%d" % (level, tag, len(items)))
            for _, msg in items:
                lines.append("  • %s" % msg)
    has_error = bool(errors) or (strict and warnings)
    lines.append("结果：%s" % ("❌ 存在 error，交付前必须修改" if has_error else
                              ("⚠️ 有 warning（无 error），建议修改后交付" if warnings else "✅ 可交付")))
    return "\n".join(lines), has_error


def main():
    ap = argparse.ArgumentParser(description="视频/图像 prompt 反模式检测器（manju-director 配套）")
    ap.add_argument("--file", help="单个 prompt 文件（.txt/.md）")
    ap.add_argument("--dir", help="批量扫描目录（*.txt/*.md）")
    ap.add_argument("--text", help="直接传入 prompt 文本")
    ap.add_argument("--strict", action="store_true", help="warning 也计入失败（退出码 1）")
    args = ap.parse_args()

    if args.file:
        if not os.path.isfile(args.file):
            sys.exit("错误：文件不存在 %s" % args.file)
        text = open(args.file, encoding="utf-8", errors="replace").read()
        out, has_error = format_result(os.path.basename(args.file), text, args.strict)
        print(out)
        sys.exit(1 if has_error else 0)

    if args.dir:
        if not os.path.isdir(args.dir):
            sys.exit("错误：目录不存在 %s" % args.dir)
        files = sorted(f for f in os.listdir(args.dir)
                       if f.lower().endswith((".txt", ".md")))
        if not files:
            sys.exit("目录内未找到 .txt/.md 文件")
        any_error = False
        for f in files:
            text = open(os.path.join(args.dir, f), encoding="utf-8", errors="replace").read()
            out, has_error = format_result(f, text, args.strict)
            print(out)
            print()
            any_error = any_error or has_error
        sys.exit(1 if any_error else 0)

    if args.text:
        out, has_error = format_result("inline prompt", args.text, args.strict)
        print(out)
        sys.exit(1 if has_error else 0)

    ap.print_help()


if __name__ == "__main__":
    main()
