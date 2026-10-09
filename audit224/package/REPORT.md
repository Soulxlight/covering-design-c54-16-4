# An internally audited lower bound: C(54,16,4) >= 224

8 October 2026. Local proof report, package version 01.

Every complete covering of the quadruples of a 54-point set by 16-element
blocks requires at least **224 blocks**. The proof permits repeated whole
blocks as separately indexed occurrences, so it also applies to distinct
blocks. This conclusion passed fresh internal mathematical review with
limits; formal verification, qualified human acceptance, and literature
priority remain unresolved.

The argument has two parts. First, the included analytic child proof gives
**C(53,15,3) >= 66**. It directly proves the pair-link floor
C(52,14,2) >= 18 through a tight-point incidence Gram matrix, without
assuming an external table entry. One-surplus geometry, an avoidance lemma
for a 19-occurrence pair link, and exact intersection moments then give
the contradiction 0 <= H <= -63 for a hypothetical 65-occurrence child
cover. Padding excludes smaller child covers as well.

Every point link of a complete target cover satisfies that child theorem.
Consequently each point degree r_x is at least 66. Incidence counting gives
16b >= 54*66 = 3564, already excluding b <= 222. If b=223, the nonnegative
integer excesses d_x=r_x-66 sum to four. Their positive entries have
exactly five possible partitions: 4, 3+1, 2+2, 2+1+1, and 1+1+1+1.
Relabeling exceptional points requires no symmetry assumption.

For each partition, the included case map sends an arbitrary complete
cover to a bounded linear model. Variables count physical point subsets,
pairs of occurrence indices, endpoint degree classes, and nested
inclusions. Exact third and fourth moment defects vanish on actual
covers; the model objective H is therefore zero on their images.
Both endpoints' residual pair-excess budgets constrain high-degree triple
extensions. Case-specific caps and tightness constraints are proved in
the accompanying documents and independently reconstructed in the code.

| Excess partition | Point degrees | Exact certified upper on H |
|---|---|---|
| 4 | 66^53, 70^1 | -571108487517/1250000000 |
| 3+1 | 66^52, 67^1, 69^1 | -142277733302693/500000000000 |
| 2+2 | 66^52, 68^2 | -132999957096373/1000000000000 |
| 2+1+1 | 66^51, 67^2, 68^1 | -30987510834737/250000000000 |
| 1+1+1+1 | 66^50, 67^4 | -1665576420999/500000000000 |

Each upper is strictly negative and contradicts the actual-cover image
H=0 in its own case. All five cases were freshly reviewed individually,
and their complete assembly, point links, partition exhaustion, and
repeated-occurrence padding were separately reviewed. No 223-occurrence
cover exists, and the incidence boundary excludes every smaller cover.

The reproducibility ZIP includes the complete child dependency, all five
case proofs, exact matrix and certificate bytes, a source-attribution
ledger, and a Python standard-library verifier. The verifier reconstructs
every variable and row, replays signed row bounds with every positive
column residual charged against its finite upper bound, checks the full
dependency graph and case exhaustion, and runs rejection controls. A
separately supplied manifest SHA-256 pins the package. No solver,
installation, network access, private archive, or construction witness is
needed for its checks.

These executable checks establish exact arithmetic and preservation of
the reviewed model data. The universal covering-to-model maps, Gram/rank
argument, and lifting remain ordinary mathematical proofs internally
reviewed, rather than proof-assistant theorems. Repeated agreement does
not independently prove shared premises. No upper-bound construction,
sharpness, publication, public adoption, record, or novelty is claimed.

Source contributions are attributed to the internal research agents Peta
(analytic child argument), Scout (five-case models and certificates), and
the independent internal reviewer (semantic reconstruction and assembly).
The methods have established incidence-rank and block-intersection
background: [Horsley and Singh](https://arxiv.org/html/1706.06825v2),
[Cameron and Soicher, DOI 10.1112/blms/bdm034](https://doi.org/10.1112/blms/bdm034),
and [Soicher, Corollary 2.2 and LP/IP formulations](https://webspace.maths.qmul.ac.uk/l.h.soicher/nbip2_v2.pdf).
No new general framework is asserted. A bounded project literature check
dated 8 October 2026 did not identify an independent published claim of
224 or stronger for these parameters; it was not exhaustive or a priority
certificate. The [LJCR retirement notice](https://dmgordon.org/ljcr/)
states that its covering database froze after 1 March 2026, so its absence
of a later entry cannot establish novelty. See REFERENCES.md in the ZIP.
