# Video Prompt Framework / 按任务组织视频输入

A shared shot specification supplies intent, visible evidence, focus, blocking, action and start/end states. Model text is a task-specific projection of that specification.

Read the selected version/entry adapter. Chinese and English are selectable; preserve original dialogue. No universal language, character-count target or mandatory negative paragraph is assumed.

## 1. Choose the task

| Task | Model input should emphasize |
|---|---|
| text_to_video | Subject + initial space + medium/style + event + camera + end state |
| image_to_video | Supplied first frame + changes over time + camera + required end state |
| keyframe_pair | First/end frame binding + plausible intermediate trajectory and timing |
| multimodal_reference | Each asset's responsibility + explicit subject binding + scene/event/camera |
| video_edit | Source clip + exact change, its time/location + preserved dimensions |
| video_extend | Actual preceding clip/interaction + new event + required continuity |

Keep aspect ratio, output duration, resolution and other API options in the actual parameter fields when available. A written “4K” does not set output resolution.

## 2. Author the shot

Before compiling the model text, fill:

- **Intent:** what the viewer learns or feels differently.
- **Visible evidence:** behavior/composition that makes the intent observable.
- **Focus:** where attention begins and where it goes.
- **Start/end state:** position, facing, gaze, ownership/contact, action progress and light as needed.
- **Action:** a coherent event, including causal substeps where they matter.
- **Camera:** justified composition or move; a static camera is a complete choice.
- **Priority:** must realize / preferred refinement / task-specific exclusions.
- **Acceptance:** what evidence would make this clip usable.

An event can include several verbs or several subjects. Split when independent narrative events cannot be read or controlled within the chosen duration; do not split based on a word count.

## 3. Task-specific examples

**Image to video:** use the input frame for existing appearance and layout. Describe the new behavior and essential preserve constraints. Avoid copying the full character/scene cards by default.

**Reference to video:** distinguish identity reference from first-frame constraint. A portrait is not automatically the desired opening composition.

**First/last frame:** verify both images describe a physically compatible path. State the motion needed between them and inspect the landing.

**Editing:** describe only the intended changes plus important preserve constraints. Keep each iteration linked to the actual source clip or interaction.

**Extension:** continue the actual accepted output, not a remembered shot description or a portrait. If the platform requires an interaction/job ID, record that ID.

## 4. Time, performance and sound

Use the chosen model's documented timing syntax. Ordered beats are the conservative fallback; precise timestamps in the specification are scheduling intent and do not guarantee exact generated timing.
Allocate time by the action and line, not a fixed establish/develop/climax/close recipe for every shot.
Estimate dialogue length, then validate by reading/recording it; speech-rate heuristics do not prove fit.

Choose sound delivery explicitly:
- native: include speech, sound and timing only when that version supports them;
- post: retain the sound plan for editing, without promising model-generated speech;
- none: omit unneeded sound prose.

Micro-expression details should make a specific performance readable. Do not mandate two expressions, throat movement or fingertip detail on every shot.
Focus hunting, exposure fluctuation and rolling shutter are optional source-style choices; adding defects is not a universal route to cinematic quality.

## 5. Detail and length

Use the endpoint's documented limits in profiles.json. The compiler reports over-limit text and never silently trims core events.
Start with enough information to specify the event and critical constraints. Add material, light or performance details when they improve the desired shot in repeated tests.
Remove irrelevant descriptions first. No target minimum length or Chinese/English character conversion is treated as an industry benchmark.

## 6. Check and observe

Run structured input validation before generation. Review lexical warnings with subject/time scope.
Then generate and evaluate: event completed, identity retained, spatial logic, action/contact, camera intention, style and cut/connection.
Keep “prepared”, “generated” and “visually accepted” as separate states. See [evaluation](evaluation.md).
