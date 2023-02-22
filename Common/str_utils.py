from datetime import datetime, timedelta
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


def get_hms(td: timedelta):
    return f"{td.seconds//3600}:{(td.seconds//60)%60:0>2}:{td.seconds%60:0>2}"

           
def log(msg: object):
    print(f"[LOG] [{get_now()}] {str(msg)}")


def flog(msg: object):
    return f"[LOG] [{get_now()}] {str(msg)}"


def random_name():
    return f"{choice(alphabet)}_{randint(10, 99)}"
