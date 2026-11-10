# Verified upper bound C(54,16,4) ≤ 297

The [297-block witness](../data/cover-297.txt) has 297 distinct legal 16-subsets
of points 1 through 54 and covers all 316,251 quadruples. Independent colex subset
enumeration and point-incidence intersection checks agree. This improves the
previous GitHub release's 335-block incumbent by 38 blocks. Optimality is not claimed.

SHA-256: `188eaba56fb0260bb6b7c5c2adaf2d0025e10882d52cd24688688ac0dee96362`.
[RESULT.json](RESULT.json), [VERIFICATION.json](VERIFICATION.json) and
[INDEPENDENT-297.json](INDEPENDENT-297.json) pin the witness and separate checks.
Research was paused at the user's request on November 9, 2026. The
[restart checkpoint](resume-20261109/README.md) records that stop and the best
incomplete 296-block candidates. [SESSION-20261109.json](SESSION-20261109.json)
is the earlier running snapshot, preserved as historical provenance.
This GitHub publication is dated November 10, 2026.

## Constructive proof

Let V = {1, ..., 54}, and let B be the family of rows in the pinned witness.
The parsers verify that B contains exactly 297 pairwise distinct blocks, each
with 16 distinct elements of V. For every four-subset T of V, the exhaustive
checks verify that at least one block in B contains T. Therefore B is a
(54,16,4) covering, and the definition of the covering number gives
**C(54,16,4) <= |B| = 297**.

The first implementation enumerates all C(16,4) = 1,820 quadruples in each
block, for 540,540 block-quadruple occurrences, and marks their integer colex
ranks. For labels a < b < c < d, the rank is
C(a-1,1) + C(b-1,2) + C(c-1,3) + C(d-1,4). These ranks biject the target
quadruples with 0 through 316,250; all 316,251 ranks are covered.

The second implementation builds, for each point x, a bitset I(x) of the
blocks containing x. It separately enumerates all C(54,4) = 316,251 target
quadruples and checks I(a) & I(b) & I(c) & I(d) != 0 for every one. A nonzero
intersection identifies a common containing block. This checker uses no
colex ranking and does not consume the first checker's output.

The witness and these finite exhaustive checks supply the upper-bound
certificate independently of the search heuristic or a replay of its random
trajectory. They do not prove that 297 is minimal. The retained lower-bound
proof has its own review qualifications.

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

## Paused continuation toward 296

The main [296-block restart candidate](resume-20261109/partial-296-h2.txt)
covers 316,249 quadruples and misses `{9,12,41,54}` and `{23,24,30,42}`.
It is **not a cover**. All four saved 296-block candidates have their exact
hole lists and independent checks in [PARTIALS.json](resume-20261109/PARTIALS.json).
The restart guide distinguishes completed local exclusions, bounded searches
that were inconclusive, and prepared work that has not run. None of these
partial results changes the verified upper bound of 297.

## Preserved history and attribution

The [301 checkpoint](README-301.md), its registered neutral-preparation ancestry,
all earlier reproduction directories and the [November 6 final evidence](campaign_evidence/README.md)
remain unchanged. Old incomplete restart files remain explicitly incomplete.
The internally reviewed lower bound 230 and its pending qualified external-review
status are unchanged, as are all lower-proof bytes.

The engines adapt Wynand van Staden's MIT-licensed WLS2. Perry Kern directed the
AI-assisted search and independent checking. The [dated public observation](PUBLIC_BOUND-20261108.json)
reported 302 on November 8; the unavailable public block list was not identified
with any local witness. This GitHub release publishes the witness, verification,
search provenance and restart notes. Covering Repository curator acceptance and
literature priority remain unconfirmed; neither is implied by this publication.
