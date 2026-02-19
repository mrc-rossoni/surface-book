---
title: Splines

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

A physical spline is a slender, flexible strip (traditionally made of wood or metal) used by draftsmen to draw smooth curves. The strip is held in place at selected points by weighted supports, often called *dogs* or *ducks*. Due to its elastic properties, it bends into a smooth and visually pleasing shape.

Mathematically, the curve formed by such a device can be modeled as a piecewise polynomial function with a prescribed degree of smoothness at the junction points. The first explicit mathematical use of the term *spline* in this context appears in {cite}`Schoenberg_1946a`, where spline functions of order {math}`k` are formally introduced. In modern terminology:

> A spline curve is a function defined piecewise by polynomial curve segments.

# Definitions

A first fundamental concept when discussing splines is the knot vector.  
Consider a strictly increasing sequence of real numbers

```{math}
u_0 < u_1 < \dots < u_L
```

Each value {math}`u_i` is called a knot and lies in the parameter space (not in the geometric space where the curve lives).
The knots partition the global parameter interval {math}`[u_0, u_L]` into smaller subintervals
```{math}
[u_0,u_1],\; [u_1,u_2],\; \dots,\; [u_{L-1},u_L],
```
called knot spans. On each knot span, the spline is defined by a polynomial segment.
The ordered list
```{math}
(u_0, u_1, \dots, u_L)
```
is called the knot vector. It determines how the parameter domain is subdivided and therefore where polynomial pieces meet. While the knot vector does not directly change the geometry of each individual polynomial segment, it controls how segments are connected and how the global parameter traverses the curve.

```{figure}../imgs/global_local_param.png
:label: fig_global_local_param
:alt: Global and local parameter relation across knot spans
:align: center

Global parameter {math}`u` across knot spans and corresponding local parameter {math}`t\in[0,1]` on each span.
```


A (parametric) spline curve {math}`s` is a {term}`continuous mapping<map>` that is polynomial on each knot span:

```{math}
s : [u_0,u_L] \to \mathbb{E}^d,
\qquad
s\big|_{[u_i,u_{i+1}]} \text{ is a polynomial curve segment.}
```

This means that:

- The curve is defined over the entire parameter interval {math}`[u_0,u_L]`.
- The image of the map lies in {math}`\mathbb{E}^d`, i.e., in a {math}`d-dimensional` Euclidean space (typically {math}`d=2` or {math}`d=3` in CAD).
- On each knot span {math}`[u_i,u_{i+1}]`, the restriction of {math}`s` is a polynomial function of the parameter {math}`u`.

In other words, a spline curve is locally polynomial: each segment between two consecutive knots is described by a polynomial curve, and the complete spline is obtained by joining these polynomial pieces together at the knots.

# Bézier Representation of a Spline

A single Bézier curve can model many shapes, but complex geometries typically require a prohibitively high degree to capture local detail. A practical solution is to join several low-degree Bézier segments end-to-end. A curve defined piecewise by polynomial segments is called a spline.

## Piecewise Bézier form

Assume each segment is a Bézier curve of degree {math}`n`. On each knot span {math}`[u_i, u_{i+1}]`, we introduce a local parameter {math}`t \in [0,1]` defined by

```{math}
t = \frac{u - u_i}{u_{i+1} - u_i}.
```

The {math}`i-th` segment is written as
```{math}
s_i(t) = \sum_{k=0}^{n} P_{i,k}\,B_k^{n}(t),
\qquad t \in [0,1],
```

where {math}`\{P_{i,k}\}` are the control points of segment {math}`i`, and {math}`B_k^n(t)` are the Bernstein polynomials of degree {math}`n`.
The global spline is obtained by concatenating these segments:

```{math}
s(u) = s_i(t), \qquad u \in [u_i, u_{i+1}].
```
The point {math}`s(u_i) = s_i(0) = s_{i-1}(1)` is called a joint (or junction point). The concatenation of all control polygons forms a piecewise Bézier polygon, providing local geometric control of the spline shape.
{numref}`fig_composite_bezier_knot_span` illustrates both the piecewise cubic Bézier geometry and the corresponding span-local Bernstein basis support in the global parameter domain. The {math}`u` value is the global parameter for the whole spline: its integer part is representing the “curve index”, its fractional part is representing the local {math}`t-value` for each individual curve. Please not that the global parameter {math}`u` belongs to the parameter domain and simply indexes points along the curve, whereas {math}`x(u)` and {math}`y(u)` are spatial coordinates, so their numerical ranges are unrelated. 

```{figure}../imgs/composite_bezier_knot_span.png
:label: fig_composite_bezier_knot_span
:alt: Composite cubic Bezier spline and piecewise Bernstein basis functions over knot spans
:align: center

Top: a spline composed of three cubic Bézier segments (blue, orange, green) joined at shared endpoints. Red markers and dashed lines show the piecewise Bézier control polygon. Bottom: the corresponding cubic Bernstein basis functions plotted in the global parameter space. Each group of four basis functions is active only on its own knot span, illustrating the piecewise polynomial structure of the spline.
```


# Parameterization

On each knot span {math}`[u_i, u_{i+1}]`, it is convenient to introduce a local parameter
{math}`t \in [0,1]`, defined by a linear rescaling of the global parameter {math}`u`:

```{math}
:label: eq_local_param
t = \frac{u - u_i}{u_{i+1} - u_i}
= \frac{u - u_i}{\Delta_i},
\qquad
\Delta_i := u_{i+1} - u_i.
```

Thus, as {math}`u` moves from {math}`u_i` to {math}`u_{i+1}`, the local parameter {math}`t` moves from 0 to 1.

Each spline segment can therefore be expressed in normalized local form:
```{math}
s(u) = s_i(t),
\qquad u \in [u_i, u_{i+1}].
```

The transformation between global and local parameter is linear:
```{math}
u = u_i + \Delta_i t.
```

Since {math}`\Delta_i` is constant on the span, the derivative of {math}`t` with respect to {math}`u` is
```{math}
:label: dt_du
\frac{dt}{du} = \frac{1}{\Delta_i}.
```

# Derivatives

Because each segment is expressed in terms of the local parameter {math}`t`,
derivatives with respect to the global parameter {math}`u`
must be computed using the chain rule:
```{math}
\frac{ds(u)}{du}
=
\frac{ds_i(t)}{dt}
\frac{dt}{du}.
```
Using Eq. {numref}`dt_du`:
```{math}
:label: eq_first_derivative_scaling
\frac{ds(u)}{du}
=
\frac{1}{\Delta_i}
```
Hence, the global derivative differs from the local derivative by a scaling factor
{math}`1/\Delta_i`.

Differentiating again with respect to {math}`u`:
```{math}
\frac{d^2 s}{du^2}
=
\frac{1}{\Delta_i}
\frac{d}{du}\left(\frac{ds_i}{dt}\right).
```

```{math}
\frac{d}{du}\left(\frac{ds_i}{dt}\right)
=
\frac{d}{dt}\left(\frac{ds_i}{dt}\right)
\frac{dt}{du}
=
\frac{d^2 s_i}{dt^2}
\frac{1}{\Delta_i}.
```

```{math}
:label: eq_second_derivative_scaling
\frac{d^2 s(u)}{du^2}
=
\frac{1}{\Delta_i^2}
\frac{d^2 s_i(t)}{dt^2}
```

The second derivative scales with the square of the knot interval.


This scaling has important geometric, numerical, and modeling implications. First of all, derivatives (in global parameter space) amplify as the knot span shrinks. As such, even if the local polynomial {math}`s_i(t)` is perfectly well-behaved, the curve in global parameter {math}`u`
can have large slope, large curvature and increased oscillatory behavior. This is why clustered knots can create regions of high curvature. Changing knot spacing affects curvature distribution even if control points are unchanged. We well dive into the details of this in the [Chapter 3.3](ch-knots-vectors).

:::{tip} FEM Analogy
In classical FEM, shape functions are local per element.
The scaling of second derivatives is {math}`h^-2` because the transformation from a reference element to a physical element of size {math}`h` involves involves a Jacobian that scales like {math}`h^1`, so its inverse is {math}`h^-1`. Through the chain rule, this inverse Jacobian is applied twice when computing second-order spatial derivatives, leading to the {math}`h^-2` factor.
Since second derivatives enter the stiffness matrix, this {math}`h^-2` scaling causes stiffness contributions to increase as elements become smaller. As a consequence small elements lead to larger stiffness entries, the system becomes increasingly ill-conditioned and mesh refinement increases the matrix condition number.

In spline-based discretizations, although basis functions overlap multiple knot spans, the derivative scaling {math}`\Delta_i^-2` is structurally identical to the finite element {math}`h^-2` scaling. Each knot span behaves as a parametric element whose size directly controls the magnitude of derivatives and, consequently, the conditioning of stiffness operators.
:::

## Derivatives of order k
Proceeding inductively, we obtain the general formula:

```{math}
:label: eq_kth_derivative_scaling
\frac{d^k s(u)}{du^k}
=
\frac{1}{\Delta_i^{\,k}}
\frac{d^k s_i(t)}{dt^k},
\qquad
u \in [u_i, u_{i+1}].
```

The {math}`k-th` derivative in global parameter space scales with the
{math}`k-th` power of the inverse knot span:
```{math}
\frac{d^k}{du^k}
\sim
\Delta_i^{-k}.
```
Thus, in general, {math}`k-th` derivatives scale like {math}`\Delta_i^{-k}`.  Further implication of this will be explained in the [Chapter 3.3](ch-knots-vectors).

## Conclusion

We have defined a spline as a piecewise polynomial curve in which each segment is itself a parametric curve (for example, a Bézier curve or another polynomial form). We now need to establish how these segments are connected, and how to control the degree of smoothness across the knots. This requirement is expressed mathematically through the concept of continuity, which will be the subject of the next chapter.