# Shot List — <Drama Title / 片名> Episode N（Phase 3 output; freezes after gate 3 confirms）

> Transcribed from the standard shooting script, one line per shot. The first-frame source and the transition method decide the production order. Any shot that hits an item on the shot-language.md chapter 8 blacklist MUST fill in a mitigation plan.

## Shot List / 分镜表

| Shot / 镜号 | Dur (s) / 时长 | Shot Size / 景别 | Camera Move / 运镜 | Subject / 画面主体 | Primary Action (single) / 主动作·唯一 | Micro-Expression / 微表情 | Line / 台词 | Emotion / 情绪 | Transition / 衔接方式 | First-Frame Source / 首帧来源 | Risk Flags / 风险标记 | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | 5.0 | extreme long shot | ultra-slow push-in | full view of the observation station | snow sweeping across the ridge | — | — | suspense building | jump cut | SC-01 establishing image | — | ⏳ |
| S02 | 6.0 | medium shot | handheld follow | Shen Zhao | shoves the door open, flashlight sweeping | wrist pause + white breath cloud | "不可能还有电" | building tension | tail-frame carry | S01 tail frame | handheld — slow down | ⏳ |
| S03 | 6.0 | close-up | slight push-in | fingertip & screen | finger taps the screen | lashes flutter + jaw tightens | — | discovery | tail-frame carry | S02 tail frame | hand close-up — fixed-camera alternative | ⏳ |
| S04 | 6.0 | extreme close-up | fixed | screen coordinates | characters freeze in place | breath stops | — | discovery escalates | keyframe insert · new prop | PR-01 establishing frame | on-screen text — switch to blurred character stream | ⏳ |

## Fill-In Rules / 填写规则
1. **Primary action (single) / 主动作·唯一**: one primary action per cell（R3）; if you write two actions → split the shot.
2. **Micro-expression / 微表情**: 1–2 part-level details, quoted from the script body.
3. **Transition has exactly 4 allowed values / 衔接方式四值**: tail-frame carry / keyframe insert · new character / keyframe insert · new prop / jump cut — must match the script's end-of-line annotation; changing either one requires syncing the other.
4. **First-frame source / 首帧来源** takes a concrete ID: S## tail frame / CH-## look image / SC-## establishing image / PR-## establishing frame.
5. **Start / end framing / 起幅·落幅**（required for camera-move shots; optional for fixed shots）: for each shot, write with "→" what is in frame at the start and at the end of the move, e.g. "start: her hand holding the pearl hangs at her side → end: the pearl pressed against her lips". The end frame MUST be a completed action state（for tail-frame extraction）.
6. **Production order / 生产排序**: establishing images and look images（the sources of jump cuts and keyframes）must be produced FIRST; shots on a tail-frame carry chain MUST be produced strictly in shot-number order — no skipping numbers.

## Stats Self-Check（before submitting to gate 3）/ 统计自检
- [ ] Sum of all shot durations = the script's total duration
- [ ] Transition chain complete: every shot's first-frame source is an existing previous shot or a frozen asset, except S01 and the jump-cut shots
- [ ] The keyframe-insert shots' look / frame IDs are listed in the production plan and scheduled BEFORE those shots
- [ ] Blacklist（shot-language.md chapter 8）scanned shot by shot; any hits already have a mitigation plan filled in
