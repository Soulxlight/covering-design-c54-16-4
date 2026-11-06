# Verified upper bound C(54,16,4) ≤ 302

The [302-block witness](../data/cover-302.txt) has 302 distinct legal 16-subsets
of points 1 through 54. Two independent exhaustive methods verify coverage of
all 316,251 quadruples. This improves the supplied 335-block incumbent by 33 blocks.
Optimality is not claimed. [RESULT.json](RESULT.json) pins the witness SHA-256:
`96c6adca7d06f51c04a029a3a807978fed7ccd587a95abdc04cb1c4130fda4fd`.

The cover was verified on 6 November 2026 at 16:32:33 UTC. This fixed checkpoint
is preserved while the campaign continues; newer results require separate
verification and an explicit update. The combined certificate check is
[VERIFICATION.json](VERIFICATION.json).

## Verify the certificate

From the project root, using standard-library Python 3.10 or later:

```sh
python -B upper_search/verify_best.py
python -B -O upper_search/verify_best.py
```

One checker enumerates the quadruples of every block and marks their colex
ranks. The other traverses all target quadruples and intersects point-to-block
incidence bitsets. Both require the pinned hash, legal distinct blocks, the
exact count and zero uncovered targets. Verification uses no search-engine state.

## Reproduce the winning search

[reproduction302](reproduction302/README.md) includes the actual C++ source,
required header, MIT license, direct input, original metadata, log snapshot,
independent verifiers and portable replay driver. No executable is distributed.

The [direct input](reproduction302/input.txt) has **302 blocks and exactly nine
uncovered quadruples**, SHA-256
`dc3a0bb71bb023de9b2efd73489dc8a02d63396f3466940791af39bc261a1b4c`.
Run 1243 used seed 1243, tabu tenure 12 and noise 0.02. It completed the cover after
4,528,541 steps at 131.7 seconds of the recorded 300-second allocation.
The environment was `BALANCE_POINT=16`, `BALANCE_PAIR=1`, with target weighting
enabled. GCC was Debian 14.2.0-19. [REPLAY.json](reproduction302/REPLAY.json) pins
arguments, environment, checkpoint-output settings, input and output hashes.

A C++17 compiler is needed only to rerun the search:

```sh
python -B upper_search/reproduction302/replay.py --compile-only
python -B upper_search/reproduction302/replay.py
```

The driver starts from the included nine-hole partial with targetB=302 and uses
a fresh external output directory. It rejects a failed search process and
independently verifies new completed output. `--native` retains the original
architecture optimization; `--seconds 1800` allows a longer budget. Compiler, runtime and timing differences may change
search trajectories. Portable compilation has passed; a fresh search replay
is not claimed. The pinned witness and exhaustive checks establish the bound.

The direct input came from run 1242. The preserved original metadata records
its immutable path/hash and the producing environment. Complete replay of all
earlier search ancestors is not claimed.

## Retained history and attribution

The [305 milestone](README-305.md), [result](RESULT-305.json),
[verification](VERIFICATION-305.json) and entire `reproduction305/` directory
are preserved unchanged. The [318 milestone](README-318.md), its result and
verification, and `reproduction/` are retained, along with the first
[334 milestone](../upper334/README.md), supplied [335 witness](../upper335/README.md)
and all lower-proof files. [CAMPAIGN_CHECKPOINTS.json](CAMPAIGN_CHECKPOINTS.json)
indexes intermediate covers through 302; [campaign_improvements.jsonl](campaign_improvements.jsonl)
extends the existing size-improvement ledger without rewriting earlier events.

The search adapts Wynand van Staden's MIT-licensed WLS2. Later changes include
64-bit masks, cached quadruple ranks, sparse move scoring, point/pair incidence
balancing, and immutable equal-partial checkpoints. Perry Kern directed the
AI-assisted search and independent verification. The supplied 335 witness and
original WLS2 license retain their existing attribution.

The published Covering Repository upper bound was checked as 335 on 6 November 2026.
This local checkpoint claims no submission, curator acceptance, worldwide
priority, or optimality. The internally reviewed lower bound 230 and its pending
qualified external-review status are unchanged.
