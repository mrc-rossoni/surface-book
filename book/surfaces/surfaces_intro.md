---
title: Parametric Surfaces
---

(ch-surfaces)=
# Parametric Surfaces

So far, geometric entities have been described using a single parameter
{math}`u`. This leads to curves embedded in space, written in the general form

```{math}
\mathbf{C}(u) = \bigl(x(u),y(u),z(u)\bigr)
```

A surface is the natural extension of this idea to two independent parameters.
Instead of moving along a one-dimensional parameter interval, we move over a
two-dimensional parameter domain.

A parametric surface is defined as a mapping

```{math}
\mathbf{S}(u,v)
= \bigl(x(u,v),y(u,v),z(u,v)\bigr),
\qquad (u,v)\in\Omega,
```

where {math}`\Omega \subset \mathbb{R}^2` is the parameter domain.

Geometrically, the surface is obtained by associating each parameter pair
{math}`(u,v)` with one point in space.

A parametric surface can be understood from three complementary points of view. As a **mapping** 
```{math}
\mathbf{S}(u,v)
= \bigl(x(u,v),y(u,v),z(u,v)\bigr),
\qquad (u,v)\in\Omega,
```
where {math}`\Omega \subset \mathbb{R}^2` is the parameter domain. The image of this mapping lies in physical space, usually {math}`\mathbb{R}^3` in CAD applications. Geometrically, the surface is obtained by associating each parameter pair {math}`(u,v)` with one point in space. In this sense, the parameter domain plays the same role as the interval of a curve, but with one additional direction.
  
As a **family of curves**, where, one parameter is fixed and the other is allowed to vary:
  ```{math}
  \mathbf{S}(u,v_0)
  \qquad \text{or} \qquad
  \mathbf{S}(u_0,v)
  ```
The first expression describes a curve obtained by fixing {math}`v=v_0` and varying {math}`u`. The second expression describes a curve obtained by fixing {math}`u=u_0` and varying {math}`v`. These two families are called isoparametric curves. Together, they form a grid on the surface, often called the parametric net. In CAD systems, this
net is important because it reveals how the two parameter directions are organized and how the surface will be evaluated, trimmed, subdivided, or connected to other patches.
  
Finally, as a {term}`tensor product` construction. 
```{math}
\mathbf{S}(u,v)
=
\sum_{i=0}^{n}\sum_{j=0}^{m}
\mathbf{P}_{i,j} N_{i,p}(u) M_{j,q}(v)
```
where The coefficients {math}`\mathbf{P}_{i,j}` define the control net. Most parametric surfaces used in CAD are constructed as tensor products of curve
bases. The idea is to choose one basis in the {math}`u` direction and another basis in the {math}`v` direction. Let {math}`N_{i,p}(u)` be basis functions of degree {math}`p` in the {math}`u` direction, and let {math}`M_{j,q}(v)` be basis functions of degree {math}`q` in the {math}`v` direction. A tensor-product surface is written as
```{math}
\mathbf{S}(u,v)
=
\sum_{i=0}^{n}\sum_{j=0}^{m}
\mathbf{P}_{i,j}\,N_{i,p}(u)\,M_{j,q}(v).
```
The coefficients {math}`\mathbf{P}_{i,j}` are control points arranged in a control net. This is the surface analogue of the control polygon used for curves.

The tensor-product construction is therefore a direct extension of the basis-function representation introduced for curves:
```{math}
\mathbf{C}(u)=\sum_{i=0}^{n}\mathbf{P}_i N_i(u).
```
For curves, each control point is associated with one basis function. For surfaces, each control point is associated with the product of one basis function in the {math}`u` direction and one basis function in the {math}`v` direction.

:::{note} Control net
The indices {math}`i,j` are not only labels. They define the connectivity of the control net. Neighboring control points in the grid determine neighboring regions of the surface, and the two grid directions correspond to the two parameter directions {math}`u` and {math}`v`.
:::

In general, a tensor-product spline surface does not interpolate all control points. Instead, it is shaped by the control net. As in the curve case, the control points act as design variables, while the basis functions determine the smoothness, locality, and approximation properties of the representation.

:::{prf:example} Bilinear surface
The simplest tensor-product surface is obtained by using linear basis functions
in both parameter directions. Let {math}`(u,v)\in[0,1]\times[0,1]`. Given four
corner points {math}`\mathbf{P}_{00}`, {math}`\mathbf{P}_{10}`,
{math}`\mathbf{P}_{01}`, and {math}`\mathbf{P}_{11}`, the bilinear patch is

```{math}
\mathbf{S}(u,v)
=
(1-u)(1-v)\mathbf{P}_{00}
+u(1-v)\mathbf{P}_{10}
+(1-u)v\mathbf{P}_{01}
+uv\mathbf{P}_{11}.
```

This surface interpolates the four corner points. Along each boundary, one parameter is fixed and the patch reduces to a linear curve. Inside the domain, the surface is obtained by blending the four corners through two independent linear interpolations.

The bilinear patch is the surface counterpart of linear interpolation for curves. More advanced CAD surfaces follow the same tensor-product principle, but replace the linear basis functions with Bernstein, B-spline, or rational B-spline basis functions.
:::

These are not different definitions, but different ways to understand the same object. The tensor-product view explains the formula, the control
net explains how the shape is edited, and the family-of-curves view explains the geometry of the parameter directions.



# Properties

Parametric surfaces inherit properties from the curve representations studied earlier: local control, when locally supported spline bases are used; continuity control, through the degree and the knot vectors in each parameter direction; affine invariance; convex-hull behavior, in the same sense as the underlying curve basis.
On top of them, surfaces introduce additional complexity:

- there are two parameter directions instead of one;
- the degrees and knot vectors may differ in the {math}`u` and {math}`v`
  directions;
- geometric behavior may be anisotropic, meaning that the surface can behave
  differently along the two parameter directions;
- continuity must be considered not only along curves, but also across patch
  boundaries.

This last point is especially important in CAD. Complex models are rarely
described by a single surface patch. They are usually assembled from many
patches, and the quality of the resulting model depends strongly on how these
patches meet.


# NURBS Surfaces

NURBS surfaces extend the concept of NURBS curves to two parameters, combining the tensor-product construction of surfaces with the rational formulation introduced for curves. As for curves, the key idea is to combine B-spline basis functions (to control smoothness and locality) and weights (to control geometric influence and enable exact shapes). A NURBS surface of degree {math}`p` in the {math}`u` direction and degree {math}`q` in the {math}`v` direction is defined as:
```{math}
\mathbf{S}(u,v) =
\frac{
\displaystyle \sum_{i=0}^{n} \sum_{j=0}^{m}
w_{i,j} \, \mathbf{P}_{i,j} \, N_{i,p}(u)\, M_{j,q}(v)
}{
\displaystyle \sum_{i=0}^{n} \sum_{j=0}^{m}
w_{i,j} \, N_{i,p}(u)\, M_{j,q}(v)
}
```
where:
- {math}`\mathbf{P}_{i,j}` are control points arranged in a control net,
- {math}`w_{i,j} > 0` are the associated weights,
- {math}`N_{i,p}(u)` and {math}`M_{j,q}(v)` are B-spline basis functions,
- {math}`\mathbf{T}_u` and {math}`\mathbf{T}_v` are knot vectors,
- {math}`(u,v)` belongs to the parametric domain.
