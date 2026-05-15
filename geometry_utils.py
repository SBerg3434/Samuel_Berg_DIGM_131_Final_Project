# --- geometry_utils.py ---
"""
geometry_utils.py -- Geometry creation functions 
for building_generator_tool.py.
===============================================================================
DIGM 131 - Week 6 | Author: Samuel Berg

Geometry utility functions for creating and manipulating 3D primitives.

This module provides helper functions that wrap maya.cmds geometry creation
with sensible defaults, automatic naming, and ground-plane alignment.

Usage:
    import geometry_utils as geo
    geo.create_floor(width=10, height=2, depth=8)
"""

import maya.cmds as cmds


def create_floor(
            width=50,
            height=1,
            depth=50):

    """Create a polygonal box with its base resting on the ground plane.

    Args:
        width (float): Size along the X axis.
        height (float): Size along the Y axis.
        depth (float): Size along the Z axis.

    Returns:
        str: The name of the created transform node.
    """

    #Create the floor with the given parameters and position it at ground level
    floor = cmds.polyCube(name="floor_01",
                width=width,
                height=height,
                depth=depth) [0]
    cmds.move(0, height/2.0, 0, floor)
    
    return floor

def create_walls(
            radius=36,
            height=30,
            thickness=2):
                
    """Create a four-sided polygonal pipe with its base resting on the ground plane.

    Args:
        radius (float): Radius of the pipe.
        height (float): Size along the Y axis.
        thickness (float): Thickness of the walls.

    Returns:
        str: The name of the created transform node.
    """
    
    #Create the walls with the given parameters, position them at ground level,
    #    and rotate them 45 degrees so they line up with the floor
    walls = cmds.polyPipe(name="wall_01",
                height=height,
                radius=radius,
                thickness=thickness,
                subdivisionsAxis=4)[0]
    cmds.move(0, height/4.0, 0, walls)
    cmds.rotate(0, 45, 0, walls)
    
    return walls
    
    
def create_window(name="window_pane_01",
            width=17,
            height=9,
            depth=4,
            pane_thickness=0.75,
            position=(0, 7.5, 25)):
                
    """Create two boxes, an interceptor to cut trhough the wall and one to be the window pane.

    Args:
        width (float): Size along the X axis.
        height (float): Size along the Y axis.
        depth (float): Size along the Z axis of the interceptor.
        pane_thickness: Size along the Z axis of the window pane.
        position (tuple): (x, y, z) The position of the interceptor and window pane.
    Returns:
        str: The name of the created transform node.
    """
    
    #Create and position the interceptor with the given parameters
    window_interceptor = cmds.polyCube(
                width=width,
                height=height,
                depth=depth)[0]
    cmds.move(position[0], 
                position[1], 
                position[2],
                window_interceptor)
    
    #Create and position the window pane with the given parameters
    window_pane = cmds.polyCube(name=name,
                width=width,
                height=height,
                depth=pane_thickness)[0]  
    cmds.move(position[0], 
                position[1], 
                position[2],
                window_pane)

    return (window_pane, window_interceptor)
 
    
def create_roof(
            width=50,
            roof_height=1,
            depth=50,
            radius=37,
            edge_height=4,
            thickness=2,
            position=(0, 16, 0)):
                
    """Create a polygonal box and a four-sided polygonal pipe.

    Args:
        width (float): Size along the X axis of the roof.
        roof_height (float): Size along the Y axis of the roof.
        depth (float): Size along the Z axis of the roof.
        radius (float): Radius of the edge pipe.
        edge_height (float): Size along the Y axis of the edge pipe.
        thickness (float): Thickness of the edge pipe.
        position (tuple): (x, y, z) Position of the full roof.

    Returns:
        str: The name of a group node containing the roof and roof ledge.
    """
    
    #Create the roof with the given parameters
    roof = cmds.polyCube(name="roof_01",
                width=width,
                height=roof_height,
                depth=depth) [0]
    
    #Create the roof edge with the given parameters and rotate them
    #    45 degrees so they line up with the rest of the building
    roof_edge = cmds.polyPipe(name="roof_edge_01",
                height=edge_height,
                radius=radius,
                thickness=thickness,
                subdivisionsAxis=4)[0]
    cmds.rotate(0, 45, 0, roof_edge)
    
    #Group the roof and roof edge together
    #    and position the group with the given parameters
    roof_full = cmds.group(roof, roof_edge, name="roof_full_01")
    cmds.move(position[0], 
                position[1], 
                position[2],
                roof_full)
                
    return roof_full
    
                  
if __name__ == "__main__":
    #Self-test: runs only when executed directly
    cmds.file(new=True, force=True)
    create_floor()
    create_walls()
    create_window()
    create_roof()
    print("geometry_utils self-test: Success!")