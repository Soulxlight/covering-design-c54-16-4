"""Exact evaluations of identified published bounds, with stated inputs/limits."""
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def ceiling(value):
    return -(-value.numerator // value.denominator)


def cb(v, k, s, bs, alpha, beta):
    return F(comb(v, s)) * (bs * (alpha - beta) + alpha) / (comb(k, s) * (alpha - beta) + 1)


def main():
    # Floors 4/18 are derived from the identified published link and pair result;
    # 64/216 are their recurrence consequences, not an assumption of this project.
    pair_v, pair_k, r, d, n = 52, 14, 4, 1, 3
    need(51 == r * 13 - d and d < n, "Horsley pair parameters")
    first = F(pair_v * (r + 1), pair_k + 1)
    alpha, beta = F(23, 24), F(1, 6)
    stronger = cb(pair_v, pair_k, 1, r, alpha, beta)
    need(ceiling(first) == ceiling(stronger) == 18, "published pair floor")
    floors = {4: 1, 3: ceiling(F(51, 13)), 2: 18, 1: ceiling(F(53 * 18, 15))}
    target = ceiling(F(54 * floors[1], 16))
    need(floors == {4: 1, 3: 4, 2: 18, 1: 64} and target == 216, "published recurrence chain")
    cases = []
    for v, k, t, values, s in ((54, 16, 4, floors, 1), (54, 16, 4, floors, 2),
                              (53, 15, 3, {1: 18, 2: 4}, 1)):
        a = sum((-1) ** (i + s) * comb(s, i) * values[2 * s - i] for i in range(s + 1))
        degree = values[s] * (comb(k, s) - 1) - sum(comb(s, i) * comb(v - s, s - i) * values[2 * s - i] for i in range(s))
        row = dict(v=v, k=k, t=t, s=s, floor_inputs={str(i): values[i] for i in range(s, 2 * s + 1)},
                   a_s=a, d=degree, choose_k_s=comb(k, s), theorem6_applicable=degree < a,
                   theorem15_applicable=degree >= a >= 1 and values[s] < comb(k, s),
                   theorem18_applicable=degree < a and values[s] < comb(k, s))
        if row["theorem6_applicable"]:
            exact = F(comb(v, s) * (values[s] + 1), comb(k, s) + 1)
            row["theorem6_exact"] = str(exact)
            row["theorem6_ceiling"] = ceiling(exact)
        if row["theorem15_applicable"]:
            alpha = F(a + 1, 2 * (degree + 1))
            beta = F(a + 1, 2 * (degree + comb(k, s)))
            exact = cb(v, k, s, values[s], alpha, beta)
            row["theorem15_exact"] = str(exact)
            row["theorem15_ceiling"] = ceiling(exact)
        need(not row["theorem18_applicable"], "unexpected applicable theorem18 branch")
        need(all(value < 224 for key, value in row.items() if key.endswith("_ceiling")), "published result reaches224")
        cases.append(row)
    result = dict(status="PASS_BOUNDED_PUBLISHED_FORMULA_COMPARISON", retrieved_date_utc="2026-10-08",
        sources=["https://arxiv.org/html/1409.0485v3", "https://arxiv.org/html/1706.06825v2"],
        horsley2014_pair=dict(v=52, k=14, r=4, d=1, n=3, theorem1_exact=str(first),
            theorem1_ceiling=18, theorem14a_exact=str(stronger), theorem14a_ceiling=18,
            theorem14b_applicable=False, theorem14c_applicable=False,
            theorem14c_test=dict(left=4*(n+1)*(n+2)*(n-d), right=d*(d+pair_k)**2)),
        published_floor_chain=dict(triple=4, pair=18, point=64, target=216),
        horsley_singh2017_natural_floor_cases=cases,
        target224_found=False, establishes_priority=False,
        limitations="Checks only the identified formulas with the displayed published floor inputs. It is not an exhaustive literature/theorem catalog, all auxiliary-floor choices, later papers, or unpublished results. General moment/rank and LP/IP methods are established prior art.")
    path = Path(__file__).with_name("PUBLISHED_BOUND_EVALUATIONS.json")
    if not path.exists():
        with path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
    else:
        need(json.loads(path.read_text()) == result, "frozen evaluation differs")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
