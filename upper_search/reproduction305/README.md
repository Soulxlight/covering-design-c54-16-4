# Replay the verified 305-block checkpoint

This directory is self-contained for compiling and rerunning the final search.
Its input has 305 blocks and **five uncovered quadruples**. The complete
certificate is [cover-305.txt](../../data/cover-305.txt).

The exact source is [wls_balance_sparse.cpp](source/wls_balance_sparse.cpp),
including [balance_move_sparse.hpp](source/balance_move_sparse.hpp), with the
original [MIT license](source/LICENSE). [REPLAY.json](REPLAY.json) records seed
1167, tenure 3, noise 0.05, the input hash, balancing environment, compiler
arguments and expected output hash. [original_metadata.json](original_metadata.json)
and [winning_run.log](winning_run.log) preserve the original run.

From the project root, with Python 3.10+ and a C++17 compiler:

```sh
python -B upper_search/reproduction305/replay.py --compile-only
python -B upper_search/reproduction305/replay.py
```

The driver compiles into a separate temporary directory and replays with
`targetB=305`. An explicit `--work-dir` must be outside this packet and empty.
Use `--native` for the original architecture-specific optimization flag;
`--seconds 1800` overrides the recorded 600-second budget on a slower machine.
The driver rejects failed processes and checks completed output with both
included exhaustive verifiers. It also reports whether the output bytes match
the original witness. The checked-in witness is the certificate; portable
compilation has been checked, and a fresh search replay is not claimed here.

`verification/input.json` independently confirms the initial five holes.
`verification/best.json` records both checks of the completed witness.
[INPUT_ANCESTRY.json](INPUT_ANCESTRY.json) indexes the preserved input recipes
and predecessor metadata; original absolute paths are provenance pointers,
while every file needed for the final search is included locally. Full replay
of ancestor searches is not claimed. The platform-specific binary is omitted.

From this directory, `sha256sum -c SHA256SUMS` checks its complete file inventory.
This packet preserves research performed with AI assistance under Perry Kern's
direction. The original WLS2 algorithm is attributed to Wynand van Staden.
No optimality, external acceptance or public submission is claimed.
