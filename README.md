# Master-director / 漫剧导演工作流

把原文或主题转为可编辑的剧本、资产卡、分镜、图像与视频模型输入，以及连续性和成片评估记录。

本轮重构采用“共同的镜头设计 + 按任务与模型版本组织输入”。支持为 Seedance、MiniMax/海螺、Google Gemini Omni 和可灵准备输入；具体能力取决于版本与入口。当前已完成本地验证，真实视频效果仍待样片验证。

## 从这里开始

**输入一段故事 → 得到剧本、资产卡、分镜和逐镜提示词 → 到视频平台生成 → 带回结果迭代。**

选择你的 AI 助手，在本项目目录运行一条安装命令：

| 宿主 | 用户级安装命令 | 使用说明 |
|---|---|---|
| Codex | `python scripts/manage_skill.py install --host codex` | [Codex](docs/CODEX.md) |
| Claude Code | `python scripts/manage_skill.py install --host claude` | [Claude Code](docs/CLAUDE_CODE.md) |
| WorkBuddy | `python scripts/manage_skill.py install --host workbuddy`，或导入 ZIP | [WorkBuddy](docs/WORKBUDDY.md) |

安装器会保留同名旧安装，避免覆盖已有修改。[安装/更新/卸载](docs/INSTALL.md) · [支持状态与实测范围](docs/SUPPORT.md)

**先看一个完整例子：**[《关门前的来信》](examples/last-letter/README.md)，60 秒、10 镜，含源故事、6 张资产卡、分镜和 20 份模型输入文本。

```bash
python scripts/prepare_example.py --out demo-output
```

这个命令复制并编译内置示例，不需要模型 key。它会保留待制作状态，图片和视频由你在实际平台生成。

需要上传技能包时运行 `python scripts/build_bundle.py`，得到 dist/manju-director.zip。

## 工作方式

1. 先确定每镜的信息变化、可见证据和注意力落点。
2. 设计人物位置、视线、道具接触、起始与结束状态。
3. 选择文生、首帧图生、首尾帧、多模态参考、编辑或延长任务。
4. 按对应版本检查输入并组织提示词。
5. 生成后观察真实结果，记录失败证据，针对一个因素修改和比较。

人物与场景档案保存完整设定。给模型的输入只包含当前任务需要的内容。
画风、光影、景深、语言和负面约束按目标选择；不统一强制英文、浅景深、三处复写或固定提示词长度。

## 文件入口

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | 技能入口、制作阶段与逐镜循环 |
| [references/agent-loop.md](references/agent-loop.md) | 维护与优化循环 |
| [references/image-prompt-engine.md](references/image-prompt-engine.md) | 资产、首帧、末帧和图像编辑 |
| [references/video-prompt-framework.md](references/video-prompt-framework.md) | 按生成任务组织视频输入 |
| [references/model-adapters/README.md](references/model-adapters/README.md) | 模型版本与入口选择 |
| [references/model-adapters/profiles.json](references/model-adapters/profiles.json) | 有来源和核对日期的能力配置 |
| [assets/shot-spec-template.json](assets/shot-spec-template.json) | 可编辑镜头说明 |
| [references/shot-spec.md](references/shot-spec.md) | 字段、素材绑定和声明状态承接 |
| [references/evaluation.md](references/evaluation.md) | 真实样片评估与采纳标准 |
| [benchmarks/README.md](benchmarks/README.md) | 六类镜头和离线对照 |
| [docs/INSTALL.md](docs/INSTALL.md) | 三个平台安装、更新、卸载和打包 |
| [examples/last-letter/README.md](examples/last-letter/README.md) | 60 秒完整生产准备示例 |

assets/ 还提供项目档案、角色、场景、道具、复合参考和对话关系板模板。
references/genres/ 提供题材参考；按项目画风筛选视觉建议。

## 本地运行

Python 3.8+，工具只用标准库，无需 pip 依赖。UTF-8 命令行输出兼容 Windows 管道。
本项目不启动 Web 服务，也没有内置模型 API 客户端。

~~~bash
# 为缺少实际素材的镜头准备可审阅草稿
python scripts/prepare_shot.py assets/shot-spec-template.json --profile seedance-2.0-ark --draft --out benchmarks/results/example.json

# 素材和能力核实后，去掉 --draft 执行严格输入检查
python scripts/prepare_shot.py shot.json --profile seedance-2.0-ark --out prepared.json

# 按任务检查提示词文本；--strict 额外将提示性 warning 计为失败
python scripts/check_prompt.py --file prompt.txt --task image_to_video

# 查看候选失败原因
python scripts/diagnose.py "人物变脸"

# 执行离线镜头矩阵与回归
python scripts/run_benchmark.py
python -X utf8 -m unittest discover -s tests -v
~~~

模型配置中的 true/false 只适用于列明版本；null/缺项表示未核实。
草稿不会被标记为可提交。严格准备通过也仍需核验媒体格式、实际上传、平台权限及具体请求参数。
输出始终区分本地检查、真实生成和视觉验收。离线报告不会填写虚构视频评分或成本。

## 模型覆盖与限制

- Seedance：已按 Ark 2.0 资料配置；其他版本/即梦入口需要独立核对。
- MiniMax/海螺：2.3 和 02 分开，检查时长与分辨率组合及首尾帧差异。
- Google Omni：单独的 Gemini Omni 1.1 Flash 配置，不借用 Veo 参数；部分数值限制待核对。
- 可灵：保留版本配置入口；本轮官方文档访问受限，未臆造跨版本能力。
- 当前没有视频 API key，未执行真实视频生成；六类镜头素材槽位和样片记录待补齐。

## 尾帧工具

需要 ffmpeg 与 ffprobe 加入 PATH，或设置 FFMPEG_BIN / FFPROBE_BIN：

~~~bash
python scripts/extract_last_frame.py input.mp4 -o frames --shot 1
~~~

衔接方式由剪辑目的和模型能力共同决定。视频延长、首尾帧、尾帧输入与新镜头切换没有统一优先级。

## 使用与维护

本目录是技能源码。可按目标宿主的技能目录约定安装；名称为 manju-director。
创作过程沿用用户已确认的资产与决策；仓库维护和离线实验不触发新剧集制作确认门。

同步远程前检查本地修改，工作区干净时再切换主分支：

~~~bash
git status
git switch main
git fetch origin
git pull --ff-only
~~~

## 协议

[MIT License](LICENSE) © 2026 liangie7420
