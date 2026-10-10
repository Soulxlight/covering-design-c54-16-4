# Every finite universe: completeness and limits

1. The macro universe is a=8..17 and j=0..floor(a/2), exactly 70 pairs. The
   matching and rank arguments prove every actual18-row case is in it. 63
   macros exclude; the seven remaining are(8,0..3),(9,0..1),(10,0).
2. Joint normal types satisfy point count 52-a, degree excess a-8, and partner
   sum a-2j. In the surviving macros the degree excess is 0,1 or2. All fives,
   one six, one seven or two sixes and all partner counts, including zero,
   are covered. Repeated types keep multiplicity. Case counts 22,11,5,2,97,45,392
   sum 574. Specialized author enumeration, generic vector partitions and the
   reviewer's partner-first enumeration independently agree on the complete keys.
3. The 574 full types contain 2363 distinct row-maximization records. Each uses
   the entire integer box at its exact load, cap 4 or at most one cap 5 neighbor.
   These are necessary relaxations, not covering enumerations.559 types exclude.
4. The remaining 15 all have a=8, j=0, 44 degree 5 normal points and partner sum 8.
   All 22 partitions of 8 are reconstructed BEFORE selecting the 15 actual
   survivors. Refinement uses cap 3 precisely on edges touching a positive
   partner count, cap 4 otherwise. All 48 row maxima and 15 gaps exclude.
   Minimum gap is 686878/1225 on partition 2+6; no type is skipped or assumed absent.
5. Stage08 checker toys: lengths 1..4, caps4 or one cap 5, every coefficient
   vector over {-1/2,0,1/2}: 119328 allocations and 3768 load maxima. Stage09:
   all 62 cap 3/4 patterns of lengths 1..5, coefficients (2i-n)/6: 66429 allocations
   and 965 load maxima. Its binary toy uses56 weight 3 supports squared against
   70 weight 4 test vectors on eight coordinates, 219520 comparisons.
6. Reviewer grouped-optimizer toys cover 1020 declared small mixed-cap/coefficient
   models, 333450 allocations and 14166 load maxima. Its binary census checks 8885
   same-weight support pairs at weights 0..4 and 33824 distinguishing coordinates.
7. Semantic boundaries cover all 177100 multisets of six triples on six points,
   finding 30 pair covers. This demonstrates the small dependent-ones boundary,
   not a target exception. Six repeated-row residual tests, 219520 weight 5/tight
   coordinate comparisons, 56 legal plain twins and 20280 duplicate-coordinate
   checks test multiplicity and containment. They do not enumerate 52-point covers.
8. Seventeen regenerated certificate corruptions (seven coarse, ten refined)
   run under both normal and optimized Python:34 processes. Each must fail
   explicitly and write no false-success receipt. They test omissions, changed
   coefficients/maxima/caps/gaps, false lifts and unsupported acceptance claims.

Only universes 1-4 supply the exact computer-assisted exclusion. Universes 5-8
test implementation and semantic boundaries. The proof explains why the finite
necessary domains include every actual covering. No optimizer, numerical LP,
target-cover search, selected 19-row family or heuristic success is a premise.
Arithmetic checking and corruption rejection do not replace that semantic proof.
