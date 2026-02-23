---
title: Change the Degree of a Bezier Curve
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python

---


Changing the degree of a Bézier curve is crucial in CAD, computer graphics, and numerical analysis. The degree affects flexibility, computational cost, and compatibility with other curves. Two key operations are used in practice:
- **Degree elevation** to increase the degree while preserving the shape.
- **Degree reduction** to approximate the curve with a lower-degree representation.

## Degree Elevation
We start from the Bernstein form:

```{math}
C(t)=\sum_{i=0}^{n} P_i\,B_i^n(t),
\qquad t\in[0,1].
```

Degree elevation rewrites the same curve as a Bézier curve of degree {math}`n+1`:

```{math}
\bar{C}(t)=\sum_{i=0}^{n+1} \bar{P}_i\,B_i^{n+1}(t).
```

The new control points are:

```{math}
:label: eq_elevation
\bar{P}_i = \frac{i}{n+1} P_{i-1} + \left(1-\frac{i}{n+1}\right) P_i,
\qquad i=0,\dots,n+1,
```


:::{prf:proof .simple .dropdown} Degree Elevation Formula

We want to find a curve such that:
```{math}
\sum_{i=0}^{n} P_i B_i^n(t)=\sum_{i=0}^{n+1} \bar{P}_i B_i^{n+1}(t).
```

Starting from the Bézier definition and expanding the Bernstein basis:
```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```

We multiply the left-hand side by {math}`t+(1-t)=1`:
```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} (t+(1-t))
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```

Expanding:
```{math}
\begin{aligned}
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i+1} (1-t)^{n-i}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

To express all terms in the same monomials {math}`t^i(1-t)^{n+1-i}`, we shift the index in the first sum by setting {math}`j=i+1`:
```{math}
\begin{aligned}
&\sum_{j=1}^{n+1} P_{j-1} \binom{n}{j-1} t^{j} (1-t)^{n+1-j}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Renaming the index {math}`j` back to {math}`i` in the first sum:
```{math}
\begin{aligned}
&\sum_{i=1}^{n+1} P_{i-1} \binom{n}{i-1} t^{i} (1-t)^{n+1-i}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Using the binomial identities:
```{math}
\begin{aligned}
\binom{n}{i} &= \frac{n+1-i}{n+1}\binom{n+1}{i}, \quad 0 \le i \le n \\
\binom{n}{i-1} &= \frac{i}{n+1}\binom{n+1}{i}, \quad 1 \le i \le n+1
\end{aligned}
```

we obtain:
```{math}
\begin{aligned}
&\sum_{i=1}^{n+1} P_{i-1} \frac{i}{n+1}\binom{n+1}{i} t^{i} (1-t)^{n+1-i}
+\\
&\sum_{i=0}^{n} P_i \frac{n+1-i}{n+1} \binom{n+1}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Thus:
```{math}
\sum_{i=1}^{n+1} \frac{i}{n+1} P_{i-1} B_i^{n+1}(t)
+
\sum_{i=0}^{n} \frac{n+1-i}{n+1} P_i B_i^{n+1}(t)
=
\sum_{i=0}^{n+1} \bar{P}_i B_i^{n+1}(t).
```

Since {math}`\{B_i^{n+1}(t)\}_{i=0}^{n+1}` is a basis, the representation is unique, hence the coefficients {math}`B_i^{n+1}(t)` must match. So the degree-elevated control points are:
```{math}
\bar{P}_0 = P_0, \quad i = 0
```

```{math}
\bar{P}_i = \frac{i}{n+1} P_{i-1}
+
\left(1 - \frac{i}{n+1}\right) P_i,
\quad 1 \le i \le n
```

```{math}
\bar{P}_{n+1} = P_n, , \quad i = n+1
```

:::

Equation {numref}`eq_elevation` shows that each new control point is obtained as a convex linear combination of two consecutive control points of the original control polygon, with weights depending on the parameter {math}`\frac{i}{n+1}`, the degree-elevated control polygon lies entirely within the convex hull of the original one and defines exactly the same Bézier curve. Degree elevation therefore preserves the curve geometry while increasing the number of control points, providing additional degrees of freedom for subsequent shape manipulation without altering the underlying geometry.


By using the slider at the bottom of the following figure you can have a visual demonstration of the degree elevation for a Bézier curve with 4 control points, hence degree 3 (cubic).

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import pandas as pd
import altair as alt

# ------------------------------------------------------------
# Bézier evaluation (no external helpers)
# ------------------------------------------------------------
def bernstein(n, i, u):
    """Bernstein polynomial B_i^n(u)."""
    from math import comb
    return comb(n, i) * (u**i) * ((1-u)**(n-i))

def bezier_eval(control_points, u_values):
    """
    Evaluate a Bézier curve at parameter values u_values.
    control_points: (n+1, 2) array
    u_values: array of u in [0,1]
    returns: (len(u_values), 2) array
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    U = np.asarray(u_values, dtype=float).reshape(-1, 1)

    C = np.zeros((len(U), 2))
    for i in range(n + 1):
        Bi = bernstein(n, i, U[:, 0]).reshape(-1, 1)
        C += P[i] * Bi
    return C

# ------------------------------------------------------------
# Degree elevation (taken from your reference; vectorized-friendly)
# ------------------------------------------------------------
def degree_elevate(control_points):
    """Perform one degree elevation on a Bézier curve."""
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1  # current degree
    # New control points Q_0..Q_{n+1}
    Q = []
    Q.append(P[0])
    for i in range(1, n + 1):
        alpha = i / (n + 1)
        # Q_i = alpha * P_{i-1} + (1-alpha) * P_i
        Q.append(alpha * P[i - 1] + (1 - alpha) * P[i])
    Q.append(P[-1])
    return np.array(Q, dtype=float)

def elevate_k_times(control_points, k):
    Pk = np.asarray(control_points, dtype=float)
    for _ in range(int(k)):
        Pk = degree_elevate(Pk)
    return Pk

# ------------------------------------------------------------
# Build dataframe for control polygons at different elevations
# ------------------------------------------------------------
def build_control_polygon_df(P, k, tag="selected"):
    """Return two dataframes: points and segments for a given control polygon."""
    P = np.asarray(P, dtype=float)
    pts = []
    segs = []
    deg = len(P) - 1

    for i, p in enumerate(P):
        pts.append({
            "type": "point",
            "k": k,
            "tag": tag,
            "degree": deg,
            "i": i,
            "x": float(p[0]),
            "y": float(p[1]),
            "label": f"{tag}: P{i} (deg={deg})"
        })

    for i in range(len(P) - 1):
        p0, p1 = P[i], P[i + 1]
        segs.append({
            "type": "segment",
            "k": k,
            "tag": tag,
            "degree": deg,
            "i": i,
            "x0": float(p0[0]),
            "y0": float(p0[1]),
            "x1": float(p1[0]),
            "y1": float(p1[1]),
        })

    return pd.DataFrame(pts), pd.DataFrame(segs)

# ------------------------------------------------------------
# Example control points (edit freely)
# ------------------------------------------------------------
P0 = np.array([
    [0.0, 0.0],
    [0.2, 0.9],
    [0.8, 0.9],
    [1.0, 0.0],
], dtype=float)

deg0 = len(P0) - 1

# Curve samples (the curve is invariant under degree elevation)
u_curve = np.linspace(0, 1, 300)
curve_pts = bezier_eval(P0, u_curve)
df_curve = pd.DataFrame({"u": u_curve, "x": curve_pts[:, 0], "y": curve_pts[:, 1]})

# ------------------------------------------------------------
# Precompute elevated control polygons for k = 0..K_MAX
# ------------------------------------------------------------
K_MAX = 8

all_pts = []
all_segs = []

# original polygon (tag="original"), stored at k=0 for reference
dfp0, dfs0 = build_control_polygon_df(P0, k=0, tag="original")
all_pts.append(dfp0)
all_segs.append(dfs0)

# elevated polygons (tag="selected"), stored for each k
for k in range(0, K_MAX + 1):
    Pk = elevate_k_times(P0, k)
    dfp, dfs = build_control_polygon_df(Pk, k=k, tag="selected")
    all_pts.append(dfp)
    all_segs.append(dfs)

df_pts = pd.concat(all_pts, ignore_index=True)
df_segs = pd.concat(all_segs, ignore_index=True)

curve_data = alt.Data(values=df_curve.to_dict(orient="records"))
pts_data = alt.Data(values=df_pts.to_dict(orient="records"))
segs_data = alt.Data(values=df_segs.to_dict(orient="records"))

# ------------------------------------------------------------
# Slider: number of elevations k
# ------------------------------------------------------------
k_slider = alt.binding_range(min=0, max=K_MAX, step=1, name="Elevations k: ")
k_param = alt.param(value=0, bind=k_slider)

# ------------------------------------------------------------
# Chart layers
# ------------------------------------------------------------
x_all = np.concatenate([
    df_curve["x"].to_numpy(),
    df_pts["x"].to_numpy(),
    df_segs["x0"].to_numpy(),
    df_segs["x1"].to_numpy(),
])
y_all = np.concatenate([
    df_curve["y"].to_numpy(),
    df_pts["y"].to_numpy(),
    df_segs["y0"].to_numpy(),
    df_segs["y1"].to_numpy(),
])

x_pad = 0.12 * (x_all.max() - x_all.min() + 1e-9)
y_pad = 0.12 * (y_all.max() - y_all.min() + 1e-9)
x_domain = [x_all.min() - x_pad, x_all.max() + x_pad]
y_domain = [y_all.min() - y_pad, y_all.max() + y_pad]

bezier_curve = alt.Chart(curve_data).mark_line(strokeWidth=3, color="#ef4444").encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=y_domain)),
).properties(width=760, height=440)

# Shadows: show all polygons for k <= selected k
shadow_segments = alt.Chart(segs_data).mark_rule(
    strokeWidth=1.5,
    opacity=0.18,
    color="#334155"
).encode(
    x="x0:Q", y="y0:Q", x2="x1:Q", y2="y1:Q"
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.tag == "selected") & (alt.datum.k <= k_param)
)

shadow_points = alt.Chart(pts_data).mark_point(
    filled=True,
    size=48,
    opacity=0.16,
    color="#334155"
).encode(
    x="x:Q", y="y:Q",
    tooltip=["k:O", "degree:O", "i:O", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.tag == "selected") & (alt.datum.k <= k_param)
)

# Highlight: selected k
sel_segments = alt.Chart(segs_data).mark_rule(
    strokeWidth=3.0,
    opacity=0.95,
    color="#000000"
).encode(
    x="x0:Q", y="y0:Q", x2="x1:Q", y2="y1:Q"
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.tag == "selected") & (alt.datum.k == k_param)
)

sel_points = alt.Chart(pts_data).mark_point(
    filled=True,
    size=95,
    color="#000000"
).encode(
    x="x:Q", y="y:Q",
    tooltip=["k:O", "degree:O", "i:O", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.tag == "selected") & (alt.datum.k == k_param)
)

# Dynamic header row (outside plotting area)
header = alt.Chart(
    alt.Data(values=[{"dummy": 1}])
).mark_text(
    align="left",
    baseline="middle",
    fontSize=13,
    color="#334155"
).transform_calculate(
    label=f"'Degree Elevation | k = ' + {k_param.name} + ' | degree = ' + ({deg0} + {k_param.name})"
).encode(
    text="label:N"
).properties(width=760, height=28)

main = bezier_curve + shadow_segments + shadow_points + sel_segments + sel_points

chart = alt.vconcat(
    header,
    main,
    spacing=6
).add_params(k_param).properties(
    title="Interactive Degree Elevation (Bezier)"
)

chart
```

### Why Degree Elevation?
Degree elevation has important applications:
- When combining or blending curves and surfaces of different degrees, degree elevation allows them to be brought to a common degree, enabling exact algebraic operations such as addition, subtraction, or interpolation.
- In surface design, several algorithms that generate surfaces from curve inputs require all curves to have the same degree. A notable example is the construction of Coons surfaces implemented as tensor-product Bézier or NURBS patches, where boundary curves must be expressed with a common polynomial degree. Degree elevation allows this requirement to be satisfied without altering the curve geometry.
- Outside traditional CAD, degree elevation (often referred to as p-refinement) is a core operation in isogeometric analysis (See {cite}`Hughes_2005`), where increasing the polynomial degree improves approximation accuracy without changing the geometry.
- In robotics and control, trajectories are often represented using Bézier. Degree elevation is used to bring trajectories of different polynomial degrees to a common representation, enabling smooth trajectory blending, time reparameterization, and the enforcement of continuity and dynamic constraints (e.g. velocity or acceleration continuity) without altering the geometric path. See, for example, {cite}`Durakl__2022`.
 - ...

## Degree Reduction
Degree elevation can be viewed as a process that introduces redundancy, in the sense that the same curve geometry is represented using more control points, and therefore more parameters, than are strictly necessary. Although the representation becomes redundant, degree elevation enlarges the space of admissible control point configurations that represent the same geometry, which can be advantageous in optimization, approximation, and constraint-based formulations. Despite its advantages, degree elevation also introduces drawbacks. The increased polynomial degree and number of control points lead to higher computational and memory costs and may negatively affect numerical conditioning. Moreover, higher-degree representations tend to reduce local control, making shape manipulation less intuitive and increasing the complexity of subsequent geometric algorithms.

Degree reduction is the inverse process and is of interest for several reasons. It addresses the question of whether a given Bézier curve of degree {math}`n` can be represented by a curve of lower degree, for instance {math}`n-1`. While this is generally not possible without loss of information, degree reduction is valuable in practice for:
- Computational efficiency, by reducing the cost of curve evaluation, rendering, and downstream geometric operations.
- Data compression, through a reduction in the number of control points.
- Improved interactive control, as lower-degree curves are often easier to manipulate in CAD/CAM workflows.

In general, exact degree reduction is not possible unless the original curve already lies in a lower-degree polynomial space.
### Why Degree Reduction Is an Approximation (Intuitive Explanation)
The Bernstein polynomials of degree {math}`n` form a basis for the vector space of all polynomials of degree at most {math}`n`. Consequently, a Bézier curve of degree {math}`n` represents a generic element of this space. When considering degree reduction to a lower degree {math}`m < n`, the target representation is restricted to a strictly smaller subspace spanned by the Bernstein polynomials of degree {math}`m`.

Since this lower-degree space is a proper subspace of the original one, most degree-{math}`n` polynomials do not belong to it. Exact representation is therefore only possible if the original curve happens to lie entirely within that lower-dimensional space, namely if its highest-degree components vanish. In terms of control points, this corresponds to the vanishing of higher-order forward differences, which is a nongeneric and highly restrictive condition.

From a geometric perspective, degree elevation introduces redundancy by embedding a lower-degree polynomial into a higher-degree space without changing the curve geometry. Degree reduction attempts the inverse operation: it seeks to project a higher-degree polynomial onto a lower-dimensional space. However, unlike degree elevation, this projection cannot, in general, preserve all information. As a result, some geometric detail is inevitably lost.

Therefore, exact degree reduction exists only in exceptional cases, specifically when the curve was originally of lower degree and later degree-elevated. In all other cases, degree reduction must be formulated as an approximation problem, where the goal is to find the closest lower-degree curve according to a chosen error metric. 

A common approach is to determine the reduced-degree curve by minimizing the squared error between the two curves. See {ref}`degree-red-note` for a formal implementation of the Least-Squares Degree Reduction applied to Bézier curve, {ref}`degree-red-concrete` for a numerical example.

(degree-red-note)=
:::{prf:example .simple .dropdown} Least-Squares Degree Reduction Example

Let a Bézier curve of degree {math}`n` be given by
```{math}
c(t)=\sum_{i=0}^{n} P_i\,B_i^n(t),
\qquad t\in[0,1].
```

We seek a lower-degree curve {math}`\tilde{c}(t)` of degree {math}`m<n`:
```{math}
\tilde{c}(t)=\sum_{j=0}^{m} \tilde{P}_j\,B_j^m(t).
```

We choose the reduced control points {math}`\{\tilde{P}_j\}` by minimizing the squared error:
```{math}
\min_{\{\tilde{P}_j\}}
\int_0^1 \|c(t)-\tilde{c}(t)\|^2\,dt.
```

Substituting the Bézier representations gives
```{math}
\min_{\{\tilde{P}_j\}}
\int_0^1
\left\|
\sum_{i=0}^{n} P_i B_i^n(t)
-
\sum_{j=0}^{m} \tilde{P}_j B_j^m(t)
\right\|^2
\,dt.
```

To derive the linear system, expand the squared error and set its partial derivatives with respect to each unknown control point {math}`\tilde{P}_j` to zero. This yields one equation for each index {math}`j=0,\ldots,m`.
```{math}
:label: linear_sys
\sum_{k=0}^{m} M_{jk}\,\tilde{P}_k
=
b_j,
\qquad j=0,\ldots,m.
```
Where:
```{math}
M_{jk}=\int_0^1 B_j^m(t)\,B_k^m(t)\,dt
```
The index {math}`k` is the summation index over the basis functions, so for each fixed {math}`j` we sum {math}`k=0,\ldots,m`. {math}`M_{jk}` has a closed form:
```{math}
M_{jk}=
\frac{\binom{m}{j}\binom{m}{k}}{(2m+1)\binom{2m}{j+k}},
\qquad j,k=0,\ldots,m.
```

Analyzing the right-hand side of Eq. {numref}`linear_sys`:
```{math}
b_j=\int_0^1 c(t)\,B_j^m(t)\,dt = \int_0^1 \left( \sum_{i=0}^{n} P_i\,B_i^n(t)\right)\,B_j^m(t)\,dt
```
in the same way as before:

```{math}
b_j= \sum_{i=0}^{n} P_i\,N_{ji}, \qquad N_{ji} = \int_0^1 B_j^m(t)B_i^n(t)\,dt
```

where {math}`N_{ji}` has the following closed-form solution:
```{math}
N_{ji}=\frac{\binom{m}{j}\binom{n}{i}}{(m+n+1)\binom{m+n}{i+j}}
```

So the linear system to solve for the unknown control points is:
```{math}
[M]\tilde{P}=[N]P
```

where {math}`M` is the {math}`(m+1)\times(m+1)` Gram matrix of the basis:

```{math}
M=
\begin{pmatrix}
\int_0^1 B_0^m(t)\,B_0^m(t)\,dt & \cdots & \int_0^1 B_0^m(t)\,B_m^m(t)\,dt\\
\vdots & \ddots & \vdots\\
\int_0^1 B_m^m(t)\,B_0^m(t)\,dt & \cdots & \int_0^1 B_m^m(t)\,B_m^m(t)\,dt
\end{pmatrix},
```
and {math}`N_{ij}` is a {math}`(m+1) \times (n+1)` matrix:
```{math}
N=
\begin{pmatrix}
\int_0^1 B_0^m(t)\,B_0^n(t)\,dt & \cdots & \int_0^1 B_0^m(t)\,B_n^n(t)\,dt\\
\vdots & \ddots & \vdots\\
\int_0^1 B_m^m(t)\,B_0^n(t)\,dt & \cdots & \int_0^1 B_m^m(t)\,B_n^n(t)\,dt
\end{pmatrix},
```
Being the matrix {math}`M` symmetric and positive definite (the Bernstein basis is linearly independent), so the solution is unique. Solving this linear system (with stable method, e.g. Cholesky, not by inverting [M]) yields the reduced-degree Bézier curve that minimizes the mean (to be precice the {math}`L^2`) squared distance to the original curve.
:::


(degree-red-concrete)=
:::{prf:example .simple .dropdown} Least-Squares Degree Reduction: Cubic to Quadratic

We consider a concrete example of least-squares degree reduction from a cubic Bézier curve ({math}`n=3`) to a quadratic one ({math}`m=2`).

Let the original cubic Bézier curve be
```{math}
c(t)=\sum_{i=0}^{3} P_i\,B_i^3(t),
\qquad t\in[0,1].
```

We seek a quadratic Bézier curve
```{math}
\tilde{c}(t)=\sum_{j=0}^{2} \tilde{P}_j\,B_j^2(t),
```
that minimizes the squared error
```{math}
\int_0^1 \|c(t)-\tilde{c}(t)\|^2\,dt.
```

The minimization problem leads to the normal equations
```{math}
\sum_{k=0}^{2} M_{jk}\,\tilde{P}_k = b_j,
\qquad j=0,1,2,
```
with
```{math}
M_{jk} = \int_0^1 B_j^2(t)\,B_k^2(t)\,dt,
\qquad
b_j = \int_0^1 c(t)\,B_j^2(t)\,dt.
```

Since
```{math}
c(t)=\sum_{i=0}^3 P_i B_i^3(t),
```
we can write
```{math}
b_j = \sum_{i=0}^3 P_i N_{ji},
\qquad
N_{ji} = \int_0^1 B_j^2(t)\,B_i^3(t)\,dt.
```

Hence, the system becomes
```{math}
M\,\tilde{P} = N\,P.
```

For this case, the matrices are
```{math}
M=
\begin{pmatrix}
\frac15 & \frac{1}{10} & \frac{1}{30}\\
\frac{1}{10} & \frac{2}{15} & \frac{1}{10}\\
\frac{1}{30} & \frac{1}{10} & \frac15
\end{pmatrix},
```

```{math}
N=
\begin{pmatrix}
\frac16 & \frac{1}{10} & \frac{1}{20} & \frac{1}{60}\\
\frac{1}{15} & \frac{1}{10} & \frac{1}{10} & \frac{1}{15}\\
\frac{1}{60} & \frac{1}{20} & \frac{1}{10} & \frac16
\end{pmatrix}.
```

Solving the system yields the reduced control points in closed form:
```{math}
\begin{aligned}
\tilde{P}_0 &= \frac{19}{20}P_0+\frac{3}{20}P_1-\frac{3}{20}P_2+\frac{1}{20}P_3,\\
\tilde{P}_1 &= -\frac14 P_0+\frac34 P_1+\frac34 P_2-\frac14 P_3,\\
\tilde{P}_2 &= \frac{1}{20}P_0-\frac{3}{20}P_1+\frac{3}{20}P_2+\frac{19}{20}P_3.
\end{aligned}
```

These formulas apply componentwise and therefore hold for planar and spatial Bézier curves.

Let
```{math}
P_0=(0,0),\quad
P_1=(1,2),\quad
P_2=(3,2),\quad
P_3=(4,0).
```

The reduced quadratic control points are
```{math}
\tilde{P}_0=\left(-\frac{1}{10},0\right),\quad
\tilde{P}_1=(2,3),\quad
\tilde{P}_2=\left(\frac{41}{10},0\right).
```

This example illustrates how least-squares degree reduction distributes the approximation error over the parameter interval and does not, in general, preserve endpoint interpolation unless additional constraints are imposed.
:::


Great references for degree reduction are {cite}`Watkins_1988` and {cite}`Eck_1993`.

By using the slider at the bottom of the following figure you can have a visual demonstration of the degree elevation for a Bézier curve with 4 control points, hence degree 3 (cubic).

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import pandas as pd
import altair as alt

# ------------------------------------------------------------
# Bézier evaluation (no external helpers)
# ------------------------------------------------------------
def bernstein(n, i, u):
    """Bernstein polynomial B_i^n(u)."""
    from math import comb
    return comb(n, i) * (u**i) * ((1-u)**(n-i))

def bezier_eval(control_points, u_values):
    """
    Evaluate a Bézier curve at parameter values u_values.
    control_points: (n+1, 2) array
    u_values: array of u in [0,1]
    returns: (len(u_values), 2) array
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    U = np.asarray(u_values, dtype=float).reshape(-1, 1)

    C = np.zeros((len(U), 2))
    for i in range(n + 1):
        Bi = bernstein(n, i, U[:, 0]).reshape(-1, 1)
        C += P[i] * Bi
    return C

# ------------------------------------------------------------
# Degree reduction (least-squares via discrete sampling)
#   - No SciPy: solve linear least squares with numpy.linalg.lstsq
#   - Works for repeated reductions: n -> n-1 -> ... 
# ------------------------------------------------------------
def degree_reduce_ls(control_points, m=None, num_samples=200):
    """
    Reduce degree of a Bézier curve from degree n to degree m (m = n-1 by default)
    by least squares fitting of sampled points.

    control_points: (n+1, 2)
    m: target degree (if None, m = n-1)
    num_samples: how many parameter samples in [0,1]

    Returns: (m+1, 2) reduced control points
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    if n < 1:
        return P.copy()
    if m is None:
        m = n - 1
    m = int(m)
    if m < 0:
        raise ValueError("Target degree m must be >= 0.")
    if m >= n:
        # no reduction needed
        return P.copy()

    # Sample curve points from original
    u = np.linspace(0.0, 1.0, num_samples)
    C = bezier_eval(P, u)  # (num_samples, 2)

    # Build Bernstein basis matrix for degree m: A[j,i] = B_i^m(u_j)
    A = np.zeros((num_samples, m + 1), dtype=float)
    for i in range(m + 1):
        A[:, i] = bernstein(m, i, u)

    # Solve A @ Qx ~= Cx and A @ Qy ~= Cy in least squares
    Qx, *_ = np.linalg.lstsq(A, C[:, 0], rcond=None)
    Qy, *_ = np.linalg.lstsq(A, C[:, 1], rcond=None)
    Q = np.column_stack([Qx, Qy])

    return Q

def reduce_k_times(control_points, k, num_samples=200):
    """
    Repeatedly reduce degree k times (if possible).
    Degree stops at 0.
    """
    Pk = np.asarray(control_points, dtype=float)
    for _ in range(int(k)):
        n = len(Pk) - 1
        if n <= 0:
            break
        Pk = degree_reduce_ls(Pk, m=n-1, num_samples=num_samples)
    return Pk

# ------------------------------------------------------------
# Build dataframe for control polygon (points + segments)
# ------------------------------------------------------------
def build_control_polygon_df(P, k, tag="selected"):
    P = np.asarray(P, dtype=float)
    pts = []
    segs = []
    deg = len(P) - 1

    for i, p in enumerate(P):
        pts.append({
            "type": "point",
            "k": int(k),
            "tag": tag,
            "degree": int(deg),
            "i": int(i),
            "x": float(p[0]),
            "y": float(p[1]),
            "label": f"{tag}: P{i} (deg={deg})"
        })

    for i in range(len(P) - 1):
        p0, p1 = P[i], P[i + 1]
        segs.append({
            "type": "segment",
            "k": int(k),
            "tag": tag,
            "degree": int(deg),
            "i": int(i),
            "x0": float(p0[0]),
            "y0": float(p0[1]),
            "x1": float(p1[0]),
            "y1": float(p1[1]),
        })

    return pd.DataFrame(pts), pd.DataFrame(segs)

# ------------------------------------------------------------
# Example control points (edit freely)
# ------------------------------------------------------------
P0 = np.array([[0, 0], [1, 1], [2, 2], [3, 2], [4, 1.5], [5, 1], [6, 0]], dtype=float)

deg0 = len(P0) - 1

# Base curve samples (original curve)
u_curve = np.linspace(0, 1, 300)
curve0 = bezier_eval(P0, u_curve)
df_curve0 = pd.DataFrame({"u": u_curve, "x": curve0[:, 0], "y": curve0[:, 1]})

# ------------------------------------------------------------
# Precompute reductions for k = 0..K_MAX
# ------------------------------------------------------------
K_MAX = max(0, deg0)  # you cannot reduce more than the degree

all_pts = []
all_segs = []
all_curves = []
error_rows = []

# original polygon (tag="original"), stored at k=0
dfp0, dfs0 = build_control_polygon_df(P0, k=0, tag="original")
all_pts.append(dfp0)
all_segs.append(dfs0)

# reduced polygons + reduced curves for each k
for k in range(0, K_MAX + 1):
    Pk = reduce_k_times(P0, k, num_samples=250)
    dfp, dfs = build_control_polygon_df(Pk, k=k, tag="selected")
    all_pts.append(dfp)
    all_segs.append(dfs)

    # reduced curve samples
    Ck = bezier_eval(Pk, u_curve)
    df_ck = pd.DataFrame({
        "u": u_curve,
        "x": Ck[:, 0],
        "y": Ck[:, 1],
        "k": k
    })
    all_curves.append(df_ck)

    # RMSE against the original curve samples (iterative reduction quality)
    rmse = np.sqrt(np.mean(np.sum((curve0 - Ck) ** 2, axis=1)))
    deg_k = len(Pk) - 1
    error_rows.append({
        "k": k,
        "degree": int(deg_k),
        "rmse": float(rmse),
        "label": f"Degree Reduction | k = {k} | degree = {deg_k} | RMSE = {rmse:.4e}"
    })

df_pts = pd.concat(all_pts, ignore_index=True)
df_segs = pd.concat(all_segs, ignore_index=True)
df_curves = pd.concat(all_curves, ignore_index=True)
df_errors = pd.DataFrame(error_rows)

pts_data = alt.Data(values=df_pts.to_dict(orient="records"))
segs_data = alt.Data(values=df_segs.to_dict(orient="records"))
curves_data = alt.Data(values=df_curves.to_dict(orient="records"))
curve0_data = alt.Data(values=df_curve0.to_dict(orient="records"))
error_data = alt.Data(values=df_errors.to_dict(orient="records"))

# ------------------------------------------------------------
# Slider: number of reductions k
# ------------------------------------------------------------
k_slider = alt.binding_range(min=0, max=K_MAX, step=1, name="Reductions k: ")
k_param = alt.param(value=0, bind=k_slider)

# ------------------------------------------------------------
# Chart layers
# ------------------------------------------------------------
x_all = np.concatenate([
    df_curve0["x"].to_numpy(),
    df_curves["x"].to_numpy(),
    df_pts["x"].to_numpy(),
    df_segs["x0"].to_numpy(),
    df_segs["x1"].to_numpy(),
])
y_all = np.concatenate([
    df_curve0["y"].to_numpy(),
    df_curves["y"].to_numpy(),
    df_pts["y"].to_numpy(),
    df_segs["y0"].to_numpy(),
    df_segs["y1"].to_numpy(),
])

x_pad = 0.12 * (x_all.max() - x_all.min() + 1e-9)
y_pad = 0.12 * (y_all.max() - y_all.min() + 1e-9)
x_domain = [x_all.min() - x_pad, x_all.max() + x_pad]
y_domain = [y_all.min() - y_pad, y_all.max() + y_pad]

# Original curve (faint, for comparison)
orig_curve = alt.Chart(curve0_data).mark_line(
    opacity=0.25,
    strokeWidth=2.0,
    color="#0f172a"
).encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=y_domain)),
)

# Reduced curve (selected k)
reduced_curve = alt.Chart(curves_data).mark_line(
    strokeWidth=3.0,
    color="#ef4444"
).encode(
    x="x:Q",
    y="y:Q",
).transform_filter(
    alt.datum.k == k_param
)

# Shadows: all reduced polygons for k <= selected
shadow_segments = alt.Chart(segs_data).mark_rule(
    strokeWidth=1.5,
    opacity=0.18,
    color="#334155"
).encode(
    x="x0:Q", y="y0:Q", x2="x1:Q", y2="y1:Q"
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.tag == "selected") & (alt.datum.k <= k_param)
)

shadow_points = alt.Chart(pts_data).mark_point(
    filled=True,
    size=48,
    opacity=0.16,
    color="#334155"
).encode(
    x="x:Q", y="y:Q",
    tooltip=["k:O", "degree:O", "i:O", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.tag == "selected") & (alt.datum.k <= k_param)
)

# Reduced control polygon (selected k)
sel_segments = alt.Chart(segs_data).mark_rule(
    strokeWidth=3.0,
    opacity=0.95,
    color="#000000"
).encode(
    x="x0:Q", y="y0:Q", x2="x1:Q", y2="y1:Q"
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.tag == "selected") & (alt.datum.k == k_param)
)

sel_points = alt.Chart(pts_data).mark_point(
    filled=True,
    size=95,
    color="#000000"
).encode(
    x="x:Q", y="y:Q",
    tooltip=["k:O", "degree:O", "i:O", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.tag == "selected") & (alt.datum.k == k_param)
)

# Dynamic header row (outside plotting area)
header = alt.Chart(
    error_data
).mark_text(
    align="left",
    baseline="middle",
    fontSize=13,
    color="#334155"
).encode(
    text="label:N"
).transform_filter(
    alt.datum.k == k_param
).properties(width=760, height=28)

main = (
    orig_curve
    + reduced_curve
    + shadow_segments
    + shadow_points
    + sel_segments
    + sel_points
).properties(width=760, height=440)

chart = alt.vconcat(
    header,
    main,
    spacing=6
).add_params(k_param).properties(
    title="Interactive Degree Reduction (Least Squares Approx.)"
)

chart
```

# Conclusions
Degree elevation and degree reduction play complementary roles in geometric modeling. Degree elevation is exact: it increases the polynomial degree and the number of control points while preserving the curve geometry. It is mainly used to match degrees across curves and patches and to enable operations that require a common polynomial order.

Degree reduction is generally approximate: it seeks a lower-degree representation that is as close as possible to the original curve according to a chosen metric, typically least squares. It reduces model complexity and can improve efficiency, but introduces approximation error.


```{figure}../imgs/degree_reduction.png
:label: degree_reduction_example
:alt: Degree reduction example with original and reduced Bézier curves
:align: center

Degree elevation and reduction example: original curve (black) and reduced curve (red).
```

The examples in this chapter show this trade-off clearly. Elevation leaves the curve unchanged but modifies the control polygon, while reduction changes both the control polygon and the curve shape. The iterative reduction plot and its RMSE indicator make this effect explicit: as reduction steps increase, complexity decreases and approximation error typically grows. A static, yet quite significative example is provided in {ref}`degree_reduction_example`.









