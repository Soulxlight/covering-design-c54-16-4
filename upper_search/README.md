# Verified upper bound C(54,16,4) ≤ 297

The [297-block witness](../data/cover-297.txt) has 297 distinct legal 16-subsets
of points 1 through 54 and covers all 316,251 quadruples. Independent colex subset
enumeration and point-incidence intersection checks agree. This improves the
supplied 335-block incumbent by 38 blocks. Optimality is not claimed.

SHA-256: `188eaba56fb0260bb6b7c5c2adaf2d0025e10882d52cd24688688ac0dee96362`.
[RESULT.json](RESULT.json), [VERIFICATION.json](VERIFICATION.json) and
[INDEPENDENT-297.json](INDEPENDENT-297.json) pin the witness and separate checks.
The search remains active toward 296 blocks; [this session record](SESSION-20261109.json)
is an intermediate checkpoint, not a final stop report.

## Verify

From the repository root with standard-library Python 3.10+:

```sh
python -B upper_search/verify_best.py
python -B -O upper_search/verify_best.py
```

## New complete milestones

| Blocks | First owner verification, UTC | Producing run | Input blocks / holes | Source and replay |
| --- | --- | --- | --- | --- |
| 300 | 2026-11-08T22:39:12.255094+00:00 | run_21141 | 300 / 3 | [replay](reproduction300/README.md) |
| 299 | 2026-11-08T23:21:19.701977+00:00 | run_21171 | 299 / 4 | [replay](reproduction299/README.md) |
| 298 | 2026-11-09T00:13:51.875162+00:00 | run_21199 | 298 / 23 | [replay](reproduction298/README.md) |
| 297 | 2026-11-09T00:16:45.435477+00:00 | run_21202 | 298 / 0 | [replay](reproduction297/README.md) |

All four complete witnesses are included under `data/`. Their actual producing
sources, MIT licenses, direct inputs, seeds, environments and logs are preserved.
The 299-, 300- and 298-block inputs were incomplete; each input's exact deficit
is explicit in its verification receipt. The 297-block run started from the
complete 298-block witness, then removed and repaired a block. Portable replay
uses the actual input count and targetB for each result. A fresh search replay
is not claimed merely because the certificates and build recipes verify.

[reproduction297](reproduction297/README.md) records seed 21202, tenure 12,
noise 0.02 and ordinary weighted scores. The direct input hash is
`8c0e2a39f1bef466eb63dd9373f88185cab55888ee2144ac0075362b0b666542`.
`MILESTONES-20261109.json` binds the source packets, and the
[size-improvement ledger](campaign_improvements.jsonl) remains append-only.

## Preserved history and attribution

The [301 checkpoint](README-301.md), its registered neutral-preparation ancestry,
all earlier reproduction directories and the [November 6 final evidence](campaign_evidence/README.md)
remain unchanged. Old incomplete restart files remain explicitly incomplete.
The internally reviewed lower bound 230 and its pending qualified external-review
status are unchanged, as are all lower-proof bytes.

The engines adapt Wynand van Staden's MIT-licensed WLS2. Perry Kern directed the
AI-assisted search and independent checking. The [dated public observation](PUBLIC_BOUND-20261108.json)
reported 302 on November 8; the unavailable public block list was not identified
with any local witness. No curator acceptance, literature priority, external
publication, upload or push is claimed by this local checkpoint.
