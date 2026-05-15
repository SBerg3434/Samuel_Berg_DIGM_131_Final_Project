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

BUILDINGS_CONFIG = [
    {
        "name": "Office_Building_01",
        "floor_size": 50,
        "floor_thickness": 1,
        "wall_height": 30,
        "wall_thickness": 2,
        "window_count": 3,
        "window_width": 17,
        "window_height": 9,
        "window_pane_thickness": 0.75,
        "window_position": (0, 7.5),
        "story_count": 15,
        "position": (0, 0, 0)
    },
    {
        "name": "Office_Building_02",
        "floor_size": 100,
        "floor_thickness": 1,
        "wall_height": 20,
        "wall_thickness": 2,
        "window_count": 2,
        "window_width": 13,
        "window_height": 5,
        "window_pane_thickness": 0.75,
        "window_position": (0, 7.5),
        "story_count": 5,
        "position": (125, 0, 100)
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
            window_position=(0, 7.5)):
     
    """Create a full story of the building, with a floor, wall, and windows.

    Args:
       floor_size (float): Size along the X and Z axis of the floor.
       floor_thickness (float): Size along the Y axis of the floor.
       wall_height (float): Size along the Y axis of the walls.
       wall_thickness (float): Thickness of the walls.
       window_count (int): The number of windows, with one window per wall; can be 0 to 4.
       wnidow_width (float): Size along the X axis of the window.
       window_height (float): Size along the Y axis of the window.
       window_pane_thickness (float): Size along the Z axis of the window pane.
       window_position (tuple): (x, y) Position on the wall of the window.

    Returns:
        str: The name of a group node containing the floor, walls, and windows.
    """
    
    #Create the floor with the given parameters          
    floor = geo.create_floor(
                width=floor_size,
                height=floor_thickness,
                depth=floor_size)
    
    #Create the walls with the given parameters            
    walls = geo.create_walls(
                radius=(floor_size/1.39),
                height=wall_height,
                thickness=wall_thickness)
    
    #Hard-code the window pane's Z position so it is always in the middle of the wall            
    window_z = (floor_size/2.02)
    
    #Store references for the window panes
    pane_list = []
    
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
            cmds.rename(pane, f"window_pane_0{i+1}")
            #print(pane)
            pane_list.append(pane)
            cmds.rotate(0, (90*i), 0, interceptor, objectSpace=True, pivot=(0,0,0))
            
            #Cut the window interceptor out of the wall and delete history
            walls = cmds.polyBoolOp(walls, interceptor, op=2, constructionHistory=False, name="wall_with_window")
    
    #Group all the window panes together
    #print(pane_list)
    pane_group = cmds.group(pane_list, name="panes_grp")
    
    #Group the floor, walls, and windows together
    full_story = cmds.group(floor, walls, pane_group, name="full_story_01")
                 
    return full_story
    
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
            story_count=15, 
            position=(0,0,0)):
                
    """Generate the full building.
    
        Args:
           floor_size (float): Size along the X and Z axis of the floor.
           floor_thickness (float): Size along the Y axis of the floor.
           wall_height (float): Size along the Y axis of the walls.
           wall_thickness (float): Thickness of the walls.
           window_count (int): The number of windows, with one window per wall; can be 0 to 4.
           wnidow_width (float): Size along the X axis of the window.
           window_height (float): Size along the Y axis of the window.
           window_pane_thickness (float): Size along the Z axis of the window pane.
           window_position (tuple): (x, y) Position on the wall of the window.
           story_count (int): The number of stories in the building.
           position (tuple): (x, y, z) Position of the full building at ground level.
    
        Returns:
            str: The name of a group node containing the entire buidling with all generated stories.
    """
    
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
                window_position=window_position)
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
        roof = create_roof(width=floor_size,
                roof_height=floor_thickness,
                depth=floor_size,
                radius=(floor_size/1.35),
                edge_height=(floor_thickness*4),
                thickness=(floor_thickness*2),
                position=(0, height*story_count, 0))    
        
        #Group all the floors of the building together   
        full_building = cmds.group(story_list, roof, name=name)
        
        return full_building
        
    else:
        #Print the error message if the number of stories is 0 (impossible)
        error_msg = print("Error! Need at least one story.")
        
        return error_msg
    
    
if __name__ == "__main__":
    #Self-test: runs only when executed directly
    cmds.file(new=True, force=True)
    #create_story()
    for info in BUILDINGS_CONFIG:
        generate_building(**info)
    print("main self-test: Success!")    
         