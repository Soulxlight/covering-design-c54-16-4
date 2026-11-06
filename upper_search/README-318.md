# Verified upper bound C(54,16,4) ≤ 318

The [318-block witness](../data/cover-318.txt) contains 318 distinct legal
16-subsets of 1 through 54. Both independent exhaustive verifiers find that
all 316,251 four-subsets are covered. This improves the supplied 335-block
incumbent by 17 blocks. Optimality is not claimed.

[RESULT-318.json](RESULT-318.json) pins the witness and its SHA-256. The deterministic
combined result is [VERIFICATION-318.json](VERIFICATION-318.json).

## Verify the certificate

From the project root, using standard-library Python 3.10 or later:

```sh
python -B upper334/verify_colex.py 54 16 4 data/cover-318.txt
python -B upper334/verify_incidence.py data/cover-318.txt --expected-blocks 318
```

One implementation enumerates every block's quadruples and marks their colex
ranks. The other independently enumerates every quadruple of points and
intersects their block-incidence bitsets. Both reports must show 318 legal
distinct blocks and zero uncovered quadruples; compare their witness hash
with the retained result and verification records above. Neither checker uses search-engine state. Both algorithms
and malformed-input controls are preserved in [upper334](../upper334/).

## Reproduce the final search

The search uses a modified version of Wynand van Staden's MIT-licensed WLS2.
The exact optimized source is [wls64.cpp](reproduction/wls64.cpp); the original
license is [LICENSE](reproduction/LICENSE). Changes include 64-bit masks,
progress/checkpoint logging, cached colex ranks, and a specialized quadruple
move-scoring loop. The adapted score updates were checked against complete
recomputation, and every claimed cover was exhaustively verified.

The direct input is [partial-318-input.txt](reproduction/partial-318-input.txt).
It is a 318-block partial candidate with **four uncovered quadruples**, not a
valid covering certificate. Starting from that immutable input, seed 603,
tabu tenure 12 and noise 0.02 repaired all holes after 67,690 steps (6.5 seconds
in the original run). GCC was Debian 14.2.0-19. Source, input and output hashes
and the original invocation are recorded in
[seed-603.json](reproduction/seed-603.json), with the full
[run log](reproduction/seed-603.log).

A portable invocation stops at the verified result instead of searching
further. Run from the project root:

```sh
g++ -O3 -march=native -std=c++17 upper_search/reproduction/wls64.cpp -o /tmp/c54-wls64
cover_input="$(pwd)/upper_search/reproduction/partial-318-input.txt"
mkdir -p /tmp/c54-reproduce-318
cd /tmp/c54-reproduce-318
SAVE_PARTIAL=best_partial.txt /tmp/c54-wls64 54 16 4 318 1800 603 "$cover_input" 12 0.02 318
```

The output is `shrink_cover_54_16_4_318_603.txt`. Validate any regenerated
candidate with both exhaustive scripts. Runtime and random trajectories may
vary with compiler and C++ standard library; the checked-in witness and its
exhaustive verification establish the bound independently of replay.

## Search ancestry

The unchanged [335-block incumbent](../data/cover-335.txt) was the starting
cover. Seed 201 found the preserved [334-block milestone](../upper334/README.md).
The optimized seed 301 then found [333 blocks](../data/cover-333.txt). Seed 401
continued shrinking, reaching [324 blocks](../data/cover-324.txt) and later
producing a frozen 323-block partial input with five holes at step 863,969.
Seed 502 continued from that input, reaching [319 blocks](../data/cover-319.txt)
at step 722,768 and a 318-block partial with four holes before its time limit.
Seed 603 repaired that partial. Both intermediate partial snapshots, run
metadata and logs are included in `reproduction/`.

The current published Covering Repository upper bound was checked as 335 on
6 November 2026. This package establishes a local, explicitly checkable upper
bound; no submission, curator acceptance, or worldwide priority is claimed.
Perry Kern directed the AI-assisted work. The prior 335-block cover retains
its attribution in `upper335/`, and the original WLS2 algorithm retains
Wynand van Staden's attribution and license. The existing lower-bound proof
and its review status are unchanged.
