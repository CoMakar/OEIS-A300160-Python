import itertools as ittls
from Common.Printer import Printer
           

def help_me_to_understand(num_len=2, exponent=2):
    cowr = list(ittls.combinations_with_replacement([d**exponent for d in range(9+1)], num_len))
    cowrs = list(map(sum, cowr))
    cowrf = list(filter(lambda l: len(str(l)) == num_len, cowrs))
    cowrn = list(map(lambda l: (l-1, l+1), cowrf))
    cowrc = list(ittls.chain.from_iterable(cowrn))
    cowrcset = set(cowrc)
    
    
    printer = Printer(4, 16)
    
    
    print()
    print(f"(cowr)          (amount = {len(cowr)}; 100%)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowr)
    else:
        print("...")
    
    print()
    print(f"(cowrs)         (amount = {len(cowrs)}; {len(cowrs) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrs)
    else:
        print("...")    
        
    print()
    print(f"(cowrf)         (amount = {len(cowrf)}; {len(cowrf) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrf)
    else:
        print("...")    
    
    print()
    print(f"(cowrn)        (amount = {len(cowrn)}; {len(cowrn) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrn)
    else:
        print("...")
    
    print()
    print(f"(cowrc)       (amount = {len(cowrc)}; {len(cowrc) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrc)
    else:
        print("...")   
    
    print()
    print(f"(cowrcset)    (amount = {len(cowrcset)}; {len(cowrcset) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrcset)
    else:
        print("...")
        
    num_of_num_of_len_n = 9 * 10**(num_len-1)
    print()
    print(f"There are {num_of_num_of_len_n} number of length {num_len}.")
    print(f"For the exponent = {exponent}:")
    print(f"    We only need to process {len(cowrcset)} (unique values) or {len(cowrc)} (with duplicates) of them.")
    print(f"    These are {len(cowrcset) / num_of_num_of_len_n * 100:.8f}% and {len(cowrc) / num_of_num_of_len_n * 100:.8f}% of {num_of_num_of_len_n} respectively.")
