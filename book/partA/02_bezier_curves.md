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


## Geometric Interpretation 

Let's start with a simple and intuitive explanation. Given two points ($P_0,P_1$) in the 2D space, what's the simplest way for connecting them you can think of? The answer is trivial: a straight line!
We can then blend between these two points, to find any point in between. The input to this function is a value ranging from 0 to 1. This value determines how far we want to go from the first point to the second. This is the most common type of blending function, known as **Linear Interpolation**.

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
                "label": f"P^{r}_{i}"
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
u_slider = alt.binding_range(min=0, max=1, step=0.01, name="u:")
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

bezier_curve = alt.Chart(curve_data).mark_line().encode(
    x=alt.X("x:Q", title="x", scale=alt.Scale(domain=x_domain)),
    y=alt.Y("y:Q", title="y", scale=alt.Scale(domain=y_domain)),
).properties(height=420)

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

### De Casteljau's Algorithm

Paul de Casteljau developed the algorithm at Citroën as a a recursive method for evaluating Bézier curves. The method provides an intuitive **geometric construction**, where the curve is defined by successive (linear) interpolations between control points. Unlike polynomial-based approaches, De Casteljau's algorithm relies solely on **linear interpolation (lerp)**, making it numerically stable and robust.

Given a set of control points $ P_0, P_1, \dots, P_n $, the Bézier curve is defined parametrically by a recursive interpolation process:

1. At each step, new intermediate points are computed by performing linear interpolation between adjacent points from the previous step.
2. The interpolation follows the equation:

   $$
   P_i^{(k)}(t) = (1 - t) P_i^{(k-1)} + t P_{i+1}^{(k-1)}
   $$

   where:
   - $ P_i^{(0)} $ are the original control points.
   - $ P_i^{(r)} $ are the intermediate points at recursion depth $ r $.
   - $ t $ is the curve parameter, ranging from 0 to 1.

3. This process continues until only one point remains, which is the evaluated point on the Bézier curve for the given $ t $.




##### Python Helpers

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, Play, jslink, HBox, VBox

import time

# Enable inline plotting
%matplotlib inline

# Linear interpolation (lerp) function
def lerp(p0, p1, t):
    """Perform linear interpolation between points p0 and p1 using parameter t."""
    return (1 - t) * np.array(p0) + t * np.array(p1)

# De Casteljau's algorithm using only lerp
def de_casteljau(points, t):
    """
    Computes the point on the Bézier curve at parameter t by recursively applying lerp.
    
    Parameters:
      points: List of control points (each a tuple or list of coordinates)
      t: Parameter value in [0, 1]
    
    Returns:
      point: The computed point on the Bézier curve at t.
      levels: A list of lists, where each inner list contains the intermediate points at that recursion level.
    """
    points = [np.array(p) for p in points]
    levels = [points]  # level 0: the original control points
    while len(points) > 1:
        points = [lerp(points[i], points[i + 1], t) for i in range(len(points) - 1)]
        levels.append(points)
    return points[0], levels
```

### Geometric Construction

The following cell creates an interactive animation of the De Casteljau algorithm using a slider to vary the parameter **t**. In addition, a **Play** widget is linked to the slider so that the animation runs automatically.

The animation shows:

- The **control polygon** (dashed line connecting the control points).
- The **intermediate levels** of linear interpolated points (each in a different color).
- The final computed point on the Bézier curve for the given t.

##### Python Helpers

```{code-cell} python
def plot_de_casteljau(t):
    """
    Plots the control polygon, intermediate levels, and the Bézier curve traced from t=0 to t.
    """
    colors = ['red', 'green', 'blue', 'orange', 'black']
    cp = np.array(control_points)
    # Compute current point and intermediate levels for t
    point, levels = de_casteljau(control_points, t)
    
    plt.figure(figsize=(15, 10))
    
    # Plot the control polygon
    #plt.plot(cp[:, 0], cp[:, 1], 'k--', label='Control Polygon')
    plt.plot(cp[:, 0], cp[:, 1], 'ko')
    
    # Plot each intermediate level
    for i, level in enumerate(levels[:-1]):  # skip the final level (single point)
        pts = np.array(level)
        plt.plot(pts[:, 0], pts[:, 1], 'o-', color=colors[i % len(colors)], label=f'Recursion Level {i+1}')
    
    # Trace the curve from t=0 to the current t
    if t > 0:
        t_values = np.linspace(0, t, 100)
        curve_points = np.array([de_casteljau(control_points, ti)[0] for ti in t_values])
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'k-', linewidth=2, label='Traced Curve')
    
    # Highlight the final computed point on the curve
    plt.plot(point[0], point[1], 'ko', markersize=10, label=f'Curve Point t={t:.2f}')
    
    plt.title("De Casteljau's Algorithm: Geometric Construction")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
```

##### Run the following code to get an animated view

```{code-cell} python
# Define control points and additional variables for the animation
control_points = [(0, 0), (1, 2), (3, 3), (4, 0)]

# Create a FloatSlider widget for t
t_slider = widgets.FloatSlider(value=0.0, min=0.0, max=1.0, step=0.01, description='t')

# Create a Play widget to animate t (0 to 100 corresponds to t from 0 to 1)
play = widgets.Play(value=0, min=0, max=100, step=1, description="Press play", interval=100)

# Link the Play widget to the slider using an observer with a simple transform.
def update_slider(change):
    t_slider.value = change['new'] / 100

play.observe(update_slider, names='value')

# Display the Play widget and slider side by side.
display(HBox([play]))

# Create the interactive plot: as the slider moves, plot_de_casteljau is updated.
interact(plot_de_casteljau, t=t_slider);
```

## 3. Complexity Analysis

The computational complexity of De Casteljau’s algorithm can be analyzed as follows:

- For **n control points**, the algorithm requires computing **n-1 interpolations** at each recursion level.
- The total number of interpolations performed follows a triangular sum:

  $$
  \sum_{r=1}^{n-1} r = \frac{(n-1) n}{2}
  $$

- Therefore, the **time complexity is $ O(n^2) $**, meaning that as the number of control points increases, the computation time grows quadratically. More precisely, the computational complexity is  **$ O(d n^2) $** where d is the number of dimensions.



This quadratic complexity is evident in the generated plot (below), where computation time increases non-linearly as control points increase.

###### Python Helpers

```{code-cell} python
def measure_de_casteljau_time(n, t=0.5, trials=10):
    """
    Measures the average computation time of the de_casteljau algorithm for n control points.
    
    Parameters:
      n: Number of control points.
      t: Parameter for the algorithm.
      trials: Number of runs to average over.
    
    Returns:
      Average computation time in seconds.
    """
    total_time = 0.0
    for _ in range(trials):
        # Generate n random 2D control points.
        control_points = [np.random.rand(2) for _ in range(n)]
        start_time = time.perf_counter()
        de_casteljau(control_points, t)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    return total_time / trials


def measure_curve_time(n, discretization=100, trials=100):
    """
    Measures the average computation time to compute a full Bézier curve 
    (evaluated at a specified number of discretization points) for a curve 
    defined by n control points.
    
    Parameters:
      n: Number of control points.
      discretization: Number of points along the curve (t values).
      trials: Number of trials for averaging.
    
    Returns:
      Average computation time (in seconds) for computing the full curve.
    """
    total_time = 0.0
    for _ in range(trials):
        control_points = [np.random.rand(2) for _ in range(n)]
        t_values = np.linspace(0, 1, discretization)
        start_time = time.perf_counter()
        for t in t_values:
            de_casteljau(control_points, t)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    return total_time / trials

def plot_computation_time(max_points=50, t=0.5, trials=100):
    """
    Plots the average computation time of De Casteljau's algorithm vs. the number of control points,
    with computation time converted to milliseconds (dividing seconds by 1000).
    
    Parameters:
      max_points: Maximum number of control points to test (starting from 2).
      t: Parameter for the algorithm.
      trials: Number of runs per test for averaging.
    """
    num_points = list(range(2, max_points + 1))
    # Collect times as a list and convert to a numpy array for element-wise operations.
    times = np.array([measure_de_casteljau_time(n, t, trials) for n in num_points])
    
    plt.figure(figsize=(10, 6))
    plt.plot(num_points, times * 1000, marker='o')  # times in milliseconds
    plt.xlabel('Number of Control Points')
    plt.ylabel('Average Computation Time (ms)')
    plt.title("De Casteljau's Algorithm Computation Time vs. Number of Control Points")
    plt.grid(True)
    plt.show()

def plot_computation_time_points(discretization_range, cps_values, trials):
    # Dictionary to store computation times (in milliseconds)
    results = {}
    
    for cps in cps_values:
        times = []
        for d in discretization_range:
            avg_time = measure_curve_time(cps, discretization=d, trials=10)
            times.append(avg_time * 1000)  # convert seconds to milliseconds
        results[cps] = times
    
    # Plot the results: x-axis is the number of discretization points; one curve per control point count
    plt.figure(figsize=(10, 6))
    for cps in cps_values:
        plt.plot(list(discretization_range), results[cps], marker='o', label=f'{cps} control points')
    plt.xlabel('Number of Discretization Points')
    plt.ylabel('Average Computation Time (milliseconds)')
    plt.title('Computation Time vs. Discretization Points (per Bézier Curve)')
    plt.grid(True)
    plt.legend()
    plt.show()
```

##### Plot the computation time
The `plot_computation_time` function takes the following input:

- max_points: Maximum number of control points to test (starting from 2).
- t: Parameter for the algorithm.
- trials: Number of runs per test for averaging.

```{code-cell} python
# Run the function to display the plot.
plot_computation_time(max_points=50, t=0.5, trials=100)
```

It also depends on the number of discretization points (the point on the curve I want to cumpute, it affect visualization performance)

The `plot_computation_time` function takes the following input:

- max_points: Maximum number of control points to test (starting from 2).
- t: Parameter for the algorithm.
- trials: Number of runs per test for averaging.

```{code-cell} python
# Define a range for the number of discretization points
discretization_range = range(10, 201, 10)  # 10, 20, ... 200

# Define the control point counts to test
cps_values = [3, 4, 5]

plot_computation_time_points(discretization_range, cps_values, trials= 100)
```

De Casteljau’s algorithm **quadratic complexity** can become a bottleneck for high-degree curves. 

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