# Character Card — <Character Name / 角色名>（编号 CH-##）

> Fill in during Phase 2; FREEZE this card once the look image passes gate 2 (过闸2). From then on, every prompt's character description MUST be a VERBATIM reuse of this card's "Appearance Anchor" section（R4）— rewriting is forbidden.

## 1. Basic Info / 基本信息
- **Name / age feel / identity / 姓名·年龄感·身份**: <>
- **One-sentence aura / 一句话气质**: <e.g. "a ruler who looks lazy outside but is razor-sharp inside">
- **Voice profile / 音色**（for dubbing & dialogue prompts）: <timbre + gender / age bracket + emotional texture, e.g. "low and magnetic, male ~30s, gravelly undercurrent">

## 2. Appearance Anchor（LOCKED — reuse verbatim）/ 外观锚点
- **Face shape & features / 脸型五官**: <e.g. "long narrow face, raised brow peaks, single eyelids, slightly drooping eye corners, thin pale lips">
- **Hairstyle & hair color / 发型发色**: <e.g. "waist-length black hair, high ponytail, two loose strands at the forehead">
- **Skin tone & texture / 肤色肤质**: <e.g. "cool pale skin, one small mole at the tail of the left brow">
- **Outfit — default set / 服装·默认套**: <list top to bottom: collar / lapel / sleeve / hem / shoes, including material & primary HEX>
- **Accessories / 配饰**: <item by item: position + form, e.g. "single long silver earring on the right ear only">
- **Posture signature / 体态签名**: <e.g. "back straight as a blade, weight shifted back when standing">

## 3. Form Fatalities（the features most often drawn wrong — ban each in the negative layer）/ 形态命门
- **Fatality 1 / 命门 1**: <feature> → negative phrasing: <e.g. "no double eyelids, no Korean-style flat brows">
- **Fatality 2 / 命门 2**: <>

## 4. Performance Profile（vocabulary for script & prompts）/ 表演档案
- **Habitual micro-expression / 习惯性微表情**: <e.g. "rubs the second knuckle of the thumb while thinking">
- **How emotion externalizes / 情绪外化方式**: <e.g. "smiles when furious — the voice gets quieter instead">
- **Forbidden zone / 禁区**: <e.g. "no exaggerated expressions; even a breakdown only reddens the eyes">

## 5. Reference Image Ledger / 参考图台账
- Look image ref: <path/ID>（neutral-light version）
- Per-scene lighting versions ref: <SC-01 version / SC-02 version …>
- State-change versions ref: <injured / costume-change — outputs of keyframe inserts>

## 6. Look Image Prompt（used in Phase 2）/ 定妆图提示词
```
<visual-style anchor block>, single-character look test, <full appearance anchor, verbatim>,
lighting method (male-dominant drama = Rembrandt light / femme-fatale = butterfly light / default = three-point) + a hint of catchlight in the eyes,
85mm shallow depth of field, plain or scene-bokeh background, front-facing with a slight 15° turn, half-body shot, expression: <aura>.
Negative: <form-fatality negatives> + <project shared negative library>（all negative words concentrated on the final line）
```
> Lighting method / focal length / skin-tone fit details: see `references/lighting-styles.md`. Prompt formatting discipline（line breaks, negative on the final line, reference image IDs）: see `references/image-prompt-engine.md`.
