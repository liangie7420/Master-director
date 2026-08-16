# Lighting & Focal-Length Style Library (reference for Phase 2 makeup/establishing and Phase 3 shot design)

> A photographic-perspective lighting & focal-length system, translated into executable prompt language for AI video/image models. Every entry can be written directly into the lighting line of first-frame image / video prompts.
>
> v2 added on top of v1: "lighting four-piece set, three-DP tone table, two development chains, word-deletion regulator, long-distance dialogue eye-line lock".

---

## 1. Character-Frame Lighting Four-Piece Set (EVERY character frame MUST include)

**Iron rule**: the 【lighting】line of character frames (close-up/medium/over-shoulder/full body/two-person/two-person multi-panel) must nail down **4 pieces**:

1. **Where the light comes from** (MUST state a direction: `from camera-right / 45° left` etc.)
2. **Half-face light** (which half bright, which half in shadow + add `warm shadow, not crushed black` to the dark side)
3. **Highlight points** (specific positions: `highlights on cheekbone, nose bridge, lips, collarbone`)
4. **Wide aperture blur** (`shallow DoF / wide aperture / background heavily out of focus`)

**Missing any one = flat light + clear background = looks like a costume photo, not a film frame**.

**Plain one-sentence template** (copy & adapt directly):
```
Warm light from camera-right. Right half of her face brightly lit, left half in warm shadow.
Highlights on cheekbone, nose bridge, lips, collarbone. Shallow DoF, wide aperture,
background heavily out of focus.
```

**Exceptions**: four-view makeup (studio neutral backdrop), color card, gray-background material → not needed (product-level images). **Any character + real scene background requires wide aperture blur**.

**Lighting + blur section total ≤ 80 words**; trim if over.

## 2. Three-DP Tone Table (writing one DP name ≈ dozens of lighting/composition/color directives)

| DP Credit | Tones It Produces |
|---|---|
| **Greig Fraser** (Dune 2021) | warm sand gold-brown, fire-lit interiors, low-contrast soft diffused light, "sun-baked by the desert" texture |
| **Roger Deakins** | minimal, cold, epic loneliness, large negative space, hard light ratios, restrained color |
| **Hoyte van Hoytema** | large-format IMAX texture, cold-blue night scenes, color depth retained in shadows |

The three names **can be stacked** as a "tone recipe". DP credit must be self-consistent with film/format style (writing Deakins cold/minimal → don't stack high-saturation HDR; writing Fraser desert → don't stack fresh blue sky).

**Pitfall**: prefer "DP + recognized masterpiece + time" (more stable than a bare name); `analog grain` pairs with `Avoid: heavy digital grain`.

## 3. Two Development Chains (copy directly)

```
// Color day/night development chain (low saturation high contrast, skip-bleach desolate hard tone)
35mm Kodak Vision3 500T film stock with skip-bleach negative LUT,
analog photochemical grain, single still frame from a feature film.

// B&W martial-arts development chain (real B&W film-base grayscale)
Kodak Double-X 5222 black-and-white film stock aesthetic. Anamorphic widescreen lens.
Subtle organic film grain only. Colors restrained, slight gray tone.
```

**B&W films still use a color card + write grayscale hierarchy** (prevent muddy layers): "red→medium dark gray, black stays deep, white stays bright".

## 4. Word-Deletion Regulator (clean/bright vs dark/oppressive)

Tone is a foundational decision; **decide first, then generate**. Prompts aren't just "what to add", but "what to delete".

**Clean/bright tone** (blue sky/transparent/urban):
- **DELETE**: `Dune aesthetic / skip-bleach LUT / analog grain / dusty haze / HDR glow`
- **ADD**: `bright clean fresh daylight + clear/soft light-blue sky + white clouds + high clarity + shallow DoF`
- Cold effects rely on teal-orange complement (warm background vs cold effects); blue sky not over-saturated (`not over-saturated`).

**Dark/oppressive tone** (sand dust/cold/wasteland):
- **KEEP**: `Dune aesthetic + Kodak Vision3 500T + skip-bleach + analog grain + dusty haze + desaturated`
- Entire signature follows this tone, no mixing.

**Pitfall**: skip-bleach desaturation eats accent colors together; accent colors need `sole saturated / glowing` explicit elevation.

## 5. Classic Lighting Methods (write into makeup images and character shots' "lighting line")

| Method | Light Effect | Fits | Prompt Wording |
|---|---|---|---|
| Three-point | key+fill+rim, clean & dimensional | default safe, commercial feel | `three-point lighting, key 45° side-above` |
| Rembrandt | triangular light patch on one side of face, dimensional & mysterious | male characters, power-play, oppressive scenes | `Rembrandt lighting, triangular light zone on one side of face` |
| Butterfly | butterfly shadow under the eyes, soft & refined | female characters, seductive scenes, fashion | `butterfly lighting, soft high frontal light` |
| Side light | 90° strong contrast, dramatic | suspense, confrontation, hard-edged portraits | `90° side light, half-lit half-shadow` |
| Rim/back light | bright edge line outlining, separates background | backlit silhouette, highlight moments, ambiguous scenes | `backlit rim light, gold edge on hair and shoulder line` |
| Catchlight | highlight point in pupils, aliveness | MUST write in every portrait shot! | `a catchlight in the eyes` |

**Priority**: every portrait shot (incl. makeup, close-up) writes catchlight; male power scenes prefer Rembrandt, female allure scenes prefer butterfly; when unsure, use three-point.

## 6. Time-of-Day Lighting (reference for scene card's "time & weather" field)

| Period | Light Character | Prompt Wording | Fits |
|---|---|---|---|
| Golden hour | 1h before sunset, warm orange raking light, long shadows | `golden hour, warm orange side-backlight, long shadows` | romance, farewell, highlight, warmth |
| Blue hour | 20–30 min after sunset, cold blue + warm light contrast | `blue hour, cold blue sky clashing with warm window light` | urban night, loneliness, suspense, sci-fi |
| Noon hard light | top light, high contrast | `noon top light, high-contrast hard shadows` | modern architecture, sun oppression, western feel |
| Overcast diffuse | even soft, no shadow | `overcast diffuse light, soft and shadowless` | art-house, daily life, oppressive flat |

**Key vs fill clause** (scene card MUST include): write the key light direction + fill source & color temperature + time or environment — none may be missing.

## 7. Focal-Length Psychology (reference for camera line's "focal-length feel")

| Focal Feel | Visual Effect | Prompt Wording | Use |
|---|---|---|---|
| Wide 24–35mm | perspective stretch, environment pulled in | `24mm wide feel, near large far small` | establishing, pressure, action, interior space |
| Standard 50mm | near human eye, no distortion | `50mm feel` | dialogue default |
| Medium 85mm | good facial proportions, beautiful blur | `85mm feel, shallow DoF` | portrait close-up, emotional scenes (portrait golden focal length) |
| Telephoto 135mm+ | spatial compression, background peeled away | `135mm telephoto feel, compressed background` | emotional close-up, ambiguous scenes, tracking feel |

**Focal discipline**: emotional scenes 85/135mm feel; establishing & action 24–35mm feel; dialogue 50mm feel. Always write "feel" (感), avoiding the model interpreting real lens parameters.

## 8. Skin-Tone & Material Adaptation (for character makeup)

| Skin/Material Type | Lighting Key | Prompt Wording |
|---|---|---|
| Dark skin | soft light + fill, avoid hard shadows swallowing detail | `soft key light with fill, avoid hard shadows` |
| Light skin | side light enhances contour, avoid overexposure | `side light sculpting contours, prevent overexposure` |
| Special fabrics (silk/metal) | precise light control, clear highlight points | `silk fabric, single highlight point, even sheen` |

## 9. Product/Prop Lighting (for prop establishing frames)

| Prop Type | Lighting Plan | Prompt Wording |
|---|---|---|
| Luxury/keepsake | single light + reflector precision control, dark background | `single soft key light, dark gradient background, precise specular highlights` |
| Tech/artifact | black background + edge light, cold colors | `black background, cold edge light outlining, tech feel` |
| Food/lifestyle | top light + soft fill | `top warm light with soft fill, natural sheen` |
| Transparent/glass/crystal | backlight + edge light | `backlit transmission plus edge light, translucent refraction` |

## 10. Region/Style Lighting Signatures (optional quick-matching across genres)

| Style | Lighting Signature | Prompt Wording |
|---|---|---|
| Chinese mood | low-saturation Morandi, negative space | `low-saturation Morandi palette, compositional negative space, oriental mood` |
| Japanese minimal | large window light, clean | `large window light, clean and soft, Japanese minimal` |
| Hollywood epic | backlight + fog, grand depth | `backlit fog world, layered depth, epic feel` |
| European vintage | cool gray, painterly light | `cool gray tone, soft painterly light` |
| Middle-Eastern elegant | gold + deep blue, symmetrical geometry | `golden warm light contrasting deep blue, symmetrical composition` |
| American street | high contrast vivid, night neon | `high contrast, neon color blocks, street texture` |

## 11. Long-Distance Dialogue Eye-Line Lock (dialogue reinforcement)

Long-distance dialogue frames (across-room confrontation / across-table) once beyond "arm's length" lose control; the model draws both people looking down in thought (seemingly looking but not).

**Reinforcement three-piece set** (replicated in 【body】+【CONSTRAINTS】+【Avoid】):
1. **Positive**: `eyelines MEET across the room, both heads slightly LIFTED to look at each other`
2. **Avoid section** excludes the "looking-down-in-thought" family item by item: `looking down at the table / heads bowed / eyes lowered / each lost in their own thoughts / averted gaze`
3. **Pure profile → 3/4 turn toward the other**; `head TURNED toward the other person, chin slightly LIFTED`

**Scope**: all dialogue shots. Pair with `assets/dialogue-board-card.md` (6-cell 2×3 relationship board).
