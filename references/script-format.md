# Standard Storyboard Script Format Spec (MUST READ in Phase 1)

> This format is the single source of truth for the entire "script → shot list → prompt" chain. All output fields are backward compatible: every shot in the script maps losslessly to one row of the shot list and one segment of the prompt.

---

## 1. Document Skeleton

```markdown
---
# 《Title》Episode N
> **Aspect ratio**: 9:16 vertical / 16:9 horizontal | **Duration**: approx. XX s | **Scenes**: N
> **Emotional curve**: build-up → tug-of-war → climb → reversal → close (one line, filled per the genre file Chapter 1 template)
> **This episode's hook**: (the suspense left to the audience at the end, one line)
---

### 【Scene 1】Scene name (corresponding scene card SC-##)

**Environment**: (full-element environment description: time / light source & direction / primary color tone / spatial layers i.e. foreground-midground-background / ground & materials / ambient-sound hints. This section is reused by the scene card and the establishing-image prompt; write it to the level where an image can be produced directly.)

---

**[MM:SS.S – MM:SS.S] Beat name**

`[shot scale|camera move|frame key points (≤15 chars)]`

(Body text: prose-style description of action & micro-expression. Iron rule R1: specific to body parts, breathing, fabric, and the physical dynamics of props.)

> **Character name**: (tone/subtext) line text.

`[Emotion: stage emotion | Hook: this shot's suspense type | Connection: last-frame / keyframe-insert-new-character / keyframe-insert-new-prop / jump-cut]`

---

(next shot...)
```

## 2. Field Rules (every one is mandatory)

### 1. Timecodes
- Format `MM:SS.S`, consecutive from 00:00.0; no overlap, no gaps.
- Single shot duration 4–10 seconds (the video model's single-segment capability window); content over 10 seconds MUST be split into more shots.
- Sum of all shot durations = the total duration declared in the header, with zero error.

### 2. Shot-label line `[shot scale|camera move|frame key points]`
- Shot-scale and camera-move words MUST be taken from the lookup tables in `references/shot-language.md`; self-invented words are forbidden (models don't respond to made-up words).
- Frame key points ≤15 characters; write only the core of "who does what where"; details go to the body text.
- Two-person/multi-person shots mark relative positions in the key points (e.g., "Yu left, Xie right") for axis discipline.

### 3. Body text (action & micro-expression) — the soul of this format
- **Action chain**: within one shot, write the primary action as "preparation → process → landing" (iron rule R3: ONE primary action per shot).
- **Micro-expressions**: at least TWO body-part-specific descriptions per shot — eyes (where they look, how long they stay, when they move away), mouth corners, jaw, Adam's apple, brow peak, eyelashes, breathing (a beat heavier / held / slowed), fingers (curling, tapping, rolling, hovering).
- **Physical dynamics**: fabric, hair strands, and props physically responding to the action ("the red skirt trailed off the couch edge" "the tassel swayed with each breath") — these are the seeds for the video model to generate realistic dynamics.
- **Forbidden**: bare abstract emotion words ("she was enchanting"), novel-style inner monologue ("she thought to herself"), off-camera information (settings the audience can't see). Everything must be shootable.

### 4. Dialogue
- Format: `> **Character name**: (tone/subtext) line`; tone describes the voice state (breathy / lowered / a pause); subtext may be omitted but is REQUIRED for ambiguous/confrontational scenes.
- Speech-rate conversion: normal 3–4 chars/second, agitated 4–5 chars/second, heavy/slow 2–3 chars/second; line duration must not exceed shot duration minus 1 second of breathing room.
- Voice-over marked `（画外音）`; monologue marked `（内心独白）` (for dubbing distinction).

### 5. Line-end label `[Emotion | Hook | Connection | Sound]`
- **Emotion**: take from this episode's emotional-curve stage names (build-up / tug-of-war / climb / reversal / close, or the stage words given by the genre file); used for emotional tinting in the shot list and prompts.
- **Hook**: this shot's information-gap type given to the audience — visual spectacle / behavioral mystery / information gap / relationship mystery / crisis approaching / none (transition shot). At least one non-"none" hook per 3 shots.
- **Sound**: this shot's sound cue in ≤8 words — ambient (wind / rain / clock ticking) + music mood (low strings / no music / heartbeat) + any diegetic sound the shot NEEDS (screen beep / footsteps / breath). Written at script time so voice and music stay consistent across shots and episodes (AI video models need the same sound baseline every shot). Example: `wind through glass crack + low strings` / `screen beep + no music` / `breathing + heartbeat`.
- **Connection**: one of six values, decides the next shot's first-frame source:
  - `video extension` (default when the model supports it): this shot's first frame = previous shot's whole output extended (`@视频1`).
  - `keyframe pair`: first frame + designed end frame generated as a keyframe pair; video produced by first-and-last-frame interpolation.
  - `tail-frame carry` (fallback): this shot's first frame = previous shot's output last frame (extracted); only when the model supports neither extension nor 首尾帧.
  - `keyframe insert · new character`: this shot has a new character's first appearance → first produce that character's makeup keyframe; flow in continuity-playbook Chapter 3.
  - `keyframe insert · new prop`: this shot has a key prop's first close-up → first produce the prop establishing frame.
  - `jump cut`: scene/time change → use the scene establishing image as the first frame, not the last frame.

### 6. Silence and pauses
- Silence at emotional overload is acting; write it: `[silence N seconds — type]` (types e.g. emotional-overload / confrontation-pressure / breathing-space), and count it into the duration.

## 3. Original Example (format anchor, 6-shot miniature)

> The following is an original excerpt from 《归航信标》(Homebound Beacon, sci-fi suspense), only a format reference; genre-specific writing style per the corresponding genre file.

---

# 《归航信标》Episode 1 · Excerpt

> **Aspect ratio**: 9:16 vertical | **Duration**: approx. 34 s | **Scenes**: 1 (abandoned observatory main control room)
> **Emotional curve**: suspense build-up → discovery → crisis approaching
> **This episode's hook**: the coordinates the beacon responds with are the protagonist's own position

### 【Scene 1】Abandoned observatory main control room

**Environment**: Polar night. An observatory main control room abandoned for thirty years, a third of the dome glass shattered, moonlight pouring through the crack, casting sharp cold-blue light bands onto the dusty floor. The main console ring-arranged, half the screens cracked, only one terminal glowing a dim green standby light. Foreground: a toppled swivel chair and scattered documents; midground: the main console; background: the dome and starfield. Dust particles float in the air. Only wind squeezes through the crack, like a low whistle.

---

**[00:00.0 – 00:05.0] Entry · The only light**

`[extreme long shot|extremely slow push-in|observatory panorama, one green light in the control room]`

Snow squalls sweep across the ring ridge; the observatory is like a rusted rivet nailed to the cliff edge. The camera slowly pushes in from the ridge, passing the cracked dome — deep in the control room, the terminal's dim green standby light flickers on and off in the darkness, like breathing.

`[Emotion: suspense build-up | Hook: visual spectacle | Connection: jump-cut (this episode's first shot, use scene establishing image) | Sound: wind through glass crack + low strings]`

---

**[00:05.0 – 00:11.0] Flashlight · Dust**

`[medium shot|handheld tracking|Shen Zhao's flashlight sweeps the main console]`

Shen Zhao (scene SC-01, character CH-01) squeezes sideways into the control room; her parka shoulder scrapes the door frame, dust sifting onto her shoulder. She holds a tactical flashlight in her right hand, the beam cutting the darkness — **dust motes churn inside the beam like tiny startled creatures**. When the light sweeps across the lit terminal, **her wrist visibly pauses; her breath condenses into a puff of white fog inside the face mask**.

> **沈昭**: (lowered, to herself) ……不可能还有电。

`[Emotion: suspense build-up | Hook: behavioral mystery (who maintains the power) | Connection: video extension | Sound: footsteps on dust + breath fog + no music]`

---

**[00:11.0 – 00:17.0] Touchscreen · Awakening**

`[close-up|micro push-in|fingertip hovering three inches above the screen]`

She walks to the terminal. **Her left hand hovers three inches above the screen; the fingertip stays suspended for a full two seconds** — the gray-green standby light reflected in her pupils. **Her eyelashes tremble once; she finally lands her finger**. The instant the fingertip touches the screen, the standby light dies, the screen goes black for a frame, then bursts into a full-screen stream of characters. **She instinctively leans back half an inch, jaw tensing**.

`[Emotion: discovery | Hook: information gap (screen content) | Connection: last-frame continuation]`

---

**[00:17.0 – 00:23.0] Response · Coordinates (new prop debuts)**

`[big close-up|static|screen characters freeze into one line of coordinates]`

The character stream suddenly contracts, freezing into one line of coordinates, with a line of small text slowly emerging below. **Shen Zhao's breath stops** — the fog on the mask disperses, and no new fog comes. She raises her right hand, **knuckles pressing against the screen edge, her thumb unconsciously rubbing the cracked glass edge**, as if confirming this is not an illusion.

(**Keyframe insert · new prop**: the terminal screen debuts as the narrative-core prop → first produce "screen-coordinates close-up establishing frame" PR-01, freeze it, then use it as this shot's first frame.)

`[Emotion: discovery upgraded | Hook: information gap (where do the coordinates point) | Connection: keyframe insert · new prop PR-01]`

---

**[00:23.0 – 00:29.0] Reading · Blood color**

`[close-up|extremely slow push-in|coordinates reflected in her pupils]`

She reads the coordinates digit by digit. **The digits reflected in her pupils run backward, yet line up one by one with a position she knows by heart**. Reading the second-to-last digit, **her brow peak suddenly knots, her Adam's apple rolls once, the finger pressed against the screen edge curls tight, knuckles going white**.

> **沈昭**: (breathy, barely forming words) 这是……观测站自己。

`[Emotion: crisis approaching | Hook: relationship mystery (who is calling her) | Connection: last-frame continuation]`

---

**[00:29.0 – 00:34.0] Wind stops · Lights on**

`[medium shot|static|all cracked screens light up green at once]`

The wind stops without warning. **Every cracked screen in the control room lights up at once**, green light falling on her from all directions — **she freezes in place, a layer of dust shaken off her shoulders, a dozen green glows reflected in her pupils**.

`[silence 2 seconds — crisis-arrival type]`

`[Emotion: crisis arrival | Hook: this episode's hook collected | Connection: last-frame continuation (Episode 2's first shot continues from it)]`

---

## 4. Key Points for Adapting Source Text

1. **Keep golden lines and plot points, re-arrange sight and sound**: the source's psychological descriptions are all externalized into shootable actions/expressions/props; what cannot be externalized is deleted, not forced into lines.
2. **Episode-splitting principle**: each episode ends at the frame of "maximum information gap"; the new episode's first shot defaults to video extension (serial feel, `@视频1`) — tail-frame carry only as fallback.
3. **Volume conversion**: 90 seconds ≈ 10–16 shots; ~800 characters of source narrative ≈ one episode. Exceed → split episodes, don't compress single-shot duration.

## 5. Post-Writing Self-Check (MUST pass before Gate 1)

- [ ] Timecodes consecutive, single shot 4–10s, sum = total duration
- [ ] Every shot's label line uses words from the shot-language.md lookup table
- [ ] Every shot has at least two body-part-level micro-expressions and one physical dynamic
- [ ] Every shot has only ONE primary action (R3)
- [ ] Line-end triple labels complete; connection values legal; every new character/new prop first appearance marked with keyframe insert
- [ ] Line duration ≤ shot duration - 1 second
- [ ] No inner monologue, no unshootable information, no copyright risk (R6)
