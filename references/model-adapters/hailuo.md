# MiniMax / Hailuo Adapter

Audit: 2026-10-17. MiniMax is the provider; Hailuo/海螺 is the video family. Keep exact versions separate.

## Profiles and tasks

- minimax-hailuo-2.3: MiniMax-Hailuo-2.3 text and first-frame image generation.
- minimax-hailuo-02: MiniMax-Hailuo-02 additionally has a documented first/last-frame endpoint.
- The first/last-frame API currently lists Hailuo-02 only. Do not infer support for 2.3 from the shared provider.
- Video duration is coupled to resolution. The 02 first/last-frame task also excludes 512P; see preparation checks.
- Native sound, editing and extension are unverified by the sources used here. Keep sound in post-production unless the chosen entry is confirmed.

## Prompt organization

Choose one coherent event and explicit subject binding. In image-to-video, the first-frame parameter supplies appearance/composition; describe the changes and final state.
The official API supports bracketed camera commands for these named versions. Use the actual command vocabulary if that level of control is needed; ordinary camera description remains available.
Respect the documented 2000-character prompt limit; do not pad to a target length.
Record prompt_optimizer and other actual generation settings during comparisons so platform rewriting does not confound the experiment.

## Sources

- [Text-to-video](https://platform.minimax.io/docs/api-reference/video-generation-t2v)
- [Image-to-video](https://platform.minimax.io/docs/api-reference/video-generation-i2v)
- [First/last-frame tasks](https://platform.minimax.io/docs/api-reference/video-generation-fl2v)

No live model evaluation has been performed for this repository's revised prompts.
