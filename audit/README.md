# Reviewer entry point

This package documents **the already-public lower bound 222** and **two
internally audited proposed routes to 223** for C(54,16,4). External
mathematical review, literature priority and formal proof verification are
pending. Perry Kern directed this publication audit; the work used AI
assistance, including Mopî's preparation and the independent internal
reviewer. A second implementation is evidence of arithmetic agreement,
not a substitute for qualified mathematical review.

Start with [PROOFS.md](PROOFS.md), numbered Definitions/Lemmas/Theorems
1–18. Lemmas 1–5 give the shared premises. Theorems 6–9 reconstruct 222;
10–14 give Pētā's analytic 223 route; 15–17 give scout's exact certificate;
18 gives the lift. [DEPENDENCIES.md](DEPENDENCIES.md) maps each premise to
code. [ENUMERATIONS.md](ENUMERATIONS.md) states the complete finite universes
and their limits. [ATTRIBUTION.md](ATTRIBUTION.md) distinguishes prior art
from project derivations. [CHANGELOG.md](CHANGELOG.md) records every source
adaptation and [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json) pins the
frozen inputs.

From the repository root, Python 3.10+ and its standard library suffice:

```sh
python -B audit/verify_audit.py --check-manifest
python -B -O audit/verify_audit.py --check-manifest
python -B audit/run_checks.py --check-manifest
```

The checks rebuild both full matrices, replay both exact signed
certificates, verify the direct rank-floor algebra, check Pētā's 557 chord
cases, reconstruct all support graphs, and test repeated-block/completeness
boundaries. They reject damaged data in normal and optimized modes and
check that both modes produce identical mathematical receipts.
[receipts/TEST_RECEIPT.json](receipts/TEST_RECEIPT.json) contains the
recorded full test evidence. Use `--output NEW_RECEIPT.json` to save another
receipt; output creation is exclusive. No LP solver or network is needed.

Expected exact values:

| Route | Exact contradiction | Status before this addition |
| --- | --- | --- |
| 222 | F <= -1330103235427/500000000 | Already public; external review pending |
| Pētā 223 | H <= -7086 at b=64; H <= -63 at b=65 | Internal review passed with limits |
| Scout 223 | F2 <= -121049912921/100000000 | Internal review passed with limits |

Read [REVIEW_LIMITS.md](REVIEW_LIMITS.md) for the trust boundary and
unresolved review work. No target cover of 335 blocks or exact covering
number is claimed. The original public 222 data, proof, verifier and
tests remain unchanged. Publication is coordinated separately by the
parent task; this directory is a prepared handoff.
