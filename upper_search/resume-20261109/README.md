# Paused research checkpoint — November 9, 2026

The user explicitly paused research to preserve remaining usage. All search
workers and the independent watcher have stopped. Nothing is scheduled to resume.
The historical clocks remain unchanged; paused wall time must not count as active
search stall in a future user-authorized session.

The verified complete upper bound is **297**, preserved in local commit
`2533512be428e70ff60eceb228992ba8a4e419bb` and [cover-297.txt](../../data/cover-297.txt).
This checkpoint adds restart data; it does not change the lower proof or claim
optimality, external acceptance, or publication.

**Every `partial-296-h2*.txt` file here is NOT A COVER.** Each has 296 distinct
16-point rows and misses exactly two of the 316,251 quadruples. The main seed's
holes are `{9,12,41,54}` and `{23,24,30,42}`. Exact hashes and all four seed hole
lists are in [PARTIALS.json](PARTIALS.json). Verify them without running search:

```sh
python -B upper_search/resume-20261109/verify_partials.py
```

[RESTART.json](RESTART.json) is the saved research guide. Its absolute workspace
paths locate larger immutable experiments retained outside Git; the small files
here are portable. The lower-bound qualification in the main repository remains
unchanged. [pause/](pause/) records the explicit user stop, matched producer
barriers, drained inbox, and stopped watcher. This was not a three-hour stall.

The main partial came from run 21289. Its actual direct input has 296 rows and
three holes; the input, original metadata and log are under [producer/](producer/).
The producer was unweighted; the example continuation below is a fresh weighted restart.
The exact source/header/license already exist under `upper_search/reproduction299/source/`
and their hashes are bound by [REPRODUCTION.json](REPRODUCTION.json).
The e5c5 seed is also reconstructed from the main seed by the included point trace.
Stochastic producer replay depends on timing; the archived witnesses themselves
remain independently checkable.

Only after the user explicitly requests another search, one portable continuation
from the main two-hole seed is:

```sh
g++ -O3 -std=c++17 upper_search/reproduction299/source/wls_background_sparse_equal_v2.cpp -o /tmp/c54-resume-wls
mkdir resume-output
cd resume-output
BACKGROUND_EVERY=128 BACKGROUND_CAP=6 BACKGROUND_START=1 SAVE_PARTIAL=best_partial.txt SAVE_FINAL=final_state.txt SAVE_EQUAL_PARTIAL=equal_partial.txt EQUAL_INTERVAL=1000 EQUAL_MAX_HOLES=2 /tmp/c54-resume-wls 54 16 4 296 300 21289 ../upper_search/resume-20261109/partial-296-h2.txt 3 0.05 296
```

This is a fresh bounded continuation, not an automatic resume or a promise to
reproduce identical output. Independently verify any output before using it as
a bound. For a coordinated multi-worker restart, follow the guide's fresh-session
clock and exclusive-lane rules instead of reviving old controls.

The saved local results have limited scope. The two-state neutral component is
closed only for nonworsening one-row paths from its pinned seed. The strict pair
portfolio leaves 24,503 nonrigid pairs untested. The latest 825-column pool reports
native SAT UNSAT at defect cap one; it has no separately checked UNSAT proof log
and implies no unrestricted lower bound. The 62-row/80-membership core union
preserves three complete local domains; its native solve was inconclusive.

[tools/](tools/) contains the reviewed and tiny-tested faster pair and generic
2/3-row SAT backends, requiring `python-sat` for their validators. They are local
repair tools, not complete covering-number solvers. No real new search or large
proof replay was run while saving this checkpoint.
