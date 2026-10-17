#!/usr/bin/env python3
"""Install/check/update/uninstall the local source without overwriting user edits.

Python 3.8+, no network, no configuration/auth changes. Only manifest-owned,
unchanged files are removed; extra files remain in place.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = "manju-director"
MARKER = ".manju-install.json"
HOST_DIRS = {"codex": ".agents", "claude": ".claude", "workbuddy": ".workbuddy"}
PAYLOAD_DIRS = ("assets", "references", "scripts", "examples", "docs", "benchmarks", "tests")
PAYLOAD_ROOTS = ("SKILL.md", "README.md", "LICENSE")
EXTENSIONS = {".md", ".json", ".py", ".txt", ".png", ".jpg", ".jpeg", ".webp", ".svg"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload(source=ROOT):
    source = Path(source).resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError("源码目录缺少 SKILL.md")
    files = {}
    paths = [source / name for name in PAYLOAD_ROOTS]
    for name in PAYLOAD_DIRS:
        if (source / name).is_dir():
            paths.extend((source / name).rglob("*"))
    for path in sorted(paths):
        relative = path.relative_to(source)
        if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
            continue
        if relative.parts[:2] == ("benchmarks", "results"):
            continue
        if path.is_symlink():
            raise ValueError("包内不接受符号链接: " + str(relative))
        if path.is_file() and path.suffix.lower() in EXTENSIONS or path.name == "LICENSE" and path.is_file():
            if source not in path.resolve().parents:
                raise ValueError("包文件超出源码目录")
            data = path.read_bytes()
            if path.suffix in (".md", ".json", ".py", ".txt"):
                data = data.replace(b"\r\n", b"\n")
            files[relative.as_posix()] = data
    return files


def manifest(files):
    hashes = {name: digest(data) for name, data in sorted(files.items())}
    bundle_id = digest(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode())
    return {"format": 1, "name": NAME, "bundle_id": bundle_id, "files": hashes}


def destination(host, scope="user", root=None):
    if scope == "project" and root is None:
        raise ValueError("项目级安装需要 --root 指定创作项目目录")
    base = Path(root).expanduser().resolve() if root else Path.home().resolve()
    return base / HOST_DIRS[host] / "skills" / NAME


def safe_file(target, relative):
    if not isinstance(relative, str):
        raise ValueError("受管文件路径必须是字符串")
    part = PurePosixPath(relative)
    if relative != part.as_posix() or relative == MARKER or part.is_absolute() or not part.parts or any(
            x in (".", "..") or ":" in x or "\\" in x for x in part.parts):
        raise ValueError("不合法的受管文件路径")
    path = target.joinpath(*part.parts)
    if target.resolve() not in path.resolve().parents:
        raise ValueError("受管文件越过安装目录")
    for ancestor in (path,) + tuple(path.parents):
        if ancestor == target.parent:
            break
        if ancestor.is_symlink():
            raise ValueError("安装目录内不接受符号链接")
    return path


def read_manifest(target):
    if target.is_symlink():
        raise ValueError("安装目标不能是符号链接")
    marker = target / MARKER
    if marker.is_symlink():
        raise ValueError("受管清单不能是符号链接")
    if not marker.is_file():
        raise ValueError("不是本安装器管理的版本；已保留现有目录")
    data = json.loads(marker.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("受管清单必须是 JSON 对象")
    bundle_id = data.get("bundle_id")
    if data.get("format") != 1 or data.get("name") != NAME or not isinstance(data.get("files"), dict) or not isinstance(bundle_id, str) or len(bundle_id) != 64:
        raise ValueError("受管清单格式不正确")
    for relative, expected in data["files"].items():
        safe_file(target, relative)
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("受管清单哈希不正确")
    return data


def check(target):
    target = Path(target)
    data = read_manifest(target)
    changed, missing = [], []
    for relative, expected in data["files"].items():
        path = safe_file(target, relative)
        if not path.is_file():
            missing.append(relative)
        elif digest(path.read_bytes()) != expected:
            changed.append(relative)
    return {"target": str(target), "bundle_id": data["bundle_id"], "files": len(data["files"]),
            "changed": changed, "missing": missing, "ok": not changed and not missing}


def _remove_owned(target, relatives):
    directories = set()
    for relative in relatives:
        path = safe_file(target, relative)
        if path.is_file():
            path.unlink()
        directories.update(p for p in path.parents if target.resolve() in p.resolve().parents)
    for directory in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        if directory.exists() and not any(directory.iterdir()):
            directory.rmdir()


def install(target, source=ROOT, update=False):
    target, source = Path(target), Path(source).resolve()
    if target.is_symlink() or target.resolve() == source or target.resolve() in source.parents:
        raise ValueError("安装目标不能覆盖源码或指向符号链接")
    if target.parent.exists() and target.parent.resolve() != target.parent.absolute():
        raise ValueError("安装目标父目录包含链接；请使用明确的实际路径")
    files = payload(source)
    current = manifest(files)
    old = None
    if target.exists():
        if not update:
            raise ValueError("安装目录已存在；现有内容未改动。受管版本更新请使用 update")
        old = read_manifest(target)
        status = check(target)
        if not status["ok"]:
            raise ValueError("受管文件已修改或缺失；为保留本地编辑而停止更新")
        for relative in files.keys() - old["files"].keys():
            if safe_file(target, relative).exists():
                raise ValueError("新增包文件与用户文件同名: " + relative)
    elif update:
        raise ValueError("更新目标不存在；请先 install")
    for relative in files:
        safe_file(target, relative)
    target.mkdir(parents=True, exist_ok=True)
    for relative, data in files.items():
        path = safe_file(target, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    if old:
        _remove_owned(target, set(old["files"]) - set(files))
    (target / MARKER).write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return check(target)


def uninstall(target):
    target = Path(target)
    data = read_manifest(target)
    status = check(target)
    if status["changed"]:
        raise ValueError("受管文件存在本地编辑，未卸载；请先保留编辑")
    # Every computed target is validated before the first deletion.
    for relative in data["files"]:
        safe_file(target, relative)
    _remove_owned(target, data["files"])
    (target / MARKER).unlink()
    retained = [str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()]
    if not any(target.iterdir()):
        target.rmdir()
    return {"target": str(target), "uninstalled": True, "retained": retained}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="manju-director 本地技能安装管理；无需网络或模型 key")
    ap.add_argument("action", choices=("install", "check", "update", "uninstall"))
    ap.add_argument("--host", required=True, choices=tuple(HOST_DIRS))
    ap.add_argument("--scope", choices=("user", "project"), default="user")
    ap.add_argument("--root", help="用户级的用户目录，或项目级的项目目录")
    args = ap.parse_args()
    try:
        target = destination(args.host, args.scope, args.root)
        if args.action in ("install", "update"):
            result = install(target, update=args.action == "update")
        elif args.action == "check":
            result = check(target)
        else:
            result = uninstall(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok", True) else 1
    except (OSError, ValueError, TypeError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
