# Video Prompt General Skeleton (MUST READ when writing video prompts in Phase 4)

## ⛔ NON-NEGOTIABLE ELEMENTS (every video prompt MUST contain all of these; omitting any = defective prompt)

1. **Reference-image lines** — only the images actually used in THIS shot, each with its purpose; @ references state their use (video-extension chaining writes `extend @视频1 by N seconds` when applicable).
2. **Core-rules opening** — the first sentence matches the connection method (last-frame continuation / keyframe insert / jump cut / video extension).
3. **ONE primary action** (R3) + at most two micro-expression changes — with a full action-state flow (initial → trigger → reaction → body linkage → emotion → end) and body linkage.
4. **Camera move with 4 variables** — path / reference object / parallax / inertia; at most ONE move per shot.
5. **Dialogue section** — `Character says "line text"` (Chinese line kept), voice copied verbatim from the character card, tone marked; performance control for dialogue/emotional shots; dialogue beyond arm's reach gets the eye-line-lock three-piece set.
6. **Sound & lighting baseline** — one credible light source + 2–4 concrete sound-field anchors.
7. **Imperfection event** — for realistic/life-flow shots (skip only when the style demands clean/crisp).
8. **Ending aftertaste** — key line/action ends 1–2s before the final frame; last frame is an action landing point.
9. **Negative prompts** — concentrated on the end line; combat scenes include the violence de-escalation sentence.
10. **Character budget** — total ≤2000 chars; narrative section ≤300 chars (intent + key details, environment dressing left to reference images).

> A layered skeleton common to all three models (Seedance / Kling / Hailuo). Field order and wording are calibrated per `references/model-adapters/<target model>.md`; the skeleton itself works across all three. Each shot outputs ONE video-prompt code block with a total character budget ≤ 2000 (including spaces).
>
> v3 absorbed open-source community patterns on top of v2: action-state flow, body-linkage lookup table, camera-movement realism four variables, imperfection events for de-AI-ifying, material-source identity, sound & lighting baseline, dialogue-performance control, ending-aftertaste rules, shot-scale abbreviation standard.
>
> v4 integrated star-topping projects (seedance-prompt-skill 2669★ / awesome-seedance 2295★ / Seedance2-Storyboard-Generator 2104★ / higgsfield-seedance2-jineng 753★) on top of v3: timestamp storyboarding format, @ reference system, intent-vs-detail balance, 2-second hook framework.

## 0. Camera-Language Quick Lookup (decide the camera words BEFORE writing the prompt)

**Shot-scale abbreviations** (use uniformly in storyboard and prompts):
`ECU` extreme close-up / `VCU` very close-up / `BCU` big close-up / `CU` close-up / `MCU` medium close-up / `MS` medium shot / `MLS` medium long shot / `WS` wide shot / `FLS` full shot / `LS` long shot / `ELS` extreme long shot / `KS` over-the-shoulder

**Camera-move words** (put the English original into the prompt):
`Dolly In/Out`, `Pan Right/Left`, `Tilt Up/Down`, `Track Right/Left`, `Handheld`, `Static`

**Focal-length quick lookup** (determines the psychological distance of the frame):
`14-24mm` wide = environmental pressure / speed / spatial distortion / `35mm` narrative / street / person-environment balance / `50mm` near human eye / natural realism / `85mm` portrait close-up / emotion / shallow depth of field / `135mm+` spatial compression / isolation / voyeuristic feel / strong emotion

**Shot scale follows the psychological-defense line** (dialogue/emotional scenes): keep MCU/CU during the defensive phase; only enter BCU/ECU when the true emotion is exposed — do NOT start with a big close-up.

## 1. General Layered Skeleton (assemble in order)

```
【Reference Images】
(One line per image actually used in THIS shot + code & purpose; do not write appearance descriptions)
[Image 1] previous shot's last frame / first frame (baseline for frame continuation);
[Image 2] character makeup image CH-##;
[Image 3] scene establishing image SC-##;
...

【Core Rules】
Frame continues from first frame: character pose, position, light direction follow the first frame, only natural gradation allowed;
Keep character identity consistent: face/hairstyle/clothing/accessories match the makeup image, unchanged throughout;
Keep environment consistent: background/props/spatial layout match the establishing image;
Follow real physics: natural inertia, real weight, subtle breathing rise and fall;
Camera moves smoothly and with motivation; forbid static panning, slideshow-style switching, PPT transitions;
Forbid subtitles, watermarks, auto-added background music.

【Video Style】
(Style-anchor block, 4–6 phrases, restated verbatim from the project archive)

【Camera & Narrative】
(Write 3–8 sentences of continuous natural language per the shot-list row:
scene atmosphere → camera movement (opening frame → movement → closing frame) →
character blocking & action (ONE primary action + micro-expression + body linkage) →
dialogue (Character says "line text", voice copied from character card, tone X + performance control) →
sound design (credible light source + 2–4 concrete sound-field anchors) → closing image)

【Motion Constraints】
(4–8 items from the model adapter file: physical inertia, fabric/hair dynamics, no light flicker, true perspective...)

【Negative Prompts】
(Concentrated on the end line: facial deformation, clothing drift, floating actions, light jumps, background replacement,
prop clipping, extra people, text, watermarks, looping actions...)
```

## 2. Single-Shot Four-Beat Rhythm (apply when writing 【Camera & Narrative】)

Each 4–10s shot is laid out in four beats (short-video shot rhythm):

| Beat | Time Window | Task | Writing Key |
|---|---|---|---|
| Establish | 0–2s | Continue from first frame, confirm scene & character position | Write "frame starts from the first frame: ..." |
| Develop | 2–8s | Primary action advances, micro-expression changes | Write the action's "preparation → process → landing" |
| Climax | 8–12s | Emotional point / line point / visual hook | The most important info of this shot, ONE emphasized sentence |
| Close | 12–15s | Action lands and freezes, for last-frame extraction | Write "action settles, frame stills, final frame is the action-complete state" |

Short shots (4–6s) compress to: Establish(0–1s) → Develop(1–4s) → Close(4–6s).

**Ending-Aftertaste Iron Rule**: key lines or peak actions end at least 1–2 seconds early; the remaining time is for facial reaction, sound decay, stillness, motion continuation, or visual afterimage. Forbidding lines/actions that cut off abruptly on the final frame (unless the user explicitly wants a hard cut).

## 3. Action-State Flow (internal derivation when writing the primary action)

**Every primary action is derived through the state flow, then written into the prompt** (missing causality = the model "rationalizes" the action into its most mediocre version):

```
Initial state → Trigger cause → First reaction → Body linkage → Emotional change → End state
```

Example: `She is sitting (initial) → hears the door (trigger) → looks up (first reaction) → shoulders stiffen first, then slowly turns head toward the door (body linkage) → eyes shift from hope to disappointment (emotional change) → looks down and keeps folding clothes (end state)`

### Body-Linkage Lookup Table (MUST check when writing actions; missing linkage = mannequin feel)

| Action | Linkage to add |
|---|---|
| Walking | center of gravity, stride, arm swing, clothing response, foot-ground contact |
| Turning head | eyes move first, head turns second, shoulders follow last |
| Picking something up | fingers wrap, wrist takes force, object weight, contact shadow |
| Sitting down | knees bend, body sinks, clothing wrinkles, chair bears weight |
| Running | torso leans forward, arm swing, breathing, hair/clothes trail, ground feedback |
| Standing up | hands push off (if any), center of gravity rises, legs exert, hem drops |

## 4. Camera-Movement Realism (use when writing the camera move in 【Camera & Narrative】)

A camera move is not "where the camera goes"; it is four things written together:

| Variable | What to specify |
|---|---|
| Path | push, pull, pan, track, follow, orbit, rise, descend |
| Reference object | what the camera follows, at what distance |
| Parallax | whether foreground/midground/background move at different speeds (the key to real motion) |
| Inertia | whether start, accelerate, decelerate, stop are natural |

**Camera-move formula**:
```
camera start point + camera height + object being followed + motion path + speed change + foreground/background parallax + closing composition + forbid clipping/drifting/deformation
```

**Camera-move downgrade rule** (when the model fails): lower the camera speed one notch (fast → moderately fast → uniform), change motion amplitude to "half-step/slight-tilt" level; at most ONE camera move per shot; forbid stacking "orbit + push-in + pan".

## 5. Dialogue-Performance Control (MUST add for dialogue/emotional scenes)

Dialogue is not just "who said what"; it also carries **performance**. When the scene depends on long lines (interrogation, confession, breakup, cross-examination, rebuttal, apology, line-triggered emotional turn), add a compact performance-control block:

```
character's purpose / emotional barrier / trigger words / pauses & breath / facial & body changes / which reaction must not appear too early
```

**Dual performance tracks** (≥2-person dialogue): speaker performance track + listener reaction track written separately with timecodes. The listener's reactions (swallowing, fingertip tapping, averting gaze) carry equal weight with the speaker's lines.

**Line-trigger-word rule**: write clearly "at which line does the emotion start to change" — models are weak at "line-driven turns", so the turning point must be pinned to a specific line.

## 6. Sound & Lighting Baseline (every prompt MUST include)

**Minimum description standard**: every prompt includes one credible light source + 2–4 concrete sound-field anchors. Light source and sound field must match the scene card / character card; forbid "sourceless light" and "sourceless sound".

**Sound-field writing**: sound elements map one-to-one with visual elements — if there is a cat, there is meowing; if there is a clothesline, there is fabric sound; if it rains, there is rain hitting the window. First declare the mode (ambient only / on-site recording + environment), then list 2–4 concrete sounds, finally negate as needed (no music, no sound design, no narration).

**Multi-shot/suspense/action/continuation scenes**: add a compact 【Overall Sound & Lighting】 block to unify continuity (same light direction, same sound decay across the shot group), avoiding sound/light jumps between shots.

## 7. Imperfection Events (the key to de-AI-ifying)

AI models have a strong default aesthetic (perfect composition, clean images, smooth camera). To get cinematic feel instead of "AI feel", implant **imperfection events** in the timeline — one per shot, chosen from the following list (do not repeat the same one across the shot's 7 frames):

```
slight loss of focus then recovery / focus hunting / exposure fluctuation / rolling-shutter jelly effect / compression artifacts /
a lock of hair blown out of place by wind / a hem caught by the door for an instant / a blink briefly occluding the lens / breath-induced micro camera shake /
a prop shifting slightly then returning / character pausing briefly before continuing an action / gaze averting then returning
```

**Scope**: realistic/documentary/life-flow shots MUST include; animation/ads/big-VFX shots decide by style (omit when "clean and crisp" is wanted).

## 8. Material-Source Identity (whole-film tone decision, set during Phase 1 scripting)

The essence of a high-quality prompt is answering: **who shot this material, with what device, in what era, for what purpose?**

- Cinematic feature → film camera + 35mm Kodak Vision3 500T + director choreography
- Documentary texture → handheld + natural light + unscripted improvised behavior
- Home video / DV feel → jitter + defocus + sudden shutdown + low frame rate
- Surveillance perspective → high angle + no sound + low frame rate + compression noise

Once the material identity is fixed, all details can be derived. **The core of de-AI-ifying**: negative constraints turn off the model's default aesthetic (cinematic camera moves, perfect composition, commercial color grading, clean images), and the timeline gets imperfection events.

## 9. Dialogue & Voice Rules

- The dialogue section MUST state: `Character says "(line text)"`, voice = character card "voice" field **copied verbatim**, tone = the emotion marked at the line end. **The line text stays in the original Chinese** (e.g., `She says, "……不可能还有电。"`); only the surrounding prompt is English.
- Line word conversion: normal 3–4 characters/second; line duration must not exceed shot duration - 1 second (and keep another 1–2 seconds of reaction aftertaste).
- Strong lip-sync scenes (close-up long lines) → recommend post-dubbing; prompt writes "mouth opens and closes naturally when speaking, lip sync need not be precise".

## 10. Character Budget & Trimming Priority

- Total budget ≤ 2000 characters (incl. spaces). Reference images + core rules + style + negatives ≈ fixed overhead 600; narrative available ≈ 1400.
- Graded by duration (open-source practice): default target 800–1300 chars (8–15s); simple single-person or single-action 500–800; complex 10–15s 1300–2000; 16–30s only then 2000–3000.
- Over-budget trimming order (first to last): ① negative prompts (keep only the most critical 8) → ② motion constraints (cut to 4) → ③ sound description (≤10 words) → ④ environment dressing (≤10 words).
- **NEVER trim**: reference-image declarations, core rules, line text, primary action & micro-expression, style anchors.

## 11. Connection with the Four Consistency Mechanisms

- Last-frame continuation: the first reference image MUST be `[Image 1] previous shot's last frame`; core rules open with "frame continues from the first frame".
- Keyframe insert: reference is `[Image 1] makeup/establishing keyframe`; core rules write "new character/new prop is already in frame, then ...".
- Jump cut: reference is `[Image 1] scene establishing image SC-##`; core rules' first sentence rebuilds scene anchors (light/color copied verbatim from the scene card).
- **Video-extension chaining** (preferred when the model supports it; smoother than first-frame images): upload the previous shot's full output as `@视频1`; the prompt opens with `extend @视频1 by N seconds`, achieving seamless shot/episode connection (see continuity-playbook §1.5).

## 12. @ Reference System (Seedance 2.0 multimodal reference syntax)

Seedance 2.0 supports mixed image/video/audio reference; use `@` in the prompt to invoke references. **Every reference MUST state its purpose**:

```
@图片1 as first frame
@图片2 as character appearance reference
@图片3 as scene reference
@视频1 reference camera moves / reference fight actions / extension connection
@音频1 background music reference / voice reference
```

**Capacity limits**: images ≤9, videos ≤3 (total duration ≤15s), audio ≤3; mixed input ≤12 files.
**⚠ Platform limits**: uploading material containing realistic human faces is not supported (auto-blocked); generation with reference videos costs more; complex prompts (300+ characters) may follow instructions inconsistently — **keep the narrative section within 300 characters**, push extra information into reference materials.

**Multi-image division of labor** (consistent with image-prompt-engine one-image-one-job): each image has one job (first frame / character A / character B / scene / prop), explicitly bound with `@` syntax; forbid multiple images managing the same dimension.

## 13. Timestamp Storyboarding (advanced narrative-section format)

The narrative section has two writing styles, chosen by shot complexity:

**Style A · Continuous description** (simple shots, default): 3–8 sentences of natural language, as in §1 skeleton.

**Style B · Timestamp segmentation** (complex shots/long shots/key shots, strong control): mark per-second segments; models follow timestamps better than long-sentence descriptions:

```
0-3s: [camera/shot scale] + [frame] + [action]
3-6s: [camera/shot scale] + [frame] + [action]
6-9s: [camera/shot scale] + [frame] + [action]
9-12s: [camera/shot scale] + [frame] + [action]
12-15s: [camera/shot scale] + [frame] + [action] + [closing]
```

**Timestamp writing keys** (from awesome-seedance high-fidelity cases):
- Each segment opens with camera info: `[00-05s] Shot 1: (close-up/interior). Subject action.`
- Style prefix goes first: `Style: XXX, duration: N seconds.`
- Lines marked explicitly with `Dialogue cue: he says "..."`, not mixed into the frame description.
- Each segment carries ONE primary piece of info (R3's video version: one primary action per second-segment).
- Long shots / emotional shots: segment by "psychological task" rather than mechanical seconds (interrogating → accepting → remembering → letting go).

## 14. 2-Second Hook Framework (MUST use for each episode's first shot / key hook shots)

Short-video life or death happens in the first 2 seconds. The opening shot MUST have a **hook** that stops the viewer from scrolling. Choose the hook type by scene:

| Hook | Suitable Scene | Writing Example |
|---|---|---|
| Conflict direct-entry | action/confrontation | `Open on conflict: both draw swords at once, blades clash` |
| Visual spectacle | xuanhuan/sci-fi | `Open on spectacle: a massive magic array unfolds beneath their feet` |
| Suspense question | mystery/reveal | `Open on suspense: a half-opened letter sits on the table` |
| Emotional explosion | emotional drama | `Open on emotion: she stands in the rain, clutching torn photos` |
| Speed lines become motion blur | comic-drama fight | `The speed lines in the frame become real motion blur; the character bursts out of frame` |
| Panel border dissolves | comic-to-video | `The comic panel borders dissolve; the character moves out of the static image` |
| Ink-splash transition | ink-wash comic | `An ink splash covers the frame, revealing the next scene` |
| Background comes alive | environmental storytelling | `The character stays still; the fire/water/crowd in the background begins to flow` |

**Hook discipline**: the hook completes within the first 2 seconds of the opening shot, not stealing from the narrative body's duration; each episode has at least 1 strong hook, placed in the first shot or the most critical turning shot.

## 15. "Write Intent, Not Detail" Balance (reconciling with R1)

Seedance 2.0-class models have world knowledge + directorial thinking: **describing intent is more effective than encyclopedia-style detail stacking**. But abandoning detail entirely loses control. The balance law:

- **Intent + key details**: write "what happens + emotional direction + key visual constraints (form weakness / color / prop)"; leave the rest to the model's directorial thinking.
- **When to write details** (R1's active zone): the action's causal chain (state flow), body linkage, micro-expression body parts, form weakness, line text — these are what the model cannot infer itself.
- **When to save details**: environment dressing (scene card already has reference images), lighting-term stacking, camera technical parameters (the model plans them automatically) — hand these to the reference images and the model.
- **Complexity red line**: single narrative section ≤300 characters; over → split reference materials or split the shot.

## 16. Pre-Output Self-Check

- [ ] Reference-image lines: only images actually used in this shot, no extras; all @ references state their purpose
- [ ] Core rules: first sentence matches the connection method
- [ ] Narrative section: opening→motion→closing complete, primary action unique (R3), micro-expression at body-part level, with body linkage
- [ ] Action-state flow: all six stages (initial→trigger→reaction→linkage→emotion→end) present (add causality if missing)
- [ ] Camera move: path/reference/parallax/inertia all present, no stacked moves
- [ ] Dialogue section: voice copied verbatim, character count compliant, performance control present (dialogue/emotional shots)
- [ ] Sound & lighting: credible light source + 2–4 concrete sound-field anchors
- [ ] Imperfection event: implanted for realistic/life-flow shots (animation/ads decide by style)
- [ ] Ending aftertaste: key lines/actions end 1–2 seconds early; last frame is an action landing point
- [ ] Timestamp segmentation (complex shots): one primary action per segment, style prefix + dialogue cue explicit
- [ ] 2-second hook: first shot / key turning shot has a hook (conflict/spectacle/suspense/emotion/comic effect)
- [ ] Intent balance: narrative section ≤300 chars, key details (state flow/linkage/weakness/lines) kept, environment dressing left to reference images
- [ ] Negative end line: concentrated, precise, no repetition in the positive zone
- [ ] Total characters ≤ 2000
