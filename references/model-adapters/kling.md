# Kling (Kuaishou) Adapter Manual

> Target: Kling 1.6 / 2.0 / 2.1 | Updated: 2026-08 | Basis: official docs + community testing
> Use case: when target model = Kling, Phase 4 per-shot prompts are assembled per this file's structure formula (general skeleton in video-prompt-framework.md).

## 1. Capability-Boundary Quick Table

| Capability | Parameter | Notes |
|---|---|---|
| Single-segment duration | 5s / 10s (2.x supports longer experimental tiers) | comic-drama single shot recommended 5–8s |
| Aspect ratio | 9:16 / 16:9 / 1:1 | vertical short drama 9:16 |
| First/last frame | supports first-frame, last-frame, both | **last-frame continuation usable**; multi-image reference supported (count varies by version) |
| Motion amplitude | low/medium/high three tiers adjustable | limb/face close-ups use low-medium; action scenes medium; **default low is more stable** |
| Prompt language | Chinese-friendly | formulaic paragraphs beat prose |
| Image-to-video | supported, reference-image stickiness strong | character consistency better than pure text-to-video |
| Text rendering | weak | same as before: blurry character stream replacement |
| Audio | none | post dubbing |

## 2. Prompt Structure Formula (official recommendation: subject first)

```
【Subject】who + appearance anchors (verbatim from character card)
【Motion】primary action + motion-amplitude word (slight/slowly/uniform) + direction
【Scene】environment anchors + spatial layers + light
【Camera】shot scale + camera move + angle
【Style & Texture】style-anchor block
【Negative】concentrated on the end line
```

Key point: Kling is sensitive to "motion amplitude" — writing the clear "slight/obvious" tier is more effective than stacking action words; Chinese with clear word spacing and comma-segmented sentences beats long sentences.

## 3. Camera & Action Vocabulary (words that test well in practice)

- Camera moves: fixed camera / extremely-slow push-in / slow push-in / lateral track / follow / orbit (Kling orbit is more stable, but the ≤90° principle stays)
- Amplitude words: slight / slowly / uniform / obvious ("violent/fast" are high-risk)
- Actions: clear subject + verb + amplitude ("she slowly turns her head, amplitude slight"); multi-person actions MUST state order
- Expressions: Kling's face-following is strong; close-ups get "eye change + mouth-corner micro-movement" level detail; forbid whole-face exaggerated expressions

## 4. First/Last-Frame Connection in Practice

1. Extract last frame → image-to-video first frame; first sentence writes "starting from the first frame, continue character pose and lighting".
2. First/last-frame dual-end mode: fits "character from pose A to pose B" complete action shots; both ends must be action-landing frames (not motion-blur frames).
3. Consistency tip: Kling has strong "reference-image stickiness"; continuous shots of the same character keep referencing the same makeup image — face stays even across scene changes.
4. Known pitfalls: vertical first frame gets cropped top/bottom; a half-bystander/half-prop in the first frame gets continued and amplified; clean the composition first.

## 5. Common Failures & Avoidance

| Symptom | Root Cause | Avoidance Wording |
|---|---|---|
| Character deformation | high motion amplitude + complex action | lower amplitude to "low", split action into detail (first...then...), reduce people in frame |
| Plastic face | realistic style lacks texture words | add "delicate skin texture, real pore texture, cinematic grain" |
| Motion amplitude insufficient | amplitude word missing | explicitly write "obvious" or "larger amplitude" (when needed) |
| Loop feel | no camera movement | even fixed camera writes character micro-motion (breathing rise-fall, gaze movement) |
| Multi-person face swap | frame overload | reduce people in frame, split shot/reverse-shot, over-shoulder occlusion |
| Background drift | insufficient scene anchors | scene card verbatim restatement + establishing-image reference |

## 6. Card-Pull Cost Control

- Start motion amplitude at "low" by default — highest pass rate; upgrade to "medium" only if needed; don't jump to high.
- Reuse the same reference-image chain (makeup + scene + last frame) across the whole episode; rewrite only the action section, reducing variables.
- On failure, first check whether "amplitude word vs action complexity" matches: complex action MUST pair with low amplitude + slow speed.
- Rerun ≤3 times; after 3 failures → split shot / lower scale / keyframe-insert supplementary narrative (continuity-playbook Chapter 4 matrix).

## 7. Full Examples (original content)

Dialogue close-up (last-frame continuation):
```
【Subject】She: long hair in a low bun, dark-green cheongsam, a pearl stud earring (same as makeup image CH-01);
【Motion】She slowly raises her eyes, amplitude slight, eyelashes trembling once, gaze falling toward off-frame lower-right;
【Scene】late-night study, one desk lamp, warm-yellow glow, rain streaks slanting on the glass outside (same as scene card SC-02);
【Camera】close shot, 85mm feel, shallow DoF, fixed camera;
【Style】cinematic realism, warm low-saturation, delicate skin texture, natural film grain;
【Negative】no facial deformation, no clothing change, no watermark or text, no extra people.
```

Action shot (keyframe insert · new character):
```
【Subject】He: short neat hair, dark-gray trench coat (makeup image CH-03), starting from the first-frame image;
【Motion】He abruptly sidesteps to dodge, amplitude obvious but motion smooth, coat hem flaring with the turn;
【Scene】abandoned warehouse, one beam of top light slanting in, dust floating in the light column (scene card SC-04);
【Camera】medium shot, side-tracking camera, 28mm wide feel; opening he faces away from camera, closing his profile enters frame;
【Style】cel-shaded animation texture, high-contrast lighting, cold-blue primary tone;
【Negative】no limb deformation, no clothing clipping, no extra people, no text or watermarks.
```
