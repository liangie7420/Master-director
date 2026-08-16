# Continuity Playbook: Last-Frame Continuation / Video-Extension Chaining / Keyframe Insert / Jump Cut / Failure Handling / Quality Check

> This playbook is the engineering core of "reducing card-pull losses". How to read: consult throughout Phase 5 shooting execution; when output fails, check Chapter 4 matrix FIRST, don't rush to rerun.
>
> v2 added on top of v1: "dual-register failure decision, upscale-to-2K prescription, violence de-escalation sentences, form-weakness SOP upgrade".
>
> v3 added: video-extension chaining as the fourth connection mechanism (Seedance 2.0 native capability, from Seedance2-Storyboard-Generator 2104★), refined light-consistency QC, continuation workflow, card-pull control & iteration discipline.

---

## 1. Overview of the Four Connection Mechanisms

| Mechanism | Solves | First-Frame Source | When to Use |
|---|---|---|---|
| Video-extension chaining | inter-shot/episode seamless continuation | previous shot's whole output as `@视频1` | **PRIMARY** — when the model supports extension |
| Keyframe-pair shooting (首尾帧) | batch-production continuity | designed first + end frame pair (image model) | **PRIMARY batch** — when the model supports first-and-last-frame interpolation |
| Tail-frame carry | inter-shot visual coherence (fallback) | previous shot's output last frame (extracted by `scripts/extract_last_frame.py`) | fallback only — neither of the above supported |
| Keyframe insert | safe entry of new character/prop/state | separately produced makeup keyframe | the shot where a new element first appears |
| Jump cut | scene/time change | new scene's establishing image | between scenes |

Memory phrase: **same scene same beat → video extension or keyframe pair; new face → makeup first; new place → establishing first; neither extension nor 首尾帧 supported → tail-frame carry (fallback).**

## 1.5 Video-Extension Chaining SOP (PRIMARY connection — use whenever the model supports extension)

Seedance 2.0 / Jimeng extend / Kling 2.x / Vidu support uploading existing video and natively extending it (the added part becomes an independent shot). This is the industry-mainstream connection: frame/lighting/action continuity is inferred by the model from the whole video, no manual last-frame extraction needed. **If the model supports extension, this is the DEFAULT connection — do not fall back to tail-frame carry.**

1. After shot N's output passes acceptance, upload the whole segment as `@视频1`.
2. Shot N+1's prompt opens with: `extend @视频1 by N seconds` (N = this shot's added duration).
3. The narrative section continues from the previous shot's ending state (emotion advances, does not restart; see §6.3), and may change camera angle/shot scale.
4. Generation length selects the "added part" duration, NOT the total duration.
5. Video extension is also capacity-limited: reference videos ≤3, total duration ≤15s; for extra-long scenes, extend in segments.

**Choice vs keyframe-pair shooting / tail-frame carry**:
- Model supports video extension + needs seamless action/lighting continuation → **video extension** (first choice, most stable).
- Model supports first-and-last-frame interpolation + batch production needed → **keyframe-pair shooting** (§2.5).
- Model supports neither / needs precise first-frame composition control (major camera change) → **tail-frame carry** (§2).
- Scene/time change → neither; use **jump cut**.

## 2. Tail-Frame Carry SOP (FALLBACK — use only when the model supports NEITHER video extension NOR first-and-last-frame interpolation)

### 2.1 Execution flow (per-shot loop — PATH C fallback)

1. After shot N's output passes acceptance, extract the last frame:
   `python scripts/extract_last_frame.py <shotN.mp4> -o <project/frames>` → produces `shot_###_last.png`.
2. Visually inspect the last frame: is the character pose/lighting/composition suitable to "grow into" the next shot's starting frame? If unsuitable (e.g., last frame is a motion-blur frame) → use the `-t` parameter to take a frame 0.2–0.5 seconds earlier.
3. In shot N+1's video prompt: that last frame is the first-frame input; the prompt's opening section writes "frame continues from the first frame: character keeps pose and position from the first frame, light direction unchanged, then ...".
4. Shot N+1 shot-scale/camera rules:
   - Same scale continuation (CU→CU): most stable, directly continue.
   - Push closer (MS→CU): safe; the last frame itself is the enlargement source.
   - Pull back (CU→WS): usable, but the last frame only provides the central area; the prompt must fill in surrounding props (restate from the scene card).
   - Change viewing angle (front→side): **do NOT use last-frame continuation**; when the angle jumps, the last frame is misleading; rebuild with the character makeup image + scene establishing image as dual references.

### 2.2 Landing-frame quality principles (apply to BOTH tail-frame extraction AND keyframe-pair end-frame design)

- The last frame should preferably be an "action landing frame" (the still instant of a completed action). Design this actively when writing the script: end each shot's body text with the action reaching its landing point ("hand stops at the cup rim" "gaze settles"), never cut mid-motion.
- The last frame must NOT contain: motion blur, half-closed eyes, a mouth mid-speech, a half prop at the frame edge. If it does → take an earlier frame.
- For 9:16 vertical last frames, keep the subject away from the top/bottom 10% edges (platform UI occlusion zone).

### 2.3 Cross-episode connection

Serial episodes (model supports video extension): the previous episode's full output as `@视频1`; this episode's first shot opens with "extend @视频1 by N seconds", achieving seamless episode connection (Seedance 2.0 native, more stable than last-frame images).
Serial episodes (last-frame only): previous episode's last shot's last frame = this episode's first shot's first frame.
Standalone episodes: this episode's first shot uses jump cut (scene establishing image).

## 2.5 Keyframe-Pair Shooting SOP (首尾帧插帧 · 批量生产主流)

Industry batch-production mode: design keyframe pairs in Phase 3, generate them all with the image model, then interpolate each shot on the platform's first-and-last-frame feature (Kling 首尾帧 / Jimeng). This is the PRIMARY batch path — choose it whenever the model supports first-and-last-frame interpolation.

### 2.5.1 Design (Phase 3, in the shot list)

- Every shot carries an **end-frame design**: an action-landing frame (the action's completion instant — same principles as §2.2: no motion blur, no half-closed eyes, no mid-speech mouth, subject away from the top/bottom 10% edges).
- The pair (first frame + end frame) defines the shot's full motion path; the video prompt then only describes the **intermediate motion** (state flow), not the landing state.
- Same-scene runs: first frames derive from the scene establishing image + character makeup (anchor restatement); end frames are the same space with the action landed.

### 2.5.2 Batch generation (Phase 4/5)

1. Generate ALL first frames and ALL end frames with the image model, using the Phase 4 image prompts (end-frame prompt: same structure formula, subject in the designed landing pose).
2. Present a **contact sheet** (all pairs tiled) to the user — this IS the acceptance gate for this path.
3. Interpolate per shot: upload first + end frame → first-and-last-frame interpolation → video of the shot's duration. Shots are independent → **batch interpolation allowed** (no data dependency between pairs).
4. QC per shot (evidence required); by design shot N's end frame ≈ shot N+1's first frame — check this at the pair seams.

### 2.5.3 Why this beats tail-frame carry

- Keyframes are **designed and controllable** (image model), not extracted and inherited (video output).
- Shots are independent → **batchable** → no sequential bottleneck.
- Consistency comes from anchor locking + frozen reference images, not from the previous shot's output.

### 2.5.4 Failure handling

- Interpolated motion unnatural → rewrite the **intermediate motion** in the video prompt, keep the pair frames.
- End frame and first frame inconsistent (face/light jump at the seam) → regenerate the pair's end frame from the same anchor image; don't patch in the video.
- Max 3 reruns per shot, then downgrade plan (Chapter 7).

## 3. Keyframe-Insert SOP

### 3.1 Trigger conditions (check item by item during script scan)

- A new character first shows their face (back/silhouette first appearance does NOT count; only face-reveal counts).
- A key prop's first close-up (plot anchor objects: keepsake, document, weapon, terminal screen).
- A character's major state change: costume change, injury, disguise, form switch.

### 3.2 Flow

1. **Produce the makeup keyframe** (image-to-image, NOT in narrative):
   - New character: single person, neutral light, this scene's light color temperature, half-body or full-body, front with slight 15° turn. If a character card already exists, use the card's makeup image and only add the "this-scene lighting version".
   - New prop: close-up establishing frame — prop centered occupying 40–60% of the frame, all form weaknesses visible, shallow depth of field, this scene's light source.
2. **Freeze numbering**: write `CH-02`, `PR-01`-style numbers into the character card / prop card `ref:` field.
3. **Enter the narrative shot**: that shot's video prompt = keyframe as first frame (or dual images: previous shot's last frame + keyframe, per model multi-image capability, check model-adapters) + anchor restatement + "the new element is already in frame, then the camera ...".
4. **Debut shot design**: give a new character's debut shot 4–6 seconds, slow push-in or slight movement, medium-close-up or closer scale, so the audience (and the model) fully absorb the appearance; forbid big movements or face occlusion in the debut.

### 3.3 Composite asset image (more effective in practice)

High-frequency practice in open-source projects: **one image covering character + scene + prop + atmosphere**. manju-director implements this with `assets/scene-actor-card.md`.

### 3.4 State-change inserts

Costume change / injury and other state changes of the SAME character: produce a "new-state makeup frame" (same angle same light, only the state changed), the prompt writes "same person as the reference image, only clothing/wound changed to ...", other anchors remain verbatim unchanged.

## 4. Failure-Handling Matrix (diagnose first, then treat)

| Symptom | Most Likely Root Cause | Treatment (try in order) |
|---|---|---|
| Face changes / face swapping | missing reference image or over-loaded multi-person frames | ① add/replace makeup reference ② reduce people in frame, split into shot/reverse-shot ③ close-up → medium-close-up ④ anti-face-swap three-piece set (per image-prompt-engine §2) |
| Limb/finger breakdown | multiple actions in one shot (violates R3) or hand close-up + camera move | ① cut to single action ② hand out of frame or fixed camera ③ lower camera speed |
| Light jumps | scene-card light source not restated / conflict between last frame and prompt light direction | ① copy the scene card's light sentence into the prompt's first section ② change last-frame extraction point ③ enable lighting four-piece set (lighting-styles §1) |
| Clothing/hairstyle drift | anchors not restated verbatim (R4 violation) | restate verbatim and rerun; still drifting → promote that element to form weakness + three-place repetition (image-prompt-engine §9) |
| Garbled text | screen/paper text entering frame | change to "blurred glowing character stream / illegible handwriting"; readable text must be post-composited |
| Motion glitch / teleporting | camera too fast + action amplitude too large stacked | lower camera one notch (fast→moderately fast→uniform), change action amplitude to "half-step/slight-tilt" level |
| Background bystander breakdown | deep depth of field group shots | switch to shallow DoF blurred background, or prompt writes "background figures silhouetted, no facial details" |
| First-last-frame loop feel | zero camera displacement + symmetric action | add a micro-displacement (slow push 5%) or gaze change to break symmetry |
| Visual anchor missing | one image multiple focuses | cut to only 1 visual anchor (light spot / ribbon / sword tip) |
| **Noisy/blurry/dirty** | resolution too low (**NOT real noise**) | ① pull overall size to 2K/4K ② HD remaster = feed the existing image back as base + strongly write "keep character/face/pose/composition/color/effects ALL unchanged, only improve quality" |
| **Long-distance dialogue: both looking down in thought** | eye-line control lost | long-distance dialogue eye-line-lock three-piece set (lighting-styles §11) replicated in 【body+CONSTRAINTS+Avoid】three places |

### 4.1 Dual-register failure decision (heavy build vs light edit)

Already decided when writing prompts: Phase 2 keyframes are all heavy-build; Phase 5 failure first tries **light edit** once:

- **Light edit one sentence** (with a Nano-Pro-class visual understanding model):
  - change only 1 variable (e.g., change expression, light, composition)
  - template: "Change X to Y, do not touch anything else."
- **Heavy rerun** (complete rebuild with an Image-class model):
  - change ≥3 things simultaneously
  - change pose / change structure / change camera angle
  - continuous light edits begin melting face and swapping identity
  → Stop, return to Phase 2/4 and rebuild.

### 4.2 Violence de-escalation sentences (MUST include for martial-arts/combat scenes)

Review gate: `opponents are knocked back by force, not visibly injured. No wounds, no damage, no blood.`
- Clash-frame add-on: `sword meeting sword, NOT sword meeting body`
- Downed-frame add-on: `lying still as if asleep or unconscious, no visible injuries`

**Scope**: xuanhuan martial arts, urban business warfare, campus conflict, sci-fi armed confrontation — all shots with confrontation/violence.

**Anti-AI-quality ending** (permanent in Avoid, carried in image-prompt-engine §14).

## 5. Quality Checklist

### 5.1 First-frame image QC (every image)

- [ ] Character face/hairstyle/clothing consistent with the frozen makeup image (check item by item: brow shape, hair color, pupil color, collar style, accessories)
- [ ] Scene props consistent with the scene-card inventory (light-source direction, primary color tone, key prop positions)
- [ ] Lighting four-piece set complete: direction / half-face / highlight points / wide aperture blur (character frames)
- [ ] Cinematic five-piece signature block: composition + palette + DP + film + anti-AI seal
- [ ] Three-place repetition: core constraint appears once each in subject line + CONSTRAINTS + Avoid
- [ ] No text, no watermark, no extra people, no extra fingers
- [ ] Subject clear of the frame edges by 10%

### 5.2 Output QC (every shot)

- [ ] Consistent with first frame: no face change, no clothing change, no light-direction jump
- [ ] Action complies with R3: single primary action, no teleporting, no glitch loops
- [ ] Physics plausible: no floating, no clipping, fabric/hair dynamics natural
- [ ] Landing state correct: the shot ends on its designed end-frame state (keyframe-pair mode) / final frame is an action landing point, no motion blur, usable as next shot's first frame (tail-frame mode)
- [ ] Lip sync roughly matches (strong lip-sync scenes use post-dubbing)
- [ ] Platform safety: no out-of-bounds content, no copyright marks, no real trademarks, combat scenes have violence de-escalation sentences

### 5.3 Full-episode continuous-watch QC (at wrap)

- [ ] Watch all shots continuously: no color/light/position jumps at connections
- [ ] Keyframe-pair seams (if PATH A): shot N's end frame ≈ shot N+1's first frame by design; any seam mismatch flagged and regenerated
- [ ] Emotional curve matches the script line-end labels; hook distribution at least 1 per 3 shots
- [ ] Full-episode character consistency spot check: randomly compare 3 shots against the makeup image
- [ ] Dialogue relationship board aligned: shot-list shots map one-to-one with the 6 cells of assets/dialogue-board-card
- [ ] Shot-list ledger updated: each shot's status (✅locked / 🔄to-fix / ⏳to-produce)

### 5.4 Light-consistency refinement (add to output QC)

- [ ] Each shot's light-source direction consistent with the scene card (sourceless light = flat light, rewrite the light sentence)
- [ ] Subject and environment share the same light (when environment is cold-toned, character must not have sourceless warm light)
- [ ] Contact shadows present (subject touching ground, hand-object contact darkened, no floating feel)
- [ ] Camera logic: move has start/path/closing frame, no wall-clipping, random spinning, drifting

## 6. Continuation Workflow (multi-episode / cross-shot continuous narrative, maps to Phase 5 per-shot loop)

Continuation is not an unrelated new prompt. It must preserve continuity and push the story forward. When the user says "continue / keep writing / continue the previous one / next shot / continue with the previous one's last frame", run this flow.

### 6.1 Continuation judgment (answer three questions before writing)

```
Previous segment's ending state:  (character position / emotional residue / action-complete state)
Next segment's emotional advance: (NOT restart; natural extension from the previous ending)
Continuity notes:                (which of clothing/wound/makeup/props/light direction must not change)
```

### 6.2 Reference-image reuse rules

- Character/scene/prop unchanged → directly reuse the previous segment's reference images, **do NOT re-describe** the full appearance; only restate the identity/clothing/scene/prop anchors needed for stability.
- New character / costume change / scene change / new key prop → give **a fresh compact description + new reference-image prompt**.
- Precise posture/action continuity → use the previous segment's last frame; general connection → use a natural bridge of "different shot scale/angle + matching action", don't force-paste the last frame.

### 6.3 Emotion advances, does not restart

Whatever emotion the previous segment ended on, the next segment must **advance** rather than replay: shock → denial/action/numbness/anger/collapse; joy → savoring/testing/unease. Forbid repeating the same discovery / the same reaction. Each 15s segment adds only ONE main event or emotional turn.

### 6.4 Continuous-short-film mode (maintained when producing multiple segments)

Maintain an internal character bible and scene continuity sheet; carry a compact version with each segment's output so the user can stay consistent when generating continuously.

## 7. Card-Pull Control & Iteration Discipline (maps to Phase 6)

- **Minimal change**: feedback touches only the relevant lines; everything else stays verbatim. Unnecessary changes make the parts the user liked run away together.
- **Diagnose before changing**: first judge "which line of the previous version wasn't controlled, which avoidance was missed"; prioritize strengthening positive anchors, don't blindly pile negative words.
- **Directional rejection needs a redo**: when style/composition/subject is overturned as a whole, don't patch the old version; return to Phase 2/3 to re-imagine.
- **Max 3 reruns per shot**: after 3 failures → downgrade plan (split shot / change shot scale / keyframe-insert supplementary narrative), and mark the change in the shot list.
- **Rerun-failure root-cause checklist** (in priority): ① reference images missing/conflicting (deleting style words can worsen collapse → swap reference images) → ② multiple actions stacked (R3) → ③ camera overdone (lower one notch) → ④ resolution insufficient (upscale to 2K/4K) → ⑤ color written in only one place (three-place repetition).
