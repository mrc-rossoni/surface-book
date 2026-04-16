---
title: Rational Form of a Bézier Curve
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

Rational Bézier curves extend the polynomial Bézier formulation by associating a scalar weight to each control point. This extension is not just a mathematical refinement: it is the key step that makes Bézier geometry suitable for the exact representation of conic sections and, more generally, for projective geometry. In CAD, this is essential because circles, circular arcs, ellipses, parabolas, and hyperbolas appear everywhere, from mechanical parts to freeform blends. A purely polynomial Bézier curve cannot represent these objects exactly; a rational Bézier curve can. 

The discussion developed so far for Bézier curves remains valid: the curve is still driven by control points and basis functions, and geometric intuition remains central. However, the rational form enriches the model with an additional set of parameters (degrees of freedom), the weights, which allow us to modulate how strongly each control point attracts the curve. 

# Why Rational Form?

In the polynomial Bézier form, a curve of degree {math}`n` is written as

```{math}
C(t)=\sum_{i=0}^{n} P_i B_i^n(t),
\qquad t\in[0,1].
```

This representation is extremely useful because the Bernstein basis is non-negative and forms a partition of unity, which gives endpoint interpolation, convex-hull containment, and stable geometric control. However, it also has an important limitation: polynomial Bézier curves are not able, in general, to represent conic sections exactly. In particular, even the unit circle cannot be expressed exactly with a non-rational polynomial Bézier curve. The rational form is introduced precisely to overcome this limitation.

:::{prf:example .simple} Circle by Polynomials
Let us assume we want to represent the unit circle in the {math}`xy`-plane, centered at the origin, by means of a non-rational polynomial parametrization. Its implicit equation is
```{math}
x^2+y^2-1=0
```
Assume that {math}`x(u)` and {math}`y(u)` are polynomials of degree {math}`n`:

```{math}
\begin{aligned}
x(u) &= a_0 + a_1 u + \dots + a_n u^n \\
y(u) &= b_0 + b_1 u + \dots + b_n u^n
\end{aligned}
```

Substituting into the circle equation gives:

```{math}
\left(a_0 + a_1u + \dots + a_nu^n\right)^2
+
\left(b_0 + b_1u + \dots + b_nu^n\right)^2
-1 = 0.
```
Expanding, we obtain a polynomial in {math}`u`
```{math}
(a_0^2 + b_0^2 - 1)
+ 2(a_0 a_1 + b_0 b_1)u
+ (a_1^2 + 2a_0 a_2 + b_1^2 + 2b_0 b_2)u^2
+ \dots
+ (a_n^2 + b_n^2)u^{2n}
= 0
```

Since this identity must hold for all {math}`u`, every coefficient must vanish. In particular, the highest-degree coefficient gives:
```{math}
a_n^2+b_n^2=0
```
which implies {math}`a_n=b_n=0`.

Repeating the same argument recursively for the remaining highest-degree terms shows that
```{math}
a_i=b_i=0,
\qquad i=1,\dots,n.
```
{math}`a_0` and {math}`b_0` are excluded.

Therefore, the only possible polynomial parametrization is
```{math}
x(u)=a_0,\qquad y(u)=b_0,
```
with:
```{math}
a_0^2+b_0^2=1.
```
Hence, a non-rational polynomial parametrization cannot represent the circle exactly, except in the trivial constant case. This is why rational parametrizations are needed to represent circles and, more generally, conic sections exactly.
:::
This is one of the main conceptual turning points in geometric modeling. Polynomial Bézier curves are affine objects; rational Bézier curves are projective objects. By moving from affine combinations to weighted projective combinations, one gains the ability to describe shapes that are fundamental in engineering geometry but inaccessible to the polynomial formulation.

# Rational Bézier Curve Definition

A rational Bézier curve of degree {math}`n` is defined as

```{math}
R(t)=\frac{\sum_{i=0}^{n} w_i P_i B_i^n(t)}{\sum_{i=0}^{n} w_i B_i^n(t)},
\qquad t\in[0,1],
```

where:
- {math}`P_0,\dots,P_n` are the control points,
- {math}`w_0,\dots,w_n` are the associated scalar weights,
- {math}`B_i^n(t)` are the Bernstein basis polynomials.

The denominator is a scalar function

```{math}
W(t)=\sum_{i=0}^{n} w_i B_i^n(t),
```

while the numerator is a vector-valued polynomial curve

```{math}
\widetilde{R}(t)=\sum_{i=0}^{n} w_i P_i B_i^n(t).
```

Hence the curve can be written compactly as

```{math}
R(t)=\frac{\widetilde{R}(t)}{W(t)}.
```

This explains the name rational: the curve coordinates are rational functions of the parameter {math}`t`, that is, ratios of polynomials.

It is often convenient to introduce the rational Bernstein functions

```{math}
R_i^n(t)=\frac{w_i B_i^n(t)}{\sum_{j=0}^{n} w_j B_j^n(t)}.
```

With this notation, the curve becomes

```{math}
R(t)=\sum_{i=0}^{n} P_i R_i^n(t).
```

This expression looks formally identical to the polynomial Bézier form, but the basis functions are now rational rather than polynomial.

:::{prf:example .simple} Circle: Exact Representation

Following up the example about the circle, a full circle is not represented by a single quadratic Bézier segment, but it can be represented exactly by joining four quadratic rational Bézier arcs.

Consider the unit circle in the \(xy\)-plane:

```{math}
x^2+y^2=1.
```

We split it into four quarter-arcs. Each quarter is represented exactly by a quadratic rational Bézier curve. For the first quadrant, we choose the control points:
```{math}
P_0=(1,0),
\qquad
P_1=(1,1),
\qquad
P_2=(0,1),
```
with weights:
```{math}
w_0=1,
\qquad
w_1=\frac{1}{\sqrt{2}},
\qquad
w_2=1
```
The corresponding rational quadratic Bézier curve is:
```{math}
R(t)=\frac{w_0P_0B_0^2(t)+w_1P_1B_1^2(t)+w_2P_2B_2^2(t)}{w_0B_0^2(t)+w_1B_1^2(t)+w_2B_2^2(t)},
```
```{math}
R_1(t)=
\frac{(1,0)(1-t)^2 + \frac{1}{\sqrt{2}}(1,1)\,2t(1-t) + (0,1)t^2}
{(1-t)^2 + 2\frac{1}{\sqrt{2}}t(1-t) + t^2},
\qquad t\in[0,1].
```
This curve lies exactly on the unit circle and traces the arc from {math}`(1,0)` to {math}`(0,1)`.
The remaining three quarters are obtained similarly:
```{math}
\begin{aligned}
R_2 &: (0,1)\to(-1,0),
& P_0=(0,1),\; P_1=(-1,1),\; P_2=(-1,0), \\
R_3 &: (-1,0)\to(0,-1),
& P_0=(-1,0),\; P_1=(-1,-1),\; P_2=(0,-1), \\
R_4 &: (0,-1)\to(1,0),
& P_0=(0,-1),\; P_1=(1,-1),\; P_2=(1,0),
\end{aligned}
```
and in each case the weights are
```{math}
w_0=1,
\qquad
w_1=\frac{1}{\sqrt{2}},
\qquad
w_2=1
```

By joining these four rational quadratic Bézier segments, we obtain an exact representation of the full unit circle.
This is a major qualitative difference from polynomial Bézier curves: polynomial curves may approximate a circle very well, but they cannot represent it exactly, whereas a piecewise rational Bézier representation can.

Concerning the weight, more generally, for a circular arc subtending an angle {math}`2\theta`, the middle weight of the corresponding quadratic rational Bézier representation is
```{math}
w_1=\cos\theta,
```
with endpoint weights equal to 1. This compact formula is widely used in CAD and geometric modeling.
:::

## Interpretation of the Weights

The weights control the influence of the control points on the curve. If all weights are equal, say {math}`w_i=1` for all {math}`i`, then the denominator reduces to

```{math}
\sum_{i=0}^{n} B_i^n(t)=1,
```

and the rational Bézier curve collapses exactly to the ordinary polynomial Bézier curve:

```{math}
R(t)=\sum_{i=0}^{n} P_i B_i^n(t).
```

Therefore, the polynomial Bézier curve is just a special case of the rational one.

If a weight {math}`w_i` is increased relative to the others, the curve is pulled closer to the corresponding control point {math}`P_i`. If it is decreased, the attraction of that control point weakens. This gives an additional and very powerful design parameter that does not require changing the control polygon itself.

A useful intuition is the following:
- large weight {math}`\Rightarrow` stronger attraction toward the corresponding control point,
- small positive weight {math}`\Rightarrow` weaker attraction,
- identical weights {math}`\Rightarrow` standard polynomial Bézier behavior.

For practical CAD use, weights are usually taken positive. Positive weights preserve the most important geometric properties and avoid singularities in the denominator. The following interactive plot shows the effect of modifying the weight of one control point on the curve.

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import pandas as pd
import altair as alt
from math import comb
from IPython.display import HTML, display

# ------------------------------------------------------------
# Bernstein basis
# ------------------------------------------------------------
def bernstein(n, i, u):
    """Bernstein polynomial B_i^n(u)."""
    return comb(n, i) * (u**i) * ((1-u)**(n-i))

# ------------------------------------------------------------
# Rational Bézier evaluation
# ------------------------------------------------------------
def rational_bezier_eval(control_points, weights, u_values):
    """
    Evaluate a rational Bézier curve at parameter values u_values.

    control_points: (n+1, 2) array
    weights: (n+1,) array
    u_values: array in [0,1]

    returns: (len(u_values), 2) array
    """
    P = np.asarray(control_points, dtype=float)
    W = np.asarray(weights, dtype=float)
    U = np.asarray(u_values, dtype=float)

    n = len(P) - 1
    C = np.zeros((len(U), 2), dtype=float)
    denom = np.zeros(len(U), dtype=float)

    for i in range(n + 1):
        Bi = bernstein(n, i, U)
        WiBi = W[i] * Bi
        C += WiBi[:, None] * P[i]
        denom += WiBi

    mask = np.abs(denom) > 1e-12
    out = np.full((len(U), 2), np.nan, dtype=float)
    out[mask] = C[mask] / denom[mask, None]
    return out

# ------------------------------------------------------------
# Example control points (cubic)
# ------------------------------------------------------------
P = np.array([
    [0.0, 0.0],
    [0.2, 0.9],
    [0.8, 0.9],   # third control point -> P_2
    [1.0, 0.0],
], dtype=float)

# ------------------------------------------------------------
# Parameter samples
# ------------------------------------------------------------
u_curve = np.linspace(0.0, 1.0, 500)

# ------------------------------------------------------------
# Precompute curves for different values of w2
# ------------------------------------------------------------
# Note: w2 = 1 corresponds to the ordinary polynomial Bézier case
w2_grid = np.round(np.linspace(0.1, 10.0, 199), 2)

curve_rows = []
for w2 in w2_grid:
    weights = np.array([1.0, 1.0, float(w2), 1.0], dtype=float)
    curve_pts = rational_bezier_eval(P, weights, u_curve)

    for u, pt in zip(u_curve, curve_pts):
        curve_rows.append({
            "w2": float(w2),
            "u": float(u),
            "x": float(pt[0]) if np.isfinite(pt[0]) else None,
            "y": float(pt[1]) if np.isfinite(pt[1]) else None,
        })

df_curve = pd.DataFrame(curve_rows)

# ------------------------------------------------------------
# Control polygon data
# ------------------------------------------------------------
df_pts = pd.DataFrame({
    "x": P[:, 0],
    "y": P[:, 1],
    "i": list(range(len(P))),
    "label": [f"P_{i}" for i in range(len(P))]
})

seg_rows = []
for i in range(len(P) - 1):
    seg_rows.append({
        "x0": float(P[i, 0]),
        "y0": float(P[i, 1]),
        "x1": float(P[i + 1, 0]),
        "y1": float(P[i + 1, 1]),
    })
df_segs = pd.DataFrame(seg_rows)

curve_data = alt.Data(values=df_curve.to_dict(orient="records"))
pts_data = alt.Data(values=df_pts.to_dict(orient="records"))
segs_data = alt.Data(values=df_segs.to_dict(orient="records"))

# ------------------------------------------------------------
# Slider for weight of third control point P_2
# ------------------------------------------------------------
w2_slider = alt.binding_range(min=0.1, max=10.0, step=0.05, name="weight w₂ (for P₂): ")
w2_param = alt.param(value=1.0, bind=w2_slider)

# ------------------------------------------------------------
# Plot domains
# ------------------------------------------------------------
x_domain = [-0.1, 1.1]
y_domain = [-0.1, 1.5]

# ------------------------------------------------------------
# Chart layers
# ------------------------------------------------------------
curve = alt.Chart(curve_data).mark_line(strokeWidth=3).encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=y_domain)),
    tooltip=["u:Q", "x:Q", "y:Q"]
).transform_filter(
    alt.datum.w2 == w2_param
)

control_segments = alt.Chart(segs_data).mark_rule(
    strokeDash=[6, 4],
    opacity=0.8
).encode(
    x="x0:Q",
    y="y0:Q",
    x2="x1:Q",
    y2="y1:Q"
)

control_points = alt.Chart(pts_data).mark_point(
    filled=True,
    size=100
).encode(
    x="x:Q",
    y="y:Q",
    tooltip=["label:N", "x:Q", "y:Q"]
)

control_labels = alt.Chart(pts_data).mark_text(
    dx=8,
    dy=-8,
    fontSize=12
).encode(
    x="x:Q",
    y="y:Q",
    text="label:N"
)

# Dynamic header
header = alt.Chart(
    alt.Data(values=[{"dummy": 1}])
).mark_text(
    align="left",
    baseline="middle",
    fontSize=13,
    color="#334155"
).transform_calculate(
    label="'Cubic rational Bézier | varying weight of P₂ | w₂ = ' + format(" + w2_param.name + ", '.2f')"
).encode(
    text="label:N"
).properties(width=620, height=28)

main = (
    curve
    + control_segments
    + control_points
    + control_labels
).properties(
    width=620,
    height=420,
    title="Rational Cubic Bézier Curve — Effect of the Third Control-Point Weight"
)

chart = alt.vconcat(
    header,
    main,
    spacing=6
).add_params(w2_param)

display(HTML("""
<style>
.vega-embed:has(.vega-bind-name):has(canvas[aria-label*="Rational Cubic Bézier Curve"]),
.vega-embed:has(.vega-bind-name):has(svg[aria-label*="Rational Cubic Bézier Curve"]) {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.vega-embed:has(canvas[aria-label*="Rational Cubic Bézier Curve"]) .vega-bindings,
.vega-embed:has(svg[aria-label*="Rational Cubic Bézier Curve"]) .vega-bindings {
  order: -1;
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 8px;
}
</style>
"""))

chart
```

## Basic properties

When the weights are positive, rational Bézier curves preserve most of the fundamental geometric properties of ordinary Bézier curves. In particular, they still interpolate the first and last control points, and their rational basis functions still form a partition of unity. Consequently, the curve remains an affine combination of the control points for every value of the parameter.

Under the same positivity assumption, rational Bézier curves also satisfy the convex-hull property, since the rational basis functions are non-negative over the parameter interval. Furthermore, if all weights are chosen equal, the rational Bézier curve reduces exactly to the classical polynomial Bézier curve. The rational form should therefore be understood as a direct extension of the polynomial formulation rather than as a separate construction.

The role of the weights is to introduce an additional degree of geometric control without modifying the control polygon. In particular, the endpoint tangents retain the same qualitative interpretation as in the polynomial case, being governed by the first and last edges of the control polygon, although their magnitude is affected by the associated weights.

Finally, rational Bézier curves possess a natural projective interpretation. This property is closely related to their ability to represent conic sections exactly and also provides the basis for a stable recursive evaluation procedure through homogeneous coordinates.

:::{note}
# Projective / Homogeneous Interpretation

The cleanest way to understand rational Bézier curves is through homogeneous coordinates. Instead of working directly in Euclidean space, we lift each control point to one dimension higher:

```{math}
\widehat{P}_i=(w_i P_i,\, w_i).
```

For a planar curve, if {math}`P_i=(x_i,y_i)`, then

```{math}
\widehat{P}_i=(w_i x_i,\, w_i y_i,\, w_i).
```

We then build an ordinary polynomial Bézier curve in homogeneous space:

```{math}
\widehat{R}(t)=\sum_{i=0}^{n} \widehat{P}_i B_i^n(t).
```

This curve is polynomial in homogeneous coordinates. Writing

```{math}
\widehat{R}(t)=(X(t),Y(t),W(t)),
```

we recover the Euclidean curve by projective division:

```{math}
R(t)=\left(\frac{X(t)}{W(t)},\frac{Y(t)}{W(t)}\right).
```

This point of view is fundamental because it shows that rational Bézier curves are simply polynomial Bézier curves in projective space, followed by projection back to Euclidean space. The rational form is therefore not an arbitrary trick: it is the natural projective extension of the polynomial formulation.
:::


:::{note}
## Geometric Role of the Weights in Conics

In a quadratic rational Bézier curve, the interior weight has a direct geometric significance. For a fixed and suitable configuration of the control points, the value of the middle weight determines the type of conic arc represented by the curve.

In particular:
- if {math}`0<w_1<1`, the curve is elliptic, including the special case of a circular arc;
- if {math}`w_1=1`, the rational form reduces to the ordinary polynomial quadratic Bézier curve, corresponding to the parabolic case;
- if {math}`w_1>1`, the curve represents a hyperbolic branch.

This classification is one of the clearest manifestations of the projective nature of rational Bézier curves. It can be verified directly in CAD systems such as Rhino by drawing conic arcs and inspecting the weight of the middle control point using the `Weight` command. Repeating the same check for circular, parabolic, and hyperbolic cases reveals exactly this behavior. The effect is illustrated in {numref}`rational` where the middle weight is set to {math}`1/\sqrt{2}`, {math}`1` and {math}`2` for the circular arc, parabolic case, and hyperbolic branch, respectively.

```{figure}../imgs/rational.png
:label: rational
:alt: Effect of different weights on a quadratic rational Bézier curve.
:align: center

Effect of different weights on a quadratic rational Bézier curve..
```
:::

# Conclusions

Rational Bézier curves provide the natural extension of the classical polynomial Bézier formulation. By introducing weights, they preserve the geometric intuition of control points and Bernstein blending while greatly increasing representational power. Their most important advantage is the exact representation of conic sections, which is impossible in the purely polynomial case.

From a geometric viewpoint, the rational form is most naturally understood through homogeneous coordinates: a rational Bézier curve is obtained by constructing a polynomial Bézier curve in projective space and then projecting it back to Euclidean space. This interpretation explains both the role of the weights and the projective invariance of the representation.

In practical CAD, this extension is fundamental. Engineering geometry relies heavily on circles, circular arcs, and other conic sections, and these objects must often be represented exactly rather than approximately. Rational Bézier curves therefore form the conceptual bridge between classical Bézier geometry and the more general NURBS representations used in industrial modeling systems. This point will become even more important later in the book, when NURBS are introduced and the role of the “R”, standing for Rational, is made explicit.
