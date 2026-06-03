import maya.cmds as cmds

#---------------------------------------
# Instructions
"""
This program will create a grid of cubes with height values driven by fractal noise values.
DO NOT EXCEED 50 FOR THE grid_size.
"""
#---------------------------------------
# Grid Resolution (DO NOT EXCEED 50)
grid_size = 25
spacing = 1.25
cube_size = 1.0
#---------------------------------------
# Grid (x, y, z)
for x in range(grid_size):
        for z in range(grid_size):
            # Create the cube
            cube = cmds.polyCube(w=cube_size, h=cube_size, d=cube_size)
     
            # Move the cube
            cmds.move(x * spacing, cube_size/2, z * spacing, cube)
