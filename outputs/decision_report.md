# Decision Report: Ada Bench

An open, reproducible retrospective benchmark for predicting clinical anti drug antibody (ADA) rates on FDA approved monoclonal antibodies - the de facto leaderboard ALP Bio can quote in every BD meeting.

## Evidence-Grounded Findings

CLAIM: important boundary probe should `route to reviewer with evidence packet` because blocks=3 reviews=4 mean_severity=2.528. [EVID: ev_0077]
CLAIM: pharma operator packet should `accept only if decision claims cite fixture evidence` because blocks=4 reviews=5 mean_severity=2.556. [EVID: ev_0055]
CLAIM: question regression harness should `open a regression issue with trace and benchmark delta` because blocks=3 reviews=5 mean_severity=2.528. [EVID: ev_0066]
CLAIM: single evidence replay should `block release until cited evidence is regenerated` because blocks=4 reviews=5 mean_severity=2.611. [EVID: ev_0132]
