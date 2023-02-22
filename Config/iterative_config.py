import json
from os import path, chdir
from time import sleep


config_standard = {
    "MIN_DIGITS"        : 2,
    "MAX_DIGITS"        : 6,
    "UPPER_EXP_LIMIT"   : 10,
    "LOWER_EXP_LIMIT"   : 1,
    "PROCESSES"         : 2,
    "USE_GUI"           : True,
    "CHUNK_SIZE"        : 8048,
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
    

MIN_DIGITS      = config["MIN_DIGITS"]
MAX_DIGITS      = config["MAX_DIGITS"]
UPPER_EXP_LIMIT = config["UPPER_EXP_LIMIT"]
LOWER_EXP_LIMIT = config["LOWER_EXP_LIMIT"]

PROCESSES       = config["PROCESSES"]
USE_GUI         = config["USE_GUI"]
CHUNK_SIZE      = config["CHUNK_SIZE"]
LOOKUP_SIZE     = config["LOOKUP_SIZE"]


# ####################################################################################################################
try:
    assert LOOKUP_SIZE > MAX_DIGITS + UPPER_EXP_LIMIT + 1,  "Increase const.LOOKUP_SIZE"
    assert MIN_DIGITS >= 2,                                 "const.MIN_DIGITS must be greater than 2"
    assert MAX_DIGITS >= MIN_DIGITS,                        "const.MAX_DIGITS must be greater ot equal const.MIN_DIGITS"
    assert MIN_DIGITS - LOWER_EXP_LIMIT >= 0,               "Increase const.MIN_DIGITS or decrease const.LOWER_EXP_LIMIT"
    assert PROCESSES >= 1,                                  "const.PROCESSES must be  at least 1"
    assert type(USE_GUI) == bool,                           "const.USE_GUI must be a boolean"
    assert CHUNK_SIZE >= 1024,                              "const.CHUNK_SIZE must be greater than 1024"

except AssertionError as e:
    print(f"Config validation failed: ITERATIVE > {e}")
    if __name__ != "__main__":
        input(">...")
        exit(0)
