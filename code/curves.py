import numpy as np

# ============================================================
# Bézier curves
# ============================================================

def bernstein(i, n, u):
    """Bernstein polynomial B_i^n(u)."""
    from math import comb
    return comb(n, i) * (u**i) * ((1 - u)**(n - i))

def bezier_eval(control_points, u):
    """
    Evaluate a Bézier curve C(u) using Bernstein basis.
    control_points: (n+1, dim)
    u: scalar or array in [0,1]
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1
    u = np.asarray(u, dtype=float)

    # output shape: (..., dim)
    C = np.zeros(u.shape + (P.shape[1],), dtype=float)
    for i in range(n + 1):
        C += bernstein(i, n, u)[..., None] * P[i]
    return C

def de_casteljau(control_points, u):
    """
    Evaluate a Bézier curve using De Casteljau algorithm.
    More numerically stable than direct Bernstein evaluation.
    """
    P = np.asarray(control_points, dtype=float)
    u = float(u)
    Q = P.copy()
    n = len(Q) - 1
    for r in range(1, n + 1):
        for i in range(n - r + 1):
            Q[i] = (1 - u) * Q[i] + u * Q[i + 1]
    return Q[0]

# ============================================================
# B-spline curves
# ============================================================

def find_span(n, p, u, U):
    """
    Find knot span index.
    n = number of control points - 1
    p = degree
    u = parameter
    U = knot vector
    """
    if u >= U[n + 1]:
        return n
    if u <= U[p]:
        return p

    low, high = p, n + 1
    mid = (low + high) // 2
    while u < U[mid] or u >= U[mid + 1]:
        if u < U[mid]:
            high = mid
        else:
            low = mid
        mid = (low + high) // 2
    return mid

def basis_funs(span, u, p, U):
    """
    Compute nonzero B-spline basis functions N_{i-p,...,i}(u).
    """
    N = np.zeros(p + 1)
    left = np.zeros(p + 1)
    right = np.zeros(p + 1)

    N[0] = 1.0
    for j in range(1, p + 1):
        left[j] = u - U[span + 1 - j]
        right[j] = U[span + j] - u
        saved = 0.0
        for r in range(0, j):
            denom = right[r + 1] + left[j - r]
            temp = N[r] / denom
            N[r] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        N[j] = saved
    return N

def bspline_eval(control_points, U, p, u):
    """
    Evaluate B-spline curve C(u) at a single parameter value u.
    control_points: (n+1, dim)
    U: knot vector
    p: degree
    """
    P = np.asarray(control_points, dtype=float)
    n = len(P) - 1

    span = find_span(n, p, u, U)
    N = basis_funs(span, u, p, U)

    C = np.zeros(P.shape[1], dtype=float)
    for j in range(0, p + 1):
        C += N[j] * P[span - p + j]
    return C
