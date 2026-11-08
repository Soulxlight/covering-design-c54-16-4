# Reproduce the 301-block milestone

`input.txt` is the actual 301-block, one-hole input of run 21058. Its incomplete
status is explicit in `verification/input.json`. The complete witness is
`../../data/cover-301.txt`, SHA-256 `84b0b0692729a279c274c65ca07e67a405b2935803f6679e35ca434184c40602`.

From this directory with Python 3.10+ and a C++17 compiler:

```sh
sha256sum -c SHA256SUMS
python -B replay.py --compile-only
python -B replay.py
```

`REPLAY.json` records seed 21058, tenure 7, noise 0.01, targetB=301, the 173-second
budget and the actual algorithm/checkpoint environment. The original source,
required header and MIT license are under `source/`. The original platform
binary is omitted. Portable compilation drops `-march=native`; `--native`
retains it. Use `--seconds 1800` to extend the budget.
Generated files go to a fresh external directory; any new full output is checked
by both exhaustive methods. Timing/compiler changes can alter reproduction.
The record does not claim a fresh search replay merely from successful checks.

The actual search reached 301 blocks after 5,948,881 steps at 122.4 seconds.
`provenance/ancestry/` preserves preparation run 21057, its first one-hole input,
source, 1024-step settings and final state handoff. The winning input is the
verified terminal preparation state 0aca4d6e. Only the winning phase is invoked
by `replay.py`; complete replay of all ancestors is not claimed.

Original WLS2 attribution to Wynand van Staden is retained in `source/LICENSE`.
Perry Kern directed the AI-assisted modifications and independent verification.
