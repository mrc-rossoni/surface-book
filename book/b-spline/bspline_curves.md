---
title: B-spline Curves
---

(ch-bspline-curves)=
# B-spline Curves

B-spline curves extend the Bezier and piecewise-Bezier constructions from the previous chapters into a single basis-function framework with local support, controllable smoothness, and scalable complexity.

In previous chapters, a spline was introduced as a piecewise polynomial curve on knot spans. In piecewise Bezier form, each span has its own local Bernstein basis and its own local control points. This is geometrically intuitive, but it duplicates control data across segments and requires explicit continuity constraints at joints.

B-splines provide a more compact formulation:

- one global control polygon,
- one global knot vector,
- one family of basis functions with local support.

So instead of stitching many Bezier segments manually, we define the whole curve directly as

```{math}
C(u) = \sum_{i=0}^{n} N_{i,p}(u)\,P_i,
```

where {math}`P_i` are control points and {math}`N_{i,p}` are B-spline basis functions of degree {math}`p`.

## Knot vector and indexing

Let

```{math}
U=(u_0,u_1,\dots,u_m),\qquad u_j \le u_{j+1}
```

be a non-decreasing knot vector.

For a curve of degree {math}`p` with {math}`n+1` control points, indices satisfy

```{math}
m=n+p+1.
```

The parameter domain is typically {math}`[u_p, u_{m-p}]`. Knot spans are intervals {math}`[u_j,u_{j+1})` where basis-function support is defined.

## Cox-de Boor basis recursion

B-spline basis functions are defined recursively.

Degree 0:

```{math}
N_{i,0}(u)=
\begin{cases}
1, & u_i \le u < u_{i+1},\\
0, & \text{otherwise.}
\end{cases}
```

Degree {math}`p>0`:

```{math}
N_{i,p}(u)=
\frac{u-u_i}{u_{i+p}-u_i}N_{i,p-1}(u)
+
\frac{u_{i+p+1}-u}{u_{i+p+1}-u_{i+1}}N_{i+1,p-1}(u).
```

With the standard convention: if a denominator is zero, the corresponding fraction is treated as zero.

This recursion preserves the main CAD properties:

- non-negativity: {math}`N_{i,p}(u)\ge 0`,
- partition of unity: {math}`\sum_i N_{i,p}(u)=1`,
- compact support: each basis function is nonzero only on a limited knot range.

## 4. B-spline curve definition

A B-spline curve of degree {math}`p` is

```{math}
C(u)=\sum_{i=0}^{n} N_{i,p}(u)\,P_i,
\qquad u\in[u_p,u_{m-p}].
```

This matches the basis-function perspective introduced in {ref}`ch-motivations`: geometry is controlled by coefficients ({math}`P_i`) and function space is controlled by the basis ({math}`N_{i,p}`).

Compared with a single high-degree Bezier curve:

- control is local, not global,
- degree can remain low (often cubic),
- the model scales to many control points robustly.

Compared with manually connected Bezier segments:

- continuity is encoded by knot structure,
- one consistent basis spans the entire curve,
- local edits are easier to manage.

## Local support and local edit behavior

A degree-{math}`p` basis function {math}`N_{i,p}` is supported on

```{math}
[u_i, u_{i+p+1}).
```

Therefore, moving control point {math}`P_i` affects the curve only where {math}`N_{i,p}` is nonzero.
This is one of the most important engineering advantages: local geometric edits do not propagate over the full curve.

## Continuity and knot multiplicity

In B-splines, continuity is controlled by knot multiplicity.

Let an internal knot {math}`u_k` have multiplicity {math}`r` in a degree-{math}`p` curve. Then continuity at that knot is

```{math}
C^{p-r}.
```

So:

- {math}`r=1` (simple knot) gives {math}`C^{p-1}` continuity,
- larger multiplicity reduces continuity,
- {math}`r=p` gives only {math}`C^0` continuity,
- {math}`r=p+1` creates a break between pieces.

This directly connects to the continuity chapter: derivative matching at joints becomes a knot-design choice instead of manual constraint solving between separate Bezier segments.

## Bezier relation (important special cases)

B-splines include Bezier curves as a special case.

- With a clamped knot vector and minimal spans, a B-spline segment behaves like a Bezier segment.
- By knot insertion (without geometry change), a B-spline can be decomposed into Bezier pieces.

This is why many CAD pipelines move between B-spline and Bezier representations depending on the operation (evaluation, trimming, export, analysis, manufacturing).

## Evaluation in practice: de Boor algorithm

Direct evaluation via all basis functions is possible, but robust implementations usually use the de Boor algorithm, which is the B-spline analogue of de Casteljau:

- numerically stable,
- local to the active knot span,
- efficient for repeated evaluation.

Conceptually, de Boor performs recursive affine interpolation on the relevant local control points in the active span.

## Derivatives of B-spline curves

B-spline derivatives remain in spline form. For first derivative:

```{math}
C'(u)=\sum_{i=0}^{n-1} P_i^{(1)}\,N_{i,p-1}(u),
```

with derivative control points

```{math}
P_i^{(1)} = \frac{p}{u_{i+p+1}-u_{i+1}}\,(P_{i+1}-P_i).
```

This mirrors the Bezier derivative structure seen previously: derivatives are driven by control-point differences, scaled by knot-dependent factors.

## Design guidelines

For most CAD and geometry-processing tasks:

1. Use cubic degree ({math}`p=3`) unless a different degree is justified.
2. Start with clamped knot vectors for endpoint interpolation behavior.
3. Use simple internal knots for smooth default continuity.
4. Increase multiplicity only where reduced continuity is required (corners, sharp transitions, feature boundaries).
5. Keep control points moderate and rely on local refinement (knot insertion) instead of high global degree.

## Conclusion

B-splines provide the standard polynomial curve model for engineering CAD because they combine:

- strong geometric intuition (control polygon),
- local support and local editing,
- explicit continuity control via knots,
- robust numerical evaluation.

They are the direct bridge from the Bezier and spline foundations covered so far to NURBS, surface patches, fitting workflows, and analysis-oriented geometry pipelines.
