# Image Prompt Engine / 图像提示词设计

Use for asset creation, shot first frames, designed end frames and image edits. Select one task before assembling text. Detailed asset records stay in the project; send only the fields needed by this image.

## 1. Establish the image's job

| Task | Primary decision | What to leave out |
|---|---|---|
| Character/prop asset | Which identity or design features must be easy to inspect? | Story action that obscures those features |
| Scene asset | Which layout, entrances, light sources and depth relationships must be reusable? | Unnecessary portrait blur |
| Shot first frame | Where are the subjects, what do they see, what can begin naturally from this pose? | The entire future action sequence |
| Designed end frame | What exact visible state should the action reach? | Instructions to animate time in a still image |
| Edit | What changes, and which source dimensions are retained? | A complete redesign of untouched dimensions |

New assets can be generated from text. Require references only when the task promises to preserve an existing identity/design or edit an existing image.

## 2. Design before writing

Record the shot's information change, visible evidence, attention target and composition.
Choose a layout that makes the evidence legible: a hand withholding a letter may need both the hand and face visible; an environment reveal may need deep focus.
Choose surface treatment for the medium: cel shapes and line weight for 2D; material/shading for 3D; photographic texture for live action.

## 3. Assemble by relevance

1. Subject/design and target state.
2. Composition, blocking, gaze and depth needed to read the state.
3. Reference roles, when actually supplied.
4. Light/color/material choices that serve the medium and scene.
5. The few identity or structural constraints that are critical for this image.
6. Optional exclusions supported by the target model and tied to an observed failure.

Do not enforce half-face light, shallow depth of field, skin pores, film stock or a cinematographer credit on every frame. They are selectable aesthetic tools.
Hex codes describe desired colors, not guaranteed pixel-exact output. Exact palette compliance requires observing the image.

## 4. Reference bindings

Assign every uploaded asset an ID and responsibilities: identity, scene, prop, style or target pose.
A composite reference may cover several explicitly named dimensions. If references disagree about one dimension, choose a source of truth before generation.
Text role declarations guide interpretation; inspect the output for unwanted pose/background/style leakage.

Example structure, filled only with available references:

~~~text
Image 1 supplies the character identity and coat design.
Image 2 supplies the room layout and window position.
[Target state and composition]
[Medium-specific line/shading/light/material description]
[Critical preserve/change instructions]
[Optional task-specific exclusions]
~~~

Keep immutable anchor wording in the source cards. Repeat in model text only the distinguishing features not already adequately supplied by the input or needed to correct a demonstrated failure.
Three-place repetition and negative-last-line placement are hypotheses to compare, not global requirements.

## 5. Style-conditioned choices

| Medium | Useful controls | Common incompatibility to review |
|---|---|---|
| 2D comic/animation | line thickness, shape language, shadow grouping, palette, controlled expression | Generic exclusions of anime/cartoon; compulsory pores/photographic grain |
| 3D animation | proportions, material response, shading, stylized lighting, pose readability | Unrequested photoreal face treatment or 2D line work |
| Live action | motivated lighting, tonal separation, material texture, lens/depth if relevant | A portrait preset obscuring story-critical space |
| Ink/painterly/stop motion | medium-specific marks, paper/material, edge behavior | Generic anti-CGI/anti-animation exclusions that contradict the target |

Use a reference look to clarify observable properties. Optional photographer/film references do not replace an explicit design decision.

## 6. Acceptance and iteration

Inspect identity, count, composition, gaze, contact, material and intended medium in the actual image.
Change one failing dimension at a time; broad changes to style or staging may require a fresh frame.
A local text checker cannot decide whether an image is beautiful or whether a face matches a reference.
