# 首帧图提示词引擎（阶段 4 写首帧图提示词时必读，重构版 v2）

> 面向自然语言类图像模型（即梦/Nano Banana/GPT Image 等无独立负向字段的模型）。所有控制都写进文本本身。本文件与 `assets/character-card.md`、`assets/scene-card.md`、`assets/prop-card.md`、`assets/scene-actor-card.md`、`assets/dialogue-board-card.md` 模板配合使用。
>
> v2 在 v1 基础上吸收了"参考图排他声明、三处复写、签名块五件套、删词调节器、双寄存器、5 类过度复杂"等实战规律。

## 一、六条铁律

1. **分行**：每个语义模块独立一行。碎片化单行、长串堆叠都会降低模型控制精度。
2. **负面末行**：所有"不要/禁止/无"集中写在提示词**最后一行**；正向描述区**绝不出现**不想要的词（点名 = 召唤）。
3. **参考图代号**：正文里只用 `图1/图2` 或 `image1/image2` 指代，禁止出现文件名与路径。
4. **空间锚点具体化**：用方位（左/右/前景/后景）+ 层级（前/中/远景）+ 距离参照（"贴近画面右下角""距主体约一步"），禁止模糊的"旁边/附近"。**高度用构图关系，不用米数**（"脚下踩着、在画面下半部，离地约 10 米 + 保持平视/仰拍 + 绝不要鸟瞰"）。
5. **光影四件套**（角色帧必含）：① 光从哪来（具体方向） ② 半脸光（哪半亮哪半暗） ③ 高光点（具体位置，颧骨/鼻梁/唇/锁骨） ④ 大光圈虚化（背景虚化、wide aperture）。任何一帧角色镜头缺一个 = 平光 + 背景清晰 = 定妆照不是电影。
6. **一图一焦点**：一张首帧图只锁一个视觉焦点（人/道具/空间关系），多焦点稀释后全部糊掉。

## 二、一图一职 + 排他声明（防漂核心）

每张参考图必须**唯一职责 + 排他声明**。参考图不是"参考整图"，而是"参考某一维度"。

**反例**（必翻车）：
```
[图1] 角色定妆图 [图2] 场景图
```
模型会自己脑补两者各自管什么 → 串脸/漂色。

**正例**（唯一职责 + 排他=不归我管就不问我要）：
```
[图1] 角色定妆图 —— 仅作为角色身份锚（脸/发/服装），不提供场景/构图/光影
[图2] 场景定场图 —— 仅作为环境与色板锚（建筑/光/色调），不提供人物身份
[图3] 道具定场帧 —— 仅作为道具形态锚（结构/光泽/工艺），不提供场景与人物
```

**凡没分配的维度，模型一定自作主张**。排他声明就是给模型画"自治边界"。

## 三、结构公式（按序输出）

```
主体行（谁：外观锚点逐字复述 + 位置）
空间与构图行（景别/机位/站位/前景后景层次 + 高度用构图关系）
光影行（光影四件套：方向+半脸+高光点+大光圈；时段/布光法见 lighting-styles.md）
环境行（场景锚点逐字复述 + 陈设要点）
镜头行（焦段感 + 视角，如"85mm 感，平视微仰"）
画风行（电影感签名块五件套 + 风格锚点）
负面末行（不要……，不要……，不要……）
```

**三处复写铁律**：同一核心约束（角色形态命门 / 配色铁律 / 核心负面）要在「主体行或光影行（正向）+ 末尾【CONSTRAINTS】或锁定段（禁令）+ 负面末行（Avoid）」三处各说一遍。**适度重复 = 注意力强化**，只写一处 = 跑偏。

## 四、电影感签名块五件套（避免 AI 味）

按"摆→色→谁拍→拿啥拍→封口"五件套锁定摄影签名：

```
构图流派：电影感对角构图 / 居中对称 / 越肩轴线等
hex 色板：#xxx（主色）+ #xxx（辅色）+ #xxx（焦点色），锁死对应
DP 摄影师署名：Greig Fraser (Dune 2021) / Roger Deakins / Hoyte van Hoytema 等
胶片型号/画幅：35mm Kodak Vision3 500T / Kodak Double-X 5222 / 6K 大画幅
反 AI 味封口：the overall PHOTO is clean, NO digital grain; NOT CGI / anime / video-game render
```

五件套必须自洽：写 Deakins 冷峻就别叠高饱和 HDR；写 Fraiser 沙漠就别叠清新蓝天。**清爽调整套签名要按 §六 删负**。

**显影链配方（直接可抄）**：
```
// 彩色日/夜景（低饱和高对比、跳漂白苍茫硬调）
35mm Kodak Vision3 500T film stock with skip-bleach negative LUT,
analog photochemical grain, single still frame from a feature film.

// 黑白武戏（真实黑白片基灰阶）
Kodak Double-X 5222 black-and-white film stock aesthetic. Anamorphic widescreen lens.
Subtle organic film grain only. Colors restrained, slight gray tone.
```

**黑白片仍用彩色色卡 + 写灰阶层级**（防层次糊）："红→中深灰、黑保深、白保亮"。

## 五、参考图纪律（图生图部分）

### 改图模式（在已有图上修改）
- 首行声明：`严格基于提供的参考图（图1），`
- 只写改动，不重述原图；必须有 Keep 锚点：`保持图1中人物的五官、发型、服装完全不变，`（具体到特征）。
- 末行负向：`不要改动人物本身，不要多余人物，不要水印。`
- 适用：阶段 5 翻车处理中的"轻改不让底图漂"。

### 参考提取模式（取元素画新图）
- 首行声明：`仅提取参考图（图1）中的[具体元素]（点名到特征），并构建一张全新画面，`
- 明确两清单：从图1提取什么 / 全新构建什么（背景/构图/光影/风格）。
- 多图点名来源：`图1提供角色，图2提供场景风格，`
- **防整图搬运末行**：`不要照搬参考图原本的背景与构图。`
- 适用：阶段 2 角色定妆、阶段 5 视角切换时的"尾帧换机位"。

### 尾帧承接模式（本技能特有）
- 首帧 = 上镜尾帧时无需生成新图；若因视角切换需重建，按"参考提取模式"处理：尾帧为图1，提取人物姿态与服装，重建新机位下的画面，并写 `保持图1中人物的姿态、服装与光影方向，仅改变机位角度。`

## 六、删词调节器（清爽调 vs 压抑调）

调子是基调级决策，**先定再出图**。提示词不只是"加什么"，更是"删什么"。

**清爽明亮调**（蓝天/通透/都市）：
- **删**：`Dune aesthetic / skip-bleach LUT / analog grain / dusty haze / HDR glow`
- **加**：`bright clean fresh daylight + clear/soft light-blue sky + white clouds + high clarity + shallow DoF`
- 冷特效靠 teal-orange 互补（暖背景 vs 冷特效）；蓝天别过饱和（`not over-saturated`）。

**压抑/末世调**（沙尘/冷峻/废土）：
- **保留**：`Dune aesthetic + Kodak Vision3 500T + skip-bleach + analog grain + dusty haze + desaturated`
- 全套签名按本调走，不混用。

**坑**：skip-bleach 去饱和会一起吃掉焦点色，搭配时焦点色要 `sole saturated / glowing` 显式拔高。

## 七、双寄存器（重型建 vs 轻改）

| 任务 | 模型 | 提示词 |
|---|---|---|
| **重型建**（定妆图/定场图/关键帧从零生成） | 重型图像模型（Image 类） | 完整六段式提示词 |
| **轻改**（在底图上微调一处） | 视觉理解模型（Nano Pro 类） | 中文一句话 + "其余不变" |

**7 类轻改模板**（中文一句话，均配"其余不变"）：
```
镜头远近：  把镜头拉远一点，其余不变。
居中/构图：把人物挪到左三分之一，其余不变。
景别：     从全身改成半身特写，其余不变。
表情：     表情改成眯眼挑眉，其余不变。
材质改写： 把衣袖材质改成丝绸，结构不变，其余不变。
去元素：   去掉丝袜，改成光脚，其余不变。
换元素：   把背景换成沙漠（@基底 @风格），其余不变。
```

**两条规则**：
- 删元素必给替代状态（去丝袜→"光脚"，别只说"去掉"）。
- 改动必给物理因果（湿身→"衣袖紧贴皮肤"），否则模型把反常理细节"合理化"抹平。

**何时轻改 vs 重刷**：
- 只动 1 个变量、底图基本满意 → 轻改（一句话）
- 同时改 ≥3 件事 / 换姿态 / 换结构 / 换机位 / 连续轻改后开始熔脸串身份 → 停手，回重型完整重起

## 八、5 类过度复杂（写完逐项自检）

1. **术语堆叠 vs 朴素一句**：光影别写 `★1/3 warm DIRECTIONAL key light at ~45°...★2/3 chiaroscuro...`，写 `Warm light from camera-right. Right half lit, left half in warm shadow.`。
2. **"族"标签分组 Avoid vs 平铺**：别写 `★(锚点漂移族)★...`，直接平铺 6-12 条核心禁令，无标签。
3. **★★ 大块开头声明 vs 一行点题**：别在开头堆 4-6 行 `THIS IS X NOT Y`，压成一行。
4. **每张 ref 都长 disclaim vs 只对易漂处**：只对真正易漂的那张写长排他声明，其他简单一句。
5. **HEX 色板大全堆叠 vs 沿用色卡一句**：第一帧定色卡后，后续仅 `warm crimson-gold per established color bible`，别每帧抄一遍 HEX 全表。

**总字数目标**：复杂帧 ≤ 500 词；简单帧 ≤ 350 词。超了回头剪。

## 九、高风险特征必出 SOP（形态命门升级版）

**铁律**：如果某个特征翻车了整张图就废了（角色脸/形态命门/数量/颜色对垒），就必须走这套 SOP。

1. **前置标** `if missing the design fails`：在主体行或 CONSTRAINTS 段把关键形态特征前置。
2. **预想翻车**：预想它最可能翻成什么（手部→六指；法阵→气泡；魔兽→卡通）。
3. **写"失败模式 → 补救句"**：每个翻车点一条补救句。
4. **出图后逐项对账**：对照清单逐项核。
5. **没到位真重跑 + 追加补救句**：别凑合。

例（玄幻法阵）：
```
主体行：[图1] 法阵居中，[法阵纹路=八角放射，内环三圈、外环十二芒，禁止画成连续同心圆]
CONSTRAINTS：法阵纹路必须八角放射，禁连续同心圆；如有失败模式→追加补救句"外环必须十二芒，单数不可"
负面末行：do not deform the rune; do not use circles
```

## 十、对话戏高风险区：远距离视线锁定

远距离对话帧（隔屋对峙/跨桌）一旦超出"一臂之内"就掉控，模型会把两人画成各自低头沉思（看似在看其实没看）。
**加固三件套**：
1. 正向：`eyelines MEET across the room, both heads slightly LIFTED to look at each other`
2. Avoid 段把"低头沉思"族逐项排除：`looking down at the table / heads bowed / eyes lowered / each lost in their own thoughts / averted gaze`
3. 纯侧脸改 3/4 朝向对方；`head TURNED toward the other person, chin slightly LIFTED`

**作用范畴**：所有对话戏镜头，按【正文】+【CONSTRAINTS】+【Avoid】三处复写。

## 十一、迭代纪律（对应抽卡控制）

- **最小改动**：反馈只动相关行，其余逐字保留。无谓改动会让用户满意的部分一起跑掉。
- **先诊断再改**：先判"上一版哪一行没控住、漏了哪条规避"，优先强化正向锚点，不无脑堆负面词。
- **方向性否定要重做**：风格/构图/主体被整体推翻时，不回旧版小修，回阶段 2/3 重新构想。
- **假设透明**：用户需求过简时，内部补齐一套合理假设直接产出，输出后一行标注关键假设。

## 十二、 API 参数建议（附录）

```
【API 参数建议】
model: <gpt-image-2 / nano-banana-pro / 即梦>
[改图任务(在已有图上改光/改局部)注明：调用 images.edit，不是 generate]
size: 单帧 1K~2K；多格/多视图/群像站位图 1536 长边或 2K+
quality: medium（默认）；high 留最终交付
Thinking Mode: 复杂合成/多约束/多角色时开启
参考图：图1 = [职责]   图2 = [职责]   …
【提醒】改图 Preset list 核心；九宫格在 PRESERVE 开头加"preserve the multi-panel grid layout and the content of every panel"
```

- 改图（edit）vs 建图（generate）不分是"双寄存器翻车"根因。
- `output_format`：成片/物料一律 jpeg；透明底/无损叠层才 png。
- `size`：单帧 1K–2K；九宫格/多视图/群像站位必须 1536 长边或 2K+（否则每格细节糊）。

## 十三、 定妆/定场/道具/复合资产提示词（与 assets 模板联动）

- **角色定妆**（character-card.md / scene-actor-card.md）：add 眼神光 + 布光法（伦勃朗光 男/蝴蝶光 女 优先）+ 85mm 感 + 形态命门三处复写 + 排他声明。
- **场景定场**（scene-card.md）：add 时段光影（黄金时刻/蓝调时刻/阴天漫射 按基调选）+ 布光法按场景选 + 双区分轴色板。
- **道具定场**（prop-card.md）：add 产品布光（奢侈品单光+反光板精控 / 科技产品冰盒感黑背景 按题材选）+ 形态命门三处复写。
- **复合资产图**（scene-actor-card.md）：一图覆盖角色+场景+道具+氛围，最高效的关键帧插入方式。
- **对话关系板**（dialogue-board-card.md）：6 格 2×3 锁 180° 轴线，对话戏前置必出。

## 十四、 反 AI 味词库（Avoid 常驻）

⚠️ 不在正向描述里出现。用一段写完补充到末行。

```
overpolished studio look, plastic smoothing skin, oversaturation of non-red elements,
glossy highlight blowout, generic AI image quality, HDR glow, doll-like skin,
3D rendered look, cartoon / anime / video-game render, mosaic / pixelated artifacts,
text, watermark, logo, signature, multiple characters without intent,
unnamed facial features mixing into subject
```

**题材级负向**（每个题材的"翻车点"段已列），逐个点名（如科幻：`cyberpunk = blue-purple tint`；古装：`studio portrait look`）。
