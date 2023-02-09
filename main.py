import json
import os
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from math import ceil
from time import sleep
from typing import List, Union


from Common.DontInterrupt import DontInterrupt
from Common.term import *


#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    This file serves as the entry point for the program. It provides a terminal interface for every feature in the
#    project, however everything can run without it.
#
#   What about this file - it is behemoth abomination of code what works. To be honest, at some point I just wanted to
#   complete this TUI and I did not care about anything else. At least all code is devided into sections and commented.
# 
#--------------------------------------------------------------------------------------------------------------------------


#SECTION - Config
#ANCHOR - Paths
APP = os.path.dirname(__file__) # <root>/
CFG = f"{APP}\\Config"          # <root>/<Config>
DMP = f"{APP}\\dumps"           # <root>/<dumps>

#ANCHOR - Text formats 
WhiteBlueBold =     Format(FG.WHITE, BG.BLUE, STYLE.BOLD)
BlackYel =          Format(FG.BLACK, BG.YEL)
BlackRed =          Format(FG.BLACK, BG.RED)
BlackGreen =        Format(FG.BLACK, BG.GREEN)
GreenBlinking =     Format(FG.GREEN, style=STYLE.BLNK)
WhiteItalic =       Format(FG.WHITE, style=STYLE.ITALIC)
Blue =              Format(FG.BLUE)
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Interfaces
class IContext:
    """
    basic context interface
    must implement execute() function
    """
    def execute(self) -> "IContext":
        """
        must return other context to execute or None
        """
        raise NotImplementedError


class IRenderable:
    """
    interface for renderable elements
    must implement render() function
    """
    def render(self):
        raise NotImplementedError
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Base classes
@dataclass
class Option:
    """
    class container for pairs (value/key -> Context)
    text is what will be displayed
    """
    value: str
    context: IContext
    text: str
 

class OptionList():
    def __init__(self, options: List[Option]):
        self.entries = options
        self.contexts = {
            o.value: o.context for o in self.entries
        }
        
    def get_context(self, option_val: str):
        """
        returns context for given option value, None if not found
        """
        return self.contexts.get(option_val, None)

            
class Command:
    """ 
    Command in form of (operation, arg1 .. argN):
        does nothing itself, just provides convenient data validation and storage;
        supports parsing string with arguments type given (same type for all);
        object constructor supports Command.Arg.ANY as an argument for template creation
    """

    class Arg(Enum):
        """
        abstract argument type, used for template creation
        """
        ANY = 0
        
        def __repr__(self) -> str:
            return f"Command.Arg.{self.name}"
    
    _OP_DELIM = "@"
    _ARG_DELIM = ","
    _repr = ""
    _str = ""
    
    def __init__(self, operation: str, *argv):
        """
        takes operation string and n numbers of comand arguments;
        argumnets can be of any type however parse_command() function can handle only arguments of single type
        (for custom type handling use str type and implement you own logic)
        
        """
        if not isinstance(operation, str):
            raise TypeError("Operation must be a string value")        
        if operation == "":
            raise ValueError("Operation field cannot be empty")
        
        self._operation = operation
        self._args = argv if argv else None
        
        arg_str = Command._ARG_DELIM.join(map(repr, argv)) if argv else "None"
        self._str = f"{operation}{Command._OP_DELIM}{arg_str}"
        
        arg_repr = f"{Command._ARG_DELIM} ".join(map(repr, argv)) if argv else ""
        self._repr = f"Command({repr(operation)}, {arg_repr})"
        
    def parse_command(raw: str, type: Union[int, str, float, bool] = str) -> "Command":
        """
        if invalid type is given, TypeError is raised;
        if argument cannot be treated as given type ValueError is raised.
        @returns Command instance
        """
        
        allowed_type = (int, str, float, bool)
        
        if type not in allowed_type:
            raise TypeError("Unsupported argument type")

        operation, _, tokens = raw.partition(Command._OP_DELIM) 
        # separate operation from arguments
        try:
            tokens = [type(t) for token in tokens.split(Command._ARG_DELIM) if (t := token.strip()) != ""]
            # splits remaining string into tokens. if type specified, then converts tokens to given type  
        except ValueError:
            raise ValueError(f"Arguments must be valid {type.__name__} values")

        return Command(operation, *tokens)
        
    def count_args(self):
        """
        @returns number of arguments or 0 if arguments is None
        """
        return len(self._args) if self.args_exists() else 0
    
    def args_exists(self):
        """
        @returns boolean
        """
        return True if self._args is not None else False
     
    def get_args(self):
        """
        @returns list of arguments
        """
        return self._args
    
    def get_operation(self):
        """
        @returns operation string
        """
        return self._operation
    
    def __repr__(self) -> str:
        return self._repr
    
    def __str__(self) -> str:
        return f"{self._str}"
    
    def __eq__(self, obj) -> bool:
        """
        two commands are equal if they have same operation and same arguments
        | or |
        Command.Arg.ANY is always considered equal to any other argument
        """
        if isinstance(obj, Command):
            args_eq = self.count_args() == obj.count_args() 
            if self.args_exists() and args_eq:
                args_eq = all([(arg1 == arg2 or arg1 == Command.Arg.ANY or arg2 == Command.Arg.ANY) for arg1, arg2 in zip(self._args, obj._args)])
            return self._operation == obj._operation and args_eq

        return False


class Folder:
    """
    stub class for folder renderer class
    """
    def __init__(self, folder):
        self.folder = folder
        
    def ls(self):
        return os.listdir(self.folder)
    

class File:
    """
    stub class for file renderer class
    """
    def __init__(self, file_path):
        self.file_path = file_path
        
    def read_file_lines(self):
        with open(self.file_path) as file:
            lines = file.readlines()
        
        return lines    
#---------------------------------------------------------------------------
#!SECTION
  

#SECTION - Renderable elements
#ANCHOR - Render folder
class RFolder(IRenderable):
    def __init__(self, folder):
        self.folder = Folder(folder)

    def render_folder_ls(self):
        files = self.folder.ls()
        
        for n, file in enumerate(files):
            writef(f"{n}. ", WhiteItalic)
            write(f"{file}\n")
            
    def render(self):
        self.render_folder_ls()
        

#ANCHOR - Render full with textbox element
class RFullWideLabel(IRenderable):
    def __init__(self, msg: str, y0: int, y1: int):
        if y1 <= y0:
            raise ValueError("y1 must be greater than y0")
        
        self.y0 = y0
        self.y1 = y1
        self.msg = msg
    
    def render_fw_label(self):
        size = os.get_terminal_size()
        textbox(self.msg, 1, self.y0, size.columns, self.y1)   
        
    def render(self):
        self.render_fw_label()    
    

#ANCHOR - Render warning message
class RWarning(RFullWideLabel):
    def __init__ (self, msg: str):
        super().__init__(msg, Scr.maxy()-5, Scr.maxy()-2)

    def render(self):
        set_color(BlackYel.fg, BlackYel.bg)
        self.render_fw_label()
        Scr.reset_mode()
            

#ANCHOR - Render info message    
class RInfo(RFullWideLabel):
    def __init__ (self, msg: str):
        super().__init__(msg, Scr.maxy()-5, Scr.maxy()-2)

    def render(self):
        set_color(WhiteBlueBold.fg, WhiteBlueBold.bg)
        self.render_fw_label()
        Scr.reset_mode()
        

#ANCHOR - Render error message
class RError(RFullWideLabel):
    def __init__ (self, msg: str):
        super().__init__(msg, Scr.maxy()-5, Scr.maxy()-2)

    def render(self):
        set_color(BlackRed.fg, BlackRed.bg)
        self.render_fw_label()
        Scr.reset_mode()
        

#ANCHOR - Render success message    
class ROk(RFullWideLabel):
    def __init__ (self, msg: str):
        super().__init__(msg, Scr.maxy()-5, Scr.maxy()-2)

    def render(self):
        set_color(BlackGreen.fg, BlackGreen.bg)
        self.render_fw_label()
        Scr.reset_mode()
            
#ANCHOR - Render input field  
class RInput(IRenderable):
    """
    renders '>' ar (x, y) position
    read function moves cursor back to saved position and returns user input
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def render(self):
        Cur.to(self.y, self.x)
        writef(">", GreenBlinking)
        
    def read(self) -> str:
        Cur.to(self.y, self.x)
        Cur.right(2)
        userin = input()
        return userin

#ANCHOR - Render file lines
class RFile(IRenderable):
    def __init__(self, file_path):
        self.file = File(file_path)
        
    def render_file(self):
        try:
            lines = self.file.read_file_lines()
        except FileExistsError as e:
            line = []
            writef(f"ERROR: {self.file_path}: {e}", BlackRed)
            
        for n, line in enumerate(lines, 1):
            writef(f"{f'{n}.':<5}", WhiteItalic)
            write(f"{line}")
            
    def render(self):
        self.render_file()


#ANCHOR - Render options list
class ROptionsList(IRenderable):
    def __init__(self, options_list: OptionList):
        self.options_list = options_list

    def render_options(self, label_width: int = 8, loffset: int = 1,
                        multi_col: bool = True, coffset: int = 8):
        options = self.options_list.entries #shortening
        if multi_col:
            # calcluates is it possible to print in 2 columns
            # and if so -> sets var jump_at to an element at which should jump to 2nd column
            longest_line = sorted(options, key=lambda o: len(o.text) + len(o.value), reverse=True)[0]
            second_col = len(longest_line.text) + len(longest_line.value) + label_width + coffset
            size = os.get_terminal_size()
            jump_at = ceil(len(options) / 2) if size.columns > second_col * 2 else -1
            
        for c, option in enumerate(options):
            if c == jump_at:
                Cur.to(0, second_col)
            Cur.pos_save()
            writef(f" | {option.value:<{label_width}}> ", WhiteBlueBold)
            Cur.right(loffset)
            write(f": {option.text}")
            Cur.pos_restore()
            Cur.down()

    def render(self):
        self.render_options()
        

class REnum(IRenderable):
    def __init__(self, items: List):
        self.items = items
          
    def render_enum(self):
        items = self.items
        for i, item in enumerate(items):
            writef(f" {i} ", WhiteBlueBold)
            write(f": {item}\n")
      
    def render(self):
        self.render_enum()
#---------------------------------------------------------------------------
#!SECTION


#SECTION - Contexts
#ANCHOR - Options context (Super class)
class OptionsContext(IContext):
    #NOTE - uses warning, input field, options list elements
    def __init__(self, warning_msg: str = None):
        self.warning = RWarning(warning_msg)
        self.input_field = RInput(1, Scr.maxy() - 1)
        self.options_list: ROptionsList
    
    def options(self) -> OptionList:
        """
        uses function to get the list of options because 
        class variable is initialized with class, 
        so jumping between 2 contexts will be impossible
        """
        raise NotImplementedError

    def select_option(self) -> IContext:
        options = self.options()
        self.options_list = ROptionsList(options)
        Scr.clear_os()
        self.options_list.render()
        
        if self.warning.msg:
            self.warning.render()
            
        self.input_field.render()
        
        option = self.input_field.read()
        context = options.get_context(option) 

        if context is not None:
            return context
        else:
            # returns the same context from which it was called
            return type(self)(f"Invalid option -> {option}")
      

#ANCHOR - Config editor
class ConfigEdit(IContext):
    #NOTE - uses warning, error, info, success, input, enum elements
    def __init__(self, cfg_name: str, validator: str, 
                 warning_msg: str = None, error_msg: str = None, ok_msg: str = None):
        """
        cfg_name - name of config file
        validator - name of python script what validates corresponding config
        """    
    
        self.warning = RWarning(warning_msg)
        self.error = RError(error_msg)
        self.ok = ROk(ok_msg)
        self.info = RInfo("Usage: b -> back  |  a@n,value -> set config[n] = value")
        self.input_field = RInput(1, Scr.maxy() - 1)
        self.enum: REnum
        
        self.cfg_name = cfg_name
        self.validator = validator
                
    def ensure(self):
        """
        make sure the file exists
        returns error message if they are present
        """
        s = subprocess.run([sys.executable, self.validator], capture_output=True)
        return s.stdout.decode("utf-8")
                     
    def execute(self):
        assign = Command("a", Command.Arg.ANY, Command.Arg.ANY)
        back = Command("b")
        
        self.ensure()
        with open(self.cfg_name, 'r') as config_file:
            config: dict = json.load(config_file)
            
        self.enum = REnum([f"{i[0]:>16} = {fg(FG.YEL)}{i[1]}{fg(FG.DEF)}" for i in config.items()])
        Scr.clear_os()
        self.enum.render()
        
        if self.error.msg:
            self.error.render()
            sleep(4)
            
        if self.ok.msg:
            self.ok.render()
            sleep(0.5)
            
        if self.warning.msg:
            self.warning.render()
            sleep(2)
            
        self.info.render()
        self.input_field.render()

        try:
            command = Command.parse_command(self.input_field.read(), int)
        except ValueError as e:
            return ConfigEdit(self.cfg_name, self.validator, str(e))

        if command == back:
            return ConfigOptions()
        elif command == assign:
            index, value = command.get_args()
            key_list = config.keys()
            if index <= len(key_list) - 1:
                key =  tuple(key_list)[index]
                config[key] = value
                with open(self.cfg_name, 'w') as config_file:
                    config_file.write(json.dumps(config, indent=4))
                msg = self.ensure()
                # if no error message returned everything is fine
                if msg:
                    return ConfigEdit(self.cfg_name, self.validator, error_msg=f"ERROR: {msg.strip()}")
                else:
                    return ConfigEdit(self.cfg_name, self.validator, ok_msg="OK")
            else:
                return ConfigEdit(self.cfg_name, self.validator, "Invalid n")

        else:
            return ConfigEdit(self.cfg_name, self.validator, f"Invalid command -> {command}")
            

#ANCHOR - View dump file
class DumpFile(IContext):
    #NOTE - uses file, input elements
    def __init__(self, file_path):
        self.file = RFile(file_path)
        self.input_field = RInput(1, Scr.maxy() - 1)
        
    def execute(self):
        Scr.clear_os()   
        self.file.render()
        Cur.lf(3)
        
        write("Press enter to continue...")
        
        self.input_field.render()
        self.input_field.read()

        return DumpsList()
        

#ANCHOR - List of dump files
class DumpsList(IContext):
    #NOTE - uses warning, folder, input elements
    #NOTE - workdir -> DMP
    def __init__(self, warning_msg: str = None) -> None:
        self.warning = RWarning(warning_msg)
        self.folder = RFolder(DMP)
        self.input_field = RInput(1, Scr.maxy() - 1)
    
    
    def execute(self):
        view = Command("v", Command.Arg.ANY)
        back = Command("b")
        
        os.chdir(DMP)
        
        Scr.clear_os()       
        self.folder.render()
        Cur.lf()
    
        write("Usage: b -> back  |  v@n -> view file[n]")
        
        if self.warning.msg:
            self.warning.render()
            Cur.lf()
        
        self.input_field.render()
        
        try:
            command = Command.parse_command(self.input_field.read(), int)
        except ValueError as e:
            return DumpsList(str(e))
        
        if command == back:
            return DumpsOptions()
        elif command == view:
            index = command.get_args()[0]
            files = self.folder.folder.ls()
            if index <= len(files) - 1:
                return DumpFile(f"{DMP}\\{files[index]}")
            else:
                return DumpsList("Invalid n")
        else:
            return DumpsList(f"Invalid command -> {command}")

        
#ANCHOR - List of available dump files operations
class DumpsOptions(OptionsContext):
    #NOTE - workdir -> APP
    def options(self) -> OptionList:
        return OptionList([
            Option("collect", CollectDumps(), "Collect all available dumps - compress all significant data in one file"),
            Option("list", DumpsList(), "List all available dumps"),
            Option("back", Main(), "<-")
        ])
    
    def execute(self):
        os.chdir(APP)
        if not os.path.exists(DMP):
            return Main("`dumps` directory does not exist")
        return self.select_option()
    

#ANCHOR - List of available config files operations
class ConfigOptions(OptionsContext):
    #NOTE - workdir -> CFG
    def options(self):
        return OptionList([
            Option("iter", ConfigEdit("iterative_config.json", "iterative_config.py"), "Open configuration for iterative method configuration"),
            Option("direct", ConfigEdit("direct_config.json", "direct_config.py"), "Open configuration for direct method"),
            Option("back", Main(), "<-")
    ])
    
    def execute(self):
        os.chdir(CFG)
        return self.select_option()
      

#SECTION - Executable contexts
#ANCHOR - Help menu
class Help(OptionsContext):
    def options(self):
        return OptionList([
            Option("hiw", HowIterWorks(), "Show how the iterative method works"),
            Option("vnpi", NPInfo(), "Interactive information about near power numbers"),
            Option("back", Main(), "<-")
        ])
        
    def execute(self):
        return self.select_option()
    
    
#ANCHOR - Exit 
class Exit(IContext):
    def execute(self):
        exit(1)   
    
    
#ANCHOR - Runs help_collect_dumps.py
class CollectDumps(IContext):
    def execute(self):
        with DontInterrupt():
            subprocess.run([sys.executable, "help_collect_dumps.py"])
        return DumpsOptions()


#ANCHOR - Runs help_how_iterative_works.py
class HowIterWorks(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "help_how_iterative_works.py"])
        return Help()
    
#ANCHOR - Runs help_near_power_info.py
class NPInfo(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "help_near_power_info.py"])
        return Help()
        

#ANCHOR - Runs solver_direct_exhaust_search.py
class SolverExhaust(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "solver_direct_exhaust_search.py"])
        return Main()


#ANCHOR - Rund solver_direct_sfunc.py
class SolverSfunc(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "solver_direct_sfunc.py"])
        return Main()


#ANCHOR - Rund solver_iterative.py
class SolverIter(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "solver_iterative.py"])
        return Main()


#ANCHOR - Runs solver_iterative_mult.py 
class SolverIterMulti(IContext):
    def execute(self):
        with DontInterrupt():
            writef("Press Ctrl+C to stop at any moment\n", Blue)
            subprocess.run([sys.executable, "solver_iterative_multi.py"])
        return Main()
    
    
#ANCHOR - Main context
class Main(OptionsContext):
    #NOTE - workdir -> APP
    def options(self):
        return OptionList([
            Option("exh", SolverExhaust(), "Run Exhaust search method"),
            Option("sfunc", SolverSfunc(), "Run S-Func method"),
            Option("iter", SolverIter(), "Run Iterative method"),
            Option("mter", SolverIterMulti(), "Run Iterative method (multithreaded)"),
            Option("config", ConfigOptions(), "Edit configuration files"),
            Option("dump", DumpsOptions(), "View dump files" ),
            Option("help", Help(), "Show help"),
            Option("exit", Exit(), "exit")
    ])
    
    def execute(self):
        os.chdir(APP)
        return self.select_option()
#!SECTION
#!SECTION


def main():
    try:
        #FIXME - I DONT KNOW HOW THIS COMMAND WILL WORK ON UNIX SYSTEMS,
        #        BUT ON WINDOWS THIS COMMAND IS NEEDED TO MAKE THINGS WORK RIGHT
        os.system("color")
    except Exception:
        ...
        
    Scr.clear_os()   
    Cur.hide()    
    
    context = Main()
    try:
        while context is not None:
            context = context.execute()
    except (KeyboardInterrupt, EOFError):
        ...


if __name__ == "__main__":
    main()
