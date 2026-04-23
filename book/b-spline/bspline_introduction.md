---
title: Introduction
---

(ch-bsplines-introduction)=


B-splines extend the spline and Bézier constructions introduced in the previous chapters into a basis-function formulation that combines local geometric control, controllable smoothness, and computational robustness. They are among the most important polynomial representations in computer-aided geometric design because they provide a compact and scalable way to model curves of increasing complexity without requiring a corresponding increase in polynomial degree.

In the chapter on splines, a spline curve was introduced as a piecewise polynomial mapping defined on consecutive knot spans. In the chapter on Bézier curves, polynomial segments were represented in Bernstein form and controlled through a finite set of control points. That construction is geometrically intuitive and well suited for many operations, but it also has two structural limitations. First, a single Bézier curve has global support: moving one control point influences the entire curve. Second, when complex shapes are represented by several Bézier segments, continuity conditions at the joints must be imposed explicitly.

B-splines resolve these limitations by replacing the segment-wise Bernstein representation with a family of basis functions defined over a knot vector. The knot vector partitions the parameter domain and determines where basis functions are active, while the control points determine the geometry of the curve. In this way, the complete curve is described by one global control polygon, one degree, and one knot vector, rather than by a collection of separate polynomial pieces with manually enforced continuity conditions.

The central idea is that the curve is expressed as a linear combination of control points and basis functions,

```{math}
C(u)=\sum_{i=0}^{n} N_{i,p}(u)\,P_i,
```

where {math}`P_i` are the control points and {math}`N_{i,p}` are the B-spline basis functions of degree {math}`p`. Unlike Bernstein polynomials, B-spline basis functions have local support: each basis function is nonzero only on a limited parameter interval. As a consequence, each control point influences only a local portion of the curve. This property is essential in CAD, where local edits must not propagate unnecessarily to distant regions of the model.

A second important feature of B-splines is that continuity is controlled through the knot vector. The multiplicity of a knot determines the degree of smoothness at that parameter value, so continuity does not need to be imposed by separately matching derivatives between adjacent polynomial segments. This provides a unified mathematical framework in which both smooth transitions and reduced-continuity features can be handled by the same representation.

From a computational point of view, B-splines are also preferable to high-degree polynomial curves. In practical engineering applications, curves are usually kept at low degree (most often cubic) while additional shape complexity is introduced by adding control points and knot spans. This avoids the numerical instability and poor shape behavior often associated with high-degree global polynomial interpolation, while preserving a representation that is efficient to evaluate and differentiate.

For these reasons, B-splines have become a standard representation in geometric modeling, computer graphics, and CAD systems. They provide the polynomial foundation for more advanced constructions such as NURBS, and they play a central role in curve design, surface modeling, fitting, refinement, and downstream engineering workflows.

This chapter introduces B-splines in two steps. First, the B-spline basis functions are defined through the knot vector and the Cox-de Boor recursion. Then, these basis functions are used to construct B-spline curves and to study their geometric behavior, including local control, support, and smoothness.
