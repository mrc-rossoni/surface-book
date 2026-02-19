---
title: Knot Vectors

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

So far, we have derived continuity conditions by explicitly matching derivatives of adjacent Bézier segments. We now examine how the *knot values* (i.e., the global parameter spacing between segments) affect derivatives and continuity in a general spline.

Consider a spline composed of consecutive Bézier segments. Each segment is locally parameterized by {math}`t \in [0,1]`, but globally the spline is parameterized by a variable {math}`u`.

Let two consecutive knots be {math}`u_i` and {math}`u_{i+1}`.  
Define the knot span length

```{math}
\Delta_i = u_{i+1} - u_i.
```

If a segment is written locally as {math}`s_i(t)`, the global parameterization is obtained via the affine mapping

```{math}
t = \frac{u - u_i}{\Delta_i}.
```

---

## Effect on First Derivatives

Using the chain rule,

```{math}
\frac{ds}{du}
=
\frac{ds_i}{dt} \cdot \frac{dt}{du}
=
\frac{1}{\Delta_i} \frac{ds_i}{dt}.
```

Therefore, the derivative with respect to the global parameter {math}`u`
is scaled by the factor {math}`1/\Delta_i`.

This has an important consequence:

Even if two adjacent segments satisfy

```{math}
\left.\frac{ds_{i-1}}{dt}\right|_{t=1}
=
\left.\frac{ds_i}{dt}\right|_{t=0},
```

this does **not** automatically imply

```{math}
\left.\frac{ds}{du}\right|_{u_i^-}
=
\left.\frac{ds}{du}\right|_{u_i^+},
```

unless

```{math}
\Delta_{i-1} = \Delta_i.
```

Hence, knot spacing directly affects global {math}`C^1` continuity.

---

## Effect on Higher-Order Derivatives

Applying the chain rule repeatedly gives

```{math}
\frac{d^k s}{du^k}
=
\frac{1}{\Delta_i^k}
\frac{d^k s_i}{dt^k}.
```

Thus, the {math}`k`-th derivative scales with the factor {math}`1/\Delta_i^k`.

As a result:

- Smaller knot spans increase derivative magnitudes.
- Larger knot spans decrease derivative magnitudes.
- Continuity of order {math}`k` requires consistent scaling of adjacent spans.

---

## Consequences for Continuity

The knot spacing influences:

- derivative magnitudes,
- smoothness across joints,
- the effective parameter speed of the curve.

Even when the control polygons are arranged to enforce local derivative equality, differences in knot spans may prevent global {math}`C^k` continuity.

Therefore, continuity depends not only on control points, but also on the parameterization induced by the knot vector.

---

This observation will become fundamental when studying spline constructions where continuity is controlled directly by knot multiplicity and spacing.













-----------------------



::{prf:remark .simple}
A common pitfall: enforcing matching end tangents in the local parameter {math}`t` (i.e., imposing {math}`\left.\frac{ds_{i-1}}{dt}\right|_{t=1} = \left.\frac{ds_i}{dt}\right|_{t=0})` is not sufficient to guarantee global {math}`C^1` continuity unless {math}`\Delta_{i-1} = \Delta_i`.
The knot spacing directly affects derivative magnitudes in the global parameter {math}`u`.
:::




## Effects of uneven knot spacing

Uneven knots (non-uniform {math}`\Delta_i`) do **not** change the *geometry* of each segment, but they *do* change how the curve is traversed by the global parameter {math}`u`. This impacts:

- **Speed interpretation** (if {math}`u` represents time),
- **Derivative magnitudes** and continuity conditions,
- **Curvature plots** and “fairness” assessments,
- Numerical behavior in downstream algorithms that depend on {math}`ds/du`, {math}`d^2s/du^2`, etc.

```{figure}../imgs/spline_derivatives_even.png
:label: fig_derivatives_even
:alt: Derivatives with even knots
:align: center

Even knot spacing: local speed {math}`\|ds_i/dt\|` and global speed {math}`\|ds/du\|` differ only by a constant factor per span, and transitions are easier to keep smooth.
```

```{figure}../imgs/spline_derivatives_uneven.png
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
