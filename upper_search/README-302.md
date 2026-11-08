# Historical November 6 checkpoint: 302 blocks

The original README is reproduced unchanged below. Its frozen result and
verification records are [RESULT-302.json](RESULT-302.json) and
[VERIFICATION-302.json](VERIFICATION-302.json). Generic links to `RESULT.json`,
`VERIFICATION.json`, and `verify_best.py` follow the newer current checkpoint.
To verify this historical witness directly from the project root:

```sh
python -B upper334/verify_colex.py 54 16 4 data/cover-302.txt
python -B upper334/verify_incidence.py data/cover-302.txt --expected-blocks 302
```

---

# Verified upper bound C(54,16,4) ≤ 302

The [302-block witness](../data/cover-302.txt) has 302 distinct legal 16-subsets
of points 1 through 54. Two independent exhaustive methods verify coverage of
all 316,251 quadruples. This improves the supplied 335-block incumbent by 33 blocks.
Optimality is not claimed. [RESULT.json](RESULT.json) pins the witness SHA-256:
`96c6adca7d06f51c04a029a3a807978fed7ccd587a95abdc04cb1c4130fda4fd`.

The cover was verified on 6 November 2026 at 16:32:33 UTC. The campaign stopped
after a strict three-hour full-size stall and final producer/output drain at
2026-11-06T19:32:53.625553+00:00. The observed gap was 10820.594874 seconds.
[CAMPAIGN_FINAL.json](CAMPAIGN_FINAL.json) records the final stop and retained
search families. The complete-witness check remains [VERIFICATION.json](VERIFICATION.json).

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

## Final evidence and resumable incomplete checkpoints

The [portable evidence packet](campaign_evidence/README.md) retains three
pairwise non-isomorphic 302-block full covers and their actual source, direct
input, license, settings and replay provenance. Their differing point-degree
spectra independently rule out isomorphism.

The three useful 301-block restart files have 7, 8, 19 uncovered quadruples.
**Every restart file is incomplete; none establishes a 301-block cover.** Each
packet includes its exact holes, independent verification and portable continuation.
The [research notes](campaign_evidence/RESEARCH_NOTES.md) distinguish mathematical
witnesses, local neighborhood exclusions, finite-pool solver results and exploratory
mixed-cardinality states. No unrestricted optimality claim is made.

```sh
python -B upper_search/campaign_evidence/verify_evidence.py
python -B -O upper_search/campaign_evidence/verify_evidence.py
```

This verifies all retained full and partial witnesses without running search.
The combined release verifier also checks the packet. Optional reproduction of
the longer point-pair research certificate needs a C++17 compiler; its complete
normal and optimized replays passed before this freeze. Verification, partial
deficit improvements and equal-size covers never reset the full-size stall clock.

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
