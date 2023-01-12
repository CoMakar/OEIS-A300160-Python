from Common.printer import Printer
from Common.validators import is_np_num, is_np_num_exp


def show_details(num: int, more: bool = False, show_table: bool = False):
    valid = None
    only_ones = False
    details = {}
    exp = 0
    tail = body = -1
    
    info_printer = Printer(2, 32)
    print_info = info_printer.printf
    
    digits = tuple(map(int, [*str(num).replace('0', '')]))
        
    if more:
        print(f"VALUE: {num}")
        print(f"FORMATED: {digits}")
    else:
        print_info(["VALUE:", num])    
        print_info(["FORMATED:", digits])
    
    
    if set(digits) == {1}:
        print("FORMATED NUMBER CONTAINS ONLY 1's")
        valid = False
        only_ones = True
    
    if not only_ones:
        if more:
            print("VALIDATION LOOP:")
        while True:
            digits_pow = [d**exp for d in digits]
            sum_value = sum(digits_pow)
            
            if more:
                print(f"\tEXP: {exp}, SUM: {sum_value}")
                print("\tDIGITS:\n ", '\n'.join(map(lambda v: f'\t\t{v}', digits_pow)))
            
            details[exp] = {"digits": digits_pow, "sum_value": sum_value}
            
            if sum_value in (num + 1, num - 1):
                if more:
                    print("\tNUMBER IS A VALID NEAR POWER NUMBER")
                valid = True
                break
            elif exp == tail:
                if more:
                    print(f"\tLOOP STATE DETECTED")
                valid = False
                break

            body, tail = exp, body
            
            if sum_value < num:
                if more:
                    print("\tEXP +1")
                exp += 1
            elif sum_value > num:
                if more:
                    print("\tEXP -1")
                exp -= 1
                
            if more:
                print()
    
    if not only_ones:     
        if more:
            print(f"VALID: {valid}")
        else:
            print_info(["VALID:", valid])
        
        if valid:
            info_short = f" + ".join(map(lambda v: f"{str(v)}^{exp}", digits)) + f" = {sum_value}"
            info_long = f" + ".join(map(lambda v: str(v**exp), digits)) + f" = {sum_value}"
            side = "-1" if num - 1 == sum_value else "+1"
    
            if more:
                print(f"SIDE: {side}")
                print(f"LENGTH: {len(str(num))}")
                print(f"EXPONENT: {exp}")
                print(info_short)
                print(info_long)
            else:
                print_info(["SIDE", side])
                print_info(["LENGTH", len(str(num))])
                print_info(["EXPONENT:", exp])
                print_info(["SHORT FORM:", info_short])
                print_info(["EXPANDED FORM:", info_long])
                
            
        if show_table:        
            print("TABLE:")
            
            digit_columns = len(digits)        
            arr_details = []
            for key in details.keys():
                arr_details.extend([key, *details[key]["digits"], details[key]["sum_value"]])
            
            if digit_columns <= 8:
                table_printer = Printer(digit_columns+2, 16, use_separator=True)
            else:
                table_printer = Printer(digit_columns+2, 16, use_separator=True, skip_columns=True, skip_from=3, skip_to=-2)   
                
            table_printer.printf(["exponent", "digits", *[""]*(digit_columns-1), "sum_value"])
            table_printer.printf(arr_details)
    
    
def get_np_exponent(num: int):
    if is_np_num(num):
        exp = 0
        while is_np_num_exp(num, exp) is not True: 
            exp += 1
        return exp
    return -1