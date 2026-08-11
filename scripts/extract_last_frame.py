#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_last_frame.py — 视频尾帧提取工具（manju-director 技能配套）

用途：提取镜 N 成片的最后一帧（或倒数第 t 秒的帧），作为镜 N+1 的首帧输入，
实现"尾帧承接"的画面连贯机制。封装 ffmpeg/ffprobe，Windows/macOS/Linux 通用。

用法：
  python extract_last_frame.py input.mp4                     # 提取最后一帧
  python extract_last_frame.py input.mp4 -o frames           # 指定输出目录
  python extract_last_frame.py input.mp4 -t 0.3              # 取倒数 0.3 秒处（尾帧有运动模糊时用）
  python extract_last_frame.py input.mp4 --shot 12           # 输出命名 shot_012_last.png
  python extract_last_frame.py ./clips/ --batch              # 批量：目录内所有视频

输出：默认 <输入名>_last.png；--shot N 时输出 shot_%03d_last.png（与分镜表镜号对应）。
依赖：ffmpeg 与 ffprobe 需在 PATH 中（或设置 FFMPEG_BIN / FFPROBE_BIN 环境变量）。
"""
import argparse
import json
import os
import re
import subprocess
import sys


def find_bin(name, env_var):
    """定位 ffmpeg/ffprobe 可执行文件。"""
    candidates = [os.environ.get(env_var, ""), name, name + ".exe"]
    for c in candidates:
        if not c:
            continue
        try:
            subprocess.run([c, "-version"], capture_output=True, check=True)
            return c
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return None


def get_duration(ffprobe, path):
    """用 ffprobe 读视频时长（秒，float）。"""
    out = subprocess.run(
        [ffprobe, "-v", "error", "-print_format", "json",
         "-show_entries", "format=duration", path],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def extract(ffmpeg, ffprobe, video, out_dir, offset=0.0, shot=None):
    """提取单条视频的尾帧，返回输出路径。"""
    duration = get_duration(ffprobe, video)
    # 结尾留 1 帧安全边距（约 0.04s），再叠加用户 offset
    t = max(0.0, duration - 0.04 - offset)

    base = os.path.splitext(os.path.basename(video))[0]
    if shot is not None:
        name = "shot_%03d_last.png" % shot
    else:
        safe = re.sub(r"[^\w\-\u4e00-\u9fff]+", "_", base)
        name = "%s_last.png" % safe
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, name)

    # -ss 放 -i 前做快速seek，sseof 语义不稳，故用绝对时间点
    subprocess.run(
        [ffmpeg, "-y", "-ss", "%.3f" % t, "-i", video,
         "-frames:v", "1", "-q:v", "1", out_path],
        capture_output=True, check=True,
    )
    return out_path, t, duration


def main():
    ap = argparse.ArgumentParser(description="视频尾帧提取（尾帧承接机制配套工具）")
    ap.add_argument("input", help="视频文件路径，或 --batch 模式下的目录")
    ap.add_argument("-o", "--out", default=None, help="输出目录（默认与视频同目录）")
    ap.add_argument("-t", "--offset", type=float, default=0.0,
                    help="从末尾往前偏移的秒数，尾帧模糊时用 0.2~0.5")
    ap.add_argument("--shot", type=int, default=None,
                    help="分镜表镜号，输出命名为 shot_###_last.png")
    ap.add_argument("--batch", action="store_true", help="批量处理目录内所有视频")
    args = ap.parse_args()

    ffmpeg = find_bin("ffmpeg", "FFMPEG_BIN")
    ffprobe = find_bin("ffprobe", "FFPROBE_BIN")
    if not ffmpeg or not ffprobe:
        sys.exit("错误：未找到 ffmpeg/ffprobe。请安装 ffmpeg 并加入 PATH，"
                 "或设置 FFMPEG_BIN / FFPROBE_BIN 环境变量。")

    if args.batch:
        if not os.path.isdir(args.input):
            sys.exit("错误：--batch 模式下 input 必须是目录")
        out_dir = args.out or os.path.join(args.input, "frames")
        videos = [f for f in sorted(os.listdir(args.input))
                  if f.lower().endswith((".mp4", ".mov", ".mkv", ".webm"))]
        if not videos:
            sys.exit("目录内未找到视频文件")
        for f in videos:
            p = os.path.join(args.input, f)
            m = re.search(r"(\d+)", f)
            shot = args.shot if args.shot is not None else (int(m.group(1)) if m else None)
            try:
                out, t, dur = extract(ffmpeg, ffprobe, p, out_dir, args.offset, shot)
                print("[OK] %s -> %s (取帧点 %.2fs / 总长 %.2fs)" % (f, out, t, dur))
            except Exception as e:
                print("[FAIL] %s: %s" % (f, e), file=sys.stderr)
    else:
        if not os.path.isfile(args.input):
            sys.exit("错误：文件不存在 %s" % args.input)
        out_dir = args.out or os.path.dirname(os.path.abspath(args.input))
        out, t, dur = extract(ffmpeg, ffprobe, args.input, out_dir, args.offset, args.shot)
        print("[OK] 尾帧已提取：%s" % out)
        print("     取帧点 %.2fs / 总长 %.2fs（-t 可往前偏移）" % (t, dur))
        print("     下一步：将此图作为下一镜头的首帧输入（尾帧承接）。")


if __name__ == "__main__":
    main()
