# Reproduce the 302-block checkpoint

`input.txt` is an incomplete 302-block design with exactly nine uncovered
quadruples. It is the actual immutable input used by run 1243. `source/` contains
the exact source/header and original MIT license; `original_metadata.json`
and `winning_run.log` retain the observed run. The resulting complete cover
is `../../data/cover-302.txt`, SHA-256 `96c6adca7d06f51c04a029a3a807978fed7ccd587a95abdc04cb1c4130fda4fd`.

From this directory, with Python 3.10+ and a C++17 compiler:

```sh
sha256sum -c SHA256SUMS
python -B replay.py --compile-only
python -B replay.py
```

The replay uses seed 1243, tenure 12, noise 0.02, targetB=302, and the exact
algorithm/checkpoint environment in `REPLAY.json`. Portable compilation omits
`-march=native`; `--native` retains it. `--seconds 1800` may extend the recorded
300-second budget. Outputs go to a fresh external directory; `--work-dir PATH`
must name an empty external directory. A failed process is rejected, and any
new complete output must pass both exhaustive verifiers. The recorded search
reached 302 blocks after 4,528,541 steps at 131.7 seconds. Compiler/runtime/timing
differences can affect replay. Portable compilation and both input/output
coverage checks passed; a fresh search replay is not claimed.

The final witness independently establishes the bound. Search replay is not
required to verify it. The nine-hole input is explicitly incomplete. No
platform-specific binary is included. The complete historical 305 reproduction
is retained separately in `../reproduction305/`.

The search adapts Wynand van Staden's MIT-licensed WLS2, with AI-assisted changes
under Perry Kern's direction. Original attribution is preserved in `source/LICENSE`.
