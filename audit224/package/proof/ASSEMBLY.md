# Complete lower-bound assembly

Blocks are 16 distinct points of a 54-point set. Whole blocks may repeat
as distinct occurrence indices; every quadruple must be covered.

The included child proof establishes that every complete covering of
triples on 53 points by 15-element blocks has at least 66 occurrences.
Fix a target point x and any triple T outside x. A covering occurrence
containing T union {x}, after deleting x, covers T. Hence x's link is
such a child cover and r_x >= 66. Therefore 16b >= 54*66 = 3564,
excluding all b <= 222.

At b=223, put d_x=r_x-66. These are nonnegative integers with
sum d_x=3568-3564=4. If the largest part is four, nothing remains; if
three, one remains; if two, the remainder is two or two ones; if one,
there are four ones. Thus the five profiles in CASE_LEDGER.json exhaust
every possibility, with zeros filling the remaining 54 labels. Their
labelled assignment counts are 54, 2862, 1431, 74412, and 316251;
their sum is 395010 = C(57,4). The assignment arithmetic supports this
elementary proof and is not a covering search.

Each case proof applies to actual exceptional labels determined by those
degrees. It requires neither a symmetry nor an unlabeled realization of
a fractional histogram. The arbitrary-cover map counts all physical
subsets, all unordered pairs of different occurrence indices, and all
nested inclusions. The n16 cell remains present. Its third/fourth
intersection moment identities have zero defects, so its objective is H=0.

For rows l_i <= A_i x <= u_i, integer weights w_i, and D>0, use u_i
for w_i>0 and l_i for w_i<0. Lower-only rows cannot have positive
weights. With c_j the objective coefficient and 0 <= x_j <= U_j,
let R_j=D*c_j-sum_i w_i*A_ij. Then

    D*H <= sum_i w_i*chosen_endpoint_i + sum_j max(R_j,0)*U_j.

Every positive column residual is charged, however small. The included
certificate for each applicable profile gives a strictly negative upper
bound. It contradicts the actual image H=0; none of the five profiles
survives. Thus no complete 223-occurrence cover exists.

Independently, a nonempty smaller complete cover can be padded to exactly
223 occurrences by repeating a legal block. Links remain complete. For p
new copies of B0, its intersection histogram changes by

    n'_s = n_s + p*#{old i: |B_i intersect B0|=s}
                 + C(p,2)*[s=16],
    deg'(T) = deg(T) + p*[T subset B0].

For j=1..4 both moment sides gain

    p*sum_(T subset B0, |T|=j) deg(T) + C(p,2)*C(16,j).

This explicitly explains repeated-block compatibility. Padding does not
preserve a chosen excess partition; the resulting profile must be mapped
to its own case. Either the incidence boundary or this valid padding
eliminates smaller covers. Therefore C(54,16,4) >= 224.

The logical route is acyclic: covering definition -> direct pair floor,
tight geometry, avoidance and moments -> child66 -> point floors -> five
partitions -> case-specific maps -> signed certificates -> no223 -> 224.
The child proof does not assume the target conclusion or these five models.
Independent review accepted these universal arguments as ordinary
mathematics; exact arithmetic alone does not discharge their semantics.
