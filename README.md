# A lower bound certificate for C(54,16,4)

`C(v,k,t)` is the smallest number of `k`-subsets of a `v`-point set needed so that every `t`-subset is contained in a chosen block. Here there are `binom(54,4)=316,251` quadruples. The proofs in this packet support

```text
222 <= C(54,16,4) <= 336.
```

The upper value is the [Covering Repository's displayed construction](https://coveringrepository.com/systems.aspx?li=2), viewed 2026-10-08. The repository credits **Franco Atzeni** on that 336-block row and notes an LJCR multiple of `(27,8,4)`. This packet does not include or improve that construction. The lower value is a local counting argument and exact certificate. It has undergone internal mathematical and computational checking but **has not been externally peer reviewed**. Its **literature novelty and priority are unconfirmed**. No 335-block cover is claimed.

This research, its proof drafts, computations and release preparation used AI assistance. The exact verifier is supplied so that readers can check the arithmetic without trusting the AI, an LP solver or a numerical optimization status. The semantic argument connecting any hypothetical cover to the matrix is written in the proofs and merits independent human review.

## Contents

| File | Purpose |
| --- | --- |
| [`proofs/LOWER_BOUND_221.md`](proofs/LOWER_BOUND_221.md) | Analytic exclusion of 216 through 220 blocks, after the 216 incidence floor |
| [`proofs/LOWER_BOUND_222.md`](proofs/LOWER_BOUND_222.md) | Necessary-condition model, third-moment identity, exact certificate proof excluding 221 |
| [`data/model.json`](data/model.json) | Frozen 5,332-variable, 288-row integer-coefficient model, SHA-256 `3f65a5e44b96d0ee5844176331b4b5172ba267f29479e995f3d744d4acca1c24` |
| [`data/certificate.json`](data/certificate.json) | Frozen exact signed-row certificate, SHA-256 `9483912feec907e2f4b2118d1ebd2d83bcf881602d41ecbdf8d5674e03c0d973` |
| [`verify.py`](verify.py), [`tests/test_verify.py`](tests/test_verify.py) | Independent matrix reconstruction, exact replay and adversarial tests |
| [`CITATIONS.md`](CITATIONS.md) | Source attribution and limits on contribution claims |

The standard third-moment identity `F=0` follows from Soicher's 2010 Corollary 2.2; LP/IP use of these identities is also discussed there. Cameron and Soicher developed the block-intersection polynomial framework. [Details and links](CITATIONS.md). A potential contribution here is limited to the parameter-specific tight-link coupling and its exact numerical certificate.

## Check the certificate

Use Python 3.10 or newer. No packages, accounts or network access are required.

```sh
python verify.py
python -m unittest discover -s tests -v
```

The verifier rebuilds all model coefficients and bounds from the formulas, checks the hashes of the frozen model and certificate, validates a feasible diagnostic profile for the relaxed model, and applies every signed row weight and positive finite-domain correction with exact integers. Expected output includes `PASS_EXACT_CERTIFICATE`, 5,332 variables, 288 rows and `F <= -1330103235427/500000000`. See [`REPRODUCE.md`](REPRODUCE.md) for matrix regeneration and checks.

## Provenance and rights

The two readable proof files are editorial release copies of frozen research proofs; the numerical model rows, inequalities and certificate values are unchanged. The 222 copy clarifies that the moment identity for *arbitrary* block families uses the full triple-degree range; only a complete 221-block cover is restricted to degrees 4..104. It also states the padding argument that extends a 221-block exclusion to all smaller sizes when repeated occurrences are allowed. The source proof SHA-256 hashes were `b92fc6596391731a81a87b64d489a567e150f04a32828807b8b4dab1374a4910` (221) and `e877df2b96ffe2e12a9d75ef9dfc988af9ca2c33298ddb28788f13672a5568db` (222). Other edits add attribution, update file links, and remove internal workflow prose. The model and certificate are byte-for-byte copies. [`SHA256SUMS`](SHA256SUMS) identifies the exact release files.

**License choice is undecided.** No MIT, Creative Commons or other reuse license is granted by this packet.
