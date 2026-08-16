# First-Frame Image Prompt Engine (MUST READ when writing first-frame image prompts in Phase 4, Refactored v3)

## ⛔ NON-NEGOTIABLE ELEMENTS (every image prompt MUST contain all of these; omitting any = defective prompt)

1. **Subject line with R4 anchor restatement** — restate appearance/color anchors VERBATIM from the asset card; no paraphrasing.
2. **Exclusive declaration for every reference image** — each image states what it serves and what it does NOT provide (one-image-one-job).
3. **Lighting line with the full lighting-sculpting formula** — direction / half-face / highlight points / wide aperture / contact shadow. Character frames missing any piece = flat light = costume-photo look.
4. **CONSTRAINTS section** — shape locks / quantity locks / NO-FACE prohibitions go HERE (not in TONE or Avoid).
5. **Three-place repetition** — the core constraint (form weakness / color iron rule / core negative) appears in subject-or-TONE (positive) + CONSTRAINTS (prohibition) + Avoid (negative).
6. **Negative end line** — concentrated on the LAST line; the positive zone NEVER contains unwanted words.
7. **Five-piece signature block** — composition + hex palette + DP credit + film stock + anti-AI seal, self-consistent.
8. **Word limit** — complex frames ≤500 words; simple frames ≤350 words.

> If a reference image is unavailable for a needed anchor, STOP and tell the user — do not write the prompt without it (skipping = face-swap/drift risk).

> For natural-language image models (Jimeng / Nano Banana / GPT Image, etc. — models WITHOUT a separate negative-prompt field). All control is written into the text itself. This file works with the `assets/character-card.md`, `assets/scene-card.md`, `assets/prop-card.md`, `assets/scene-actor-card.md`, `assets/dialogue-board-card.md` templates.
>
> v2 absorbed "reference-image exclusive declarations, three-place repetition, five-piece signature block, word-deletion regulator, dual register, 5 over-complexity types" on top of v1.
>
> v3 integrated open-source patterns on top of v2: 5 need-anchoring questions, 7-layer frame decomposition, lighting-sculpting formula, contact shadows, focal-length lookup.

## 0. Need-Anchoring (ask five questions before writing)

**A prompt is not an adjective; it is a constraint system.** Bad prompts are like wishing ("generate something premium, cinematic, with good light"); good prompts are like director's blocking (state subject, light, material, action, camera, constraints). Before writing any first-frame image, run the five questions:

| Question | What to Specify |
|---|---|
| Who watches | target audience, aesthetic preference |
| What do they see | subject, person, space, event |
| Why do they watch | pain point, emotion, story hook |
| Where do they watch | platform, ratio, duration, sound environment |
| What should they do after | remember the character, feel the emotion, understand the relationship |

## 1. Six Iron Rules

1. **Line Separation**: Each semantic module on its own line. Fragmented single lines or long stacked strings reduce model control precision.
2. **Negative End Line**: All "don't/forbidden/no" concentrated in the **last line** of the prompt; positive description area **NEVER** contains unwanted words (naming = summoning).
3. **Reference Image Codes**: Use only `Image 1/Image 2` or `image1/image2` in text, NO filenames or paths allowed.
4. **Spatial Anchor Specificity**: Use directions (left/right/foreground/background) + layers (front/middle/distance) + distance references ("close to bottom-right corner of frame" "about one step from subject"), NO vague "nearby/around". **Height uses compositional relationships, NOT metric measurements** ("feet on, in lower half of frame, about 10 meters off ground + maintain eye-level/slight upward angle + NEVER bird's eye view").
5. **Four-Piece Lighting Set** (MUST include for character frames): ① Light source direction (specific direction) ② Half-face lighting (which half bright, which half in shadow) ③ Highlight points (specific positions: cheekbone/nose bridge/lips/collarbone) ④ Wide aperture background blur (background blurred, wide aperture). Any character frame missing one = flat lighting + clear background = costume photo not cinematic frame.
6. **One Image One Focus**: Each first-frame image locks only ONE visual focus (person/prop/spatial relationship), multiple focuses dilute and blur everything.

### 1.1 Lighting-Sculpting Formula (MUST check for character/scene frames' 【PHOTOGRAPHIC TONE】)

Lighting is not a one-word "warm/cold". Write it item by item per the six-variable formula:

```
time & environment + key-light direction + light quality + color temperature + light ratio + reflective medium + shadow type + material response + forbidden lighting errors
```

**Three key judgments**:
1. **Light MUST have a source**: which side the window is on, whether the streetlight is front or side-back, whether candlelight is the sole source or a fill — sourceless light = flat light.
2. **Material MUST respond to light**: metal→thin elongated highlights; glass→transparent reflections; wet ground→mirror reflections; fabric→soft diffuse reflection.
3. **Subject MUST share the environment's light**: when the environment is cold-toned, the character cannot have sourceless warm light; a product on a table MUST have a contact shadow.

**Contact shadow** (high-frequency failure point): there MUST be a real darkening between the subject and the ground, and between the hand and the object — `contact shadow under the subject, feet/object touching surface with real shadow`. No contact shadow = floating/knockout feel.

## 2. One Image One Responsibility + Exclusive Declaration (Anti-Derailment Core)

Each reference image must have **unique responsibility + exclusive declaration**. Reference images are NOT "reference the whole image", but "reference a specific dimension".

**Negative Example** (Will fail):
```
[Image 1] Character costume image [Image 2] Scene image
```
Model will make up what each controls → face swapping/color derailing.

**Positive Example** (One responsibility + exclusive = what's not mine, I don't ask for):
```
[Image 1] Character costume image —— Only serves as character identity anchor (face/hair/clothing), does not provide scene/composition/lighting
[Image 2] Scene reference image —— Only serves as environment and color palette anchor (building/light/tone), does not provide character identity
[Image 3] Prop reference frame —— Only serves as prop form anchor (structure/sheen/craftsmanship), does not provide scene or characters
```

**Any undistributed dimension, the model will definitely make its own decisions**. Exclusive declarations draw "autonomy boundaries" for the model.

## 3. Six-Section Structure Formula (Output in Order)

> Based on neoimage-prompt-engine's six-section skeleton, **English as the default skeleton (image model's native language), Chinese lock sentences embedded in 【Locks】section; Chinese dialogue lines and character names stay in the original**. Prompts are written in English by default; a Chinese gloss is optional for the user's reading only.

```
【Reference Image Annotations】
Image 1 (Character Reference · <Who>): Anchors ONLY <Who>'s identity (face/hair/clothing), strictly preserved unchanged, provides appearance only NOT pose; this image corresponds to frame area [<Position>].
Image 2 (……): …… (each image one line, each line with "Only serves as..." / "Does not provide..." exclusive declaration)
Image N (Scene Reference): Anchors ONLY the environment, provides background only, NOT characters or color tone.
Image C (Color Palette / Cinematic Tone Reference): Anchors ONLY the overall cinematic tone and color palette (hue/brightness/saturation orientation), NOT characters/composition/specific content.

[Subject] <One sentence defining the frame>: Shot scale/camera angle/perspective + who is doing what where + environment. Position/height use compositional relationships, NOT metric measurements.

[Effects Layer] <What color, what texture, how large the effects are>. Texture uses positive/negative word banks for precision. For multiple characters, write each character's effects separately with explicit color/shape contrast.

【Locks & Constraints】Written in two layers, do NOT mix:
· PRESERVE — Do not change <Who>'s facial features/hair/clothing (<specific>), only change pose to "<new pose>"; face and identity strictly preserved from Image X, no face swapping; for multiple characters add "no face swapping between characters + bind positions".
· CONSTRAINTS — Logic/shape/quantity prohibitions go here (exactly N / maintain mechanical face non-human / wall must be solid). ⚠ Iron rule: shape locks · quantity locks · NO-FACE type logical prohibitions MUST go in CONSTRAINTS, NOT in TONE or Avoid — wrong block weight causes failures.

【PHOTOGRAPHIC TONE】Tone (clean/dark), sky, light, color palette, clarity/texture (clean sharp no noise OR film grain). Character frames MUST include three-dimensionality of light + wide aperture background blur.

【Avoid】Write negative iron rules for the most common failure points in this path: wrong colors, wrong textures, face swapping, whole-image noise, wrong camera angles, cartoon/game feel, text watermarks, etc.

size <ratio>, quality <2K/4K>
```

**Three-Place Repetition Iron Rule**: The same core constraint (character form weakness / color palette iron rule / core negative) MUST be stated in THREE places: 「[Subject] or 【PHOTOGRAPHIC TONE】(positive) + 【Locks & Constraints】CONSTRAINTS section (prohibition) + 【Avoid】(negative)」. **Moderate repetition = attention strengthening**, only one place = derailing.

### 3.1 Seven-Layer Frame Decomposition (skeleton derivation before writing [Subject])

Abstract style must be decomposed into concrete frame layers; write each layer clearly, then merge into one sentence:

| Layer | What to Specify |
|---|---|
| Subject | who is the protagonist: form, proportion, pose, material |
| Environment | where: time, weather, spatial attributes |
| Composition | where the subject sits in the frame: negative space, symmetry, leading lines |
| Foreground | any occlusion: raindrops, door frames, plants, glass |
| Midground | where the subject and key action occur |
| Background | does the background provide emotion, information, or depth |
| Depth | distance and focus relationship between front/mid/back layers |

### 3.2 Focal-Length Lookup Table (choose when writing the camera line)

| Focal Length | Fits |
|---|---|
| 14-24mm wide | environmental pressure, speed, spatial distortion, on-scene feel |
| 35mm | narrative, street, person-environment balance |
| 50mm | near human eye, natural realism |
| 85mm | portrait close-up, emotion, shallow DoF |
| 135mm+ | spatial compression, isolation, voyeuristic feel, strong emotion |

## 4. Cinematic Signature Block Five-Piece Set (Avoid AI Quality)

Lock cinematography signature with "Composition → Color → Who shot → With what → Seal" five-piece set:

```
Composition Style: Cinematic diagonal composition / centered symmetry / over-the-shoulder axis etc.
Hex Color Palette: #xxx (primary) + #xxx (secondary) + #xxx (accent), locked exactly
Cinematographer Credit: Greig Fraser (Dune 2021) / Roger Deakins / Hoyte van Hoytema etc.
Film Stock / Format: 35mm Kodak Vision3 500T / Kodak Double-X 5222 / 6K large format
Anti-AI Quality Seal: the overall PHOTO is clean, NO digital grain; NOT CGI / anime / video-game render
```

Five-piece set must be self-consistent: if writing Deakins cold/minimalist, don't stack high-saturation HDR; if writing Fraiser desert, don't stack fresh blue sky. **Clean/bright tone adjust entire signature per §6 delete negatives**.

**Development Chain Recipes (Directly Copyable)**:
```
// Color Day/Night (low saturation high contrast, skip-bleach hard tone)
35mm Kodak Vision3 500T film stock with skip-bleach negative LUT,
analog photochemical grain, single still frame from a feature film.

// B&W Action (real B&W film base grayscale)
Kodak Double-X 5222 black-and-white film stock aesthetic. Anamorphic widescreen lens.
Subtle organic film grain only. Colors restrained, slight gray tone.
```

**B&W films still use color palette + write grayscale hierarchy** (prevent muddy layers): "red → medium dark gray, black stays deep, white stays bright".

## 5. Reference-Image Discipline (image-to-image section)

### Edit mode (modify an existing image)
- Opening declaration: `Strictly based on the provided reference image (Image 1),`
- Write only the change; do not re-describe the original; MUST have a Keep anchor: `Keep the facial features, hairstyle, and clothing of the person in Image 1 completely unchanged,` (specific to features).
- End-line negative: `do not alter the person themselves, no extra people, no watermark.`
- Fits: Phase 5 failure handling's "light edit without letting the base image drift".

### Reference-extraction mode (take an element to draw a new image)
- Opening declaration: `Only extract [specific element] from reference image (Image 1) (named down to features), and build an entirely new frame,`
- State two lists: what to extract from Image 1 / what to build new (background/composition/light/style).
- Multi-image source naming: `Image 1 provides the character, Image 2 provides the scene style,`
- **Anti-whole-image-copy end line**: `do not copy the original background and composition of the reference image.`
- Fits: Phase 2 character makeup, Phase 5 "last-frame camera-change" when switching angles.

### Last-frame continuation mode (specific to this skill)
- When first frame = previous shot's last frame, no new image needed; if rebuilding due to angle change, handle per "reference-extraction mode": the last frame is Image 1, extract the character's pose and clothing, rebuild the frame under the new camera angle, and write `Keep the pose, clothing, and light direction of the person in Image 1; only change the camera angle.`

## 6. Word Deletion Regulator (Clean/Bright Tone vs Dark/Oppressive Tone)

Tone is a foundational decision, **decide first then generate**. Prompts are not just about "what to add", but also "what to delete".

**Clean/Bright Tone** (Blue sky/transparent/urban):
- **DELETE**: `Dune aesthetic / skip-bleach LUT / analog grain / dusty haze / HDR glow`
- **ADD**: `bright clean fresh daylight + clear/soft light-blue sky + white clouds + high clarity + shallow DoF`
- Cold effects rely on teal-orange complement (warm background vs cold effects); blue sky not over-saturated (`not over-saturated`).

**Dark/Oppressive Tone** (Sand dust/cold/post-apocalyptic):
- **KEEP**: `Dune aesthetic + Kodak Vision3 500T + skip-bleach + analog grain + dusty haze + desaturated`
- Entire signature follows this tone, no mixing.

**Pitfall**: skip-bleach desaturation eats accent colors together; when pairing, accent colors need `sole saturated / glowing` explicit elevation.

## 7. Dual Register (Heavy Build vs Light Edit)

> This is the foundation of the entire system. Wrong register = biggest time sink.

| Task | Model | Prompt |
|---|---|---|
| **Heavy Build** (Character/Scene/Keyframe generation from scratch) | Heavy-duty Image Model (Image type) | Complete six-section prompt |
| **Light Edit** (Fine-tuning one aspect on existing image) | Visual Understanding Model (Nano Pro type) | Single Chinese sentence + "keep everything else unchanged" |

> Practical verification: Let Nano Pro build from scratch, wind effects become thin wisps; let Image 2 build and the momentum is full. So **Build uses Image 2, Edit uses Nano Pro**, working together.

**7 Light Edit Templates** (Chinese one sentence, all with "keep everything else unchanged"):
```
Camera Distance: 把镜头拉远一点，其余不变。
Composition: 把人物挪到左三分之一，其余不变。
Shot Scale: 从全身改成半身特写，其余不变。
Expression: 表情改成眯眼挑眉，其余不变。
Material: 把衣袖材质改成丝绸，结构不变，其余不变。
Remove Element: 去掉丝袜，改成光脚，其余不变。
Replace Element: 把背景换成沙漠（@基底 @风格），其余不变。
```

**Two Rules**:
- Removing elements MUST provide replacement state (remove stockings → "bare feet", don't just say "remove").
- Changes MUST provide physical causation (wet body → "sleeves clinging to skin"), otherwise model "rationalizes" and erases counter-intuitive details.

**When to Light Edit vs Re-Build**:
- Only changing 1 variable, base image basically satisfactory → Light edit (single sentence)
- Changing ≥3 things simultaneously / changing pose / changing structure / changing camera angle / continuous edits start melting face and swapping identity → Stop, go back to heavy-duty complete rebuild

## 8. Five Over-Complexity Types (self-check item by item after writing)

1. **Term stacking vs plain sentence**: for lighting, don't write `★1/3 warm DIRECTIONAL key light at ~45°...★2/3 chiaroscuro...`; write `Warm light from camera-right. Right half lit, left half in warm shadow.`.
2. **"Family"-labeled grouped Avoid vs flat list**: don't write `★(anchor-drift family)★...`; directly list 6-12 core prohibitions flat, no labels.
3. **Big ★★ opening declaration vs one-line point**: don't pile 4-6 lines of `THIS IS X NOT Y` at the opening; compress to one line.
4. **Long disclaimer for every ref vs only for drift-prone ones**: write a long exclusive declaration only for the genuinely drift-prone image; others get one simple sentence.
5. **Full HEX palette stacking vs one color-bible line**: after the first frame sets the color card, later frames only use `warm crimson-gold per established color bible`; don't copy the full HEX table every frame.

**Total word targets**: complex frames ≤ 500 words; simple frames ≤ 350 words. Trim if over.

## 9. High-Risk Feature "MUST APPEAR" SOP (Form Weakness Upgrade)

**Iron Rule**: If a feature failing ruins the entire image (character face/form weakness/quantity/color confrontation), MUST follow this SOP.

1. **Precondition Mark** `if missing the design fails`: Place critical form features in subject line or CONSTRAINTS section.
2. **Anticipate Failure**: Imagine what it most likely fails into (hands → six fingers; magic array → bubbles; monster → cartoon).
3. **Write "Failure Mode → Remedy Sentence"**: One remedy sentence for each failure point.
4. **Post-Generation Checklist**: Check against list item by item.
5. **Re-run with Additional Remedy if Needed**: Don't compromise.

Example (Fantasy Magic Array):
```
Subject Line: [Image 1] Magic array centered, [array pattern=octagonal radial, inner ring three circles, outer ring twelve points, forbidden to draw as continuous concentric circles]
CONSTRAINTS: Array pattern must be octagonal radial, no continuous concentric circles; if failure mode → add remedy sentence "outer ring must be twelve points, odd number not allowed"
Negative End Line: do not deform the rune; do not use circles
```

## 10. Dialogue High-Risk Zone: Long-Distance Eye-Line Lock

Long-distance dialogue frames (across room confrontation/across table) once beyond "arm's length" lose control, model draws both people looking down in thought (seems like looking but actually not).
**Reinforcement Three-Piece Set**:
1. Positive: `eyelines MEET across the room, both heads slightly LIFTED to look at each other`
2. Avoid section excludes "looking down in thought" family item by item: `looking down at the table / heads bowed / eyes lowered / each lost in their own thoughts / averted gaze`
3. Pure profile changed to 3/4 turn toward other person; `head TURNED toward the other person, chin slightly LIFTED`

**Scope**: All dialogue frames, replicated in three places: 【body text】+【CONSTRAINTS】+【Avoid】.

## 11. Iteration Discipline (maps to card-pull control)

- **Minimal change**: feedback touches only the relevant lines; everything else stays verbatim. Unnecessary changes make the parts the user liked run away together.
- **Diagnose before changing**: first judge "which line of the previous version wasn't controlled, which avoidance was missed"; prioritize strengthening positive anchors, don't blindly pile negative words.
- **Directional rejection needs a redo**: when style/composition/subject is overturned as a whole, don't patch the old version; return to Phase 2/3 to re-imagine.
- **Transparent assumptions**: when the user's need is too sparse, fill in a reasonable set of assumptions internally and produce directly; after output, mark the key assumptions in one line.

## 12. API Parameter Suggestions (appendix)

```
【API Parameter Suggestions】
model: <gpt-image-2 / nano-banana-pro / Jimeng>
[edit tasks (change light/partial area on existing image) note: call images.edit, NOT generate]
size: single frame 1K~2K; multi-panel/multi-view/group-blocking images 1536 long edge or 2K+
quality: medium (default); high reserved for final delivery
Thinking Mode: enable for complex composites / multi-constraint / multi-character
Reference images: Image 1 = [role]   Image 2 = [role]   ...
【Reminder】Preset list is core for edits; for 3x3 grids, add at the PRESERVE opening "preserve the multi-panel grid layout and the content of every panel"
```

- Confusing edit vs generate is the "dual-register failure" root cause.
- `output_format`: final images/materials always jpeg; only transparent-background / lossless-layer needs png.
- `size`: single frame 1K–2K; 3x3 grids / multi-view / group blocking MUST be 1536 long edge or 2K+ (otherwise per-cell detail blurs).

## 13. Makeup/Establishing/Prop/Composite-Asset Prompts (linked with assets templates)

- **Character makeup** (character-card.md / scene-actor-card.md): add catchlight + lighting method (Rembrandt for male / butterfly for female preferred) + 85mm feel + form weakness three-place repetition + exclusive declaration.
- **Scene establishing** (scene-card.md): add time-of-day lighting (golden hour / blue hour / overcast diffuse per tone) + lighting method per scene + dual-axis color palette.
- **Prop establishing** (prop-card.md): add product lighting (luxury: single light + reflector precision control / tech: ice-box black background per genre) + form weakness three-place repetition.
- **Composite asset image** (scene-actor-card.md): one image covering character+scene+prop+atmosphere, the most efficient keyframe-insert method.
- **Dialogue relationship board** (dialogue-board-card.md): 6-cell 2×3 locking the 180° axis, required before dialogue scenes.

### 13.1 Selling-Point → Evidence Conversion (MUST check for prop/product/ability establishing)

Writing "powerful/premium/strong" is useless — the model doesn't know what "premium" looks like. Translate abstract selling points into **visible evidence**:

| Selling Point | Visible Evidence |
|---|---|
| Lightweight | fabric swaying gently in wind, wrist not drooping, a feather landing without bending it |
| Waterproof | water beads rolling off, surface not absorbing, wet-ground reflection |
| Premium | material detail, restrained light, real proportions (NOT random gold light effects) |
| Tech | precise structure, smooth interaction, restrained UI (NOT full-screen blue lines) |
| Sharp | thin elongated highlight on the blade, clean cut surfaces, edge reflecting as a line |
| Powerful | cracks in the ground, grip surface depressed under force, clothes lifted by air pressure |

**Product/prop hard constraints**: ① structure must not change ② no random generated text/trademarks ③ hand-object contact must have pressure & shadow ④ proportions must not deform from wide angle or camera move ⑤ selling point must have visible evidence ⑥ don't let the model generate big Chinese characters/signs/incorrect packaging copy.

## 14. Anti-AI-Quality Word Bank (permanent in Avoid)

⚠️ Not in the positive description. Write it as one paragraph appended to the end line.

```
overpolished studio look, plastic smoothing skin, oversaturation of non-red elements,
glossy highlight blowout, generic AI image quality, HDR glow, doll-like skin,
3D rendered look, cartoon / anime / video-game render, mosaic / pixelated artifacts,
text, watermark, logo, signature, multiple characters without intent,
unnamed facial features mixing into subject
```

**Genre-level negatives** (each genre's "failure points" section lists them); name them one by one (e.g., sci-fi: `cyberpunk = blue-purple tint`; costume drama: `studio portrait look`).
