# Reproduction

1. Use Python 3.10 or newer; `requirements.txt` lists no third-party package.
2. From the release root, run `python verify.py` and `python -m unittest discover -s tests -v`.
3. To reconstruct the mathematical matrix separately, run `python verify.py --emit-rebuilt-matrix rebuilt.json`. The emitted file holds only variables and rows; the verifier already compares them with every corresponding entry in `data/model.json`. `rebuilt.json` is generated output and is not part of `SHA256SUMS`.

`verify.py` requires no LP solver. It hashes the byte-exact model and certificate, rebuilds all 5,332 domains/objective coefficients and 288 necessary rows, and evaluates the signed-row certificate using Python integers. The saved weights came from a numerical LP exploration, but a numerical solve is **not** a premise of the proof: the negative inequality is replayed exactly. The diagnostic profile with objective `-19318` confirms that the necessary-condition model is nonempty. Every block family satisfies the *full-range* third-moment identity. A hypothetical complete 221-block cover has triple degrees `4..104`, so its *restricted model objective* has `F=0`. Thus the certified `F<0` over the relaxed feasible domain excludes such a cover after the cover-to-model implications in the proof are checked.

Expected exact calculation:

```text
scale                         1,000,000,000
signed row bound sum       -2,660,294,744,798
finite-domain correction      88,273,944
numerator                 -2,660,206,470,854
F upper bound      -1,330,103,235,427 / 500,000,000
```

No downloaded scripts, full covering archive, credentials, paid service or external data are used. The external papers and record pages are linked in `CITATIONS.md` for attribution and independent reading.
