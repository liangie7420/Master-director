# Sci-Fi Genre Directing Manual

> Applies to: cyberpunk / near-future / space / post-apocalyptic wasteland / AI-ethics sci-fi short dramas | All content is 100% original, no copyright risk
> Companion docs: when filling the scene card's "color-palette iron rules" field, take keywords from this chapter; for shot design, consult shot-language.md and lighting-styles.md.

## 1. Genre Tone & Emotional-Curve Paradigm

### 1.1 Core Satisfier / Hook Engines

The hook of a sci-fi short drama is NOT its VFX — it is the **cognitive gap (认知差)**: the audience knows rule A, while the protagonist has discovered rule B. That gap between what the viewer believes and what is actually true is what generates the suspense that holds attention. Four main engines, each exploiting that gap from a different direction:

- **Cognitive overturn (认知颠覆)**: The rules of the world get broken — an AI gains self-awareness, memories are rewritten, a time loop closes in on itself.
- **Techno-dread (技术恐惧)**: Technology turns against its creators — a cybernetic limb goes out of control, surveillance systems make autonomous decisions, weapons run amok.
- **Post-apocalyptic survival (末日求生)**: Scarcity forces moral choices — when resources run out, deciding who deserves to be saved is the drama itself.
- **Identity puzzle (身份谜题)**: "Who am I?" — clones, uploaded consciousness, manufactured humans carrying implanted memories.

### 1.2 The 90-Second Single-Episode Emotional-Curve Template (Four Beats)

| Time window | Beat | What the audience gets |
|---|---|---|
| 0–15s | Anomaly injection | One counter-intuitive visual or event (a floating beacon, a light still burning in an abandoned station) → the hook |
| 15–45s | Cause probing | The protagonist tries to explain what she saw, but the clues contradict each other → an information gap |
| 45–75s | Reversal | One cognitive overturn (a rule of the world is toppled) → the high-energy point |
| 75–90s | Escalation | A larger anomaly arrives / the protagonist's identity falls under suspicion → the episode-ending hook |

### 1.3 The Multi-Episode Serial Curve

Each episode runs the same cycle of "anomaly → cause-probing → reversal → escalation." From episode 2 onward, the previous episode's "escalation" becomes this episode's "anomaly," so the episodes chain into one continuous arc. Every 3–4 episodes, deliver one major worldbuilding reveal to refresh the information gap.

## 2. Worldbuilding & Visual Tone

### 2.1 Color-Palette Iron Rules for the Three Sub-Styles (locked for the entire episode — no drifting)

| Style | Primary | Secondary | Accent | Iron rule |
|---|---|---|---|---|
| Cyber neon | #1A1B2E 深靛夜 (Deep Indigo Night) | #0FF2C9 电青 (Electric Cyan) / #FF3D8B 霓虹粉 (Neon Pink) | #FFD166 警示琥珀 (Warning Amber) | Night dominates over day; neon is used ONLY as light sources and reflections, never painted across object surfaces |
| Cold near-future | #2E3440 冷灰 (Cold Gray) | #88C0D0 钢青 (Steel Cyan) / #4C566A 岩灰 (Rock Gray) | #E5E9F0 冷白 (Cold White) | Low saturation; white and gray cover 70% of the frame; highlights appear only on screens and windows |
| Wasteland dusk | #5C4033 锈棕 (Rust Brown) | #8C7A6B 沙尘 (Dusty Sand) / #2F3E46 暗钢 (Dark Steel) | #E8A87C 落日橙 (Sunset Orange) | A pervasive dusty feel; any greenery or vivid color reads as an anomaly signal |

### 2.2 Lighting Signatures

- Cyber neon: key light comes from the neon itself (dual cyan/pink), with reflections off rain-soaked ground; high contrast, shadows leaning blue.
- Near-future: large areas of cold white diffused light (fluorescent overhead) plus a single-point screen glow; shadows are clean and sharp.
- Wasteland: low-angle dusk backlight; dust visible inside light beams; shadows long and soft.

### 2.3 Sci-Fi Texture Keyword Bank (Chinese–English)

| 中文 | English | Use case |
|---|---|---|
| 全息投影，半透明 | holographic projection, translucent | screens / information interfaces |
| 金属拉丝质感 | brushed metal texture | cybernetic limbs / machinery |
| 雨夜霓虹反光 | neon reflections on wet asphalt | cyber night scenes |
| 蒸汽与冷凝 | steam and condensation | industrial / low-temperature settings |
| 故障特效，数据乱码感 | glitch effect | anomalies / hacking |
| 悬浮粒子 | floating particles | atmosphere / energy fields |
| 哑光磨砂材质 | matte frosted material | futuristic furniture / panels |

## 3. Shot-Language Preferences

### 3.1 High-Frequency Shot Reference Table

| Situation | Recommended shot scale / camera move / focal length |
|---|---|
| Revealing something colossal (mega-structure / starship) | Extreme wide + very slow push-in + 24mm wide-angle |
| Hacking / terminal operation | Screen-reflection close-up + locked-off + 85mm |
| Cybernetic limb activation / energy flare | Extreme close-up (arm / eye) + very slow push-in |
| Urban chase | Medium + lateral tracking + 50mm |
| AI vs. human confrontation | Shot/reverse shot + over-the-shoulder + eye level; camera positions strictly on the same side of the axis |
| Post-apocalyptic emptiness | Wide + locked-off long take, 8–10s |
| Glitch / memory flashback | Fast cuts + jump cuts + Dutch angle (one use per shot) |

### 3.2 Shots to Use with Caution — and Their Replacements

- ❌ Holographic screen + orbiting camera move (the on-screen content will always come out as garbled code) → Use a locked-off camera plus a "blurred, glowing" character-stream treatment instead.
- ❌ Mechanical-transformation close-up + fast camera move (parts collapse into broken geometry) → Use a very slow push-in; transform only ONE component at a time.
- ❌ A large-scale space battle in a single shot (the ships always render mushy) → Split it into two shot groups: "distant silhouette of the ship + close-up inside the cockpit."

### 3.3 Pacing Control

- Dialogue / slow-burn scenes 6–8s per shot; action / chase 4–6s per shot; atmospheric empty shots 2–4s (a sci-fi atmosphere shot is a common weapon for the episode-ending hook).
- Inside a single shot, "tech-operation" actions must be broken into fine, sequential steps — raise hand → hover → press down → interface responds; four beats of 0.5–1s each, so the model renders one clean state at a time.

## 4. Performance & Dialogue Style

### 4.1 Action / Micro-Expression Description Templates (directly reusable)

1. Terminal operation: `The fingertip hovers an inch above the screen, hangs for two full seconds, then presses down; the interface lights up the instant the finger lands`.
2. Cybernetic response: `The metal joints of the right arm make a faint click as the fingers tighten one after another`.
3. Holographic interaction: `The light panel reflects in her pupils as she sweeps a finger through the air; data streams flow along the fingertip`.
4. Facing the anomaly: `Her breath skips half a beat; the pupils dilate, then contract, and she forces herself to look away`.
5. Memory flashback: `For an instant her gaze loses focus, as if looking at something beyond the frame, then her lashes flicker sharply once`.
6. Suppressed fear: `Her fingertips dig into her palm; on the surface she stays calm, but her voice is pressed flat and level`.
7. Mechanical acting (AI characters): `Her head-turn carries one frame of stutter, like a read, before she finally responds`.

### 4.2 Dialogue Style (each with an original example line)

- Cold humor (under high tension): "系统说我该休息了。上一个这么说的系统，已经被我断电了。"
- Terminology density (professional credibility): "信标回传的不是坐标——是心跳频率。生物信号，活的。"
- Despairing ellipsis (a dead-end feeling): "你救不了所有人。"（停顿）"但至少……别让他们白死。"

## 5. High-Frequency Scenes & Props Checklist

### 5.1 High-Frequency Scenes (one-line anchors for the scene card)

1. Underground neon alley (rainy night, signs, puddle reflections)
2. Observatory / space-station main control room (curved console, cracked screens, starfield beyond the window)
3. Server room / data center (cold blue light strips, cabinet rows, chilled mist)
4. Laboratory (white walls, incubation pods, single-point cold light)
5. Wasteland highway (rusted car wrecks, dusk, windblown sand)
6. Rooftop helipad (night wind, city lights, drone takeoffs and landings)
7. Cybernetic clinic (shadowless surgical light, instrument tray, an implied smell of disinfectant)
8. AI core chamber (optic cables like veins, a central pillar of light)
9. Abandoned residence (layers of dust, tripped breakers, withered plants)
10. Underground shelter (low ceiling, warm yellow emergency lights, supply racks)

### 5.2 High-Frequency Props (form weakness marked — where AI tends to draw them wrong)

| Prop | Form weakness (AI likely to mess up) |
|---|---|
| Holographic terminal | Text inside the screen → always render as blurred character streams |
| Cybernetic arm | The number of joints and the metal texture |
| Energy beacon | Its glow color must be unique (locked to a HEX value) |
| Pills / genetic reagents | Capsule shape and the bubbles inside the liquid |
| Data card / chip | The gold-finger contact layout |
| Helmet / breathing mask | Mask reflection and the condensation of breath |
| Laser gun | Magazine position and the glowing parts |
| Drone | Number of rotors (twin / quad) |
| Scanner | Scan-beam color and shape |
| Monitor screen | Content on the screen → blur it |

## 6. Genre-Level Failure Points & Negative Constraints

| Failure | Negative phrasing (Chinese–English) |
|---|---|
| Garbled text on holographic screens | 不要可辨认文字 do not show readable text |
| Mechanical structures collapsing | 不要机械关节错位 do not deform mechanical joints |
| "Cyber" read as an all-blue-purple tint | 不要整屏蓝紫滤镜 avoid monochrome blue-purple tint |
| Plastic-looking cybernetic limbs | 不要塑料质感 avoid plastic-like metal |
| Weightlessness continuity error in space | 不要物体悬浮不稳 avoid floating objects |
| "Futuristic" = shiny overload | 不要过度反光金属堆砌 avoid excessive chrome |

## 7. Video-Model Adaptation Notes

- **Seedance**: Cool-toned night scenes are its strong suit; neon rainy-night shots have a high success rate; write action continuity in sequence.
- **Kling**: Static tech scenes (server rooms / labs) hold together well; its default motion amplitude is low.
- **Hailuo**: Stylized looks (a cyber anime feel) adapt well; the 6s preset's tight rhythm suits breaking up chase scenes.
- (Community experience — verify against each model's current version before relying on it.)

## 8. Original Example Excerpt — 《零号信号》(Signal Zero)

> A 90-second single-scene piece: an underground observatory, discovering an anomalous signal. 12 shots, demonstrating last-frame continuation ×2, keyframe insert · new prop ×1, and keyframe insert · new character ×1.

### 【Scene 1】Abandoned Observatory Main Control Room

**Environment**: Polar night; the dome glass is cracked by a third, and moonlight pours in, laying a cold blue light band across the dust on the floor. A ring-shaped main console; half its screens are shattered, only one terminal glowing with a dim green standby light. Foreground: an overturned swivel chair and scattered files; middle ground: the main console; background: the dome and starfield. Dust motes float in the air. Wind squeezes through the cracks, like a low, hoarse whistle.

---

**[00:00.0 – 00:06.0] Entrance · The Only Light**
`[Extreme wide | very slow push-in | full view of the observatory, a single green light]`
Snow and wind sweep across the crater ridge; the observatory sits riveted onto the cliff edge like a rusted bolt. The camera pushes in slowly from the ridge, passing the cracked dome — deep in the control room, that terminal's dim green standby light blinks on and off in the dark, like breathing.
`[Emotion: Suspense building | Hook: Visual spectacle | Connection: Jump cut (first shot of the episode — use the scene establishing image)]`

---

**[00:06.0 – 00:12.0] Flashlight · Dust**
`[Medium | handheld, slight shake | Shen Zhao squeezes through the door, beam sweeping the console]`
Shen Zhao squeezes sideways into the control room; the shoulder of her cold-weather suit scrapes the door frame, and a flurry of dust lands on her shoulder. Her right hand holds a tactical flashlight; the beam cuts through the dark — dust motes tumble inside the light. When the beam hits the lit terminal, her wrist stops for a moment, and her breath fogs into a white puff inside the mask.
> **沈昭** (voice low, muttering to herself): ……不可能还有电。
`[Emotion: Suspense building | Hook: Behavioral mystery (who is keeping the power on) | Connection: Last-frame continuation]`

---

**[00:12.0 – 00:18.0] Touchscreen · Awakening**
`[Close-up | locked-off | fingertip hovering three inches above the screen]`
She walks to the terminal; her left hand hovers three inches above the screen for two full seconds — the green light reflecting in her pupils. Her lashes tremble; she presses down. The instant her fingertip touches the screen, the standby light dies, the screen goes black for one frame, then explodes into a full-screen character stream. She instinctively leans back half an inch, jaw tightening.
`[Emotion: Discovery | Hook: Information gap (what is on the screen) | Connection: Last-frame continuation]`

---

**[00:18.0 – 00:24.0] Response · Coordinates (new prop debuts)**
`[Extreme close-up | locked-off | the character stream freezes into a single line of coordinates]`
The character stream snaps together and freezes into a line of coordinates; small text below slowly fades in. Shen Zhao's breath stops — the white fog from her mask disperses, and no new one forms. The knuckles of her right hand press against the screen edge; her thumb unconsciously rubs the cracked glass, as if confirming this isn't a hallucination.
(**Keyframe insert · new prop**: the terminal screen debuts as the narrative core → first generate the "screen-coordinates close-up establishing frame" PR-01, freeze it, then use it as the first frame of this shot.)
`[Emotion: Discovery escalating | Hook: Information gap (where do the coordinates point) | Connection: Keyframe insert · new prop PR-01]`

---

**[00:24.0 – 00:30.0] Reading · Blood-Red**
`[Close-up | very slow push-in | the coordinates reflected in her pupils]`
She reads the digits one by one. At the second-to-last one, her brows snap together, her Adam's apple rolls once, and the fingers braced on the screen edge curl tight, knuckles going white.
> **沈昭** (breathy, barely forming words): 这是……观测站自己。
`[Emotion: Crisis approaching | Hook: Relationship mystery (who is calling her) | Connection: Last-frame continuation]`

---

**[00:30.0 – 00:36.0] Wind Stops · Lights On**
`[Medium | locked-off | every shattered screen lights up green at once]`
The wind stops without warning. All the broken screens light up simultaneously; green light falls on her from all sides — she freezes in place, a layer of dust shaken from her shoulders, a dozen green glows reflected in her pupils.
`[2s silence — crisis-arrival type]`
`[Emotion: Crisis arrives | Hook: Episode-end payoff | Connection: Last-frame continuation (carried over as Episode 2's first shot)]`

---

**[00:36.0 – 00:42.0] New Character · Behind the Door (keyframe insert)**
`[Medium | slow pull-back | a shadow appears before the terminal]`
A shadow appears before the terminal — a silhouette standing in the doorway, the hood of the windproof suit pulled low, only a stretch of jawline showing; light from his side throws a layer of shadow across Shen Zhao's face. He says nothing; his fingertip taps the door frame twice, the metallic clink crisp.
(**Keyframe insert · new character**: before the mysterious man's face is ever shown → first generate the "doorway-silhouette makeup keyframe" CH-02, freeze it, then use it as the first frame of this shot.)
> **神秘人** (voice calm, like reading a manual): 坐标是我发的。你该走了。
`[Emotion: Reversal | Hook: Identity puzzle | Connection: Keyframe insert · new character CH-02]`

---

**[00:42.0 – 00:48.0] Standoff · Light Beam**
`[Shot/reverse shot | locked-off | she looks at him, he looks at her]`
Shen Zhao turns, flashlight beam straight into his face — under the hood is a young face, an old scar across the left brow; his eyes squint against the light but he doesn't flinch. Her gun stays lowered, but her thumb has already moved to the safety.
> **沈昭**: 信号三十年前就断了。你是谁。
> **神秘人** (squinting, not backing away): 三十年前……它才刚醒。
`[Emotion: Tug-of-war | Hook: Cognitive overturn ("it" = the terminal) | Connection: Last-frame continuation]`

---

**[00:48.0 – 00:56.0] Sound Surge · Full Screen**
`[Medium | handheld, slight shake | the text on every green screen begins scrolling in sync]`
Both fall silent. The characters on all the cracked screens begin scrolling in unison, the rhythm gradually unifying — like a dozen mouths chanting the same line. Shen Zhao's flashlight beam starts to tremble — not her hand; the voltage is shaking.
`[Emotion: Crisis escalating | Hook: Information gap | Connection: Last-frame continuation]`

---

**[00:56.0 – 01:04.0] Subtitle · One Sentence**
`[Extreme close-up | very slow push-in | the characters freeze into a single sentence]`
The scrolling stops abruptly. All the screens freeze on the same sentence, green light hanging in the dark like a line of warning. Shen Zhao reads it twice; her breathing inside the mask turns rapid.
`[Emotion: Cognitive overturn | Hook: Relationship mystery | Connection: Last-frame continuation]`

---

**[01:04.0 – 01:12.0] Truth · Identity**
`[Close-up | slow push-in | the sentence reflected in her pupils]`
What the screen shows is her number — the experiment-subject number of a project abandoned thirty years ago. She pulls off her right glove; on the inside of her wrist is the same string of characters, old and new ink, identical.
> **沈昭** (voice gone dry): ……这不是观测站。是我。
`[Emotion: Identity puzzle solved | Hook: Cognitive overturn | Connection: Last-frame continuation]`

---

**[01:12.0 – 01:20.0] Closing · The First Human Voice**
`[Medium | slow pull-back | the mysterious man steps over the threshold, light stretching behind him]`
The mysterious man steps over the threshold into the green light, pulling the zipper of the windproof suit slowly down halfway — the same string of characters across his collarbone, old and new ink, identical. For the first time he looks directly at her.
> **神秘人**: 编号 07。……我是你的副本。
`[2s silence — cognitive-overload type]`
`[Emotion: Episode-ending hook | Hook: Identity puzzle deepened | Connection: Last-frame continuation (Episode 2's first shot)]`

---

### Prompt-ification Demonstration for This Excerpt (3 shots)

**Shot 5 (Reading · Blood-Red, last-frame continuation)**:
```
【Reference images】[Fig.1] Previous shot's tail frame (screen coordinates frozen); [Fig.2] Character design sheet CH-01;
【Prompt】The frame continues from the first frame; the screen's cold green coordinates light her face; she reads the coordinates digit by digit,
brows snapping together at the second-to-last digit, Adam's apple rolling, the fingers braced on the screen edge curling until the knuckles go white;
close-up, 85mm feel, very slow push-in, single fixed light source = the screen's cold green glow;
cold gray-green palette, cinematic realism, fine skin texture, a glint of screen reflection in the eyes;
no facial distortion, no readable text, no extra people, no watermark.
```

**Shot 7 (New character debuts, keyframe insert)**:
```
【Reference images】[Fig.1] Doorway-silhouette makeup keyframe CH-02; [Fig.2] Scene establishing image SC-01;
【Prompt】The frame continues from the first frame; a silhouette stands in the doorway, hood of the windproof suit pulled low,
only a stretch of jawline showing; his fingertip taps the door frame twice, the metallic clink crisp;
medium shot, slow pull-back, door frame in the foreground, him in the middle ground, the green terminal in the background;
top light from behind, face under the hood's shadow, a thread of cold light along the jawline;
cold gray-green palette, suspenseful cinematic texture, shallow depth of field;
no facial blur or distortion, no extra people, no readable text, no watermark.
```

**Shot 12 (Identity reveal, last-frame continuation)**:
```
【Reference images】[Fig.1] Previous shot's tail frame (she removes her glove); [Fig.2] Character design sheet CH-01;
【Prompt】The frame continues from the first frame; she removes her glove, revealing the characters on the inside of her wrist;
he steps over the threshold into the green light, zipper pulled halfway down, the same characters on his collarbone, the two locking eyes;
medium shot, slow pull-back, the green light brightening, his shadow stretching behind him;
key light = the screens' green glow, a warm windproof lamp as distant fill light, a subtle warm-cold collision;
cinematic realism, cool tone, light grain;
no facial distortion, no costume drift, no readable text, no watermark.
```
