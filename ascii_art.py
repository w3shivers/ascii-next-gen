from PIL import Image
from webcolors import rgb_to_hex
from rich import print as print_ascii
from os import get_terminal_size
from library.enums import ResizeType as EnumResizeType

class AsciiArt():
    """ The AsciiArt object is only for generating
    images into ASCII art. The object does offer
    the following customizable options:
     """
    __ascii_characters: str = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    color: bool = True
    """ color: bool (Default True)
     - True = ASCII art will output with color.
     - False = ASCII art will only output characters 
       in CLI standard text color. """
    single_character: str|None = None
    resize_type: str = EnumResizeType.percentage_size.value
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
        if self.resize_type == EnumResizeType.exact_size.value:
            width, height = self.__determine_exact_size(image_width=image.width, image_height=image.height)
        else:
            width, height = self.__determine_adaptive_size(image_width=image.width, image_height=image.height)
        image = image.resize((width, height))
        ascii_lines = self.__convert_to_ascii_art(image=image)
        return '\n'.join(ascii_lines)

    def __determine_exact_size(self, image_width: int, image_height: int) -> tuple:
        width = image_width
        height = image_height
        if not self.respect_aspect_ratio:
            if self.column_size:
                width = self.column_size
            if self.line_size:
                height = self.line_size
            return (self.column_size, self.line_size)
        else:
            height = image_height / 2
        return width, height

    def __determine_adaptive_size(self, image_width: int, image_height: int) -> tuple:
        width = image_width
        height = image_height / 2
        terminal_size = get_terminal_size()
        image_ratio = image_height / image_width
        terminal_ratio = ( terminal_size.lines * 2 ) / terminal_size.columns
        if terminal_ratio < image_ratio: # adapt by height
            height = terminal_size.lines
            width = ( height / image_ratio ) * 2 
        else: # adapt by width
            width = terminal_size.columns
            height = ( width * image_ratio ) / 2
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

if __name__ == '__main__':
    ascii = AsciiArt()
    ascii.color = True
    ascii.single_character = '#'
    ascii.resize_type = EnumResizeType.exact_size.value
    ascii.respect_aspect_ratio = False
    ascii.line_size = 50
    ascii.column_size = 100
    ascii.print_image(
        # ascii.create(image_file='walking_duck_frames/23.jpg')
        ascii.create(image_file='test_images/cat.jpg')
    )
    # ascii.print_image(
    #     ascii.create(image_file='walking_duck_frames/25.jpg', width=70, height=35)
    # )