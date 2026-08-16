# Shot-Language Quick Reference (use when designing shots in Phase 3 and writing prompts in Phase 4)

> Usage: the shot-scale/camera-move words in the script's shot-label line `[shot scale|camera move|frame key points]` MUST come from this table; the camera fields in prompts also use this table's vocabulary (vocabulary common to all three models; model-specific wording per model-adapters).

---

## 1. Shot-Scale Table (far to near)

| Shot Scale | Framing Range | Typical Use | Video-Model Risk |
|---|---|---|---|
| Extreme long shot | environment is the subject, people are dots | opening establishing, isolation, giant-object pressure | low; safe to use |
| Long shot | full body + lots of environment | blocking, positional relations, full view of fight scenes | low-mid; many people tend to blur |
| Full shot | full body, headroom above | action exposition, costume display | mid; watch the limbs |
| Medium shot | above knee/waist | dialogue workhorse, action + expression balance | mid |
| Medium close-up | above chest | dialogue + emotion, MOST used in comic drama | mid |
| Close shot | above shoulders | emotional-scene workhorse | mid-high; facial details need anchors |
| Close-up | face as subject | emotional explosion, reaction shots | high; facial features drift easily, needs character reference |
| Big close-up | eye/lip/hand/prop close-up | key props, micro-expressions, hook frames | high; hands are the top failure zone |

## 1.1 Shot-Scale Inference Table (from text features to shot scale — use when cutting the script in Phase 1)

> When splitting narrative text into shots, pick the shot scale by the DOMINANT text feature below — do not leave scale choice to subjective feel. After inferring, cross-check against the shot's narrative intent (emotion / information density); if they conflict, the intent wins.

| Text Feature (dominant in the beat) | Infer Shot Scale | Why |
|---|---|---|
| Environment / wide description ("远处" "一片" "俯瞰" "整条街") | Extreme long / Long | establishing, spatial pressure |
| Full-body entry / blocking ("走进" "站在" "坐下" "转身离去") | Full / Medium | position relations, movement |
| Two-person dialogue ("说" "问" "答道" "他开口") | Medium / Medium close-up | dialogue workhorse |
| Upper-body action + emotion ("抬手" "低头" "肩膀一沉") | Medium close-up | action + expression balance |
| Facial expression / eyes ("眼睛" "嘴角" "皱眉" "目光") | Close / Close-up | emotional beats |
| Body-part-level detail (R1: "指尖" "睫毛" "喉结" "呼吸节奏") | Close-up / Big close-up | the detail IS the subject |
| Key prop / screen / letter ("信纸" "怀表" "屏幕" "刀刃") | Big close-up | prop hooks |
| Mental activity ("心中" "意识到" "震惊") | Close-up (face reaction) | externalize as expression |
| Chase / action run ("追赶" "闪避" "冲出") | Full + track/follow | full body in motion |
| Anything else | Medium (default) | safest, never wrong |

**Cross-check rule**: a beat rich in R1 body-part details but with low emotional weight → medium close-up (not close-up); a beat with high emotional weight → close-up even if the text is short. Scale must serve intent, not just the words.

## 2. Camera-Move Table (safe words that video models respond to well in practice)

| Move | Wording | Fits | Risk & Notes |
|---|---|---|---|
| Static | `fixed camera` | everything, most stable | lowest; common in emotional scenes |
| Push in | `slow push-in / extremely slow push-in` | build-up, approaching truth, ambiguous rise | low; require "real perspective change, NOT 2D zoom" |
| Pull back | `slow pull-back / extremely slow pull-back` | reveal the whole, close out, loneliness | low |
| Track | `lateral track / track-with` | lateral relations, walking follow | mid; background parallax must be natural |
| Follow | `rear follow / side follow` | running, chasing | mid-high; subject tends to drift, pair with shallow DoF |
| Pan | `horizontal pan / vertical pan` | scanning environment, reaction relay | mid; small amplitude preferred |
| Crane | `slow crane-up / slow crane-down` | momentum, bird's-eye, ending elevation | mid |
| Orbit | `orbit (≤90°)` | highlight moments, two-person relations | high; ≤90° safe, 180°+ easily face-swaps/breaks |
| Handheld | `handheld micro-shake` | documentary feel, tension | mid; write "slight breath-like shake", forbid "violent shake" |
| Whip pan | `fast pan` | action-scene transitions | high; use sparingly, prefer jump cut |

**Speed modifiers** (safety high to low): `extremely slow` > `slow` > `uniform` > `moderately fast` > `fast` (high risk; do not use outside action scenes).

**Compound moves**: at most TWO camera moves stacked per shot (e.g., "slow push-in + slight crane-down"); three or more WILL fail. Default to a single move.

## 3. Focal Length & Depth-of-Field Psychology

> Full lighting-method and focal-style library in `references/lighting-styles.md`.

| Wording | Effect | Use |
|---|---|---|
| `wide-angle perspective` (24-35mm feel) | space stretch, exaggerated foreground | establishing, pressure, action |
| `standard perspective` (50mm feel) | near human eye | dialogue default |
| `medium 85mm feel` | good facial proportions, beautiful blur | portrait close-up, emotional scenes (portrait golden focal length) |
| `telephoto compression` (135mm+ feel) | background compression, subject isolation | emotional close-up, ambiguous scenes, tracking feel |
| `shallow DoF, blurred background` | sharp focus, creamy out-of-focus | character frames MUST have (prevents background bystander breakdown) |
| `deep DoF` | near and far both sharp | establishing, group shots (caution; many people WILL blur) |

**Focal-length discipline**: emotional scenes use 85/135mm feel; establishing and action use 24–35mm feel; dialogue uses 50mm feel. Always write "feel" (感), avoiding the model interpreting it as real lens parameters.

## 4. Camera Position & Angle

| Wording | Psychology |
|---|---|
| `eye level` | objective, equal (default) |
| `slight low angle` | character dominant, imposing |
| `steep low angle` | giant/strong-pressure (pair with extreme long shot or close-up) |
| `slight high angle` | vulnerable, examined, pity |
| `steep high angle / top view` | god's eye, blocking view, fate feel |
| `over-the-shoulder` | dialogue, with foreground shoulder |
| `Dutch angle` | imbalance, unease (one shot once, don't chain) |

## 5. Dialogue Axis Discipline (180° rule)

1. Two-person dialogue defines the axis first: the line connecting the two characters IS the axis; all camera positions sit on the same side of the axis; never switch sides within a scene.
2. Shot/reverse-shot coverage: master shot (two-person establishing) → A over B's shoulder → B over A's shoulder → each person's close-up/reaction. Eye-line directions MUST match: if A looks screen-right, B MUST look screen-left.
3. Scene change = re-define the axis; NEVER carry the previous scene's axis across.
4. Crossing the axis is only allowed through camera movement (orbit) or character blocking, and it must be shown on screen — no hard cuts.

## 6. Pacing Control

- Single shot 4–10 seconds; dialogue scenes average 6–8s/shot, emotional close-ups up to 10s; action 4–6s/shot.
- Editing rhythm = emotional curve: build-up phase has long shots, burst phase short shots, closing phase lengthens again.
- Shot scale within a scene must "breathe": far→medium→close→close-up climbs, then a long shot after close-up to breathe; forbid the same scale throughout.
- **Shot-scale jump-cut discipline**: forbid jumping directly from long shot to big close-up (no transition = viewer lost + model mixes information); far→near must pass through medium/close shot unless an intentional jump-cut impact (then give 1 establishing shot as buffer).
- **Opening frame / closing frame**: every camera-move shot states in the shot list "opening frame → closing frame" (what is in the frame when the move starts and ends). The closing frame is preferably an action-complete state (for last-frame extraction); the opening frame must be able to naturally grow from the previous shot's last frame.

### Single-shot four-beat rhythm (applied to video-prompt narrative section)

| Beat | Time Window | Task |
|---|---|---|
| Establish | 0–2s | continue from first frame, confirm scene & character position |
| Develop | 2–8s | primary action advances, micro-expression changes (preparation→process→landing) |
| Climax | 8–12s | emotional/line/visual-hook point (the ONE emphasized sentence) |
| Close | 12–15s | action lands and freezes, for last-frame extraction |

Short shots (4–6s) compress: Establish(0–1s) → Develop(1–4s) → Close(4–6s).

### Performance amplitude (style-adapted, animation storyboard method)

Comic-drama/animation-style performance may be moderately exaggerated (live-action feel stays restrained):
- Anime-style look: action amplitude 20–30% larger than live-action feel, expressions more distinct (wide eyes, enlarged mouth-curve); prompt writes "animated performance, exaggerated vivid expressions".
- Live-action/realistic look: performance restrained, emotion carried by micro-expressions and pauses (body-part-level detail); prompt writes "restrained performance, emotion carried by micro-expressions".
- Amplitude boundary: exaggeration ≠ cartoonish; limbs stay physical (no floating, no deformation); dialogue may pair with "performance breaths" (pauses/interruptions) to heighten drama.

### Height/position via compositional relationships (don't write meters)

Models can't anchor "flies 10 meters". **Translate "height" into spatial relationships**:
- rooftop/ground **beneath his feet**, pressed to the frame's **lower edge**, small and distant.
- leave a **large expanse of empty sky** between the feet and the rooftop (air gap).
- he is in the frame's **upper half, sky all around**.
- **low-angle upward shot** (looking up at him, sky behind) → reads as "high" without becoming a bird's-eye map.

"Higher" needs a comparable quantity + locked camera: `about 10+ meters above ground + keep eye-level/upward angle + NEVER bird's-eye`. "Afloat" must write `feet not touching anything / NOT on any surface`.

### Character-relationship-driven pose (actor tier)

Pose and effects are not isolated art; they are **externalizations of character relationships**. First decide who is strong/weak, active/passive:
- **The truly strong**: calm, composed, even zero effects (strong enough not to need to display power).
- **The weak/urgent side**: flamboyant, effortful, covered in effects (the harder they try, the more suppressed they look).
- Once set, the relationship stays consistent across the whole film; don't flip mid-way.
- **Multiple people in frame**: translate "relationship" into concrete blocking and write it dead. Down to "who sits/lies/leans/stands, who is higher/lower, who looks down at whom, whose gaze locks onto whose face". **Omitting body position → the model defaults everyone standing equal height; writing only "looking in some direction" → looking at void, not at the person**. Both parties' body positions + relative height + gaze locked to the other's face, replicated in positive + CONSTRAINTS + Avoid.

### Multi-person depth order (group blocking)

**When one shot has ≥3 people** (meeting rooms, family scenes, group battles), state layer by layer who is in front/behind:

```
- Foreground (closest): [person/object + position + facing + state]
- Near-midground (2nd layer): [……]
- Far-midground (3rd layer): [……]
- Farthest (background): [……]
```

**Restate at the end**: `So the depth order from camera into the scene is: A → B → C → D → background`. Pair with long shadows (high-angle) and giant objects lying across (as "dividing walls") to make the blocking readable.

### Long-distance dialogue eye-line lock (core reinforcement)

**Once dialogue goes beyond "arm's length"** (across-room confrontation / slamming the table across), models draw both people looking down in thought — seemingly looking but not actually.

**Reinforcement three-piece set** (replicated in 【body】+【CONSTRAINTS】+【Avoid】):
1. **Positive**: `eyelines MEET across the room, both heads slightly LIFTED to look at each other`
2. **Avoid section** excludes the "looking-down-in-thought" family item by item: `looking down at the table / heads bowed / eyes lowered / each lost in their own thoughts / averted gaze`
3. **Pure profile → 3/4 turn toward the other**; `head TURNED toward the other person, chin slightly LIFTED`

Scope: all dialogue shots beyond arm's length; pair with `assets/dialogue-board-card.md` (6-cell 2×3 relationship board).

## 7. Transition Methods (connection vs shot handling)

| Connection | Shot Handling |
|---|---|
| Last-frame continuation | next shot continues from the last-frame image; may push/track/change scale, but the opening composition must naturally grow from the last frame |
| Keyframe insert | new element's makeup frame as first frame; this shot's move starts from that frame (usually slow push-in or slight movement to showcase the new element) |
| Jump cut | scene/time change; first shot uses the new scene's establishing image; recommend 1 establishing shot first (extreme long/long shot) before entering narrative |

## 8. High-Risk Combination Blacklist (avoid item by item when writing the shot list)

- ❌ big close-up + orbit move (facial drift)
- ❌ 3+ people in frame + shallow-DoF close-up (will face-swap)
- ❌ fine hand action + fast camera move (finger breakdown)
- ❌ full-sprint running + telephoto front view (limb deformation)
- ❌ screen/text in frame + any camera move (text WILL garble; use "blurred glowing character stream" instead)
- ❌ in-shot costume change/form switch (split into two shots + keyframe insert)
