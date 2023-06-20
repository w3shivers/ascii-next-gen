from PIL import Image
from webcolors import rgb_to_hex
from rich import print as print_ascii
from os import get_terminal_size
from library.enums import ResizeType, ColumnLineRatio
from math import floor

class AsciiArt():
    """ The AsciiArt object is only for generating
    images into ASCII art. The object does offer
    the following customizable options:
     """
    __ascii_characters: str = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    __column_to_line_ratio = ColumnLineRatio.half.value
    color: bool = True
    """ color: bool (Default True)
     - True = ASCII art will output with color.
     - False = ASCII art will only output characters 
       in CLI standard text color. """
    single_character: str|None = None
    resize_type: str = ResizeType.percentage_size.value
    respect_aspect_ratio: bool = True
    line_size: int|None = 100
    column_size: int|None = 100
    max_line_size: int|None = None
    max_column_size: int|None = None
    min_line_size: int|None = None
    min_column_size: int|None = None

    def create(self, image_file: str) -> str:
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
            # Rudi still to finalize this.
            image_ratio = image_height / image_width
            terminal_ratio = ( terminal_lines * self.__column_to_line_ratio ) / terminal_columns
            if terminal_ratio < image_ratio: # adapt by height
                height = terminal_lines
                width = ( height / image_ratio ) * self.__column_to_line_ratio
            else: # adapt by width
                width = terminal_columns
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
        for y in range(0, height - 1):
            line = ''
            for x in range(0, width - 1):
                pixel = image.getpixel((x, y))
                # If user doesn't want color. Then we continue after adding char to line
                if not self.color:
                     line += self.__convert_pixel_to_character(pixel=pixel)
                     continue
                # If user wants color, then...
                character = self.__convert_pixel_to_character(pixel=pixel)
                hex_color = rgb_to_hex(pixel)
                if not line:
                    line += f'[{hex_color}]{character}'
                elif previous_color != hex_color:
                    line += f'[/][{hex_color}]{character}'
                else:
                    line += character
                previous_color = hex_color
            if not self.color:
                ascii_art.append(line)
                continue
            ascii_art.append(line + '[/]')
        return ascii_art

    def __convert_pixel_to_character(self, pixel: tuple) -> str:
        if self.single_character:
            character = str(self.single_character)[0]
        else:
            (r, g, b) = pixel
            pixel_brightness = r + g + b
            max_brightness = (255 * 3)
            brightness_weight = len(self.__ascii_characters) / max_brightness
            index = int(pixel_brightness * brightness_weight) - 1
            character = self.__ascii_characters[index]
        if self.color and character == '\\':
            character = '\\\\' # Have to double escape the backslash to ensure it doesn't escape any color tags.
        return character
    def print_image(self, ascii_art: str) -> None:
        # If not color use normal print
        if not self.color:
            print(ascii_art)
        else:
            print_ascii(ascii_art)