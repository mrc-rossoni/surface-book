---

jupyter:

  jupytext:

    text_representation:

      extension: .md

      format_name: markdown

  kernelspec:

    display_name: Python 3 (ipykernel)

    language: python

    name: python3

  language_info:

    name: python

    nbconvert_exporter: python

    pygments_lexer: ipython3

  short_title: images

  title: images and figures

---

# Bézier Curves
Bézier curves are a foundational building block for surface modeling in engineering CAD systems.
Although industrial models typically rely on B-splines and NURBS, Bézier curves remain the simplest case
where the geometry is entirely controlled by a finite set of points and a well-defined basis. They are used for local shape editing (via control points), smooth profile definition (aerodynamics, industrial design), construction of surface patches and as a **conceptual entry point to B-splines**.

As we discussed in the last part of the Chapter (REF to CH), all the matter of CAD boils down to chosing a "proper" basis function to represent the curve (and then surfances) in the 3D. THe process is basically done by lying down some requirements and looking "out there" to find the optimal "functional space" whose funtions satisfies those requirement. 

As per the Bézier curves, this functional space is the one defined by the so called "Bernstein basis". We'll dive into it in one of the following chapter. As a matter of fact, from an engineering perspective, the "geometrical interpretaion" should, in my opinion, have the priority. 


## Geometric Interpretation: the "de Casteljau's" Algorithm

Let’s start with a simple and intuitive idea. Given two points in the 2D plane, {math}`P_0` and {math}`P_1`, what is the simplest way to connect them? The answer is trivial: a straight line.

Once the segment is defined, we can describe _any point along it_ by smoothly moving from {math}`P_0` to {math}`P_1`. To do so, we introduce a parameter {math}`t \in [0,1]`. The intermediate point {math}`P(t)` is defined as:

```{math}
P(t) = (1-t)\,P_0 + t\,P_1
```
This operation is called **linear interpolation**, and it is the simplest blending function in geometry processing and CAD. The parameter {math}`t` controls how far we move from {math}`P_0` to {math}`P_1`: when {math}`t=0` we obtain {math}`P_0`, when {math}`t=1` we obtain {math}`P_1`, and for intermediate values {math}`P(t)` lies between them.

Now, let’s add a third point. We can interpolate between the second point from before ({math}`P_1`) and the new point ({math}`P_2`), again using linear interpolation. The same idea applies if we keep adding points: at each step we interpolate between consecutive points and generate a new set of intermediate points.So we can generalize the idea by making use of recursion. Let:
- {math}`n` be the degree of the curve;
- {math}`N_p = n+1` be the number of points;
- {math}`r` be the recursion level (depth), with {math}`r = 0,1,\dots,n`;
- {math}`t \in [0,1]` be the interpolation parameter.
- {math}`P_i^{(r)}(t)` be the *i-th* intermediate point at recursion level *r* for the parameter value *t*.

The algorithm starts from the set of control points:

```{math}
\{P_0^{(0)}, P_1^{(0)}, \dots, P_n^{(0)}\}
```
At each recursion level, we linearly interpolate consecutive points to form a new (smaller) set:

```{math}
P_i^{(r)}(t) = (1-t)\,P_i^{(r-1)}(t) + t\,P_{i+1}^{(r-1)}(t)
\quad \text{for } i = 0,\dots,n-r
```

Algorithmically:

1. Initialize the {math}`N_p = n+1` control points {math}`P_0, P_1, \dots, P_n` and choose a value {math}`t \in [0,1]`.
2. at level {math}`r = 1`, linearly interpolate between consecutive points and compute {math}`N_p - 1` new points:
   {math}`P_0^{(1)}(t), \dots, P_{n-1}^{(1)}(t)`.
3. Increase the recursion level {math}`r \leftarrow r+1` and repeat the same interpolation step on the newly generated points.
4. Continue until {math}`r = n`, where only one point remains:

```{math}
P(t) = P_0^{(n)}(t)
```

Repeating the procedure for many values of {math}`t` generates a whole curve. The final point of each recursion {math}`P(t)` lies on a curve, the so called **Bézier curve**. The agorithm just described is the **de Casteljau’s Algorithm**


The point {math}`P(t)` is the result of the recursion for a given value of {math}`t`, and it lies on the so called **Bézier curve**, defined by the control points ({math}`P_0, P_1, \dots, P_n`).
By repeating the procedure for many values of {math}`t`, we obtain the entire **Bézier curve**. The recursive construction described above is known as **de Casteljau’s algorithm**.

Paul de Casteljau developed the algorithm at Citroën as a recursive method for evaluating Bézier curves. The method provides an intuitive geometric construction, where the curve is defined by successive (linear) interpolations between control points. Unlike polynomial-based approaches, De Casteljau's algorithm relies solely on linear interpolation, making it numerically stable and robust.

```{prf:algorithm} de Casteljau’s algorithm
Given a set of control points {math}`P_0, P_1, \dots, P_n \in \mathbb{E}^d` and a parameter {math}`t \in [0,1]`, define the recursion:

- Initialization: {math}`P_i^{(0)}(t) = P_i, \qquad i = 0,\dots,n`
- Recursion for {math}`r = 1,\dots,n` and {math}`i = 0,\dots,n-r`:

   $$
   P_i^{(r)}(t) = (1 - t)\,P_i^{(r-1)}(t) + t\,P_{i+1}^{(r-1)}(t)
   $$

The point {math}`P_0^{(n)}(t)` is the point corresponding to the parameter value {math}`t` on the Bézier curve of degree {math}`n`.
```

By using the slider at the bottom of the following figure you can have a visual demonstration of the de Casteljau’s algorithm for a Bézier curve with 4 control points, hence degree 3 (cubic).

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

    # Sum_i P_i * B_i^n(u)
    C = np.zeros((len(U), 2))
    for i in range(n + 1):
        Bi = bernstein(n, i, U[:, 0]).reshape(-1, 1)
        C += P[i] * Bi
    return C

# ------------------------------------------------------------
# De Casteljau levels (geometric construction)
# ------------------------------------------------------------
def de_casteljau_levels(control_points, u):
    """
    Returns all levels of De Casteljau points for a given u.
    levels[r][i] = point at level r, index i
    r = 0..n, i = 0..n-r
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    levels = [P.copy()]

    Q = P.copy()
    for r in range(1, n + 1):
        Q_new = []
        for i in range(n - r + 1):
            pt = (1 - u) * Q[i] + u * Q[i + 1]
            Q_new.append(pt)
        Q = np.array(Q_new)
        levels.append(Q.copy())

    return levels

# ------------------------------------------------------------
# Build dataframe with points + segments for De Casteljau triangle
# ------------------------------------------------------------
def build_casteljau_dataframe(control_points, u):
    levels = de_casteljau_levels(control_points, u)
    records = []

    # Points
    for r, pts in enumerate(levels):
        for i, p in enumerate(pts):
            records.append({
                "type": "point",
                "level": r,
                "i": i,
                "x": p[0],
                "y": p[1],
                "label": f"P^{i}_{r}"
            })

    # Segments within each level (visualize the "control polygon" at that level)
    for r, pts in enumerate(levels):
        for i in range(len(pts) - 1):
            p0, p1 = pts[i], pts[i + 1]
            records.append({
                "type": "segment",
                "level": r,
                "i": i,
                "x0": p0[0],
                "y0": p0[1],
                "x1": p1[0],
                "y1": p1[1]
            })

    return pd.DataFrame(records)

# ------------------------------------------------------------
# Example control points (edit freely)
# ------------------------------------------------------------
P = np.array([
    [0.0, 0.0],
    [0.2, 0.9],
    [0.8, 0.9],
    [1.0, 0.0],
])

n = len(P) - 1

# Base curve samples (static visualization)
u_curve = np.linspace(0, 1, 250)
curve_pts = bezier_eval(P, u_curve)
df_curve = pd.DataFrame({"u": u_curve, "x": curve_pts[:, 0], "y": curve_pts[:, 1]})

# ------------------------------------------------------------
# Parameter slider for u
# ------------------------------------------------------------
u_slider = alt.binding_range(min=0, max=1, step=0.01, name="t: ")
u_param = alt.param(value=0.35, bind=u_slider)

# Precompute De Casteljau geometry for a grid of u values (so Vega can filter)
u_grid = np.linspace(0, 1, 101)
df_all = []
for u in u_grid:
    df_u = build_casteljau_dataframe(P, float(u))
    df_u["u"] = u
    df_all.append(df_u)
df_all = pd.concat(df_all, ignore_index=True)

casteljau_data = alt.Data(values=df_all.to_dict(orient="records"))
curve_data = alt.Data(values=df_curve.to_dict(orient="records"))

# ------------------------------------------------------------
# Chart layers
# ------------------------------------------------------------

# Bézier curve

x_domain = [-0.1, 1.1]
y_domain = [-0.1, 1.1]

curve_before = alt.Chart(curve_data).mark_line().encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=y_domain)),
).transform_filter(
    alt.datum.u <= u_param
)

curve_after = alt.Chart(curve_data).mark_line(opacity=0.2).encode(
    x="x:Q",
    y="y:Q",
).transform_filter(
    alt.datum.u > u_param
)

bezier_curve = (curve_after + curve_before).properties(height=420)

# Level 0 control polygon (dashed)
control_segments = alt.Chart(casteljau_data).mark_rule(strokeDash=[6, 4]).encode(
    x="x0:Q", y="y0:Q",
    x2="x1:Q", y2="y1:Q"
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.level == 0) & (alt.datum.u == u_param)
)

# Intermediate segments (levels > 0)
casteljau_segments = alt.Chart(casteljau_data).mark_rule().encode(
    x="x0:Q", y="y0:Q",
    x2="x1:Q", y2="y1:Q",
    strokeWidth=alt.value(2),
    opacity=alt.value(0.85)
).transform_filter(
    (alt.datum.type == "segment") & (alt.datum.level > 0) & (alt.datum.u == u_param)
)

level_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

# Intermediate points (all levels)
casteljau_points = alt.Chart(casteljau_data).mark_point(filled=True, size=90).encode(
    x="x:Q",
    y="y:Q",
    color=alt.Color(
        "level:O",
        title="Recursion",
        scale=alt.Scale(domain=list(range(n+1)), range=level_colors)
    ),
    tooltip=["label:N", "level:O", "i:O", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.u == u_param)
)

# Final point C(u): last level, single point (level n, i=0)
final_point = alt.Chart(casteljau_data).mark_point(size=220, filled=True).encode(
    x="x:Q",
    y="y:Q",
    color=alt.value("red"),
    tooltip=["label:N", "x:Q", "y:Q"]
).transform_filter(
    (alt.datum.type == "point") & (alt.datum.level == n) & (alt.datum.i == 0) & (alt.datum.u == u_param)
)

# Combine everything
chart = (
    bezier_curve
    + control_segments
    + casteljau_segments
    + casteljau_points
    + final_point
).add_params(u_param).properties(
    title="De Casteljau’s Algorithm — Step-by-step Geometric Construction"
)

chart
```


:::{note .simple .dropdown icon=false open=false} Complexity Analysis

The computational complexity of de Casteljau’s algorithm can be analyzed as follows. For $N_p$ control points, the algorithm requires computing $N_p -1$ interpolations at each recursion level. Hence, the total number of interpolations performed follows a triangular sum:

  $$
  \sum_{r=1}^{N_p-1}  r\frac{(N_p-1) N_p}{2}
  $$

Therefore, the **time complexity is $ O(n^2) $**, meaning that as the number of control points increases, the computation time grows quadratically. More precisely, the computational complexity is  **$ O(d n^2) $** where d is the number of dimensions.

This quadratic complexity is evident in the generated plot (below), where computation time increases non-linearly as control points increase.

```{figure}./imgs/de_casteljau_time.png
:label: de_casteljau_time
:alt: Number of control point vs Computational Time
:align: center

Number of control point vs Computational Time
```

```{figure}./imgs/de_casteljau_time_log.png
:label: de_casteljau_time_log
:alt: Number of control point vs Computational Time - Log-log scale
:align: center

Number of control point vs Computational Time - Log-log scale
```

De Casteljau’s algorithm quadratic complexity can become a bottleneck for high-degree curves. {cite}`Wo_ny_2020` {cite}`Farin_1983`

:::

Python Implementation: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mrc-rossoni/surface-book/blob/main/book/partA/02_lab_bezier.ipynb)


## Bézier Curve with Berstein Polynomials

De Casteljau’s algorithm provides a geometric and numerically stable method for evaluating Bézier curves, relying exclusively on repeated linear interpolation. Each recursion step forms affine combinations of consecutive points. Therefore, the final point on the curve must be expressible as a weighted sum of the original control points, where the weights depend only on the parameter {math}`t`. As a matter of fact, Bézier approached the curves from a different perspective, highlighting the need for an *explicit* representation of the curve. This motivates an explicit basis-function representation of the curve:

```{math}
C(t)=\sum_{i=0}^{n} P_i\,N_i(t),
\qquad t\in[0,1]
```

where {math}`P_i` are the vertices of the control polygon, and {math}`N_i(t)` are scalar basis functions. Bézier set forth the properties that the {math}`N_i(t)` basis functions must have and look for (i.e. deliberately choose!) specific functions that that make the representation suitable for geometric design:
- **Endpoint interpolation:** the curve must interpolate the first and last control points.
- **Local control of derivatives:** the {math}`r`-th derivative at an endpoint must depend only on the {math}`r` neighboring control points.  
  In particular, the tangent direction at the endpoints is controlled by the first and last edge of the control polygon, and in fact:
  ```{math}
  C'(0)=n(P_1-P_0),\qquad C'(1)=n(P_n-P_{n-1}).
  ```
- **Symmetry:** reversing the control points should not change the curve shape, which corresponds to symmetry under {math}`t \mapsto 1-t`.

A family of polynomials satisfying these requirements is given by the **Bernstein polynomials**.

:::{prf:definition .simple icon=false open=true}
The Bernstein polynomial of degree {math}`n` and index {math}`i` is defined as:

```{math}
B_i^n(t)=\binom{n}{i}t^i(1-t)^{n-i}
```

where the binomial coefficient is:

```{math}
\binom{n}{i}=\frac{n!}{i!(n-i)!}.
```
:::

The following interactive chart shows how the Bernstein polynomials looks like by changing the degree:


```{code-cell} ipython3
:tags: [remove-input]
import numpy as np
import altair as alt
from math import comb

# ------------------------------------------------------------
# Bernstein polynomial
# ------------------------------------------------------------
def bernstein_poly(n, i, t):
    """Bernstein polynomial B_i^n(t)."""
    return comb(n, i) * (t**i) * ((1 - t)**(n - i))

# ------------------------------------------------------------
# Precompute Bernstein basis for degrees 1..N_MAX
# ------------------------------------------------------------
N_MAX = 10
t_curve = np.linspace(0, 1, 250)

basis_values = []
for n in range(1, N_MAX + 1):
    for i in range(n + 1):
        for t in t_curve:
            basis_values.append({
                "n": n,
                "i": i,
                "t": float(t),
                "value": float(bernstein_poly(n, i, float(t))),
                "label": f"B_{i}^{n}"
            })

basis_data = alt.Data(values=basis_values)

# ------------------------------------------------------------
# Precompute values at selected t (for marker + label)
# ------------------------------------------------------------
t_grid = np.linspace(0, 1, 101)

marker_values = []
for n in range(1, N_MAX + 1):
    for t_sel in t_grid:
        t_sel = float(t_sel)
        for i in range(n + 1):
            val = bernstein_poly(n, i, t_sel)
            marker_values.append({
                "n": n,
                "i": i,
                "t_sel": t_sel,
                "value": float(val),
                "value_txt": f"{val:.2f}",
                "label": f"B_{i}^{n}"
            })

marker_data = alt.Data(values=marker_values)

# ------------------------------------------------------------
# Sliders
# ------------------------------------------------------------
n_slider = alt.binding_range(min=1, max=N_MAX, step=1, name="degree n: ")
n_param = alt.param(value=3, bind=n_slider)

t_slider = alt.binding_range(min=0, max=1, step=0.01, name="t: ")
t_param = alt.param(value=0.30, bind=t_slider)

# ------------------------------------------------------------
# Color palette (matching your De Casteljau example)
# ------------------------------------------------------------
casteljau_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
color_scale = alt.Scale(range=casteljau_palette)

# ------------------------------------------------------------
# Plot: Bernstein basis functions (filtered by degree)
# ------------------------------------------------------------
basis_lines = alt.Chart(basis_data).mark_line().encode(
    x=alt.X("t:Q", title="t"),
    y=alt.Y("value:Q", title="B_i^n(t)"),
    color=alt.Color(
    "label:N",
    title="Bernstein basis",
    scale=color_scale
    ),
    tooltip=["label:N", "t:Q", "value:Q"]
).transform_filter(
    alt.datum.n == n_param
).properties(
    height=450,
    title="Bernstein Basis Polynomials"
)

# Markers at selected t
markers = alt.Chart(marker_data).mark_point(size=120, filled=True).encode(
    x=alt.X("t_sel:Q"),
    y=alt.Y("value:Q"),
    color=alt.Color(
    "label:N",
    title="Bernstein basis",
    scale=color_scale
    ),
    tooltip=["i:O", "value:Q"]
).transform_filter(
    (alt.datum.n == n_param) & (alt.datum.t_sel == t_param)
)

# Labels next to markers
labels = alt.Chart(marker_data).mark_text(
    align="left",
    dx=8,
    dy=-6,
    fontSize=12
).encode(
    x="t_sel:Q",
    y="value:Q",
    text="value_txt:N",
    color=alt.Color(
    "label:N",
    title="Bernstein basis",
    scale=color_scale
    )
).transform_filter(
    (alt.datum.n == n_param) & (alt.datum.t_sel == t_param)
)

# Combine
chart = (basis_lines + markers + labels).add_params(n_param, t_param)

chart

```


Replacing the generic basis {math}`N_i(t)` with the Bernstein basis yields the Bézier curve:

```{math}
C(t)=\sum_{i=0}^{n}P_i\,B_i^n(t),
\qquad t\in[0,1].
```

If there are {math}`n+1` control points, then {math}`C(t)` is a polynomial curve of **degree {math}`n`**. In this sense, the control points {math}`P_i` are the coefficients of the curve in the Bernstein basis.

```{code-cell} ipython3
:tags: [remove-input]
import numpy as np
import altair as alt
from math import comb

# ------------------------------------------------------------
# Bernstein basis
# ------------------------------------------------------------
def bernstein_poly(n, i, t):
    """Bernstein polynomial B_i^n(t)."""
    return comb(n, i) * (t**i) * ((1 - t) ** (n - i))


def bernstein_basis_matrix(n, t_values):
    """
    Full Bernstein basis matrix:
    rows correspond to t, columns to i.
    shape = (len(t_values), n+1)
    """
    t_values = np.asarray(t_values, dtype=float)
    B = np.zeros((len(t_values), n + 1))
    for i in range(n + 1):
        B[:, i] = [bernstein_poly(n, i, float(t)) for t in t_values]
    return B


# ------------------------------------------------------------
# Bézier curve evaluation using Bernstein basis
# ------------------------------------------------------------
def bezier_eval(control_points, t_values):
    """
    Evaluate Bézier curve points using Bernstein basis.
    control_points: (n+1, 2)
    t_values: array in [0,1]
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    B = bernstein_basis_matrix(n, t_values)  # (m, n+1)
    C = B @ P                                # (m, 2)
    return C, B


# ------------------------------------------------------------
# Example control points (edit freely)
# ------------------------------------------------------------
cps = np.array([
    [0.0, 0.0],
    [3.0, 2.0],
    [6.0, 2.0],
    [8.0, 0.0],
])

n = len(cps) - 1
t_curve = np.linspace(0, 1, 250)

curve_pts, B_curve = bezier_eval(cps, t_curve)

# ------------------------------------------------------------
# Build "values" lists (Altair-friendly, Pandas-free)
# ------------------------------------------------------------
curve_values = [{"t": float(t), "x": float(p[0]), "y": float(p[1])}
                for t, p in zip(t_curve, curve_pts)]

control_values = [{"x": float(p[0]), "y": float(p[1]), "i": i}
                  for i, p in enumerate(cps)]

basis_values = []
for i in range(n + 1):
    for t, val in zip(t_curve, B_curve[:, i]):
        basis_values.append({
            "t": float(t),
            "value": float(val),
            "i": i,
            "label": f"B_{n},{i}"
        })

# Precompute selected basis values + point on curve for slider display
t_grid = np.linspace(0, 1, 101)

selected_basis_values = []
selected_point_values = []

for t_sel in t_grid:
    t_sel = float(t_sel)

    # Bernstein weights at t_sel
    B_sel = [bernstein_poly(n, i, t_sel) for i in range(n + 1)]
    C_sel = np.dot(B_sel, cps)

    # Store weights (for markers + labels)
    for i in range(n + 1):
        selected_basis_values.append({
            "t_sel": t_sel,
            "i": i,
            "B": float(B_sel[i]),
            "B_txt": f"{B_sel[i]:.2f}"
        })

    # Store point on curve
    selected_point_values.append({
        "t_sel": t_sel,
        "x": float(C_sel[0]),
        "y": float(C_sel[1])
    })

# Wrap into Altair Data
curve_data = alt.Data(values=curve_values)
control_data = alt.Data(values=control_values)
basis_data = alt.Data(values=basis_values)
selected_basis_data = alt.Data(values=selected_basis_values)
selected_point_data = alt.Data(values=selected_point_values)

# ------------------------------------------------------------
# Slider parameter
# ------------------------------------------------------------
t_slider = alt.binding_range(min=0, max=1, step=0.01, name="t: ")
t_param = alt.param(value=0.30, bind=t_slider)

# ------------------------------------------------------------
# Consistent palette (matching your De Casteljau example)
# ------------------------------------------------------------
level_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # up to cubic
palette = level_colors[:n+1]
color_scale = alt.Scale(domain=list(range(n + 1)), range=palette)

# ------------------------------------------------------------
# Plot 1: Bézier curve with "before/after" styling + control polygon + point
# ------------------------------------------------------------
x_min = min(v["x"] for v in curve_values) - 0.5
x_max = max(v["x"] for v in curve_values) + 0.5
y_min = min(v["y"] for v in curve_values) - 0.5
y_max = max(v["y"] for v in curve_values) + 0.5

curve_before = alt.Chart(curve_data).mark_line().encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=[x_min, x_max])),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=[y_min, y_max])),
).transform_filter(
    alt.datum.t <= t_param
)

curve_after = alt.Chart(curve_data).mark_line(opacity=0.2).encode(
    x="x:Q",
    y="y:Q",
).transform_filter(
    alt.datum.t > t_param
)

control_polygon = alt.Chart(control_data).mark_line(
    point=True,
    strokeDash=[6, 4]
).encode(
    x="x:Q",
    y="y:Q",
    tooltip=["i:O", "x:Q", "y:Q"]
)

selected_point = alt.Chart(selected_point_data).mark_point(
    size=220, filled=True
).encode(
    x="x:Q",
    y="y:Q",
    color=alt.value("red"),
    tooltip=["t_sel:Q", "x:Q", "y:Q"]
).transform_filter(
    alt.datum.t_sel == t_param
)

bezier_plot = (
    (curve_after + curve_before + control_polygon + selected_point)
    .add_params(t_param)
    .properties(height=380, title="Bézier Curve — before/after styling and point at selected t")
)

# ------------------------------------------------------------
# Plot 2: Bernstein basis functions + marker + value labels at selected t
# ------------------------------------------------------------
basis_lines = alt.Chart(basis_data).mark_line().encode(
    x=alt.X("t:Q", title="t"),
    y=alt.Y("value:Q", title="B_i^n(t)"),
    color=alt.Color("i:O", title="i", scale=color_scale),
    tooltip=["label:N", "t:Q", "value:Q"]
).properties(
    height=380,
    title=f"Bernstein Basis Polynomials (n={n})"
)

basis_markers = alt.Chart(selected_basis_data).mark_point(
    size=90, filled=True
).encode(
    x="t_sel:Q",
    y="B:Q",
    color=alt.Color("i:O", scale=color_scale),
    tooltip=["i:O", "B:Q"]
).transform_filter(
    alt.datum.t_sel == t_param
)

basis_labels = alt.Chart(selected_basis_data).mark_text(
    align="left",
    dx=6,
    dy=-6,
    fontSize=12
).encode(
    x="t_sel:Q",
    y="B:Q",
    text="B_txt:N",
    color=alt.Color("i:O", scale=color_scale)
).transform_filter(
    alt.datum.t_sel == t_param
)

bernstein_plot = (
    (basis_lines + basis_markers + basis_labels)
    .add_params(t_param)
    .properties(height=380)
)

# ------------------------------------------------------------
# Combine plots vertically
# ------------------------------------------------------------
chart = alt.vconcat(bezier_plot, bernstein_plot).resolve_scale(color="independent")

chart

```

Moreover, every intermediate point in De Casteljau’s construction is itself a Bézier combination:

```{math}
P_i^{(r)}(t)=\sum_{j=0}^{r}P_{i+j}B_j^{r}(t),
\qquad r=0,\dots,n.
```

and the curve point corresponds to the final recursion step:

```{math}
C(t)=P_0^{(n)}(t)=\sum_{j=0}^{n}P_jB_j^{n}(t).
```

As a matter of fact, by expanding the De Casteljau recursion, one finds that the functions {math}`N_i(t)` are precisely the Bernstein polynomials. Thus, Bernstein polynomials provide the closed-form (non-recursive) expression of the same geometric construction. {ref}`(See proof)<bern-deCast-equiv-proof>`!

(bern-deCast-equiv-proof)=
:::{prf:proof .simple .dropdown icon=false open=false} Proof that De Casteljau’s construction leads to Bernstein polynomials
We prove by induction on the recursion level {math}`r` that every intermediate point in De Casteljau’s algorithm can be written as:

```{math}
P_i^{(r)}(t)=\sum_{j=0}^{r} P_{i+j}\,B_j^{r}(t),
\qquad r=0,\dots,n,\;\; i=0,\dots,n-r.
```

where {math}`B_j^r(t)` are Bernstein polynomials:

```{math}
B_j^r(t)=\binom{r}{j}t^j(1-t)^{r-j}.
```

**Base case ({math}`r=0`).**  
At recursion level {math}`r=0`, we have {math}`P_i^{(0)}(t)=P_i`. Since {math}`B_0^0(t)=1`, the formula holds:

```{math}
P_i^{(0)}(t)=P_i=\sum_{j=0}^{0}P_{i+j}B_j^0(t).
```

**Induction step.**  
Assume the statement holds at level {math}`r-1`. Then, by the De Casteljau recursion:

```{math}
P_i^{(r)}(t)=(1-t)P_i^{(r-1)}(t)+tP_{i+1}^{(r-1)}(t).
```

Using the induction hypothesis:

```{math}
P_i^{(r-1)}(t)=\sum_{j=0}^{r-1}P_{i+j}B_j^{r-1}(t),
\qquad
P_{i+1}^{(r-1)}(t)=\sum_{j=0}^{r-1}P_{i+1+j}B_j^{r-1}(t).
```

Substituting:

```{math}
P_i^{(r)}(t)=
\sum_{j=0}^{r-1}P_{i+j}(1-t)B_j^{r-1}(t)
+
\sum_{j=0}^{r-1}P_{i+1+j}\,t\,B_j^{r-1}(t).
```

Reindex the second sum with {math}`k=j+1` (so {math}`k=1,\dots,r`):

```{math}
P_i^{(r)}(t)=
P_i(1-t)B_0^{r-1}(t)
+
\sum_{j=1}^{r-1}P_{i+j}\left[(1-t)B_j^{r-1}(t)+tB_{j-1}^{r-1}(t)\right]
+
P_{i+r}tB_{r-1}^{r-1}(t).
```

Now recall the Bernstein recursion identity:

```{math}
B_j^r(t)=(1-t)B_j^{r-1}(t)+tB_{j-1}^{r-1}(t).
```

Therefore, the expression becomes:

```{math}
P_i^{(r)}(t)=\sum_{j=0}^{r}P_{i+j}B_j^{r}(t),
```

which completes the induction.

Finally, at recursion level {math}`r=n` we obtain the curve point:

```{math}
C(t)=P_0^{(n)}(t)=\sum_{j=0}^{n}P_jB_j^{n}(t).
```

Hence, the weights produced by De Casteljau’s geometric construction are exactly the Bernstein polynomials.
:::


Python Implementation: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mrc-rossoni/surface-book/blob/main/code/02_Bernstein.ipynb)


## Properties
The key properties are: 

1. Endpoint interpolation {math}`C(0)=P_0,C(1)=P_n`.
2. Convex hull property. For {math}`t \in [0,1]`, the curve lies inside the convex hull of its control points. This gives a strong geometric bound and makes interactive editing predictable. The Bèzier curves always lies in the convex hull (interference checking). A planar polygon always generates a planar curve.
3. Variation diminishing property. The curve does not oscillate more than its control polygon, which makes Bézier curves stable and well-behaved for design.
4. Approximating curve: it does not pass through the control points. Better global and local control on the shape of the curve (there are better ways!)
5. Invariant under affine maps: Translation, scaling, rotation and shear are example of affine maps. NB: they are not projectively invariant!
6. Invariant under affine parameter transformation: i.e.: not bounded to the interval [0,1].




## Matrix Form

NB: outer product, denoted with $\otimes$, is defined as follows. Given two vectors $u = (1 \times m)$ and $v = (1 \times n)$:

$$
\mathbf {u} =
\begin{bmatrix} 
u_{1} \\ 
u_{2} \\ 
\vdots \\ 
u_{m} 
\end{bmatrix}, 
\quad 
\mathbf {v} =
\begin{bmatrix} 
v_{1} \\ 
v_{2} \\ 
\vdots \\ 
v_{n} 
\end{bmatrix}
$$

The outer product, $\mathbf {u} \otimes \mathbf {v}$, is a $m \times n$ matrix:

$$
\mathbf {u} \otimes \mathbf {v} =\mathbf {A} =
\begin{bmatrix} 
u_{1}v_{1} & u_{1}v_{2} & \dots & u_{1}v_{n} \\ 
u_{2}v_{1} & u_{2}v_{2} & \dots & u_{2}v_{n} \\ 
\vdots & \vdots & \ddots & \vdots \\ 
u_{m}v_{1} & u_{m}v_{2} & \dots & u_{m}v_{n} 
\end{bmatrix}
$$

## Bézier Curve in Matrix Form
Using the outer product notation, we rewrite the Bézier curve equation as:

$$
\mathbf{P}(t) =
\left( \mathbf{B}(t) \otimes \mathbf{P} \right)
$$

where:
- $\mathbf{B}(t)$ is the Bernstein basis vector:

$$
\mathbf{B}(t) =
\begin{bmatrix}
B_{n,0}(t) \\ 
B_{n,1}(t) \\ 
\vdots \\ 
B_{n,n-1}(t)
\end{bmatrix}
$$

- $\mathbf{P}$ is the vector of control points:

$$
\mathbf{P} =
\begin{bmatrix}
\mathbf{P}_0 \\ 
\mathbf{P}_1 \\ 
\vdots \\ 
\mathbf{P}_{n-1}
\end{bmatrix}
$$

Since the outer product results in a summation of element-wise products, the final Bézier curve equation remains:

$$
\mathbf{P}(t) =
\mathbf{B}(t)^\top \mathbf{P}
$$

Alternatively, using the binomial coefficient matrix:

$$
\mathbf{P}(t) =
\begin{bmatrix}
1 & - (n-1) & \binom{n-1}{2} & \dots & (-1)^{n-1} \\
0 & 1 & - (n-2) & \dots & (-1)^{n-2} \binom{n-1}{n-1} \\
0 & 0 & 1 & \dots & (-1)^{n-3} \binom{n-1}{n-2} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \dots & 1
\end{bmatrix}
\begin{bmatrix}
1 \\
t \\
t^2 \\
\vdots \\
t^{n-1}
\end{bmatrix}
\begin{bmatrix}
\mathbf{P}_0 \\
\mathbf{P}_1 \\
\vdots \\
\mathbf{P}_{n-1}
\end{bmatrix}
$$

This representation generalizes Bézier curves for any number of control points, allowing for computational efficiency using matrix multiplication.


#### Quadratic Bézier Curve

For a quadratic Bézier curve defined by three control points $\mathbf{P}_0, \mathbf{P}_1, \mathbf{P}_2$, the parametric equation is:

$$
\mathbf{P}(t) = (1-t)^2 \mathbf{P}_0 + 2(1-t)t \mathbf{P}_1 + t^2 \mathbf{P}_2
$$

which can be rewritten in matrix form as:

$$
\mathbf{P}(t) =
\begin{bmatrix}
(1-t)^2 & 2(1-t)t & t^2
\end{bmatrix}
\begin{bmatrix}
\mathbf{P}_0 \\
\mathbf{P}_1 \\
\mathbf{P}_2
\end{bmatrix}
$$

Alternatively, using a matrix representation:

$$
\mathbf{P}(t) =
\begin{bmatrix}
1 & -2 & 1 \\
0 & 2 & -2 \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 \\
t \\
t^2
\end{bmatrix}
\begin{bmatrix}
\mathbf{P}_0 \\
\mathbf{P}_1 \\
\mathbf{P}_2
\end{bmatrix}
$$

#### Cubic Bézier Curve

For a cubic Bézier curve defined by four control points $\mathbf{P}_0, \mathbf{P}_1, \mathbf{P}_2, \mathbf{P}_3$, the parametric equation is:

$$
\mathbf{P}(t) = (1-t)^3 \mathbf{P}_0 + 3(1-t)^2 t \mathbf{P}_1 + 3(1-t)t^2 \mathbf{P}_2 + t^3 \mathbf{P}_3
$$

which can be rewritten in matrix form as:

$$
\mathbf{P}(t) =
\begin{bmatrix}
(1-t)^3 & 3(1-t)^2t & 3(1-t)t^2 & t^3
\end{bmatrix}
\begin{bmatrix}
\mathbf{P}_0 \\
\mathbf{P}_1 \\
\mathbf{P}_2 \\
\mathbf{P}_3
\end{bmatrix}
$$

Alternatively, using a matrix representation:

$$
\mathbf{P}(t) =
\begin{bmatrix}
1 & -3 & 3 & -1 \\
0 & 3 & -6 & 3 \\
0 & 0 & 3 & -3 \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 \\
t \\
t^2 \\
t^3
\end{bmatrix}
\begin{bmatrix}
\mathbf{P}_0 \\
\mathbf{P}_1 \\
\mathbf{P}_2 \\
\mathbf{P}_3
\end{bmatrix}
$$

This matrix representation allows efficient computation of Bézier curves using linear algebra.


# Conclusions
We can evaluate {math}`C(u)` in two main ways:

1. **Direct Bernstein basis evaluation**  
   Simple, but can be numerically unstable for high degree.

2. **De Casteljau algorithm**  
   More stable; based on repeated linear interpolation.


## 6. Engineering note: why stability matters
In engineering workflows, Bézier curves may appear indirectly:
- as part of surface patches,
- as internal representation during conversion steps,
- or during fitting.

The De Casteljau algorithm is preferred in practice because it avoids the numerical issues
of evaluating high-degree polynomials.

---

## Exercises
1. Show that {math}`\sum_{i=0}^{n} B_i^n(u) = 1`.
2. Prove endpoint interpolation.
3. Implement De Casteljau and compare its output with the Bernstein evaluation for increasing degree.

