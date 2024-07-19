# Sweep Line Algorithm

This repository contains a university project that I created for the course Advanced Data Structures at the Universitat Politècnica de Catalunya. The goal is to implement and analyze a sweep line algorithm to efficiently solve the segment intersection problem. 

## Introduction
The field of computational geometry focuses on the design and analysis of algorithms for solving geometric problems. Among these problems, one of the most fundamental and widely studied is the segment intersection problem. The ability to efficiently determine the intersection of different line segments is the basis for many applications, such as graphics rendering.

The segment intersection problem involves determining all the points at which two or more of a given set of line segments intersect. This problem can be particularly challenging when the data set is large, requiring the algorithm to be not only correct, but also highly efficient. The segments are defined in a two-dimensional plane, each represented by a pair of endpoints. The primary goal is to identify pairs of segments that intersect and the points at which these intersections occur. 

The sweep line algorithm reduces the complexity of the problem by transforming the global geometric problem into a series of simpler, localized problems. This approach systematically processes events associated with segment endpoints, maintaining a dynamically updated set of active segments that have potential intersections with the sweep line - a vertical line that traverses the plane from left to right.

## Implementation
The Sweep Line algorithm operates by simulating a line that progressively scans across the plane from left to right. The starting and ending points of the line segments as well as segment intersection points are stored in a sorted event queue that is ordered by the x-coordinate of the points. Additionally, currently active segments are sorted by the y coordinate of their starting point in an AVL tree.

When a segment’s starting point is encountered, it is added to the active segments tree. The algorithm checks for potential intersections with its immediate predecessor and successor in the tree. When a segment’s ending point is encountered, it’s removed from the active segments tree. The algorithm checks for a potential intersection between its previous and following neighbor in the tree. If an intersection event is encountered, the intersecting segments are modified by swapping their position in the tree. Additionally, the algorithm checks for potential intersections between the
