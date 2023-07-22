"""
[1] Imports
[2] Define defaults
[3] Initiation of CLI
[4] Positional Arguments
[5] Optional Arguments
[6] Run / generate CLI
[7] Validation
"""

""" [1] Imports """
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from pathlib import Path

""" [2] Define defaults """
default_msg = True
ascii = AsciiArt()
type = {
    "image": "Convert an image to an ASCII art image",
    "text": "Convert your text to ASCII text [coming soon]"
}

""" [3] Initiation of CLI """
parser = argparse.ArgumentParser(
    prog = "Program name",
    description = "Description here", 
    epilog = "Footer here",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

""" [4] Positional Arguments """
### Define the function (image, text, animation) to execute
parser.add_argument(
    "type",
    type = str,
    help = "What function [{type}] do you want to execute.",
    default = "default",
    action = "store"
)

### Define the image path
parser.add_argument(
    "path",
    type = str,
    help = "Specify the path of the image.",
    action = "store"
)

""" [5] Optional Arguments """
## Generate image in black & white
parser.add_argument(
    "-c", "--color",
    help = "By default image is generated in color. Turn off color option, and generate image in black & white.",
    action = "store_false"
)

## Keep image aspect ratio when generating
parser.add_argument(
    "-as", "--aspect",
    help = "By default the aspect ratio is not respected. When argument set the aspect ratio of the original file is respected.",
    action = "store_false"
)

## Set line size (or width of the image)
parser.add_argument(
    "-w", "--width",
    help = "Specify the width of the image that should be generated",
    action = "store",
    type = int,
)

## Set column size (or height) of the image
parser.add_argument(
    "-he", "--height",
    help = "Set the height of the image that will be generated",
    action = "store", 
    type = int,
)

""" [6] Run / generate CLI """
args = parser.parse_args()

""" [7] Validations """
### Type = IMAGE / image
if ( args.type.lower() == "image"):
    
    print("arguments:")
    print(args)

    ## Print introduction of the options in question
    type_introduction = type.get(args.type, "")
    print(type_introduction) # Print the introduction message

    ## Validate if the path name exists
    path = Path(args.path) # Get path name entered by the user

    ## Source file exists
    if ( path.is_file() == True):
        print(f"Source file exists")

        # Image default override
        ascii.color = args.color
        ascii.respect_aspect_ratio = args.aspect
        ascii.line_size = args.width
        ascii.column_size = args.height

        # Generate ASCII image
        ascii.print_image(
            ascii.create(image_file = path)
        )

    ## Source file does not exist
    else:
        print(f"Source file does not exist. Please try again.")

else:
    ## Type does not exist
    print( f"This type does not exist. Please try [image, text]")