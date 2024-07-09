'''
Python script for the rotating an object and saving the rotations as .png files
'''
import bpy
import os

def get_corrected_path(path):
    if os.name == 'nt':  # Windows
        return path.replace("/", "\\")
    else:  # Unix-based systems (Linux, macOS)
        return path.replace("\\", "/")

# User-defined parameters
axis = 'Z'  # Choose 'X', 'Y', 'Z', 'XY', 'XZ', 'YZ' or 'XYZ'
increments = 10  # Degrees increment for rotation
output_dir = "F:\Blender\Save_Frames"  # Enter your absolute path here

# Correct the output directory path
output_dir = get_corrected_path(output_dir)

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Save the initial state
initial_rotation = {}
for obj in selected_objects:
    initial_rotation[obj.name] = obj.rotation_euler.copy()

# Rotate objects and save images
for angle in range(0, 360, increments):
    for obj in selected_objects:
        if axis == 'X':
            obj.rotation_euler[0] = angle * (3.14159265 / 180)
        elif axis == 'Y':
            obj.rotation_euler[1] = angle * (3.14159265 / 180)
        elif axis == 'Z':
            obj.rotation_euler[2] = angle * (3.14159265 / 180)
        elif axis == 'XZ':
            obj.rotation_euler[0] = angle * (3.14159265 / 180)
            obj.rotation_euler[2] = angle * (3.14159265 / 180)     
        elif axis == 'YZ':
            obj.rotation_euler[1] = angle * (3.14159265 / 180)
            obj.rotation_euler[2] = angle * (3.14159265 / 180)                   
        elif axis == 'XY':
            obj.rotation_euler[0] = angle * (3.14159265 / 180)
            obj.rotation_euler[1] = angle * (3.14159265 / 180) 
        elif axis == 'XYZ':
            obj.rotation_euler[0] = angle * (3.14159265 / 180)            
            obj.rotation_euler[1] = angle * (3.14159265 / 180)
            obj.rotation_euler[2] = angle * (3.14159265 / 180)             


    # Update the scene and render
    bpy.context.view_layer.update()
    bpy.ops.render.render(write_still=True)
    
    # Save the render
    output_path = os.path.join(output_dir, f'rotation_{axis}_{angle:03d}.png')
    bpy.data.images['Render Result'].save_render(filepath=output_path)

# Restore the initial rotation state
for obj in selected_objects:
    obj.rotation_euler = initial_rotation[obj.name]
