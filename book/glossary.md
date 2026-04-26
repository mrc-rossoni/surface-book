:::{glossary}
Inner Product
: An inner product is a generalization of the dot product. In a vector space, it is a way to multiply vectors together, with the result of this multiplication being a scalar. [More detail here](https://mathworld.wolfram.com/InnerProduct.html).

Map
: A map associates each parameter value {math}`u` with one point in space. In CAD language: the parameter moves along the curve and generates points in space.

Support
: TBD

Bézier decomposition
: Bézier decomposition is the process of converting a B-spline curve into a sequence of Bézier segments by inserting knots until each internal knot has multiplicity {math}`p+1`, thereby partitioning the curve into independent polynomial pieces without altering its geometry. Bézier decomposition is widely used in manufacturing applications such as CNC toolpath generation. By converting a B-spline curve into independent Bézier segments, the geometry can be processed locally using simple and numerically stable algorithms. This facilitates adaptive subdivision, error control, and conversion into machine-level primitives such as linear and circular interpolation, which are required for execution by some CNC controllers.


Tensor Product
: The tensor product {math}`V \otimes W` of two vector spaces {math}`V` and {math}`W`, defined over the same field, is a new vector space associated with a bilinear map {math}`V \times W \rightarrow V \otimes W`. This map associates each pair {math}`(v,w)`, with {math}`v \in V` and {math}`w \in W`, with an element denoted by {math}`v \otimes w`. The key property of the tensor product is bilinearity, meaning that the mapping is linear in each argument separately. Intuitively, the tensor product provides a way to combine two independent directions or sets of functions into a higher-dimensional structure while preserving linearity in each component. For example, if one function varies along the {math}`u` direction and another varies along the {math}`v` direction, their tensor-product function is obtained by multiplying them {math}`f(u)\,g(v)`. This produces a new function that depends on both parameters {math}u and {math}v. In this sense, the tensor product can be understood as a way to combine two independent parametric directions: one along {math}`u`, one along {math}`v`, with the final result depending on both at the same time.

:::
