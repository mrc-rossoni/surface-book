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

# Continuity at joints

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
