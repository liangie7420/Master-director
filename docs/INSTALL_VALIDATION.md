# 安装与示例验证记录

日期：2026-10-17。环境：Windows、Python 3.13.14；本机 Codex 0.154.0、Claude Code 2.1.281，WorkBuddy 已运行。

## 实际完成的本地验证

以下验证使用临时目录，不替换用户当前技能，也不启动额外模型会话：

| 检查 | 结果与边界 |
|---|---|
| 三种目录布局 | Codex 的 .agents/skills、Claude Code 的 .claude/skills、WorkBuddy 的 .workbuddy/skills 均完成完整文件安装、校验、更新、卸载 |
| 包内工具 | 从与技能目录无关的创作目录运行已安装的固定示例准备器；运行后技能文件哈希未变 |
| Codex 发现 | codex debug prompt-input 的启动上下文能发现临时项目安装的 manju-director，未调用推理 |
| Claude Code 与 WorkBuddy 发现 | 未启动新版技能创作会话；菜单发现、新版导入和实际调用待验证 |
| ZIP 独立性 | 重复构建内容一致；解压完整包后可安装，并在另一个目录运行包内工具 |
| 文件保护 | 覆盖旧目录、本地编辑、新增文件重名及越界清单均拒绝；卸载保留用户额外文件 |
| 回归 | 57 项 Python unittest 通过，覆盖命令行、提示词误判、镜头准备、离线矩阵和安装分发 |
| 技能与文档 | 技能格式、JSON、Markdown 相对文件链接及 git diff --check 通过 |

WorkBuddy 用户目录下已有旧版技能，本轮保留原样。隔离目录验证通过不等于新版已在用户客户端启用，也不代表已发布到技能市场。

## 完整示例的交付范围

[《关门前的来信》](../examples/last-letter/README.md)包含原创故事、项目档案、6 张资产卡、完整剧本、10 镜分镜、镜头 JSON，以及 10 份首帧与 10 份视频提示词。

准备器会复制独立工作副本，输出 20 份准备报告、review.json 和 production-status.json。总时长 60 秒；素材路径待补，真实生成状态为 not_run，视觉评分、平台任务 ID、费用均留空。示例设计仅用于演示，没有代替用户的创作批准。

## 重跑命令

从源码根目录运行：

```bash
python -X utf8 -m unittest discover -s tests -v
python scripts/verify_installations.py --discover-codex
python scripts/build_bundle.py
python scripts/prepare_example.py --out demo-output
```

verify_installations.py 输出 dist/install-check.json；不带 --discover-codex 时只执行目录与工具验证。没有本地 Codex CLI 时，该项发现检查保留 not_run。示例输出需要使用新的空目录。

安装包为 dist/manju-director.zip，内含逐文件 SHA-256 清单。没有视频 API key 或已连接的视频生成服务，本轮没有生成图片或视频，不能据此认定画质、连续性或跨模型成功率已经提高。
