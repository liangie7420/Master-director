# Seedance (Jimeng) Adapter Manual

> Target: Seedance 1.0 Pro / 2.0 (ByteDance Jimeng) | Updated: 2026-08 | Basis: official docs + community testing
> Use case: when target model = Seedance, Phase 4 per-shot prompts are assembled per this file's structure formula (general skeleton in video-prompt-framework.md).

## 1. Capability-Boundary Quick Table

| Capability | Parameter | Notes |
|---|---|---|
| Single-segment duration | 5s / 10s | comic-drama single shot recommended 6–8s (10s tier has slightly higher card-pull risk) |
| Aspect ratio | 9:16 / 16:9 / 1:1 / 4:3 etc. | vertical short drama uses 9:16 |
| First/last frame | supports first-frame, last-frame, both | **last-frame continuation core mechanism usable**: fill the previous shot's last frame in image-to-video |
| Multi-image reference | 1.0 single image; 1.3 Pro/2.0 multi-image | keyframe insert can use "makeup image + last frame" dual images |
| Camera directives | supports natural-language camera descriptions (push/pull/pan/track/follow/orbit) | write directly in Chinese, more stable than English camera words |
| Prompt language | Chinese-friendly | segmented Chinese long sentences beat stacked keywords |
| Text rendering | weak | when readable text is required in script, use post-production; prompt writes "blurred glowing character stream" |
| Audio | none | dialogue/sound effects dubbed in post |

## 2. Prompt Structure Formula (order with highest output-success rate)

```
【Subject & Anchors】who + appearance/clothing (verbatim from character card)
【Action】ONE primary action (preparation→process→landing, R3) + at most two micro-expressions
【Scene & Space】where + spatial layers (foreground/midground/background) + prop anchors
【Camera】shot scale + camera move + focal-length feel + opening→closing frame
【Light & Tone】light-source direction + color temperature + lighting method + primary color tone (verbatim from scene card)
【Style】style-anchor block (4–6 phrases)
【Negative】don't... (concentrated on the end line)
```

Key point: Seedance is sensitive to "action continuity"; the primary action MUST clearly state sequence (first X, then Y, finally Z) — not parallel verbs.

## 3. Camera & Action Vocabulary (words that test well in practice)

- Camera moves: extremely-slow push-in / slow push-in / slow pull-back / lateral track / follow / orbit (≤90°) / fixed camera
- Speed modifiers: extremely-slow > slow > uniform ("fast"-type words use sparingly; they easily produce teleporting)
- Actions: write "verb + amplitude + body part" (e.g., "slowly raises her hand, fingertips stopping mid-air"); forbid writing bare emotion words
- Expressions: write "body part + change" ("brow first knots then relaxes"); Seedance has strong facial performance, close-ups can carry more micro-expressions

## 4. First/Last-Frame Connection in Practice

1. Previous shot's output → extract last frame with `scripts/extract_last_frame.py` (take an action-landing frame; if motion blur, `-t 0.2` earlier).
2. Next shot's image-to-video: first-frame image = that last frame; prompt's first sentence writes "frame continues from the first frame; character pose and lighting stay unchanged, then ...".
3. 10s-tier long shots: can use last-frame + first-frame dual-end constraints (first/last-frame mode), the middle process left to the model; fits "sustained action" shots.
4. Known pitfalls: text/watermarks/extra fingers in the first-frame image get amplified; keep a 10% safe margin at the frame edge (9:16 platform UI occlusion).

## 5. Common Failures & Avoidance

| Symptom | Root Cause | Avoidance Wording |
|---|---|---|
| Facial drift | close-up + no reference | reference carries character makeup image; prompt restates facial anchors; lower scale to medium-close-up |
| Action teleporting | multiple parallel actions / fast camera | make primary action unique, slow the camera, write action sequence |
| Glitch loop | zero camera displacement + symmetric action | add micro-displacement (slow push 5%) or expression change to break symmetry |
| Hand breakdown | hand big close-up + camera move | hand out of frame / fixed camera / change to medium shot, or write "hand lowered, avoid finger close-up" |
| Light jumps | light sentence missing | first section copies the scene card's light sentence (direction + color temp + time) |
| Clothing drift | anchors not restated | restate clothing verbatim; if drifting, promote to form weakness + negative once |
| Garbled text | screen entering frame | unify to "blurred glowing character stream, illegible" |

## 6. Card-Pull Cost Control

- Freeze first: makeup images, scene establishing images, previous shot's last frame all frozen first; this shot leaves only "action" as one variable.
- First shot MUST pass Gate 4 (user confirms prompt style) before batching; output failure first changes prompt structure before rerunning; same-words rerun ≤3 times.
- When 10s-tier failure rate is high, downgrade to 5s tier and split shots; don't force long shots.
- When shooting multiple shots of the same scene continuously, keep reference images consistent; the whole batch can reuse the same first-frame chain, reducing re-pulls.

## 7. Full Examples (original content)

Dialogue close-up (last-frame continuation):
```
【Reference Images】
[Image 1] previous shot's last frame (baseline for continuation);
[Image 2] character makeup image CH-01;

【Prompt】
Frame continues from the first frame; she keeps her sitting pose, fingertips resting at the letter's edge;
then she slowly raises her eyes, eye-tails slightly lifting, gaze passing over the frame toward the front-right;
close-up, 85mm feel shallow DoF, blurred background, fixed camera;
cold-white moonlight from the left window frame is the key light, two-thirds of the face lit, a catchlight in the eyes;
cool gray tone, cinematic realism, fine skin texture;
no facial deformation, no clothing change, no subtitles or watermarks, no extra people.
```

Action shot (keyframe insert · new prop):
```
【Reference Images】
[Image 1] prop establishing frame PR-01 (glowing beacon);
[Image 2] character makeup image CH-02;

【Prompt】
Frame continues from the first frame; the beacon floats two inches above her palm, glowing faint blue;
she slowly closes her five fingers, pausing half a beat when the fingertips touch the beacon's edge, brow lightly knitting;
medium close-up, slight high angle, slow push-in; foreground beacon, background her face;
cold-blue key light from the beacon, lower half of face lit, shadow detail retained in the background;
cel-shaded animation texture, delicate lighting, low-saturation cool tone;
no hand deformation, no beacon clipping, no extra people, no text or watermarks.
```
