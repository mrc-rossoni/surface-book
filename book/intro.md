---
title: Course Introduction
numbering:
  title: false
  headings: false
---


Welcome to the course book for **Surface Modeling for Engineering Applications (Master Level)**.

This book has two goals:

1. **Foundations (Part A):** build the fundamental algorithms (curves, surfaces, continuity, curvature) *from scratch*.
2. **Engineering workflows (Part B):** use professional-grade libraries and pipelines to solve realistic problems (fitting, point clouds, fairness, manufacturability constraints).

---

## How to use this book
This book is designed as a hybrid between textbook and lab manual:

- **Theory chapters** explain concepts, derivations, and engineering implications.
- **Lab notebooks** contain runnable code and practical experiments.

You can read everything online and run notebooks directly in **Google Colab** with one click.

---

## Running the lab notebooks
Each notebook starts with a setup cell that:
1. clones the GitHub repository
2. installs dependencies
3. makes the `code/` folder importable

Always run that cell first.

---


# Course Information

The capability to conceive and generate digital representations of their products and projects is an essential skill for engineers. As the design and manufacturing technologies advance, the shape of the products evolves as well, becoming more and more complex. 

This course aims at giving students the ability to make 3D models of complex shapes through surface modeling approaches and understand the role of this technology in different phases of the product development process. The course will present an introduction to 3D surface modeling techniques and their applications in Engineering. The mathematical foundation of parametric curves and surfaces (splines, Bezier, NURBS) will be briefly presented. Beyond the theory, the course will adopt a hands-on approach by allowing students to practice with modern computer-aided design tools. Different 3D models of both aesthetic surfaces and technical surfaces (e.g. ship hull, airfoils, blades, etc.) will be made and discussed. Finally, the capability to prepare those models for numerical analysis will be also discussed.

## Topics
The course covers the following topics:

- Introduction to surface modeling: the role in the product development process and comparison with solid modeling.

- Mathematical foundation of parametric curves and surfaces. The Bézier, Spline, Coons and NURBS both in their rational and non-rational forms will be introduced. The concept of geometric continuity will be discussed.

- Surface modeling approaches: Freeform, patch and subdivision surface.

- Algorithmic and generative approaches to surface generation.

- Reverse Engineering: from point clouds/meshes to surface models.

- Implications of surface topology and geometry for numerical analysis and mesh preparation.

- Strategies to approach the modeling of complex objects with applications and examples to specific domains, such as product design, marine, wind, airfoils and mold.

The course contents will be delivered through lectures and laboratory activities using a 3D modeling software. 

## Prerequisites
Nice-to-have:
- basic calculus
- Programming fundamentals
- Basics of feature-based modeling

## Learning outcomes
By the end of the course, students will:

- understand how CAD tools and 3D modeling software work “under the hood” (geometric representations, surface construction, parameterization, and numerical robustness) and use this knowledge to make more informed modeling decisions throughout the product development process;

- understand why surface modeling is not only a way to create 3D shapes for visualization, but also a key enabler for downstream phases of the PDP, including simulation (CAE/CFD), manufacturing preparation (CAM), tolerance and quality workflows, robotics/offline programming, and digital twins;

- recognize current and emerging industrial and research applications of surface modeling, and evaluate which modeling approaches (and levels of geometric fidelity) are appropriate for a specific use case, balancing accuracy, robustness, and computational cost.

*Rationale:* Since 3D models are ubiquitous—from visualization to simulation—understanding the mathematical and computational principles behind modeling tools helps students drive the development process with greater awareness. The hands-on exercises are designed to let students “try at least once” to build a complex surface-based model, so they can experience the practical challenges and limitations of modeling systems and learn how to create higher-quality digital representations suitable for downstream phases of the product development process. The theoretical part, supported by applied Python implementations, reinforces this understanding and connects surface modeling to broader domains such as robotics and simulation.

# References

## Recommended textbooks
- Piegl, L., Tiller, W. *The NURBS Book.*
- Farin, G. *Curves and Surfaces for CAGD.*
- Rogers, D. *An Introduction to NURBS.*
- Do Carmo, M. *Differential Geometry of Curves and Surfaces* (selected sections)

## Engineering and CAD perspective
- Hoschek, J., Lasser, D. *Fundamentals of Computer Aided Geometric Design.*


## 
- 10.14658/PUPJ-DRNA-2024-3-9


## Assessment
- Multiple Choice Test on Theoretical Concepts (individual) - Accounting for 30\%
- Final project (team or individual) - Accounting for 70\%
