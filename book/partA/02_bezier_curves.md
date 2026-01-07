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


The point {math}`P(t)` is the result of the recursion for a given value of {math}`t`, and it lies on the so called **Bézier curve**, defined by the control points (`P_0, P_1, \dots, P_n`).
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

De Casteljau’s algorithm **quadratic complexity** can become a bottleneck for high-degree curves. 

:::


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mrc-rossoni/surface-book/blob/main/book/partA/02_lab_bezier.ipynb)

## The Bernstein Form of a Bézier Curve

De Casteljau’s algorithm is an elegant method for evaluating Bézier curves, relying **exclusively on linear interpolation** for numerical stability. However, Bézier approached curves from a different perspective, highlighting the need for an *explicit* representation of the curve. In other words, expressing a Bézier curve through a non-recursive mathematical formula—rather than an iterative algorithm—is essential. This explicit representation not only significantly facilitates further theoretical developments but also enables more efficient implementations.

Specifically, any point on a curve segment must be given by a parametric function of the following form:

$$
    P(t) = \sum_{i=0}^{n} P_i f_{i}(t)
$$

Where $P_{i}$ are the vectors of the $n+1$ vertices of the control polygon.

Then, Bézier set forth the properties that the $f_{i}(t)$ basis function must have and look for specific functions that meet these requirements. The requirements were:

- The functions must interpolate the first ($P_0$) and the last ($P_n$) vertex points.
- The $r-th$ derivative at an endpoint must be determined by its $r$ neighboring vertices. Thus, the tangent (first derivative) at $P_0$ must be given by $P_1 - P_0$ and the tangent at $P_n$ by $P_n - P_{n-1}$. This give the user the control of the tangent on the curve at each end. The second derivative at $P_0$ must bedetermined by $P_0, P_1$ and $P_2$, and so on.
- The functions $f_{i}(t)$ must be symmetric w.r.t. $t$ and $t-1$. This means that we can revers the sequence of the vertex points defining the curve without changing the shape of the curve.

Bézier chose a family of functions called *Bernstein Polynomials*. Bernstein polynomials are a family of polynomials that play an important role in approximation theory and computational mathematics. They are particularly famous for their use in Bézier curves in computer graphics and geometric modeling.

$$
  B_{n,i}(t) = \binom{n}{i} t^n (1-t)^{n-i}
$$

The Binomial coefficient is defined as follow:

$$
  \binom{n}{i} = \frac{n!}{i!(n-i)!}
$$




## 2. Definition
A Bézier curve of degree \(n\) is defined by \(n+1\) control points \(P_0, ..., P_n\) and is written as:

\[
C(u) = \sum_{i=0}^{n} B_i^n(u) P_i, \qquad u \in [0,1]
\]

where \(B_i^n(u)\) are the **Bernstein polynomials**:

\[
B_i^n(u) = \binom{n}{i} u^i (1-u)^{n-i}
\]

---

## 3. Key properties

### 3.1 Endpoint interpolation
\[
C(0) = P_0,\qquad C(1) = P_n
\]

### 3.2 Convex hull property
For \(u \in [0,1]\), the curve lies inside the convex hull of its control points.
This is extremely important in engineering: it gives a geometric bound
and makes control point editing predictable.

### 3.3 Variation diminishing property
The curve does not oscillate more than its control polygon.
This makes Bézier curves stable and well-behaved for design.

---

## 4. Evaluating a Bézier curve
We can evaluate \(C(u)\) in two main ways:

1. **Direct Bernstein basis evaluation**  
   Simple, but can be numerically unstable for high degree.

2. **De Casteljau algorithm**  
   More stable; based on repeated linear interpolation.

---

## 5. De Casteljau algorithm (derivation)
Given control points \(P_0, ..., P_n\), define recursively:

\[
P_i^{(0)} = P_i
\]

\[
P_i^{(r)} = (1-u)P_i^{(r-1)} + uP_{i+1}^{(r-1)}
\]

for \(r = 1, ..., n\).

The final point on the curve is:

\[
C(u) = P_0^{(n)}
\]

---

## 6. Engineering note: why stability matters
In engineering workflows, Bézier curves may appear indirectly:
- as part of surface patches,
- as internal representation during conversion steps,
- or during fitting.

The De Casteljau algorithm is preferred in practice because it avoids the numerical issues
of evaluating high-degree polynomials.

---

## Exercises
1. Show that \(\sum_{i=0}^{n} B_i^n(u) = 1\).
2. Prove endpoint interpolation.
3. Implement De Casteljau and compare its output with the Bernstein evaluation for increasing degree.