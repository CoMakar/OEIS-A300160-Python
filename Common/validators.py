from Config.lookup_tables import pow_lookup


def is_np_num_exp(num: int, exp: int):
    digits = map(int, [*str(num)])
    digits_sum = sum([pow_lookup[exp][i] for i in digits])
    
    return digits_sum in (num - 1, num + 1)


def is_np_num(num: int):
    exp = 0
    tail = -1
    body = -1
    
    digits = tuple(map(int, [*str(num)]))
        
    if set(digits) == {1}:
        return False
    
    while True:
        digits_pow = [d**exp for d in digits]
        sum_value = sum(digits_pow)
        
        if sum_value in (num + 1, num - 1):
            return True
        elif exp == tail:
            return False

        body, tail = exp, body
        
        if sum_value < num:
            exp += 1
        elif sum_value > num:
            exp -= 1
