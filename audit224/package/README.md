# C(54,16,4) >= 224: reproducibility package, version 01

This package is separate from earlier 222/223 artifacts. It contains no
private correspondence, host paths, inventories, publication ledgers,
accounts, or construction witnesses. Mathematical source documents may
retain historical pending-review language; the included review projections
and report record the subsequently completed reviews.

Requirements: Python 3.10 or newer, standard library only. No installation,
solver, network service, or private research archive is required. Unzip the
package, then run from its root:

```
python -B verify.py --manifest-sha256 <the supplied 64-character manifest hash>
python -B -O verify.py --manifest-sha256 <the same supplied manifest hash>
```

The checker prints a JSON receipt and exits nonzero on failure. Its checks
use explicit exceptions and remain active under Python -O. No package file
is written. The externally supplied hash is mandatory: a checker and
manifest replaced together cannot authenticate themselves. The file
SHA256SUMS.txt next to the delivered ZIP records the final hashes; keep
the separately supplied delivery hash as the trust anchor.

Read REPORT.md, proof/CHILD_BOUND_66.md, proof/ASSEMBLY.md, then the common
model and the five case maps identified in PROOF_DEPENDENCIES.json.
cases/*/MODEL.json and CERTIFICATE.json are unchanged frozen mathematical
inputs. audits/reconstruct_*.py contain only the independently written
reconstruction, validation, required constants, and standard-library
imports extracted from the reviewed sources. All private file I/O,
historical local launchers, and review-main functions have been omitted.
PROVENANCE.json gives original-source and packaged-byte hashes and every
declared transformation; raw source hashes inside model metadata remain
historical provenance, not unavailable runtime dependencies.

Explicit fail-closed checks cover an exact file whitelist, missing files,
extra files, symlinks, unsafe relative paths, duplicate JSON keys,
nonintegral coefficients/domains, every reconstructed coefficient,
n16 (equal whole-block intersections), exactly five profiles, strict
negative upper bounds, all signed endpoints, all residual corrections,
the reviewed child premise, required proof assets, and a complete acyclic
dependency graph. In-memory corruption controls independently exercise
the structural, arithmetic, and dependency checks, not just hash checks.

This package reproduces exact model reconstruction and arithmetic. It
does not convert the arbitrary-cover semantic maps into proof-assistant
theorems. All five case maps and their global junction passed internal
ordinary mathematical review with limits. Formal-kernel verification,
qualified human acceptance, and literature priority remain outstanding.
