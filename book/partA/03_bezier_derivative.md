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

# Bézier Curve Derivatives
Bézier curves admit clean, geometric derivative formulas. This is one of the reasons they are so useful in CAD: tangents and higher-order shape constraints are easy to compute and directly linked to the control polygon.

We start from the Bernstein form:

```{math}
C(t)=\sum_{i=0}^{n} P_i\,B_i^n(t),
\qquad t\in[0,1].
```

## First Derivative
Since the control points are constants independent of {math}`t`, differentiating the curve reduces to differentiating the Bernstein basis functions {math}`B_i^n(t)`.
The derivative of the Bernstein basis satisfies:

```{math}
:label: bernstein-derivative
\frac{d}{dt} B_i^n(t) = n\left[B_{i-1}^{n-1}(t) - B_i^{n-1}(t)\right],
\qquad i=0,\dots,n,
```
with the convention {math}`B_{-1}^{n-1}=B_{n}^{n-1}=0`.
:::{prf:proof .simple .dropdown icon=false open=false} Proof of the Derivative Formula for Bernstein Polynomials
We want to prove:

```{math}
\frac{d}{dt} B_i^n(t)=n\left[B_{i-1}^{n-1}(t)-B_i^{n-1}(t)\right].
```

By definition and the product rule,

```{math}
\frac{d}{dt} B_i^n(t)=\frac{d}{dt}\left[\binom{n}{i}t^i(1-t)^{n-i}\right]
=\binom{n}{i}\left[i\,t^{i-1}(1-t)^{n-i}-(n-i)t^i(1-t)^{n-i-1}\right].
```

We now express each term in terms of Bernstein polynomials of degree {math}`n-1`. For the first term,

```{math}
B_{i-1}^{n-1}(t)=\binom{n-1}{i-1}t^{i-1}(1-t)^{(n-1)-(i-1)}
=\binom{n-1}{i-1}t^{i-1}(1-t)^{n-i}.
```

Hence,

```{math}
t^{i-1}(1-t)^{n-i}
=\frac{\binom{n-1}{i-1}}{\binom{n}{i}}\,B_{i-1}^{n-1}(t),
```

and using

```{math}
\frac{\binom{n}{i}}{\binom{n-1}{i-1}}=\frac{n}{i},
```

we obtain:

```{math}
i\,t^{i-1}(1-t)^{n-i}=n\,B_{i-1}^{n-1}(t).
```

For the second term,

```{math}
B_i^{n-1}(t)=\binom{n-1}{i}t^i(1-t)^{(n-1)-i}
=\binom{n-1}{i}t^i(1-t)^{n-i-1},
```

so that

```{math}
(n-i)t^i(1-t)^{n-i-1}=n\,B_i^{n-1}(t).
```

Substituting back,

```{math}
\frac{d}{dt} B_i^n(t)=\binom{n}{i}\left[nB_{i-1}^{n-1}(t)-nB_i^{n-1}(t)\right]
=n\left[B_{i-1}^{n-1}(t)-B_i^{n-1}(t)\right],
```

which completes the proof.
:::

Substituting into the curve definition and collecting terms gives:

```{math}
C'(t)=n\sum_{i=0}^{n-1}\big(P_{i+1}-P_i\big)\,B_i^{n-1}(t).
```

:::{prf:proof .simple .dropdown icon=false open=false} Proof of the Bézier Curve Derivative Formula
Substituting Eq. {eq}`bernstein-derivative` into the Bézier definition:

```{math}
\frac{d}{dt}C(t)
=\sum_{i=0}^{n}P_i\,n\left[B_{i-1}^{n-1}(t)-B_i^{n-1}(t)\right].
```

Rearrange the sums:

```{math}
\frac{d}{dt}C(t)
=n\sum_{i=0}^{n}P_i\,B_{i-1}^{n-1}(t)-n\sum_{i=0}^{n}P_i\,B_i^{n-1}(t).
```

Let's shift the index with {math}`j=i-1`:

```{math}
\frac{d}{dt}C(t)=n\sum_{j=-1}^{n-1}P_{j+1}\left[B_{j}^{n-1}(t) - B_{j+1}^{n-1}(t)\right]
```
Let's split it:
```{math}
\frac{d}{dt}C(t)=n\sum_{j=-1}^{n-1}P_{j+1}B_{j}^{n-1}(t) - n\sum_{j=-1}^{n-1}P_{j+1}B_{j+1}^{n-1}(t)
```
since out-of-range Bernstein polynomials are zero, i.e. {math}`B_{-1}^{n-1}(t)=0` and {math}`B_{n}^{n-1}(t)=0`:

```{math}
\frac{d}{dt}C(t)=n\sum_{j=0}^{n-1}P_{j+1}B_{j}^{n-1}(t) - n\sum_{j=0}^{n-1}P_{j}B_{j}^{n-1}(t)
```
and nothing changes numerically since we just removed zero terms. Therefore,

```{math}
:label: eq_first_der
\frac{d}{dt}C(t)
=n\sum_{j=0}^{n-1}\left[P_{j+1}-P_j\right],B_j^{n-1}(t).
```

Defining the new control points

```{math}
P'_j=n\big(P_{j+1}-P_j\big),\qquad j=0,\dots,n-1,
```

we obtain

```{math}
\frac{d}{dt}C(t)=\sum_{j=0}^{n-1}P'_j\,B_j^{n-1}(t),
```

which is a Bézier curve of degree {math}`n-1`. This completes the proof.
:::

So the derivative is again a Bézier curve of degree {math}`n-1`. The control points of the derivative curve are computed as differences of consecutive control points, scaled by {math}`n`. In other words, {math}`P_{i+1} - P_i` is the direction vector from {math}`P_i` to {math}`P_{i+1}` and  {math}`n(P_{i+1} - P_i)` is a vector {math}`n`- times longer than the direction vector. 

As the coefficient of this new curve are not scalars but vectors, the derivative curve does not belong to {math}`E^3` but in {math}`R^3`. For this reasone, this derivative curve is usually called hodograph. 

:::{prf:definition .simple icon=false open=true}
The **hodograph** of a Bézier curve {math}`C(t)` is its derivative {math}`C'(t)`. The hodograph is itself a Bézier curve with control points:

```{math}
D_i=n\big(P_{i+1}-P_i\big),
\qquad i=0,\dots,n-1.
```
:::

The {numref}`derivative_bezier_curve` show a cubic Bézier curve, while {numref}`derivative_hodograph` shows the corresponding hodograph. Notice that the distance from the origin to each control point of the hodograph corresponds to the distance between consecutive control points of the Bézier curve, multiplied by 3 (since 3 is the degree of the curve).

```{figure}../imgs/derivative_BezierCurve.png
:label: derivative_bezier_curve
:alt: Bezier curve derivative control points
:align: center

Bezier curve derivative control points
```

```{figure}../imgs/derivative_Hodograph.png
:label: derivative_hodograph
:alt: Hodograph of the Bezier curve in {numref}`derivative_bezier_curve`
:align: center

Hodograph of the Bezier curve in {numref}`derivative_bezier_curve`
```


Once the control points are known, the control points of its derivative curve can be obtained immediately. This formula is useful for tangent vector computation and spline smoothing.


## Higher-Order Derivatives
Let's define the iterated forward difference operator:
```{math}
\Delta^k P_i=
\sum_{j=0}^{k}(-1)^{k-j}\binom{k}{j}P_{i+j}.
```
where k denotes the order of the derivative. By recursively applying the differentiation formula:

```{math}
C^{(k)}(t)=\frac{n!}{(n-k)!}
\sum_{i=0}^{n-k}
\Delta^k P_i\,B_i^{n-k}(t),
\qquad k=1,\dots,n,
```

We can notice that, for the first-order difference we obtain:
```{math}
\Delta P_i
= \sum_{j=0}^{1} (-1)^{1-j} \binom{1}{j} P_{i+j}
= P_{i+1} - P_i.
```
This expression corresponds to the factor appearing in Eq. {numref}`eq_first_der`. The factor associated with the second derivative can be obtained in the same manner:
```{math}
\Delta^2 P_i
= \sum_{j=0}^{2} (-1)^{2-j} \binom{2}{j} P_{i+j}
= P_{i+2} - 2P_{i+1} + P_i.
```
From this expression, we can observe that the second derivative is influenced by the control point and 2 subsequent points. Generalizing, we can say that the k-th derivative of a Bézier curve is influenced by k+1 consecutive control points. More precisely, the k-th forward difference {math}`\Delta^k P_i`​ involves the control points {math}`P_i,....,P_{i+k}`, highlighting the local nature of Bézier curve derivatives.

### Endpoint Derivatives
Two important cases are given by t=0 and t=1.

```{math}
\frac{d}{d^{k}t}C(0) = \frac{n!}{(n-k)!}\Delta^k P_0
```
```{math}
\frac{d}{d^{k}t}C(1) = \frac{n!}{(n-k)!}\Delta^k P_{n-k}
```
Thus, the k-th derivative of a Bézier curve at an endpoint depends only on the k+1 control points closest to and including that endpoint.

The endpoint tangents follow immediately from the first-order case:

```{math}
C'(0)=n(P_1-P_0), \qquad C'(1)=n(P_n-P_{n-1}).
```

This means that for any order {math}`k`, the Bézier curve derivative remains a Bézier curve but of reduced degree {math}`n - k`, with new computed control points. These expressions are widely used to impose tangent constraints in curve design.
