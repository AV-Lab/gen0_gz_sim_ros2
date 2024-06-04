import json
import math 

file_path = 'station1.json'
point_flag= 1.0
distance_threshold_v5_v0 = 8.33 # Vf^2=Vi^2 + 2* (a) * distance || 0 = 25 + 2 (-1.5) * distance
distance_threshold_v2_v0 = 1.33
# distance_threshold_v5_v2 =
desired_deceleration = -1.5

with open(file_path, 'r') as file:
    global_path = json.load(file)


for i in range(len(global_path)):
    if global_path[i][5] == point_flag:
        distance_threshold= (global_path[i][3]**2 - global_path[i-1][3]**2)/(2*desired_deceleration) # Vf^2=Vi^2 + 2* (a) * distance
        print(distance_threshold)

        cumulative_distance = 0 
        counter=0
        path_to_stop = []
        while cumulative_distance < distance_threshold:
            cumulative_distance += global_path[i-counter][4]
            counter += 1
        print(cumulative_distance)
        path_to_stop = global_path[i-counter:i+1]
        print(path_to_stop)
        velocities = []
        prev_Vf=0
        for j in range(1, len(path_to_stop)-1):
            Vi= path_to_stop[j-1][3] if j==1 else Vf
            # print(Vi**2 - (2*desired_deceleration * path_to_stop[j][4]))
            try:
                Vf= min(path_to_stop[j][3], math.sqrt(Vi**2 + (2*desired_deceleration * path_to_stop[j][4])))
                prev_Vf=Vf
            except:
                Vf=prev_Vf
            global_path[int(path_to_stop[j][6])][3] = Vf
            velocities.append(Vf)
            print(velocities)
        print("**")

with open('station11.json', 'w') as file:
    json.dump(global_path, file, indent=4)


