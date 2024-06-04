import pandas as pd
import json

# Read the CSV file
csv_file_path = 'station2.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file_path)

# Select the columns x, y, yaw, and velocity
selected_columns = df[['x', 'y', 'yaw', 'velocity']]

# Add an index column starting from 0 as a float
selected_columns['index'] = range(len(selected_columns))
selected_columns['index'] = selected_columns['index'].astype(float)

# Add a c_flag column with default value 0
selected_columns['c_flag'] = 0

# Rearrange columns in the desired order
selected_columns = selected_columns[['x', 'y', 'yaw', 'velocity', 'c_flag', 'index']]

# Convert the DataFrame to a list of lists
data_list = selected_columns.values.tolist()

# Convert the list of lists to JSON format
json_output = json.dumps(data_list, indent=2)

# Print the JSON output
print(json_output)

# Optionally, you can save the JSON output to a file
with open('station2.json', 'w') as json_file:
    json_file.write(json_output)

