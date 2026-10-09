# Necessary conditions at223 block occurrences

Premise: the internally reviewed C(53,15,3)>=66 theorem, with repeated block
occurrences allowed. Thus every point of a complete C(54,16,4) covering has
degree r_x>=66. This stage neither edits nor republishes its proof. Pad any
hypothetical covering with at most223 occurrences to exactly223 by repeating
a block. The66 floor then gives the following conditions at the padded size.

## Four units of point excess

Let d_x=r_x-66. These are nonnegative integers and

    sum_x d_x=16*223-54*66=4.

The five nonzero partitions are4;3+1;2+2;2+1+1;1+1+1+1. In particular50 or
more points have degree66, and every point degree is at most70. The complete
class populations are determined by a partition, not chosen fractional
point counts. If u_a is its population, the first intersection moment is

    I1=sum_x C(r_x,2)=54*C(66,2)+66*4+sum_x C(d_x,2).

It is116100,116097,116096,116095,116094 in the order above.

## Weighted pair-excess graph and subset caps

The reviewed pair floor is lambda_xy>=18. Set e_xy=lambda_xy-18>=0. Then

    E=sum_(x<y)e_xy=223*C(16,2)-18*C(54,2)=1002,
    S_x=sum_(y!=x)e_xy=15*r_x-53*18=36+15*d_x.

Each e_xy is at most S_x,S_y and at most48+min(d_x,d_y), by containment
lambda_xy<=min(r_x,r_y). Thus any pair involving a normal d=0 point has
lambda<=54. Only pairs within the at-most-four exceptional points can exceed
54. The complete per-class edge caps are

    e<=min(36+15*a,36+15*b,48+min(a,b)).

For an s-point set T, s>=2, let h_T count containing block occurrences.
Every internal pair has lambda>=h_T. For x in T, if h_T>18 its s-1 incident
internal edges each spend at least h_T-18 of S_x. If h_T<=18 the resulting
bound is automatic. Therefore, universally,

    h_T<=18+floor(S_x/(s-1)) for every x in T.             (A)

This is a consequence of nonnegative pair excess and actual shared labels;
it does not assume symmetry or that a histogram is realizable.

Any triple containing a normal point has degree<=36. A triple on only
exceptional points exists only in the final two partition cases, and has
minimum d<=1, hence degree<=43. In the2+1+1 case there is only one such
triple. In the1+1+1+1 case any two distinct exceptional triples share two
points. A shared point would have three distinct incident pairs of excess
at least19 if both triple degrees exceeded36, using at least57>51=S_x.
Consequently at most ONE triple has degree>=37, in every case.

Any quadruple containing a normal point has degree<=30. An all-exceptional
quadruple exists only in the1+1+1+1 case, is unique, and has degree<=35.
Thus all other cases have quad degree<=30; the final case has at most ONE
quadruple above30. No actual covering is excluded by these caps alone.

## Compact necessary moment model

All model variables are nonnegative reals; actual counts are integers. Fix
one of the five integral class populations u. Let n_s count unordered pairs
of block-occurrence indices with intersection size s,0<=s<=16. Let p_e,t_m,q_h
be pair-excess, triple-degree and quadruple-degree histograms. Let J_(a,b,e)
count unordered pairs with endpoint excess classes a<=b and edge weight e.
Its per-cell bound is C(u_a,2) if a=b and u_a*u_b otherwise. No J cell with
zero physical population or weight above its proved class cap exists.

Exact class rows are

    sum_e J_(a,b,e)=number of pairs between these classes,
    sum_(a,b) J_(a,b,e)=p_e,
    sum_(a,b containing c,e) endpoint_multiplicity(c)*e*J_(a,b,e)
       =u_c*(36+15*c),

where endpoint multiplicity is2 on c=c and1 otherwise. These jointly couple
both endpoints of each pair, beyond the former one-endpoint transport.

Keep complete count/load and first/second intersection moment equations:

    sum n=C(223,2); sum s*n_s=I1,
    sum p=C(54,2); sum e*p_e=1002,
    sum C(s,2)*n_s=sum C(18+e,2)*p_e,
    sum t=C(54,3); sum m*t_m=223*C(16,3),
    sum q=C(54,4); sum h*q_h=223*C(16,4).

M_(e,m) counts pair/triple incidences. Its rows count52 extensions per pair,
load14*(18+e), and3 pairs per triple. Its domain uses m<=lambda and the new
global triple cap. Reuse the previously reviewed weak degree18-link cap15
and the separately reviewed degree19 avoidance cap15. Do not strengthen the
degree18 cap as an adaptive variant. A degree18 pair forces at least8 tight
degree4 triples, so M_(0,4)>=8*p0. Keep n3>=5*t4 and4*n4>=t4 from the exact
one-surplus tight-triple proof. No new rank/determinant cap is included.

N_(m,h) counts triple/quad incidences:51 extensions per triple, load13*m,
and4 contained triples per quadruple. Domain h<=m and the new quad cap;
for m=4 allow only h=1,2 by one-surplus coverage. Include every high-triple
and high-quad count bound above.

As in the frozen moment method, introduce bounded nonnegative z3p,z3m,z4p,z4m:

    F3=sum C(m,2)*t_m-sum C(s,3)*n_s=z3p-z3m,
    F4=sum C(h,2)*q_h-sum C(s,4)*n_s=z4p-z4m.

Maximize H=-(z3p+z3m+z4p+z4m). Every actual covering maps to H=0. Histogram
cells have their total physical count bounds, M cells<=52*C(54,2), N
cells<=51*C(54,3). Plus-defect bounds use their corresponding demand count
times the maximum binomial degree moment; minus-defect bounds use C(223,2)
times C(16,3) or C(16,4). These bound any actual moment difference; the model
does not assert arbitrary feasible vectors are blocks or labeled degrees.

## Certification boundary

A negative objective requires an exact signed-row upper certificate with
all positive coefficient residuals charged against rigorous finite bounds.
For lower<=A*x<=upper, signed integer row weights w at scaleD give

    D*H<=sum_i w_i*(upper_i if w_i>0 else lower_i)
          +sum_j max(0,D*c_j-sum_i w_i*A_ij)*U_j.

One-sided lower rows require w<=0. All five degree cases would have to be
excluded, with a complete semantic proof and independent exact replays,
before a global>=224 claim. A numerical status is never sufficient. An exact
feasible profile with H=F3=F4=0 in even one case shows this particular
necessary model cannot exclude all223 coverings; it is not a covering.
