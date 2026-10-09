# Every finite enumeration: universe, completeness, limits

These computations contain no seeds, numerical solvers or heuristic
sampling. The universes and endpoints are explicit. They are arithmetic
and implementation checks, except the support graphs additionally supply
finite combinatorial upper certificates after the semantic mapping.

## 1. Full matrix comparisons and exact certificates

The 222 builder reconstructs all 5332 variables and 288 rows. Complete
equality of sparse maps checks 1535616 coefficient positions, including
implicit zeros, together with every objective, row sense and finite bound.
The 223 builder similarly checks 975 variables,156 rows,152100 positions.
All row multipliers are used. All columns are visited to reconstruct the
positive residual map (95 for 222;26 for scout223), then its entire finite
correction is summed. No residual sampling or tolerance is used.

These are complete checks of the **specified** finite models, not a proof
that a hypothetical cover maps to them. That map is proved in the numbered
manuscript. A wrong semantic cut could survive exact certificate replay;
this is why coefficients and necessary status are reviewed separately.

## 2. Direct rank-floor polynomial

For a=0..52 and e=0..floor(a/2), a matching with e edges has a unique
isomorphism type: choose edges (0,1),(2,3),... and leave a-2e isolated
vertices. Every matching is a relabeling of one of these types, and
relabeling preserves the quadratic identity. There are 729 types:
even a=2j, j=0..26 contributes sum(j+1)=378; odd a=2j+1,j=0..25
contributes 351. The checker compares every monomial coefficient on
both sides of the positive-definite identity, including the empty a=0
case. It also checks integer b=0..17 against `260-14b>b`.

This is not an enumeration of all covers or a computational proof of
real positivity. The manifestly positive sum-of-squares and rank
argument are the mathematical reason for the universal floor.

## 3. Pētā's arithmetic domains

All s=0..15 are checked for the polynomial identity and nonnegativity.
All point-degree/chord pairs are checked as follows: r=18,m=4..18
(15 cases); r=19,m=4..15 (12 cases, using the proved avoidance cap);
r=20..39,m=4..r (`sum_{r=20}^{39}(r-3)=20*(17+36)/2=530` cases).
Total is 557. All d=2..21 envelope slacks are checked (20 cases),
and both b=64,65 final substitutions are checked.

Completeness comes from the excess-budget domain and the three-way
case split, not from finding no numerical counterexample. Chord checks
outside that stated integer domain make no claim.

## 4. Complete 19-occurrence support graphs

Fix m in {16,17,18,19}. Relabel the blocks containing the distinguished
point p as positions 0..m-1 and all other positions as m..18. Any actual
cover admits this relabeling, including repeated block values. A tight
point q has a four-position support S. Complete pair coverage gives
`1<=|S intersect {0,..,m-1}|<=2`. Enumerate **all** `C(19,4)=3876`
four-subsets, keeping exactly those satisfying this necessary condition.
Repeat this entire raw universe at each of the four m values:15504 visits.

Distinct tight points cannot have equal supports, which would give
codegree four. Pair coverage and unique repeated partners imply that two
supports S,T may coexist only if their overlap is one, or if their overlap
is two and both have inside count one. The latter condition keeps their
partner available. This permits some collections that violate other
global partner constraints; permitting them enlarges the graph and
therefore is a sound relaxation. Check **every** unordered candidate pair
against this criterion and compare the complete sorted CSV.

| m | candidates | candidate pairs | edges | coloring/clique upper cap | tight points forced |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | C(16,2)C(3,2)+16C(3,3)=360+16=376 | 376*375/2=70500 | 32760 | 3 | 5 |
| 17 | C(17,2)C(2,2)=136 | 136*135/2=9180 | 0 | 1 | 6 |
| 18 | 0 | 0 | 0 | 0 | 7 |
| 19 | 0 | 0 | 0 | 0 | 8 |

All candidate pairs total 79680. m>=18 has <=1 outside position and
cannot support at least two outside occurrences, hence zero candidates.
For m=16 color by the two outside positions (three colors); the 16
vertices with all three outside positions are isolated and can use any
existing color. Supports `{0,1,16,17}`,`{2,3,16,18}`,`{4,5,17,18}` form
an explicit 3-clique. For m=17 the graph is edgeless and has a single
vertex witness; the other graphs are empty. Every supplied vertex, color,
edge, isolation list and clique is checked in addition to the independent
color construction. Frozen graph JSON and CSV bytes are included.

These graphs prove capacities for a necessary support condition after
the arbitrary-cover map. They are not full pair-cover witnesses or a
statement of sharpness at degree 15. There is no cutoff on the number a
of tight points: any such family must inject into a clique and thus obey
the coloring bound.

## 5. Complete toy multisets

On labeled points 0..4 there are five legal four-block types. For each
b=0..8 enumerate every nondecreasing b-tuple of type indices using
combinations with replacement. Every multiset has exactly one such tuple.
Total `sum_{b=0}^{8}C(b+4,4)=C(13,5)=1287`. Occurrence reordering does
not change any checked invariant. All families, including incomplete
ones, exercise three intersection moments and local incidence loads.
Among 406 complete triple covers,265 have tight pairs and400 have repeated
blocks. Complete families additionally exercise the M/N transport types,
excess caps, supports and tight-pair charging rules.

On labeled points 0..3 there are four legal three-block types. Enumerate
b=0..6 the same way: `sum C(b+3,3)=C(10,4)=210` multisets. Of these95
are pair covers;48 degree-two tight-point instances exercise the
corresponding single-surplus repeated-partner rule at the toy parameters.

A complete five-point triple cover plus a repeated four-block gives a
full-intersection pair at s=4. Deliberately discarding it changes the
second-moment objective by `C(4,2)=6`. An incomplete repeated family has
outside distribution [2,2], instead of the complete single-surplus
distribution [1,1,2]. This falsifies any attempted use of the tight
geometry without completeness.

These toys are exhaustive **only** over their stated small universes.
They check implementation, occurrence counting and assumption boundaries.
They do not establish universality at v=52,53,54 or certify sharpness.

## 6. Deliberate corruptions and optimized execution

In each normal/optimized run,22 structural corruptions are rejected:
11 in each model/certificate, including dropping the repeated-block
intersection, reversing objective or cut, changing bounds/load, omitting
rows/multipliers/residuals, invalid signs/scale, undercharging corrections
and changing a stated fraction. Typed matrix checks also reject booleans
and floating coefficients. The process runner changes each of the four
frozen model/certificate files and a support edge, then demonstrates
nonzero exits under both modes (10 file-corruption processes).

Every public validation condition uses explicit exceptions. Producer
assertions that vanished under Python -O are excluded from the public
verification path. Passing under -O alone says nothing about an
assert-based producer; the runner compares complete mathematical
receipts and proves corrupted inputs still fail.
