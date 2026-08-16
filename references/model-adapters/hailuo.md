# Hailuo (MiniMax Video) Adapter Manual

> Target: Hailuo 01 / 02 (MiniMax) | Updated: 2026-08 | Basis: official docs + community testing
> Use case: when target model = Hailuo, Phase 4 per-shot prompts are assembled per this file's structure formula (general skeleton in video-prompt-framework.md).

## 1. Capability-Boundary Quick Table

| Capability | Parameter | Notes |
|---|---|---|
| Single-segment duration | 6s (mainstream tier; some scenes support longer) | comic-drama single shot recommended 4–6s; pacing tighter than the other two models |
| Aspect ratio | 9:16 / 16:9 / 1:1 | vertical short drama 9:16 |
| First/last frame | supports first-frame, last-frame (version differences; verify multi-image by testing) | **last-frame continuation usable**; multi-image reference verify per version |
| Camera directives | supports explicit camera directives (e.g., [push-in] [orbit] style markers) | Chinese natural language also works |
| Prompt language | **English preferred** (Chinese-friendly fallback) | segmented prompts respond best; keep Chinese ONLY for dialogue lines / character names / lock sentences |
| Stylization | strong (anime/ink-wash/realistic all fine) | a model with high fit for comic-drama art styles |
| Text rendering | weak | same as before: blurry character stream replacement |
| Audio | none | post dubbing |

## 2. Prompt Structure Formula (segmented responses work best)

```
【Scene】environment anchors + time + spatial layers
【Subject】who + appearance anchors (verbatim from character card)
【Action】primary action + micro-expression + motion amplitude
【Camera】shot scale + camera move + angle + opening/closing frame
【Light】light-source direction + color temperature + lighting method
【Style】style-anchor block
【Negative】concentrated on the end line
```

Key point: Hailuo responds directly to "camera-directive" words — to push in, write "camera slow push-in", not just "push toward". Within a 6s shot, place only ONE action loop (start→land); there's no room for two beats.

## 3. Camera & Action Vocabulary (words that test well in practice)

- Camera moves: static / slow push-in / slow pull-back / lateral track / orbit (Hailuo orbit is more stable; still ≤90°) / follow
- Camera-directive writing: `camera slow push-in, from full shot to close shot` (state the starting shot scale → ending shot scale)
- Actions: `subject + action + speed + ending state` ("she turns, slowly, stopping at the door")
- Expressions: write "first...then..." micro-expression sequences ("first startled, then lips pressing to suppress it"); Hailuo has good facial-emotion sequence feel

## 4. First/Last-Frame Connection in Practice

1. Extract last frame → image-to-video first frame; first sentence writes "continue the first-frame image, character pose unchanged, then ...".
2. 6s-tier rhythm: Establish(0–1s) → Develop(1–4s) → Close(4–6s); the closing frame deliberately lands as an action point (for the next shot's last-frame continuation).
3. Dual images (last frame + makeup): verify per version; if unsupported, downgrade: first-frame image holds only the last frame, makeup anchors restated in text.
4. Known pitfalls: character too small in the first-frame composition → model enlarges the background and ignores the performance; keep the character ≥30% of the frame before feeding.

## 5. Common Failures & Avoidance

| Symptom | Root Cause | Avoidance Wording |
|---|---|---|
| Performance ignored | subject occupies small share / action buried in long sentences | make action its own segment, enlarge the first-frame character, camera approaches first |
| Camera move ineffective | used "push toward" instead of "slow push-in" | use explicit camera-directive words (see Section 3) |
| Stiff expression | only emotion words | write "body-part + change sequence", add catchlight |
| Hard transitions | multiple beats crammed in one shot | 6s holds one action loop; split the extras into new shots |
| Style drift | insufficient style anchors | anchor block 4–6 phrases restated verbatim; strong stylization is both the strength and the loss-of-control point |
| First-frame contamination | edge debris | clean frame edges 10%, write "no extra objects in frame" |

## 6. Card-Pull Cost Control

- Split 6s shots finer: a 90s episode ≈ 15–20 shots; don't compress shot count to keep duration.
- Hailuo's strong stylization → the style-anchor block is the film's biggest "drift variable"; once finalized and frozen, every shot reuses it verbatim.
- On failure, first change "action complexity" (fewer beats) and "camera speed" (lower one notch); touch reference images only after.
- Rerun ≤3 times; if still failing → split shot / change scale (continuity-playbook matrix).

## 7. Full Examples (original content, English prompt + Chinese dialogue)

Dialogue close-up (last-frame continuation):
```
[Scene] rainy night rooftop, distant city lights blurred, cold-blue night (scene card SC-05);
[Subject] She: shoulder-length hair, white shirt, sleeves rolled to the forearm (makeup image CH-04), continuing the first-frame sitting pose;
[Action] She slowly grips the railing, knuckles going white, then tilts her head back, closes her eyes, raindrops landing on her lashes; she whispers, "……别再来了。" (breathy);
[Camera] close shot, 85mm feel, shallow DoF, fixed camera;
[Light] city cold-blue ambient light, a faint billboard warm glow on one side of her face, a catchlight in her eyes;
[Style] cinematic realism, low-saturation cool tone, visible rain streaks, fine grain;
[Negative] no facial deformation, no clothing change, no text or watermarks, no extra people.
```

Action shot (keyframe insert · new prop):
```
[Scene] dim archive room, ceiling lamp beam, dust floating (scene card SC-06);
[Subject] He: black-rimmed glasses, dark coat (makeup image CH-05), the envelope continuing from the first-frame image;
[Action] He opens the envelope, pulls out the photo, motion slowing, gaze fixing on the photo, brow first knitting then relaxing;
[Camera] medium close-up, camera slow push-in, from shoulder to face; opening the envelope at frame center, closing his eyes;
[Light] top light primary, face retaining shadow, a thin highlight on the envelope edge;
[Style] suspense-film texture, cool gray tone, shallow DoF, cinematic grain;
[Negative] no hand deformation, no readable text (photo content blurred), no extra people, no watermarks.
```
