## Import packages
import argparse
from ascii_art import AsciiArt
from library.enums import ResizeType
from os import get_terminal_size
import os.path

## TEMPORARY DEFAULTS
size = get_terminal_size()
ascii = AsciiArt()
ascii.color = True

## Create a new CLI object
parser = argparse.ArgumentParser(description="Display description here")

## Add new argument(s)
parser.add_argument("FileName")

## Generate parser
args = parser.parse_args()

## Execute if the Filename is not empty
if ( args.FileName is not "" ):
    
    #file_exists = exists(path_to_file)

    ## Confirm if the directory & image exists
    does_file_exist = os.path.isfile(args.FileName)

    if ( does_file_exist == True ):
        
        # Create a new file
        art = ascii.create(image_file=args.FileName)

        # Create and print the image
        # test_images/cat.jpg
        ascii.print_image(art)

    ## If the directory / image does not exist print error message
    else:
        print(f"The {args.FileName} does not exist. Please try again. ")