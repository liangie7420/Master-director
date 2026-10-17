# Model Selection / 按版本与入口适配

Shared direction lives in the shot specification. Provider guidance selects legal tasks, binding syntax, parameters and optional rendering choices.

Use [profiles.json](profiles.json) as the maintained preparation registry. Values apply only to the named version and entry:
- true: documented support; false: documented incompatibility; absent/null: not established.
- checked_on is the audit date, not a guarantee of future availability.
- recheck sources when changing entry/version or encountering conflicting behavior.
- Draft mode can prepare unknown combinations for review; it never makes them submission-ready.
- A local path existing does not verify codec, dimensions, upload success or provider access.

| Family | Adapter | Current preparation coverage |
|---|---|---|
| Seedance / Jimeng | [seedance.md](seedance.md) | Ark 2.0 version profile; other versions/consumer entries require their own limits |
| MiniMax / Hailuo / 海螺 | [hailuo.md](hailuo.md) | Separate Hailuo-2.3 and Hailuo-02 API profiles |
| Google Gemini Omni | [omni.md](omni.md) | Omni 1.1 Flash; high-level tasks documented, some numeric limits pending |
| Kling / 可灵 | [kling.md](kling.md) | Version-selectable profile; exact entry limits pending verification |

Omni and Veo are different Google model families. Do not substitute one family's capabilities or API parameters for the other.
Names alone such as “Kling”, “MiniMax” or “Omni” do not identify the version, account access, interface or task limits.
