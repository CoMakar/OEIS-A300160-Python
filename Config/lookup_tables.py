from Config import iterative_config


pow_lookup = [[i**j for i in range(9+1)] for j in range(iterative_config.LOOKUP_SIZE)]
known_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
