import json
from os import path, chdir
from time import sleep


config_standard = {
    "TARGET_DIGITS": 6
}
filename = "direct_config.json"


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


TARGET_DIGITS = config["TARGET_DIGITS"]


# ####################################################################
try:
    assert TARGET_DIGITS >= 1, "const.TARGET_DIGITS must be a positive integer"
except AssertionError as e:
    print(f"Config validation failed: DIRECT > {e}")
    if __name__ != "__main__":
        input(">...")
        exit(0)
