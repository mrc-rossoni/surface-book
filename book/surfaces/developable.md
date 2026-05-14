---
title: Developable Surfaces
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---


(ch-developable)=

Curvature plays a central role in geometric modeling and CAD because it provides quantitative information about how curves and surfaces bend in space. Curvature analysis is essential in shape design, aesthetic evaluation, manufacturability assessment and surface optimization. In the context of developable surfaces, curvature becomes particularly important because it determines whether a surface can be flattened without deformation.

# Curvature of a NURBS Curve

Curvature measures how much a curve deviates from being straight at a point. Intuitively, it describes how sharply the curve bends locally.
Recalling the parametric definition of a NURBS curve is:

```{math}
c(u)=\frac{\sum_{i=0}^{n} M_{i,p}(u)\, w_i\, P_i}
{\sum_{i=0}^{n} M_{i,p}(u)\, w_i}
```

where, {math}`P_i` are the control points, {math}`w_i` are the weights, {math}`M_{i,p}(u)` are the basis functions of degree {math}`p` and {math}`u` is the curve parameter. The parameter {math}`u` does not necessarily correspond to physical distance along the curve. For this reason, curvature is often expressed with respect to the arc length {math}`s`.

The arc length is:

```{math}
s(u)=\int_a^u \|\dot{x}(u)\|\,du
```

Curvature with respect to the arc length is defined as:

```{math}
k(s)=\left\|\ddot{c}(s)\right\|
```

:::{note}
Notation:

- {math}`\dot{(\ )}` : derivative with respect to the parameter {math}`u`
- {math}`{(\ )}'` : derivative with respect to the arc length {math}`s`
:::

For a parametric curve, curvature can be computed directly from the first and second derivatives:

```{math}
k(u)=\frac{\|c'(u)\times c''(u)\|}
{\|c'(u)\|^3}
```

where {math}`c'(u)` is the first derivative (tangent vector), {math}`c''(u)` is the second derivative and {math}`\times` denotes the cross product.

Geometrically, the formula has an intuitive interpretation: {math}`c'(u)` gives the tangent direction, while {math}`c''(u)` measures how this tangent changes along the curve. However, {math}`c''(u)` may contain two different effects: a change in speed and a change in direction. Curvature should measure only the change in direction, because this is the effect associated with bending. The cross product {math}`c'(u)\times c''(u)` removes the component of {math}`c''(u)` that is parallel to {math}`c'(u)`. This parallel component changes only the speed along the curve. The remaining perpendicular component changes the direction of the tangent vector, therefore producing bending. The denominator {math}`\|c'(u)\|^3` normalizes the expression with respect to the curve speed. This is necessary because the parameter {math}`u` is arbitrary: the same geometric curve could be traversed faster or slower depending on the chosen parametrization. Without this normalization, curvature would depend on the parametrization rather than on the geometry of the curve. The factor {math}`\|c'(u)\|^3` appears naturally when converting derivatives from parameter space to arc-length space.

Curvature analysis is fundamental in CAD and geometric modeling because it helps evaluate smoothness, manufacturability, aerodynamic behavior and aesthetic quality of free-form shapes. In industrial design and sheet metal applications, curvature is also related to bending constraints and surface developability.

# Curvature of a NURBS Surface

The curvature of a surface quantifies the extent to which the surface deviates from being locally flat at a given point. Unlike curves, surfaces can bend differently depending on the direction considered on the tangent plane. For this reason, at each point on a surface two principal curvatures can be defined: the maximum curvature {math}`k_1` and the minimum curvature {math}`k_2`.

A NURBS surface is defined parametrically as:

```{math}
S(u,v)=
\frac{
\sum_{i=0}^{n}\sum_{j=0}^{m}
N_{i,p}(u)\,M_{j,q}(v)\,w_{i,j}\,P_{i,j}
}{
\sum_{i=0}^{n}\sum_{j=0}^{m}
N_{i,p}(u)\,M_{j,q}(v)\,w_{i,j}
}
```

where {math}`P_{i,j}` are the control points, {math}`w_{i,j}` are the weights, {math}`N_{i,p}(u)` and {math}`M_{j,q}(v)` are the basis functions, and {math}`u,v` are the surface parameters. The local geometric properties of a surface are described through the First and Second Fundamental Forms.

The First Fundamental Form defines the intrinsic metric of the surface, allowing distances, angles and areas to be measured directly on the surface.

```{math}
I=dS\cdot dS=
\begin{bmatrix}
S_u\cdot S_u & S_u\cdot S_v \\
S_u\cdot S_v & S_v\cdot S_v
\end{bmatrix}
```

where {math}`S_u=\frac{\partial S}{\partial u}` is the tangent vector in the {math}`u` direction while {math}`S_v=\frac{\partial S}{\partial v}` is the tangent vector in the {math}`v` direction.

While the First Fundamental Form describes intrinsic geometry, the Second Fundamental Form describes how the surface bends in the surrounding three-dimensional space. It measures the variation of the surface normal vector.The unit normal vector is:
```{math}
\vec{n}=
\frac{S_u\times S_v}
{\|S_u\times S_v\|}
```
The Second Fundamental Form is:
```{math}
II=
\begin{bmatrix}
\vec{n}\cdot S_{uu} & \vec{n}\cdot S_{uv} \\
\vec{n}\cdot S_{uv} & \vec{n}\cdot S_{vv}
\end{bmatrix}
```
where {math}`S_{uu}` is the second derivative with respect to {math}`u`, {math}`S_{vv}` is the second derivative with respect to {math}`v` and {math}`S_{uv}` is the mixed derivative. The Second Fundamental Form measures how the tangent plane changes while moving along the surface.

The curvature tensor (or shape operator) is defined as:
```{math}
K=II\cdot I^{-1}
```
The eigenvalues of this tensor correspond to the principal curvatures, {math}`k_1` and {math}`k_2`.
```
while the eigenvectors define the principal directions. The principal directions identify the orientations along which the surface bends the most and the least.

## Gaussian and Mean Curvature

Two important scalar quantities can be derived from the principal curvatures.

The Gaussian curvature is:

```{math}
K_G=k_1k_2
```
It describes the intrinsic curvature of the surface. {math}`K_G>0` identifies elliptic region (sphere-like), {math}`K_G<0` identifies hyperbolic region (saddle-like) while {math}`K_G=0` identifies parabolic regions; developable surfaces are a special class of surfaces satisfying this condition.

The Mean curvature is:

```{math}
H=\frac{k_1+k_2}{2}
```

Mean curvature is important in CAD because it provides a compact measure of the overall local bending of a surface. While Gaussian curvature describes the intrinsic shape of the surface, mean curvature is strongly related to surface smoothness, fairness and physical behavior, which are central aspects in geometric design.

In CAD and industrial design, surfaces are rarely evaluated only by their shape; they are also evaluated by how smooth and visually pleasing they appear. Mean curvature helps identify unwanted bumps, oscillations, ripples and discontinuities between patches. Geometrically large values of {math}`H` indicate strong bending, small values indicate nearly flat regions and smooth variations of {math}`H` usually correspond to aesthetically fair surfaces.

:::{hint}
Mean curvature is also important because it appears naturally in many physical processes. For example soap films,
membrane deformation and surface tension phenomena are governed by mean curvature. A surface with 
{math}`H=0` is is called a minimal surface: this condition means that the two principal curvatures balance each other {math}`k_1=-k_2`. In other words, the surface bends equally in opposite directions. As a consequence, the surface avoids unnecessary local area expansion and tends to distribute curvature smoothly. Minimal surfaces are surfaces that locally minimize their area while satisfying given boundary conditions. They represent the most efficient geometric configuration that a surface can assume, similarly to how a stretched elastic membrane naturally settles into an equilibrium state. They are relevant in engineering because minimizing area is often associated with minimizing material usage, residual stresses, and energy concentrations. This is particularly important in shell structures, membrane structures, lattice geometries, and advanced lightweight components.
:::



# Ruled Surfaces
Ruled surfaces, also called lofted surfaces, are of considerable importance for the design of "functional" surfaces in mechanical engineering. 

A ruled surface is a surface generated by the continuous motion of a straight line in space. The moving line is called the ruling of the surface. A ruled surface can be expressed parametrically as:

```{math}
S(u,v)=c(u)+v\,d(u)
```

where {math}`c(u)` is a space curve called the directrix, {math}`d(u)` is the direction vector of the ruling and {math}`v` parameterizes the straight line associated with each value of {math}`u`.

{numref}`ruled` shows an example of ruled surface.

```{figure} ../imgs/ruled.png
:label: ruled
:alt: Ruled Surface
:align: center

Example of a ruled surface generated by a family of straight rulings (highlighted in red). Although the surface exhibits complex global shape variations, each local section is generated by the continuous motion of a straight line in space.
```

# Developable Surfaces
A special subset of ruled surfaces is represented by developable surfaces. A developable surface is a ruled surface with zero Gaussian curvature. In other words, a developable surface is a ruled surface with zero Gaussian curvature:

```{math}
K_G=0
```

In developable ruled surfaces, consecutive rulings remain tangent to the surface normal field, allowing the surface to be flattened onto a plane without stretching or tearing.

Ruled surfaces are extensively used in sheet metal design, ship hull modeling, architectural geometry, free-form surface approximation, manufacturing-oriented CAD.
In industrial applications, ruled and developable surfaces are particularly attractive because they simplify fabrication processes such as bending, rolling and extrusion.

# Manufacturing Considerations

Manufacturing free-form surfaces that are neither ruled nor developable is significantly more challenging than manufacturing developable geometries. These surfaces generally exhibit double curvature, meaning that the material must deform simultaneously in multiple directions.

Typical examples include automotive body panels, complex architectural skins, organic and ergonomic shapes, helmets and sculptural geometries, most spline-based or NURBS free-form surfaces.
Unlike developable surfaces, these geometries cannot usually be obtained by simple bending operations because their Gaussian curvature is nonzero:

```{math}
K_G\neq0
```

As a consequence, the material must undergo stretching, shrinking, or localized thinning during the forming process.

The main manufacturing challenges are material stretching or compression, thickness variation, risk of wrinkling or tearing, more complex tooling and molds, multi-stage forming processes, higher production costs. Traditional sheet-metal operations such as pure bending or rolling are often insufficient for these geometries. Instead, advanced forming technologies are required. Common manufacturing approaches include stamping, deep drawing, hydroforming, incremental sheet forming, composite layup, thermoforming, additive manufacturing, multi-piece construction.

Stamping and deep drawing are widely used in automotive manufacturing for producing large quantities of complex thin-walled components. These processes require careful control of material flow and thickness distribution in order to avoid excessive thinning and tearing. For highly complex or organic geometries, additive manufacturing and composite layup techniques can provide significantly greater geometric freedom because they are not constrained by developability requirements.

In CAD and geometric modeling, manufacturability analysis is therefore essential. Curvature analysis, Gaussian curvature maps, thickness simulations and forming simulations are commonly used to evaluate whether a surface can be manufactured efficiently and safely.