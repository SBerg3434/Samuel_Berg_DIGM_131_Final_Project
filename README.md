# Building Generator

## What It Does
A Maya tool that generates a building model from data.
Artists define sizing parameters as well as floor and window
counts in a config list and the tool builds the building
automatically.

## Planned Features
- [X] Core geometry functions (Week 6)
- [X] Data-driven configuration (Week 7)
- [ ] Error handling + debug mode (Week 8)
- [ ] Maya UI window + JSON save/load (Week 9)
- [ ] Polish + documentation (Week 10)

## Project Structure
building_generator_tool/
- geometry_utils.py    # Geometry creation functions
- material_utils.py    # Material shading functions
- config.py            # DEBUG mode on or off
- main.py              # Entry point, data, driver loop
- README.md            # This file

## Functions I Need to Write
### geometry_utils.py
- `create_floor(width, height, depth)` - Cube on ground
- `create_walls(radius, height, thickness)` - Pipe on floor
- `create_windows(count, width, height, depth, pane_thickness, position)` - Cubes in created holes
- `create_roof(width, roof_height, depth, radius, edge_height, thickness, position)` - Cube above walls

### material_utils.py
- `create_material(name, color)` - Lambert shader with RGB
- `assign_material(obj_name, shader_name)` - Apply shader to object
- `create_and_assign_material(obj_name, name, color)` - Create and assign shader to object 

### main.py
- `create_story(floor_size, floor_thickness, wall_height, wall_thickness, window_count, window_width,`
                `window_height, window_pane_thickness, window_position, floor_color, walls_color,` 
                `window_color)` - Create one story of the building
- `generate_building(floor_size, floor_thickness, wall_height, wall_thickness, window_count, window_width,`
                `window_height, window_pane_thickness, window_position, floor_color, walls_color,` 
                `window_color, story_count, position)` - Create the full building

