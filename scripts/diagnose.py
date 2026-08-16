#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnose.py — 出片失败诊断引擎（manju-director 技能配套）

把 continuity-playbook 的失败矩阵 + dual-register 决策脚本化：
Phase 5/6 出片失败时，先跑本工具定位根因，再动手改——不要盲目重跑。

用法：
  python diagnose.py "人物变脸"          # 症状关键词 → 根因 + 修复 + 止损
  python diagnose.py "手"                 # 模糊匹配（多个命中会全部列出）
  python diagnose.py --all                # 列出全部诊断项
  python diagnose.py --dual "连续失败3次"  # dual-register 决策（轻改 vs 重跑）

零第三方依赖，Python 3.8+。
"""
import argparse
import sys

# (症状关键词, 根因, 修复方案(按顺序), 止损兜底)
DIAGNOSTICS = [
    (
        ["人物变脸", "换脸", "脸变了", "不是同一个人", "face swap", "face change", "脸崩"],
        "缺参考图 / 多人同框过载 / 锚点未逐字复述(R4)",
        [
            "加/换化妆参考图（角色定妆图冻结编号）",
            "减人：拆成正反打（shot/reverse-shot），别同框",
            "景别特写→中近景",
            "上防换脸三件套（参考图排他声明，image-prompt-engine §2）",
        ],
        "连续3次仍崩 → 回 Phase 2 重建定妆图，不要继续在原图上打补丁",
    ),
    (
        ["肢体崩坏", "手崩", "手指", "多手指", "胳膊", "limb", "hand", "手指断了", "手残"],
        "多动作叠加(违反R3) / 手部特写+运镜同时出现",
        [
            "砍到单主行动作（R3：1 主动作 + 至多 2 个微表情）",
            "手出画 或 固定机位",
            "运镜速度降一档",
        ],
        "仍崩 → 该镜改用手部特写帧（关键帧插入），不硬跑运动",
    ),
    (
        ["光影跳跃", "光跳", "光变了", "light jump", "光照不一致", "明暗突变"],
        "场景卡光源句未复述 / 尾帧与 prompt 光向冲突",
        [
            "把场景卡的光源句原样复制进 prompt 第一段",
            "换尾帧提取点（-t 0.2~0.5 前移）",
            "上光影四件套（光源方向/半面光/高光点/大光圈）",
        ],
        "仍跳 → 该镜改首尾帧模式（首帧+尾帧都由图像模型生成，光影可控）",
    ),
    (
        ["服装漂移", "发型漂移", "衣服变了", "clothing", "衣服颜色变了", "头发变了"],
        "锚点未逐字复述(R4) / 锚点只写了一次",
        [
            "从资产卡逐字复制外观锚点，禁止凭记忆重写",
            "把漂移项提升为形式弱点 + 三处复写（subject/CONSTRAINTS/Avoid）",
        ],
        "仍漂 → 该元素在 Phase 2 补一张特写定妆帧冻结",
    ),
    (
        ["文字乱码", "字幕乱码", "屏幕文字", "garbled", "乱码", "字花了"],
        "屏幕/纸面文字入镜（AI 模型必乱码）",
        [
            "改为'模糊发光的字符流 / 无法辨认的手写'",
            "可读文字一律后期合成，不进模型",
        ],
        "强剧情需要清晰文字 → 后期合成或分镜换角度避开",
    ),
    (
        ["运动鬼畜", "瞬移", "传送", "glitch", "抽搐", "抖动", "动作跳变"],
        "运镜过快 + 动作幅度过大叠加",
        [
            "运镜降一档（快速→中速→匀速）",
            "动作幅度降到'半步/微倾'级",
        ],
        "仍鬼畜 → 该镜改固定机位 + 单动作",
    ),
    (
        ["路人崩坏", "背景人", "群众", "bystander", "路人脸", "背景人物"],
        "深景深群戏，后景人物模糊变形",
        [
            "换浅景深背景虚化",
            "prompt 写'背景人物剪影化，无面部细节'",
        ],
        "仍崩 → 清空后景人群，只保留主体",
    ),
    (
        ["首尾循环", "loop", "循环感", "原地循环", "走路原地"],
        "零位移 + 对称动作（模型陷入循环）",
        [
            "加微位移（慢推 5% 或视线变化）",
            "打破动作对称性",
        ],
        "仍循环 → 换首尾帧模式，首帧尾帧明确位移方向",
    ),
    (
        ["视觉锚点缺失", "多焦点", "画面杂", "没有重点", "找不到主体"],
        "一图多焦点，模型不知道该放大谁",
        [
            "只留 1 个视觉锚点（光斑/丝带/剑尖 三选一）",
            "其余元素降为环境",
        ],
        "角色多 → 拆镜，别在一镜里塞多人戏",
    ),
    (
        ["噪点", "模糊", "画质糊", "不清", "blurry", "noisy", "脏", "模糊不清"],
        "分辨率不足（不是真噪点）",
        [
            "整体拉到 2K/4K",
            "HD 重绘：原图回投 + 强写'保持角色/脸/姿势/构图/色彩/特效全部不变，只提升质量'",
        ],
        "重绘后仍糊 → 换更高质量底模/平台",
    ),
    (
        ["长对话看地", "眼神漂移", "eye-line", "视线失控", "两人都低头", "不看对方"],
        "长距离对话视线控制丢失",
        [
            "上'长对话视线锁定三件套'（lighting-styles §11）",
            "在【body + CONSTRAINTS + Avoid】三处复写视线句",
        ],
        "仍丢 → 拆成正反打单人头像，别同框",
    ),
    (
        ["口型对不上", "口型", "lip sync", "嘴型"],
        "强口型戏的唇形同步瓶颈（模型极限 92% 左右）",
        [
            "改背景旁白（不露口型）",
            "后期配音替换",
        ],
        "必须露口型 → 选平台口型能力最强模型",
    ),
    (
        ["音画脱节", "配乐不搭", "声音不对", "audio", "音效"],
        "无音频参考，模型自由发挥",
        [
            "绑定 @音频 参考（节奏/情绪锚点）",
            "视频 prompt 声音基线补全（环境音+音乐情绪）",
        ],
        "仍脱节 → 后期配乐，不靠模型",
    ),
    (
        ["动作僵硬", "不自然", "stiff", "像木偶", "机械"],
        "缺速度/物理关键词",
        [
            "补'缓慢/匀速'速度词",
            "补惯性/呼吸起伏等物理细节",
        ],
        "仍僵 → 换更自然的参考动作视频",
    ),
    (
        ["穿模", "clipping", "嵌进", "穿过", "重叠穿帮"],
        "动作幅度过大或物体交互复杂",
        [
            "简化动作",
            "减少人与物交互面积",
        ],
        "仍穿模 → 后期合成补穿帮，不硬跑",
    ),
]

# dual-register 决策：轻改 vs 重跑（continuity-playbook §4.1）
DUAL_REGISTER = {
    "light": [
        "只改 1 个变量（表情/光/构图）",
        "模板：Change X to Y, do not touch anything else.",
        "适合：用 Nano-Pro 类图生图理解模型",
    ],
    "heavy": [
        "同时改 >=3 项 / 改姿势 / 改结构 / 改机位",
        "连续轻改导致脸融化和换脸 → 立即停",
        "适合：用 Image 类模型完全重建",
    ],
    "stop": "重跑前先诊断根因（本工具），不要盲目重跑同一批词",
}


def match(query):
    q = query.lower()
    hits = []
    for keywords, cause, fixes, fallback in DIAGNOSTICS:
        if any((k.lower() in q) or (q in k.lower()) for k in keywords):
            hits.append((keywords, cause, fixes, fallback))
    return hits


def format_one(keywords, cause, fixes, fallback):
    lines = [
        "══════════════════════════════════════",
        "🩺 诊断命中：%s" % " / ".join(keywords),
        "══════════════════════════════════════",
        "【根因】%s" % cause,
        "【修复方案】（按顺序尝试）",
    ]
    for i, f in enumerate(fixes, 1):
        lines.append("  %s %s" % ("①②③④⑤⑥"[i - 1] if i <= 6 else "·", f))
    lines.append("【止损兜底】%s" % fallback)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="出片失败诊断引擎（manju-director 配套）")
    ap.add_argument("query", nargs="?", help="症状关键词，如 '人物变脸' / '手'")
    ap.add_argument("--all", action="store_true", help="列出全部诊断项")
    ap.add_argument("--dual", nargs="?", const="?", help="dual-register 决策（轻改 vs 重跑）；可传 '连续失败' 等情境词")
    args = ap.parse_args()

    if args.dual:
        print("🔄 dual-register 决策（continuity-playbook §4.1）")
        print()
        print("【轻改 light edit】先试一次：")
        for x in DUAL_REGISTER["light"]:
            print("  • %s" % x)
        print()
        print("【重跑 heavy rerun】以下情况直接重跑：")
        for x in DUAL_REGISTER["heavy"]:
            print("  • %s" % x)
        print()
        print("【铁律】%s" % DUAL_REGISTER["stop"])
        print()
        print("💡 建议：先跑 diagnose.py 定位根因，再决定轻改还是重跑。")
        return

    if args.all:
        print("🩺 全部诊断项（%d 条）" % len(DIAGNOSTICS))
        print()
        for keywords, cause, fixes, fallback in DIAGNOSTICS:
            print(format_one(keywords, cause, fixes, fallback))
            print()
        return

    if not args.query:
        ap.print_help()
        return

    hits = match(args.query)
    if not hits:
        print("❌ 未命中已知症状。试试更短的关键词（如 '手' / '光' / '脸'），或 --all 查看全部。")
        sys.exit(1)

    for keywords, cause, fixes, fallback in hits:
        print(format_one(keywords, cause, fixes, fallback))
        print()


if __name__ == "__main__":
    main()
