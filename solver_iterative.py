import os

from Common import linify
from Common.Printer import Printer
from Common.str_utils import log
from Common.Timer import Timer
from Common.validators import is_np_num_exp
from Config import iterative_config
from Iterative.near_power import get_data_sample


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    MIN_DIGITS      = iterative_config.MIN_DIGITS
    MAX_DIGITS      = iterative_config.MAX_DIGITS
    UPPER_EXP_LIMIT = iterative_config.UPPER_EXP_LIMIT
    LOWER_EXP_LIMIT = iterative_config.LOWER_EXP_LIMIT
    WIDTH           = os.get_terminal_size().columns // 2


    valid_numbers = []
    with Timer("MAIN"):
        try: 
            for digits in range(MIN_DIGITS, MAX_DIGITS + 1):
                print(f"#{'NLEN_'+str(digits):-^{WIDTH}}#")
                with Timer(f"nlen_{digits}"):  
                    for exponent in range(digits-LOWER_EXP_LIMIT, digits+UPPER_EXP_LIMIT+1):
                        with Timer(f"exp_{exponent}"):
                            
                            log(f"Processing: len={digits:<8} exp={exponent:<8}")
                            nums = get_data_sample(digits, exponent)
                            np_numbers = filter(lambda v: is_np_num_exp(v, exponent), nums)
                            valid_numbers.extend(list(np_numbers))
                                
            print(f"#{'END':-^{WIDTH}}#")
        
        except Exception as e:
            log(f"Something went wrong! Exception: {e}")
            raise e
        
        except KeyboardInterrupt:
            print(f"#{'INTERRUPTED':-^{WIDTH}}#")
    
    
    valid_numbers = sorted(set(valid_numbers))
    sum_value = sum(valid_numbers)
    
    
    print()
    
    
    printer = Printer(2, 40)
    
    print(f"#{'VALID NUMBERS':-^{WIDTH}}#")   
    printer.printf(["#"])
    printer.printf(linify(enumerate(valid_numbers, 1)))
        
    print(f"SUM = {sum_value}")
    
    input("> Press Enter to exit...")
    

if __name__ == "__main__":
    main()
