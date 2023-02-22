import itertools as ittls
from Config.lookup_tables import pow_lookup


#--------------------------------------------------------------------------------------------------------------------------
#                                                      FUNCTIONS
#--------------------------------------------------------------------------------------------------------------------------
def get_data_sample(num_len: int, exponent: int):
    """
    explanation:
    let k = num_len;
    let n = exponent;
    let DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9].
        cowr        - generates all possible combinations of length k of DIGITS to the power of n;
        cowrs       - sums combinations into integers;
        cowrf       - filters out integers whose length corresponds to the k-length;
        cowrn       - generates neighboring values;
       !cowrc       - chains them into the 1dim sequence; - DEPRECATED
        
    Generates:
        List[Tuple[int, int]]: pairs of integers that can be near power numbers
    """
    
    cowr = ittls.combinations_with_replacement(pow_lookup[exponent], num_len)
    
    cowrs = map(sum, cowr)

    cowrf = filter(lambda l: len(str(l)) == num_len, cowrs)

    cowrn = map(lambda l: (l-1, l+1), cowrf)
    
    #? chaining seems redundant and has been removed
    #? so now returns
    #? ((n-1, n+1), (m-1, m+1), ...)
    #? instead of
    #? (n-1, n+1, m-1, m+1, ....)
    #?
    #? for single threaded calculations it improves performance by 0.8-1%
    #? for multithreaded calculations no performance impact was noticed
    
    # cowrc = ittls.chain.from_iterable(cowrn)
    
    return cowrn
    