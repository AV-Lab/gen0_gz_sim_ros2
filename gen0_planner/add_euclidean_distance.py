import json
import math

# Function to calculate the Euclidean distance between two points
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Read the JSON file
with open('station1.json', 'r') as file:
    data = json.load(file)

# Initialize the previous point
previous_point = None

# Process each point in the list
for i, point in enumerate(data):
    if i == 0:
        # First point, e_distance is 0
        point.insert(4, 0.0)
    else:
        # Calculate the distance from the previous point
        x1, y1 = previous_point[0], previous_point[1]
        x2, y2 = point[0], point[1]
        e_distance = euclidean_distance(x1, y1, x2, y2)
        # Format the distance to 4 decimal points
        e_distance = round(e_distance, 4)
        point.insert(4, e_distance)
    
    # Update the previous point
    previous_point = point

# Write the updated data back to a JSON file
with open('station1.json', 'w') as file:
    json.dump(data, file, indent=4)

