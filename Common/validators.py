from Config.lookup_tables import pow_lookup
from typing import Iterable, List


def is_np_num_exp(num: int, exp: int) -> bool:
    """checks if the given pair(number, exponent) results a near power number
    
    Args:
        num (int): number to check
        exp (int): target exponent

    Returns:
        bool: is given number a near power number?
    """
    digits = map(int, [*str(num)])
    digits_sum = sum([pow_lookup[exp][i] for i in digits])
    
    return digits_sum in (num - 1, num + 1)


def is_np_num(num: int) -> bool:
    """checks if the given number is a near power number

    Args:
        num (int): nubmer to check

    Returns:
        bool: is given number a near power number?
    """
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
