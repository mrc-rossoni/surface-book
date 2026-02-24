---
title: Continuity at joints
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python

---

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

This condition means that  the last edge of the first control polygon and the first edge of the second control polygon must coincide as vectors. This requirement ensures that the two Bézier segments share the same tangent vector (both in terms of magnitude and direction) at the junction. This is called {math}`C^1` continuity.

And of course we can keep going Analogously for higher order derivatives.
Enforcing the second-derivatives to be equal, i.e. imposing {math}`C^2` continuity, requires equality of the second derivatives across the joint:

```{math}
:label: eq_equal_second_der
\left.\frac{d^2 s_1}{dt^2}\right|_{t=1}
=
\left.\frac{d^2 s_2}{dt^2}\right|_{t=0}
```

As, in this example, {math}`s_1` and {math}`s_2` are Bézier segments, the second derivative is:

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


(cubic-bezier-continuity-example)=
:::{prf:example} A practical example: cubic Bézier segments
:class: dropdown

Consider two adjacent cubic Bézier segments and enforce continuity progressively. Let's call {math}`P_0, \cdots, P_3` the control points of the first segment and {math}`Q_0, \cdots, Q_3` the ones of the second segment. The four figures show how the joint changes when moving from no continuity constraints to {math}`C^0`, then {math}`C^1`, and finally {math}`C^2`.

In this first configuration the endpoint of the first segment does not coincide with the start point of the second one, so no continuity condition is satisfied.

```{figure} ../imgs/continuity_cubic_bezier_0.png
:label: continuity_cubic_bezier_0
:align: center

Disconnected cubic Bézier segments
```

Imposing positional continuity means enforcing:

```{math}
P_3 = Q_0
```

```{figure} ../imgs/continuity_cubic_bezier_1.png
:label: continuity_cubic_bezier_1
:align: center

{math}`C^0` continuity
```

The two segments now meet at one point, but the tangent vectors at the joint can still differ. The curve is only position-continuous and a corner is still visible.

Now we also impose first-derivative matching, as written in Eq. {numref}`eq_equal_first_der`:

```{math}
P_3 - P_2 = Q_1 - Q_0.
```

Assuming that we want to modify only the control points of the second segment and since {math}`Q_0 = P_3` from the {math}`C^0` continuity:
```{math}
Q_1 = P_3 - P_2 + Q_0 = 2P_3 - P_2
```

```{figure} ../imgs/continuity_cubic_bezier_2.png
:label: continuity_cubic_bezier_2
:align: center

{math}`C^1` continuity
```

This makes the tangent vectors equal (same direction and magnitude), so the last edge of the first control polygon and the first edge of the second coincide as vectors. The kink disappears, but curvature may still change abruptly.

Finally, we impose second-derivative matching, i.e. Eq. {numref}`c2_condition`:

```{math}
P_3 - 2P_2 + P_1 = Q_2 - 2Q_1 + Q_0.
```
Assuming we keep changing only the second segment and since we already enforced {math}`C^0` and {math}`C^1` continuity:

```{math}
Q_2 = P_3 - 2P_2 + P_1 + 2Q_1 - Q_0 = 4P_3 - 4P_2 + P_1
```

```{figure} ../imgs/continuity_cubic_bezier_3.png
:label: continuity_cubic_bezier_3
:align: center

{math}`C^2` continuity
```

This adds curvature continuity to positional and tangent continuity. Geometrically, the bending of the last two edges of the first control polygon must match the bending of the first two edges of the second one. The joint is smooth in position, tangent, and curvature.

This cubic example shows that increasing continuity order progressively constrains the nearby control points and increases spline smoothness.
:::
Now: let's move from Bézier-specific formulas to spline theory

## Generalization of Continuity Conditions
Let's define a {math}`C^k`-continuity at a knot. Let {math}`s(u)` be a parametric curve and {math}`u_i` a knot. The curve is said to be {math}`C^k`-continuous at {math}`u_i` if:

```{math}
:label: ck_condition
\left.\frac{d^j s}{du^j}\right|_{u_i^-}
=
\left.\frac{d^j s}{du^j}\right|_{u_i^+}
\qquad \text{for all } j = 0, \dots, k.
```

In other words, the function and its derivatives up to order {math}`k`
are continuous across the knot. The order of continuity determines the smoothness of the curve at a knot. Specifically:

- {math}`C^0` continuity: the curve is position-continuous. The segments meet, but there may be a corner.
- {math}`C^1` continuity: the first derivatives match. The tangent vectors coincide, so the curve has no visible kink.
- {math}`C^2` continuity: the second derivatives match. The rate of change of the tangent is continuous, so the curvature does not exhibit jumps.
- {math}`C^k` continuity: all derivatives up to order {math}`k` match across the knot, yielding progressively smoother transitions.

It can be shown that {math}`C^k` continuity implies {math}`C^{k-1}` continuity. Since the condition expressed in Eq. {numref}`ck_condition` holds for all derivative orders up to {math}`k`, it necessarily holds for all orders up to {math}`k-1`. Therefore:
```{math}
C^k \;\Rightarrow\; C^{k-1}.
```

## Geometric vs Parametric Continuity

So far, we have discussed a type of continuity known as *parametric continuity* ({math}`C^k`), which requires equality of derivatives with respect to the curve parameter. While this condition guarantees smoothness, it is often unnecessarily restrictive when the primary concern is the geometric shape of the curve rather than its specific parameterization.

In geometric design, it is therefore more meaningful to consider *geometric continuity* ({math}`G^k`), which relaxes the requirement of derivative equality and instead enforces geometric agreement between curve segments.

According to Eq. {numref}`ck_condition`, parametric continuity requires that derivatives up to order {math}`k` match exactly at the joint. This means that both the direction and the magnitude of the derivatives must coincide across the knot.

Geometric continuity weakens this requirement by allowing a reparameterization of one segment relative to the other. Mathematically, this means that derivatives across the joint are not required to be equal, but may differ by a positive scalar factor (and, for higher orders, by additional terms induced by reparameterization). More precisely:

- {math}`G^0`: the curve segments share the same position at the joint. This is identical to {math}`C^0`;
- {math}`G^1`: the tangent directions coincide. The first derivatives may differ by a positive scalar factor {math}`\lambda > 0`
    ```{math}
    s_{u_{i+1}}'(0) = \lambda \, s_{u_i}'(1)
    ```
    Thus, the direction is the same, but the parameter speed may differ.
- {math}`G^2`: The curvature behavior matches up to reparameterization. In this case, there exist scalars {math}`\lambda > 0` and {math}`\mu \in \mathbb{R}`:
    ```{math}
    s_{u_{i+1}}''(0) = \lambda^2 s_{u_i}''(1) + \mu \, s_{u_i}'(1)
    ```
    This condition ensures geometric smoothness (consistent curvature evolution), even though the second derivatives with respect to the parameter are not necessarily equal.


{math}`C^k` continuity enforces equality of derivatives with respect to the same parameter, whereas {math}`G^k` continuity enforces equality of geometric behavior, allowing the parameterization (i.e., the "speed" along the curve) to change across the joint.

Formally, parametric continuity constrains both the curve and its parameterization. That is, it controls not only the geometric shape of the curve, but also how the curve is traversed by the parameter {math}`u`. Geometric continuity, in contrast, constrains only the geometric shape of the curve, allowing a reparameterization between adjacent segments.

Consequently,

```{math}
C^k \;\Rightarrow\; G^k,
```

but the converse is generally not true. Intuitively, as {math}`G^k` allows speeding up or slowing down at the joint while {math}`C^k` does not, {math}`G^k \;\Rightarrow\; C^k` when there is no speed change at the junction. In other words, {math}`G^k \;\Rightarrow\; C^k` iff the reparameterization does not distort derivative magnitudes.


(cubic-bezier-GvsC-example)=
:::{prf:example} G vs C: cubic Bézier segments 
:class: dropdown

Following the previous {ref}`cubic-bezier-continuity-example`, we now enforce {math}`G^1` continuity.  
In Bézier control-point form, the {math}`G^1` continuity condition becomes:

```{math}
3(Q_1 - Q_0) = \lambda\, 3(P_3 - P_2)
\quad\Longrightarrow\quad
Q_1 = Q_0 + \lambda (P_3 - P_2).
```
The result, obtained by setting {math}`\lambda=2`, is shown in {ref}`continuity_cubic_bezier_G1vsC1`.

```{figure} ../imgs/continuity_cubic_bezier_G1vsC1.png
:label: continuity_cubic_bezier_G1vsC1
:align: center

{math}`G^1` continuity
```


For {math}`G^2` continuity, with {math}`\lambda>0` and {math}`\mu\in\mathbb{R}`, we obtain:
```{math}
Q_2 = 2Q_1 - Q_0 + \frac{1}{6}\Big(\lambda^2\, s_1''(1) + \mu\, s_1'(1)\Big)
```

The result, obtained by setting {math}`\lambda=1.1` and {math}`\mu=0.1`, is shown in {ref}`continuity_cubic_bezier_G2vsC2`.

```{figure} ../imgs/continuity_cubic_bezier_G2vsC2.png
:label: continuity_cubic_bezier_G2vsC2
:align: center

{math}`G^2` continuity
```


:::


# Conclusions

Continuity at spline joints determines how smoothly adjacent curve segments connect.
From the Bézier case, we derived explicit algebraic conditions for {math}`C^0`, {math}`C^1`, and {math}`C^2` continuity and saw their geometric meaning in terms of control polygons: matching positions, matching tangent vectors, and matching bending behavior.
We then generalized these ideas to arbitrary parametric curves and distinguished between parametric continuity and geometric continuity. Since {math}`C^k` imposes stricter conditions, we have {math}`C^k \rightarrow G^k` but not conversely.

The choice between {math}`C^k` and {math}`G^k` depends on the application: geometric design often requires only geometric smoothness, whereas analysis and simulation may demand stronger parametric continuity.



