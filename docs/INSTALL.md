# 安装、更新与卸载

源码与安装包都是完整技能目录：SKILL.md、参考手册、模板、Python 工具和示例一起安装。
Python 3.8+ 即可运行本项目工具；视频生成仍通过你使用的平台完成。

## 从当前源码安装

在仓库根目录执行下列命令之一，默认安装到当前用户目录：

```bash
python scripts/manage_skill.py install --host codex
python scripts/manage_skill.py install --host claude
python scripts/manage_skill.py install --host workbuddy
```

| 参数 | 默认目标目录 |
|---|---|
| codex | ~/.agents/skills/manju-director |
| claude | ~/.claude/skills/manju-director |
| workbuddy | ~/.workbuddy/skills/manju-director |

这里的 ~ 指当前系统用户目录。WorkBuddy 也提供官方的“添加技能 → 上传技能”入口，见 [WorkBuddy 指南](WORKBUDDY.md)。

项目级安装需要明确指定创作项目，避免装进错误工作区：

```bash
python scripts/manage_skill.py install --host codex --scope project --root "D:/my-drama"
python scripts/manage_skill.py install --host claude --scope project --root "D:/my-drama"
```

--root 在用户级表示用户目录，在项目级表示创作项目目录。WorkBuddy 的项目级布局也可生成供环境验证，但本轮只确认本机用户级现有目录及官方 ZIP 导入入口，未将项目级自动发现标为通过。

## 已有安装

安装器默认拒绝覆盖同名目录。只有带本工具清单、且受管文件未被修改的安装才可更新：

```bash
python scripts/manage_skill.py check --host codex
python scripts/manage_skill.py update --host codex
python scripts/manage_skill.py uninstall --host codex
```

其他宿主替换 --host 即可。项目级操作继续使用相同的 --scope project --root 参数。

未受本工具管理的旧安装会保留原样。迁移旧版本时，先把旧目录复制到技能发现目录以外留存，再通过宿主导入新包或选择新的项目级安装；不要把备份仍放在 skills/ 下形成同名技能。

更新和卸载会先核对清单与文件哈希，拒绝覆盖本地编辑。额外创作文件保留，不递归删除整个用户目录。

## 打包

```bash
python scripts/build_bundle.py
```

生成 dist/manju-director.zip，只有一个顶层 manju-director/，内含 bundle-manifest.json。
包不包含 Git、临时规划、运行缓存、生成结果或账户配置。相同源码重复构建得到相同 ZIP 内容。

解压后可从 manju-director/ 运行同样的本地安装命令。现有 ZIP 不代表已在任何技能市场发布。

## 首次运行

安装后从宿主的新会话中调用 manju-director。传入故事、画风、时长与目标视频平台。
宿主需要从实际技能目录运行工具；创作产物写到你的项目目录，不写回安装目录。
需要立即看产物时，可先运行 [固定示例](../examples/last-letter/README.md)。
