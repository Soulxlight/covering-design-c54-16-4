# Precise first-partition point sharing and a complete residual-budget family

## Scope and fixed assumptions

Take an arbitrary complete C(54,16,4) covering with exactly 223 block
occurrences, or pad a smaller nonempty one by repeating a legal block.
The already reviewed C(53,15,3)>=66 child theorem gives point degrees
r_x>=66. Pair links and the independently derived (52,14,2) Gram bound
give lambda_xy>=18. Block occurrences may repeat; points within each
block are distinct. Degrees count occurrences, while triples and pairs
in histograms are distinct point subsets.

Let d_x=r_x-66 and e_xy=lambda_xy-18. Then sum d_x=4 and

    S_x=sum_(y!=x)e_xy=15r_x-53*18=36+15d_x.

This pass considers only the four-ones partition: 50 points have d=0,
four have d=1. Thus S_x is 36 or 51 and is always at most 51. All 333
old necessary rows and their occurrence map remain unchanged. The other
four point-degree partitions are not tested or excluded.

## Degree-36 triples must be point-disjoint

Make a graph on the actual 54 points with an edge xy exactly when
lambda_xy>=36, equivalently e_xy>=18. Every point's incident excess
budget is at most 51, so it has at most floor(51/18)=2 graph neighbors.
A triple of degree at least 36 gives a triangle in this graph, because
its containing occurrences also contain each of its three pairs.

Two distinct triangles sharing a point require at least three distinct
neighbors there, impossible in a graph of maximum degree two. Hence
all distinct triples of degree at least 36 are pairwise point-disjoint.
Their three edge sets are disjoint as well. Writing T36 for their count
and P36 for the number of pairs of degree at least 36 gives

    3*T36<=P36,                  T36<=floor(54/3)=18.

The threshold is "at least 36", not "above 36". The claim uses the
first partition's S_x<=51 essentially; it is not asserted for every
possible 223-block point-degree partition. Repeated whole blocks do not
create multiple copies of the same point-triple in T36.

## Remaining budgets at both endpoints of an actual pair

The following argument proves a whole threshold family, independent of
the numerical profile. Fix h>18 and a pair xy with e=e_xy. A triple of
degree at least h containing xy requires lambda_xy>=h, so e>=h-18.
If its third point is z, then both xz and yz have excess at least h-18.
Different point-triples through xy have different third points, hence
spend on distinct incident pairs at both x and y. The pair xy itself
already spends e from each endpoint's budget.

If K_h(xy) such high triples use xy, therefore

    K_h(xy)*(h-18)<=S_x-e,
    K_h(xy)*(h-18)<=S_y-e,
    K_h(xy)<=52.

Set K_h(xy)=0 for lambda_xy<h. Otherwise the integer bound is

    cap(x,y,e,h)=min(52, floor((S_x-e)/(h-18)),
                         floor((S_y-e)/(h-18))).

Each high triple is counted at exactly its three pairs, so

    3*T_h=sum_(x<y)K_h(xy)
         <=sum_(x<y: e_xy>=h-18)cap(x,y,e_xy,h).

The own-edge subtraction is necessary: the endpoint cannot spend the
same excess twice. Nonnegative excess ensures S_x>=e_xy. This argument
needs no global uniqueness of high triples and no assumption that their
pairs are independent, unlike the seven exceptional-only threshold rows.

Under the existing arbitrary-cover map, J_(a,b,e) counts pairs of endpoint
classes d_x=a,d_y=b and excess e, while t_m counts triples of degree m.
Substitute the exact budgets S_a=36+15a,S_b=36+15b, with a,b in {0,1}:

    cap(a,b,e,h)=min(52, floor((S_a-e)/(h-18)),
                        floor((S_b-e)/(h-18))),

    sum_(a<=b,e>=h-18)cap(a,b,e,h)*J_(a,b,e)
          -3*sum_(m=h..43)t_m >=0.

These are the 25 rows h=19,...,43. Zero coefficients may be omitted.
Each actual first-partition covering maps to every row and to H=0.
The family is complete over the existing allowed triple degrees above
the pair floor; it is not chosen after inspecting a solver output.

At h=36 all its positive cap coefficients are at most one, so it implies
the weaker 3*T36<=P36. The point-disjointness argument separately gives
T36<=18; that separate scalar row is not appended in this test.

## Exact strict strengthening of the prior relaxation

The frozen Pass 26 profile passes every old bound and all 333 old rows,
with H=F3=F4=0. Its exact high tails and heavy pair count are

    T36=29799720/592069,
    P36=366390/19099=11358090/592069.

All other triple degrees above 36 and pair excesses above 18 are zero.
Every used heavy J cell has cap one at h=36. Thus the new endpoint row
has exact residual

    P36-3*T36 = -78041070/592069 <0.

This exact counterexample proves the new family is not implied by the
old moment and seven linking rows in their continuous relaxation. It
removes this profile only. It neither excludes the whole first partition
nor establishes a covering lower bound of 224. No literature novelty is
claimed for the elementary neighborhood-counting argument.

## Independent small-realizable semantic gate

For any small legal block multiset, choose any integer baseline
0<=L<=minimum pair degree and threshold h>L. Compute actual pair excess
e_xy=lambda_xy-L and S_x=sum_y e_xy. The same argument gives

    K_h(xy)<=min(n-2, floor((S_x-e_xy)/(h-L)),
                      floor((S_y-e_xy)/(h-L)))

for pairs with lambda_xy>=h, zero otherwise, and 3*T_h=sum K_h.
If max_x S_x<3*(h-L), the heavy-pair graph has maximum degree two and
its high triples are point-disjoint. The literal independent census checks
these statements for every allowed L and h, including repeated blocks.
Nonvacuous controls use all triples on six points as a baseline plus ten
extra occurrences of one or two selected triples. At L=4,h=11 the two
disjoint controls have S_x<=20<21, so two high triangles can coexist
without sharing points. Overlapping controls deliberately violate that
budget premise and demonstrate that disjointness cannot be assumed alone.

These are independently realized incidence arrays, not solutions of the
target covering problem. They test the generic counting implication; the
target floors and four-ones population supply its target specialization.
An exact primal or negative signed-row certificate must be separately
replayed after the semantic gate before any scoped test conclusion.

