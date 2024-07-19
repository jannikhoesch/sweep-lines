from sortedcontainers import SortedList
import matplotlib.pyplot as plt
from AVLTree import AVLTree
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Segment:
    def __init__(self, p1, p2):
        if p1 < p2:
            self.start = p1
            self.end = p2
        else:
            self.start = p2
            self.end = p1

    def __lt__(self, other):
        if self.start.y != other.start.y:
            return self.start.y < other.start.y
        elif self.start.x != other.start.x:
            return self.start.x < other.start.x
        elif self.end.y != other.end.y:
            return self.end.y < other.end.y
        return self.end.x < other.end.x

    def __repr__(self):
        return f"Segment({self.start}, {self.end})"

    def get_y(self, x):
        return self.start.y + (self.end.y - self.start.y) * (x - self.start.x) / (
                self.end.x - self.start.x)


class Event:
    def __init__(self, point, type, segment, segment2=None):
        self.point = point
        self.type = type
        self.segment = segment
        self.segment2 = segment2

    def __lt__(self, other):
        if self.point.x != other.point.x:
            return self.point.x < other.point.x
        return self.point.y < other.point.y

    def __repr__(self):
        return f"Event({self.point}, {self.type}, {self.segment}, {self.segment2})"


def compute_intersection(s1, s2):
    x1, y1 = s1.start.x, s1.start.y
    x2, y2 = s1.end.x, s1.end.y
    x3, y3 = s2.start.x, s2.start.y
    x4, y4 = s2.end.x, s2.end.y

    # Calculate determinants
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    # Lines are parallel
    if den == 0:
        return None

    # Compute the intersection point
    num_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    num_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ix = num_x / den
    iy = num_y / den

    # Check if the computed point is within both segments
    if (min(x1, x2) <= ix <= max(x1, x2) and min(y1, y2) <= iy <= max(y1, y2) and
            min(x3, x4) <= ix <= max(x3, x4) and min(y3, y4) <= iy <= max(y3, y4)):
        return Point(ix, iy)
    return None


def find_intersections(segments):
    # Initialize data structure to store events
    events = SortedList()
    for seg in segments:
        events.add(Event(seg.start, 'start', seg))
        events.add(Event(seg.end, 'end', seg))

    # Initialize data structure to store active segments
    active_segments = AVLTree()

    # Initialize list to store found intersections
    n_comp = 0
    intersection_points = []

    # Process events
    while events:

        # Get next event
        event = events.pop(0)

        if event.type == 'start':

            # Add segment to active segments and get index
            active_segments.insert(event.segment.start.y, event.segment)

            # Check for intersections with predecessor
            pre = active_segments.predecessor(event.segment.start.y)
            if pre:
                intersection = compute_intersection(event.segment, pre.value)
                n_comp += 1
                if intersection and intersection not in intersection_points:
                    intersection_points.append(intersection)
                    if intersection not in [e.point for e in events]:
                        events.add(Event(intersection, 'intersection', pre.value, event.segment))
            # Check for intersections with sucessor
            succ = active_segments.successor(event.segment.start.y)
            if succ:
                intersection = compute_intersection(event.segment, succ.value)
                n_comp += 1
                if intersection and intersection not in intersection_points:
                    intersection_points.append(intersection)
                    if intersection not in [e.point for e in events]:
                        events.add(Event(intersection, 'intersection', event.segment, succ.value))

        elif event.type == 'end':

            # Check for intersection between neighbours
            pre = active_segments.predecessor(event.segment.start.y)
            succ = active_segments.successor(event.segment.start.y)
            if pre and succ:
                intersection = compute_intersection(pre.value, succ.value)
                n_comp += 1
                if intersection and intersection not in intersection_points:
                    intersection_points.append(intersection)
                    if intersection not in [e.point for e in events]:
                        events.add(Event(intersection, 'intersection', pre.value, succ.value))

            # Remove from active segments
            active_segments.delete(event.segment.start.y)

        elif event.type == 'intersection':

            # Swap segments
            active_segments.delete(event.segment.start.y)
            active_segments.delete(event.segment2.start.y)
            seg1 = Segment(event.point, event.segment.end)
            seg2 = Segment(event.point, event.segment2.end)
            active_segments.insert(seg2.start.y, seg2)
            active_segments.insert(seg1.start.y, seg1)

            for e in events:
                if e.segment == event.segment:
                    e.segment = seg1
                if e.segment == event.segment2:
                    e.segment = seg2

            # Check for intersection with neighbours
            pre2 = active_segments.predecessor(seg2.start.y)
            if pre2:
                intersection = compute_intersection(seg2, pre2.value)
                n_comp += 1
                if intersection and intersection not in intersection_points:
                    intersection_points.append(intersection)
                    if intersection not in [e.point for e in events]:
                        events.add(Event(intersection, 'intersection', pre2.value, seg2))
            succ1 = active_segments.successor(seg1.start.y)
            if succ1:
                intersection = compute_intersection(seg1, succ1.value)
                n_comp += 1
                if intersection and intersection not in intersection_points:
                    intersection_points.append(intersection)
                    if intersection not in [e.point for e in events]:
                        events.add(Event(intersection, 'intersection', seg1, succ1.value))

    return intersection_points, n_comp


def find_naive(segments):
    n_comp = 0
    intersection_points = []
    for seg1 in segments:
        for seg2 in segments:
            if seg1 != seg2:
                intersect = compute_intersection(seg1, seg2)
                n_comp += 1
                if intersect:
                    intersection_points.append(intersect)
    return intersection_points, n_comp

#---------------------
# Functionality test
segments = [
    Segment(Point(0, 0), Point(5, 5)),
    Segment(Point(2, 1), Point(8, 1)),
    Segment(Point(0, 3), Point(3, 0)),
    Segment(Point(6, 2), Point(8, 0)),
    Segment(Point(2, 4), Point(6, 4)),
]

# Find intersections using sweep lines
intersections, _ = find_intersections(segments)

# Plot the segments and their intersections
plt.figure()
for segment in segments:
    plt.plot([segment.start.x, segment.end.x], [segment.start.y, segment.end.y], marker='o')
for intersect in intersections:
    plt.plot(intersect.x, intersect.y, 'ro')  # Mark intersection points
plt.title("Line Sweep Algorithm Visualized")
plt.grid(True)
plt.show()

#---------------------
# Time efficiency test
naive_times = []
sweep_times = []

naive_comp = []
sweep_comp = []

for n in range(1000, 10001, 1000):
    print(f'Run for size: {n}')

    # Create segments for the test
    segments = []

    # Create diagonal
    segments.append(Segment(Point(0, 0), Point(10000, 10000)))

    # Create horizontal lines
    for y in range(1, n + 1):
        segments.append(Segment(Point(y - 0.5, y), Point(y + 0.5, y)))

    # Measure naive approach
    start = time.time()
    _, n_naive = find_naive(segments)
    naive_times.append(time.time() - start)
    naive_comp.append(n_naive)

    # Measure sweep line approach
    start = time.time()
    _, n_sweep = find_intersections(segments)
    sweep_times.append(time.time() - start)
    sweep_comp.append(n_sweep)

# Plot times
plt.figure(figsize=(10, 6))
plt.plot(range(1000, 10001, 1000), naive_times, label='Naive Approach')
plt.plot(range(1000, 10001, 1000), sweep_times, label='Sweep Line Approach')
plt.xlabel('Number of Segments')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Comparison: Naive vs. Sweep Line')
plt.grid(True)
plt.legend()
plt.show()

# Plot comparisons
plt.figure(figsize=(10, 6))
plt.plot( naive_comp, label='Naive Approach')
plt.plot( sweep_comp, label='Sweep Line Approach')
plt.xlabel('Number of Segments')
plt.ylabel('Number of Comparisons')
plt.title('Performance Comparison: Naive vs. Sweep Line')
plt.grid(True)
plt.legend()
plt.show()

print(naive_times)
print(sweep_times)
