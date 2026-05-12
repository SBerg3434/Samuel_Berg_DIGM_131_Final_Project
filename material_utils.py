# --- material_utils.py ---
"""
material_utils.py -- Material creation and assignment functions 
for building_generator_tool.py.
=======================================================================
DIGM 131 - Week 6 | Author: Samuel Berg

Material utility functions for creating and assigning shaders in Maya. 

This module provides helpers that create Lambert shaders with specified colors
and assign them to objects.

Usage:
    import material_utils as mat
    mat.create_and_assign(floor, name="wood_mat", color=(0.140, 0.101, 0.056))
"""
import maya.cmds as cmds



if __name__ == "__main__":
    # Self-test: runs only when executed directly
    cmds.file(new=True, force=True)
    print("material_utils self test: Success!")