---
name: manju-director
description: "A 100% original AI comic-drama / short-drama directing skill. It converts a source text or theme into a complete shot-by-shot production package that can be fed directly to video models (Seedance / Jimeng, Kling, Hailuo). Core mechanisms: last-frame continuation and video-extension chaining guarantee visual continuity; character/scene/prop asset cards lock consistency; keyframe insertion safely introduces new elements; action and expression descriptions are detailed down to fingertips and eye movement. Use this skill whenever the user mentions comic drama, AI short drama, drama script, storyboard script, storyboard table, shot-by-shot prompts, text-to-video scripts, image-to-video, last-frame continuation, video extension, first-frame continuation, character consistency, dynamic comics, Seedance, Kling, or Hailuo. Responsible for producing a full episode / multi-episode continuous narrative — NOT single-shot prompts."
agent_created: true
---

# Manju Director (漫剧导演)

Converts "a piece of source text / a theme" into "a complete shot-by-shot production package ready to feed to video models": Standard storyboard script → Asset cards → Shot list → Per-shot prompts (first-frame image + video) → Continuity execution → Quality check.

> **Originality Declaration**: All scripts, characters, dialogue, and prompts produced by this skill are 100% original. It never references the names, characters, or plot elements of any existing work. User-provided source material is adapted within its licensed scope.

**Core Philosophy: Directing first, engineering second.** Every prompt is merely the written form of a directing decision; every consistency mechanism exists to make the model pull fewer cards and make the user spend less money.

---

## The Four Consistency Mechanisms (the skeleton of this skill, running through the entire workflow)

1. **Last-Frame Continuation (visual coherence)** — The final frame of the previous shot's output is extracted and used as the first-frame input of the next shot. Shot N's ending frame = Shot N+1's starting frame; space, lighting, and pose continue seamlessly. This is the default connection method, except for jump cuts.

2. **Video-Extension Chaining (seamless continuation, preferred on Seedance 2.0)** — When the target model supports video extension, the entire previous shot's output is uploaded as `@视频1` (or `@video1`), and the next shot's prompt opens with "extend @视频1 by N seconds". Visual/lighting/action continuity is inferred by the model from the whole video segment, which is smoother than first-frame images. Used for both inter-shot and inter-episode connections (see continuity-playbook §1.5).

3. **Asset-Card Locking (character/scene consistency)** — Every character, scene, and key prop gets a card (appearance anchors + form weakness + reference-image number). Once the makeup reference image is generated, it is **frozen**; all subsequent prompts must restate the anchors and reference the same image. Rewriting appearance from memory is forbidden.

4. **Keyframe Insertion (safe entry of new elements)** — When a new character, new prop, or major state change (costume change / injury / form switch) appears for the first time, it must **NOT** be stuffed directly into a narrative shot. First produce a separate "makeup keyframe" (character → half-body or full-body makeup; prop → close-up establishing shot), freeze it, then use it as that shot's first-frame/reference before entering the narrative.

---

## Iron Rules (R1–R8, non-negotiable across the whole workflow)

- **[R1] Detail Density** — Action and expression descriptions in scripts and prompts must be specific to body parts (fingers, wrists, jawline, Adam's apple, eyelashes, breathing rhythm, fabric dynamics). "She was sad" is rejected draft; "Her fingertips clenched the edge of the letter, knuckles turning white, throat moved once without a sound" is the finished version.
- **[R2] Confirmation Gates** — Any node marked 【闸】(Gate) must present its output to the user and wait for explicit confirmation before proceeding. Five gates: Gate 1 outline & asset table → Gate 2 makeup reference images → Gate 3 shot list → Gate 4 first-shot prompts → Gate 5 first-shot output acceptance. Subsequent shots run on the fast track (see Phase 5).
- **[R3] One Primary Action per Shot** — A single video shot (5–10s) carries exactly ONE primary action plus at most two micro-expression changes. Stacking multiple actions is the #1 cause of model limb breakdown.
- **[R4] Anchor Restatement** — In every prompt, the appearance anchors of appearing characters and the color anchors of scenes must be restated **verbatim** from the asset card original text. No paraphrasing, no omission followed by improvised completion.
- **[R5] One-Way Asset Convergence Chain** — Color palette/tone → makeup assets → storyboard → prompts → output → last frame. Downstream always references upstream frozen outputs; modifying upstream = re-forging all downstream. Running backward is forbidden.
- **[R6] Originality Red Line** — All scripts, character names, settings, and dialogue must be original. No referencing the names, characters, dialogue, or signature settings of any real film/anime/game/novel. User-provided source text is adapted within its authorized scope.
- **[R7] Genre Isolation** — Creative decisions for different genres (tone, color palette, shot preferences) are read ONLY from the corresponding genre file. One creation session loads exactly ONE genre file. Cross-genre mixing is forbidden.
- **[R8] Scripts Belong in Files** — Long documents such as the standard storyboard script and shot list are written into project files (for reuse and iteration); prompts fed to models are output in conversation as code blocks (for direct copying).

---

## Quick Routing (which file to read first)

| User Intent | Read First |
|---|---|
| Give a theme/source text, want a full episode of comic drama | Follow workflow Phase 0→6 in order; first read `references/script-format.md` |
| Specified genre (sci-fi / xuanhuan / urban / romance / campus) | `references/genres/<genre>.md` (read ONLY that one, see R7) |
| Specified target model (Seedance / Kling / Hailuo) | `references/model-adapters/<model>.md` |
| Ask how to design a shot (shot scale / camera move / focal length / pacing) | `references/shot-language.md` + `references/lighting-styles.md` |
| Write a first-frame image prompt | `references/image-prompt-engine.md` (5 need-anchoring questions / 7-layer frame decomposition / one-image-one-job / three-place repetition / five-piece signature block / lighting-sculpting formula / focal-length lookup / dual register) |
| Write a video prompt | `references/video-prompt-framework.md` (timestamp storyboarding / @reference system / 2-second hook / action-state flow / body linkage) + model adapter file |
| Seamless shot/episode connection | `references/continuity-playbook.md` §1.5 video-extension chaining (`@视频1` extension) + §2 last-frame continuation |
| Broken continuity / face swapping / new character entry | `references/continuity-playbook.md` |
| Failed output: light edit / heavy rerun / upscale to 2K | `references/continuity-playbook.md` Chapter 4 matrix + dual-register decision |
| Dialogue scene needs a relationship board | `assets/dialogue-board-card.md` (6-cell 2×3 locking the 180° axis) |
| Composite asset image (character+scene+prop in one) | `assets/scene-actor-card.md` |
| Fill in a template (character card / scene card / shot list) | corresponding template under `assets/` |

---

## Workflow (Phase 0 → 6)

### Phase 0 · Project Setup & Global Parameters (done in conversation, no file written)

Collect and confirm four global parameters. Ask for anything missing (ask everything in ONE round):

1. **Genre**: Sci-fi / Xuanhuan / Urban / Romance / Campus / Other. (If "Other", reference the nearest of the five genres and tell the user which one was used.)
2. **Target model**: Seedance / Kling / Hailuo / Undecided. (If undecided, default to Seedance structure output; the prompt structure includes a compatibility layer for all three models.)
3. **Aspect ratio & episode duration**: 9:16 vertical (mainstream for short drama) or 16:9 horizontal; single episode defaults to 60–90 seconds.
4. **Art style**: one-line keywords (e.g., "Chinese ink-wash comic style", "cel-shaded anime feel", "live-action-style comic adaptation"). Expanded into a style-anchor block in Phase 2.

After confirmation: **load the corresponding genre file** (`references/genres/`) and **model adapter file** (`references/model-adapters/`). This phase produces no script.

### Phase 1 · Script Engineering 【Gate 1】

> Read `references/script-format.md` (format spec + original example). Read the genre file's "emotional-curve patterns" and "performance & dialogue style" sections as needed.

Input is one of two:

- **User provides source text** (novel excerpt / existing script) → Keep the main plot and golden lines, rearrange into a storyboard script per the standard format; if the source exceeds one episode's volume, split into multiple episodes by the "hook at the end" principle, each episode ending with suspense.
- **User provides only a theme** → First produce a three-line outline (one-sentence setting / three-beat emotional curve / ending hook), get user confirmation, then expand into a standard storyboard script.

Standard storyboard script format (see script-format.md, strictly enforced):

- Header: aspect ratio / total duration / number of scenes / one-line emotional curve.
- Each scene: scene header (full environment description: light, color tone, spatial layers, ambient sound).
- Each shot: `**[MM:SS.S – MM:SS.S] Beat name**` + `[shot scale | camera move | frame key points]` + extremely detailed action & micro-expression body text (R1) + dialogue (`> **Character**: (tone/subtext) line`) + line-end `[Emotion: X | Hook: Y | Connection: Z]`.
- Connection Z four values: `last-frame continuation` (default) / `keyframe insert · new character` / `keyframe insert · new prop` / `jump cut`.
- Single shot duration 4–10 seconds (within model single-segment limits); sum of all shot durations = total duration.

After producing the script, run an **asset scan**: list the full-episode character table / scene table / prop table (mark at which shot each new element triggers a keyframe insert), present together with the script to the user for confirmation → **Gate 1**.

### Phase 2 · Asset Cards & Makeup 【Gate 2】

> Templates: `assets/episode-bible.md` (project archive), `assets/character-card.md` / `assets/scene-card.md` / `assets/prop-card.md` (one card each), `assets/scene-actor-card.md` (**composite asset image**: one image covering character+scene+prop+atmosphere, the most efficient mode for keyframe insertion).

Execute in asset-convergence-chain order (R5):

1. **Project archive**: fill episode-bible — tone, color-palette iron rules (take HEX values from the genre file and lock them, including the 6-level intensity selection), style-anchor block (4–6 style descriptions), **cinematic five-piece signature block** (composition school + hex palette + DP credit + film stock + anti-AI-quality seal; all five must be self-consistent), **word-deletion regulator** (which words to delete for clean/bright vs dark/oppressive tones), general negative library (from the genre file's "failure points" chapter).
2. **Character card**: one per character — appearance anchors (face/hairstyle/clothing locked in one sentence), form weakness (the feature most likely to be drawn wrong), voice description (for dialogue dubbing and prompts), makeup prompt (add lighting method + catchlight + 85mm focal-length feel).
3. **Scene card**: one per scene — spatial-structure anchors, light-source direction, color tone, prop inventory. Multi-angle establishing images as needed (multiple camera-position versions of the same space).
4. **Prop card**: only key props (plot anchor objects), mark form weakness (product lighting plan).
5. **Composite asset image** (as needed): when **a new character first appears in a new scene AND the character is strongly tied to that scene**, one image replaces the three separate "character makeup + scene establishing + prop establishing" images (see `scene-actor-card.md`).
6. **Makeup reference image generation**: use an image-generation tool to produce makeup images one by one per the character card (single person, neutral light, solid-color or blurred background of the actual scene). Present output to user for confirmation → **Gate 2**. After freezing, write the reference-image number back into the card's `ref:` field. Produce scene establishing images the same way. All prompt writing strictly follows `image-prompt-engine.md` (**one-image-one-job + exclusive declaration + three-place repetition + five-piece signature block + lighting sculpting**).

Gate 2 not passed → entering Phase 3 prompt writing is forbidden (R5).

### Phase 3 · Shot List 【Gate 3】

> Template: `assets/shotlist-template.md`; shot design language from `references/shot-language.md` (incl. opening frame/closing frame, single-shot four-beat rhythm, character-level colored text, long-distance dialogue eye-line lock, character-relationship-driven pose) + `references/lighting-styles.md` (lighting/focal length/time-of-day light/DP tone table); genre shot preferences from the genre file Chapter 3.

**Dialogue pre-requirement**: **ANY ≥2-person dialogue scene must produce a dialogue relationship board FIRST** (`assets/dialogue-board-card.md`), 6-cell 2×3 locking the 180° axis + eye-line contact + exclusive declaration. The shot list may only be written after the relationship board passes its gate.

Convert the script shot-by-shot into a production shot list, one line per shot, columns: shot # / duration / shot scale / camera move / frame subject / primary action (unique, R3) / micro-expression / dialogue / emotion / connection method / first-frame source (last-frame=previous shot # / keyframe=makeup or composite asset image # / new=establishing image) / opening→closing frame / risk flags (⚠ multiple people in frame, hand close-up, text in frame, large motion, long-distance dialogue, blur/noise).

Present the shot list to user for confirmation → **Gate 3**. Focus user review on: whether connection methods are marked correctly, whether new characters/props all have keyframes arranged, whether any shot violates R3, whether closing frames are all action-complete states (for last-frame extraction), whether dialogue relationship boards align.

### Phase 4 · Per-Shot Prompts 【Gate 4 — first shot only】

> Writing first-frame image prompts: read `references/image-prompt-engine.md` (**5 need-anchoring questions + 7-layer frame decomposition + one-image-one-job/exclusive declaration + three-place repetition + five-piece signature block + lighting-sculpting formula + focal-length lookup + dual register + word limit ≤500**). Writing video prompts: read `references/video-prompt-framework.md` (**camera-language lookup / shot-scale abbreviations + general skeleton + single-shot four-beat rhythm + action-state flow + body-linkage lookup + camera-movement realism + dialogue-performance control + sound & lighting baseline + imperfection events + ending aftertaste + character budget**) + `references/model-adapters/<target model>.md` (that model's structure formula).

Each shot produces two code blocks:

1. **First-frame image prompt** (fed to the image model): per the image-prompt-engine structure formula — **subject line (R4 anchor restatement + exclusive declaration) + spatial-composition line (height via compositional relationships, NOT meters) + lighting line (lighting-sculpting formula: direction/half-face/highlight points/wide aperture/contact shadow, MUST include) + environment line + camera line (focal length from lookup) + five-piece signature block + CONSTRAINTS section (core constraint restatement) + negative end line**. For shots connected by "last-frame continuation", the first-frame image = previous shot's last frame; this block is marked "no generation needed, use shot N's last frame". For shots connected by "keyframe insert", the first-frame image = the composite asset / character card / scene card / prop card number.
2. **Video prompt** (fed to the video model): assembled per the video-prompt-framework general skeleton — 【reference images】【core rules】【video style】【camera & narrative】(apply the four-beat rhythm: establish→develop→climax→close, including opening/closing frame, **action-state flow**, **body linkage**, **dialogue-performance control** and line voice; **dialogue beyond arm's reach MUST add the eye-line-lock three-piece set**; **realistic/life-flow shots MUST add an imperfection event**)【motion constraints】【negative prompts】(**combat scenes MUST add the violence-de-escalation sentence**). Structure calibrated per the model adapter file.

Produce ONLY **Shot 1's** two code blocks first → **Gate 4** (user confirms prompt style and detail density), then batch-produce all remaining shots.

### Phase 5 · Shooting Execution & Shot Connection (per-shot loop)

Per-shot loop:

1. User takes the first-frame image/reference materials + video prompt to the model to produce the output.
2. After the output returns, choose the path by connection method:
   - **Video-extension chaining** (preferred when the model supports it): the whole output as `@视频1`; next shot opens with "extend @视频1 by N seconds" (no last-frame extraction needed; most stable continuity; see continuity-playbook §1.5).
   - **Last-frame continuation**: extract the last frame `scripts/extract_last_frame.py <video path> -o <output dir>` (wraps ffmpeg, auto-names `shot_###_last.png`), use it as the next shot's first-frame input; the prompt notes "first frame = previous shot's last frame; character pose/lighting continue from here".
3. Fast-track quality check: pass → next shot; fail → consult `references/continuity-playbook.md` "dual-register decision" (**light edit one sentence: change X to Y, don't touch anything else** → heavy rerun: change ≥3 things / change pose / change camera angle / continuous light edits causing face-melting and identity-swapping → stop, return to Phase 2/4).

**Keyframe-insert execution** (shots connected by keyframe insert): prefer the **composite asset image** (scene+character+prop in one image, most efficient); otherwise separate makeup frames per character/scene/prop. See continuity-playbook Chapter 3.

**Jump-cut execution**: shots that change scene/time do NOT use last-frame continuation; use that scene's establishing image as the first frame, and rebuild the scene anchors in the prompt's opening sentence.

### Phase 6 · Quality Check & Card-Pull Control

Each shot checked against the `references/continuity-playbook.md` Chapter 5 quality checklist: character consistency (face/hairstyle/clothing vs makeup image), scene consistency (props/light-source direction vs scene card), connection quality (whether last-frame continuation is natural), physical plausibility, platform safety.

Card-pull control principles (written into every failure recommendation):

- First freeze everything that can be frozen (makeup, color palette, first frame), reducing variables to only "this shot's action".
- On failure, first change the prompt structure (fewer actions, fewer people in frame, simpler camera moves) — don't rerun the same words.
- Max 3 reruns per shot; after 3 failures → downgrade plan (split shot / change shot scale / keyframe-insert supplementary narrative), and mark the change in the shot list.

---

## Continuous-Conversation Rules

- Global parameters (genre/model/aspect/art style) persist for the entire session once confirmed; update only when the user actively changes them. Genre change → reload the genre file and ask whether frozen assets need re-forging (R5).
- Cross-session for the same project: all cards and the shot list are already saved in project files; new sessions first read the project files to restore context, no missing-reporting.
- Multi-episode production: each episode independently runs Phases 1–6; character/scene cards are shared across the whole drama; new episodes only add new assets; each episode's first shot connects via the previous episode's last shot's last-frame continuation (serial) or jump cut (standalone episode).

## Output Language Rules

- Conversation and scripts use Simplified Chinese; prompts default to Chinese (all three models are friendly to it); when a model adapter file specifies that a field needs English, follow that file.
- Prompts are always placed in code blocks; first-frame image prompts and video prompts go in SEPARATE code blocks, never merged.

## Reference File Index

| File | When to Read |
|---|---|
| `references/script-format.md` | Phase 1 required: standard storyboard script format + original example |
| `references/shot-language.md` | Phase 3 shot design: shot scale/camera move/focal length/axis/opening-closing frame/rhythm lookup |
| `references/lighting-styles.md` | Phases 2–4: lighting methods/focal-length feel/time-of-day light/product lighting/style quick-matching |
| `references/image-prompt-engine.md` | Phase 4 writing first-frame image prompts required: 5 need-anchoring questions/7-layer decomposition/six-section/lighting-sculpting formula/focal-length lookup/reference-image discipline/iteration discipline |
| `references/video-prompt-framework.md` | Phase 4 writing video prompts required: camera-language lookup/general skeleton/four-beat rhythm/action-state flow/body linkage/camera-movement realism/dialogue-performance control/sound-light baseline/imperfection events/@reference system/timestamp storyboarding/2-second hook/intent-vs-detail balance/character budget |
| `references/continuity-playbook.md` | Phase 5 required: video-extension chaining/last-frame continuation/keyframe insert/jump-cut SOP + failure-handling matrix + quality checklist + continuation workflow |
| `references/genres/sci-fi.md` | When genre=sci-fi (R7: read ONLY this genre file) |
| `references/genres/xuanhuan.md` | When genre=xuanhuan/immortal-fantasy |
| `references/genres/urban.md` | When genre=urban |
| `references/genres/romance.md` | When genre=romance |
| `references/genres/campus.md` | When genre=campus |
| `references/model-adapters/seedance.md` | When target model=Seedance Jimeng (Phase 4 required) |
| `references/model-adapters/kling.md` | When target model=Kling |
| `references/model-adapters/hailuo.md` | When target model=Hailuo |
| `assets/episode-bible.md` | Phase 2 fill-in: project archive (tone/6-level color intensity/DP signature block/word-deletion regulator) |
| `assets/character-card.md` / `scene-card.md` / `prop-card.md` | Phase 2 fill-in: separate asset card templates (makeup incl. lighting/catchlight/focal length) |
| `assets/scene-actor-card.md` | Phase 2 fill-in: composite asset image (character+scene+prop+atmosphere in one) |
| `assets/dialogue-board-card.md` | Required before Phase 3: dialogue relationship board 6-cell 2×3 locking the 180° axis |
| `assets/shotlist-template.md` | Phase 3 fill-in: shot list template (incl. opening/closing frame columns) |
| `scripts/extract_last_frame.py` | Phase 5 execution: video last-frame extraction (ffmpeg wrapper) |
