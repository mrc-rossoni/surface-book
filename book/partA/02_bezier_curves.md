# Bézier Curves

## Learning objectives
By the end of this chapter you will be able to:
1. Describe Bézier curves as polynomial parametric curves.
2. Understand the role of control points and the convex hull property.
3. Derive the Bernstein basis and evaluate Bézier curves.
4. Implement the De Casteljau algorithm and explain its numerical stability.

---

## 1. Motivation
Bézier curves are a foundational building block for surface modeling in engineering CAD systems.
Although industrial models typically rely on B-splines and NURBS, Bézier curves remain the simplest case
where the geometry is entirely controlled by a finite set of points and a well-defined basis.

They are used for:
- local shape editing (via control points),
- smooth profile definition (aerodynamics, industrial design),
- construction of surface patches,
- and as a conceptual entry point to B-splines.

---

## 2. Definition
A Bézier curve of degree \(n\) is defined by \(n+1\) control points \(P_0, ..., P_n\) and is written as:

\[
C(u) = \sum_{i=0}^{n} B_i^n(u) P_i, \qquad u \in [0,1]
\]

where \(B_i^n(u)\) are the **Bernstein polynomials**:

\[
B_i^n(u) = \binom{n}{i} u^i (1-u)^{n-i}
\]

---

## 3. Key properties

### 3.1 Endpoint interpolation
\[
C(0) = P_0,\qquad C(1) = P_n
\]

### 3.2 Convex hull property
For \(u \in [0,1]\), the curve lies inside the convex hull of its control points.
This is extremely important in engineering: it gives a geometric bound
and makes control point editing predictable.

### 3.3 Variation diminishing property
The curve does not oscillate more than its control polygon.
This makes Bézier curves stable and well-behaved for design.

---

## 4. Evaluating a Bézier curve
We can evaluate \(C(u)\) in two main ways:

1. **Direct Bernstein basis evaluation**  
   Simple, but can be numerically unstable for high degree.

2. **De Casteljau algorithm**  
   More stable; based on repeated linear interpolation.

---

## 5. De Casteljau algorithm (derivation)
Given control points \(P_0, ..., P_n\), define recursively:

\[
P_i^{(0)} = P_i
\]

\[
P_i^{(r)} = (1-u)P_i^{(r-1)} + uP_{i+1}^{(r-1)}
\]

for \(r = 1, ..., n\).

The final point on the curve is:

\[
C(u) = P_0^{(n)}
\]

---

## 6. Engineering note: why stability matters
In engineering workflows, Bézier curves may appear indirectly:
- as part of surface patches,
- as internal representation during conversion steps,
- or during fitting.

The De Casteljau algorithm is preferred in practice because it avoids the numerical issues
of evaluating high-degree polynomials.

---

## Exercises
1. Show that \(\sum_{i=0}^{n} B_i^n(u) = 1\).
2. Prove endpoint interpolation.
3. Implement De Casteljau and compare its output with the Bernstein evaluation for increasing degree.
