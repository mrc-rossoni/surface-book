:::{glossary}
Inner Product
: An inner product is a generalization of the dot product. In a vector space, it is a way to multiply vectors together, with the result of this multiplication being a scalar. [More detail here](https://mathworld.wolfram.com/InnerProduct.html).

Map
: A map associates each parameter value {math}`u` with one point in space. In CAD language: the parameter moves along the curve and generates points in space.

Support
: TBD

Bézier decomposition
: Bézier decomposition is the process of converting a B-spline curve into a sequence of Bézier segments by inserting knots until each internal knot has multiplicity {math}`p+1`, thereby partitioning the curve into independent polynomial pieces without altering its geometry. Bézier decomposition is widely used in manufacturing applications such as CNC toolpath generation. By converting a B-spline curve into independent Bézier segments, the geometry can be processed locally using simple and numerically stable algorithms. This facilitates adaptive subdivision, error control, and conversion into machine-level primitives such as linear and circular interpolation, which are required for execution by some CNC controllers.


:::
