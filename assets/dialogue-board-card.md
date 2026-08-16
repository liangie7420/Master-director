# Dialogue Board Card — <Scene Name / 场景名>（编号 DB-##）

> A 6-cell 2×3 contact sheet that **locks a dialogue scene's 180° axis + true gaze sources**. It is the "blocking source of truth" produced BEFORE the shot list — one image that pins down "A is always screen-left facing right, B is always screen-right facing left, the camera never crosses the axis".
>
> **When to use**: any ≥2-person dialogue scene must produce this image before writing the shot list（blocks axis crossing, prevents gaze drift, prevents third-party intrusions）.
>
> **Source**: adapted from neoimage-prompt-engine "Figure 31 · over-the-shoulder two-person dialogue relationship board".

## 1. Figure Type & Layout / 图型与版式
- **Aspect ratio / 比例**: 6:5（fits 2 columns × 3 rows）
- **Layout / 布局**: **2 columns × 3 rows**（the left column always holds A, the right column always holds B — splitting pairs as 3×2 is forbidden）
- **Cell numbering / 格子编号**: 1–6, left to right, top to bottom; bold white in the bottom-right corner
- **Cell dividers / 格间分隔**: thin white or thin black borders, 1–2px
- **Third person / 第三人**: only as a background shadow; removed from close-ups（3/4 frames）

## 2. 180° Axis Lock（highest priority — applies to all 6 cells）/ 180° 轴线锁
- A is always on **screen-LEFT**, gaze always toward **RIGHT**
- B is always on **screen-RIGHT**, gaze always toward **LEFT**
- The camera **NEVER crosses the A–B line**
- **Declare this at the start of the prompt body + restate it in CONSTRAINTS**（double rewrite = attention reinforcement）. **If you skip it, the 6 cells' gazes go their own ways and the axis will not connect.**

## 3. Six-Cell Allocation（per neoimage Figure 31 template）/ 6 格分配
| Cell / 格号 | Position / 位置 | Camera / 机位 | A's Behavior / A 行为 | B's Behavior / B 行为 | Foreground Bokeh / 前景虚化 |
|---|---|---|---|---|---|
| 1 | row1-left | over-shoulder medium, favoring A | A speaks, gaze right | — | B's shoulder at right foreground |
| 2 | row1-right | reverse, favoring B | — | B speaks, gaze left | A's shoulder at left foreground |
| 3 | row2-left | A single close-up | face fills frame, gaze right, speaking micro-expressions | — | none |
| 4 | row2-right | B single close-up | — | face fills frame, gaze left, speaking micro-expressions | none |
| 5 | row3-left | A medium close-up | A stays left, gaze right | — | B blurred at right edge |
| 6 | row3-right | B medium close-up | — | B stays right, gaze left | A blurred at left edge |

**If any position is wrong, the axis collapses.** Check cell by cell: which shoulder owns the foreground bokeh + which way each gaze points.

## 4. Global Consistency（nine cells = ONE moment）/ 全局一致性
- Same room + same key light + same costumes + same moment
- Skip this sentence → the 6 cells drift into 6 different moments / 6 different lights
- Light direction + film stock + tonal signature consistent across all 6 cells

## 5. Anti-Face-Swap Trio（the biggest risk in multi-character frames）/ 防串脸三件套
1. **Per-image character reference exclusivity + bind to screen position**:
   `Image 1 corresponds to A's face in the LEFT column / Image 2 corresponds to B's face in the RIGHT column`
2. **CONSTRAINTS lock**: write `the two must not swap or merge faces`
3. **AVOID final line**: write `faces swapped or merged / heads merged`
4. After generation, verify identity cell by cell; if faces swapped, strengthen the position binding or use dot-marker positioning.

## 6. Prompt Structure（per the image-prompt-engine §三 formula）/ 提示词结构
```
[REFERENCE IMAGES]
- Image 1 (A look image): locks ONLY A's face / hair / costume
- Image 2 (B look image): locks ONLY B's face / hair / costume
- Image 3 (scene anchor): locks ONLY the environment and light

[180° AXIS — highest priority, applies to all 6 cells]
A always on screen-LEFT, gaze always RIGHT; B always on screen-RIGHT, gaze always LEFT;
the camera never crosses the A–B line.
<A's one-line posture>; <B's one-line posture>; <third person: hidden in B's background shadow>.
Same room, same key light, same costumes, same moment.

[6 CELLS · 2 COLUMNS × 3 ROWS · LEFT-A RIGHT-B]
Cell 1 (row1-left) over-shoulder medium favoring A: A's face and upper body on the left, looking past B's blurred right-foreground shoulder;
A speaks, gaze right.
Cell 2 (row1-right) reverse over-shoulder medium favoring B: B's face and upper body on the right, looking past A's blurred left-foreground shoulder;
B speaks, gaze left; the third-person shadow behind.
Cell 3 (row2-left) A single close-up, face fills frame, gaze right, speaking micro-expressions.
Cell 4 (row2-right) B single close-up, face fills frame, gaze left, speaking micro-expressions.
Cell 5 (row3-left) A medium close-up, B as a blurred right-edge foreground; A stays left, gaze right.
Cell 6 (row3-right) B medium close-up, A as a blurred left-edge foreground; B stays right, gaze left.

[PRESERVE] A (Image 1) and B (Image 2): faces & costumes fully identical across all 6 cells — no face-swapping or merging;
scene (Image 3) and key light consistent across cells = one moment, six cameras.

[CONSTRAINTS — restate the axis]
- Every cell: A left · facing right, B right · facing left, camera never crosses the axis, gazes connect across cells
- Third person only as a background shadow, removed from close-ups（3/4 frames）
- Exactly two speaking characters
- The only text in the entire image is the bold white cell number 1–6 in the bottom-right corner — no subtitles / watermark / logo
- Each cell separated by thin white borders

[PHOTOGRAPHIC TONE]
Real cinematic still, <tone one-liner: warm candlelight / cold blue / daylight>, 35mm film feel,
fine grain, soft depth of field, eye-level cameras across cells 3–6, restrained — neither oversaturated nor plastic.

[AVOID]
Crossing the 180° axis, gaze flips（A looking left or B looking right）, faces swapped or merged,
inconsistent costume / light across cells, oversharpening, HDR, skin-smoothing, cartoon, CGI game look, anime,
any text other than the cell numbers 1–6.
```

## 7. Verification Checklist（check item by item after generation）/ 校验清单
- [ ] Genuinely 6 cells in 2×3, thin white borders, bold white 1–6 bottom-right
- [ ] Axis not crossed（in all 6 cells A stays left looking right, B stays right looking left）
- [ ] Gazes connect（cells 1/2 over-shoulder gazes face each other; cells 3/4 close-up directions are opposite）
- [ ] Over-shoulder shoulder ownership correct（cell 1 foreground = B's shoulder on the right; cell 2 foreground = A's shoulder on the left）
- [ ] Faces consistent across the 6 cells, no swapping（face-swap is the max-risk failure）, costumes / light consistent across cells
- [ ] Cells 5/6: blurred foreground is the counterpart, not stealing focus; positions correct
- [ ] Third person only in the background shadow, absent from close-ups
- [ ] Zero text / watermark besides the cell numbers 1–6
- [ ] Long-distance dialogue frames already use the gaze-lock trio（shot-language §六）

## 8. Relationship to the Shot List / 与分镜表的关系
**Produce this image FIRST** before designing the dialogue scene's shot list. After the 6-cell camera positions are frozen, each shot in the shot list maps to its corresponding cell — guaranteeing that gaze / stance / axis stay consistent across the 6 shots.

If a dialogue scene needs more than 6 shots, **re-examine the axis issue** — for long dialogues, prefer splitting into "two dialogue segments" with a board each, rather than forcing more than 6 shots into one board.
