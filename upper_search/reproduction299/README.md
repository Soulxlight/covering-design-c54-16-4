# Reproduce the 299-block milestone

The complete witness is [cover-299.txt](../../data/cover-299.txt), SHA-256
`d0bf4dfd6f3c41f03d8ca8f5030eacefe04508b2ba5e0348e2a03dd3c21c33b3`. Its producing run is `run_21171`.
The actual direct input contains 299 blocks and 4 uncovered quadruples.
The input is incomplete and is not a cover.

`REPLAY.json` records the exact input hash, seed 21171, tenure 12,
noise 0.02, algorithm environment, and targetB=299. Source, required
headers, MIT license, original metadata and the run log are included. No platform
binary is distributed. The driver reruns only this winning phase, with the
recorded direct input; complete replay of its earlier ancestry is not claimed.

With Python 3.10+ and a C++17 compiler, from this directory:

```sh
sha256sum -c SHA256SUMS
python -B replay.py --compile-only
python -B replay.py
```

The portable build omits `-march=native`; `--native` restores that flag.
Generated outputs use a fresh external directory. Any new complete output must
pass both exhaustive verifiers. Timing and compiler changes can alter the search
trajectory; checking the pinned witness is deterministic. Successful packet
verification does not claim a new search replay.

Original WLS2 attribution to Wynand van Staden is retained in `source/LICENSE`.
Perry Kern directed the AI-assisted modifications and independent checking.
