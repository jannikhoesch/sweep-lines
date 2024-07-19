# Sweep Line Algorithm

This repository contains a university project that I created for the course Advanced Data Structures at the Universitat Politècnica de Catalunya. The goal is to implement and analyze a sweep line algorithm to efficiently solve the segment intersection problem. 

## Introduction
The field of computational geometry focuses on the design and analysis of algorithms for solving geometric problems. Among these problems, one of the most fundamental and widely studied is the segment intersection problem. The ability to efficiently determine the intersection of different line segments is the basis for many applications, such as graphics rendering.

The segment intersection problem involves determining all the points at which two or more of a given set of line segments intersect. This problem can be particularly challenging when the data set is large, requiring the algorithm to be not only correct, but also highly efficient. The segments are defined in a two-dimensional plane, each represented by a pair of endpoints. The primary goal is to identify pairs of segments that intersect and the points at which these intersections occur. 

<img width="520" alt="image" src="https://github.com/user-attachments/assets/095807d3-faa3-4104-9f86-6072098ab45a">

The sweep line algorithm reduces the complexity of the problem by transforming the global geometric problem into a series of simpler, localized problems. This approach systematically processes events associated with segment endpoints, maintaining a dynamically updated set of active segments that have potential intersections with the sweep line - a vertical line that traverses the plane from left to right.

## Implementation
The Sweep Line algorithm operates by simulating a line that progressively scans across the plane from left to right. The starting and ending points of the line segments as well as segment intersection points are stored in a sorted event queue that is ordered by the x-coordinate of the points. Additionally, currently active segments are sorted by the y coordinate of their starting point in an AVL tree.

When a segment’s starting point is encountered, it is added to the active segments tree. The algorithm checks for potential intersections with its immediate predecessor and successor in the tree. When a segment’s ending point is encountered, it’s removed from the active segments tree. The algorithm checks for a potential intersection between its previous and following neighbor in the tree. If an intersection event is encountered, the intersecting segments are modified by swapping their position in the tree. Additionally, the algorithm checks for potential intersections between the modified segments and their new neighbors in the tree. If at any point intersections are found, they are added as new events to the sorted list for further processing. The specific implementation can be found in the file sweepLines.py. The solution assumes that no line segment of the input is vertical and that no three input segments intersect at the same point.

![image](https://github.com/user-attachments/assets/e7d15b1f-9d2c-4942-8916-461612b23940)

Compared to the naive approach that checks every segment pair for intersections, the Sweep Line algorithm avoids redundant computations by strategically processing events and using the sorted data structures. This approach offers significant efficiency gains, particularly for scenarios involving a large number of line segments, which I am going to test with the following experiments.

## Experiments
In order show the general functionality of my implementation I will test and visualize the algorithm on small problem sizes. For testing the time efficiency I am generating datasets containing a varying number n of line segments (100 to 10000, in steps of 100). For simplification and to purposely show the strengths of the Sweep Line Algorithm I will generate for each problem size a diagonal line that is intersected by n horizontal lines at the intersection point (i;i) for the i-th line. Each line will span from (i-0.5; i) to (i+0.5; i), in order to enable the Sweep Line Algorithm to efficiently delete inactive line segments from the tree and make only necessary comparisons. For each size n I will measure the total execution time for both approaches and additionally the amount of comparisons between segments.

## Observations
First, I showcase the ability of my sweep line implementation to correctly identify intersections from a set of line segments as shown in the first plot. By the algorithm identified intersections are marked in red.

<img width="566" alt="image" src="https://github.com/user-attachments/assets/aeab4290-15b8-4098-a3d4-21285f1095e6">

Next, I compare the performance of my sweep line implementation with a naive approach.

<img width="586" alt="image" src="https://github.com/user-attachments/assets/f1cf33d7-f26b-454d-98eb-48ddaf767f02">

Both time complexities seem to be quadratic, however, my implementation needs significantly less time the bigger the problem size. Although the expected growth rate for a Sweep Line method should be near-logarithmic with O(n logn), my solution seems to not reach the expected behaviour.

I am further researching the number of comparisons needed by each method to
ensure that my algorithm is really reducing the amount of comparisons.

<img width="627" alt="image" src="https://github.com/user-attachments/assets/b2db7f96-566a-4612-8805-e27897df0667">

Now it is visible, that indeed my implementation using Sweep Lines is significantly reducing the amount of comparisons. However, this seems to come with a cost of higher time effort at different points such as creating and updating the event queue and the AVL tree to store the active segments.

## Conclusion
My Sweep Line implementation successfully identified intersections and offered significant performance improvement over a naive approach in terms of segment comparisons. However, both exhibited a quadratic runtime, suggesting potential opti- mizations in event queue and AVL tree handling within the Sweep Line algorithm. Overall, the Sweep Line method demonstrates a substantial reduction in comparisons, making it a promising approach for handling line segment intersections.
