# Reproduction of the complete proposed224 audit

Use Python3.10 or newer, standard library only, from the repository root.
No solver, package installation, network, account or external data is used.
Supply the overall manifest SHA256 from the independent release handoff:

```sh
python -B verify_release.py --manifest-sha256 <handoff-manifest-sha256>
python -B -O verify_release.py --manifest-sha256 <handoff-manifest-sha256>
python -B audit224/run_checks224.py
python -B audit224/check_release_inventory.py
python -B audit/run_checks.py --check-manifest
```

Replace the placeholder with the literal64-character digest, without angle
brackets. `verify_release.py` first checks the fixed exact whitelist and every
member against the independently supplied manifest, then calls the222/223
auditor, unchanged224 packet verifier, closed-form arithmetic index and
published-formula comparison. It rechecks integrity afterward. Only `.git`
at the root is excluded from on-disk inventory; place fresh output outside
the release directory and use `-B` to avoid bytecode caches. Symlinks are
rejected; junctions are also rejected when the Python Path API exposes them.
No Windows privilege changes are required or requested.

The unchanged standalone224 command is:

```sh
python -B audit224/package/verify.py --manifest-sha256 d5ebe7dba35a94b99675c670616a99c5d669760732b8f3e7cf9a935555a78308
python -B -O audit224/package/verify.py --manifest-sha256 d5ebe7dba35a94b99675c670616a99c5d669760732b8f3e7cf9a935555a78308
```

It reports47 manifested members plus its manifest, all five strict negative
certificate bounds,584 child arithmetic checks,395010 labeled excess profiles,
125 padding toy multisets/1500 moment contexts and51 in-memory rejections.
The [fresh physical controls](audit224/receipts/TEST_RECEIPT.json) additionally
reject modified model/certificate bytes, missing/extra files, malformed
inventories, duplicate JSON keys and a wrong external pin in both modes.
Structural fixtures recompute their external test pin so integrity rejection
does not mask the malformed-inventory test. See [all finite universes](audit224/ENUMERATIONS.md).
The separate complete-release runner similarly rejects malformed overall
manifests and missing or extra release/checksum members in both modes.

The original222 commands remain valid:

```sh
python -B verify.py
python -B -O verify.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

Expected222 result:5332 variables,288 rows,
F<=-1330103235427/500000000. The intermediate scout223 result has975
variables,156 rows,F2<=-121049912921/100000000; the analytic child route
contradicts64 and65 occurrences with -7086 and -63 respectively.
The five224 certificate values are in the numbered manuscript and case ledger.
Every public audit condition uses explicit failure checks; normal/-O exact
mathematical receipts match and corruption exits remain nonzero.

The complete handoff includes an exact Git patch against
946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35, a public whitelist, source hashes
and fresh receipts. Inspect/apply it only in a new dedicated clean checkout.
Use `core.autocrlf=false`; the included `.gitattributes` preserves all bytes.
The patch and package are independent handoff deliverables, not extra files
to copy inside this exact release inventory. Publication is separately gated
by final editorial review and parent coordination; these commands do not publish.

Hashes authenticate neither a fully replaced verifier/manifest set nor the
semantic necessity of a row. Pin the handoff bytes, inspect the code and read
the [assumption-to-code map](audit224/ASSUMPTION_CODE_MAP.md). No formal kernel,
qualified human acceptance or certified priority is supplied.
