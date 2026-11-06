# Final local campaign evidence

The verified complete upper bound is C(54,16,4) <= 302. This bundle retains three pairwise non-isomorphic 302-block covers with their producing source, input, license, settings and portable replay drivers. It also retains explicitly incomplete 301-block checkpoints with 7, 8, 19 uncovered quadruples, plus five optional equal 7-hole neutral seeds. **None of the partial files is a cover.**

Verify all witnesses, exact partial deficits, recipe reconstructions and checksums without running search:

```sh
python -B verify_evidence.py
python -B -O verify_evidence.py
sha256sum -c SHA256SUMS
```

Each `full/` subdirectory has its own source replay instructions. Each `partial/` subdirectory has a self-contained ordinary continuation command and exact hole list. Those searches require a C++17 compiler; the verification commands above use standard-library Python 3.10+. The exact-repair partial also includes deterministic recorded-move reconstruction and its original model/solver records. Fresh search reproduction has not been claimed by packaging.

This is an upper-search evidence packet; it does not copy or replace the repository's lower 230 proof files. Their immutable baseline hashes are retained in `history/`, and their external-review status remains unchanged. `RESEARCH_NOTES.md` states method limits, including finite-pool restrictions and mixed-input experiments. `evidence/` preserves the family-invariant and recovery audits. `research/` contains the exact finite-pool capacity proof and the optional reproducible fixed-parent point-pair switching certificate; neither establishes a global lower bound. No optimality, curator acceptance, or external publication is claimed by this packet. The final stop and producer drain are independently recorded in evidence/FINAL_STOP_AUDIT.json.

The full-count improvement clock remains 2026-11-06T16:32:33.030679+00:00. Equal-size full covers and partial improvements do not reset it. The strict three-hour no-improvement condition, cross-lane quiescence and final rescan passed. Both full point-pair certificate replays also passed normally and with Python -O. The incomplete checkpoints remain available for a later search continuation.
