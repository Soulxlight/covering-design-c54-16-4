# NOT A COVER: 301 blocks with 8 holes

This incomplete C(54,16,4) checkpoint does not establish an upper bound of 301.
The complete upper bound at staging is 302. Both exhaustive
methods check all316,251 quadruples and agree on `EXACT_HOLES.json`.
Witness SHA-256: `90d3b8659234e50a3f481851dc6825157596dcb48d83d86e10bd056eadccd402`.

Verify with standard-library Python3.10+:

```sh
python -B verify_partial.py --check-manifest
python -B -O verify_partial.py --check-manifest
sha256sum -c SHA256SUMS
python -B reconstruct_recorded_partial.py
```

The producing job was exact-protected-point-cp, kind `exact-protected-point-cp`.
Engine/mode: `mip` / `exact-protected-point-cp`.
Seed: None; radius: see original kernel/settings; recorded budget: 80.0.
A null seed means that this metadata does not specify a random seed.
Its effective input had 301 blocks and 9 holes.
`producer/` preserves the original direct input, metadata, result/history log,
selected rows, dependency trace when present, immutable sources and license.
Recorded dependency versions: `{"highspy": "1.15.1", "numpy": "2.3.5", "ortools": "9.15.6755", "python-sat": "1.9.dev21"}`.
`reconstruct_recorded_partial.py` applies the recorded row changes and requires
the identical pinned bytes. It is deterministic witness reconstruction, not a
claim to rerun the original solver trajectory.

The original solver/model sources, result, log, certificate/kernel data and complete point-move trace are preserved. `python -B reconstruct_recorded_partial.py` deterministically reconstructs the recorded witness and requires byte-identical output plus both exhaustive coverage checks. This is replay of the recorded moves, not a fresh optimization run. `producer/solver_result.json`, when present, preserves the underlying solver status and numerical bounds; these do not claim a global covering-number lower bound.

To continue searching from the included partial with portable C++17 WLS:

```sh
python -B continue_search.py --compile-only
python -B continue_search.py --seconds 3600 --seed 1287
```

The continuation engine is copied from actual input-ancestor run
`run_1287` and preserved separately in `continuation_engine/`.
It is distinct from the exact producer. `CONTINUATION.json` pins source, settings,
environment and ancestry; targetB=301. RNG, tabu and dynamic weights start
afresh. Its actual absolute background cap is retained. `--work-dir PATH` must
be empty and external; `--native` enables the recorded architecture optimization.
Portable compilation is checked or reused only for identical source/header/flags.
No fresh continuation search is claimed. Every output is verified by both methods;
exit0 requires a complete cover, while exit1 explicitly reports remaining holes.

WLS adapts Wynand van Staden's MIT-licensed WLS2. Exact repair and WLS changes were
developed with AI assistance under Perry Kern's direction. Licenses are included.
This packet claims no new upper bound, optimality, or external publication.
