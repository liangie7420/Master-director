# Composite Asset Card — <Scene + Character + Prop + Atmosphere / 场景+角色+道具+氛围>（编号 SA-##）

> One image carries FOUR kinds of information at once: **character + scene + prop + atmosphere**. The most efficient mode for keyframe inserts — a far higher reuse rate than separate character / scene / prop cards, because every downstream shot can share the same single image.
>
> **When to use**: a new character's first appearance in a new scene（especially xianxia / urban / campus genres）, when the character and the scene are strongly tied（cultivation site / workstation / residence / classroom）.
>
> Companion cards: single character across multiple scenes → `character-card.md`; pure empty scene → `scene-card.md`; key props → `prop-card.md`.

## 1. One-Image Mandate（per image-prompt-engine §二 — "one image, one duty"）/ 一图职责

The composite asset image takes on the following FOUR duties — declare each one exclusively:

- **Character identity / 角色身份**: face / hair / outfit（replaces the single-character look image）
- **Environment structure / 环境结构**: the "skeleton" of the interior / exterior（replaces the scene establishing image）
- **Core prop / 核心道具**: the key props visible in the scene（replaces the prop establishing frame）
- **Atmosphere & light / 氛围光影**: light direction / palette / film texture（replaces the TONE paragraph）

**Dimensions this image does NOT manage**（must be declared as exclusive）:
- No specific camera position or composition（each shot's camera is decided in the shot list）
- No specific action（each shot's action is decided in the shot list）
- No specific dialogue（dialogue is decided by the script）

## 2. Image Specs / 画面规格
- **Aspect ratio / 画幅**: matches the project's main ratio（9:16 / 16:9）
- **Composition / 构图**: subject centered or rule-of-thirds, keep a 10% safe-margin around the frame edge
- **Shot size / 景别**: full body or medium shot（NEVER close-up — a close-up loses the scene information）
- **Camera angle / 机位**: eye level or a slight low angle（avoid high angle — it destroys body proportions）
- **Focal feel / 焦段感**: 50mm（standard — no wide-angle distortion）

## 3. Appearance Anchor（one image locks 4 dimensions）/ 外观锚点
| Dimension / 维度 | One-Sentence Anchor / 一句话锚点 |
|---|---|
| Character / 角色 | <face shape / features / hairstyle / outfit / accessories — verbatim reuse of the character-card's "Appearance Anchor" section> |
| Scene / 场景 | <one-sentence spatial structure + set-dressing — verbatim reuse of the scene-card's "Environment Anchor" section> |
| Prop / 道具 | <key props visible in the scene: form fatality + color HEX> |
| Atmosphere / 氛围 | <light direction + color temperature + palette + 5-piece cinematic signature block> |

## 4. Prompt Structure（per the image-prompt-engine §三 formula）/ 提示词结构
```
[REFERENCE IMAGES]
(none — this image IS the final product)

[PROMPT BODY]
<character appearance anchor, verbatim>, <subject pose: one hand holding X, the other at Y, looking forward / slightly off-camera>;
<scene spatial structure + set-dressing anchor>, <core-prop form lock + color HEX>;
<atmosphere & light, 4-piece set: light from X direction + half-face light + highlight point + wide-aperture bokeh>;
<5-piece cinematic signature block: composition school + palette + DP + film stock + anti-AI seal>;
<three-location rewrites placed LAST>.

[CONSTRAINTS]
- Character identity exactly matches the character-card anchors
- Scene structure exactly matches the scene-card anchors
- Prop form exactly matches the prop-card anchors
- Single visual anchor (the character itself)

[AVOID]
Unassigned dimensions (e.g. specific camera, action, dialogue) all excluded;
genre-level negatives + shared anti-AI flavor（loaded from image-prompt-engine §十四）.
```

## 5. Practical Use / 实战用法
The composite asset image serves as the **input first frame** for:
- The shot where a new character first appears in a new scene（keyframe insert · new character）
- A "visual continuity baseline" reused across many shots / episodes of the same scene（replaces the two-input combo of single-character look + scene establishing image）
- The "visual anchor" when a story-critical prop debuts（replaces the standalone prop establishing frame）

## 6. Relationship to the Separate Cards / 与分离卡片的关系
| Situation / 场景 | Recommended Card / 推荐卡 |
|---|---|
| Character appears in 3+ scenes（e.g. protagonist / the show's POV） | character-card.md（multiple lighting versions） |
| Character appears in only ONE scene | **this card（SA）** |
| Scene with no named character（pure empty shot） | scene-card.md |
| Key prop needs a standalone close-up | prop-card.md |
| Multi-character dialogue in one frame | character-card + dialogue-board-card.md |

## 7. Worked Example（illustrates usage — not a deliverable）/ 一实战示例
> Example: xianxia drama《丹引》episode 1, the warm inner chamber; 虞晚 appears for the first time — 虞晚（red robe, gold ornaments half-removed）leans on a brocade couch, the blood elixir pearl on the couch glowing red in the candlelight, the carved-open screen behind her, moonlight entering through the window. This ONE image replaces the merged version of "虞晚 look image + 暖阁 establishing image + 血丹 establishing frame" — three images compressed into one.
>
> The image is introduced in Phase 4: shot 1 opening（keyframe insert · new character）+ shot 3 the game begins（keyframe insert · new prop — the pearl's first close-up, the elixir in 虞晚's hand）can both reuse this image as their first frame.

## 8. Cross-Check with references/threading / 与 references/threading 校验
At gate 2 (过闸2), on top of the per-character / per-scene / per-prop checks, add one more item:
- [ ] After the composite image passes the gate, every prompt's "character + scene + prop" segments must ALL reuse this image's anchors verbatim — no drifting from link to link along the chain.
