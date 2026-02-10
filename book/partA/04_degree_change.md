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

  short_title: degree change

  title: Change the Degree of a Bézier Curve

---
# Change the Degree of a Bézier Curve
Changing the degree of a Bézier curve is crucial in CAD, computer graphics, and numerical analysis. The degree affects flexibility, computational cost, and compatibility with other curves. Two key operations are used in practice. Degree elevation to increase the degree while preserving the shape and degree reduction to approximate the curve with a lower-degree representation.

# Degree Elevation
We start from the Bernstein form:

```{math}
C(t)=\sum_{i=0}^{n} P_i\,B_i^n(t),
\qquad t\in[0,1].
```

Degree elevation rewrites the same curve as a Bézier curve of degree {math}`n+1`:

```{math}
\bar{C}(t)=\sum_{i=0}^{n+1} \bar{P}_i\,B_i^{n+1}(t).
```

The new control points are:

```{math}
\bar{P}_i = \frac{i}{n+1} P_{i-1} + \left(1-\frac{i}{n+1}\right) P_i,
\qquad i=0,\dots,n+1,
```

with the convention that {math}`P_{-1}` and {math}`P_{n+1}` do not exist.

:::{prf:proof .simple .dropdown icon=false open=false} Degree Elevation Formula
we need to find a curve such that:
```{math}
\sum_{i=0}^{n} P_i B_i^n(t)=\sum_{i=0}^{n+1} \bar{P}_i B_i^{n+1}(t).
```

Starting from the Bézier definition, expanding the Bernstein definition:

```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} =\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```

We can muliply the left side of the equation by {math}`t+(1-t)=1`:

```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} (t+(1-t)) =\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```
Expanding:

```{math}
\begin{aligned}
&\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} t +\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} (1-t) =\\
&\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```
Grouping:

```{math}
\begin{aligned}
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i+1} (1-t)^{n-i} +\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i+1} =\\
&\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n-i+1}.
\end{aligned}
```
To combine terms, we want all sums expressed in the same monomials {math}`t^i(1−t)^{n+1−i}`. The second sum already has it. The first sum has {math}`t^{i+1}(1−t)^{n-i}`. By setting {math}`j=i+1`, them the first sum becomes {math}`t^{j}(1−t)^{n+1-j}`. So after shifting the index:

```{math}
\begin{aligned}
&\sum_{j=1}^{n+1} P_{j-1} \binom{n}{j-1} t^{j} (1-t)^{n-j+1} +\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i+1} =\\
&\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n-i+1}.
\end{aligned}
```

Grouping:



```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n+1-i}+\sum_{j=1}^{n+1} P_{j-1} \binom{n}{j-1} t^j (1-t)^{n+1-j}.
```

Grouping terms of equal power {math}`t^i (1-t)^{n+1-i}` and using the binomial identity
{math}`\binom{n}{i}+\binom{n}{i-1}=\binom{n+1}{i}`, we obtain:

```{math}
\bar{P}_i=\frac{i}{n+1} P_{i-1}+\left(1-\frac{i}{n+1}\right)P_i.
```
:::

So degree elevation preserves the curve geometry while increasing the number of control points.

# Degree Reduction
Degree reduction approximates a Bézier curve with a lower-degree curve. This is useful for:
- **Computational efficiency** in evaluation and rendering.
- **Data compression** by reducing control points.
- **Simplification** in CAD/CAM workflows.

Unlike degree elevation, degree reduction is generally an approximation. A common approach is to minimize the squared error:

```{math}
E = \int_0^1 \| C(t) - Q(t) \|^2\,dt,
\qquad \deg(Q)<\deg(C).
```

This leads to least-squares projections or numerical optimization of the reduced control points.

:::{prf:proof .simple .dropdown icon=false open=false} Why Degree Reduction Is an Approximation
The Bernstein polynomials of degree {math}`n` form a basis for polynomials of degree {math}`\le n`. A lower-degree basis {math}`m<n` spans a strictly smaller space. Therefore, a generic degree-{math}`n` Bézier curve cannot be represented exactly by degree {math}`m`, unless it already lies in that lower-degree space. Hence degree reduction generally introduces approximation error.
:::

## Example: Degree Reduction

```{figure}./imgs/degree_reduction.png
:label: degree_reduction_example
:alt: Degree reduction example with original and reduced Bézier curves
:align: center

Degree reduction example: original curve (blue) and reduced curve (red).
```

