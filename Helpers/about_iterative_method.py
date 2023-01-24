import itertools as ittls
from Common.printer import Printer
           

def help_me_to_understand(num_len=2, exponent=2):
    exp_lookup = [i**exponent for i in range(9+1)]
    cowr = list(ittls.combinations_with_replacement(exp_lookup, num_len))
    cowrf = list(filter(lambda l: len(str(sum(l))) == num_len, cowr))
    cowrfm = list(map(lambda l: (l-1, l+1), map(sum, cowrf)))
    cowrfmc = list(ittls.chain.from_iterable(cowrfm))
    cowrfmcset = set(cowrfmc)
    
    printer = Printer(4, 16)
    
    print()
    print(f"(cowr)          (amount = {len(cowr)}; 100%)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowr)
    else:
        print("...")
    
    print()
    print(f"(cowrf)         (amount = {len(cowrf)}; {len(cowrf) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrf)
    else:
        print("...")    
        
    
    print()
    print(f"(cowrfm)        (amount = {len(cowrfm)}; {len(cowrfm) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrfm)
    else:
        print("...")
    
    print()
    print(f"(cowrfmc)       (amount = {len(cowrfmc)}; {len(cowrfmc) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrfmc)
    else:
        print("...")   
    
    print()
    print(f"(cowrfmcset)    (amount = {len(cowrfmcset)}; {len(cowrfmcset) / len(cowr) * 100:.2f}% from base)")
    if (num_len <= 3 or exponent <= 3):
        printer.printf(cowrfmcset)
    else:
        print("...")
        
    num_of_num_of_len_n = 9 * 10**(num_len-1)
    print()
    print(f"There are {num_of_num_of_len_n} number of length {num_len}.")
    print(f"For the exponent = {exponent}:")
    print(f"    We only need to process {len(cowrfmcset)} (only unique values) or {len(cowrfmc)} (with duplicates) of them.")
    print(f"    It is {len(cowrfmcset) / num_of_num_of_len_n * 100:.2f}% and {len(cowrfmc) / num_of_num_of_len_n * 100:.2f}% of {num_of_num_of_len_n} respectively.")
