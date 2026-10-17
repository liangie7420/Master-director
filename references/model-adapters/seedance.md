# Seedance Adapter

Audit: 2026-10-17. Prepared profile: seedance-2.0-ark, model doubao-seedance-2-0-260128. Consumer Jimeng and other Seedance versions need separate profiles.

## Documented behavior used here

Ark Seedance 2.0 supports text/image video generation, first/last-frame input, multimodal reference, video editing/extension and native audio. Its duration range and input limits live in [profiles.json](profiles.json); do not inherit these into 1.0 or 2.5.

Choose task wording:
- Reference: identify which image/video/audio supplies identity, movement, scene or voice.
- Edit: explicitly edit the source video; specify changes and retained dimensions.
- Extend: extend the actual source video; state the new event and continuity.
The official guide distinguishes these intents, so do not call an edit/extension source merely a reference.

Use numbered image/video/audio references with real uploaded bindings. Technical start/end-frame roles are distinct from appearance references.
Use ordered action beats in this profile; do not promise per-second adherence.
Both Chinese and English are supported; language preference must be evaluated for the actual workload.

## Preparation example

~~~bash
python scripts/prepare_shot.py shot.json --profile seedance-2.0-ark --out prepared.json
~~~

Draft fixtures without actual references use --draft and remain unready for generation.

## Sources

- [2.0 model and tasks](https://docs.volcengine.com/docs/ark/seedance-2-0?lang=en)
- [Official prompt guide](https://docs.volcengine.com/docs/ark/seedance-2-0-prompt-guide?lang=zh)
- [API parameters and version differences](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh)

No live model evaluation has been performed for this repository's revised prompts.
