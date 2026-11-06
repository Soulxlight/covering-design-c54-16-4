# Verified upper bound C(54,16,4) ≤ 305

The [305-block witness](../data/cover-305.txt) contains 305 distinct legal
16-subsets of 1 through 54. Two independent exhaustive methods verify that
all 316,251 quadruples are covered. This improves the supplied 335-block
incumbent by 30 blocks. Optimality is not claimed.

[RESULT.json](RESULT.json) pins this checkpoint and its SHA-256:
`570f1791870e31e8b8f1b721848f8e37ce4d5d5dd3d683faf93c48162d5d4f65`.
The combined result is [VERIFICATION.json](VERIFICATION.json). The cover was
verified on 6 November 2026 at 14:28:10 UTC. This checkpoint is preserved while
the campaign continues; a later improvement requires a separately verified
witness and an explicit update.

## Verify the certificate

From the project root, using standard-library Python 3.10 or later:

```sh
python -B upper_search/verify_best.py
python -B -O upper_search/verify_best.py
```

One implementation enumerates each block's quadruples and marks their colex
ranks. The other independently traverses every target quadruple and intersects
its point-to-block incidence bitsets. Both require legal distinct blocks,
the exact count and pinned hash, and zero uncovered targets. Neither method
uses search-engine state. The algorithms and malformed-input controls remain
in [upper334](../upper334/).

## Reproduce the winning search

The self-contained [reproduction305](reproduction305/README.md) directory
preserves the exact C++ source, its required header, the MIT license, input,
run metadata, log snapshot, independent verifiers and a portable replay driver.
No platform-specific executable is included.

The direct [input](reproduction305/input.txt) has **305 blocks and exactly five
uncovered quadruples**. Seed 1167, tabu tenure 3 and noise 0.05 completed the
cover after 6,037,122 steps, at 175.3 seconds in the recorded run. The secondary
point/pair incidence-balancing weights were `BALANCE_POINT=16` and
`BALANCE_PAIR=1`; the main search retained target weighting. GCC was Debian
14.2.0-19. [REPLAY.json](reproduction305/REPLAY.json) records the actual arguments
and environment; [original_metadata.json](reproduction305/original_metadata.json)
and [winning_run.log](reproduction305/winning_run.log) preserve the run evidence.

A C++17 compiler is needed only to rerun the search:

```sh
python -B upper_search/reproduction305/replay.py --compile-only
python -B upper_search/reproduction305/replay.py
```

The driver uses the recorded five-hole input and seed, with `targetB=305`.
By default it writes generated files into a fresh directory outside this repository,
rejects a failed search process, and independently verifies any completed
output. Use `--native` to retain the original `-march=native` compilation flag
or `--seconds 1800` to allow more wall-clock time. Compiler, standard-library
and timing differences can affect search replay; the pinned witness and its
exhaustive checks establish the bound independently. Portable compilation
has been checked. A fresh search replay is not claimed for this checkpoint.

## Input ancestry and retained checkpoints

The winning branch began with a targeted replacement of row 167 (zero-based)
in a two-hole 305-block partial. It removed points 20, 45 and 52 and added
11, 32 and 53. A search temporarily fixing that modified row produced the
five-hole input `be2608951b5d805151b32d5230aef3040bee6998383aa94097545ffabd9c4ee1`.
The balancing run then completed the cover. Its 600-second allocation
preserved this branch despite other partial candidates having fewer holes.

[INPUT_ANCESTRY.json](reproduction305/INPUT_ANCESTRY.json) indexes the exact
input recipes and predecessor metadata. These preserve the branch's provenance;
complete replay of every ancestor search is not claimed. Replaying the final
run uses its included immutable five-hole input directly.

The [318-block checkpoint](README-318.md), its [result](RESULT-318.json),
[verification](VERIFICATION-318.json), and original `reproduction/` directory
remain available; the historical source, inputs and run records are unchanged. The [334 milestone](../upper334/README.md), supplied
[335 witness](../upper335/README.md), and all earlier proof files are retained.
[CAMPAIGN_CHECKPOINTS.json](CAMPAIGN_CHECKPOINTS.json) indexes the intervening
witnesses; [campaign_improvements.jsonl](campaign_improvements.jsonl) preserves
the append-only size-improvement events through 305.

## Attribution and status

The search adapts Wynand van Staden's MIT-licensed WLS2. Subsequent adaptations
include 64-bit masks, cached quadruple ranks, sparse move scoring, and
point/pair incidence balancing. Perry Kern directed the AI-assisted searches
and independent verification. The supplied 335-block cover retains its
attribution in `upper335/`; the original WLS2 license and attribution remain
with the source.

The published Covering Repository upper bound was checked as 335 on
6 November 2026. This local checkpoint claims no submission, curator acceptance,
worldwide priority, or optimality. The existing internally reviewed lower
bound 230 and its pending qualified external-review status are unchanged.
