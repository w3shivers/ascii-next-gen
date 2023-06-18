from enum import Enum

class ResizeType(Enum):
    exact_size = 'exact'
    percentage_size = 'percentage'

class ColumnLineRatio(Enum):
    """ Pixel to ASCII ratio.
     In order to keep the aspect ratio of an image 
     to character. Doing this in case some cli's
     processes this ratio differently. """
    half = 2 