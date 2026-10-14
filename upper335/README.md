# Verified upper bound C(54,16,4) <= 335

The exact [335-block witness](../data/cover-335.txt) consists of335 distinct
16-subsets of the labels1..54. Every one of the316251 four-subsets is contained
in at least one block. Two independently implemented exhaustive verifiers agree
on zero uncovered quadruples. This establishes an upper bound; optimality is
not claimed. The existing internally reviewed lower230 work is preserved.

The file is16415 bytes and has SHA256:

```text
f00db8b4253b98fecf412031948e7de4e5c5f78a9cc021ef483bb01ea9d84bc8
```

The original line and label order, trailing spaces and final LF are retained.
The parsers normalize blocks only in memory. The exact-byte pin is intentional;
an equivalent serialization with different newlines is a different byte file.

## Reproduce

From the repository root, using Python3.10+ and Node18+ with standard libraries:

```text
python -B upper335/verify_cover.py
python -B -O upper335/verify_cover.py
node upper335/verify_cover.js
python -B -m unittest discover -s tests -p test_cover335.py -v
```

Both verifiers require335 legal, pairwise distinct blocks of16 distinct labels
from1..54. Python independently builds point-to-block integer incidence columns
and intersects four columns for every target quadruple. Node independently
parses the raw rows, inserts all609700 block-quadruple occurrences in a Set of
integer colex ranks, then separately traverses all316251 target quadruples.
Neither implementation reads the other's output. Their published results are
in [VERIFICATION.json](VERIFICATION.json). Boundary controls retain uncovered
quadruples and repeated coverage; strict tests reject malformed rows, repeated
blocks and altered byte identity. No assertions disappear under Python-O.

The colex formula for increasing labels a<b<c<d is
choose(a-1,1)+choose(b-1,2)+choose(c-1,3)+choose(d-1,4). It bijects the target
four-subsets to0..316250, with exact integers below the floating-point integer
limit. The independent Python method uses no such rank formula.

## Attribution and status

Perry Kern directed this AI-assisted investigation and supplied the final
witness. According to Perry's account, Grok performed the final repair from
two uncovered quadruples to zero. This release independently checks the
resulting file; the repair trace and a complete construction ancestry are not
documented here. The project also used AI assistance for earlier research and
independent verification.

The prior336 upper-bound context credits Franco Atzeni and the Covering
Repository, as preserved in [CITATIONS.md](../CITATIONS.md). That attribution
concerns the earlier reference construction. General covering-design methods
and the project's previous lower-bound work retain their existing citations
and review qualifications.

A submission to the Covering Repository curator has been sent. Acceptance is
not confirmed at this publication. Exhaustive local verification, curator
acceptance, qualified external review and literature priority are separate
statuses. This release claims C(54,16,4)<=335 and no exact covering number.
