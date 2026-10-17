# Shot List / 分镜表

Create direction before model wording. A row can link to assets/shot-spec-template.json for executable input checks.

| Shot | Story change / visible evidence | Focus and framing | Action | Start → end state | Duration | Editorial cut | Generation task / version | Actual input | Critical acceptance event | Risk / mitigation | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | She offers evidence but cannot let go: palm remains on envelope | Face and palm both readable | Push envelope to table center and stop | Envelope before her → center, still under palm | 6s | Reaction cut next | image_to_video / configured profile | Approved first frame | Palm remains in contact at the landing | Contact — inspect clip | planned |

## Fill rules
- Specify an information/emotional change and its visible evidence; a transition/environment shot can convey spatial or temporal information.
- Treat a coherent causal event as the unit. Several verbs do not automatically require separate shots.
- Record pose, location, gaze, prop owner/contact and light only where relevant. Use stable state keys for continuity checks.
- Separate an editorial cut (reaction, match, scene change, deliberate jump, etc.) from a model generation task.
- Task: text_to_video / image_to_video / keyframe_pair / multimodal_reference / video_edit / video_extend.
- First/end-frame image generation is a separate preparation task when needed.
- Choose extension, pairs or tail-frame input by the intended connection and model support. No universal priority.
- A designed end state can be a completed gesture, an interrupted action or ongoing motion when the planned edit needs it. A tail-frame extraction candidate must be usable for the actual next task.
- Duration follows the event, delivery and exact model/version limits. Do not force every shot into 4–10 seconds.
- Every risk flag records a real concern or “none identified”; a lexical hint is not an automatic ban.

## Before generation
Check total episode timing, asset/version availability, task support, input dependencies and critical acceptance events.
Check only declared continuity invariants; intentionally changed position/angle/time is recorded as such.
Update intended states to actual observed states after reviewing the output.
