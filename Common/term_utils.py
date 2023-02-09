import os
import typing as types
from dataclasses import dataclass
from enum import Enum
from sys import stdout
from time import sleep
from typing import Union


#SECTION - Colors
class FG(Enum):
    """
    [FG] 8 classic colors enum
    """
    BLACK   = "\u001b[30m"
    RED     = "\u001b[31m"
    GREEN   = "\u001b[32m"
    YEL     = "\u001b[33m"
    BLUE    = "\u001b[34m"
    MAGNT   = "\u001b[35m"
    CYAN    = "\u001b[36m"
    WHITE   = "\u001b[37m"
    DEF     = "\u001b[39m"


class FGRGB:
    def __init__(self, r: int, g: int, b: int):
        """
        [FG] constructs color fomratting string rom RGB values
        """
        if not(0 <= r < 256 or 0 <= g < 256 or 0 <= b < 256):
            raise ValueError("Invalid RGB values")
        self.value = f"\u001b[38;2;{r};{g};{b}m"


class BG(Enum):
    """
    [BG] 8 classic colors enum
    """
    BLACK   = "\u001b[40m"
    RED     = "\u001b[41m"
    GREEN   = "\u001b[42m"
    YEL     = "\u001b[43m"
    BLUE    = "\u001b[44m"
    MAGNT   = "\u001b[45m"
    CYAN    = "\u001b[46m"
    WHITE   = "\u001b[47m"
    DEF     = "\u001b[49m"


class BGRGB:
    def __init__(self, r: int, g: int, b: int):
        """
        [BG] constructs color fomratting string rom RGB values
        """
        if not(0 <= r < 256 or 0 <= g < 256 or 0 <= b < 256):
            raise ValueError("Invalid RGB values")
        self.value = f"\u001b[48;2;{r};{g};{b}m"
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Style
class STYLE(Enum):
    RESET  = "\u001b[22m\u001b[23m\u001b[24m\u001b[25m\u001b[27m\u001b[28m\u001b[29m"
    # resets all active styles
    BOLD   = "\u001b[1m"
    ITALIC = "\u001b[3m"
    UNDER  = "\u001b[4m"
    BLNK   = "\u001b[5m"
    REVER  = "\u001b[7m"
    HIDEN  = "\u001b[8m"
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Screen
class Scr:
    def clear_os():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def clear():
        write("\u001b[2J\u001b[0;0H")

    def clear_line():
        write("\u001b[2K")

    def reset_mode():
        # resets all active styles and colors
        write("\u001b[0m")
        
    def maxx():
        return os.get_terminal_size().columns
    
    def maxy():
        return os.get_terminal_size().lines
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Cursor
class Cur:
    def up(n: int = 1):
        write(f"\u001b[{n}A")

    def down(n: int = 1):
        write(f"\u001b[{n}B")

    def left(n: int = 1):
        write(f"\u001b[{n}D")

    def right(n: int = 1):
        write(f"\u001b[{n}C")

    def prev_line(n: int = 1):
        write(f"\u001b[{n}F")

    def next_line(n: int = 1):
        write(f"\u001b[{n}E")

    def to(line: int, col: int):
        write(f"\u001b[{line};{col}H")
        
    def to_col(col: int):
        write(f"\u001b[{col}G")

    def home():
        write("\u001b[H")

    def hide():
        write("\u001b[?25l")

    def show():
        write("\u001b[?25h")

    def pos_save():
        write("\u001b[s")

    def pos_restore():
        write("\u001b[u")
        
    def lf(n: int = 1):
        write("\n" * n)
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Color/Style function
def fg(fgcol: Union[FG, FGRGB]):
    """
    @returns [FG] color string
    """
    return fgcol.value


def bg(bgcol: Union[BG, BGRGB]):
    """
    @returns [BG] color string
    """
    return bgcol.value


@dataclass
class Format:
    """
    Commonly used with writef() function
    """
    fg: Union[FG, FGRGB]      = FG.DEF
    bg: Union[BG, BGRGB]      = BG.DEF
    style: Union[STYLE, None] = None
    

def set_color(fg: Union[FG, FGRGB] , bg: Union[BG, BGRGB]  = BG.DEF):
    write(fg.value)
    write(bg.value)


def set_style(style: STYLE = STYLE.RESET):
    write(style.value)


def set_format(format: Format):
    if format.style:
        set_style(format.style)
    
    set_color(format.fg, format.bg)
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Write functions
def write(text: any = "\n"):
    """
    write with immediate flush
    """
    text = str(text)
    stdout.write(text)
    stdout.flush()


def writef(text: any, format: Format):
    """
    foramted write; automatically resets all styles and colors after writing
    """
    set_format(format)
    write(text)
    Scr.reset_mode()
    

def writew(text: types.Iterable = "\n", wait: float = 0.5, sep: str = ""):
    """
    write with sleep between chars
    """
    for char in text:
        write(f"{char}{sep}")
        sleep(wait)
        

def writebox(text: str, x0: int, y0: int, x1: int, y1: int):
    """
    Writes text in a bounding box; overflow is HIDDEN
    Args:
        text (str): text to be printed
        x0 (int): top left corner x
        y0 (int): top left corner y
        x1 (int): bottom right corner x
        y1 (int): bottom right cornre y
        
    Raises:
        ValueError: if box is too small
    """
    line_len = x1 - x0 + 1
    box_height = y1 - y0 + 1
    
    if box_height < 1 or line_len < 1:
        raise ValueError("box is too small")
        
    text = text.ljust(line_len * box_height, " ")
    # Fills the text with space to maintain formatting
    chunks = [text[i: i + line_len] for i in range(0, len(text), line_len)]
    Cur.to(y0, x0)
    for line, chunk in enumerate(chunks, 1):
        Cur.pos_save()
        write(chunk)
        Cur.pos_restore()
        Cur.down()
        if line > box_height:
            return
#---------------------------------------------------------------------------
#!SECTION
 
 
#SECTION - Draw functions
def drawline(char: str, x0: int, y0: int, x1: int, y1: int):
    """
    Bresenham's line algorithm
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1 + 1:
            Cur.to(y, x)
            write(char)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1 + 1:
            Cur.to(y, x)
            write(char)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy        
    
    
def drawbox(x0: int, y0: int, x1: int, y1: int):
    """
    Args:
        x0 (int): top left x
        y0 (int): top left y
        x1 (int): bottom right x
        y1 (int): bottom right y

    Raises:
        ValueError: if width/height is smaller than 1
                    or top left coordinates are out of bounds

    Returns:
        center: relative coordinates of the center of the box (y, x)
    """
    corners = "...."
    hor = "-"
    ver = "|"
    
    width = x1 - x0
    height = y1 - y0
    
    if width < 1 or height < 1:
        raise ValueError("Inappropriate size")
    
    if x0 < 1 or y0 < 1:
        raise ValueError("Out of bounds")
    
    center = (height // 2, width // 2)
    
    Cur.to(y0, x0)
    drawline(hor, x0, y0, x1, y0)
    drawline(ver, x1, y0, x1, y1)
    drawline(hor, x0, y1, x1, y1)
    drawline(ver, x0, y0, x0, y1)
    Cur.to(y0, x0)
    write(corners[0])
    Cur.to(y0, x1)
    write(corners[1])
    Cur.to(y1, x0)
    write(corners[2])
    Cur.to(y1, x1)
    write(corners[3])
    
    return center


def textbox(text: str, x0: int, y0: int, x1: int, y1: int):
    """
    writes text in a bounding box, draws box around it
    """
    drawbox(x0, y0, x1, y1)
    writebox(text, x0+1, y0+1, x1-1, y1-1)
#---------------------------------------------------------------------------
#!SECTION
