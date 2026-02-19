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
(ch-knots-vectors)=
# Knot Vectors

In the previous chapter, continuity conditions were derived by explicitly matching derivatives of adjacent Bézier segments. By equating endpoint derivatives in the local parameter {math}`t`, we obtained conditions ensuring {math}`C^0`, {math}`C^1`, or higher continuity at the joints.

However, these conditions were formulated in terms of the *local* parameter of each segment. A spline curve, on the other hand, is defined with respect to a single *global* parameter {math}`u`, subdivided by the knot vector {math}`(u_0, u_1, \dots, u_L)` where each knot span {math}`[u_i,u_{i+1}]` introduces a linear reparameterization:
```{math}
t = \frac{u - u_i}{\Delta_i},
\qquad
\Delta_i = u_{i+1} - u_i.
```
Therefore, while the geometric shape of each Bézier segment is determined by its control points, the relationship between local and global derivatives depends on the size of the knot span {math}`\Delta_i`.

This lead to a foundamental observation: 

> the continuity of a spline is not determined solely by the arrangement of control points. It also depends on the parameterization induced by the knot vector.

Therefore, understanding the role of knot vectors is essential because they do more than subdivide the parameter domain: they control the analytical structure through which the spline is expressed.

## Polynomial Degree Limitation
Assume each spline segment is a polynomial of degree {math}`n` in the local parameter {math}`t`. Differentiation reduces the polynomial degree by one at each step. Consequently,
```{math}
\frac{d^k s(u)}{du^k} = 0
\qquad
\text{for } k > n.
```

That is, a degree-{math}`n` spline segment cannot have nonzero derivatives of order higher than {math}`n`.

This statement is local: it holds on each knot span individually. Across knots, derivatives of order {math}`k \le n` may still be discontinuous if the continuity conditions are not satisfied.

## Continuity Across Knots

We now analyze how knot span sizes influence global smoothness.

On each knot span {math}`[u_i,u_{i+1}]`, the spline segment is expressed in terms of the local parameter. Since this transformation is linear, each differentiation with respect to the global parameter {math}`u` introduces a factor {math}`1/\Delta_i`. After {math}`k` differentiations, the scaling factor becomes {math}`\Delta_i^{-k}`.

Let {math}`u_i` be a joint between two adjacent spline segments. Global continuity of order {math}`k` at {math}`u_i` requires that the left and right limits of the {math}`k`-th derivative with respect to the global parameter {math}`u` coincide:

```{math}
\left.\frac{d^k s}{du^k}\right|_{u_i^-}
=
\left.\frac{d^k s}{du^k}\right|_{u_i^+}.
```
Using the derivative scaling relation, the left and right derivatives at the knot become
```{math}
\left.\frac{d^k s}{du^k}\right|_{u_i^-}
=
\frac{1}{\Delta_{i-1}^{\,k}}
\left.\frac{d^k s_{i-1}}{dt^k}\right|_{t=1},
```
```{math}
\left.\frac{d^k s}{du^k}\right|_{u_i^+}
=
\frac{1}{\Delta_i^{\,k}}
\left.\frac{d^k s_i}{dt^k}\right|_{t=0}.
```

Therefore, global {math}`C^k` continuity requires
```{math}
\frac{1}{\Delta_{i-1}^{\,k}}
\left.\frac{d^k s_{i-1}}{dt^k}\right|_{t=1}
=
\frac{1}{\Delta_i^{\,k}}
\left.\frac{d^k s_i}{dt^k}\right|_{t=0}.
```

So, even if the local Bézier segments are constructed so that
```{math}
\left.\frac{d^k s_{i-1}}{dt^k}\right|_{t=1}
=
\left.\frac{d^k s_i}{dt^k}\right|_{t=0},
```

global {math}`C^k` continuity is guaranteed only if
```{math}
\Delta_{i-1} = \Delta_i.
```

This condition reveals a crucial fact:

> Continuity depends not only on matching local derivatives, but also on consistent scaling induced by adjacent knot spans.



Thus, the knot vector plays an active role in determining smoothness.
Control points determine the geometric shape of each segment, but the knot spacing determines how derivatives are interpreted in the global parameter.

:::{prf:remark}
Matching endpoint derivatives in the local parameter {math}`t` is not sufficient to guarantee global {math}`C^k` continuity unless adjacent knot spans have equal length.
The parameterization induced by the knot vector directly influences derivative magnitudes.
:::


## Parameterization Effects: Local vs Global Speed

So far, we have analyzed how knot spacing affects derivatives and continuity from an analytical point of view. We now interpret these results geometrically.

Recalling that, on each knot span {math}`[u_i,u_{i+1}]`, the local parameter is defined by

```{math}
t = \frac{u-u_i}{\Delta_i},
\qquad
\Delta_i = u_{i+1}-u_i.
```
This relation is a linear rescaling of the parameter. The geometric image of each Bézier segment remains unchanged, but the rate at which the curve is traversed with respect to the global parameter {math}`u` depends on {math}`\Delta_i`.

### Global Speed

The global speed of the curve is
```{math}
\left\| \frac{ds}{du} \right\|
=
\frac{1}{\Delta_i}
\left\| \frac{ds_i}{dt} \right\|.
```
Thus, if {math}`\Delta_i` is large, the factor {math}`1/\Delta_i` is small, and the curve is traversed more slowly with respect to {math}`u`.If {math}`\Delta_i` is small, the factor {math}`1/\Delta_i` is large, and the curve is traversed more rapidly. In other words, the knot vector stretches or compresses the parameter axis.
The geometry of the curve does not change, but its parameterization does (this sentence is true for Bézier segment only).

### Interpretation When {math}`u` Represents Time
If the global parameter {math}`u` represents time, then {math}`\|ds/du\|` is the physical velocity along the curve. Smaller knot spans correspond to faster motion.
Larger knot spans correspond to slower motion.
Thus, uneven knot spacing induces non-uniform motion along the curve, even when the geometric segments are unchanged.


## Curvature and Fairness

Curvature is one of the most important geometric quantities used to assess the quality and smoothness of a curve.

For a planar parametric curve {math}`s(u)`, curvature is defined as

```{math}
\kappa(u)
=
\frac{\left| s'(u) \times s''(u) \right|}
     {\| s'(u) \|^3},
```

where derivatives are taken with respect to the global parameter {math}`u`.

Le'ts analyze the effect of Knot Spacing on the curvature. From the derivative scaling relations:
```{math}
\kappa(u)
=
\frac{
\left|
\frac{1}{\Delta_i} s_i'(t)
\times
\frac{1}{\Delta_i^2} s_i''(t)
\right|
}{
\left\|
\frac{1}{\Delta_i} s_i'(t)
\right\|^3
}.
```

Both numerator and denominator scale with {math}`\Delta_i^{-3}`, and therefore the scaling cancels:
```{math}
\kappa(u) = \kappa_i(t).
```

This shows an important fact:

> Geometric curvature is invariant under linear reparameterization.

Changing the knot span does not change the geometric curvature of the curve.

Although curvature magnitude is invariant, the way curvature is distributed with respect to the global parameter does change. If a knot span {math}`\Delta_i` is small, the same geometric variation is compressed into a smaller portion of the parameter domain. Curvature appears to vary more rapidly as a function of {math}`u`.
The contrary if {math}`\Delta_i` is large. Thus, while the curve itself is unchanged, its curvature plot with respect to {math}`u` may look very different.



## Effects of Uneven Knot Spacing

So far, we have analyzed knot spacing under the assumption of a uniform knot vector. In practice, however, non-uniform knot distributions are common.  
We now consider a spline defined piecewise on knot spans {math}`[u_i,u_{i+1}]` with non-uniform intervals {math}`\Delta_i`.

For any spline that is defined piecewise via a linear parameter transformation on each span, the scaling effect given by {math}`\Delta_i` holds independently of the specific polynomial representation (Bézier, B-spline, etc.), as it follows solely from the linear change of parameter on each span.

So: What Uneven Knots Affect?

Non-uniform knot spacing influences:

- Derivative magnitudes, since global derivatives scale as {math}`\Delta_i`. Smaller spans amplify higher derivatives.
- Continuity conditions, because global {math}`C^k `continuity requires consistent scaling of adjacent spans.
- Parameter speed, as the curve is traversed more rapidly on small spans and more slowly on large spans.
- Curvature plots, since although geometric curvature is invariant under linear reparameterization, its distribution with respect to the global parameter may appear distorted.
- Numerical conditioning, because higher derivatives enter many numerical operators. Since they scale with {math}`\Delta_i^{-k}`, highly non-uniform knot vectors may degrade conditioning.


### Fairness Interpretation

In design practice, a curve is often considered fair when its curvature plot exhibits few oscillations, smooth transitions, and limited variation in curvature extrema.

As far as I know, there is no unique definition of fairness in the literature. It is more a qualitative aesthetic judgment. However, some quantitatie metrics can be derived, often relying on curvature-based measures. Some common fairness functionals include:

- Curvature Variation Energy
    ```{math}
    \int \left( \frac{d\kappa}{ds} \right)^2 ds
    ```
    This functional measures the oscillation of curvature along the curve. Large values indicate rapid changes in curvature, which typically correspond to visually undesirable wiggles.

- Bending Energy (Elastic Energy)

    ```{math}
    \int \kappa^2 \, ds
    ```
    This quantity is physically meaningful: it is proportional to the elastic bending energy of a thin rod. Minimizing this energy produces curves with smoothly varying curvature and no unnecessary oscillations. As the term spline originates from the flexible strip historically used by draftsmen to draw smooth curves, classical spline curves arise precisely from this variational principle. 
    A thin elastic strip naturally minimizes bending energy. Thus, a fair curve can be interpreted as one that behaves like a physically relaxed elastic strip.
- Higher-Order Smoothness Measures

    ```{math}
    \int \| s''(u) \|^2 \, du
    ```
    Such functionals are widely used in smoothing splines and finite element contexts.
    They penalize large second derivatives and therefore promote smooth curvature behavior.

It is still true that fairness is a geometric property independent of parameterization, whereas curvature plots depend on parameterization. If the geometric curve is kept fixed and only its parameterization is modified (for example through linear reparameterization of knot spans), then uneven knot spacing does not alter the geometric fairness of the curve. However, it can distort curvature plots when visualized against the global parameter. This may lead to misleading assessments if parameterization effects are not taken into account.

Understanding this distinctions is essential when analyzing spline quality or when comparing curves generated under different parameterizations. In spline constructions where the knot vector also influences the basis functions (e.g., B-splines), changing knot values may modify the geometry itself, and therefore also the fairness of the curve.





## Conclusion

In this chapter, we have seen that the knot vector does far more than simply partition the parameter domain. It determines how local polynomial segments are interpreted in the global parameter and therefore plays a central role in the analytical structure of a spline.

Importantly, in the piecewise Bézier construction considered here, changing knot spacing does not alter the geometric image of the curve. Instead, it modifies how the curve is traversed and how its derivatives are measured. This distinction between geometry and parameterization is fundamental. A spline curve is not defined solely by its control points; it is defined by the interaction between control points and knot vector.

Understanding this interaction prepares us to study more general spline constructions, where knot multiplicity and non-uniform spacing influence not only derivative scaling, but also the structure of the basis functions themselves.