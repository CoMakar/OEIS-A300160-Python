import itertools as ittls


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
        cowrc       - chains them into the 1dim sequence;
    """  
    
    cowr = ittls.combinations_with_replacement([d**exponent for d in range(9+1)], num_len)
    
    cowrs = map(sum, cowr)

    cowrf = filter(lambda l: len(str(l)) == num_len, cowrs)

    cowrn = map(lambda l: (l-1, l+1), cowrf)
    
    cowrc = ittls.chain.from_iterable(cowrn)
    
    return cowrc
    