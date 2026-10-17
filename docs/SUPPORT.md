# 平台支持与验证状态

核对日期：2026-10-17。文件结构兼容、安装通过、宿主发现和完整创作是不同层次。

| 平台 | 安装入口 | 隔离安装/检查/更新/卸载 | 包内工具跨目录运行 | 宿主发现/调用 |
|---|---|---|---|---|
| Codex 0.154.0 | 用户/项目级 .agents/skills | 已验证 | 已验证 | 已在本地启动上下文发现安装技能；完整创作验收待完成 |
| Claude Code 2.1.281 | 用户/项目级 .claude/skills | 已验证 | 已验证 | 菜单发现与创作调用待验证 |
| WorkBuddy | ZIP 上传；本机用户级 .workbuddy/skills | 已验证目录布局 | 已验证 | 当前存在旧版；新版导入/启用待验证 |
| Cursor | 支持 Agent Skills 的目录 | 尚未列为实测入口 | 未实测 | 待验证 |

“隔离安装”指完整包安装到临时用户/项目目录，执行校验和工具后再更新、卸载；没有改动用户原有宿主配置或旧技能。

## 本轮提供的交付

- 通用 ZIP 和哈希清单。
- 三个宿主的安装与首次调用说明。
- 60 秒原创故事、资产卡、10 镜分镜、20 份提示词与可运行的固定示例准备器。
- 保留用户编辑、拒绝覆盖旧安装与路径越界的回归测试。

## 视频模型层

这套工作流准备 Seedance、MiniMax/海螺、Google Gemini Omni 和可灵的输入；模型参数以各版本配置为准。
当前没有视频 API key 或已连接的视频生成服务，所有真实样片仍为 not_run。
Omni 部分数值和可灵准确入口参数待核实，不能将本地编译通过描述为平台生成成功。

## 资料

- [Codex 官方技能目录](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code 官方技能说明](https://code.claude.com/docs/en/skills)
- [WorkBuddy 官方技能导入](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [Cursor 官方技能说明](https://cursor.com/docs/skills)

实际命令与结果见 [安装验证记录](INSTALL_VALIDATION.md)。
