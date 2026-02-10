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

# Change the Degree of a Bézier Curve

:::{attention} TODO
- prepare python example for degree reduction
- check example 1@
:::

Changing the degree of a Bézier curve is crucial in CAD, computer graphics, and numerical analysis. The degree affects flexibility, computational cost, and compatibility with other curves. Two key operations are used in practice:
- **Degree elevation** to increase the degree while preserving the shape.
- **Degree reduction** to approximate the curve with a lower-degree representation.

## Degree Elevation
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
:label: eq_elevation
\bar{P}_i = \frac{i}{n+1} P_{i-1} + \left(1-\frac{i}{n+1}\right) P_i,
\qquad i=0,\dots,n+1,
```


:::{prf:proof .simple .dropdown icon=false open=false} Degree Elevation Formula

We want to find a curve such that:
```{math}
\sum_{i=0}^{n} P_i B_i^n(t)=\sum_{i=0}^{n+1} \bar{P}_i B_i^{n+1}(t).
```

Starting from the Bézier definition and expanding the Bernstein basis:
```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```

We multiply the left-hand side by {math}`t+(1-t)=1`:
```{math}
\sum_{i=0}^{n} P_i \binom{n}{i} t^i (1-t)^{n-i} (t+(1-t))
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
```

Expanding:
```{math}
\begin{aligned}
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i+1} (1-t)^{n-i}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

To express all terms in the same monomials {math}`t^i(1-t)^{n+1-i}`, we shift the index in the first sum by setting {math}`j=i+1`:
```{math}
\begin{aligned}
&\sum_{j=1}^{n+1} P_{j-1} \binom{n}{j-1} t^{j} (1-t)^{n+1-j}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Renaming the index {math}`j` back to {math}`i` in the first sum:
```{math}
\begin{aligned}
&\sum_{i=1}^{n+1} P_{i-1} \binom{n}{i-1} t^{i} (1-t)^{n+1-i}
+\\
&\sum_{i=0}^{n} P_i \binom{n}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Using the binomial identities:
```{math}
\begin{aligned}
\binom{n}{i} &= \frac{n+1-i}{n+1}\binom{n+1}{i}, \quad 0 \le i \le n \\
\binom{n}{i-1} &= \frac{i}{n+1}\binom{n+1}{i}, \quad 1 \le i \le n+1
\end{aligned}
```

we obtain:
```{math}
\begin{aligned}
&\sum_{i=1}^{n+1} P_{i-1} \frac{i}{n+1}\binom{n+1}{i} t^{i} (1-t)^{n+1-i}
+\\
&\sum_{i=0}^{n} P_i \frac{n+1-i}{n+1} \binom{n+1}{i} t^{i} (1-t)^{n+1-i}
=
\sum_{i=0}^{n+1} \bar{P}_i \binom{n+1}{i} t^i (1-t)^{n+1-i}.
\end{aligned}
```

Thus:
```{math}
\sum_{i=1}^{n+1} \frac{i}{n+1} P_{i-1} B_i^{n+1}(t)
+
\sum_{i=0}^{n} \frac{n+1-i}{n+1} P_i B_i^{n+1}(t)
=
\sum_{i=0}^{n+1} \bar{P}_i B_i^{n+1}(t).
```

Since {math}`\{B_i^{n+1}(t)\}_{i=0}^{n+1}` is a basis, the representation is unique, hence the coefficients {math}`B_i^{n+1}(t)` must match. So the degree-elevated control points are:
```{math}
\bar{P}_0 = P_0, \quad i = 0
```

```{math}
\bar{P}_i = \frac{i}{n+1} P_{i-1}
+
\left(1 - \frac{i}{n+1}\right) P_i,
\quad 1 \le i \le n
```

```{math}
\bar{P}_{n+1} = P_n, , \quad i = n+1
```

:::

Equation {numref}`eq_elevation` shows that each new control point is obtained as a convex linear combination of two consecutive control points of the original control polygon, with weights depending on the parameter {math}`\frac{i}{n+1}`, the degree-elevated control polygon lies entirely within the convex hull of the original one and defines exactly the same Bézier curve. Degree elevation therefore preserves the curve geometry while increasing the number of control points, providing additional degrees of freedom for subsequent shape manipulation without altering the underlying geometry.

#### Why degree elevation?
Degree elevation has important applications:
- When combining or blending curves and surfaces of different degrees, degree elevation allows them to be brought to a common degree, enabling exact algebraic operations such as addition, subtraction, or interpolation.
- In surface design, several algorithms that generate surfaces from curve inputs require all curves to have the same degree. A notable example is the construction of Coons surfaces implemented as tensor-product Bézier or NURBS patches, where boundary curves must be expressed with a common polynomial degree. Degree elevation allows this requirement to be satisfied without altering the curve geometry.
- Outside traditional CAD, degree elevation (often referred to as p-refinement) is a core operation in isogeometric analysis (See {cite}`Hughes_2005`), where increasing the polynomial degree improves approximation accuracy without changing the geometry.
- In robotics and control, trajectories are often represented using Bézier. Degree elevation is used to bring trajectories of different polynomial degrees to a common representation, enabling smooth trajectory blending, time reparameterization, and the enforcement of continuity and dynamic constraints (e.g. velocity or acceleration continuity) without altering the geometric path. See, for example, {cite}`Durakl__2022`.
 - ...

## Degree Reduction
Degree elevation can be viewed as a process that introduces redundancy, in the sense that the same curve geometry is represented using more control points, and therefore more parameters, than are strictly necessary. Although the representation becomes redundant, degree elevation enlarges the space of admissible control point configurations that represent the same geometry, which can be advantageous in optimization, approximation, and constraint-based formulations. Despite its advantages, degree elevation also introduces drawbacks. The increased polynomial degree and number of control points lead to higher computational and memory costs and may negatively affect numerical conditioning. Moreover, higher-degree representations tend to reduce local control, making shape manipulation less intuitive and increasing the complexity of subsequent geometric algorithms.

Degree reduction is the inverse process and is of interest for several reasons. It addresses the question of whether a given Bézier curve of degree {math}`n` can be represented by a curve of lower degree, for instance {math}`n-1`. While this is generally not possible without loss of information, degree reduction is valuable in practice for:
- Computational efficiency, by reducing the cost of curve evaluation, rendering, and downstream geometric operations.
- Data compression, through a reduction in the number of control points.
- Improved interactive control, as lower-degree curves are often easier to manipulate in CAD/CAM workflows.

In general, exact degree reduction is not possible unless the original curve already lies in a lower-degree polynomial space.
#### Why Degree Reduction Is an Approximation (Intuitive Explanation)
The Bernstein polynomials of degree {math}`n` form a basis for the vector space of all polynomials of degree at most {math}`n`. Consequently, a Bézier curve of degree {math}`n` represents a generic element of this space. When considering degree reduction to a lower degree {math}`m < n`, the target representation is restricted to a strictly smaller subspace spanned by the Bernstein polynomials of degree {math}`m`.

Since this lower-degree space is a proper subspace of the original one, most degree-{math}`n` polynomials do not belong to it. Exact representation is therefore only possible if the original curve happens to lie entirely within that lower-dimensional space, namely if its highest-degree components vanish. In terms of control points, this corresponds to the vanishing of higher-order forward differences, which is a nongeneric and highly restrictive condition.

From a geometric perspective, degree elevation introduces redundancy by embedding a lower-degree polynomial into a higher-degree space without changing the curve geometry. Degree reduction attempts the inverse operation: it seeks to project a higher-degree polynomial onto a lower-dimensional space. However, unlike degree elevation, this projection cannot, in general, preserve all information. As a result, some geometric detail is inevitably lost.

Therefore, exact degree reduction exists only in exceptional cases, specifically when the curve was originally of lower degree and later degree-elevated. In all other cases, degree reduction must be formulated as an approximation problem, where the goal is to find the closest lower-degree curve according to a chosen error metric. 

{numref}`degree_reduction_example` shows an example of the effect of degree elevation and reduction on the same curve.


```{figure}./imgs/degree_reduction.png
:label: degree_reduction_example
:alt: Degree reduction example with original and reduced Bézier curves
:align: center

Degree elevation and reduction example: original curve (black) and reduced curve (red).
```


A common approach is to determine the reduced-degree curve by minimizing the squared error between the two curves. See {ref}`degree-red-note` for a formal implementation of the Least-Squares Degree Reduction applied to Bézier curve, {ref}`degree-red-concrete` for a numerical example. If you want to play with the python implementation see {ref}`degree-red-python`.

(degree-red-note)=
:::{prf:example .simple .dropdown icon=false open=false} Least-Squares Degree Reduction Example

Let a Bézier curve of degree {math}`n` be given by
```{math}
c(t)=\sum_{i=0}^{n} P_i\,B_i^n(t),
\qquad t\in[0,1].
```

We seek a lower-degree curve {math}`\tilde{c}(t)` of degree {math}`m<n`:
```{math}
\tilde{c}(t)=\sum_{j=0}^{m} \tilde{P}_j\,B_j^m(t).
```

We choose the reduced control points {math}`\{\tilde{P}_j\}` by minimizing the squared error:
```{math}
\min_{\{\tilde{P}_j\}}
\int_0^1 \|c(t)-\tilde{c}(t)\|^2\,dt.
```

Substituting the Bézier representations gives
```{math}
\min_{\{\tilde{P}_j\}}
\int_0^1
\left\|
\sum_{i=0}^{n} P_i B_i^n(t)
-
\sum_{j=0}^{m} \tilde{P}_j B_j^m(t)
\right\|^2
\,dt.
```

For a vector-valued curve {math}`c(t)\in\mathbb{R}^d`, write
```{math}
c(t)=(c_1(t),\ldots,c_d(t)),
```
so the error splits by components:
```{math}
\int_0^1 \|c(t)-\tilde{c}(t)\|^2\,dt
=\int_0^1\sum_{\ell=1}^d \big(c_\ell(t)-\tilde{c}_\ell(t)\big)^2\,dt.
```
Thus the vector problem reduces to {math}`d` independent scalar least-squares problems with the same Bernstein basis.

To derive the linear system, expand the squared error and set its partial derivatives with respect to each unknown control point {math}`\tilde{P}_j` to zero. This yields one equation for each index {math}`j=0,\ldots,m`.
Introduce the inner products between Bernstein basis functions:
```{math}
M_{jk}=\int_0^1 B_j^m(t)\,B_k^m(t)\,dt,
\qquad
b_j=\int_0^1 c(t)\,B_j^m(t)\,dt,
```
where {math}`M` is the {math}`(m+1)\times(m+1)` Gram matrix of the basis and {math}`b` is a vector of length {math}`m+1`. The index {math}`k` is the summation index over the basis functions, so for each fixed {math}`j` we sum {math}`k=0,\ldots,m`.

The normal equations for the unknown control points are:
```{math}
\sum_{k=0}^{m} M_{jk}\,\tilde{P}_k=b_j,
\qquad j=0,\ldots,m.
```

The matrix {math}`M` is symmetric and positive definite (the Bernstein basis is linearly independent), so the solution is unique. Solving this linear system yields the reduced-degree Bézier curve that minimizes the mean squared distance to the original curve.
:::


(degree-red-concrete)=
:::{prf:example .simple .dropdown icon=false open=false} Least-Squares Degree Reduction: Cubic to Quadratic

We consider a concrete example of least-squares degree reduction from a cubic Bézier curve ({math}`n=3`) to a quadratic one ({math}`m=2`).

Let the original cubic Bézier curve be
```{math}
c(t)=\sum_{i=0}^{3} P_i\,B_i^3(t),
\qquad t\in[0,1].
```

We seek a quadratic Bézier curve
```{math}
\tilde{c}(t)=\sum_{j=0}^{2} \tilde{P}_j\,B_j^2(t),
```
that minimizes the squared error
```{math}
\int_0^1 \|c(t)-\tilde{c}(t)\|^2\,dt.
```

The minimization problem leads to the normal equations
```{math}
\sum_{k=0}^{2} M_{jk}\,\tilde{P}_k = b_j,
\qquad j=0,1,2,
```
with
```{math}
M_{jk} = \int_0^1 B_j^2(t)\,B_k^2(t)\,dt,
\qquad
b_j = \int_0^1 c(t)\,B_j^2(t)\,dt.
```

Since
```{math}
c(t)=\sum_{i=0}^3 P_i B_i^3(t),
```
we can write
```{math}
b_j = \sum_{i=0}^3 P_i N_{ji},
\qquad
N_{ji} = \int_0^1 B_j^2(t)\,B_i^3(t)\,dt.
```

Hence, the system becomes
```{math}
M\,\tilde{P} = N\,P.
```

For this case, the matrices are
```{math}
M=
\begin{pmatrix}
\frac15 & \frac{1}{10} & \frac{1}{30}\\
\frac{1}{10} & \frac{2}{15} & \frac{1}{10}\\
\frac{1}{30} & \frac{1}{10} & \frac15
\end{pmatrix},
```

```{math}
N=
\begin{pmatrix}
\frac16 & \frac{1}{10} & \frac{1}{20} & \frac{1}{60}\\
\frac{1}{15} & \frac{1}{10} & \frac{1}{10} & \frac{1}{15}\\
\frac{1}{60} & \frac{1}{20} & \frac{1}{10} & \frac16
\end{pmatrix}.
```

Solving the system yields the reduced control points in closed form:
```{math}
\begin{aligned}
\tilde{P}_0 &= \frac{19}{20}P_0+\frac{3}{20}P_1-\frac{3}{20}P_2+\frac{1}{20}P_3,\\
\tilde{P}_1 &= -\frac14 P_0+\frac34 P_1+\frac34 P_2-\frac14 P_3,\\
\tilde{P}_2 &= \frac{1}{20}P_0-\frac{3}{20}P_1+\frac{3}{20}P_2+\frac{19}{20}P_3.
\end{aligned}
```

These formulas apply componentwise and therefore hold for planar and spatial Bézier curves.

Let
```{math}
P_0=(0,0),\quad
P_1=(1,2),\quad
P_2=(3,2),\quad
P_3=(4,0).
```

The reduced quadratic control points are
```{math}
\tilde{P}_0=\left(-\frac{1}{10},0\right),\quad
\tilde{P}_1=(2,3),\quad
\tilde{P}_2=\left(\frac{41}{10},0\right).
```

This example illustrates how least-squares degree reduction distributes the approximation error over the parameter interval and does not, in general, preserve endpoint interpolation unless additional constraints are imposed.
:::


Great references for degree reduction are {cite}`Watkins_1988` and {cite}`Eck_1993`.

#### Why degree reduction?

- Reduction of CPs or degree?




