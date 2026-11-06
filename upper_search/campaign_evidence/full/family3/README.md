# Verified complete cover — final local campaign copy

`data/cover-302.txt` is a complete C(54,16,4) cover with302 distinct16-sets, SHA-256 `b02a347dfbc3254bd950ad1d13a0c17834792d4f089594b7feb513f5a874f684`. This is one retained search family; no optimality or publication claim is made.

From this directory:

```sh
python -B verification/verify_colex.py 54 16 4 data/cover-302.txt
python -B verification/verify_incidence.py data/cover-302.txt --expected-blocks 302
sha256sum -c SHA256SUMS
python -B replay.py --compile-only
python -B replay.py
```

The actual producing source/headers, MIT license, direct input, seed, argv, environment, metadata and winning-log snapshot are preserved under `reproduction/`. The input may itself be incomplete; its exact deficit is recorded in `verification/input.json`. Replay compiles portable C++17 into a fresh external directory. Wall-clock stopping and compiler differences may change reproduction; witness verification is deterministic. No fresh search replay is claimed by this packaging step.

`PACKET_ORIGIN.json` pins the original staged packet. This compact copy omits its platform binary and duplicate historical checkpoint witnesses. The original staged manifest and result remain under `provenance/`. The campaign stopped after the independently verified strict three-hour stall and final output drain. This local packet does not authorize publication.
