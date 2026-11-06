# NOT A COVER: 301 blocks with 19 uncovered quadruples

This is an incomplete C(54,16,4) search checkpoint. It does **not** establish
C(54,16,4) <= 301. The separately verified complete upper bound at staging
is 302. The exact missing quadruples are in `EXACT_HOLES.json`.

`partial.txt` has SHA-256 `e8b05593d30ff9f54e4bbdb1bf550686b3ca2964968a953d5e1ec01bfa112f60`. Both independent exhaustive
methods check all316,251 quadruples, report 316,232 covered and 19 uncovered,
and reconstruct the same complete hole list. `VERIFICATION.json` preserves their
reports. The copied cover verifiers correctly label this input incomplete.

Verify the packet using standard-library Python3.10+:

```sh
python -B verify_partial.py --check-manifest
python -B -O verify_partial.py --check-manifest
sha256sum -c SHA256SUMS
```

The packet checker exits zero when the pinned partial and its stated holes
match. Its result remains `VERIFIED_PARTIAL_NOT_A_COVER`.

## Continue searching

A C++17 compiler is needed for continuation. From this directory:

```sh
python -B continue_search.py --compile-only
python -B continue_search.py --seconds 3600 --seed 1319
```

The driver uses a fresh external work directory, compiles portable C++17, and
starts from these 301 blocks with targetB=301. `--native` retains the original
architecture-specific optimization flag; `--work-dir PATH` chooses an empty
external output directory. A new search initializes RNG, tabu state and dynamic
weights afresh. Compiler, runtime and random trajectories can affect outcomes.

The original producing run was `run_1319`, seed 1319, tenure
7, noise 0.05, using 301 blocks and
22 holes as its direct input. Exact source/header, license,
original direct input, metadata, input recipe and log are preserved under
`producer/`. `CONTINUATION.json` records the continuation settings.
It retains the producing run's algorithm environment, including NOWEIGHT and the absolute background hole cap. No platform-specific executable is distributed.

After a continuation search, exit zero requires a newly produced complete cover
that passes both exhaustive methods. Exit one means the time budget ended with
an incomplete checkpoint; `CONTINUATION_RESULT.json` retains its exact holes and
explicit `PARTIAL_NOT_A_COVER` status. Portable compilation and packet verification
were checked at staging; a fresh search continuation is not claimed.

The search adapts Wynand van Staden's MIT-licensed WLS2 with AI-assisted changes
under Perry Kern's direction. The original license is preserved with its source.
This local checkpoint claims no new upper bound, optimality, or publication.
