# Claude Code 使用指南

## 安装

```bash
python scripts/manage_skill.py install --host claude
python scripts/manage_skill.py check --host claude
```

默认目录 ~/.claude/skills/manju-director。项目级安装用 --scope project --root 指定创作项目。
打开项目后，从命令菜单确认技能，再显式调用 /manju-director。

## 第一次创作

```text
/manju-director
为下面故事设计一段 60 秒二维漫剧，16:9。
先完成剧本、资产设计、分镜与逐镜提示词。保留角色、道具和视线的连续性记录。
目标平台：填写实际视频模型及版本。视频生成由我在平台执行。
故事：……
```

让助手把文件写到创作项目，调用安装目录内的 Python 工具；不要假设当前项目恰好有 scripts/。

## 验证范围

本机有 Claude Code 2.1.281。已对其目录布局进行隔离安装和包内脚本验证；本轮没有启动另一个语言模型会话，技能菜单发现和完整创作调用仍待宿主内验收。
如果看不到技能，核对安装目录、会话所在项目、技能启用和组织策略；不要只凭文件复制就认定实际调用通过。

官方说明：[Extend Claude with skills](https://code.claude.com/docs/en/skills)。
