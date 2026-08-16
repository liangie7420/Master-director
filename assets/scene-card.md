# Scene Card — <Scene Name / 场景名>（编号 SC-##）

> Fill in during Phase 2; FREEZE once the establishing image passes gate 2 (过闸2). The first paragraph of every prompt for shots in this scene must copy this card's "Light Source & Tone" sentence VERBATIM（prevents light jumps between shots）.

## 1. Environment Anchor（LOCKED — reuse verbatim）/ 环境锚点
- **Time & weather / 时间与天气**: <e.g. "midnight, sky clear right after a snowfall">
- **Spatial structure / 空间结构**: <foreground / midground / background contents, the depth axis, window & door positions>
- **Key light / 主光源**: <direction + quality, e.g. "cold white moonlight through the left window lattice — the only hard light">
- **Fill light / 辅助光**: <e.g. "warm orange candlelight reflecting off the floor, filling the jaw">
- **Dominant palette / 主色调**: <HEX primary + HEX secondary, consistent with the project bible's color rules>
- **Floor / material / 地面·材质**: <e.g. "dark crimson rug, low reflectance; the screen is frosted-silk">
- **Ambient-sound hint / 环境声暗示**: <e.g. "water-clock drips, distant wind" — feeds the video prompt's atmosphere>

## 2. Set-Dressing Checklist（cross-shot consistency check）/ 陈设清单
| Prop / 陈设 | Position / 位置 | Form Key Points / 形态要点 | Movable? / 是否可动 |
|---|---|---|---|
| <brocade couch> | <rear-left of frame> | <> | fixed |
| <> | <> | <> | <> |

## 3. Axis Archive（required for dialogue scenes）/ 轴线档案
- **Axis definition / 轴线定义**: <A placed left, B placed right; the camera is ALWAYS on the south side of the A–B axis line>
- **Master-shot（two-shot）composition / 主机位·双人过场构图**: <>
- **Over-the-shoulder cameras / 正反打机位**: <A over B's shoulder / B over A's shoulder — gaze directions: A looks screen-RIGHT, B looks screen-LEFT>

## 4. Form Fatality & Negatives / 形态命门与负向
- **Most easily misdrawn / 最易画错处**: <e.g. "window lattice has 6 panes; the candlestick has three legs"> → negative: <>

## 5. Establishing Image / 定场图
- Establishing image ref: <path/ID>（empty shot, no people）
- Time-of-day lighting: <golden hour / blue hour / harsh noon light / overcast diffusion — pick to match the tone>
- Establishing image prompt:
```
<visual-style anchor block>, empty establishing shot, <full environment anchor, verbatim>, no people,
<set-dressing key points>, <key-light sentence + time-of-day lighting>, <dominant palette HEX>.
Negative: <scene-fatality negatives> + <project shared negative library>（all negative words concentrated on the final line）
```
> Time-of-day lighting / lighting methods / architectural-perspective writing: see `references/lighting-styles.md`.
