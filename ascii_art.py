# Author: Rudi Esterhuysen <rudi.esterhuyzen@gmail.com>

""" AsciiArt NextGen

This module generates static images into ASCII images and offers the following customization options:
* Generate image in full color or the default CLI output color.
* Define the size of the ASCII image that should be generated.
* Generate image in a single character or several characters.

The following is a simple usage of the module::

    if __name__ == '__main__':
        ascii = AsciiArt()
        ascii.print_image(
            ascii.create(image_file='test_images/cat.jpg')
        )

This module holds the following class(es):
    
    - AsciiArt() -- Describe the class here

"""

from PIL import Image
from webcolors import rgb_to_hex
from rich import print as print_ascii
from os import get_terminal_size
from library.enums import ResizeType, ColumnLineRatio
from math import floor

class AsciiArt():
    """ The AsciiArt object generates images into ASCII
    art. The object offers several customization options.
    * color
    """
    __ascii_characters: str = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    __column_to_line_ratio = ColumnLineRatio.half.value
    color: bool = True
    """ color: bool (Default: True)

    Generate the ASCII image in full color or the standard output color. The following options are available:
        - True -- AsciiArt will be generated in full color.
        - False -- AsciiArt will be generated in the default output color of your CLI.
    """

    single_character: str|None = None
    """ single_character: str|None = None

    Defined characters will be used to generate the AsciiArt image. Single or multiple characters can be defined. The following default characters are set::
        `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$
    """

    resize_type: str = ResizeType.percentage_size.value
    """ resize_type: str = ResizeType.percentage_size.value

    Define the parameters that should be used to resize the AsciiArt image. Options are:
        - Percentage -- Resize the AsciiArt image using a percentage.
        - Size -- Resize the AsciiArt image by defining a width and height.
    """

    respect_aspect_ratio: bool = True
    """ respect_aspect_ratio: bool = True

    Generate the AsciiArt image to a specific size or adhering to the source files aspect ratio. The following options are available::
        - True -- If set to true the image is generated in a specific size.
        - False -- If set false the image is generated respecting the aspect ratio of the original image.
    """

    line_size: int|None = 100
    column_size: int|None = 100
    max_line_size: int|None = None
    max_column_size: int|None = None
    min_line_size: int|None = None
    min_column_size: int|None = None 
    __temp_count = 0

    def create(self, image_file: str) -> str:
        """ Create the AsciiArt image
        
        Run the method to generate the identified source file (or image) into an AsciiArt image. 

        """
    
        width = 0
        height = 0
        image = Image.open(image_file)
        if self.resize_type == ResizeType.exact_size.value:
            width, height = self.__determine_exact_size(image_width=image.width, image_height=image.height)
        else:
            width, height = self.__determine_adaptive_size(image_width=image.width, image_height=image.height)
        image = image.resize((width, height))
        ascii_lines = self.__convert_to_ascii_art(image=image)
        return '\n'.join(ascii_lines)

    def __determine_exact_size(self, image_width: int, image_height: int) -> tuple:
        width = image_width
        height = floor(image_height / self.__column_to_line_ratio) # calculate aspect ratio of image.
        image_ratio = height / width
        if self.column_size:
            width = self.column_size
        if self.line_size:
            height = self.line_size 
        if self.respect_aspect_ratio: # If aspect ratio isn't important to user.
            if (height > width):
                width = floor(height / image_ratio)
            else:
                height = floor(width * image_ratio)
        return width, height

    def __determine_adaptive_size(self, image_width: int, image_height: int) -> tuple:
        width = image_width
        height = image_height / 2
        terminal_size = get_terminal_size()
        terminal_lines = terminal_size.lines
        terminal_columns = terminal_size.columns
        # Adjust terminal to percentage size.
        if self.column_size:
            terminal_columns = terminal_columns * ( self.column_size / 100 )
        if self.line_size:
            terminal_lines = terminal_lines * ( self.line_size / 100 )
        # If aspect ratio needs to be adhered too.
        if self.respect_aspect_ratio: 
            """ TODO: Need to improve on this. There has to be a simpler way tp calculate
            this and also have it adhere to the min and max values better. """
            image_ratio = image_height / image_width
            terminal_ratio = ( terminal_lines * self.__column_to_line_ratio ) / terminal_columns
            width = terminal_columns
            if self.min_column_size and self.min_column_size > width:
                width = self.min_column_size
            elif self.max_column_size and self.max_column_size < width:
                width = self.max_column_size
            height = terminal_lines
            if self.min_line_size and self.min_line_size > height:
                height = self.min_line_size
            elif self.max_line_size and self.max_line_size < height:
                height = self.max_line_size
            if terminal_ratio < image_ratio: # adapt by height
                width = ( height / image_ratio ) * self.__column_to_line_ratio
            else: # adapt by width
                height = ( width * image_ratio ) / self.__column_to_line_ratio
            return (int(width), int(height))
        # If aspect ratio does not matter.
        width = terminal_columns
        height = terminal_lines
        # Adjust width if needed
        if self.max_column_size and width > self.max_column_size:
            width = self.max_column_size
        elif self.min_column_size and width < self.min_column_size:
            width = self.min_column_size
        # Adjust height if needed
        if self.max_line_size and height > self.max_line_size:
            height = self.max_line_size
        elif self.min_line_size and height < self.min_line_size:
            height = self.min_line_size
        return (int(width), int(height))

    def __convert_to_ascii_art(self, image: Image) -> list:
        previous_color = ''
        ascii_art = []
        (width, height) = image.size
        hex_color = None
        count = 0
        for y in range(0, height - 1):
            line = ''
            for x in range(0, width - 1):
                count += 1
                character, pixel = self.__convert_pixel_to_character(image=image, x=x, y=y)
                if self.color: # if user wants color.
                    hex_color = rgb_to_hex(pixel)
                if hex_color and not line:
                    line += f'[{hex_color}]{character}'
                elif hex_color and previous_color != hex_color:
                    line += f'[/][{hex_color}]{character}'
                else:
                    line += character
                previous_color = hex_color
            if not self.color:
                ascii_art.append(line)
                continue
            ascii_art.append(line + '[/]')
        print('total: ', count, '\nerrors:', self.__temp_count)
        return ascii_art

    def __convert_pixel_to_character(self, image: Image, x: int, y:int) -> tuple:
        pixel = image.getpixel((x, y))
        character = ' '
        (r, g, b, a) = self.__convert_pixel_to_rgba_color_profile(pixel=pixel)
        if a == 0: # If completely transparent 
            character = ' '
        else: 
            pixel_brightness = r + g + b
            max_brightness = (255 * 3)
            brightness_weight = len(self.__ascii_characters) / max_brightness
            index = int(pixel_brightness * brightness_weight) - 1
            if self.single_character:
                character = str(self.single_character)[0]
            character = self.__ascii_characters[index]
        if self.color and character == '\\':
            character = '\\\\' # Have to double escape the backslash to ensure it doesn't escape any color tags.
        return (character, (r, g, b))
    
    def __convert_pixel_to_rgba_color_profile(self, pixel: tuple) -> tuple:
        try: # Try RGB profile first
            (r, g, b) = pixel
            a = 1
        except ValueError: # Try RGBA profile
            (r, g, b, a) = pixel
            a = (a / 255)
            r = int(r * a)
            g = int(g * a)
            b = int(b * a)
        return (r, g, b, a) # Always return RGBA

    def print_image(self, ascii_art: str) -> None:
        # If not color use normal print
        if not self.color:
            print(ascii_art)
        else:
            print_ascii(ascii_art)