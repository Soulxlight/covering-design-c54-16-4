# Reviewed lower 230; retained upper 336

Read [PROOF.md](PROOF.md) first. The standalone proof excludes every indexed
18-occurrence (52,14,2) pair cover, including repeated whole rows, and all
smaller sizes by padding. Point-link counting then proves
C(53,15,3)>=68 and **C(54,16,4)>=230**. The recorded upper 336 and Franco Atzeni
credit remain unchanged; no upper witness or exact covering number is supplied.

Independent internal review is [PASS WITH LIMITS](REVIEW_STATUS.json), classifying
this as a complete computer-assisted ordinary proof with no mathematical gap
or required mathematical edit reported. Qualified external human acceptance,
proof-assistant verification and literature priority remain pending. The research,
manuscript and separate internal review used AI assistance under Perry Kern's
direction. No private correspondence is reproduced or treated as endorsement.

The dependency is ONLY this18-row contradiction, padding and the two lifts.
Neither previous 224, another lower-bound argument, selected 19-row systems,
later endpoint work, an avoidance lemma, a construction search nor a numerical
solver is a premise. Stage08 alone is inconclusive:63 of 70 macros and559 of 574
joint types exclude, leaving 15. Stage09's justified binary containment cap
excludes those15, with minimum gap686878/1225. Running only that refinement
does not reconstruct the preceding universe. The complete runner performs BOTH
stages and the third reviewer's full reconstruction.

Inspect the [assumption map](ASSUMPTION_CODE_MAP.md), [finite universes](ENUMERATIONS.md),
the complete [readable ledger](CASE_LEDGER.md), both pinned JSON records and the
three independent implementations. Positive trace-square minus rank times a
Frobenius UPPER bound is the exclusion direction; nonpositive earlier gaps are
retained honestly as inconclusive. Plain identical columns and repeated rows
remain allowed. Required producer sources/receipts are provided for hash binding;
verification reads their bytes and does not rerun them.

From the repository root, standard-library Python 3.10+:

```text
python -B audit230/verify230.py --check-manifest
python -B -O audit230/verify230.py --check-manifest
python -B audit230/run_corruption_checks.py
```

For a restricted temporary directory, create a writable scratch directory OUTSIDE
the repository and add `--work-dir PATH` to each command. All computations use
temporary copies and preserve the published files. Full-release validation with
an externally pinned manifest is described in [REPRODUCE.md](../REPRODUCE.md).
The two arithmetic JSON outputs must match; all 34 corrupt processes must reject
without a false-success file. Nothing in these commands publishes or uses a network.

Hashes bind inspected bytes, not mathematical truth. Generation-era status flags
in the frozen data remain unchanged, including their historical publication and
review-pending captions. The current review and publication status are recorded
separately. [Source provenance](SOURCE_PROVENANCE.json) and [changes](CHANGELOG.md)
explain every transformation; no certificate value or mathematical assumption changed.
