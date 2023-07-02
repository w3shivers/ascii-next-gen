### IMPORTS ###
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from os import get_terminal_size
import os.path

### Configuration / Default Values ###
size = get_terminal_size()
ascii = AsciiArt()
ascii.color = True

### Create a new CLI Object ###
parser = argparse.ArgumentParser(

    ## Program name
    prog = "ASCII Image Generator",

    ## Add program description
    description = "Convert any image into an ASCII image",

    ## Footer
    epilog = "v0.0.1 Copyright Rudi and Yolinda",   

)

### Create argument groups ###
required = parser.add_argument_group( "Required Argument(s)")

### Add arguments ###
required.add_argument("FileName")

### Parse Arguments ###
args = parser.parse_args()

### Execute if the Filename is not empty ###
if ( args.FileName != "" ):
    
    ## Get the identified file ##
    does_file_exist = os.path.isfile( args.FileName )

    ## Trigger action if file exists ##
    if ( does_file_exist == True ):

        ## Create a new file
        art = ascii.create(
            image_file = args.FileName
        )
    
    ## Create and print the image
    # test_images/cat.jpg
    ascii.print_image( art )

## Print error if file does not exist
else:
    print(f"The {args.FileName} does not exist. Please try again.")
