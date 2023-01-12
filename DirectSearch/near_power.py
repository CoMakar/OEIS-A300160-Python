import itertools as ittls


#--------------------------------------------------------------------------------------------------------------------------
#                                                     GLOBALS
#--------------------------------------------------------------------------------------------------------------------------
pow_dict = dict()
known_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
pow_arr = [None, known_digits]
max_k = 1
last_k = max_k


#--------------------------------------------------------------------------------------------------------------------------
#                                                     FUNCTIONS
#--------------------------------------------------------------------------------------------------------------------------
def exhaust_search(num: int):
    nums = list(map(int, [*str(num).replace('0', '')]))
    if nums.count(1) == len(nums): return False
    k = 1
    kbasesum = sum(nums)
    
    while kbasesum < num + 1 and kbasesum != num - 1:
        if k not in pow_dict.keys():
            pow_dict[k] = tuple(i**k for i in (1, 2, 3, 4, 5, 6, 7, 8, 9))
        kbasesum = sum([pow_dict[k][i-1] for i in nums])  
        k += 1 

    return kbasesum == num - 1 or kbasesum == num + 1


def exhaust_search_withCache(num: int):
    global max_k
    global last_k
    digits = list(map(int, [*str(num).replace('0', '')]))
    if set(digits) == {1}:
        return False

    k = last_k
    c0 = c1 = -1

    while True:
        kbasesum = sum([pow_arr[k][i] for i in digits])

        if k == c1:
            last_k = k
            return False
        elif kbasesum in (num - 1, num + 1):
            last_k = k
            return True

        c0, c1 = k, c0

        if kbasesum < num:
            k += 1
        elif kbasesum > num:
            k -= 1

        if k == max_k:
            max_k += 1
            pow_arr.append(list(map(lambda x: x**max_k, known_digits)))
            
        
def s_func(n: int, print_info: bool = False):
    valid_numbers = []
    for k in range(1, n+1):
        for power in range(max(1, k-2), k+2):  
            xmin = 2**power * k
            xmax = 9**power * k
             
            if len(str(xmin)) > k:
                continue
            if len(str(xmax)) < k:
                continue
            
            if print_info:
                print(f"Processing: len = {k};\t exp = {power}")

            powers = map(lambda x: [x, x**power], (range(0, 9+1)))
            combinations = ittls.combinations_with_replacement(powers, k)
            
            for c in combinations:
                xsum     = sum([i[1] for i in c])
                xsumadd1 = sorted(str(xsum+1))
                xsumsub1 = sorted(str(xsum-1))
                concat   = sorted([str(i[0]) for i in c]) 
                
                if (xsumadd1 == concat):
                    if print_info:
                        print(f"[+1] Found: {xsum+1}")
                    valid_numbers.append(xsum+1)
                
                if (xsumsub1 == concat):
                    if print_info:
                        print(f"[-1] Found: {xsum-1}")
                    valid_numbers.append(xsum-1)
    return valid_numbers
