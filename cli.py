""" AsciiArt NextGen CLI

This CLI can be used to interact with the AsciiArt NextGen module. 
"""

""" [1] Imports
"""
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from pathlib import Path
from rich import print


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
    allow_abbrev = True,
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

### Optional Argument: Size type
run_image.add_argument(
    "-st", "--size_type",
    action = "store",
    default = "Percentage",
    choices = ["Percentage","Fixed"],
    help = "Generate the ASCII image based on a percentage size or an exact size."    
)

""" [5] Get arguments
"""
args = parser.parse_args()

""" [6] Validations
"""

## Type = Default
if ( args.type.lower() == "show_help" ):
    default_msg = """Welcome to the [bold]AsciiArt NextGen CLI[/bold]

This CLI allows you to interact with the AsciiArt NextGen module.

Enter -h to get started
"""
    print(default_msg)

## Type = Image
elif ( args.type.lower() == "image"):
    path = Path(args.path) # Get the path name

    ## Source file exists
    if ( path.is_file() == True):
        
        ### Overwrite the default image options using the CLI parameters specified
        ascii.color = args.color
        
        # Determine which sizing option should be used
        if ( args.size_type == "Percentage"):
            ascii.resize_type = ResizeType.percentage_size.value
        elif ( args.size_type == "Fixed"):
            ascii.resize_type = ResizeType.exact_size.value

        

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