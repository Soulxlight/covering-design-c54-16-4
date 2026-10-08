"""Independent exact verifier for the C(54,16,4) >= 222 certificate.

Python standard library only. This rebuilds the necessary-condition matrix
from counting formulas and checks the saved rational dual without an LP solver.
The third-moment identity itself is standard; see CITATIONS.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path


MODEL_SHA256 = "3f65a5e44b96d0ee5844176331b4b5172ba267f29479e995f3d744d4acca1c24"
CERT_SHA256 = "9483912feec907e2f4b2118d1ebd2d83bcf881602d41ecbdf8d5674e03c0d973"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def matrix() -> tuple[list[dict], list[dict]]:
    """Rebuild every physical domain, objective coefficient, and row."""
    v, k, b, base_point, base_pair, cap = 54, 16, 221, 64, 18, 86
    point_excess = b * k - v * base_point
    pair_excess = b * comb(k, 2) - comb(v, 2) * base_pair
    require((point_excess, pair_excess) == (80, 762), "incidence totals")
    variables: list[dict] = []
    rows: list[dict] = []

    def variable(name: str, upper: int, objective: int = 0) -> None:
        variables.append(dict(name=name, lower=0, upper=upper, objective=objective))

    def row(label: str, terms: dict[str, int], lower: int = 0,
            upper: int | None = 0) -> None:
        rows.append(dict(label=label,
                         coefficients={name: value for name, value in terms.items() if value},
                         lower=lower, upper=upper))

    def series(prefix: str, lo: int, hi: int, function) -> dict[str, int]:
        return {f"{prefix}{i}": function(i) for i in range(lo, hi + 1)}

    for s in range(k + 1):
        variable(f"n{s}", comb(b, 2), -comb(s, 3))
    for d in range(point_excess + 1):
        variable(f"u{d}", v)
    for e in range(cap + 1):
        variable(f"p{e}", comb(v, 2))
    for m in range(4, base_pair + cap + 1):
        variable(f"t{m}", comb(v, 3), comb(m, 2))
    for e in range(cap + 1):
        for m in range(4, base_pair + e + 1):
            variable(f"M{e}_{m}", (v - 2) * comb(v, 2))

    row("block_pairs", series("n", 0, k, lambda _: 1), comb(b, 2), comb(b, 2))
    row("point_profile", series("u", 0, point_excess, lambda _: 1), v, v)
    row("point_excess", series("u", 0, point_excess, lambda d: d),
        point_excess, point_excess)
    row("point_intersection", {
        **series("n", 0, k, lambda s: s),
        **series("u", 0, point_excess, lambda d: -comb(base_point + d, 2))})
    row("pair_profile", series("p", 0, cap, lambda _: 1), comb(v, 2), comb(v, 2))
    row("pair_excess", series("p", 0, cap, lambda e: e), pair_excess, pair_excess)
    row("pair_intersection", {
        **series("n", 0, k, lambda s: comb(s, 2)),
        **series("p", 0, cap, lambda e: -comb(base_pair + e, 2))})
    row("triple_profile", series("t", 4, base_pair + cap, lambda _: 1),
        comb(v, 3), comb(v, 3))
    row("triple_load", series("t", 4, base_pair + cap, lambda m: m),
        b * comb(k, 3), b * comb(k, 3))
    row("tight_intersection3", {"n3": 1, "t4": -5}, 0, None)
    row("tight_intersection4", {"n4": 4, "t4": -1}, 0, None)
    row("tight_pair_triples", {"t4": 3, "p0": -8}, 0, None)
    row("tight_pair_transport", {"M0_4": 1, "p0": -8}, 0, None)
    for e in range(cap + 1):
        count = {f"M{e}_{m}": 1 for m in range(4, base_pair + e + 1)}
        load = {f"M{e}_{m}": m for m in range(4, base_pair + e + 1)}
        count[f"p{e}"] = -(v - 2)
        load[f"p{e}"] = -(k - 2) * (base_pair + e)
        row(f"transport_count{e}", count)
        row(f"transport_load{e}", load)
    for m in range(4, base_pair + cap + 1):
        terms = {f"t{m}": -3}
        terms.update({f"M{e}_{m}": 1 for e in range(cap + 1) if m <= base_pair + e})
        row(f"transport_column{m}", terms)
    require((len(variables), len(rows)) == (5332, 288), "matrix dimensions")
    return variables, rows


def validate_model(model: dict, expected_variables: list[dict],
                   expected_rows: list[dict]) -> None:
    require(model["parameters"] == [54, 16, 4, 221], "model parameters")
    require(model["pair_excess_cap"] == 86, "pair excess cap")
    require(model["objective_sense"] == "maximize", "objective sense")
    require(model["variables"] == expected_variables, "variable domains/objective mismatch")
    require(model["rows"] == expected_rows, "necessary-condition matrix mismatch")


def validate_diagnostic(model: dict) -> int:
    """Check that the weaker profile system itself has an integer solution."""
    witness = model["feasible_integer_diagnostic"]
    require(set(witness) <= {v["name"] for v in model["variables"]}, "diagnostic names")
    for variable in model["variables"]:
        value = witness.get(variable["name"], 0)
        require(type(value) is int and 0 <= value <= variable["upper"],
                "diagnostic domain: " + variable["name"])
    for constraint in model["rows"]:
        value = sum(a * witness.get(name, 0)
                    for name, a in constraint["coefficients"].items())
        require(value >= constraint["lower"] and
                (constraint["upper"] is None or value <= constraint["upper"]),
                "diagnostic row: " + constraint["label"])
    objective = sum(variable["objective"] * witness.get(variable["name"], 0)
                    for variable in model["variables"])
    require(objective == model["feasible_integer_diagnostic_objective"] == -19318,
            "diagnostic objective")
    return objective


def replay_certificate(model: dict, certificate: dict) -> Fraction:
    """Apply exact signed row weights and every finite upper correction."""
    scale = int(certificate["denominator"])
    require(scale == 1_000_000_000, "certificate scale")
    weights = [int(value) for value in certificate["row_numerators"]]
    require(len(weights) == len(model["rows"]), "dual row count")
    sums = {variable["name"]: 0 for variable in model["variables"]}
    signed_bound = 0
    for weight, constraint in zip(weights, model["rows"]):
        require(weight <= 0 or constraint["upper"] is not None,
                "positive weight on unbounded row")
        bound = constraint["upper"] if weight > 0 else constraint["lower"]
        signed_bound += weight * bound
        for name, coefficient in constraint["coefficients"].items():
            sums[name] += weight * coefficient
    positive_residuals = {}
    correction = 0
    for variable in model["variables"]:
        name = variable["name"]
        residual = scale * variable["objective"] - sums[name]
        if residual > 0:
            positive_residuals[name] = str(residual)
            correction += residual * variable["upper"]
    require(positive_residuals == certificate["positive_column_residuals"],
            "positive residual list mismatch")
    require(signed_bound == int(certificate["row_bound_sum_numerator"]),
            "signed row bound mismatch")
    require(correction == int(certificate["finite_bound_correction_numerator"]),
            "finite correction mismatch")
    upper = Fraction(signed_bound + correction, scale)
    require(upper == Fraction(certificate["exact_objective_upper_bound"]),
            "exact bound mismatch")
    require(upper == Fraction(-1330103235427, 500000000) and upper < 0,
            "nonnegative or unexpected bound")
    return upper


def verify_files(data_dir: Path) -> dict:
    model_path, cert_path = data_dir / "model.json", data_dir / "certificate.json"
    model_bytes, cert_bytes = model_path.read_bytes(), cert_path.read_bytes()
    require(hashlib.sha256(model_bytes).hexdigest() == MODEL_SHA256, "model SHA-256")
    require(hashlib.sha256(cert_bytes).hexdigest() == CERT_SHA256, "certificate SHA-256")
    model, certificate = json.loads(model_bytes), json.loads(cert_bytes)
    require(certificate["model_sha256"] == MODEL_SHA256, "certificate model pin")
    expected_variables, expected_rows = matrix()
    validate_model(model, expected_variables, expected_rows)
    diagnostic = validate_diagnostic(model)
    upper = replay_certificate(model, certificate)
    return {"status": "PASS_EXACT_CERTIFICATE", "variables": len(expected_variables),
            "rows": len(expected_rows), "diagnostic_objective": diagnostic,
            "exact_F_upper": str(upper),
            "conclusion": "No complete 221-block cover, given the documented map from complete covers to the necessary rows."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--emit-rebuilt-matrix", type=Path,
                        help="Write independently rebuilt variables/rows as JSON")
    args = parser.parse_args()
    result = verify_files(args.data)
    if args.emit_rebuilt_matrix:
        variables, rows = matrix()
        args.emit_rebuilt_matrix.write_text(
            json.dumps({"variables": variables, "rows": rows}, indent=2) + "\n",
            encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
