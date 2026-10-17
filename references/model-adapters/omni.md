# Google Gemini Omni Adapter

Audit: 2026-10-17. Omni is a separate family from Veo.

## Current prepared profile

google-omni-1.1-flash identifies gemini-omni-1.1-flash.
Official material documents text/image/reference-to-video, video editing, and 1.1 scene extension and first/last-frame control.
The registry leaves per-task duration/resolution limits unconfigured until checked against the chosen API/app entry. Consequently this profile currently produces drafts; it does not silently reuse Veo limits.

## Task-specific direction

- Generation: describe the event and roles of available references.
- Edit: identify the source video/interaction, one change and important retained dimensions.
- Extension: continue the actual previous interaction; a textual Video 1 label alone is not an API request.
- First/last frames: bind the actual keyframes through the entry's controls and describe the motion between them.
- Conversational iteration: record the source interaction ID and the exact delta for every version.

Use natural language. The compiler preserves authored language; it is not a translator or a provider SDK.
Do not assume voice-reference input means every possible native-audio output control is available.

## Sources

- [Model family](https://deepmind.google/models/gemini-omni/)
- [Official prompt guide](https://deepmind.google/models/gemini-omni/prompt-guide/)
- [Omni 1.1 controls and API example](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/)

No live model evaluation has been performed for this repository's revised prompts.
