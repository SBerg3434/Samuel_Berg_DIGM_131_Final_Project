\# My Scene Generator



\## What It Does

A Maya tool that generates a building model from data.

Artists define sizing parameters as well as floor and window

counts in a config list and the tool builds the building

automatically.



\## Planned Features

* \[ ] Core geometry functions (Week 6)
* \[ ] Data-driven configuration (Week 7)
* \[ ] Error handling + debug mode (Week 8)
* \[ ] Maya UI window + JSON save/load (Week 9)
* \[ ] Polish + documentation (Week 10)



\## Project Structure

building\_generator\_tool/

&#x20;   geometry\_utils.py    # Geometry creation functions

&#x20;   material\_utils.py    # Material/shading functions

&#x20;   main.py              # Entry point, data, driver loop

&#x20;   README.md            # This file



\## Functions I Need to Write

\### geometry\_utils.py

* `create\_floor(width, height, depth)` - Cube on ground
* `create\_walls(height, thickness)` - Pipe on floor
* `create\_windows(count, width, height, pane\_thickness, position)` - Cubes in created holes
* `create\_roof(height)` - Cube above walls



\### material\_utils.py

* `create\_material(name, color)` - Lambert shader with RGB
* `assign\_material(obj\_name, shader\_name)` - Apply shader to object
* `create\_and\_assign\_material(obj\_name, name, color)` - Create and assign shader to object 



\### main.py

* `create\_story(floor\_width, floor\_thickness, floor\_depth, wall\_height, wall\_thickness,`

&#x20;                `window\_count, window\_width, window\_height, window\_pane\_thickness,`

&#x20;                `window\_position)` - Create one story of the building

* `create\_building(floor\_count, roof\_thickness)` - Create the full building

