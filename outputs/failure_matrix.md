# Failure Matrix: Ada Bench

| Scenario | Failure mode | Metric | Gate | Evidence |
| --- | --- | --- | --- | --- |
| single evidence replay | single_drift | single_coverage | block release until cited evidence is regenerated | ev_0000 |
| pharma operator packet | pharma_blindspot | pharma_latency | accept only if decision claims cite fixture evidence | ev_0007 |
| pharma operator packet | pharma_blindspot | pharma_latency | accept only if decision claims cite fixture evidence | ev_0011 |
| question regression harness | question_misroute | question_precision | open a regression issue with trace and benchmark delta | ev_0014 |
| important boundary probe | important_gap | important_risk | route to reviewer with evidence packet | ev_0021 |
| question regression harness | question_misroute | question_precision | open a regression issue with trace and benchmark delta | ev_0022 |
| single evidence replay | single_drift | single_coverage | block release until cited evidence is regenerated | ev_0028 |
