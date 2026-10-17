# Continuity Playbook / 连续性与生成方式

Track identity, world space, action/contact, sound and editorial continuity separately. A valid cut can change framing or location; only declared invariants must carry over.

## 1. Select the connection by its purpose

| Method | Useful when | Required real input |
|---|---|---|
| Video extension | Continue time/action from an accepted clip | Accepted clip or provider interaction ID |
| Keyframe pair | Control both ends of a shot | Compatible first/end images |
| Tail-frame carry | Start the next event from an extracted observed state | Actual previous clip's usable extracted frame |
| Fresh frame/reference generation | Change framing, angle, scene or establish a new state | Approved identity/layout references as needed |
| Editorial cut | Change viewpoint or time while preserving story clarity | Adjacent clips and an explicit cut intention |

There is no universal ranking. Model support, intended editing, reference quality and observed results decide.
Distinguish generation independence from editorial compatibility: independently generated pairs still need seam/identity checks.

## 1.5 Video-extension SOP

Choose only when the named version/entry supports it and continuation serves the shot.
1. Review the previous clip and record its observed ending state.
2. Supply the actual clip/interaction and request the next event.
3. Preserve the needed identity/space/contact; specify intentional changes.
4. Inspect the join and update the observed ledger.
Do not substitute a portrait or a textual description for a required prior output.

## 2. Tail-frame input

Use scripts/extract_last_frame.py with ffmpeg/ffprobe. If a frame is blurred, inspect an earlier extraction with --offset.
Check the extracted image exists and is readable before using it.
Record its actual pose, gaze, contacts and light; write the next event from that state.
Dependent extraction/generation is sequential. Extraction failure leaves the dependency unresolved; choose a separately designed new shot only as an explicit production change.

### 2.2 Landing state

Design the ending for the cut: completed action, held reaction, interrupted gesture or continuing motion may all be valid.
A frame reused as a new image input must be readable and compatible with the next task.
Do not freeze every shot solely for extraction convenience.

## 2.5 Keyframe pairs

Design both states and check that subject position, geometry, identity and motion admit a plausible path.
Generate/review the real images before interpolation. Keep actual first/last bindings distinct from identity references.
Describe the intermediate event and critical end state. Check the actual clip reaches it.
Independent pairs can be prepared together; check continuity against adjacent actual clips before accepting an episode.

## 3. New assets and changed states

Create and approve new identity/design assets before promising to preserve them.
A new prop or character may need a dedicated establishing shot when its design/story role is unreadable in the narrative shot; an insert is not automatic.
A composite reference may supply several dimensions. Observe leakage of pose, background or camera instead of assuming an exclusivity sentence eliminates it.

## 4. Diagnose the evidence

Run scripts/diagnose.py to retrieve candidate causes, then compare those candidates with the actual prompt, sources, settings and output.
A symptom can come from asset ambiguity, direction, binding, unsupported control, model limitation or a stochastic failure.
Keep the failed result; record the visible failure and its time/frame. Do not claim a hardcoded diagnostic table proves a root cause.

### 4.1 Change scope

- Local correction: change one relevant factor and retain the source/result lineage.
- Broad direction change: redesign the affected frame/shot and invalidate its dependents.
- Choose by the actual failed requirement, not a universal count of changed words.
- Stop when the configured attempt/cost limit is reached; record unresolved evidence and the next production option.

## 5. Review actual output

### 5.1 Frame checks
Identity, count, medium/style, framing, gaze, contact, source consistency and design legibility.

### 5.2 Clip checks
Core event completed; identity retained; space/contact coherent; camera serves direction; acting/sound match the plan; intended landing/cut works.
Every acceptance needs an observed frame/time and a reason. Input/lint pass is a separate field.

### 5.3 Sequence checks
Watch accepted clips in sequence. Look for broken action, ownership, orientation, light, sound and pacing. Intentional changes should remain understandable.
See [evaluation](evaluation.md) for trial records and costs.

## 6. Continuing a project

### 6.1 Restore before the next shot
Record: previous observed ending state; next information/emotional advance; invariants and intentional changes.
Read approved assets and actual outputs relevant to those records.
A planned end_state is not an observation.

## 7. Iteration budget
Set attempt and cost limits for the actual task. Change a diagnosed factor between comparisons.
When input correctness is established but output quality remains poor, consider different references, staging, task mode or a shorter event. Record which alternative was tested; do not automatically slow every action or return to asset generation.
