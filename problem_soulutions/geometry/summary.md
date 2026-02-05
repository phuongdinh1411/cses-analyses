---
layout: simple
title: "Geometry Summary"
permalink: /problem_soulutions/geometry/summary
---

# Geometry

Welcome to the Geometry section! This category covers computational geometry algorithms and techniques for solving geometric problems.

## Key Concepts & Techniques

### Basic Geometry Operations

#### Points and Vectors
- **Point Representation**: (x, y) coordinates
  - *When to use*: Representing positions in 2D space
  - *Implementation*: Use pairs or structs with x, y coordinates
  - *Applications*: All geometric problems, coordinate systems
- **Vector Operations**: Addition, subtraction, scaling
  - *When to use*: Representing directions and displacements
  - *Implementation*: Component-wise operations
  - *Applications*: Movement, transformations, calculations
- **Distance Calculations**: Euclidean, Manhattan, Chebyshev
  - *When to use*: Measuring distances between points
  - *Implementation*: sqrt((x2-x1)² + (y2-y1)²) for Euclidean
  - *Applications*: Closest pair, path planning, optimization

#### Line and Segment Operations
- **Line Representation**: Point-slope, two-point, general form
  - *When to use*: Representing lines in 2D space
  - *Implementation*: ax + by + c = 0 or y = mx + b
  - *Applications*: Line intersection, point-line distance
- **Line Segment Intersection**: Check if segments intersect
  - *When to use*: When you need to check if two segments cross
  - *Implementation*: Use cross product to check orientation
  - *Applications*: Collision detection, path planning
- **Point-Line Distance**: Distance from point to line
  - *When to use*: When you need distance from point to line
  - *Implementation*: |ax + by + c| / sqrt(a² + b²)
  - *Applications*: Closest point, projection, optimization

### Geometric Primitives

#### Cross Product
- **2D Cross Product**: Determinant of 2x2 matrix
  - *When to use*: Orientation, area, perpendicular vectors
  - *Implementation*: (x1*y2 - x2*y1) for vectors (x1,y1), (x2,y2)
  - *Applications*: Convex hull, line intersection, area calculation
- **Orientation Test**: Clockwise, counterclockwise, collinear
  - *When to use*: Determining relative positions of points
  - *Implementation*: Sign of cross product
  - *Applications*: Convex hull, point in polygon, line intersection

#### Dot Product
- **2D Dot Product**: Sum of component products
  - *When to use*: Projection, angle calculation, perpendicularity
  - *Implementation*: x1*x2 + y1*y2 for vectors (x1,y1), (x2,y2)
  - *Applications*: Angle between vectors, projection, optimization
- **Angle Calculation**: Between two vectors
  - *When to use*: When you need angle between vectors
  - *Implementation*: acos(dot / (|v1| * |v2|))
  - *Applications*: Rotation, orientation, optimization

#### Area Calculations
- **Triangle Area**: Using cross product
  - *When to use*: When you need area of triangle
  - *Implementation*: |cross_product| / 2
  - *Applications*: Polygon area, point in polygon, optimization
- **Polygon Area**: Shoelace formula
  - *When to use*: When you need area of polygon
  - *Implementation*: Sum of cross products / 2
  - *Applications*: Area calculation, point in polygon, optimization

### Advanced Geometric Algorithms

#### Convex Hull
- **Graham Scan**: Sort by angle, then scan
  - *When to use*: When you need convex hull of points
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Optimization, collision detection, path planning
- **Andrew's Algorithm**: Sort by coordinates, then scan
  - *When to use*: Alternative to Graham scan
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Convex hull, optimization, geometric algorithms
- **Quick Hull**: Divide and conquer approach
  - *When to use*: When you need fast convex hull
  - *Time*: O(n log n) average, O(n²) worst case
  - *Space*: O(n)
  - *Applications*: Convex hull, optimization, geometric algorithms

#### Closest Pair of Points
- **Divide and Conquer**: Split points, solve recursively
  - *When to use*: When you need closest pair of points
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Optimization, collision detection, path planning
- **Sweep Line**: Process points in order
  - *When to use*: Alternative to divide and conquer
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Closest pair, geometric algorithms

#### Line Intersection
- **All Intersections**: Find all line intersections
  - *When to use*: When you need all intersections
  - *Time*: O(n log n + k) where k is number of intersections
  - *Space*: O(n + k)
  - *Applications*: Line arrangement, geometric algorithms
- **Sweep Line**: Process line events
  - *When to use*: When you need efficient line intersection
  - *Time*: O(n log n + k)
  - *Space*: O(n)
  - *Applications*: Line intersection, geometric algorithms

### Point Location and Containment

#### Point in Polygon
- **Ray Casting**: Cast ray and count intersections
  - *When to use*: When you need to check if point is in polygon
  - *Time*: O(n) where n is number of vertices
  - *Space*: O(1)
  - *Applications*: Point location, collision detection, optimization
- **Winding Number**: Sum of angles
  - *When to use*: Alternative to ray casting
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Point location, geometric algorithms

#### Point Location in Line Arrangement
- **Binary Search**: Search in sorted line arrangement
  - *When to use*: When you need to locate point in line arrangement
  - *Time*: O(log n) per query
  - *Space*: O(n²)
  - *Applications*: Point location, geometric algorithms
- **Sweep Line**: Process events in order
  - *When to use*: When you need efficient point location
  - *Time*: O(n log n + q log n) where q is number of queries
  - *Space*: O(n)
  - *Applications*: Point location, geometric algorithms

### Specialized Geometric Techniques

#### Sweep Line Algorithm
- **Event Processing**: Process events in order
  - *When to use*: When you need to process geometric events
  - *Time*: O(n log n + k) where k is number of events
  - *Space*: O(n)
  - *Applications*: Line intersection, closest pair, geometric algorithms
- **Status Maintenance**: Maintain current status
  - *When to use*: When you need to maintain current state
  - *Implementation*: Use balanced tree or segment tree
  - *Applications*: Sweep line, geometric algorithms

#### Binary Search on Answer
- **Geometric Binary Search**: Search on geometric properties
  - *When to use*: When you need to find optimal geometric value
  - *Time*: O(log n) per search
  - *Space*: O(1)
  - *Applications*: Optimization, geometric algorithms
- **Monotonic Properties**: When function is monotonic
  - *When to use*: When geometric property is monotonic
  - *Implementation*: Binary search with geometric check
  - *Applications*: Optimization, geometric algorithms

#### Coordinate Compression
- **Discrete Coordinates**: Map to smaller range
  - *When to use*: When coordinates are large or sparse
  - *Time*: O(n log n) preprocessing
  - *Space*: O(n)
  - *Applications*: Large coordinate spaces, geometric algorithms
- **Grid Mapping**: Map to grid
  - *When to use*: When you need to map to grid
  - *Implementation*: Sort and map to indices
  - *Applications*: Grid-based algorithms, geometric algorithms

### Optimization Techniques

#### Precision Handling
- **Floating Point**: Use appropriate precision
  - *When to use*: When you need floating point calculations
  - *Implementation*: Use double or long double
  - *Applications*: All geometric calculations
- **Integer Coordinates**: Use integer arithmetic
  - *When to use*: When coordinates are integers
  - *Implementation*: Use integer arithmetic with cross product
  - *Applications*: Grid-based problems, exact calculations
- **Epsilon Comparison**: Handle floating point errors
  - *When to use*: When comparing floating point numbers
  - *Implementation*: Use small epsilon for comparison
  - *Applications*: Floating point comparisons, geometric algorithms

#### Space Optimization
- **In-place Algorithms**: Modify data in place
  - *When to use*: When memory is limited
  - *Example*: In-place convex hull, in-place sorting
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy geometric calculations, on-demand computation

#### Time Optimization
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute distances, precompute angles
- **Caching**: Store computed results
  - *When to use*: When calculations are expensive
  - *Example*: Cache geometric calculations, cache intersections

## Problem Categories

### Basic Geometry
- [Point Location Test](point_location_test_analysis) - Point position relative to line
- [Line Segment Intersection](line_segment_intersection_analysis) - Finding intersection points
- [Polygon Area](polygon_area_analysis) - Computing polygon area

### Distance and Location
- [Minimum Euclidean Distance](minimum_euclidean_distance_analysis) - Closest pair of points
- [Maximum Manhattan Distance](maximum_manhattan_distance_analysis) - Maximum Manhattan distance
- [All Manhattan Distances](all_manhattan_distances_analysis) - All Manhattan distances
- [Point in Polygon](point_in_polygon_analysis) - Point containment test

### Line and Segment Operations
- [Line Segments Trace](line_segments_trace_analysis) - Following line segments
- [Lines and Queries I](lines_and_queries_i_analysis) - Basic line queries
- [Lines and Queries II](lines_and_queries_ii_analysis) - Advanced line queries

### Advanced Geometry
- [Convex Hull](convex_hull_analysis) - Graham scan algorithm
- [Polygon Lattice Points](polygon_lattice_points_analysis) - Points with integer coordinates
- [Intersection Points](intersection_points_analysis) - All intersection points
- [Robot Path](robot_path_analysis) - Path planning
- [Area of Rectangles](area_of_rectangles_analysis) - Union of rectangles

## Detailed Examples and Implementations

### Classic Geometry Algorithms with Code

#### 1. Basic Geometric Primitives
```python
import math
from typing import List, Tuple, Optional

class Point:
  def __init__(self, x: float, y: float):
    self.x = x
    self.y = y
  
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)
  
  def __mul__(self, scalar):
    return Point(self.x * scalar, self.y * scalar)
  
  def __repr__(self):
    return f"Point({self.x}, {self.y})"

def distance(p1: Point, p2: Point) -> float:
  """Calculate Euclidean distance between two points"""
  return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def manhattan_distance(p1: Point, p2: Point) -> float:
  """Calculate Manhattan distance between two points"""
  return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def chebyshev_distance(p1: Point, p2: Point) -> float:
  """Calculate Chebyshev distance between two points"""
  return max(abs(p1.x - p2.x), abs(p1.y - p2.y))

def dot_product(p1: Point, p2: Point) -> float:
  """Calculate dot product of two vectors"""
  return p1.x * p2.x + p1.y * p2.y

def cross_product(p1: Point, p2: Point) -> float:
  """Calculate cross product of two vectors (2D)"""
  return p1.x * p2.y - p1.y * p2.x

def orientation(p1: Point, p2: Point, p3: Point) -> int:
  """Determine orientation of three points"""
  val = cross_product(p2 - p1, p3 - p1)
  if abs(val) < 1e-9:
    return 0  # Collinear
  return 1 if val > 0 else -1  # Counterclockwise or clockwise

def angle_between_vectors(v1: Point, v2: Point) -> float:
  """Calculate angle between two vectors in radians"""
  cos_angle = dot_product(v1, v2) / (distance(Point(0, 0), v1) * distance(Point(0, 0), v2))
  return math.acos(max(-1, min(1, cos_angle)))  # Clamp to avoid numerical errors
```

#### 2. Line and Segment Operations
```python
class Line:
  def __init__(self, p1: Point, p2: Point):
    self.p1 = p1
    self.p2 = p2
    self.direction = p2 - p1
  
  def slope(self) -> Optional[float]:
    """Calculate slope of line"""
    if abs(self.direction.x) < 1e-9:
      return None  # Vertical line
    return self.direction.y / self.direction.x
  
  def y_intercept(self) -> Optional[float]:
    """Calculate y-intercept of line"""
    slope = self.slope()
    if slope is None:
      return None  # Vertical line
    return self.p1.y - slope * self.p1.x

def line_intersection(line1: Line, line2: Line) -> Optional[Point]:
  """Find intersection point of two lines"""
  denom = cross_product(line1.direction, line2.direction)
  if abs(denom) < 1e-9:
    return None  # Parallel lines
  
  t = cross_product(line2.p1 - line1.p1, line2.direction) / denom
  return line1.p1 + line1.direction * t

def segment_intersection(seg1: Line, seg2: Line) -> Optional[Point]:
  """Find intersection point of two line segments"""
  # Check if segments are parallel
  denom = cross_product(seg1.direction, seg2.direction)
  if abs(denom) < 1e-9:
    # Check if segments are collinear and overlapping
    if abs(cross_product(seg2.p1 - seg1.p1, seg1.direction)) < 1e-9:
      # Segments are collinear, check for overlap
      t1 = dot_product(seg2.p1 - seg1.p1, seg1.direction) / dot_product(seg1.direction, seg1.direction)
      t2 = dot_product(seg2.p2 - seg1.p1, seg1.direction) / dot_product(seg1.direction, seg1.direction)
      t_min, t_max = min(t1, t2), max(t1, t2)
      if t_max >= 0 and t_min <= 1:
        return seg1.p1 + seg1.direction * max(0, t_min)
    return None
  
  t1 = cross_product(seg2.p1 - seg1.p1, seg2.direction) / denom
  t2 = cross_product(seg1.p1 - seg2.p1, seg1.direction) / (-denom)
  
  if 0 <= t1 <= 1 and 0 <= t2 <= 1:
    return seg1.p1 + seg1.direction * t1
  
  return None

def point_to_line_distance(point: Point, line: Line) -> float:
  """Calculate distance from point to line"""
  return abs(cross_product(line.direction, point - line.p1)) / distance(Point(0, 0), line.direction)

def point_to_segment_distance(point: Point, segment: Line) -> float:
  """Calculate distance from point to line segment"""
  t = dot_product(point - segment.p1, segment.direction) / dot_product(segment.direction, segment.direction)
  t = max(0, min(1, t))  # Clamp to segment
  closest_point = segment.p1 + segment.direction * t
  return distance(point, closest_point)
```

#### 3. Polygon Operations
```python
def polygon_area(points: List[Point]) -> float:
  """Calculate area of polygon using shoelace formula"""
  n = len(points)
  if n < 3:
    return 0
  
  area = 0
  for i in range(n):
    j = (i + 1) % n
    area += points[i].x * points[j].y
    area -= points[j].x * points[i].y
  
  return abs(area) / 2

def polygon_perimeter(points: List[Point]) -> float:
  """Calculate perimeter of polygon"""
  n = len(points)
  if n < 2:
    return 0
  
  perimeter = 0
  for i in range(n):
    j = (i + 1) % n
    perimeter += distance(points[i], points[j])
  
  return perimeter

def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
  """Check if point is inside polygon using ray casting"""
  n = len(polygon)
  if n < 3:
    return False
  
  inside = False
  j = n - 1
  
  for i in range(n):
    pi, pj = polygon[i], polygon[j]
    
    if ((pi.y > point.y) != (pj.y > point.y)) and \
     (point.x < (pj.x - pi.x) * (point.y - pi.y) / (pj.y - pi.y) + pi.x):
      inside = not inside
    j = i
  
  return inside

def point_in_polygon_winding(point: Point, polygon: List[Point]) -> bool:
  """Check if point is inside polygon using winding number"""
  n = len(polygon)
  if n < 3:
    return False
  
  winding_number = 0
  for i in range(n):
    p1, p2 = polygon[i], polygon[(i + 1) % n]
    
    if p1.y <= point.y:
      if p2.y > point.y and orientation(p1, p2, point) > 0:
        winding_number += 1
    else:
      if p2.y <= point.y and orientation(p1, p2, point) < 0:
        winding_number -= 1
  
  return winding_number != 0

def is_convex_polygon(polygon: List[Point]) -> bool:
  """Check if polygon is convex"""
  n = len(polygon)
  if n < 3:
    return False
  
  prev_orientation = 0
  for i in range(n):
    p1, p2, p3 = polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n]
    curr_orientation = orientation(p1, p2, p3)
    
    if curr_orientation == 0:
      continue  # Collinear points
    
    if prev_orientation == 0:
      prev_orientation = curr_orientation
    elif prev_orientation != curr_orientation:
      return False
  
  return True
```

#### 4. Convex Hull Algorithms
```python
def graham_scan(points: List[Point]) -> List[Point]:
  """Find convex hull using Graham scan"""
  n = len(points)
  if n < 3:
    return points
  
  # Find bottom-most point (and leftmost in case of tie)
  start = min(points, key=lambda p: (p.y, p.x))
  
  # Sort points by polar angle with respect to start point
  def polar_angle(p):
    return math.atan2(p.y - start.y, p.x - start.x)
  
  sorted_points = sorted([p for p in points if p != start], key=polar_angle)
  hull = [start]
  
  for point in sorted_points:
    # Remove points that create clockwise turn
    while len(hull) > 1 and orientation(hull[-2], hull[-1], point) <= 0:
      hull.pop()
    hull.append(point)
  
  return hull

def jarvis_march(points: List[Point]) -> List[Point]:
  """Find convex hull using Jarvis march (Gift wrapping)"""
  n = len(points)
  if n < 3:
    return points
  
  # Find leftmost point
  leftmost = min(points, key=lambda p: p.x)
  hull = [leftmost]
  
  current = leftmost
  while True:
    next_point = points[0]
    for point in points:
      if point == current:
        continue
      
      # Find point that makes leftmost turn
      if (next_point == current or 
        orientation(current, next_point, point) < 0):
        next_point = point
    
    if next_point == leftmost:
      break
    
    hull.append(next_point)
    current = next_point
  
  return hull

def andrew_monotone_chain(points: List[Point]) -> List[Point]:
  """Find convex hull using Andrew's monotone chain algorithm"""
  n = len(points)
  if n < 3:
    return points
  
  # Sort points by x-coordinate (and y-coordinate in case of tie)
  points.sort(key=lambda p: (p.x, p.y))
  
  def build_hull(points):
    hull = []
    for point in points:
      while len(hull) > 1 and orientation(hull[-2], hull[-1], point) <= 0:
        hull.pop()
      hull.append(point)
    return hull
  
  # Build lower hull
  lower_hull = build_hull(points)
  
  # Build upper hull
  upper_hull = build_hull(reversed(points))
  
  # Remove duplicate points
  return lower_hull[:-1] + upper_hull[:-1]
```

### Advanced Geometry Techniques

#### 1. Closest Pair of Points
```python
def closest_pair_divide_conquer(points: List[Point]) -> Tuple[float, Point, Point]:
  """Find closest pair of points using divide and conquer"""
  def closest_pair_rec(px, py):
    n = len(px)
    if n <= 3:
      return brute_force_closest_pair(px)
    
    mid = n // 2
    mid_point = px[mid]
    
    pyl = [p for p in py if p.x <= mid_point.x]
    pyr = [p for p in py if p.x > mid_point.x]
    
    dl, pl1, pl2 = closest_pair_rec(px[:mid], pyl)
    dr, pr1, pr2 = closest_pair_rec(px[mid:], pyr)
    
    d = min(dl, dr)
    if d == dl:
      min_dist, p1, p2 = dl, pl1, pl2
    else:
      min_dist, p1, p2 = dr, pr1, pr2
    
    # Check strip
    strip = [p for p in py if abs(p.x - mid_point.x) < d]
    
    for i in range(len(strip)):
      j = i + 1
      while j < len(strip) and strip[j].y - strip[i].y < d:
        dist = distance(strip[i], strip[j])
        if dist < min_dist:
          min_dist = dist
          p1, p2 = strip[i], strip[j]
        j += 1
    
    return min_dist, p1, p2
  
  px = sorted(points, key=lambda p: p.x)
  py = sorted(points, key=lambda p: p.y)
  return closest_pair_rec(px, py)

def brute_force_closest_pair(points: List[Point]) -> Tuple[float, Point, Point]:
  """Brute force closest pair for small sets"""
  n = len(points)
  min_dist = float('inf')
  p1, p2 = None, None
  
  for i in range(n):
    for j in range(i + 1, n):
      dist = distance(points[i], points[j])
      if dist < min_dist:
        min_dist = dist
        p1, p2 = points[i], points[j]
  
  return min_dist, p1, p2
```

#### 2. Line Sweep Algorithms
```python
class Event:
  def __init__(self, x: float, event_type: str, segment: Line, index: int):
    self.x = x
    self.event_type = event_type  # 'start', 'end', 'intersection'
    self.segment = segment
    self.index = index
  
  def __lt__(self, other):
    if abs(self.x - other.x) < 1e-9:
      # Handle events at same x-coordinate
      order = {'start': 0, 'intersection': 1, 'end': 2}
      return order[self.event_type] < order[other.event_type]
    return self.x < other.x

def find_all_intersections(segments: List[Line]) -> List[Point]:
  """Find all intersection points using line sweep"""
  events = []
  for i, segment in enumerate(segments):
    start_x = min(segment.p1.x, segment.p2.x)
    end_x = max(segment.p1.x, segment.p2.x)
    events.append(Event(start_x, 'start', segment, i))
    events.append(Event(end_x, 'end', segment, i))
  
  events.sort()
  active_segments = []
  intersections = []
  
  for event in events:
    if event.event_type == 'start':
      # Add segment to active set
      active_segments.append(event.segment)
      # Check for intersections with other active segments
      for other_segment in active_segments[:-1]:
        intersection = segment_intersection(event.segment, other_segment)
        if intersection:
          intersections.append(intersection)
    
    elif event.event_type == 'end':
      # Remove segment from active set
      active_segments.remove(event.segment)
  
  return intersections

def rectangle_union_area(rectangles: List[Tuple[Point, Point]]) -> float:
  """Calculate area of union of rectangles using line sweep"""
  events = []
  for i, (p1, p2) in enumerate(rectangles):
    events.append((p1.x, 'start', p1.y, p2.y, i))
    events.append((p2.x, 'end', p1.y, p2.y, i))
  
  events.sort()
  active_intervals = []
  total_area = 0
  prev_x = None
  
  for x, event_type, y1, y2, rect_id in events:
    if prev_x is not None and x > prev_x:
      # Calculate area covered by active intervals
      active_intervals.sort()
      merged_intervals = []
      
      for start, end in active_intervals:
        if not merged_intervals or start > merged_intervals[-1][1]:
          merged_intervals.append([start, end])
        else:
          merged_intervals[-1][1] = max(merged_intervals[-1][1], end)
      
      width = x - prev_x
      height = sum(end - start for start, end in merged_intervals)
      total_area += width * height
    
    if event_type == 'start':
      active_intervals.append([y1, y2])
    else:
      active_intervals.remove([y1, y2])
    
    prev_x = x
  
  return total_area
```

#### 3. Voronoi Diagrams and Delaunay Triangulation
```python
class VoronoiCell:
  def __init__(self, site: Point):
    self.site = site
    self.edges = []
    self.vertices = []

def voronoi_diagram(points: List[Point]) -> List[VoronoiCell]:
  """Simple Voronoi diagram using perpendicular bisectors"""
  cells = [VoronoiCell(point) for point in points]
  
  for i, cell in enumerate(cells):
    for j, other_cell in enumerate(cells):
      if i == j:
        continue
      
      # Find perpendicular bisector
      mid_point = Point((cell.site.x + other_cell.site.x) / 2,
              (cell.site.y + other_cell.site.y) / 2)
      
      # Direction perpendicular to line between sites
      direction = Point(-(other_cell.site.y - cell.site.y),
              other_cell.site.x - cell.site.x)
      
      # Normalize direction
      length = distance(Point(0, 0), direction)
      if length > 1e-9:
        direction = Point(direction.x / length, direction.y / length)
      
      # Create edge (simplified)
      edge_start = Point(mid_point.x - direction.x * 1000,
              mid_point.y - direction.y * 1000)
      edge_end = Point(mid_point.x + direction.x * 1000,
             mid_point.y + direction.y * 1000)
      
      cell.edges.append(Line(edge_start, edge_end))
  
  return cells

def delaunay_triangulation(points: List[Point]) -> List[Tuple[Point, Point, Point]]:
  """Simple Delaunay triangulation (incremental algorithm)"""
  if len(points) < 3:
    return []
  
  # Sort points by x-coordinate
  points.sort(key=lambda p: p.x)
  
  triangles = []
  
  # Start with first triangle
  if len(points) >= 3:
    triangles.append((points[0], points[1], points[2]))
  
  # Add remaining points
  for i in range(3, len(points)):
    point = points[i]
    bad_triangles = []
    
    # Find triangles whose circumcircle contains the new point
    for triangle in triangles:
      if point_in_circumcircle(point, triangle):
        bad_triangles.append(triangle)
    
    # Find boundary of polygonal hole
    polygon = []
    for triangle in bad_triangles:
      for edge in [(triangle[0], triangle[1]), 
            (triangle[1], triangle[2]), 
            (triangle[2], triangle[0])]:
        # Check if edge is shared with another bad triangle
        shared = False
        for other_triangle in bad_triangles:
          if other_triangle == triangle:
            continue
          if edge in [(other_triangle[0], other_triangle[1]),
               (other_triangle[1], other_triangle[2]),
               (other_triangle[2], other_triangle[0])] or \
           (edge[1], edge[0]) in [(other_triangle[0], other_triangle[1]),
                      (other_triangle[1], other_triangle[2]),
                      (other_triangle[2], other_triangle[0])]:
            shared = True
            break
        
        if not shared:
          polygon.append(edge)
    
    # Remove bad triangles
    for triangle in bad_triangles:
      triangles.remove(triangle)
    
    # Add new triangles
    for edge in polygon:
      triangles.append((edge[0], edge[1], point))
  
  return triangles

def point_in_circumcircle(point: Point, triangle: Tuple[Point, Point, Point]) -> bool:
  """Check if point is inside circumcircle of triangle"""
  p1, p2, p3 = triangle
  
  # Calculate circumcircle center and radius
  ax, ay = p1.x, p1.y
  bx, by = p2.x, p2.y
  cx, cy = p3.x, p3.y
  
  d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
  if abs(d) < 1e-9:
    return False  # Degenerate triangle
  
  ux = ((ax * ax + ay * ay) * (by - cy) + 
     (bx * bx + by * by) * (cy - ay) + 
     (cx * cx + cy * cy) * (ay - by)) / d
  
  uy = ((ax * ax + ay * ay) * (cx - bx) + 
     (bx * bx + by * by) * (ax - cx) + 
     (cx * cx + cy * cy) * (bx - ax)) / d
  
  center = Point(ux, uy)
  radius = distance(center, p1)
  
  return distance(point, center) < radius
```

## Tips for Success

1. **Master Vector Operations**: Essential for geometry
2. **Handle Precision**: Use appropriate types
3. **Learn Sweep Line**: Important technique
4. **Practice Implementation**: Code geometric primitives
5. **Study Advanced Algorithms**: Convex hull, closest pair, etc.
6. **Handle Edge Cases**: Degenerate cases, precision issues

## Common Pitfalls to Avoid

1. **Floating Point Errors**: Precision issues
2. **Degenerate Cases**: Special configurations
3. **Orientation Errors**: Wrong direction
4. **Boundary Cases**: Edge point handling

## Advanced Topics

### Computational Geometry
- **Convex Hull Algorithms**: Different approaches
- **Voronoi Diagrams**: Space partitioning
- **Delaunay Triangulation**: Optimal triangulation
- **Line Arrangements**: Multiple lines

### Optimization Techniques
- **Sweep Line**: Event processing
- **Binary Search**: On geometric properties
- **Divide and Conquer**: Geometric partitioning
- **Dynamic Updates**: Online geometry

### Special Cases
- **Collinear Points**: Points on line
- **Parallel Lines**: No intersection
- **Overlapping Segments**: Multiple intersections
- **Integer Coordinates**: Grid points

## Algorithm Complexities

### Basic Operations
- **Point Location**: O(1) time
- **Line Intersection**: O(1) time
- **Polygon Area**: O(n) time
- **Point in Polygon**: O(n) time

### Advanced Operations
- **Convex Hull**: O(n log n) time
- **All Intersections**: O(n log n + k) time
- **Closest Pair**: O(n log n) time
- **Rectangle Union**: O(n log n) time

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[Math and Geometry Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential mathematical and geometric problem patterns
- **[Advanced Algorithm Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Complex algorithmic techniques and optimization strategies

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce geometry and mathematical concepts:

- **Geometric Algorithms**: [Valid Square](https://leetcode.com/problems/valid-square/), [Rectangle Overlap](https://leetcode.com/problems/rectangle-overlap/), [Convex Polygon](https://leetcode.com/problems/convex-polygon/)
- **Mathematical Problems**: [Pow(x, n)](https://leetcode.com/problems/powx-n/), [Sqrt(x)](https://leetcode.com/problems/sqrtx/), [Perfect Squares](https://leetcode.com/problems/perfect-squares/)
- **Coordinate Geometry**: [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/), [Minimum Area Rectangle](https://leetcode.com/problems/minimum-area-rectangle/)
- **Advanced Math**: [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/), [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

---

Ready to start? Begin with [Point Location Test](point_location_test_analysis) and work your way through the problems in order of difficulty!