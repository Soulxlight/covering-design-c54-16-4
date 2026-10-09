# Transparent changes from frozen inputs

Baseline: GitHub main `946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35`.
Frozen source bytes are identified in SOURCE_PROVENANCE.json. No original
workspace input was edited. Exact public data values and proof assumptions
remain fixed.

| File/group | Change | Mathematical effect |
| --- | --- | --- |
| Original `data/model.json`, `data/certificate.json` | No change | Public222 certificate values and domains preserved |
| Original proof files, `verify.py`, `tests/test_verify.py`, `LICENSE`, `requirements.txt` | No change | Existing public proof/code/rights preserved |
| `README.md`,`REPRODUCE.md`,`CITATIONS.md` | Add audit navigation, proposed223 status and reproduction | No replacement of public222 statement by an externally accepted223 claim |
| `audit/PROOFS.md` | New numbered editorial exposition of both222 and223, full arithmetic and shared direct floor | No altered certificate, additional cover restriction or claimed priority |
| `audit/SEMANTIC_CERTIFICATE_223.md` | Byte-for-byte copy of independent reviewer six-step certificate | Same mathematical statements, with explicit review limits |
| `audit/data/scout/*` | Two byte-for-byte copies of frozen model/certificate | All975 variables,156 rows and exact weights preserved |
| `audit/data/support/*` | Eight byte-for-byte copies of frozen support JSON/CSV | Full finite support data and witnesses preserved |
| `audit/independent222.py` | Fresh formula implementation; imports no baseline verifier/generator | Independent coefficient reconstruction and exact replay |
| `audit/independent223.py` | Adapt reviewer reconstruction to relative public data; remove private path/integrity/output machinery | Core model, arithmetic, graph and toy formulas unchanged |
| `audit/verify_audit.py`,`audit/run_checks.py`,`tests/test_audit.py` | Explicit exceptions, all coefficient typing, saved graph checks, both-mode parity and deliberate corruptions | Reject incomplete, malformed, mutated or unsafe validation inputs; no changed premise |
| `audit/DEPENDENCIES.md`,`ENUMERATIONS.md`,`ATTRIBUTION.md`,`REVIEW_LIMITS.md` | New reviewer explanations | Distinguish semantic proof, exact arithmetic, finite checks and search history |
| `audit/receipts/*`,`audit/PUBLIC_MANIFEST.json`,`SHA256SUMS` | New complete public receipts and whitelist hashes | Integrity evidence, not proof of semantic correctness or authorship |
| `.gitattributes` | Disable automatic text conversion so every public byte hash survives Windows/Linux checkout | Frozen CRLF certificate/model bytes and original committed documentation bytes preserved |

The original frozen staging README predates the baseline's MIT decision;
the actual baseline LICENSE and README govern this package. No obsolete
licensing statement from staging is copied into the new documentation.
Producer scripts using `assert` are provenance inputs, not public
verification dependencies. Their optimized zero exit alone is not evidence.

Excluded from publication: private email, absolute installed paths,
execution environment inventory, session/account metadata, internal logs,
exploratory solver artifacts, unreviewed later research and unrelated
construction work. The generalized avoidance addendum is not incorporated.
No GitHub write, deployment, external contact, account or paid computation
is part of this handoff.

Git initially converted the baseline's LF documentation into CRLF in the
Windows checkout. Before sealing, unchanged baseline files were restored
to their exact committed blob bytes; this creates no Git content change.
The frozen JSON and copied reviewer/support files retain their source
bytes. New prose/code is emitted with LF. Explicit `* -text` attributes
prevent a future checkout from silently changing a manifested byte hash.

## Revision02 after the independent final publication gate

The original39-file packet and all handoff bytes are frozen. The final
independent review found no mathematical or privacy flaw, but publication
was conditional on release-verification fixes. This separate revision:

- fixes `verify_manifest` to require the exact ordered38 canonical paths
  independently of the manifest, plus explicit schema/entry/hash typing;
- adds five unit tests covering empty/missing/unexpected inventories,
  equal-count substitution, four path aliases and duplicate paths;
- adds seven file-level inventory corruption cases in each Python mode,
  including an empty manifest paired with empty SHA256SUMS;
- documents a clean dedicated Windows patch application and forced
  byte-restoring index checkout, with fresh two-mode replay evidence;
- qualifies the two historical216..336 /216..350 table observations and
  the fresh reviewer's access limits in CITATIONS.md, the root README and
  audit attribution, so entry-point wording implies no fresh table check;
- regenerates test receipts, checksums, manifest, exact base diff, and a
  separately named report/ZIP; independent re-review remains pending.

The original broad corruption-rejection wording referred to its tested
model/certificate/support corruptions; the original checker did not reject
an empty manifest with empty checksums. Revision02 explicitly repairs and
tests that missing integrity case. No mathematical hypothesis, certificate
number, copied data file, original222 proof/code or compact semantic
certificate changes. Hashes establish integrity, not authenticity of a
validator replaced together with all its hashes.
