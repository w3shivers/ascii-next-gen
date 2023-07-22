### Imports 
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from pathlib import Path

### Default variable
default_msg = True
ascii = AsciiArt()

### Initiate a new CLI
parser = argparse.ArgumentParser(
    prog = "Program name",
    description = "Description here", 
    epilog = "Footer here"
)

""" Positional Arguments """

### ASCII Type [image, animation, text]
parser.add_argument(
    "type",
    help = "Please specify an ASCII Type. Choice are [image, animation, text]",
)

### Define image path
parser.add_argument(
    "image_path",
    help = "Define the image path.",
)

""" Optional Arguments """
parser.add_argument(
    '-c', '--color',
    help = "Generate the image in color or black and white. [True, False]. Default = True",
    type = bool,
    default = True,
    choices = ['True', 'False'],
)

### Get arguments parsed by user 
args = parser.parse_args()

### Type set to IMAGE
if ( args.type.lower() == "image"):

    ### Define the image path
    if ( args.image_path != ""):
        img_path = Path(args.image_path)
        
        ### Image path exists
        if ( img_path.is_file() == True):
            print(f"Image path exists")
            print(f"{args.color}")
            
            ### Options
            ascii.color = args.color

            ascii.print_image(
                ascii.create(image_file=img_path)
            )
    
    ### Image path empty
    else:
        print(f"image path empty")

### No type has been selected by the user
else:
    print(f"Oh No... Please specify a function or type you want to run. Options are: image")