# Vectors, Frames, and Parametric Geometry

## Learning objectives
By the end of this chapter you will be able to:
1. Describe vectors and coordinate frames in an engineering geometry context.
2. Use affine combinations and barycentric coordinates.
3. Interpret parametric representations as mappings from parameter space to geometry space.
4. Recognize why stable numerical operations matter in surface modeling.

---

## 1. Why this matters in surface modeling
Engineering geometry is built on **coordinate frames**, **transformations**, and **parametric mappings**.

A curve is a function:
\[
C: [a,b] \rightarrow \mathbb{R}^d
\]
A surface is a function:
\[
S: D \subset \mathbb{R}^2 \rightarrow \mathbb{R}^3
\]

In both cases, we are mapping a parameter space into physical space.

---

## 2. Vectors and affine space
In geometric modeling, points and vectors play different roles:

- A **point** represents a location in space.
- A **vector** represents a displacement.

Affine combinations are crucial. Given points \(P_0, P_1\),
\[
P(u) = (1-u)P_0 + uP_1
\]
is a **linear interpolation**. This is the basic operation behind:
- Bézier curves (De Casteljau)
- B-splines (recursive blending)
- surface patches (tensor product interpolation)

---

## 3. Coordinate frames and transformations
A coordinate frame consists of an origin \(O\) and basis vectors \(\{e_1, e_2, e_3\}\).

A rigid transformation is:
\[
x' = R x + t
\]
where \(R\) is a rotation matrix and \(t\) is a translation vector.

Engineering note: transformations appear everywhere in CAD interoperability
(STEP/IGES), assembly modeling, and simulation pipelines.

---

## 4. Parametric viewpoint
A parametric representation is a mapping:

\[
(u, v) \mapsto S(u,v)
\]

This viewpoint is essential because:
- derivatives w.r.t. parameters give tangent directions
- normals derive from cross products
- curvature depends on first and second derivatives

---

## Exercises
1. Write a function that linearly interpolates between two points.
2. Given a set of points, compute their centroid and interpret it as an affine combination.
3. Implement a rigid transformation and apply it to a point cloud.
