""" AsciiArt NextGen CLI

This CLI can be used to interact with the AsciiArt NextGen module. 
"""

""" [1] Imports
"""
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from pathlib import Path

""" [2] Define defaults
"""
ascii = AsciiArt()

""" [3] Define CLI
"""
parser = argparse.ArgumentParser(
    prog = "AsciiArt NextGen CLI",
    description = "Interact with the AsciiArt NextGen module to see what options are available and how they work.", 
    epilog = "© AsciiArt NextGen CLI. 2023. YVDL & RE",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    add_help = True,
)

""" [4] Arguments 
"""
### Positional Argument: Type
parser.add_argument(
    "type",
    nargs = "?",
    type = str,
    help = "Specify the action you would like to take. Options IMAGE, TEXT.",
    default = "show_help",
    action = "store"
)

### Positional Argument: Path
parser.add_argument(
    "path",
    nargs = "?",
    type = str,
    help = "Provide the path and image name you would like to generate",
    action = "store",
)

### Argument groups
run_image = parser.add_argument_group(
    title = "Ascii Image Generation",
    description = "explain more about these options"
)

### Optional Argument: Color
run_image.add_argument(
    "-c", "--color",
    action = "store_false",
    default = True,
    help = "Ascii image generated in full color by default. Turn off and generate Ascii image using CLI output color."
)


""" [5] Get arguments
"""
args = parser.parse_args()

""" [6] Validations
"""

## Type = Default
if ( args.type.lower() == "show_help" ):
    print(f"Show default CLI message with all of the options")

## Type = Image
elif ( args.type.lower() == "image"):
    path = Path(args.path) # Get the path name

    ## Source file exists
    if ( path.is_file() == True):
        
        ### Overwrite the default image options using the CLI parameters specified
        ascii.color = args.color

        ### Generate Ascii Image
        ascii.print_image(
            ascii.create(image_file = path)
        )
                 
    ## Source file does not exist
    else:
        print(f"The path specified does not exist. Please try again!")


## Type = Text
elif ( args.type.lower() == "text" ):
    print(f"Show all things text related")


## Incorrect types selected
else:
    print(f"please specify a type!")