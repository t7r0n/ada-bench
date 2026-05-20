# Ada Bench

An open, reproducible retrospective benchmark for predicting clinical anti-drug antibody rates on FDA-approved monoclonal antibodies. The output is a partner-facing evidence pack Ada Bench can use to show where an immunogenicity predictor generalizes, where it fails, and what evidence supports the claim.

![Ada Bench working dashboard](outputs/project_working.svg)

## Why it exists

The first serious question in a pharma BD conversation is not whether the organoid is interesting. It is whether the predictor generalizes beyond the molecules and assays it was tuned on.

Most internal demos stop at a pretty chart. This repository is built around the harder part: a repeatable path from fixture, to failure, to evidence, to the operator action a serious team would actually trust.

## What is inside

- A deterministic replay harness tuned around ADA generalization, blind antibody splits, and BD-grade evidence.
- Company-specific strategy code in `src/ada_bench/strategy.py`, not just README-level customization.
- Citation-locked reports where every decision claim has to point back to a generated evidence ID.
- Two visual artifacts generated from the latest run: `outputs/project_working.svg` and `outputs/evidence_map.svg`.
- A portable demo pack with JSON, CSV, Markdown, HTML, SVG, and benchmark artifacts.

![Ada Bench evidence map](outputs/evidence_map.svg)

## Signals it measures

- `single coverage`
- `important risk`
- `question precision`
- `pharma latency`

## Failure modes it plants

- single drift
- important gap
- question misroute
- pharma blindspot

## Run it locally

```bash
uv sync
uv run ada-bench all
uv run pytest -q
uv run ruff check .
```

## Outputs worth opening

- `outputs/dashboard.html`
- `outputs/project_working.svg`
- `outputs/evidence_map.svg`
- `outputs/operator_brief.md`
- `outputs/decision_report.md`
- `outputs/strategy_model.json`
- `outputs/demo_pack.zip`

## Boundary

Everything runs locally against synthetic fixtures. There are no credentials, no customer records, no outreach files, and no hosted API dependency.
