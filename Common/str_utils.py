from datetime import datetime
from random import choice, randint


#---------------------------------------------------------------------------
#                            GLOBALS
#---------------------------------------------------------------------------
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
     

#---------------------------------------------------------------------------
#                            FUNCTIONS
#---------------------------------------------------------------------------
def get_now():
    now = datetime.now()
    return now.strftime("%d_%m_%Y %H:%M:%S")

               
def log(msg: object):
    print(f"[LOG] [{get_now()}] {msg}")
        

def random_name():
    return f"{choice(alphabet)}_{randint(10, 99)}"
