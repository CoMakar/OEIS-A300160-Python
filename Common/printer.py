import typing


#--------------------------------------------------------------------------------------------------------------------------
#                                                     CLASS
#--------------------------------------------------------------------------------------------------------------------------
class Printer:
    def __init__(self, columns: int = 1, width: int = 3,
                compress: bool = True, use_separator: bool = False,
                column_separator: str = "|", line_separator: str = "-", cross_separator: str = "+",
                autocomplete: bool = True, filler: str = " ",
                skip_columns: bool = False, skip_from: int = 2, skip_to: int = -1):
            """
            columns:        number of columns
            width:          width of each column
            compress:       if element length is greater than width it will be replace with `...`
            use_separator:  draws | between columns and - between lines
            autocomplete:   fills empty cells with filler value
            skip:           skips columns [skip_from, skip_to]
                            automatically disables if number of columns < 4 or skip_from == skip_to
            """
            width  = 3 if width < 3 else width
            skip_to = columns + skip_to if skip_to <= -1 else skip_to
            
            if columns < 1:
                raise ValueError("at least one column must be present")
            
            if skip_from == skip_to or columns < 4:
                skip_columns = False
            
            if skip_from > skip_to and skip_columns:
                raise ValueError(f"skip_from ({skip_from}) should be lower than skip_to ({skip_to})")
            if skip_to >= columns and skip_columns:
                raise ValueError(f"skip_to ({skip_to}) value cannot be greater than or equal to number columns ({columns})")
            if skip_from < 2 and skip_columns:
                raise ValueError(f"skip_from ({skip_from}) cannot be lower than 2")


            self.__columns       = columns
            self.__width         = width
            
            self.__compress      = compress
            
            self.__use_separator = use_separator
            self.__col_sep       = column_separator if use_separator else " "
            self.__line_sep      = line_separator
            self.__crs_sep       = cross_separator
            
            self.__autocomplete  = autocomplete
            self.__filler        = filler
            
            self.__skip_columns  = skip_columns
            self.__skip_from     = skip_from
            self.__skip_to       = skip_to
            
    
    
    def __print_frame(self, frame):
            free_space = self.__width - 3
            frame = str(frame)
            frame = f"{frame[0:free_space]}..." if len(frame) > self.__width and self.__compress else frame
            print(f"{str(frame):<{self.__width}}", end=self.__col_sep)
    
    
    def printf(self, data: typing.Iterable):
        skipped = self.__skip_to - self.__skip_from + 1 if self.__skip_columns else 1
        formated_line_separator = f"{self.__line_sep * self.__width}{self.__crs_sep}" * (self.__columns - skipped + 1)
        
        if self.__use_separator: 
            print(formated_line_separator)
        
        dots_printed = False
        lf_counter = 0
        for lf_counter, frame in enumerate (data, 1):
            if self.__skip_columns:
                if lf_counter % self.__columns >= self.__skip_from and lf_counter % self.__columns <= self.__skip_to:
                    if not dots_printed:
                        self.__print_frame("...")
                        dots_printed = True
                    continue
                
            self.__print_frame(frame)
            if lf_counter % self.__columns == 0:
                dots_printed = False    
                print()
                if self.__use_separator: 
                    print(formated_line_separator)
                    
        if lf_counter % self.__columns != 0 and self.__autocomplete:
            while lf_counter % self.__columns != 0:
                self.__print_frame(self.__filler)
                lf_counter += 1
            print()
        elif lf_counter % self.__columns != 0:
            print()
                
        if self.__use_separator: 
            last_line_separator = f"{self.__line_sep * self.__width}{self.__crs_sep}" * (lf_counter % self.__columns - self.__columns)
            print(last_line_separator, end="")
