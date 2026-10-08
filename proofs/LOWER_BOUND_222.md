# Counting certificate: C(54,16,4) >= 222

Status: an exact certificate excludes 221 blocks under the necessary
conditions derived below. This is an editorially prepared copy of a frozen
research proof; the mathematical rows and certificate are unchanged.
Internal review has checked the argument. It has not been externally peer
reviewed, and literature novelty has not been established.

The scope is every complete covering by legal 16-subsets of a 54-point set.
There is no prescribed block pool, parent, pairing, orbit family or repair
neighborhood. Repeated block occurrences are allowed by this argument, so
it also applies to the required distinct-block case. No size from 222
through 335 is excluded, and no 335-block construction is supplied here.

The third-moment identity in Section 6 is established prior art: it is
Soicher's 2010 Corollary 2.2 with `S=V, r=2, j=3`. Soicher also discusses
linear and integer programming with these identities; Cameron and Soicher
developed the block-intersection polynomial framework. See
[the citation notes](../CITATIONS.md). Any potential contribution here is
the parameter-specific tight-link coupling and its exact certificate, not
the moment identity or the general LP method.

## 1. Pair-link floors and companion analytic bound

The companion proof [`LOWER_BOUND_221.md`](LOWER_BOUND_221.md) establishes
C(54,16,4) >= 221. Its unedited research source has SHA256

```text
b92fc6596391731a81a87b64d489a567e150f04a32828807b8b4dab1374a4910
```

That proof, including its local degree floors and tight-link lemma, has
undergone internal semantic review. The certificate uses the same floors,
whose derivation is repeated here. The companion proof is useful context
but is not a logical dependency of the final certificate: this proof
allows repeated block occurrences, so any smaller complete cover could
be padded by repeated blocks to exactly 221 occurrences.

Write r_x for the number of block occurrences containing point x,
lambda_P for the number containing a point pair P, and mu_T for the
number containing a point triple T. A complete covering implies

```text
lambda_P >= 18,          r_x >= 64,          mu_T >= 4.       (1)
```

The pair floor follows from the (52,14,2) link and
[Horsley's Theorem 1](https://arxiv.org/html/1409.0485v3): in its notation,
51 = 4*13 - 1, r = 4 and d = 1 satisfy the hypotheses, giving
ceil(52*5/15) = 18. Removing repeated link blocks, if any, only reduces
their count, so the floor remains valid for block occurrences.
For each point x, summing pair degrees gives 15*r_x >= 53*18 = 954;
integrality gives r_x >= 64. A triple has 51 outside points to cover,
with 13 outside points per containing block, so mu_T >= ceil(51/13) = 4.

It suffices to exclude b = 221, because padding preserves coverage and
repeated occurrences are allowed in every step below.

## 2. Complete degree domains for 221 blocks

Assume a complete covering with exactly 221 block occurrences. Define

```text
delta_x = r_x - 64 >= 0,       e_P = lambda_P - 18 >= 0.
D = sum_x delta_x = 221*16 - 54*64 = 80.
E = sum_P e_P = 221*120 - 1431*18 = 762.                  (2)
```

The quantities delta_x and e_P are integers. Consequently
0 <= delta_x <= 80. If P = {x,y}, then

```text
e_P <= 46 + min(delta_x,delta_y)
    <= 46 + floor((delta_x+delta_y)/2)
    <= 46 + floor(D/2) = 86.                              (3)
```

The first inequality uses lambda_P <= min(r_x,r_y); the last uses
nonnegative excesses on every other point. A triple T containing P has
mu_T <= lambda_P, because every block through T also contains P. Thus

```text
4 <= mu_T <= 104,
4 <= mu_T <= 18 + e_P whenever P is contained in T.         (4)
```

These are universal necessary bounds, not selected degree ranges. The
separate experimental graph cap e_P <= 73 is NOT used in the certificate
proved below.

## 3. Histograms and transport counts

Define the following integer counts, which will then be relaxed to real
nonnegative variables:

| Symbol | Meaning | Index domain | Physical upper bound |
| --- | --- | --- | --- |
| n_s | Unordered pairs of distinct block occurrences with intersection size s | 0 <= s <= 16 | binom(221,2) = 24,310 |
| u_d | Points x with delta_x = d | 0 <= d <= 80 | 54 |
| p_e | Point pairs P with e_P = e | 0 <= e <= 86 | binom(54,2) = 1,431 |
| t_m | Point triples T with mu_T = m | 4 <= m <= 104 | binom(54,3) = 24,804 |
| M_{e,m} | Incidences (P,T), P contained in T, with e_P = e and mu_T = m | 0 <= e <= 86, 4 <= m <= 18+e | 52*1,431 = 74,412 |

Every actual complete 221-block covering therefore supplies a vector x
with 0 <= x_j <= U_j in exactly these domains. Including n_16 allows
repeated block occurrences; forbidding them would only strengthen the model.
The M upper bound is the total number of pair/triple incidences and is
deliberately loose. No upper bound assumes a structured construction.

There are 17 + 81 + 87 + 101 + 5,046 = 5,332 variables.

## 4. Necessary equalities from double counting

All the following equalities hold in every assumed covering. The first
and second intersection moments count common points or pairs in two
block occurrences in two orders.

```text
sum_s n_s = 24,310.
sum_d u_d = 54.
sum_d d*u_d = 80.
sum_s s*n_s = sum_d binom(64+d,2)*u_d.

sum_e p_e = 1,431.
sum_e e*p_e = 762.
sum_s binom(s,2)*n_s = sum_e binom(18+e,2)*p_e.

sum_m t_m = 24,804.
sum_m m*t_m = 221*binom(16,3) = 123,760.                 (5)
```

For every e = 0,...,86, each pair of excess e lies in 52 point triples.
Every block containing that pair contributes 14 such triples. Therefore

```text
sum_{m=4}^{18+e} M_{e,m} = 52*p_e.
sum_{m=4}^{18+e} m*M_{e,m} = 14*(18+e)*p_e.               (6)
```

For each m = 4,...,104, a triple has exactly three contained pairs, so

```text
sum_{e: m <= 18+e} M_{e,m} = 3*t_m.                      (7)
```

The restriction m <= 18+e in (6) and (7) is justified by (4); it does
not omit any incidence arising from an actual covering.

## 5. Necessary inequalities from tight links

If mu_T = 4, the four blocks through T cover all 51 outside points using
52 outside incidences. Exactly one outside point is repeated twice and
every other outside point occurs once. Consequently five of the six
pairs of those blocks intersect in T alone, and one intersects in T plus
the repeated point. An intersection of size 3 determines its unique
common triple. An intersection of size 4 contains only four triples.
Counting the assignments from these tight triples gives

```text
n_3 - 5*t_4 >= 0,
4*n_4 - t_4 >= 0.                                        (8)
```

This assignment argument does not assume that different tight triples
have disjoint containing block sets. The possible overlap is precisely
why the second coefficient is 4.

For a pair of degree 18, its 52 triple extensions have degrees at least
4 and sum to 18*14 = 252. If z of them have degree 4, the sum is at
least 4*z + 5*(52-z) = 260-z, so z >= 8. Summing these incidences gives

```text
M_{0,4} - 8*p_0 >= 0,
3*t_4 - 8*p_0 >= 0.                                     (9)
```

The latter also follows from (7) and the former, together with
nonnegativity. Retaining this redundant necessary row is harmless.

## 6. Full third-moment identity and complete-cover specialization

For *any* family of 221 block occurrences, let `hat_t_m` count triples of
degree `m` for the full range `0<=m<=221`. Count incidences consisting of
one triple T and an unordered pair of distinct block occurrences both
containing T. Counting by T and then by the block pair gives

```text
sum_{m=0}^{221} binom(m,2)*hat_t_m
    - sum_{s=0}^{16} binom(s,3)*n_s = 0.              (10)
```

This full-range identity holds even for incomplete families and repeated
block occurrences. For the *hypothetical complete* 221-block cover here,
(1) and (4) force every triple degree into `4..104`. The full histogram
then equals the model's `t_m` on that range and is zero elsewhere. Hence
its model objective satisfies

```text
F(x) = sum_{m=4}^{104} binom(m,2)*t_m
       - sum_{s=0}^{16} binom(s,3)*n_s = 0.          (11)
```

Completeness is required for this restriction to the saved variable
domain and for the link inequalities (1), (8) and (9). It is not needed
for the full-range identity (10).

The LP omits (11) and maximizes F over the weaker conditions (2)--(9)
and the physical variable bounds. An exact strictly negative upper bound
on this maximum contradicts (11) for every complete 221-block covering.

## 7. Exact certificate lemma, including rounding corrections

Here is the entire arithmetic rule used to certify that upper bound.
Let the model rows be l_i <= A_i*x <= h_i, with h_i possibly infinite;
let c be the integer coefficient vector of F. For integer row weights
q_i and positive integer scale S, require q_i <= 0 whenever h_i is
infinite. Put b_i = h_i if q_i > 0 and b_i = l_i if q_i < 0; rows
with q_i = 0 contribute zero. Define

```text
R_j = max(0, S*c_j - sum_i q_i*A_{ij}).
H   = sum_i q_i*b_i + sum_j R_j*U_j.                      (12)
```

For every model-feasible x,

```text
S*F(x)
 = sum_i q_i*(A_i*x)
   + sum_j (S*c_j - sum_i q_i*A_{ij})*x_j
 <= sum_i q_i*b_i + sum_j R_j*U_j = H.                  (13)
```

The first bound uses the signed appropriate row bound. The second uses
0 <= x_j <= U_j: negative residuals contribute at most zero, and positive
residuals at most R_j*U_j. Thus (13) is exact and does not depend on a
solver's tolerance, numerical optimality claim or approximate dual
feasibility. The weights were found numerically, but the proof uses only
the saved integers and exact arithmetic.

## 8. Saved certificate and independently verified values

The model is [`data/model.json`](../data/model.json), SHA256

```text
3f65a5e44b96d0ee5844176331b4b5172ba267f29479e995f3d744d4acca1c24
```

The 288 rows are in the following zero-based order, which also indexes
`row_numerators` in the exact certificate:

```text
0: block-pair count             1: point profile
2: point excess                 3: first intersection moment
4: pair profile                 5: pair excess
6: second intersection moment   7: triple profile
8: triple load                  9: n3 - 5*t4 >= 0
10: 4*n4 - t4 >= 0             11: 3*t4 - 8*p0 >= 0
12: M0_4 - 8*p0 >= 0
13+2*e: transport count e       14+2*e: transport load e (0<=e<=86)
187+(m-4): transport column m (4<=m<=104)
```

All rows except 9--12 are equalities. Rows 9--12 have lower bound zero
and infinite upper bound. The exact integer weights and every positive
column residual are saved in
[`data/certificate.json`](../data/certificate.json), SHA256

```text
9483912feec907e2f4b2118d1ebd2d83bcf881602d41ecbdf8d5674e03c0d973
```

The release [`verify.py`](../verify.py) rebuilds every variable,
objective coefficient, row coefficient and bound from (2)--(9) and (11), compares
them against the saved model, and replays (12) with exact Python integers.
It loads no LP solver or downloaded code. The original independent BigInt
audit was run separately; the release verifier is a fresh minimal replay.

The independently recomputed values are

```text
S = 1,000,000,000.
sum_i q_i*b_i = -2,660,294,744,798.
sum_j R_j*U_j =     88,273,944.   (95 positive residual columns)
H =             -2,660,206,470,854.

F(x) <= H/S = -1,330,103,235,427 / 500,000,000 < 0.        (14)
```

This contradicts (11). Therefore no complete 221-occurrence covering
exists. A smaller complete cover could be padded to 221 occurrences by
repeating any one of its blocks, so it too is excluded. Thus
C(54,16,4) >= 222 under the explicitly stated counting argument.

## 9. Reproducibility and adversarial checks

Run `python verify.py` from the release root. It verifies both immutable
data-file hashes, independently rebuilds the full matrix, checks the
diagnostic and replays the exact signed certificate. `python -m unittest
discover -s tests -v` checks the scalar 221 calculation, moment identity
fixtures and rejection of altered inputs. These are implementation checks;
the double-counting argument in Section 6 supplies the global identity.

The necessary-condition LP is nonempty. The release verifier checks this
exact integer diagnostic profile against every domain and row:

```text
n3=8920, n4=473, n5=4170, n6=10721, n7=26;
u1=28, u2=26;
p0=669, p1=762;
t4=1784, t5=21496, t6=1524;
M0_4=5352, M0_5=29436, M1_5=35052, M1_6=4572;
all other variables zero.
```

Its F is -19,318. It is an aggregate diagnostic, not a block family,
because a complete 221-block family would satisfy the omitted identity F=0.
This check prevents confusing an accidentally empty model with the
certified negative maximum of a genuine relaxation.

The exact negative upper bound proves the result only because every
complete 221-block cover maps to all rows and physical bounds in Sections
2--5. The certificate alone is an inequality for that relaxation. The
origin of its integer weights was a numerical LP; verifying them is exact
and needs no solver. External mathematical and literature review remain
welcome.
