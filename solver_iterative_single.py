from Common.debug import linify, log
from Common.printer import Printer
from Common.timer import Timer
from Common.validators import is_np_num_exp
from Config import iterative_config
from Iterative.near_prime import get_data_sample


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    MIN_DIGITS =      iterative_config.MIN_DIGITS
    MAX_DIGITS =      iterative_config.MAX_DIGITS
    UPPER_EXP_LIMIT = iterative_config.UPPER_EXP_LIMIT
    LOWER_EXP_LIMIT = iterative_config.LOWER_EXP_LIMIT
    

    valid_numbers = []
    with Timer("MAIN"):
        try: 
            for digits in range(MIN_DIGITS, MAX_DIGITS + 1):
                print(f"{'NLEN_'+str(digits):-^64}")
                with Timer(f"nlen_{digits}"):  
                    for exponent in range(digits-LOWER_EXP_LIMIT, digits+UPPER_EXP_LIMIT+1):
                        with Timer(f"exp_{exponent}"):
                            
                            log(f"Processing: len={digits:<8} exp={exponent:<8}")
                            nums = get_data_sample(digits, exponent)
                            np_numbers = filter(lambda v: is_np_num_exp(v, exponent), nums)
                            valid_numbers.extend(list(np_numbers))
                                
            print(f"{'END':-^64}")
        
        except Exception as e:
            log(f"Something went wrong! Exception: {e}")
            raise e
        
        except KeyboardInterrupt:
            print(f"{'INTERRUPTED':-^64}")
    
    
    valid_numbers = sorted(set(valid_numbers))
    sum_value = sum(valid_numbers)
    
    
    print()
    
    
    print(f"{'VALID NUMBERS':-^128}")   
    printer = Printer(2, 40)
    printer.printf(["#"])
    printer.printf(linify(enumerate(valid_numbers, 1)))
        
    print(f"{'SUM':-^128}") 
    print(f"SUM = {sum_value}")
    
    input(">...")
    

if __name__ == "__main__":
    main()
