# --- main.py ---
"""
main.py -- Entry point for building_generator_tool.py.
=============================================================
DIGM 131 - Week 10 | Author: Samuel Berg

Main entry point that imports and uses all utility modules to
generate a building.
"""

from functools import partial

import os
import sys
import importlib
import math
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

widgets = {}
WINDOW_NAME = "buildingGeneratorToolWin"
output_dir  = os.path.join(os.path.expanduser("~"), "maya_exports")

BUILDINGS_CONFIG = []
        
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
    if con.DEBUG:
        print(f"[DEBUG] Create Story: Floor Size={floor_size}, Floor Thickness={floor_thickness}, "
            f"Wall Height={wall_height}, Wall Thickness={wall_thickness}, Window Count={window_count}, "
            f"Window Width={window_width}, Window Height={window_height}, Window Pane Thickness={window_pane_thickness} " 
            f"Window Position={window_position}, Floor Color={floor_color}, Walls Color={walls_color}, "
            f"Window Color={window_color}")
            
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
        cmds.error(f"Window width '{window_width}' cannot be less than or equal to floor size '{floor_size}'")
    if floor_size <= wall_thickness:
        cmds.error(f"Wall thickness '{wall_thickness}' cannot be less than or equal to floor size '{floor_size}'")
    if floor_size <= floor_thickness:
        cmds.error(f"Floor thickness '{floor_thickness}' cannot be less than or equal to floor size '{floor_size}'")
    if wall_height <= window_height:
        cmds.error(f"Wall height '{wall_height}' cannot be less than or equal to window height '{window_height}'")
    if wall_thickness < window_pane_thickness:
        cmds.error(f"Window thickness '{window_thickness}' cannot be more than wall thickness '{wall_thickness}'")
    if abs(window_position[0]) >= ((floor_size/2.0)-(window_width/2.0)):
        cmds.error(f"Window horizontal position '{window_position[0]}' must exist on the wall")
    if window_position[1] >= (wall_height-(window_height/2.0)):
        cmds.error(f"Window vertical position '{window_position[1]}' must exist on the wall")
    if window_position[1] <= (window_height/2.0):
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
                    radius=(floor_size/2)*math.sqrt(2)+0.1,
                    height=wall_height*2,
                    thickness=wall_thickness)
                    
        walls_mat = mat.create_and_assign(walls, name="M_Walls_01", color=walls_color,
                    material_type="lambert")
        
        #Hard-code the window pane's Z position so 
        #    it is always in the middle of the wall            
        window_z = ((floor_size/2)-(((wall_thickness/2)*math.sqrt(2))/2))
        
        #Store references for the window panes
        pane_list = []
        print(pane_list)
        
        #Create the number of windows chosen in the parameters;
        #    loop allows each interceptor and window pane to be created, 
        #    renamed, and positioned and rotated correctly based on the 
        #    number of windows defined; loop will not run with 
        #    more than 4 windows
        if window_count>0:
            for i in range(window_count):
                if i<4:
                    #Create and position the window interceptor 
                    #    and window pane with the given parameters
                    (pane, interceptor) = geo.create_window(
                            width=window_width,
                            height=window_height,
                            depth=(wall_thickness*2),
                            pane_thickness=window_pane_thickness,
                            position=(
                                window_position[0],
                                window_position[1],
                                window_z))
                    
                    #Rotate and rename the window interceptor 
                    #    and window pane based on which of 
                    #    the window_count number of windows was just created       
                    cmds.rotate(0, (90*i), 0, pane, objectSpace=True, pivot=(0,0,0))
                    print(pane)
                    #print(pane)
                    pane_list.append(pane)
                    cmds.rotate(
                            0, (90*i), 0, 
                            interceptor, 
                            objectSpace=True, 
                            pivot=(0,0,0))
                    
                    #Cut the interceptor out of the wall and delete history
                    walls = cmds.polyBoolOp(
                                    walls, 
                                    interceptor, 
                                    op=2, 
                                    constructionHistory=False, 
                                    name="wall_with_window")
            
            #Group all the window panes together
            print(pane_list)
            pane_group = cmds.group(pane_list, name="panes_grp")
            
            window_mat = mat.create_and_assign(
                        pane_group, 
                        name="M_Window_01", 
                        color=window_color,
                        material_type="lambert")
                        
            #Group the floor, walls, and windows together
            full_story = cmds.group(
                        floor,
                        walls, 
                        pane_group, 
                        name="full_story_01")
                         
            return full_story
        else:
            #Group the floor and walls together
            full_story = cmds.group(floor, walls, name="full_story_01")
                         
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
        print(f"[DEBUG] Generate Building: Floor Size={floor_size}, Floor Thickness={floor_thickness}, "
            f"Wall Height={wall_height}, Wall Thickness={wall_thickness}, Window Count={window_count}, "
            f"Window Width={window_width}, Window Height={window_height}, Window Pane Thickness={window_pane_thickness} " 
            f"Window Position={window_position}, Floor Color={floor_color}, Walls Color={walls_color}, "
            f"Window Color={window_color}, Roof Color={roof_color}, Story Count={story_count}, "
            f"Building Position={position}")
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
        cmds.error(f"Window width '{window_width}' cannot be less than or equal to floor size '{floor_size}'")
    if floor_size <= wall_thickness:
        cmds.error(f"Wall thickness '{wall_thickness}' cannot be less than or equal to floor size '{floor_size}'")
    if floor_size <= floor_thickness:
        cmds.error(f"Floor thickness '{floor_thickness}' cannot be less than or equal to floor size '{floor_size}'")
    if wall_height <= window_height:
        cmds.error(f"Wall height '{wall_height}' cannot be less than or equal to window height '{window_height}'")
    if wall_thickness < window_pane_thickness:
        cmds.error(f"Window pane thickness '{window_pane_thickness}' cannot be more than wall thickness '{wall_thickness}'")
    if abs(window_position[0]) >= ((floor_size/2.0)-(window_width/2.0)):
        cmds.error(f"Window horizontal position '{window_position[0]}' must exist on the wall")
    if window_position[1] >= (wall_height-(window_height/2.0)):
        cmds.error(f"Window vertical position '{window_position[1]}' must exist on the wall")
    if window_position[1] <= (window_height/2.0):
        cmds.error(f"Window vertical position '{window_position[1]}' must exist on the wall")
    try:
        #Generate the building; conditional ensures building 
        #    will not try to generate if the amount of stories is 0
        if story_count>=1:
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
            bbox = cmds.xform(
                        story, 
                        query=True, 
                        boundingBox=True, 
                        objectSpace=True)
            
            #Store the height of the first story's 
            #    bounding box in the height variable
            height = abs(bbox[4]-bbox[1])
            
            #Generate the rest of the stories; loop allows for the 
            #    amount of stories created to correspond to story_count
            for i in range(story_count-1):
                #Duplicate the most recently created story 
                #    and stack the duplicate on top of it
                story = cmds.duplicate(story)[0]
                cmds.move(0, (height * (i+1)), 0, story)
                story_list.append(story)
            
            #Create the roof with given parameters
            #    and position it on top of the full building    
            roof = geo.create_roof(width=floor_size,
                    roof_height=floor_thickness,
                    depth=floor_size,
                    radius=(floor_size/2)*math.sqrt(2)+1,
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
    
    if con.DEBUG:
        print(f"Create element Function - Element Parameters are {data}")
        
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

    
def build_all(buildings_config):
    """Build everything in buildings_config."""
    # Store references for the results
    results = []
    
    #Show a warning if no parameters are set by the user
    if not buildings_config:
        cmds.warning(f"No parameters set, no building created")
        
    # Generate the buildinng using buildings_config;
    #    loop allows multiple buildings to be in the config
    for entry in buildings_config:
        obj = create_element(entry)
        if obj:
            results.append(obj)
                
    #Put the whole scene in focus
    cmds.viewFit(allObjects=True)
    return results   
    

def on_generate_building_clicked(*args):
    """The config setup and generation of the full building based on the UI element.
    
        Args:
           None
    
        Returns:
            None
    """
    
    #Set up the new building config
    buildings_config = [{
        "type": "building",
        "name": cmds.textField(
            widgets["name_field"],   q=True, text=True) or "Unnamed_Building",
        "floor_size": cmds.floatSliderGrp(
            widgets["floor_size_slider"], q=True, value=True),
        "floor_thickness": cmds.floatSliderGrp(
            widgets["floor_thickness_slider"], q=True, value=True),
        "wall_height": cmds.floatSliderGrp(
            widgets["wall_height_slider"], q=True, value=True),
        "wall_thickness": cmds.floatSliderGrp(
            widgets["wall_thickness_slider"], q=True, value=True),
        "window_count": cmds.intSliderGrp(
            widgets["window_count_slider"], q=True, value=True),
        "window_width": cmds.floatSliderGrp(
            widgets["window_width_slider"], q=True, value=True),
        "window_height": cmds.floatSliderGrp(
            widgets["window_height_slider"], q=True, value=True),
        "window_pane_thickness": cmds.floatSliderGrp(
            widgets["window_pane_thickness_slider"], q=True, value=True),
        "window_position": (
            cmds.floatSliderGrp(
                    widgets["window_horizontal_position_slider"], 
                    q=True, value=True),
            cmds.floatSliderGrp(
                    widgets["window_vertical_position_slider"], 
                    q=True, value=True)
            ),
        "floor_color": (
            cmds.floatField(widgets["floor_color_r"], q=True, value=True),
            cmds.floatField(widgets["floor_color_g"], q=True, value=True),
            cmds.floatField(widgets["floor_color_b"], q=True, value=True)
            ),
        "walls_color": (
            cmds.floatField(widgets["wall_color_r"], q=True, value=True),
            cmds.floatField(widgets["wall_color_g"], q=True, value=True),
            cmds.floatField(widgets["wall_color_b"], q=True, value=True)
            ),
        "window_color": (
            cmds.floatField(widgets["window_color_r"], q=True, value=True),
            cmds.floatField(widgets["window_color_g"], q=True, value=True),
            cmds.floatField(widgets["window_color_b"], q=True, value=True)
            ),
        "roof_color": (
            cmds.floatField(widgets["roof_color_r"], q=True, value=True),
            cmds.floatField(widgets["roof_color_g"], q=True, value=True),
            cmds.floatField(widgets["roof_color_b"], q=True, value=True)
            ),
        "story_count": cmds.intSliderGrp(
                            widgets["story_count_slider"], 
                            q=True, 
                            value=True),
        "position": (
            cmds.floatField(widgets["building_x_position"], q=True, value=True),
            cmds.floatField(widgets["building_y_position"], q=True, value=True),
            cmds.floatField(widgets["building_z_position"], q=True, value=True)
            ),
            }]
            
    #Generate the building
    if con.DEBUG:
        print(f"Building Parameters are {buildings_config}")
        
    build_all(buildings_config)
    
    return
    
    
def on_change_wall_window(
            wall_height_slider_name, 
            window_height_slider_name, 
            window_vertical_position_slider_name, 
            *args):
    """Change window vertical slider limits based on update from other sliders 
    
        Args:
           wall_height_slider_name (str): The name of the wall height slider
           window_height_silder_name (str): The name of the window height slider
           window_vertical_position_slider_name (str):
               The name of the window vertical position slider
    
        Returns:
            None
    """
    
    #Get the new value of the wall height or window height slider
    wall_height = cmds.floatSliderGrp(
                        wall_height_slider_name, q=True, v=True)
    print(f"Wall Height changed to: {wall_height}")
    window_height = cmds.floatSliderGrp(
                        window_height_slider_name, q=True, v=True)
    print(f"window Height changed to: {window_height}")

    #Calculate the new min and max value for the window vertical position
    new_min = (window_height/2.0)+0.1
    new_max = (wall_height-(window_height/2.0))-0.1
    
    #Update the window vertical position slider's min and max values
    cmds.floatSliderGrp(window_vertical_position_slider_name, e=True,
                        minValue=new_min, 
                        maxValue=new_max,
                        fieldMinValue=new_min, 
                        fieldMaxValue=new_max)
    
    #If the current value of the window vertical position exceeds 
    #    the new min and max, reset it
    current_val = cmds.floatSliderGrp(
        window_vertical_position_slider_name, q=True, v=True)
    if current_val > new_max:
        cmds.floatSliderGrp(
            window_vertical_position_slider_name, e=True, 
            value=(wall_height/2.0))
    if current_val < new_min:
        cmds.floatSliderGrp(
            window_vertical_position_slider_name, e=True, 
            value=(wall_height/2.0))


def on_change_wall_window_horizontal(
            floor_size_slider_name, 
            window_width_slider_name, 
            window_horizontal_position_slider_name, 
            *args):
    """Change window horizontal slider limits based on update from other sliders 
    
        Args:
           floor_size_slider_name (str): The name of the floor size slider
           window_width_silder_name (str): The name of the window width slider
           window_horizontal_position_slider_name (str):
               The name of the window horizontal position slider
    
        Returns:
            None
    """
    
    #Get the new value of the floor size or window width slider
    floor_size = cmds.floatSliderGrp(
                        floor_size_slider_name, q=True, v=True)
    print(f"Floor Size changed to: {floor_size}")
    window_width = cmds.floatSliderGrp(
                        window_width_slider_name, q=True, v=True)
    print(f"Window Width changed to: {window_width}")

    #Calculate the new min and max value for the window horizontal position
    new_min = -(((floor_size/2.0)-(window_width/2.0))-0.1)
    new_max = ((floor_size/2.0)-(window_width/2.0))-0.1
    
    #Update the window horizontal position slider's min and max values
    cmds.floatSliderGrp(window_horizontal_position_slider_name, e=True,
                        minValue=new_min, 
                        maxValue=new_max,
                        fieldMinValue=new_min, 
                        fieldMaxValue=new_max)
    
    #If the current value of the window horizontal position
    #    exceeds the new min and max, reset it
    current_val = cmds.floatSliderGrp(
        window_horizontal_position_slider_name, q=True, v=True)
    if current_val > new_max:
        cmds.floatSliderGrp(
            window_horizontal_position_slider_name, e=True, value=0)
    if current_val < new_min:
        cmds.floatSliderGrp(
            window_horizontal_position_slider_name, e=True, value=0)
        
    return
    
    
def open_color_picker(color_r_input, color_g_input,color_b_input, *args):
    """Change RGB color float fields based on color picker inputs 
    
        Args:
           color_r_input (float, 0.0-1.0): The R value of the color
           color_g_input (float, 0.0-1.0): The G value of the color
           color_b_input (float, 0.0-1.0): The B value of the color
    
        Returns:
            None
    """
    
    #Get the new values of the RGB float fields
    r = cmds.floatField(color_r_input, q=True, v=True)
    g = cmds.floatField(color_g_input, q=True, v=True)
    b = cmds.floatField(color_b_input, q=True, v=True)
    
    #Open the color editor
    result = cmds.colorEditor(rgbValue=[r, g, b])
    
    #Check if the user confirmed a selection
    if cmds.colorEditor(query=True, result=True):
        #Query the RGB values
        r,g,b = cmds.colorEditor(query=True, rgb=True)
        
        #Update the RGB float fields
        cmds.floatField(color_r_input, e=True, value=r)
        cmds.floatField(color_g_input, e=True, value=g)
        cmds.floatField(color_b_input, e=True, value=b)
    else:
        print("Editor cancelled")
    return
    
            
def build_ui():
    """Build the UI element to facilitate user input 
    
        Args:
           None
    
        Returns:
            None
    """
    
    #Delete the UI window if it is already open
    if cmds.window(WINDOW_NAME, exists=True): cmds.deleteUI(WINDOW_NAME)
    
    #Create the UI window
    cmds.window(
        WINDOW_NAME, 
        title="Building Generator", 
        widthHeight=(750, 1000))
        
    #Make the window scrollable
    cmds.scrollLayout(
        horizontalScrollBarThickness=0,
        verticalScrollBarThickness=15,
        childResizable=True
    )
    
    #Make all columns adjust to the size of the window
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6,
                      columnOffset=("both", 10))
    
    #Title the window                  
    cmds.text(label="--- Generate New Building ---", font="boldLabelFont")
    
    #Create a text field so the user can name the building,
    #    default is "Unnamed_Building"
    cmds.text(label="Name:", align="left")
    widgets["name_field"]    = cmds.textField(text="Unnamed_Building")
    
    #Create a floor section of the UI window
    cmds.separator(height=12, style="in")
    cmds.text(label="Floor:", align="left")
    
    #Create a slider and float field to 
    #    control the floor size and floor thickness
    widgets["floor_size_slider"]  = cmds.floatSliderGrp(
                                            label="Floor Size: ", 
                                            field=True, 
                                            minValue=1, 
                                            maxValue=1000, 
                                            fieldMinValue=1, 
                                            fieldMaxValue=10000000, 
                                            value=100.0)
    widgets["floor_thickness_slider"]  = cmds.floatSliderGrp(
                                            label="Floor Thickness: ", 
                                            field=True, 
                                            minValue=0.1, 
                                            maxValue=1000, 
                                            fieldMinValue=0.1, 
                                            fieldMaxValue=10000000, 
                                            value=1.0)
                                            
    #Create float fields aligned horiztonally to control the floor color
    cmds.text(label="Floor Color (RGB): ", align="left")
    cmds.rowLayout(
            numberOfColumns=3,
            columnWidth3=(500/3,500/3,500/3), 
            adjustableColumn=[1,2,3], 
            columnAttach=[(1,'both',0), (2, 'both', 0), (3, 'both', 0)])
    widgets["floor_color_r"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.129)
    widgets["floor_color_g"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.094)
    widgets["floor_color_b"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.068)
    cmds.setParent('..')
    
    #Create a color picker button for the floor to control its color
    widgets["floor_color_button"] = cmds.button(label="Pick Floor Color",
                    backgroundColor=(0.4, 0.5, 0.8),
                    command=partial(open_color_picker,
                                widgets["floor_color_r"],
                                widgets["floor_color_g"],
                                widgets["floor_color_b"])) 
    
    #Create a wall section of the UI window
    cmds.separator(height=12, style="in")
    cmds.text(label="Walls:", align="left")
    
    #Create a slider and float field to 
    #    control the wall height and thickness
    widgets["wall_height_slider"] = cmds.floatSliderGrp(
                                            label="Wall Height: ", 
                                            field=True, 
                                            minValue=0.1, 
                                            maxValue=1000, 
                                            fieldMinValue=0.1, 
                                            fieldMaxValue=10000000, 
                                            value=60.0)
    widgets["wall_thickness_slider"]  = cmds.floatSliderGrp(
                                            label="Wall Thickness: ", 
                                            field=True, 
                                            minValue=0.1, 
                                            maxValue=1000, 
                                            fieldMinValue=0.1, 
                                            fieldMaxValue=10000000, 
                                            value=1.5)
    
    #Create float fields aligned horiztonally to control the wall color
    cmds.text(label="Wall Color (RGB): ", align="left")
    cmds.rowLayout(
            numberOfColumns=3, 
            columnWidth3=(380/3,380/3,380/3), 
            adjustableColumn=[1,2,3], 
            columnAttach=[(1,'both',0), (2, 'both', 0), (3, 'both', 0)])
    widgets["wall_color_r"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.075)
    widgets["wall_color_g"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.045)
    widgets["wall_color_b"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.036)
    cmds.setParent('..')
    
    #Create a color picker button for the walls to control their color
    widgets["wall_color_button"] = cmds.button(label="Pick Wall Color",
                    backgroundColor=(0.4, 0.5, 0.8),
                    command=partial(open_color_picker,
                                widgets["wall_color_r"],
                                widgets["wall_color_g"],
                                widgets["wall_color_b"])) 
    
    #Create a window section of the UI window    
    cmds.separator(height=12, style="in")
    cmds.text(label="Windows:", align="left")
    widgets["window_count_slider"]  = cmds.intSliderGrp(
                                            label="Window Count: ", 
                                            field=True, 
                                            minValue=0, 
                                            maxValue=4, 
                                            fieldMinValue=0, 
                                            fieldMaxValue=4, 
                                            value=0)   
    widgets["window_width_slider"]  = cmds.floatSliderGrp(
                                            label="Window Width: ", 
                                            field=True, 
                                            minValue=0.1, 
                                            maxValue=1000, 
                                            fieldMinValue=0.1, 
                                            fieldMaxValue=10000000, 
                                            value=23.0)
    widgets["window_height_slider"]  = cmds.floatSliderGrp(
                                            label="Window Height: ", 
                                            field=True, 
                                            minValue=0.1, 
                                            maxValue=1000, 
                                            fieldMinValue=0.1, 
                                            fieldMaxValue=10000000, 
                                            value=14.0)
    widgets["window_pane_thickness_slider"]  = cmds.floatSliderGrp(
                                            label="Window Pane Thickness: ", 
                                            field=True, 
                                            minValue=0.01, 
                                            maxValue=1000, 
                                            fieldMinValue=0.01, 
                                            fieldMaxValue=10000000, 
                                            value=0.75)
    widgets["window_horizontal_position_slider"]  = cmds.floatSliderGrp(
                                            label="Horizontal Position: ", 
                                            field=True, 
                                            minValue=-38.4, 
                                            maxValue=38.4, 
                                            fieldMinValue=-38.4, 
                                            fieldMaxValue=38.4, 
                                            value=0.0)
    widgets["window_vertical_position_slider"]  = cmds.floatSliderGrp(
                                            label="Vertical Position: ", 
                                            field=True, 
                                            minValue=7.1, 
                                            maxValue=52.9, 
                                            fieldMinValue=7.1, 
                                            fieldMaxValue=52.9, 
                                            value=30.0)
    cmds.text(label="Window Color (RGB): ", align="left")
    cmds.rowLayout(
            numberOfColumns=3, 
            columnWidth3=(380/3,380/3,380/3), 
            adjustableColumn=[1,2,3], 
            columnAttach=[(1,'both',0), (2, 'both', 0), (3, 'both', 0)])
    widgets["window_color_r"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.467)
    widgets["window_color_g"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.765)
    widgets["window_color_b"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.814)
    cmds.setParent('..')
    widgets["window_color_button"] = cmds.button(label="Pick Window Color",
                    backgroundColor=(0.4, 0.5, 0.8),
                    command=partial(open_color_picker,
                                widgets["window_color_r"],
                                widgets["window_color_g"],
                                widgets["window_color_b"])) 
        
    cmds.separator(height=12, style="in")
    cmds.text(label="Full Building Parameters:", align="left")
    
    cmds.text(label="Roof Color (RGB): ", align="left")
    cmds.rowLayout(
            numberOfColumns=3, 
            columnWidth3=(380/3,380/3,380/3), 
            adjustableColumn=[1,2,3], 
            columnAttach=[(1,'both',0), (2, 'both', 0), (3, 'both', 0)])
    widgets["roof_color_r"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.118)
    widgets["roof_color_g"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.118)
    widgets["roof_color_b"]  = cmds.floatField(
                                        minValue=0.0, 
                                        maxValue=1.0, 
                                        value=0.118)
    cmds.setParent('..')
    widgets["roof_color_button"] = cmds.button(label="Pick Roof Color",
                    backgroundColor=(0.4, 0.5, 0.8),
                    command=partial(open_color_picker,
                                widgets["roof_color_r"],
                                widgets["roof_color_g"],
                                widgets["roof_color_b"])) 
                
    widgets["story_count_slider"]  = cmds.intSliderGrp(
                                        label="Story Count: ", 
                                        field=True, minValue=1, 
                                        maxValue=50, 
                                        fieldMinValue=0, 
                                        fieldMaxValue=10000000, 
                                        value=1)
    cmds.text(label="Full Building X Position: ", align="left")
    widgets["building_x_position"]  = cmds.floatField(value=0.0)
    cmds.text(label="Full Building Y Position: ", align="left")
    widgets["building_y_position"]  = cmds.floatField(value=0.0)
    cmds.text(label="Full Building Z Position: ", align="left")
    widgets["building_z_position"]  = cmds.floatField(value=0.0)
    
    #Update the window vertical position sliders to
    #    the new values determined in the on_change functions above
    cmds.floatSliderGrp(widgets["wall_height_slider"], e=True, 
                        cc=partial(on_change_wall_window, 
                                    widgets["wall_height_slider"], 
                                    widgets["window_height_slider"],
                                    widgets["window_vertical_position_slider"]))
    cmds.floatSliderGrp(widgets["window_height_slider"], e=True, 
                        cc=partial(on_change_wall_window, 
                                    widgets["wall_height_slider"],
                                    widgets["window_height_slider"],
                                    widgets["window_vertical_position_slider"]))
    
    #Update the window horizontal position sliders to
    #    the new values determined in the on_change functions above                               
    cmds.floatSliderGrp(widgets["floor_size_slider"], e=True, 
                        cc=partial(on_change_wall_window_horizontal, 
                                    widgets["floor_size_slider"],
                                    widgets["window_width_slider"],
                                    widgets["window_horizontal_position_slider"])) 
    cmds.floatSliderGrp(widgets["window_width_slider"], e=True, 
                        cc=partial(on_change_wall_window_horizontal, 
                                    widgets["floor_size_slider"],
                                    widgets["window_width_slider"],
                                    widgets["window_horizontal_position_slider"]))  
                                              
                
    cmds.button(label="Generate", command=on_generate_building_clicked,
                backgroundColor=(0.4, 0.7, 0.4))
    cmds.showWindow(WINDOW_NAME) 
  
    return
    
if __name__ == "__main__":
    build_ui()
    print("main self-test: Success!")    
         