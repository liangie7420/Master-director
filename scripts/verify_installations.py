#!/usr/bin/env python3
"""Verify isolated installs and bundled tools, with optional local Codex discovery.

No model inference, account writes, live user skill replacement or video calls.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from manage_skill import ROOT, check, destination, install, uninstall


def _strings(obj):
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for value in obj.values() for s in _strings(value)]
    if isinstance(obj, list):
        return [s for value in obj for s in _strings(value)]
    return []


def verify(discover=False):
    result = {"schema_version": 1, "inference_called": False, "video_generation": "not_run", "hosts": []}
    with tempfile.TemporaryDirectory(prefix="manju-host-verification-") as temporary:
        temp = Path(temporary).resolve()
        for host in ("codex", "claude", "workbuddy"):
            scope = temp / host
            scope.mkdir()
            target = destination(host, "project", scope)
            installed = install(target)
            run = subprocess.run([sys.executable, str(target / "scripts/prepare_example.py"),
                                  "--out", str(scope / "creative-output")], cwd=scope,
                                 capture_output=True, text=True, encoding="utf-8", timeout=25)
            if run.returncode != 0:
                raise ValueError(host + " 包内示例失败: " + run.stderr)
            example = json.loads(run.stdout)
            if example["shots"] != 10 or example["seconds"] != 60 or example["generation_status"] != "not_run":
                raise ValueError("示例状态不符合预期")
            unchanged = check(target)["ok"]
            updated = install(target, update=True)["ok"]
            discovery = {"status": "not_run", "reason": "No host model session is started"}
            if host == "codex" and discover and shutil.which("codex"):
                if os.name == "nt":
                    command = ["powershell", "-NoProfile", "-Command",
                               "codex -C '" + str(scope).replace("'", "''") + "' debug prompt-input"]
                else:
                    command = ["codex", "-C", str(scope), "debug", "prompt-input"]
                discovered = subprocess.run(command, capture_output=True, text=True,
                                            encoding="utf-8", errors="replace", timeout=35)
                if discovered.returncode == 0:
                    context = "\n".join(_strings(json.loads(discovered.stdout))).replace("\\", "/")
                    match = re.search(r"manju-director:.*?\(file: (r\d+)/manju-director/SKILL\.md\)", context)
                    expected = str(target.parent).replace("\\", "/")
                    alias_line = any(expected in line and match and match.group(1) in line
                                     for line in context.splitlines())
                    # Some versions print full paths instead of root aliases.
                    full_path = str(target / "SKILL.md").replace("\\", "/") in context
                    discovery = {"status": "passed" if alias_line or full_path else "unconfirmed",
                                 "method": "codex debug prompt-input", "inference_called": False}
                else:
                    discovery = {"status": "unavailable", "command_exit": discovered.returncode}
            removed = uninstall(target)["uninstalled"]
            result["hosts"].append({"host": host, "files": installed["files"],
                                    "install": installed["ok"], "check_after_tools": unchanged,
                                    "example_shots": example["shots"], "example_seconds": example["seconds"],
                                    "update": updated, "uninstall": removed, "host_discovery": discovery})
    result["local_pass"] = all(all(row[key] for key in ("install", "check_after_tools", "update", "uninstall"))
                               for row in result["hosts"])
    return result


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="隔离验证三个宿主的技能安装与包内示例；不调用模型")
    ap.add_argument("--discover-codex", action="store_true", help="使用本地 CLI 只读检查启动技能上下文")
    ap.add_argument("--out", default=str(ROOT / "dist/install-check.json"))
    args = ap.parse_args()
    try:
        output = Path(args.out).resolve()
        if output.suffix.lower() != ".json" or any(folder in output.parents for folder in
                (ROOT / "scripts", ROOT / "assets", ROOT / "references", ROOT / "examples", ROOT / "tests")):
            raise ValueError("请把 JSON 验证结果写到独立产物目录")
        result = verify(args.discover_codex)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["local_pass"] else 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
