# Reproduce the complete public release

Python 3.10+; standard library only. Inspect PROOF.md and the executable source.
Acquire an expected 64-hex SHA256 for PUBLIC_MANIFEST.json from a trusted pinned
handoff or commit. Replace YOUR_TRUSTED_64_HEX_SHA256 in these commands:

```text
python -B verify_release.py --manifest-sha256 YOUR_TRUSTED_64_HEX_SHA256
python -B -O verify_release.py --manifest-sha256 YOUR_TRUSTED_64_HEX_SHA256
python -B audit230/run_corruption_checks.py
python -B -O audit230/run_corruption_checks.py
```

The release runner checks the exact whole-repository whitelist, preserved 222/223
arithmetic, all five 224 certificates and the COMPLETE 230 argument. For 230 it
reconstructs 70 macros, 574 joint types/2363 maxima and 15 refinements/48 maxima,
then repeats the full argument using the independent reviewer's actual-basis
bordering, partner-first enumeration and grouped row optimization. It also
checks the declared repeated-row, containment and all-ones toy boundaries.
No producer or cover solver is rerun, and no network is used.

The current proof establishes pair floor 19, child 68 and parent 230. The minimum
refined gap is 686878/1225; the weakest trace is 5458/35 and Frobenius upper is
3233654/1225. Read [PROOF.md](audit230/PROOF.md) and
[ENUMERATIONS.md](audit230/ENUMERATIONS.md) for why each finite universe contains
all actual cases and what the toy checks do not prove. Stage08's15 unresolved
types are deliberately preserved; Stage09 alone is not complete reproduction.

For only 230, from the root:

```text
python -B audit230/verify230.py --check-manifest
python -B -O audit230/verify230.py --check-manifest
```

These two mathematical JSON outputs must be identical. The corruption runner
regenerates all 17 reviewed false specimens and checks both interpreter modes,
34 explicit rejected processes with no false-success file. It checks missing
cases, coefficients, caps, row maxima, rank gaps, lifts and acceptance claims.
Assertions are not used for validation, so Python -O cannot erase the checks.

All 230 checks use temporary COPIES. If the default temporary directory is
restricted, create a writable scratch directory outside this repository and
append `--work-dir PATH` to the release runner,230 runner or corruption runner.
The chosen scratch child is verified to stay within that parent and removed
afterwards. Preserve the exact published files; use core.autocrlf=false. The
retained .gitattributes disables newline conversion. Frozen receipt comparison
uses parsed mathematics so generated platform newlines do not change the result.

Retained legacy checks:

```text
python -B verify.py
python -B -O verify.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

Expected 222 certificate: 5332 variables, 288 rows,
F<=-1330103235427/500000000. The scout 223 certificate has 975 variables, 156 rows,
F2<=-121049912921/100000000; the analytic child route has contradictions -7086
and -63. The224 case coefficients and certificates remain in their original packet.
SHA256SUMS and audit/PUBLIC_MANIFEST.json retain the old 38-path subset domain
with refreshed hashes for mutable entry-point documents. PUBLIC_MANIFEST.json
and PUBLIC_SHA256SUMS cover the whole current release. Hashes prove neither a
semantic implication nor authentication of a replaced code/manifest set.

Independent internal review is PASS WITH LIMITS for the complete ordinary 230
proof. Qualified external human acceptance, formal-kernel verification and
priority remain pending. No exact covering number, upper witness, 335 cover or
external endorsement is supplied. The recorded upper 336/Franco Atzeni credit
is unchanged. These commands verify files and arithmetic; they do not publish.
