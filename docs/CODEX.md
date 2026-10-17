# Codex 使用指南

## 安装

```bash
python scripts/manage_skill.py install --host codex
python scripts/manage_skill.py check --host codex
```

默认放到 ~/.agents/skills/manju-director。也可用 --scope project --root 指定项目级 .agents/skills。
在下一轮或新会话检查技能列表，显式使用 $manju-director 调用。

## 第一次创作

```text
使用 $manju-director，把下面故事做成 60 秒、16:9 的二维都市动画生产包。
先给剧本、角色与场景设计、分镜和逐镜模型输入；目标视频平台为我选择的版本。
我目前没有视频 API key，图片与视频没有生成前保持待制作状态。
故事：……
```

给出已有资产时说明文件位置。批准创作方向后再推进相应制作阶段；已有批准沿用。

## 无需模型 key 的本地示例

从源码根目录运行：

```bash
python scripts/prepare_example.py --out demo-output
```

从安装版本运行时，用实际技能目录下 scripts/prepare_example.py 的完整路径，并把 --out 指向创作目录。

## 验证范围

本机已验证 Codex 0.154.0 的本地源码工具运行。安装/校验/更新/卸载在隔离目录验证；宿主发现结果见 [支持状态](SUPPORT.md)。本轮不调用额外语言模型或视频模型来伪造端到端验收。

官方目录约定：[Build skills](https://learn.chatgpt.com/docs/build-skills)。
