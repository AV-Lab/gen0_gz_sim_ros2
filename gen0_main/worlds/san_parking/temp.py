import os

def change_texture_paths(mtl_file, textures_folder):
    new_mtl_lines = []
    mtl_folder = os.path.dirname(mtl_file)
    # Calculate the relative path from the .mtl folder to the textures folder
    rel_textures_folder = os.path.relpath(textures_folder, mtl_folder)
    
    with open(mtl_file, 'r') as f:
        for line in f:
            if line.startswith('map_Kd'):
                # Extracting the texture file name
                _, texture_path = line.strip().split(maxsplit=1)
                # Constructing the new relative path
                new_texture_path = os.path.join(rel_textures_folder, os.path.basename(texture_path))
                new_line = f'map_Kd {new_texture_path}\n'
                new_mtl_lines.append(new_line)
            else:
                new_mtl_lines.append(line)

    # Writing the modified MTL file
    with open(mtl_file, 'w') as f:
        f.writelines(new_mtl_lines)

# Example usage:
mtl_file = 'san_parking.mtl'
textures_folder = '../textures'  # Adjust the relative path to textures folder as needed
change_texture_paths(mtl_file, textures_folder)

