from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


COMPANY = 'Ada Bench'
REPO = 'ada-bench'
PROJECT_TERMS = ['evidence', 'workflow', 'review', 'claims', 'fixtures', 'replay', 'handoff', 'trace', 'policy', 'decision', 'coverage', 'latency']
PROJECT_METRICS = ['evidence_coverage', 'handoff_risk', 'claim_precision', 'review_latency']
PROJECT_FAILURES = ['evidence_drift', 'handoff_gap', 'claim_misroute', 'review_blindspot']
PROJECT_ARCHETYPES = [{'name': 'evidence replay', 'trigger': 'source evidence changes while workflow context is stale', 'expected': 'block release until cited evidence is regenerated'}, {'name': 'handoff boundary probe', 'trigger': 'handoff crosses a policy or trust boundary', 'expected': 'route to reviewer with evidence packet'}, {'name': 'claim regression harness', 'trigger': 'claim behavior regresses against the last accepted fixture', 'expected': 'open a regression issue with trace and benchmark delta'}, {'name': 'review operator packet', 'trigger': 'review output needs a human-readable audit packet', 'expected': 'accept only if decision claims cite fixture evidence'}]
PROJECT_DIRECTION = 'An open, reproducible retrospective benchmark for predicting clinical anti-drug antibody rates on FDA-approved monoclonal antibodies. The output is a partner-facing evidence pack Ada Bench can use to show where an immunogenicity predictor generalizes, where it fails, and what evidence supports the claim.'


def _short(value: str, limit: int = 44) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "..."


def _wrap(value: str, limit: int = 48, max_lines: int = 3) -> list[str]:
    words = " ".join(value.split()).split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if len(candidate) <= limit:
            current.append(word)
            continue
        if current:
            lines.append(" ".join(current))
        current = [word]
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = _short(lines[-1], max(8, limit - 1))
    return lines or [""]


def _text_block(
    value: str,
    *,
    x: int,
    y: int,
    css: str,
    limit: int,
    max_lines: int,
    line_height: int,
) -> str:
    lines = _wrap(value, limit=limit, max_lines=max_lines)
    parts = [f'<text class="{css}" x="{x}" y="{y}">']
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{_escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_signal_model(rows: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> dict[str, Any]:
    total = max(1, len(rows))
    blocked = sum(1 for row in rows if row["status"] == "block")
    review = sum(1 for row in rows if row["status"] == "review")
    evidence_density = round(sum(len(row["evidence_quote"].split()) for row in rows) / total, 2)
    pressure = round((blocked * 1.9 + review) / total, 4)
    ranked_clusters = sorted(
        clusters,
        key=lambda item: (item["blocks"], item["reviews"], item["mean_severity"]),
        reverse=True,
    )
    leverage = []
    for index, cluster in enumerate(ranked_clusters[:4], start=1):
        metric = PROJECT_METRICS[(index - 1) % len(PROJECT_METRICS)]
        failure = PROJECT_FAILURES[(index - 1) % len(PROJECT_FAILURES)]
        leverage.append(
            {
                "rank": index,
                "scenario": cluster["scenario"],
                "metric": metric,
                "failure_mode": failure,
                "evidence": cluster["top_evidence_id"],
                "operator_action": cluster["recommended_action"],
                "severity": cluster["mean_severity"],
            }
        )
    return {
        "company": COMPANY,
        "repo": REPO,
        "terms": PROJECT_TERMS,
        "metrics": PROJECT_METRICS,
        "failure_modes": PROJECT_FAILURES,
        "evidence_density": evidence_density,
        "pressure_index": pressure,
        "blocked_share": round(blocked / total, 4),
        "review_share": round(review / total, 4),
        "top_leverage_points": leverage,
        "readout": (
            "This local harness runs a deterministic pressure test around "
            f"{PROJECT_TERMS[0]}, {PROJECT_TERMS[1]}, and {PROJECT_TERMS[2]}. "
            f"The useful part is not the dashboard; it is the repeatable evidence path "
            f"from fixture to failure to operator action."
        ),
    }


def write_showcase_assets(
    outputs: Path,
    profile: dict[str, Any],
    rows: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    model: dict[str, Any],
) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    (outputs / "operator_brief.md").write_text(_operator_brief(model), encoding="utf-8")
    (outputs / "architecture.json").write_text(json.dumps(_architecture(model), indent=2), encoding="utf-8")
    (outputs / "project_working.svg").write_text(_working_svg(model), encoding="utf-8")
    (outputs / "evidence_map.svg").write_text(_evidence_svg(model), encoding="utf-8")


def _operator_brief(model: dict[str, Any]) -> str:
    lines = [
        f"# Operator Brief: {COMPANY}",
        "",
        model["readout"],
        "",
        "## Highest-leverage checks",
        "",
    ]
    for point in model["top_leverage_points"]:
        lines.append(
            f"- {point['scenario']} -> {point['operator_action']} "
            f"({point['metric']}, evidence {point['evidence']})."
        )
    lines.extend(
        [
            "",
            "## What makes this useful",
            "",
            "The workflow is intentionally local and deterministic. A reviewer can run the same fixture set, inspect the evidence IDs, open the dashboard, and see exactly why a recommendation passed, went to review, or blocked.",
        ]
    )
    return "\n".join(lines) + "\n"


def _architecture(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "layers": [
            {"name": "synthetic_fixture_replay", "purpose": f"exercise {PROJECT_TERMS[0]} and {PROJECT_TERMS[1]} cases"},
            {"name": "domain_strategy", "purpose": f"score {PROJECT_METRICS[0]} and {PROJECT_METRICS[1]}"},
            {"name": "evidence_lock", "purpose": "reject narrative claims without fixture evidence IDs"},
            {"name": "operator_packet", "purpose": "emit dashboard, SVG readout, CSV, markdown report, and demo pack"},
        ],
        "pressure_index": model["pressure_index"],
        "top_leverage_points": model["top_leverage_points"],
    }


def _working_svg(model: dict[str, Any]) -> str:
    gate_rows = []
    claim_cards = []
    colors = ["#0f766e", "#4f46e5", "#b45309", "#2563eb"]
    for index, point in enumerate(model["top_leverage_points"]):
        y = 370 + index * 66
        width = min(370, 226 + int(float(point["severity"]) * 54))
        gate_rows.append(
            f'<text x="92" y="{y - 12}" class="label">{_escape(point["metric"].replace("_", " "))}</text>'
            f'<text x="455" y="{y - 12}" class="mono">{_escape(point["evidence"])}</text>'
            f'<rect x="92" y="{y}" width="390" height="14" rx="7" fill="#e5e7eb"/>'
            f'<rect x="92" y="{y}" width="{width}" height="14" rx="7" fill="{colors[index % len(colors)]}"/>'
            f'<text x="92" y="{y + 38}" class="caption">{_escape(_short(point["scenario"], 48))}</text>'
        )
        card_x = 622 + (index % 2) * 242
        card_y = 350 + (index // 2) * 142
        claim_cards.append(
            f'<rect class="claim" x="{card_x}" y="{card_y}" width="212" height="116" rx="8"/>'
            f'<text class="rank" x="{card_x + 18}" y="{card_y + 28}">claim {index + 1}</text>'
            + _text_block(
                point["operator_action"],
                x=card_x + 18,
                y=card_y + 56,
                css="claimtext",
                limit=24,
                max_lines=3,
                line_height=17,
            )
            + f'<text class="mono" x="{card_x + 18}" y="{card_y + 100}">{_escape(point["evidence"])}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="700" viewBox="0 0 1120 700" role="img" aria-label="{_escape(COMPANY)} ADA benchmark dashboard preview">
  <defs>
    <style>
      .bg {{ fill:#f7faf9; }}
      .panel {{ fill:#ffffff; stroke:#d7e2df; stroke-width:1.1; }}
      .card {{ fill:#ffffff; stroke:#d7e2df; stroke-width:1.1; }}
      .claim {{ fill:#fbfdfc; stroke:#d7e2df; stroke-width:1.1; }}
      .title {{ font:760 30px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#10201c; }}
      .sub {{ font:420 15px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#475569; }}
      .label {{ font:700 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#1f2937; }}
      .caption {{ font:500 12px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#64748b; }}
      .small {{ font:650 12px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#64748b; }}
      .metric {{ font:780 29px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#0f172a; }}
      .rank {{ font:760 13px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#0f766e; }}
      .claimtext {{ font:650 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#14211e; }}
      .mono {{ font:700 12px ui-monospace,SFMono-Regular,Menlo,monospace; fill:#334155; }}
    </style>
  </defs>
  <rect class="bg" width="1120" height="700"/>
  <rect class="panel" x="28" y="28" width="1064" height="644" rx="8"/>
  <text class="title" x="64" y="76">ADA Generalization Bench</text>
  {_text_block(PROJECT_DIRECTION, x=64, y=108, css="sub", limit=86, max_lines=2, line_height=22)}
  <rect class="card" x="64" y="166" width="232" height="84" rx="8"/>
  <text class="small" x="84" y="194">pressure index</text>
  <text class="metric" x="84" y="230">{model["pressure_index"]}</text>
  <rect class="card" x="320" y="166" width="232" height="84" rx="8"/>
  <text class="small" x="340" y="194">evidence density</text>
  <text class="metric" x="340" y="230">{model["evidence_density"]}</text>
  <rect class="card" x="576" y="166" width="480" height="84" rx="8"/>
  <text class="small" x="596" y="194">partner-facing claim under test</text>
  {_text_block(model["top_leverage_points"][0]["scenario"], x=596, y=224, css="label", limit=56, max_lines=1, line_height=16)}
  <rect class="card" x="64" y="292" width="482" height="338" rx="8"/>
  <text class="label" x="92" y="322">blind-set benchmark gates</text>
  {''.join(gate_rows)}
  <text class="label" x="622" y="324">BD claims must carry evidence IDs</text>
  {''.join(claim_cards)}
</svg>
"""


def _evidence_svg(model: dict[str, Any]) -> str:
    nodes = []
    edges = []
    x_positions = [64, 294, 548, 764]
    for index, point in enumerate(model["top_leverage_points"]):
        y = 118 + index * 88
        nodes.append(
            f'<rect class="split" x="{x_positions[0]}" y="{y}" width="178" height="56" rx="8"/>'
            + _text_block(point["scenario"], x=x_positions[0] + 14, y=y + 23, css="node", limit=21, max_lines=2, line_height=16)
        )
        nodes.append(
            f'<rect class="failure" x="{x_positions[1]}" y="{y}" width="186" height="56" rx="8"/>'
            f'<text x="{x_positions[1] + 14}" y="{y + 34}" class="node">{_escape(point["failure_mode"].replace("_", " "))}</text>'
        )
        nodes.append(
            f'<rect class="evidencebox" x="{x_positions[2]}" y="{y}" width="146" height="56" rx="8"/>'
            f'<text x="{x_positions[2] + 27}" y="{y + 35}" class="mono">{_escape(point["evidence"])}</text>'
        )
        nodes.append(
            f'<rect class="claimbox" x="{x_positions[3]}" y="{y}" width="292" height="56" rx="8"/>'
            + _text_block(point["operator_action"], x=x_positions[3] + 14, y=y + 23, css="node", limit=36, max_lines=2, line_height=16)
        )
        edges.extend([
            f'<path d="M242 {y + 28} L294 {y + 28}" class="edge"/>',
            f'<path d="M480 {y + 28} L548 {y + 28}" class="edge"/>',
            f'<path d="M694 {y + 28} L764 {y + 28}" class="edge"/>',
        ])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="500" viewBox="0 0 1120 500" role="img" aria-label="{_escape(COMPANY)} evidence map">
  <defs>
    <style>
      .bg {{ fill:#f7faf9; }}
      .panel {{ fill:#ffffff; stroke:#d7e2df; stroke-width:1.1; }}
      .title {{ font:760 28px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#10201c; }}
      .node {{ font:620 13px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#1f2937; }}
      .head {{ font:700 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; fill:#64748b; }}
      .mono {{ font:720 13px ui-monospace,SFMono-Regular,Menlo,monospace; fill:#334155; }}
      .edge {{ stroke:#94a3b8; stroke-width:2; fill:none; marker-end:url(#arrow); }}
      .split {{ fill:#ecfdf5; stroke:#bbf7d0; }}
      .failure {{ fill:#eef2ff; stroke:#dbe4ff; }}
      .evidencebox {{ fill:#fffbeb; stroke:#fde68a; }}
      .claimbox {{ fill:#f0f9ff; stroke:#bae6fd; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker>
  </defs>
  <rect class="bg" width="1120" height="500"/>
  <rect class="panel" x="28" y="28" width="1064" height="444" rx="8"/>
  <text x="56" y="70" class="title">{_escape(COMPANY)} retrospective claim chain</text>
  <text x="64" y="104" class="head">blind split</text><text x="294" y="104" class="head">failure gate</text><text x="548" y="104" class="head">evidence</text><text x="764" y="104" class="head">BD-safe action</text>
  {''.join(edges)}
  {''.join(nodes)}
</svg>
"""
