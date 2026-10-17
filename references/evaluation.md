# Evaluation / 输入验证与真实效果验证

## Local input checks

Validate task, supported version/entry, asset IDs/roles/files, parameter compatibility, beat boundaries and declared continuity.
Text linting can suggest ambiguity and complexity; it cannot decide aesthetics, acting, identity similarity or actual model adherence.

## Fixed experiment cases

benchmarks/shots/ contains six authored cases: dialogue, two-person blocking, hand-object contact, movement, emotional reveal and continuation.
The baseline manifest preserves original lint output and file hashes. It is a static baseline, not historical generated video.
Legacy prompt files are reconstructed from the old template with the same authored fields and clearly labelled as such.

## Real trial record

For each variant, preserve model/version/entry, exact prompt and hash, actual source media hashes, parameters, optimizer settings, seed when supported, trial ID, result URI/file, latency and charged cost.
Use the same inputs/settings and multiple trials per variant. Do not assume a seed guarantees determinism or compares across providers.
Keep trial order/labels blinded when practical. Decide acceptance events before viewing results.

## Review

Score or explicitly mark not-applicable:
- core_event: the intended visible event occurred;
- identity: distinguishing features and costume persist;
- spatial_contact: position, gaze, ownership and contact are coherent;
- continuity: the planned cut/connection works against actual adjacent outputs;
- performance: timing and behavior express the intended turn;
- aesthetics: medium/style/composition support the shot;
- adherence: critical constraints are followed.

Every score needs an observed time/frame and a short reason. Empty scores mean unreviewed, never zero or passed.
A clip with a failed critical event is unusable regardless of its average aesthetic score.
Usable-output cost = total charged cost / number of accepted clips; do not report this without actual costs and acceptance.

## Adoption decision

Adopt a change only within the tested model/task boundary when repeat evidence supports its purpose and critical regressions are absent.
Otherwise retain it as a hypothesis, revise or roll back.
Never promote a fictional trial, a local lint pass or a reconstructed baseline to evidence of better video.
