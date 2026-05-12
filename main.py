# --- main.py ---
"""
main.py -- Entry point for building_generator_tool.py.
=============================================================
DIGM 131 - Week 6 | Author: Samuel Berg

Main entry point that imports and uses all utility modules to
generate a building.
"""
import os
import sys
import importlib
import maya.cmds as cmds

try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import geometry_utils as geo
importlib.reload(geo)

import material_utils as mat
importlib.reload(mat)
