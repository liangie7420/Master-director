# Episode Bible (Project Archive) — <Drama Title / 片名>

> One file per drama; fill in during Phase 2, then FREEZE. (R5: every downstream deliverable references this archive — editing it after freezing forces a full redo of everything downstream.)

## 1. Global Parameters / 全局参数
- **Genre / 题材**: <sci-fi / xianxia / urban / romance / campus>（对应 `references/genres/<题材>.md`）
- **Target Model / 目标模型**: <Seedance / Kling / Hailuo>（对应 `references/model-adapters/<模型>.md`）
- **Aspect Ratio / 画幅**: <9:16 / 16:9> | **Episode Length / 单集时长**: <60–90s> | **Total Episodes / 总集数**: <N>

## 2. Tone & Visual-Style Anchor Block / 基调与画风锚点块
- **One-sentence tone / 基调一句话**: <e.g. "oppressive, cold near-future mystery" — locked for the entire show>
- **Visual-style anchor block**（4–6 pairs, reused VERBATIM as the opening line of every first-frame image / video prompt）:
  `<e.g. cel-animation texture, fine cel shading, film-grade grain, cinematic lighting, wide composition>`
- **DP / reference look / DP·参考影调**: <e.g. "Roger Deakins-style low-key realistic light" — must be self-consistent with the film stock and aspect ratio>
- **Deletion-word regulator / 删词调节器**（lighting-styles §四）: for a clean / bright tone DELETE `Dune / skip-bleach / analog grain / dusty haze`; for an oppressive tone keep the full set.
- **Cinematic signature block, 5-piece set / 电影感签名块五件套**（image-prompt-engine §四）: composition school + hex palette + DP credit + film stock + anti-AI-flavor seal — must be self-consistent.

## 3. Color Rules（locked for the whole show — no drifting）/ 配色铁律

### 3.1 Dual-Axis Differentiation（color + form）/ 双区分轴

| Object / 对象 | Color (HEX) | Form / Texture | One-Sentence Rule / 一句话铁律 |
|---|---|---|---|
| <Character A's power / faction> | <#______> | <particles / crystals / flowing light / gaseous / solid> | <e.g. "A's spiritual energy is always green-white flowing light — red is banned"> |
| <Character B> | <#______> | <> | <> |
| Main scene tone | <#______ primary + #______ secondary> | — | <> |

> **Dual-axis differentiation / 双区分轴**: Axis 1 pulls hue / saturation apart; Axis 2 pulls form / texture apart（"soft flowing particles vs hard sharp crystals"）. Even inside the same color family, the two forms must be distinguishable at a glance.
> **Three-location rewrite requirement / 三处复写要求**: every color / form rule must be stated in all THREE places — the VFX layer（positive）+ the LOCK / constraint（prohibition）+ the final AVOID line（negative）. Missing any one spot and it will likely drift.
> **Permanent negatives / 负向常驻**: <wrong color 1>, <wrong color 2>, <A must not collide with B's color>.

### 3.2 Color Intensity — 6 Levels（pick as needed）/ 配色强度 6 级

| Level / 级别 | Approach / 做法 | Best For / 适用 |
|---|---|---|
| L1 per-element hex | Embed directly in the description: `cinnabar red #A82A2A talisman strips` | Local key objects |
| L2 full color bible（13–22 colors） | List a named palette BEFORE the TONE line | Whole-project uniformity |
| L3 60-30-10 hero-color rule + countable constraint | `10% accent color appearing at EXACTLY 4 named spots — no more than 4 accent points anywhere` | Multi-color clash scenes |
| L4 Mondrian counting method | Balance color blocks by QUANTITY among same-size objects（a larger block = a cluster of 5-6 identical items） | Group shots / crowds |
| L5 sweet spot of 13–22 colors | Too few（<8）can't pin the look; too many（>25）the model forgets | Complex color design |
| L6 B&W shots still get a color card + grayscale hierarchy | `render as black-and-white but preserve tonal hierarchy (red→mid-dark gray, black stays deep, white stays bright)` | B&W action scenes |

> Place the palette strip BEFORE the TONE / development chain（fix color first, then film texture）.

## 4. Asset Registry（each ID = the frozen ID）/ 资产清单
| ID / 编号 | Type / 类型 | Name / 名称 | Card File / 卡片文件 | Look / Establishing Ref / 定妆·定场图 | Status / 状态 |
|---|---|---|---|---|---|
| CH-01 | Character / 角色 | <> | character-card copy | <image path/ID> | <⏳ / ✅ frozen> |
| SC-01 | Scene / 场景 | <> | scene-card copy | <> | <> |
| PR-01 | Prop / 道具 | <> | prop-card copy | <> | <> |
| SA-01 | Composite asset / 复合资产 | <> | scene-actor-card copy（character+scene+prop+atmosphere） | <> | <> |
| DB-01 | Dialogue board / 对话关系板 | <> | dialogue-board-card copy（6-cell 2×3 locked axis） | <> | <> |

## 5. Character Relationships（drive posture & blocking — lock them down）/ 角色关系
- <Who is stronger / weaker, who chases whom, who looks down on whom>. **The strong stay calm, move little, and even have zero VFX; the weak move a lot and carry all the VFX** — kept consistent across the whole show（shot-language: relationships drive posture）.
- Multi-character frames: translate each "relationship" into concrete blocking and write it down（who sits / lies / leans / stands, who is higher or lower, who looks down or up, whose gaze is locked on whose face）. If you omit the posture, the model defaults to everyone standing at equal height.

## 6. Shared Negative Library（must appear in every prompt）/ 通用负向库
```
<terms taken from the genre-pitfall chapter, bilingual>, text, watermark, logo,
extra people, extra fingers, deformed faces, costume drift, flickering light,
<genre-specific negatives>
```

## 7. Shot Progress Ledger / 分镜进度台账
| Episode / 集 | Shot / 镜 | Content / 内容 | Transition / 衔接 | Status |
|---|---|---|---|---|
| E1 | S01 | <> | jump cut / tail-frame / keyframe | ⏳ |
