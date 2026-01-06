# Parametric Curves

A curve is the locus of a one-parameter family of points. In computational geometry, a curve can be defined more precisely as a mapping:

```{math}
\mathbf{C}: \mathbb{R} \rightarrow \mathbb{R}^3
```

meaning that for every parameter value {math}`u`, the curve returns a point in 3D space.

Different mathematical representations exist (intrinsic, explicit, implicit, parametric), but for CAD and computational applications we need a framework that is:

- **independent of the chosen coordinate system**, so that shape does not change when the reference frame changes;
- **computable**, i.e. easy to evaluate, differentiate, and integrate numerically;
- **flexible**, to represent planar and non-planar geometries;
- **controllable**, so that designers can modify the shape locally and predictably.

Explicit and implicit equations are useful in mathematics, but they are not the best foundation for geometric modeling systems.

## Explicit Equations

In the plane, the explicit equation of a curve takes the general form:

```{math}
y = f(x)
```

This form has important limitations:

- there is only one {math}`y` value for each {math}`x`;
- it cannot represent closed curves or multi-valued geometries.

## Implicit Equations

An implicit curve in the plane is defined as:

```{math}
f(x,y)=0
```

Example: a unit circle in the {math}`XY` plane:

```{math}
f(x,y)=x^2+y^2-1=0
```

```{figure}./imgs/image.png
:label: myFigure
:alt: Circle in a plane
:align: center

circle lying in the XY plane
```

Implicit equations avoid some limitations of explicit ones, but they still present major issues for CAD:

- they are **axis-dependent**;
- they are harder to sample parametrically. As they do not provide a natural parameterization, generating points on the curve (needed for tessellation, meshing, and rendering) typically requires numerical procedures such as root finding or marching algorithms.
- geometric properties (tangents, curvature) are not naturally expressed;
- extending to bounded, trimmed, or non-planar curves is non-trivial.

## Why explicit and implicit forms are not ideal for modeling

Both explicit and implicit representations are **axis-dependent**.

- The shapes of most objects are intrinsically independent of any coordinate system. We need a modeling framework where the choice of a CSYS does not affect the shape.
- Any solid (closed object) will have tangent lines or tangent planes that may become parallel to principal axes of the chosen CSYS. This can lead to ill-defined mathematical properties or numerical instabilities.
- Curves and surfaces are often non-planar and bounded, making them difficult to represent robustly using explicit and implicit equations.

For programming and computability, other forms are preferable.

## Parametric Equations of Curves

A parametric curve in the plane is written as:

```{math}
\begin{cases}
x = x(u) \\
y = y(u)
\end{cases}
```

In 3D:

```{math}
\begin{cases}
x = x(u) \\
y = y(u) \\
z = z(u)
\end{cases}
```

Example: a helix

```{math}
\begin{cases}
x=\sin(u) \\
y=\cos(u) \\
z=u
\end{cases}
```

:::{figure}
:label: Helix
:alt: Helix
:align: center
:class: grid grid-cols-2 items-end gap-4 

(Helix3D)=
![Helix in 3D Space](./imgs/3D_Curve_Helix.png)

(HelixPar)=
![Helix in Parameters Space](./imgs/3D_Curve_Helix_Parameter_Space.png)

Helix in the 3D and Parametric Space
:::

Parametric representations are the standard approach in CAD and computational geometry because:

- they are **coordinate-system independent**;
- they can represent **bounded, non-planar curves** naturally;
- they enable **efficient evaluation and differentiation** (tangent, curvature, arc length, etc.);
- they provide a consistent foundation for curves, surfaces, and solid modeling schemes.

## The key question: how do we build parametric curves in a general way?

A parametric curve is only as useful as the functions used to define {math}`x(u), y(u), z(u)`.

In the helix example, we selected:

```{math}
\{\sin(u), \cos(u), u\}
```

but these functions are too specific: they generate one particular curve and do not provide a general modeling framework.

In engineering design we often need to solve a more general problem:

> Given a set of points, find a smooth curve interpolating or approximating the data.

To address this, we need a **generic and controllable way** to construct parametric curves.

## From “functions” to a modeling framework: basis functions

Instead of defining {math}`x(u), y(u), z(u)` independently, we build the curve as a linear combination of **basis functions**:

```{math}
\mathbf{C}(u)=\sum_{i=0}^{n} \mathbf{P}_i\,N_i(u)
```

where:

- {math}`\mathbf{P}_i \in \mathbb{R}^3` are **control points**{ref}`(see note)<control-point-note>`; 
- {math}`N_i(u)` are **basis functions**{ref}`(see note)<basis-function-note>` that determine the shape, continuity, and smoothness;
- the curve becomes controllable by editing {math}`\mathbf{P}_i`.

(control-point-note)=
:::{note .simple .dropdown icon=false open=false} Control Point
**Control points** are not points on the curve. Points on the curve are outcomes (results) of the representation and are not suitable parameters for design: specifying them leads either to piecewise-linear approximations or to unstable global interpolation problems. Control points, instead, act as a compact set of design variables that shape the curve through basis functions, enabling smoothness, efficient evaluation, and predictable local editing.

If we need the curve to pass through data points, we do that via:

- **interpolation**: solve for control points such that {math}`C(u_k)=Q_k`
- **approximation / fitting**: least squares
- **constraint-based modeling**: force certain curve points to match

So even when we start from points on the curve, we still convert them into control points.
:::

(basis-function-note)=
:::{note .simple .dropdown icon=false open=false} Basis Function
A set of basis functions $\{Ni(u)\}$ is a collection of functions that span a space of parametric curves. Any curve in this space can be written as a linear combination  $\sum_{i} P_i N_i(u)$, where the coefficients $P_i$ are the control points.
 :::



This is the fundamental idea behind curves and surface representation in CAD. The choice of basis functions is what turns parametric equations into a powerful and general modeling system. Basis functions span a function space: they define what shapes are possible and what properties the curve will have. Different choices of basis functions produce different curve families:

- power basis $\rightarrow$ polynomials in $u$
- Bernstein basis $\rightarrow$ Bézier curves
- B-spline basis $\rightarrow$ B-splines
- rational B-spline basis $\rightarrow$ NURBS

The choice of basis functions determines key geometric and computational features, such as degree of the curve, continuity, local vs global control (local support or not), smoothness and fairness and the ability to represent special shapes (e.g., conics). So basis functions are not just “mathematical convenience”: they are the core design decision behind a modeling system.