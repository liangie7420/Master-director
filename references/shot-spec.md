# Shot Specification / 镜头说明

Use assets/shot-spec-template.json as an editable starting point. scripts/prepare_shot.py checks and projects an authored specification; it does not create directorial decisions or translate text.

## Required fields

- id, task: stable shot ID and an explicit generation task.
- intent: internal note on the viewer's information/emotional change.
- visible_evidence: what must actually be visible to express that intent.
- focus: starting attention target and its transfer.
- action: coherent event; an image task uses the chosen start/end state instead.
- style: medium and observable rendering choices.
- start_state / end_state: non-empty maps from stable state key to a concrete description.
- camera.description: composition/move needed for the shot.
- duration_seconds: video generation length; image tasks omit it.

Optional fields: lighting, lighting_changes, must/prefer/avoid string lists, beats, audio, resolution and assets.
prompt_language selects zh/en boilerplate (default zh); author the prose in that language. This choice does not translate existing fields or assert that one language performs better.
All prose should already be in the desired prompt language. Internal intent/focus notes are saved in the report, not blindly sent to the video model.

## Asset binding

Each asset has id, kind (image/video/audio), role, source and optional description.
Roles: first_frame, last_frame, identity, scene, prop, style, motion, base_video, voice, music.
Use local paths relative to the specification file. An empty/missing source is a planning placeholder and passes only in --draft mode.
Remote URLs remain unverified until access/upload is checked; this offline tool does not fetch them.
One strict first-frame task uses exactly one frame. A strict keyframe-pair task uses exactly first + last; use the selected model's multimodal mode for additional references.

## Declared continuity

preserve lists state keys to compare with --previous <shot.json>.
The previous end_state and next start_state must match on those keys. Omitted keys may change intentionally.
This validates declared records, not what actually appears in a generated clip. After visual review, update the actual observed state and source result IDs before a dependent generation.

## Preparation

~~~bash
python scripts/prepare_shot.py shot.json --profile seedance-2.0-ark --draft --out prepared.json
~~~

Remove --draft after references and version limits are actually ready. The report contains model text, binding manifest, parameters, editorial notes, checks and generation_status=not_run.
submission_ready denotes only the implemented local input checks; upload/codec/access/provider-specific request validation remain separate.
