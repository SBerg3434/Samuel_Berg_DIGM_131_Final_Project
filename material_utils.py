# --- material_utils.py ---
"""
material_utils.py -- Material creation and assignment functions 
for building_generator_tool.py.
=======================================================================
DIGM 131 - Week 7 | Author: Samuel Berg

Material utility functions for creating and assigning shaders in Maya. 

This module provides helpers that create Lambert shaders with specified colors
and assign them to objects.

Usage:
    import material_utils as mat
    mat.create_and_assign(floor, name="wood_mat", color=(0.140, 0.101, 0.056))
"""
import maya.cmds as cmds


def create_material(name="custom_mat", color=(0.5, 0.5, 0.5),
                    material_type="lambert"):
    """Create a new shader and connect it to a shading group.

    The shading group is named "<name>_SG" and is wired up internally;
    callers do not need to track it -- assign_material() looks it up
    from the shader name.

    Args:
        name (str): Name for the shader node.
        color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
        material_type (str): Type of shader to create. Supported values
            are "lambert" and "blinn".

    Returns:
        str: The name of the created shader node.
    """
    
    #Create material
    shader = cmds.shadingNode(material_type, asShader=True, name=name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    cmds.setAttr(shader + ".color", *color, type="double3")
    
    return name
    

def assign_material(obj_name, shader_name):
    """Assign an existing shader to a Maya object.

    Looks up the shading group connected to the shader and adds the
    object to it. Pass the shader name returned from create_material();
    you do not need to track the shading group yourself.

    Args:
        obj_name (str): The name of the Maya transform or shape node.
        shader_name (str): The shader name returned from create_material().

    Returns:
        None
    """
    
    #Assign material
    sgs = cmds.listConnections(shader_name + ".outColor", type="shadingEngine")
    cmds.sets(obj_name, edit=True, forceElement=sgs[0])


def create_and_assign(obj_name, name="auto_mat", color=(0.5, 0.5, 0.5),
                      material_type="lambert"):
    """Convenience function: create a material and immediately assign it.

    Args:
        obj_name (str): The Maya object to receive the material.
        name (str): Name for the new shader.
        color (tuple): (r, g, b) color, values 0.0 to 1.0.
        material_type (str): "lambert" or "blinn".

    Returns:
        str: The name of the created shader node.
    """
    
    #Create a material with the create_material function
    shader = create_material(name, color, material_type)
    
    #Assign the created material with the assign_material function
    assign_material(obj_name, shader)
    
    return shader


if __name__ == "__main__":
    # Self-test: runs only when executed directly
    cmds.file(new=True, force=True)
    print("material_utils self test: Success!")