# Verified 334-block milestone for C(54,16,4)

The exact [334-block witness](../data/cover-334.txt) contains 334 distinct
16-subsets of labels 1 through 54. Exhaustive enumeration verifies that every
one of the 316,251 four-subsets is contained in at least one block. This proves
the upper bound 334; it does not establish optimality or a lower bound. This
directory preserves the 334-block milestone even when subsequent searches
produce smaller covers. It is not a claim that 334 remains the best bound.

The witness SHA-256 is:

```text
961691b0e66f690460d652b75d949e547862c01394ae11fcdf6ba4ca17e16107
```

## Verify

From the repository root, using Python 3.10 or later with its standard library:

```sh
python -B upper334/verify_colex.py 54 16 4 data/cover-334.txt
python -B upper334/verify_incidence.py
python -B upper334/validate_controls.py
```

The two implementations do not use search-engine state. The first enumerates
the four-subsets of every block and marks a colex-ranked coverage array. The
second enumerates every quadruple of points and intersects their block-incidence
bitsets. Both reject malformed blocks and duplicate blocks. The incidence
verifier additionally requires exactly 334 blocks. Saved receipts and negative
controls are in [validation](validation/). To check a later witness, supply its
path and `--expected-blocks N` to the incidence verifier; the colex verifier
accepts an arbitrary block count and prints the observed count.

## Reproduce the search

The successful search started from the unchanged
[335-block witness](../data/cover-335.txt), using seed 201, tabu tenure 7, and
noise 0.05. It reached 334 blocks after 48,542 steps (11.3 seconds in the original
environment). The exact source, original log, and original execution metadata
are [wls64.cpp](wls64.cpp), [search.log](search.log), and
[search_result.json](search_result.json).

From the repository root, compile and run in a fresh output directory:

```sh
g++ -O3 -march=native -std=c++17 upper334/wls64.cpp -o /tmp/c54-wls64
mkdir -p /tmp/c54-reproduction
cover_input="$(pwd)/data/cover-335.txt"
cd /tmp/c54-reproduction
SAVE_PARTIAL=best_partial.txt /tmp/c54-wls64 54 16 4 335 1800 201 "$cover_input" 7 0.05 334
```

The resulting witness is named `shrink_cover_54_16_4_334_201.txt`. Validate it with
both scripts above. Runtime depends on the machine. Exact random trajectories
may depend on the compiler and C++ standard library; the checked-in witness and
its exhaustive verification are the certificate. The search metadata retains
the original environment's absolute paths as provenance, rather than portable
paths. This source uses 64-bit point masks and rejects `v > 64`.

## Attribution and scope

The search code derives from Wynand van Staden's
[covering-design-records](https://github.com/WynandVStaden/covering-design-records),
`v2/wls2.cpp`, source blob `9e2769fc0c661483ced24b541e521a29a2d89ebe`.
The successful variant adds progress and partial-witness saving and uses
64-bit masks for this problem. The original MIT license is preserved in
[third_party/WLS2-LICENSE](third_party/WLS2-LICENSE).

This package records a locally verified improvement over the supplied
335-block incumbent. It does not claim independent confirmation of worldwide
priority or submission to a public covering repository. Existing lower-bound
and 335-block research artifacts are preserved separately.
