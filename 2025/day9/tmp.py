from shapely.geometry import Polygon

# Define the outer polygon
outer_polygon = Polygon([(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)])

# Define the inner polygon (completely inside)
inner_polygon_1 = Polygon([(1, 1), (1, 9), (9, 9), (9, 1), (1, 1)])

# Define another polygon (partially outside)
inner_polygon_2 = Polygon([(5, 5), (5, 12), (12, 12), (12, 5), (5, 5)])

# Define a polygon that shares a boundary
inner_polygon_3 = Polygon([(0, 0), (0, 5), (5, 5), (5, 0), (0, 0)])

# Check for containment
print(f"Does outer_polygon contain inner_polygon_1? {outer_polygon.contains(inner_polygon_1)}")
print(f"Does outer_polygon contain inner_polygon_2? {outer_polygon.contains(inner_polygon_2)}")
print(f"Does outer_polygon contain inner_polygon_3? {outer_polygon.contains(inner_polygon_3)}")