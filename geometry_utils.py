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



if __name__ == "__main__"":
    #Self-test: runs only when executed directly
    cmds.file(new=True, force=True)
    print("geometry_utils self-test: Success!")