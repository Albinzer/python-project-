from itertools import permutations

# Distance dictionary (symmetric)
distances = {
    ("A", "B"): 5, ("A", "C"): 10, ("B", "C"): 3,
    ("A", "D"): 7, ("B", "D"): 2, ("C", "D"): 4
}

# Function to get distance regardless of order
def get_distance(city1, city2):
    return distances.get((city1, city2)) or distances.get((city2, city1))

# Cities list
cities = ["A", "B", "C", "D"]

# Variables to track best route
min_distance = float("inf")
best_route = None

# Brute force: try all possible permutations (routes)
for perm in permutations(cities[1:]):   # keep A fixed as start
    route = ("A",) + perm + ("A",)      # complete round trip
    total_distance = 0

    # Calculate distance for this route
    for i in range(len(route) - 1):
        total_distance += get_distance(route[i], route[i+1])

    # Print each route with distance
    print("Route:", route, "→ Distance:", total_distance)

    # Update best if shorter
    if total_distance < min_distance:
        min_distance = total_distance
        best_route = route

# Final result
print("\nBest route:", best_route)
print("Shortest distance:", min_distance)
