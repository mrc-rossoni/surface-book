import numpy as np

def as_array(x, dtype=float):
    """Convert input to numpy array with a given dtype."""
    return np.asarray(x, dtype=dtype)

def norm(x):
    """Euclidean norm."""
    x = as_array(x)
    return np.linalg.norm(x)

def normalize(x, eps=1e-12):
    """Normalize a vector, with numerical safeguard."""
    x = as_array(x)
    n = norm(x)
    if n < eps:
        return x * 0.0
    return x / n

def dot(a, b):
    """Dot product."""
    return float(np.dot(as_array(a), as_array(b)))

def cross(a, b):
    """Cross product (3D)."""
    return np.cross(as_array(a), as_array(b))
