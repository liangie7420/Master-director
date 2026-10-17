---
name: manju-director
description: "Create or revise AI comic-drama and short-drama production packages: scripts, asset cards, storyboards, task-specific image/video prompts, continuity plans and shot evaluation. Use for episode production or an established project's next shot. Repository maintenance and prompt-system experiments use the improvement loop, without starting a new drama's approval gates."
---

# Manju Director / 漫剧导演

Turn a source text or theme into an editable production package. Design what the viewer learns, then the visible behavior and composition, then the model input. Conversation and scripts use Simplified Chinese; model-text language follows the user and measured results for the selected model. Keep original dialogue and names.

## Invariants

- Use original material or adapt user-provided material within its authorized scope.
- Keep approved asset identities and explicit continuity states consistent. Changes invalidate only the dependent shots; record those dependencies.
- Bind each input asset to its actual role. A composite image may provide several declared dimensions; do not assert that text can remove all influence from other dimensions.
- Every shot needs an intent, visible evidence, attention target, start/end state and acceptance event. Detail serves these decisions.
- Separate editorial notes from model text. Do not send the entire project bible to every generation.
- A lexical warning is a review hint. Missing assets, impossible timelines and documented capability mismatches are input errors. Neither local pass nor successful generation proves video quality.
- Respect the user's existing authorization and budget. Dependent outputs run sequentially; independent shots may be prepared together. Never fabricate images, model calls, approvals or observed evidence.

## Choose the mode

**Full production:** run phases 0–6 below. Confirm creative decisions at the gates unless the user already authorized that scope. Preserve existing approvals; revisions resume at the first affected phase.

**Continue/revise an existing shot:** restore its approved cards, previous observed state and change request. Reopen only affected decisions.

**Maintain/improve this workflow:** follow [the improvement loop](references/agent-loop.md). Local fixtures are experiments, not a new production; production gates do not block code, document or test maintenance.

## Production phases

| Phase | Work and deliverable | Read |
|---|---|---|
| 0 · Setup | Genre, visual medium, platform + exact model/version/entry, ratio, duration, language, available assets and budget. Record unresolved choices. | [model selection](references/model-adapters/README.md) |
| 1 · Script | Script with information change, visible evidence, behavior and sound plan. Gate 1: approve story and asset needs. | [script format](references/script-format.md), relevant genre only |
| 2 · Assets | Bible, character/scene/prop cards and needed reference images. Gate 2: approve identities and style. New asset creation may be text-only. | [image engine](references/image-prompt-engine.md), relevant assets/ templates |
| 3 · Shots | Intent, focus, blocking, camera, start/end states, editorial cut, generation task and risks. Gate 3: approve shot plan. A relationship board is useful for difficult spatial scenes, not compulsory for every conversation. | [shot language](references/shot-language.md), [shot table](assets/shotlist-template.md), [shot specification](references/shot-spec.md) |
| 4 · Model inputs | Prepare the exact task with real asset bindings and a version profile. Gate 4: approve the first representative shot's direction. Produce only the image/video blocks the selected task requires. | [video framework](references/video-prompt-framework.md), selected adapter |
| 5 · Generate | Check tool availability and budget, submit through the actual platform, preserve input/settings/job ID. Gate 5: accept the first result before a dependent production batch. | [continuity playbook](references/continuity-playbook.md) |
| 6 · Evaluate | Compare actual output to per-shot criteria and continuity states, update ledger. Review the episode in sequence. | [evaluation](references/evaluation.md) |

Do not freeze a state merely because it was planned. Record whether it is intended, generated or visually accepted.

## Per-shot loop

1. Restore approved assets, prior observed state and this shot's intent.
2. Select the generation task by the desired edit/connection and verified model support.
3. Write the shot specification; choose only details that carry story, identity or style.
4. Run structured input checks and review lexical hints.
5. Generate within the available authorization/budget; save the result and settings.
6. Evaluate the actual clip with concrete evidence.
7. Diagnose failure, change one relevant factor and compare again.
8. Accept, revise, change production method or stop at the configured attempt/cost limit.

A deliberate cut can change angle, scale or scene. Extension, keyframe pairs and tail-frame carry have different purposes; none is a universal production priority. Tail-frame dependencies must use the actual preceding accepted output.

## Tools

Resolve the skill directory from the SKILL.md path supplied by the host. Tool paths below are relative to that directory, not the user's creative project. Run scripts by their absolute installed path, pass project inputs explicitly, and save outputs in the creative project. Do not write production outputs into the installed skill folder.

For first use, see [installation](docs/INSTALL.md) and the [60-second authored example](examples/last-letter/README.md). Use scripts/prepare_example.py with an explicit new output directory to inspect a complete production package without model calls. The built-in example is illustrative and does not imply approved/generated assets.

- `python scripts/prepare_shot.py shot.json --profile <version-key> --out prepared.json`
  checks declared input constraints and prepares task-specific text. It does not call a model or translate prose.
- `--draft` permits planned assets/unverified capabilities for review; never treat its output as submission-ready.
- `python scripts/check_prompt.py --file prompt.txt --task image_to_video`
  lints model text. `--strict` additionally rejects warnings; that is a local policy, not a quality guarantee.
- `python scripts/diagnose.py "<symptom>"` lists candidate causes; verify them against actual output.
- `python scripts/extract_last_frame.py clip.mp4 --shot 1`
  extracts a fallback connection asset; requires ffmpeg/ffprobe.
- `python scripts/run_benchmark.py --out benchmarks/results/local`
  reproduces the local experiment matrix without model calls.

## Load references only when needed

- [Lighting and texture](references/lighting-styles.md): optional choices suited to the visual medium.
- [Continuity](references/continuity-playbook.md): generation dependencies, observed state and editing.
- [Model profiles](references/model-adapters/profiles.json): documented version/entry constraints; null means unverified.
- [Evaluation](references/evaluation.md): repeat trials, inspect failures and record limitations.
- Genre guides: `references/genres/{sci-fi,xuanhuan,urban,romance,campus}.md`. Use relevant narrative guidance; filter visual suggestions by the selected medium.
- Templates: [bible](assets/episode-bible.md), [character](assets/character-card.md), [scene](assets/scene-card.md), [prop](assets/prop-card.md), [composite](assets/scene-actor-card.md), [dialogue board](assets/dialogue-board-card.md).

## Delivery

Save long scripts, asset records and shot specifications as project files. Present ready model text in a copyable block, with actual upload bindings adjacent to it. Report local checks, generation status and visual acceptance separately. If no generator is connected, deliver the prepared experiment and state that video quality remains unverified.
