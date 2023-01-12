from Helpers.about_iterative_method import help_me_to_understand

def explain():
    print("explanation:")
    print("let k = num_len;")
    print("let n = exponent;")
    print("let DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9].")
    print("cowr        - generates all possible combinations of length k of DIGITS to the power of n;")
    print("cowrs       - sums combinations into integers;")
    print("cowrf       - filters out integers whose length corresponds to the k-length:")
    print("                 num: 35; exp: 2 -> 3^2 + 5^2 = 9 + 25 = 34    | condition met")
    print("                 num: 99; exp: 3 -> 9^2 + 9^2 = 81 + 81 = 162  | condition not met")
    print("cowrn       - generates neighboring values;")
    print("cowrc       - chains them into a 1dim sequence;")
    print("cowrcset    - removes all duplicates")
    print("* Removing duplicates via set function requires a lot of RAM for long numbers, so this technique is not used to make calculations RAM `friendly`")
    
    input("> ...")
    
    print(f"{'SHORT NUMBERS':-^32}") 
    print(f"{'LEN:2 | EXP:2':-^32}") 
    help_me_to_understand(2,2)
    
    input("> ...")
    
    print(f"{'LEN:2 | EXP:3':-^32}") 
    help_me_to_understand(2,3)
    
    input("> ...")
    
    print(f"{'LEN:3 | EXP:3':-^32}") 
    help_me_to_understand(3,3)
    
    input("> ...")
    
    print(f"{'LONG NUMBERS':-^132}") 
    print(f"{'LEN:9 | EXP:9':-^32}") 
    help_me_to_understand(9,9)
    
    input("> ...")
    
    print(f"{'LEN:16 | EXP:16':-^32}") 
    help_me_to_understand(16,16)
    
    input("> ...")
    
    print(f"{'LEN:16 | EXP:26':-^32}") 
    help_me_to_understand(16,20)
        
    input("> ...")
    

if __name__ == '__main__':
    try:
        explain()
    except KeyboardInterrupt:
        print("Interrupted...")