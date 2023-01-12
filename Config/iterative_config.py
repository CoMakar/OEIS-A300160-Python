MIN_DIGITS      = 2
MAX_DIGITS      = 16
PROCESSES       = 6

UPPER_EXP_LIMIT = 10
LOWER_EXP_LIMIT = 1
LOOKUP_SIZE     = 256


# ####################################################################################################################
assert LOOKUP_SIZE > MAX_DIGITS + UPPER_EXP_LIMIT + 1,  "Increase const.LOOKUP_SIZE"
assert PROCESSES >= 1,                                  "const.PROCESSES must be  at least 1"
assert MIN_DIGITS >= 2,                                 "const.START_DIGITS must be greater than 2"
assert MAX_DIGITS >= MIN_DIGITS,                        "const.MAX_DIGITS must be greater ot equal const.MIN_DIGITS"
assert MIN_DIGITS - LOWER_EXP_LIMIT >= 0,               "Increase const.MIN_DIGITS or decrease const.LOWER_EXP_LIMIT"
