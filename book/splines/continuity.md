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
Continuity describes the smoothness conditions imposed at the joints between adjacent spline segments. It determines how derivatives of successive pieces relate to each other at the knots, and therefore how smoothly the overall curve behaves across those connections.

Let us derive the condition first on two adjacent Bézier segments.
Consider segments {math}`s_1` and {math}`s_2` (both degree {math}`n`), each expressed with local parameter {math}`t\in[0,1]`:
```{math}
s_1(t)=\sum_{k=0}^{n} B_k^{n}(t)\,P_k,
\qquad
s_2(t)=\sum_{k=0}^{n} B_k^{n}(t)\,Q_k.
```
Globally, these correspond to two consecutive spans, and the first basic requirement is that the two segments meet at the joint:
```{math}
s_1(1)=s_2(0)\;\Longrightarrow\;P_n=Q_0.
```
This is {math}`C^0` continuity.

This condition guarantees that the two segments meet, but it does not impose any restriction on *how* they meet.
To control smoothness, we impose derivative constraints at the joint. For local first-derivative matching:
```{math}
:label: eq_equal_first_der
\left.\frac{ds_1}{dt}\right|_{t=1}
=
\left.\frac{ds_2}{dt}\right|_{t=0}
```

For a degree-{math}`n` Bézier segment with control points {math}`R_k`, the first derivative is:
```{math}
\frac{d}{dt}\!\left(\sum_{k=0}^{n} B_k^{n}(t)\,R_k\right)
=
\sum_{k=0}^{n-1} n\bigl(R_{k+1}-R_k\bigr)\,B_k^{n-1}(t).
```
By definition, at the endpoints all Bernstein polynomials vanish except  
{math}`B_{0}^{n-1}(0)=1` and {math}`B_{n-1}^{n-1}(1)=1`.  
Therefore, in the derivative expressions, the only non-zero terms in the summations are those corresponding to {math}`i=n-1` for {math}`s_1` at {math}`t=1`, and {math}`i=0` for {math}`s_2` at {math}`t=0`.
Hence,
```{math}
\left.\frac{ds_1}{dt}\right|_{t=1} =
n\bigl(P_n-P_{n-1}\bigr)
```
```{math}
\left.\frac{ds_2}{dt}\right|_{t=0} 
=
n\bigl(Q_1-Q_0\bigr).
```
Therefore, Eq. {numref}`eq_equal_first_der` becomes:
```{math}
\bigl(P_n-P_{n-1}\bigr)
=
\bigl(Q_1-Q_0\bigr).
```

This condition means that  the last edge of the first control polygon and the first edge of the second control polygon must coincide as vectors. This requirement ensures that the two Bézier segments share the same tangent vector (bith in term of magnitude and direction) at the junction. This is called {math}`C^1` continuity.

And of course we can keep going Analogously for higher order derivatives.
Enforcing the second-derivatives to be equal, i.e. imposing {math}`C^2` continuity, requires equality of the second derivatives across the joint:

```{math}
:label: eq_equal_second_der
\left.\frac{ds^2_1}{dt^2}\right|_{t=1}
=
\left.\frac{ds^2_2}{dt^2}\right|_{t=0}
```

As, in this example, {math}`s_1` and {math}`s_2` are Bézioer segments, the second derivative is:

```{math}
:label: eq_equal_second_der_sum
\frac{d^2}{dt^2}\!\left(\sum_{k=0}^{n} B_k^{n}(t)\,R_k\right)
=
\sum_{k=0}^{n-2} n(n-1)\bigl(R_{k+2}-2R_{k+1}+R_k\bigr)\,B_k^{n-2}(t).
```

As for the first derivative, at the endpoints, all Bernstein polynomials vanish except {math}`B_{0}^{n-2}(0)=1` and {math}`B_{n-2}^{n-2}(1)=1`. So only one term of Eq. {numref}`eq_equal_second_der_sum` survives at each endpoint. We get:
```{math}
\left.\frac{d^2 s_1}{dt^2}\right|_{t=1}
=
n(n-1)\bigl(P_n-2P_{n-1}+P_{n-2}\bigr)
```
```{math}
\left.\frac{d^2 s_2}{dt^2}\right|_{t=0}
=
n(n-1)\bigl(Q_2-2Q_1+Q_0\bigr)
```

```{math}
:label: c2_condition
\bigl(P_n-2P_{n-1}+P_{n-2}\bigr)
=
\bigl(Q_2-2Q_1+Q_0\bigr).
```

Enforcing this condition not only makes the tangent vectors match (as in 
{math}`C^1`-continuity), but also ensures that the rate of change of the tangent is the same on both sides of the joint. Thus, the curve does not merely appear smooth; its bending is smooth as well.

Each side of Eq. {numref}`c2_condition` measures how much the last two edges of a control polygon change direction. Enforcing their equality means that the way the last two edges of the first control polygon bend must exactly match the way the first two edges of the second control polygon bend.

As a result, {math}`C^2`-continuity imposes an additional constraint relating the four control points surrounding the joint (two before and two after the knot). Once the previous continuity conditions are enforced, it effectively determines the position of the next control point.

Now: let's move from Bézier-specific formulas to spline theory

## Generalization of Continuity Conditions
Let's defina a {math}`C^k`-continuity at a knot. Let {math}`s(u)` be a parametric curve and {math}`u_i` a knot. The curve is said to be {math}`C^k`-continuous at {math}`u_i` if:

```{math}
:label: ck_condition
\left.\frac{d^j s}{du^j}\right|_{u_i^-}
=
\left.\frac{d^j s}{du^j}\right|_{u_i^+}
\qquad \text{for all } j = 0, \dots, k.
```

In other words, the function and its derivatives up to order {math}`k`
are continuous across the knot.The order of continuity determines the smoothness of the curve at a knot. Specifically:

- {math}`C^0` continuity: the curve is position-continuous. The segments meet, but there may be a corner.
- {math}`C^1` continuity: the first derivatives match. The tangent vectors coincide, so the curve has no visible kink.
- {math}`C^2` continuity: the second derivatives match. The rate of change of the tangent is continuous, so the curvature does not exhibit jumps.
- {math}`C^k` continuity: all derivatives up to order {math}`k` match across the knot, yielding progressively smoother transitions.

It can be shown that {math}`C^k` continuity implies {math}`C^{k-1}` continuity. Since the condition exapressed in Eq. {numref}`ck_condition` holds for all derivative orders up to {math}`k`, it necessarily holds for all orders up to {math}`k-1`. Therefore:
```{math}
C^k \;\Rightarrow\; C^{k-1}.
```


## Geometric vs Parametric Continuity

So far, we have discussed a type of continuity known as *parametric continuity* ({math}`C^k`), which requires equality of derivatives with respect to the parameter. However, enforcing this condition is often unnecessarily restrictive, especially when the primary concern is the geometric shape of the curve. In geometric design, it is therefore often more meaningful to relax this requirement and instead consider *geometric continuity* ({math}`G^k`).

According to Eq. {numref}`ck_condition`, parametric continuity requires that both the direction and the magnitude of the derivatives match across the joint. Geometric continuity relaxes this requirement: instead of enforcing equality of derivatives, it only enforces geometric agreement of the curve segments. Specifically:

- {math}`G^0`: same position;
- {math}`G^1`: tangent directions coincide (vectors may differ by a positive scalar factor);
- {math}`G^2`: curvature behavior matches up to reparameterization. 

For example, {math}`G^1` continuity requires

```{math}
\left.\frac{ds}{du}\right|_{u_i^+}
=
\lambda \,
\left.\frac{ds}{du}\right|_{u_i^-}
\qquad \text{with } \lambda > 0.
```

Thus, the two segments share the same tangent direction, but not necessarily the same parameter speed.

Formally, parametric continuity ({math}`C^k`) constrains the curve and its parameterization, i.e. not only the shape of the curve but even how the curve is traversed by the parameter {math}`u`. Geometric continuity ({math}`G^k`) constrains only the shape of the curve, allowing reparameterization.

Consequently,

```{math}
C^k \;\Rightarrow\; G^k,
```

but the converse is generally not true. Intutively, as {math}`G^k` allows speeding up or slowing down at the joint while {math}`C^k` does not, {math}`G^k \;\Rightarrow\; C^k` when there is no speed change at the junction. In other words, {math}`G^k \;\Rightarrow\; C^k` iff the reparameterization does not distort derivative magnitudes.









