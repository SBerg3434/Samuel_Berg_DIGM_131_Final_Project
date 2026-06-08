# Building Generator

## What It Does
A Maya tool that generates a building model from data.
Artists define a name, sizing parameters, positional parameters for 
the windows and the full building, window and story counts, and 
material colors, and the tool builds the building automatically.

## How To Use
1. Open the main.py script in Maya's script editor.  
	NOTE: The main.py script should automatically look for the other three
	modules in the correct location, but if it does not, paste them into
	Maya's default script folder (Documents --> maya --> scripts)
2. Run the script from the script editor. A UI Window should open.
3. Adjust any desired settings in the UI window. The tool defaults to a 
   building with no windows and one story. 
4. Click the "Generate" button at the bottom of the UI window to generate a 
   building. If a value is invalid, an error will appear explaining what value
   failed and why that is the case. For more detailed troubleshooting, set the 
   "DEBUG" variable to "True" in config.py.  
   
NOTE: The tool can be used to generate as many buildings as desired by the
artist by simply clicking the "Generate" button multiple times.

