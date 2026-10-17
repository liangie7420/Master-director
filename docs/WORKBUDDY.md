# WorkBuddy 使用指南

## 推荐入口：导入 ZIP

先构建安装包：

```bash
python scripts/build_bundle.py
```

在 WorkBuddy 左侧“专家·技能·连接器”进入技能页，选择“添加技能 → 上传技能”，选中 dist/manju-director.zip。
在“已安装”确认 manju-director 已启用；新会话中调用。

官方说明支持用户上传技能包：[技能](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。

## 本地目录安装

本机已经观察到 ~/.workbuddy/skills/manju-director 的旧安装。本项目安装器也支持该布局：

```bash
python scripts/manage_skill.py install --host workbuddy
```

若目录已存在，命令会停止并保留原目录；不会直接覆盖未受管的旧技能。本轮保持用户旧安装不变，新版包通过隔离目录验收。

## 第一次创作

```text
使用 manju-director 漫剧导演技能，把下面故事做成 60 秒二维漫剧的生产包。
先产出剧本、角色卡、场景卡、分镜和逐镜提示词。素材与视频还未生成时标记待制作。
目标视频平台和版本：……
故事：……
```

需要看固定产物时，请助手从实际技能目录运行 scripts/prepare_example.py，输出到你的创作目录。

## 验证范围

已确认本机 WorkBuddy 正在运行且存在旧版安装；新版的隔离安装、校验、卸载及包内 Python 工具经过验证。
本轮没有替换旧安装，没有在客户端上传 ZIP，也没有把新版自动加载或完整创作列为通过。
