# Shot Language / 镜头设计参考

Use vocabulary to describe a directorial choice. It is not a list of words every prompt must contain.

## 1. Shot scale

| Scale | Useful information |
|---|---|
| Extreme long / long | Place, geography, isolation, relation to environment |
| Medium / medium close | Blocking, hand/prop interaction, social distance |
| Close / extreme close | A selected reaction, clue, texture or detail |

Choose the scale that makes the shot's evidence readable. Emotional intensity alone does not determine distance.
Natural-language terms and familiar abbreviations are both usable; map special controls through the selected model's adapter.

## 2. Camera motion

| Choice | Directorial question |
|---|---|
| Static | Can behavior or composition carry the change? |
| Push / pull | Does changing distance reveal or withhold information? |
| Pan / tilt | Which subject, path or new information motivates the move? |
| Track / follow | What spatial relation should remain readable during movement? |
| Orbit | Does changing viewpoint serve a reveal or relationship? |
| Handheld | Is a human-operated source style intended? |

Define useful start/end framing, subject of the move and speed/amplitude when they matter.
Complexity is a risk to test, not a fixed count of allowed moves. A move should not compete with the shot's critical event.

## 3. Lens and depth

Wide views can emphasize spatial relationships and perspective; longer-lens looks can isolate subjects or compress apparent space.
Focus depth follows the information needed: a clue in the background may require deep focus; a reaction may benefit from separation.
Optical terms are aesthetic instructions unless an actual camera/render parameter controls them.
Do not require 85mm, blur, lens flare or grain by scene category.

## 4. Position and angle

Describe frame-relative and world-relative positions where useful, with a visible scale reference for height/distance.
For a floating object, specify the visible gap and contact/shadow situation if needed.
Choose a high/low/eye-level viewpoint for the information and power relation of this shot; no angle is universally forbidden.

## 5. Dialogue axis

Define subject locations, facing and gaze targets in world space. Map screen direction for each planned camera.
Keep shot/reverse-shot relations readable. When deliberately crossing the axis, provide a reorientation cue.
A relationship board is optional support for complex staging; its grid layout does not dictate every shot's screen positions.

## 6. Rhythm and performance

Set duration from the event, line and edit, within version/entry limits.
A shot may contain anticipation, change and aftermath, or just one immediate reaction. Use only the beats it needs.
Consecutive shots may share scale when dramatically useful. A large scale change may be an intentional reveal.
Performance amplitude follows medium, character and scene: stylized animation can use stronger shapes; restrained action can still belong in animation.
Express relationships through observable position, timing, gaze, ownership and response rather than a permanent “strong = still / weak = moving” formula.

### Start and end state

Record the action/contact/position at the boundaries. The end may be complete, interrupted or still moving according to the cut.
A reused end frame needs image-input suitability; a normal editorial cut does not require a frozen landing.

### Gaze and groups

For each important subject, identify who or what they look at and where that target is.
Group blocking can use foreground/midground/background descriptions or a diagram when it improves readability.
If actual generations repeatedly miss gaze, test stronger binding, a clearer pose or a different camera. Triple repetition is optional and must earn its place.

## 7. Editorial cut and generation method

Choose the cut for storytelling; choose the generation method for the desired shot and model support.
Extension, keyframe pairs, previous-frame input and a fresh reference-based frame are alternatives with different dependencies.
Use references/continuity-playbook.md for their checks.

## 8. Risks to test

Fine contact plus fast camera movement, crowded identities, large viewpoint changes and readable text can be difficult.
Record the specific risk and acceptance evidence. Test the actual target model rather than banning these combinations universally.
If a shot fails, compare simpler staging, different references or another task mode; preserve the failure record and change one relevant factor.
