import json
from os import path, chdir
from time import sleep


config_standard = {
    "MIN_DIGITS"        : 2,
    "MAX_DIGITS"        : 6,
    "PROCESSES"         : 2,
    "UPPER_EXP_LIMIT"   : 10,
    "LOWER_EXP_LIMIT"   : 1,
    "LOOKUP_SIZE"       : 256
}
filename = "iterative_config.json"


CFG = path.dirname(__file__)
chdir(CFG)
try:
    with open(filename, 'r') as config_file:
        config: dict = json.load(config_file)
    
    if config.keys() != config_standard.keys():
        raise KeyError
    
    
except (FileNotFoundError, KeyError):
    with open(filename, 'w') as config_file:
        config_file.write(json.dumps(config_standard, indent=4))
        
    config = config_standard
    
    sleep(3)


MIN_DIGITS      = config["MIN_DIGITS"]
MAX_DIGITS      = config["MAX_DIGITS"]
PROCESSES       = config["PROCESSES"]

UPPER_EXP_LIMIT = config["UPPER_EXP_LIMIT"]
LOWER_EXP_LIMIT = config["LOWER_EXP_LIMIT"]
LOOKUP_SIZE     = config["LOOKUP_SIZE"]


# ####################################################################################################################
try:
    assert LOOKUP_SIZE > MAX_DIGITS + UPPER_EXP_LIMIT + 1,  "Increase const.LOOKUP_SIZE"
    assert PROCESSES >= 1,                                  "const.PROCESSES must be  at least 1"
    assert MIN_DIGITS >= 2,                                 "const.MIN_DIGITS must be greater than 2"
    assert MAX_DIGITS >= MIN_DIGITS,                        "const.MAX_DIGITS must be greater ot equal const.MIN_DIGITS"
    assert MIN_DIGITS - LOWER_EXP_LIMIT >= 0,               "Increase const.MIN_DIGITS or decrease const.LOWER_EXP_LIMIT"
except AssertionError as e:
    print(f"Config validation failed: ITERATIVE > {e}")
    if __name__ != "__main__":
        input(">...")
        exit(0)
