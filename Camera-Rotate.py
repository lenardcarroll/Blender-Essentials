'''
Python script for rotating the camera around a selected object
'''
import bpy
import mathutils
from math import radians

# User-defined parameters
axis = 'Z'  # Choose 'X', 'Y', 'Z', 'XY', 'XZ', 'YZ' or 'XYZ'
increments = 1  # Degrees increment for rotation
target_object = bpy.context.selected_objects[0]  # Assuming one object is selected

# Ensure exactly one object is selected
if len(bpy.context.selected_objects) != 1:
    raise ValueError("Please select exactly one object.")

# Create an empty object at the target object's location
empty = bpy.data.objects.new("Empty", None)
target_location = target_object.location
empty.location = target_location
bpy.context.collection.objects.link(empty)

# Use an existing camera in the scene
camera = None
for obj in bpy.context.scene.objects:
    if obj.type == 'CAMERA':
        camera = obj
        break

if camera is None:
    raise ValueError("No camera found in the scene. Please add a camera.")

# Calculate the initial offset of the camera from the target location
initial_offset = camera.location - empty.location

# Parent the camera to the empty object while preserving its current position
camera.parent = empty
camera.location = initial_offset

# Add a Track To constraint to the camera to ensure it always points at the target object
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = target_object
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Reset any existing rotation on the empty object
empty.rotation_euler = (0, 0, 0)

# Apply rotation to the empty object and keyframe it
num_steps = 360 // increments
for step in range(num_steps):
    angle = increments * step
    if axis == 'X':
        empty.rotation_euler[0] = radians(angle)
    elif axis == 'Y':
        empty.rotation_euler[1] = radians(angle)
    elif axis == 'Z':
        empty.rotation_euler[2] = radians(angle)
    elif axis == 'XY':
        empty.rotation_euler[0] = radians(angle)        
        empty.rotation_euler[1] = radians(angle)
    elif axis == 'XZ':
        empty.rotation_euler[0] = radians(angle)        
        empty.rotation_euler[2] = radians(angle)   
    elif axis == 'YZ':
        empty.rotation_euler[1] = radians(angle)        
        empty.rotation_euler[2] = radians(angle)        
    elif axis == 'XYZ':
        empty.rotation_euler[0] = radians(angle)     
        empty.rotation_euler[1] = radians(angle)              
        empty.rotation_euler[2] = radians(angle)               

    # Insert keyframes for the empty object's rotation
    empty.keyframe_insert(data_path="rotation_euler", frame=step + 1)

# Restore the initial state
bpy.context.view_layer.update()
