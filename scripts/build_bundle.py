#!/usr/bin/env python3
"""Create a deterministic local skill ZIP, with hashes and no Git/private state."""
import argparse
import json
from pathlib import Path
import sys
import zipfile

from manage_skill import NAME, ROOT, manifest, payload


def build(output, source=ROOT):
    output = Path(output).expanduser()
    if output.is_symlink():
        raise ValueError("安装包不能指向符号链接")
    output = output.resolve()
    source = Path(source).resolve()
    if output.suffix.lower() != ".zip":
        raise ValueError("安装包必须是 .zip")
    if output.is_symlink() or source / ".git" in output.parents:
        raise ValueError("安装包不能指向链接或 Git 元数据目录")
    for name in ("assets", "references", "scripts", "examples", "docs", "benchmarks", "tests"):
        folder = source / name
        if output == folder or folder in output.parents:
            raise ValueError("安装包不能写入包内源码目录")
    files = payload(source)
    data = manifest(files)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        members = dict(files)
        members["bundle-manifest.json"] = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
        for relative, content in sorted(members.items()):
            entry = zipfile.ZipInfo(NAME + "/" + relative, date_time=(2020, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    return {"path": str(output), "bundle_id": data["bundle_id"], "files": len(files), "bytes": output.stat().st_size}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="构建 manju-director 通用技能安装包")
    ap.add_argument("--out", default=str(ROOT / "dist/manju-director.zip"))
    args = ap.parse_args()
    try:
        print(json.dumps(build(args.out), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
