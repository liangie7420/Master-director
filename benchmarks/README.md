# Prompt experiments

This suite separates input correctness from generated-video quality.

- baseline/manifest.json preserves the original scanner outcomes, file hashes and Git baseline.
- shots/ holds six authored, fictional test specifications. References are deliberately unfilled.
- results/ contains reproducible local output; it is ignored by Git. Run the command below to recreate it.

```bash
python -X utf8 scripts/run_benchmark.py
```

The runner creates task-specific drafts for five version configurations, a labelled reconstruction of the former universal template, a lint comparison, and a blank real-trial record.
Unsupported combinations should fail rather than silently change the selected task or model. Unknown limits remain visible draft warnings.
These are editorial fixtures, not an accepted episode or observed output. No API key, model call or paid generation is used.

For real comparisons, provide actual frozen assets, exact provider settings and multiple trial records. Record source/output paths and hashes, time, charged cost, observed evidence and scores following references/evaluation.md. Do not infer a visual gain from this local suite.
