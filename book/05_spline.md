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

  short_title: splines

  title: spline curves

---

# Splines
A physical spline is a slender, flexible strip (traditionally made of wood or metal) used by draftsmen to draw smooth curves. The strip is held in place at selected points by weighted supports, often called *dogs*. Due to its elastic properties, it bends into a smooth and visually pleasing shape.

Mathematically, the curve formed by such a device can be modeled as a piecewise polynomial function with a prescribed degree of smoothness at the junction points. The first explicit mathematical use of the term *spline* in this context appears in {cite}`Schoenberg_1946a`, where spline functions of order {math}`k` are formally introduced. In modern terminology:
> A spline curve is a function that is defined piecewise by polynomials curve 

As such, a single Bézier is not a spline.







Given knots

```{math}
u_0 < u_1 < \cdots < u_L,
```

a spline curve of degree {math}`n` in {math}`\mathbb{E}^d` is a function {math}`s:[u_0,u_L]\to\mathbb{E}^d` such that each restriction {math}`s|_{[u_i,u_{i+1}]}` is polynomial of degree at most {math}`n`.
At interior knots {math}`u_i`, one usually enforces continuity constraints ({math}`C^r` or {math}`G^r`) so adjacent pieces join smoothly.

This piecewise structure gives local control: moving data on one segment primarily affects nearby geometry, while continuity conditions preserve global smoothness.

# Spline Curves in Bézier Form

A single Bézier curve can model many shapes, but **complex curves typically require a prohibitively high degree** to capture local detail.  
In CAD and geometric modeling, the standard solution is to **join several low-degree Bézier segments** end-to-end. A curve defined piecewise by polynomial segments is called a **spline**.

## Definitions, terminology, and conventions

Let

```{math}
u_0 < u_1 < \dots < u_L
```

be a strictly increasing sequence of real numbers. Each value {math}`u_i` is called a **knot** (in parameter space). The ordered list is the **knot vector**.

A (parametric) **spline curve** {math}`s` is a continuous map that is *polynomial on each knot span*:

```{math}
s : [u_0,u_L] \to \mathbb{E}^d,
\qquad
s\big|_{[u_i,u_{i+1}]} \text{ is a polynomial curve segment.}
```

For Bézier-form splines, we represent each segment on a **local parameter** {math}`t\in[0,1]` defined by

```{math}
:label: eq_local_param
t = \frac{u-u_i}{u_{i+1}-u_i} = \frac{u-u_i}{\Delta_i},
\qquad
\Delta_i := u_{i+1}-u_i.
```

We denote the {math}`i`-th Bézier segment by {math}`s_i`, so that for {math}`u\in[u_i,u_{i+1}]`:

```{math}
s(u) = s_i(t).
```

The point {math}`s(u_i)=s_i(0)=s_{i-1}(1)` is the **joint** (or **junction point**) in Euclidean space.

## Piecewise Bézier representation

Assume each segment is a Bézier curve of degree {math}`n`:

```{math}
:label: eq_piecewise_bezier
s_i(t)=\sum_{k=0}^{n} P_{i,k}\,B_k^{n}(t),
\qquad t\in[0,1],
```

where {math}`\{P_{i,k}\}` are the control points of segment {math}`i` and {math}`B_k^n` are the Bernstein polynomials.

```{figure}./imgs/spline_composite_even.png
:label: fig_composite_bezier
:alt: Composite Bézier curve and Bernstein basis functions per segment
:align: center

A composite (piecewise) Bézier curve. The bottom plot shows how each segment has its *own* Bernstein basis on its local parameter; conceptually you can “stitch” segments along the global curve.
```

:::{prf:remark .simple}
A **piecewise Bézier polygon** is obtained by concatenating the control polygons of all segments. It provides an intuitive, local-control handle on the spline shape.
:::

## Global vs local derivatives

Because each segment is parameterized by a **local** variable {math}`t`, derivatives with respect to the **global** parameter {math}`u` must use the chain rule.

```{math}
\frac{d s(u)}{d u} = \frac{d s_i(t)}{d t}\,\frac{d t}{d u},
\qquad
\frac{d t}{d u} = \frac{1}{\Delta_i}.
```

Hence:

```{math}
:label: eq_first_derivative_scaling
\boxed{
\frac{d s(u)}{d u} = \frac{1}{\Delta_i}\,\frac{d s_i(t)}{d t}
}
```

Similarly, differentiating again:

```{math}
:label: eq_second_derivative_scaling
\boxed{
\frac{d^2 s(u)}{d u^2} = \frac{1}{\Delta_i^2}\,\frac{d^2 s_i(t)}{d t^2}
}
```

:::{prf:proof .simple .dropdown icon=false} Second-derivative scaling
On a fixed span {math}`[u_i,u_{i+1}]`, {math}`\Delta_i` is constant and {math}`t=(u-u_i)/\Delta_i`.  
From Eq. {numref}`eq_first_derivative_scaling`:

```{math}
\frac{ds}{du} = \frac{1}{\Delta_i}\frac{ds_i}{dt}.
```

Differentiate again w.r.t. {math}`u`:

```{math}
\frac{d^2 s}{du^2}
=\frac{1}{\Delta_i}\frac{d}{du}\left(\frac{ds_i}{dt}\right)
=\frac{1}{\Delta_i}\frac{d}{dt}\left(\frac{ds_i}{dt}\right)\frac{dt}{du}
=\frac{1}{\Delta_i}\frac{d^2 s_i}{dt^2}\cdot\frac{1}{\Delta_i}
=\frac{1}{\Delta_i^2}\frac{d^2 s_i}{dt^2}.
```
:::

## Continuity at joints

Let the joint between segments {math}`s_{i-1}` and {math}`s_i` correspond to {math}`u=u_i`, i.e. to {math}`t=1` on the left segment and {math}`t=0` on the right segment.

### Positional continuity (C0)

```{math}
:label: eq_C0
s_{i-1}(1)=s_i(0)
\quad\Longleftrightarrow\quad
P_{i-1,n}=P_{i,0}.
```

### Tangent continuity (C1) in global parameter

A true {math}`C^1` spline requires

```{math}
\left.\frac{ds}{du}\right|_{u_i^-} = \left.\frac{ds}{du}\right|_{u_i^+}.
```

Using Eq. {numref}`eq_first_derivative_scaling`:

```{math}
:label: eq_C1_global
\frac{1}{\Delta_{i-1}}\,\left.\frac{ds_{i-1}}{dt}\right|_{t=1}
=
\frac{1}{\Delta_{i}}\,\left.\frac{ds_{i}}{dt}\right|_{t=0}.
```

Since for a degree-{math}`n` Bézier curve:

```{math}
\left.\frac{ds_i}{dt}\right|_{t=0}=n(P_{i,1}-P_{i,0}),
\qquad
\left.\frac{ds_i}{dt}\right|_{t=1}=n(P_{i,n}-P_{i,n-1}),
```

Eq. {numref}`eq_C1_global` becomes

```{math}
:label: eq_C1_ctrl
\boxed{
\frac{P_{i-1,n}-P_{i-1,n-1}}{\Delta_{i-1}}
=
\frac{P_{i,1}-P_{i,0}}{\Delta_{i}}
}
```

### Curvature continuity (C2) in global parameter

Analogously, {math}`C^2` requires

```{math}
\left.\frac{d^2s}{du^2}\right|_{u_i^-} = \left.\frac{d^2s}{du^2}\right|_{u_i^+}.
```

Using Eq. {numref}`eq_second_derivative_scaling`, the local second derivatives must satisfy a **square** scaling with the knot intervals:

```{math}
:label: eq_C2_global
\frac{1}{\Delta_{i-1}^2}\,\left.\frac{d^2s_{i-1}}{dt^2}\right|_{t=1}
=
\frac{1}{\Delta_{i}^2}\,\left.\frac{d^2s_{i}}{dt^2}\right|_{t=0}.
```

:::{prf:remark .simple}
A common pitfall: enforcing “matching end tangents” in local {math}`t` (i.e., {math}`ds_{i-1}/dt(1)=ds_i/dt(0)`) is **not** enough for {math}`C^1` unless {math}`\Delta_{i-1}=\Delta_i`. The knot spacing matters.
:::

## Effects of uneven knot spacing

Uneven knots (non-uniform {math}`\Delta_i`) do **not** change the *geometry* of each segment, but they *do* change how the curve is traversed by the global parameter {math}`u`. This impacts:

- **Speed interpretation** (if {math}`u` represents time),
- **Derivative magnitudes** and continuity conditions,
- **Curvature plots** and “fairness” assessments,
- Numerical behavior in downstream algorithms that depend on {math}`ds/du`, {math}`d^2s/du^2`, etc.

```{figure}./imgs/spline_derivatives_even.png
:label: fig_derivatives_even
:alt: Derivatives with even knots
:align: center

Even knot spacing: local speed {math}`\|ds_i/dt\|` and global speed {math}`\|ds/du\|` differ only by a constant factor per span, and transitions are easier to keep smooth.
```

```{figure}./imgs/spline_derivatives_uneven.png
:label: fig_derivatives_uneven
:alt: Derivatives with uneven knots
:align: center

Uneven knot spacing: the same local derivatives produce different global derivatives due to the scaling {math}`1/\Delta_i`. If control points are not adjusted accordingly, {math}`C^1` / {math}`C^2` in global parameter can be lost.
```

### Parameterization and “local vs global speed”
From Eq. {numref}`eq_first_derivative_scaling`, a larger {math}`\Delta_i` *reduces* {math}`\|ds/du\|` on that span, i.e. the curve is traversed **more slowly** in global parameter. A smaller {math}`\Delta_i` increases {math}`\|ds/du\|`, effectively **speeding up** traversal.

### Curvature and fairness

Curvature (for a planar curve) is commonly written as

```{math}
\kappa(u) = \frac{|s'(u)\times s''(u)|}{\|s'(u)\|^3},
```

where derivatives are w.r.t. the **global** parameter. Because both {math}`s'` and {math}`s''` scale with {math}`\Delta_i` (Eqs. {numref}`eq_first_derivative_scaling`–{numref}`eq_second_derivative_scaling`), the curvature plot over {math}`u` can change substantially when knots are made uneven—even if the geometry of each Bézier segment is unchanged.

A practical “designer-friendly” interpretation (intentionally loose) is that a curve tends to look **fair** when its curvature plot has relatively few oscillations (few monotone pieces).

## Python example

:::{prf:example .simple .dropdown icon=false} Generate the figures in this lesson
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def bernstein(n, k, t):
    return comb(n, k) * (t**k) * ((1-t)**(n-k))

def bezier_curve(ctrl, npts=200):
    n = len(ctrl) - 1
    t = np.linspace(0, 1, npts)
    c = np.zeros((npts, 2))
    for i in range(n+1):
        c += np.outer(bernstein(n, i, t), ctrl[i])
    return c, t

def bezier_derivative_ctrl(ctrl):
    n = len(ctrl) - 1
    return n*(ctrl[1:] - ctrl[:-1])

def plot_derivatives(control_points, knots):
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    for i, pts in enumerate(control_points):
        c, t = bezier_curve(pts)

        dctrl = bezier_derivative_ctrl(pts)
        d_dt, _ = bezier_curve(dctrl)

        delta = knots[i+1] - knots[i]
        u = knots[i] + t*delta
        d_du = d_dt / delta

        axs[0].plot(c[:,0], c[:,1], lw=2, label=f"Seg {i+1}")
        axs[0].plot(pts[:,0], pts[:,1], "r--", alpha=0.5)

        axs[1].plot(u, np.linalg.norm(d_du, axis=1), lw=2, label=r"$\|ds/du\|$ seg "+str(i+1))
        axs[1].plot(u, np.linalg.norm(d_dt, axis=1), "--", lw=2, label=r"$\|ds_i/dt\|$ seg "+str(i+1))
        axs[1].axvline(knots[i+1], color="k", ls="--", alpha=0.6)

    axs[0].grid(True); axs[0].legend()
    axs[1].grid(True); axs[1].legend()
    plt.show()

control_points = [
    np.array([[0,0],[1,2],[2,2],[3,0]]),
    np.array([[3,0],[4,-2],[5,-2],[8,0]]),
    np.array([[8,0],[11,2],[12,2],[13,0]])
]
knots = [0, 1, 2, 4]
plot_derivatives(control_points, knots)
```
:::


