# --- main.py ---
"""
main.py -- Entry point for building_generator_tool.py.
=============================================================
DIGM 131 - Week 7 | Author: Samuel Berg

Main entry point that imports and uses all utility modules to
generate a building.
"""

import os
import sys
import importlib
import maya.cmds as cmds
import config

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

import config as con
importlib.reload(con)

BUILDINGS_CONFIG = [
    {
        "type": "building",
        "name": "Office_Building_01",
        "floor_size": 50,
        "floor_thickness": 1,
        "wall_height": 30,
        "wall_thickness": 2,
        "window_count": 3,
        "window_width": 16,
        "window_height": 9,
        "window_pane_thickness": 0.75,
        "window_position": (0, 7.5),
        "floor_color": (0.129, 0.094, 0.068),
        "walls_color": (0.075, 0.045, 0.036),
        "window_color": (0.467, 0.765, 0.814),
        "roof_color": (0.118, 0.118, 0.118),
        "story_count": 15,
        "position": (0, 0, 0)
    },
    {
        "type": "building",
        "name": "Office_Building_02",
        "floor_size": 75,
        "floor_thickness": 0.75,
        "wall_height": 15,
        "wall_thickness": 4,
        "window_count": 4,
        "window_width": 65,
        "window_height": 4,
        "window_pane_thickness": 0.85,
        "window_position": (0, 4),
        "floor_color": (0.129, 0.094, 0.068),
        "walls_color": (0.075, 0.045, 0.036),
        "window_color": (0.467, 0.765, 0.814),
        "roof_color": (0.118, 0.118, 0.118),
        "story_count": 5,
        "position": (50, 0, 75)
    },

]    
        
def create_story(
            floor_size=50,
            floor_thickness=1,
            wall_height=30,
            wall_thickness=2,
            window_count=3,
            window_width=17,
            window_height=9,
            window_pane_thickness=0.75,
            window_position=(0, 7.5),
            floor_color=(0.129, 0.094, 0.068),
            walls_color=(0.075, 0.045, 0.036),
            window_color=(0.623, 0.765, 0.814)):
     
    """Create a full story of the building, with a floor, wall, and windows.

    Args:
       floor_size (float): Size along the X and Z axis of the floor.
       floor_thickness (float): Size along the Y axis of the floor.
       wall_height (float): Size along the Y axis of the walls.
       wall_thickness (float): Thickness of the walls.
       window_count (int): The number of windows, with one window per wall; can be 0 to 4.
       window_width (float): Size along the X axis of the window.
       window_height (float): Size along the Y axis of the window.
       window_pane_thickness (float): Size along the Z axis of the window pane.
       window_position (tuple): (x, y) Position on the wall of the window.
       floor_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
       walls_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
       window_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.

    Returns:
        str: The name of a group node containing the floor, walls, and windows.
    """
    
    #Create the floor with the given parameters          
    if con.DEBUG:
        print(f"[DEBUG] create_floor: width={floor_size}, height={floor_thickness}, depth={floor_size}")
    #Warning messages for negative values
    if floor_size <= 0:
        cmds.warning(f"Invalid floor size {floor_size}"); floor_size = 1
    if floor_thickness <= 0:
        cmds.warning(f"Invalid floor thickness {floor_thickness}"); floor_thickness = 1
    if wall_height <= 0:
        cmds.warning(f"Invalid wall height {wall_height}"); wall_height = 1
    if wall_thickness <= 0:
        cmds.warning(f"Invalid wall thickness {wall_thickness}"); wall_thickness = 1
    if window_count < 0:
        cmds.warning(f"Invalid amount of windows {window_count}"); window_count = 0
    if window_width <= 0:
        cmds.warning(f"Invalid window width {wnidow_width}"); window_width = 1
    if window_height <= 0:
        cmds.warning(f"Invalid window height {window_height}"); window_height = 1
    if window_pane_thickness <= 0:
        cmds.warning(f"Invalid window pane thickness {window_pane_thickness}"); window_pane_thickness = 1
    if window_count > 4:
        cmds.warning(f"Too many windows, defaulted to 4"); window_count = 4
        
    #Error messages for broken values
    if floor_size <= window_width:
        cmds.error(f"Window width '{window_width}' cannot be less than floor size '{floor_size}'")
    if floor_size <= wall_thickness:
        cmds.error(f"Wall thickness '{wall_thickness}' cannot be less than floor size '{floor_size}'")
    if floor_size <= floor_thickness:
        cmds.error(f"Floor thickness '{floor_thickness}' cannot be less than floor size '{floor_size}'")
    if (wall_height/2.0) <= window_height:
        cmds.error(f"Window height '{window_height}' cannot be less than wall height '{wall_height}'")
    if wall_thickness < window_pane_thickness:
        cmds.error(f"Window thickness '{window_thickness}' cannot be more than wall thickness '{wall_thickness}'")
    if abs(window_position[0]) >= ((floor_size/2.0)-(window_width/2.0)):
        cmds.error(f"Window horizontal position '{window_position[0]}' must exist on the wall")
    if abs(window_position[1]) >= ((wall_height/2.0)-(window_height/2.0)):
        cmds.error(f"Window vertical position '{window_position[1]}' must exist on the wall")
    try:
        floor = geo.create_floor(
                    width=floor_size,
                    height=floor_thickness,
                    depth=floor_size)
                    
        floor_mat = mat.create_and_assign(floor, name="M_Floor_01", color=floor_color,
                    material_type="lambert")
    
        #Create the walls with the given parameters            
        walls = geo.create_walls(
                    radius=(floor_size/1.39),
                    height=wall_height,
                    thickness=wall_thickness)
                    
        walls_mat = mat.create_and_assign(walls, name="M_Walls_01", color=walls_color,
                    material_type="lambert")
        
        #Hard-code the window pane's Z position so it is always in the middle of the wall            
        window_z = (floor_size/2.02)
        
        #Store references for the window panes
        pane_list = []
        print(pane_list)
        #Create the number of windows chosen in the parameters;
        #    loop allows each interceptor and window pane to be created, renamed, and
        #    positioned and rotated correctly based on the number of windows defined;
        #    loop will not run with more than 4 windows
        for i in range(window_count):
            if i<4:
                #Create and position the window interceptor and window pane with the given parameters
                (pane, interceptor) = geo.create_window(
                        width=window_width,
                        height=window_height,
                        depth=(wall_thickness*2),
                        pane_thickness=window_pane_thickness,
                        position=(
                            window_position[0],
                            window_position[1],
                            window_z))
                
                #Rotate and rename the window interceptor and window pane based on which of the
                #    window_count number of windows was just created       
                cmds.rotate(0, (90*i), 0, pane, objectSpace=True, pivot=(0,0,0))
                print(pane)
                #print(pane)
                pane_list.append(pane)
                cmds.rotate(0, (90*i), 0, interceptor, objectSpace=True, pivot=(0,0,0))
                
                #Cut the window interceptor out of the wall and delete history
                walls = cmds.polyBoolOp(walls, interceptor, op=2, constructionHistory=False, name="wall_with_window")
        
        #Group all the window panes together
        print(pane_list)
        pane_group = cmds.group(pane_list, name="panes_grp")
        
        window_mat = mat.create_and_assign(pane_group, name="M_Window_01", color=window_color,
                    material_type="lambert")
                    
        #Group the floor, walls, and windows together
        full_story = cmds.group(floor, walls, pane_group, name="full_story_01")
                     
        return full_story
    except Exception as e:
        cmds.warning(f"Failed: {e}"); return None
    
def generate_building(name="Unnamed_Building_01",
            floor_size=50,
            floor_thickness=1,
            wall_height=30,
            wall_thickness=2,
            window_count=3,
            window_width=17,
            window_height=9,
            window_pane_thickness=0.75,
            window_position=(0, 7.5),
            floor_color=(0.129, 0.094, 0.068),
            walls_color=(0.075, 0.045, 0.036),
            window_color=(0.623, 0.765, 0.814),
            roof_color=(0.118, 0.118, 0.118),
            story_count=15, 
            position=(0,0,0)):
                
    """Generate the full building.
    
        Args:
           floor_size (float): Size along the X and Z axis of the floor.
           floor_thickness (float): Size along the Y axis of the floor.
           wall_height (float): Size along the Y axis of the walls.
           wall_thickness (float): Thickness of the walls.
           window_count (int): The number of windows, with one window per wall; can be 0 to 4.
           window_width (float): Size along the X axis of the window.
           window_height (float): Size along the Y axis of the window.
           window_pane_thickness (float): Size along the Z axis of the window pane.
           window_position (tuple): (x, y) Position on the wall of the window.
           floor_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
           walls_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
           window_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
           roof_color (tuple): (r, g, b) color values, each in the range 0.0 to 1.0.
           story_count (int): The number of stories in the building.
           position (tuple): (x, y, z) Position of the full building at ground level.
    
        Returns:
            str: The name of a group node containing the entire buidling with all generated stories.
    """
    
    #Create the floor with the given parameters          
    if con.DEBUG:
        print(f"[DEBUG] create_floor: width={floor_size}, height={floor_thickness}, depth={floor_size}")
    #Warning messages for negative values
    if floor_size <= 0:
        cmds.warning(f"Invalid floor size {floor_size}"); floor_size = 1
    if floor_thickness <= 0:
        cmds.warning(f"Invalid floor thickness {floor_thickness}"); floor_thickness = 1
    if wall_height <= 0:
        cmds.warning(f"Invalid wall height {wall_height}"); wall_height = 1
    if wall_thickness <= 0:
        cmds.warning(f"Invalid wall thickness {wall_thickness}"); wall_thickness = 1
    if window_count < 0:
        cmds.warning(f"Invalid amount of windows {window_count}"); window_count = 0
    if window_width <= 0:
        cmds.warning(f"Invalid window width {window_width}"); window_width = 1
    if window_height <= 0:
        cmds.warning(f"Invalid window height {window_height}"); window_height = 1
    if window_pane_thickness <= 0:
        cmds.warning(f"Invalid window pane thickness {window_pane_thickness}"); window_pane_thickness = 1
    if story_count <= 0:
        cmds.warning(f"Invalid amount of stories {story_count}"); story_count = 1
    if window_count > 4:
        cmds.warning(f"Too many windows, defaulted to 4"); window_count = 4
        
    #Error messages for broken values
    if floor_size <= window_width:
        cmds.error(f"Window width '{window_width}' cannot be less than floor size '{floor_size}'")
    if floor_size <= wall_thickness:
        cmds.error(f"Wall thickness '{wall_thickness}' cannot be less than floor size '{floor_size}'")
    if floor_size <= floor_thickness:
        cmds.error(f"Floor thickness '{floor_thickness}' cannot be less than floor size '{floor_size}'")
    if (wall_height/2.0) <= window_height:
        cmds.error(f"Window height '{window_height}' cannot be less than wall height '{wall_height}'")
    if wall_thickness < window_pane_thickness:
        cmds.error(f"Window pane thickness '{window_pane_thickness}' cannot be more than wall thickness '{wall_thickness}'")
    if abs(window_position[0]) >= ((floor_size/2.0)-(window_width/2.0)):
        cmds.error(f"Window horizontal position '{window_position[0]}' must exist on the wall")
    if abs(window_position[1]) >= ((wall_height/2.0)-(window_height/2.0)):
        cmds.error(f"Window vertical position '{window_position[1]}' must exist on the wall")
    try:
        #Generate the building; 
        #    conditional ensures building will not try to generate if the amount of stories is 0
        if story_count>1:
            #Store references for the stories
            story_list = []
            
            #Create the first story with the given parameters
            story = create_story(floor_size=floor_size,
                    floor_thickness=floor_thickness,
                    wall_height=wall_height,
                    wall_thickness=wall_thickness,
                    window_count=window_count,
                    window_width=window_width,
                    window_height=window_height,
                    window_pane_thickness=window_pane_thickness,
                    window_position=window_position,
                    floor_color=floor_color,
                    walls_color=walls_color,
                    window_color=window_color)
            story_list.append(story)
            
            #Get the bounding box information of the first story        
            bbox = cmds.xform(story, query=True, boundingBox=True, objectSpace=True)
            
            #Store the height of the first story's bounding box in the height variable
            height = abs(bbox[4]-bbox[1])
            
            #Generate the rest of the stories;
            #    loop allows for the amount of stories created to correspond to story_count
            for i in range(story_count-1):
                #Duplicate the most recently created story and stack the duplicate on top of it
                story = cmds.duplicate(story)[0]
                cmds.move(0, (height * (i+1)), 0, story)
                story_list.append(story)
            
            #Create the roof with given parameters and position it on top of the full building    
            roof = geo.create_roof(width=floor_size,
                    roof_height=floor_thickness,
                    depth=floor_size,
                    radius=(floor_size/1.35),
                    edge_height=(floor_thickness*4),
                    thickness=(floor_thickness*2),
                    position=(0, height*story_count, 0))    
            
            roof_mat = mat.create_and_assign(roof, name="M_Roof_01", color=roof_color,
                    material_type="lambert")
                    
            #Group all the floors of the building together   
            full_building = cmds.group(story_list, roof, name=name)
            cmds.move(position[0], position[1], position[2], full_building)
            
            return full_building

    except Exception as e:
        cmds.warning(f"Failed: {e}"); return None

        
BUILDERS = {
        "building": generate_building,
        "story": create_story
    }    
 
    
def create_element(data):
    """Dispatch one config entry to the right builder."""
    element_type = data.get("type")
    if not element_type:
        cmds.warning("Entry missing 'type' key — skipping.")
        return None
        
    builder = BUILDERS.get(element_type)
    if not builder:
        cmds.warning("Unknown type '{}' — skipping.".format(element_type))
        return None
        
    params = {k: v for k, v in data.items() if k != "type"}
    
    try:
        return builder(**params)
    except TypeError as error:
        cmds.warning("Bad params for '{}': {}".format(element_type, error))
        return None


def build_all():
    """Build everything in BUILDINGS_CONFIG."""
    cmds.file(new=True, force=True)
    results = []
    if not BUILDINGS_CONFIG:
        cmds.warning(f"No parameters set, no building created")
    for entry in BUILDINGS_CONFIG:
        obj = create_element(entry)
        if obj:
            results.append(obj)
    cmds.viewFit(allObjects=True)
    return results    
  
    
if __name__ == "__main__":
    build_all()
    print("main self-test: Success!")    
         