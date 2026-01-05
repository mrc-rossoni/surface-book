# B-spline Curves

## Learning objectives
By the end of this chapter you will be able to:
1. Explain why B-splines generalize Bézier curves.
2. Define a B-spline curve using control points, degree, and knot vector.
3. Derive and implement the Cox–de Boor recursion.
4. Evaluate a B-spline curve numerically and interpret continuity from knots.

---

## 1. Motivation
Bézier curves are globally controlled: moving one control point changes the whole curve.
For complex engineering shapes we need:
- local control,
- scalable complexity,
- piecewise polynomial representation.

This is exactly what B-splines provide.

---

## 2. Definition
A B-spline curve of degree \(p\) is defined as:

\[
C(u) = \sum_{i=0}^{n} N_{i,p}(u) P_i
\]

where:
- \(P_i\) are control points
- \(N_{i,p}(u)\) are B-spline basis functions
- \(U = \{u_0, u_1, ..., u_m\}\) is a non-decreasing knot vector
- \(m = n + p + 1\)

---

## 3. Cox–de Boor recursion
The basis functions are defined recursively.

### Degree 0:
\[
N_{i,0}(u) =
\begin{cases}
1 & \text{if } u_i \le u < u_{i+1} \\
0 & \text{otherwise}
\end{cases}
\]

### Degree p:
\[
N_{i,p}(u) =
\frac{u-u_i}{u_{i+p}-u_i} N_{i,p-1}(u)
+
\frac{u_{i+p+1}-u}{u_{i+p+1}-u_{i+1}} N_{i+1,p-1}(u)
\]

---

## 4. Continuity and knot multiplicity
Let a knot \(u_k\) have multiplicity \(s\).
Then the curve is:
\[
C^{p-s} \text{ continuous at } u_k
\]

This connects directly to engineering constraints:
- sharp edges: reduced continuity
- smooth transitions: higher continuity

---

## Exercises
1. Prove that B-spline basis functions form a partition of unity.
2. Construct knot vectors for open uniform B-splines and evaluate continuity.
3. Compare local control of B-splines vs Bézier curves.
