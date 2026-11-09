> Historical 301-block checkpoint. Its frozen records are [RESULT-301.json](RESULT-301.json) and [VERIFICATION-301.json](VERIFICATION-301.json). The generic `verify_best.py` follows the current result; verify this historical witness directly with `python -B upper_search/reproduction301/verification/verify_colex.py 54 16 4 data/cover-301.txt` from the repository root. The original checkpoint text follows unchanged.

# Verified upper bound C(54,16,4) ≤ 301

The [301-block witness](../data/cover-301.txt) contains 301 distinct legal 16-subsets
of points 1 through 54 and covers all 316,251 quadruples. Two independent exhaustive
checks agree. This improves the November 6 bound 302 by one block and the supplied
335-block incumbent by 34 blocks. Optimality is not claimed.

Witness SHA-256: `84b0b0692729a279c274c65ca07e67a405b2935803f6679e35ca434184c40602`.
The first owner verification was 2026-11-08T19:51:33.674693+00:00; the independent
watcher confirmed it at 19:51:43.929677 UTC. [RESULT.json](RESULT.json),
[VERIFICATION.json](VERIFICATION.json) and [INDEPENDENT-301.json](INDEPENDENT-301.json)
pin those separate records. The resumed search continues toward 300 blocks.
This repository checkpoint is not a final campaign-stop report.

## Verify the witness

From the project root with standard-library Python 3.10+:

```sh
python -B upper_search/verify_best.py
python -B -O upper_search/verify_best.py
```

One checker enumerates each block's quadruples by colex rank. The other
intersects point-to-block incidence bitsets for every target quadruple.
Both enforce the exact count, distinct legal blocks, pinned hash and zero holes.

## Reproduce the recorded search

[reproduction301](reproduction301/README.md) preserves the actual source/header,
MIT license, direct input, settings, seed and log snapshot. No executable is
distributed. Its direct input has 301 blocks and one uncovered quadruple,
SHA-256 `0aca4d6eece82a9278391c5a1cb5fc676b661e6dc6bf45cb4cfa82d3c02f3937`.
Run 21058 used seed 21058, tenure 7, noise 0.01, unweighted target scores, and
`BACKGROUND_EVERY=128`, `BACKGROUND_CAP=5`, `BACKGROUND_START=1`.
It found the cover after 5,948,881 steps, at 122.4 seconds of its 173-second budget.

```sh
python -B upper_search/reproduction301/replay.py --compile-only
python -B upper_search/reproduction301/replay.py
```

The portable driver compiles the pinned C++17 source and uses targetB=301.
It requires a fresh external output directory and verifies any newly produced
cover by both exhaustive methods. Compiler/runtime differences and timing may
change the search trajectory. Search replay is not required to verify the bound,
and no fresh search replay is claimed by this checkpoint.

The input came from registered preparation run 21057, which started at the
first one-hole parent 278f2de9 and ran 1024 bounded neutral steps. Its verified
terminal one-hole state was passed to run 21058 through a durable handoff.
The preparation source, input, metadata, log and experiment recipe are included
in [the ancestry record](reproduction301/provenance/INPUT_ANCESTRY.json).
This preserves the observed lineage; it does not claim preparation was necessary
or replay every earlier ancestor.

## Preserved history and attribution

The [302 checkpoint](README-302.md), all `reproduction302/` bytes and the
[November 6 final campaign evidence](campaign_evidence/README.md) remain unchanged.
That historical packet retains three 302 covers, incomplete 301 restarts with 7, 8, 19
holes, local research records and its own final stop receipts. Those old partials
remain incomplete. The 305, 318, 334 and335 milestones and all lower-proof files
are also retained. The [size ledger](campaign_improvements.jsonl) is append-only.

The search adapts Wynand van Staden's MIT-licensed WLS2. Perry Kern directed
the AI-assisted search and independent checking; original license attribution
is preserved. The public Covering Repository displayed 302 on November 8;
[the dated receipt](PUBLIC_BOUND-20261108.json) does not identify its unavailable
block list with a local witness or infer acceptance or priority.

The internally reviewed lower bound 230 and its pending qualified external-review
status remain unchanged. No external publication, upload or push was performed
for this checkpoint. [SESSION-20261108.json](SESSION-20261108.json) distinguishes
the live session from the preserved November 6 stopped campaign.
