# Sources and prior methods

This packet cites sources; it does not redistribute their papers or datasets.

- Daniel Horsley, [“Generalising Fisher’s inequality to coverings and packings”](https://arxiv.org/html/1409.0485v3), Theorem 1. Applied to the `(52,14,2)` link, it gives at least 18 blocks through each pair. This is the key published input to the local point and pair floors.
- Peter J. Cameron and Leonard H. Soicher, [“Block intersection polynomials”](https://maths.qmul.ac.uk/~leonard/bip.pdf). This is prior framework for block-intersection polynomial and moment reasoning. The linked preprint is dated 2006.
- Leonard H. Soicher, [“More on block intersection polynomials and new applications to graphs and block designs”](https://webspace.maths.qmul.ac.uk/l.h.soicher/nbip2_v2.pdf), preprint dated 2010. Corollary 2.2, specialized to `S=V`, two blocks and triples, yields precisely the third-moment identity `F=0` used in the 222 certificate. Section 3 expressly discusses linear and integer programming. Neither the identity nor general LP method is claimed as new here.
- Daniel Gordon, [La Jolla Coverings Repository v1.2](https://zenodo.org/records/19735294), 2026-04-24. The project previously recorded an archived `(54,16,4)` row with lower216 and upper350. The fresh publication reviewer confirmed the record's author, version and date, but could not recheck that row: the8.3 MB `coverdata.json` request returned HTTP429 and its preview was unavailable. Treat216..350 as a prior project observation, not a freshly verified table value. No dataset or witness archive is copied here.
- [Covering Repository latest improvements](https://coveringrepository.com/systems.aspx?li=2) and its [filtered k=16,m=4,t=4 view](https://coveringrepository.com/systems.aspx?k=16&m=4&t=4). The project previously recorded a `(54,16,4)` row with lower216, upper336, **Franco Atzeni** credit, an LJCR multiple of `(27,8,4)`, and entry date2026-09-26. The fresh publication reviewer could not confirm that row: the latest-improvements page did not display it and the filtered view returned HTTP403. These historical observations provide context only; neither current table status nor priority is certified by this packet. Preserve the prior Atzeni credit, with this verification qualification.
- Daniel Horsley and Rakhi Singh, [“New lower bounds for t-coverings”](https://arxiv.org/html/1706.06825v2). This gives additional lower-bound context and the standard point-link recurrence in Equation (2). The current proof does not claim an exhaustive comparison with every bound in this or later papers.

The possible contribution under discussion is the *parameter-specific* coupling of tight triple links, pair-degree transport and an exact negative certificate at 221 blocks. Literature novelty is unconfirmed.

The additional [audit attribution](audit/ATTRIBUTION.md) identifies the
Pētā analytic route, scout model/certificate and independent review
contributions for the proposed 223 bound. The same established rank,
intersection-polynomial, moment and recurrence methods apply. Pētā
Method/Proof is a working label; no priority is asserted. The
[review limits](audit/REVIEW_LIMITS.md) distinguish internally checked
proofs from pending qualified human acceptance and formal verification.

The combined224 audit supplies [dated expanded prior-art checks](audit224/prior_art/SEARCH_REPORT.md),
the exact query ledger and a reproducible limited comparison with published
formulas. Cameron–Soicher's journal DOI is [10.1112/blms/bdm034](https://doi.org/10.1112/blms/bdm034);
Soicher2010 Corollary2.2 also supplies the fourth moment used in224.
The new five-case models and exact certificates are attributed to the scout;
the analytic child route to Pētā, and separately reconstructed mathematical
maps/case reviews to the independent internal reviewer. Mopî prepared the
combined editorial audit and process controls under Perry Kern's direction.
All contributions used AI assistance. [Source hashes and transformations](audit224/package/PROVENANCE.json)
are explicit. No general moment, rank or LP/IP framework is claimed as new.

The [230 proof](audit230/PROOF.md) is a standalone18-row pair-cover rank/projection
argument with a binary containment refinement and classical point-link lifts.
It invokes no external bound as a premise. The general incidence-rank and
recurrence methods above remain prior art. Mopi prepared this parameter-specific
reduction and manuscript; a separate internal investigator independently reviewed
the semantics and supplied a third exact reconstruction. All work used AI
assistance under Perry Kern's direction. [Review status](audit230/REVIEW_STATUS.json)
and [source transformations](audit230/SOURCE_PROVENANCE.json) distinguish completed
internal checking from pending qualified external acceptance, formal verification
and literature priority. No new literature search or priority finding is represented.
