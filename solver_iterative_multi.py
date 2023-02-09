import json
import signal
from os import chdir, getcwd, getpid, mkdir, path, get_terminal_size
from time import sleep

try:
    from loky import get_reusable_executor
except ImportError:
    print(f"{'REQUIRED PACKAGES NOT FOUND':-^32}") 
    print("Please install `loky`")
    print("> pip install loky")
    input("...")
    exit()

try:
    import psutil
except ImportError:
    print(f"{'RECOMENDATION':-^32}") 
    print("`psutil` is recommended to be installed")
    print("> pip install psutil")
    print(f"{'':-^32}") 
    sleep(1)

from Common import linify
from Common.Printer import Printer
from Common.str_utils import get_now, log
from Common.Timer import Timer
from Common.validators import is_np_num, is_np_num_exp
from Config import iterative_config
from Iterative.near_power import get_data_sample


#--------------------------------------------------------------------------------------------------------------------------
#                                                     PREPARATIONS
#--------------------------------------------------------------------------------------------------------------------------
def process_task(args):
    nums_to_check, num_len, exp = args
    np_nums = []
    pid = getpid()
    try:
        timer = Timer()
        timer.tic()
                
        log(f"pid_{pid:<8} Processing: len={num_len:<8} exp={exp:<8}")
        
        np_nums = [num for num in nums_to_check if is_np_num_exp(num, exp)]

        log(f"pid_{pid:<8} Finished:   len={num_len:<8} exp={exp:<8} elapsed {timer.toc():.2f} sec")
    except KeyboardInterrupt:
        log(f"pid_{pid:<8} __worker__ Interrupted!")
   
    return np_nums


def get_tasks(min_digits: int, max_digits: int,
              lower_exp_limit: int, upper_exp_limit: int):
    tasks = []
    for num_len in range(min_digits, max_digits+1):
        for exp in range(num_len-lower_exp_limit, num_len+upper_exp_limit+1):
            tasks.append((get_data_sample(num_len, exp), num_len, exp))
                         
    return tasks

    
#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    MIN_DIGITS      = iterative_config.MIN_DIGITS
    MAX_DIGITS      = iterative_config.MAX_DIGITS
    UEXPL           = iterative_config.UPPER_EXP_LIMIT
    LEXPL           = iterative_config.LOWER_EXP_LIMIT    
    NPRC            = iterative_config.PROCESSES
    WIDTH           = get_terminal_size().columns // 2
    APP             = path.dirname(__file__)
    
    
    chdir(APP)
    if not path.exists("dumps"):
        mkdir("dumps")
    chdir("dumps")
    
    
    timer = Timer()
    executor = get_reusable_executor(max_workers=NPRC)
    tasks = get_tasks(MIN_DIGITS, MAX_DIGITS, LEXPL, UEXPL)
        
    start_date = get_now()
    timer.tic()
           
 
    error_occured = False
    was_interrupted = False
    results = []
    print(f"#{'START':-^{WIDTH}}#")    
    with Timer("MAIN"):
        try:
            futures = [executor.submit(process_task, task) for task in tasks]
            for f in futures:
                if r := f.result():
                    results.append(r)
                    
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            log(f"pid_{getpid():<8} __main__ Interrupted! Killing workers...")
            executor.shutdown(False, True)
            sleep(1)
            print(f"#{'INTERRUPTED':-^{WIDTH}}#")
            log("Workers killed; Executor stopped")
            was_interrupted = True
    
        except Exception as e:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            log(f"pid_{getpid():<8} Error! Killing workers...")
            executor.shutdown(False, True)
            sleep(1)
            print(f"#{'ERROR':-^{WIDTH}}#")
            log(f"Something went wrong! Exception: {e}")
            error_occured = True
            
        print(f"#{'END':-^{WIDTH}}#")


    end_date = get_now()
    elapsed = timer.toc()
    
    valid_numbers = sorted(list(set(linify(results))))
    sum_value = 0
    extra_validation_results = [False]
    longest_num_len = 0

    
    print()


    if len(valid_numbers) > 0:
        sum_value = sum(valid_numbers)
        extra_validation_results = [is_np_num(num) for num in valid_numbers]
        longest_num_len = len(str(valid_numbers[-1]))
    
        printer = Printer(2, 40) 
        
        print(f"#{'VALID NUMBERS':-^{WIDTH}}#")  
        printer.printf(["#", "number"])
        printer.printf(linify(enumerate(valid_numbers, 1)))
        
        print(f"SUM = {sum_value}")
        
        print(f"#{'EXTRA_VALIDATION':-^{WIDTH}}#") 
        printer.printf(["number", "extra validation passed"])
        printer.printf(linify(zip(valid_numbers, extra_validation_results)))
    
    
    dump = {"config": {
        "min digits":                   MIN_DIGITS,
        "max digits":                   MAX_DIGITS,
        "number of parallel processes": NPRC,
        "upper exponent limit":         UEXPL,
        "lower exponent limit":         LEXPL,
    },
        "start date":                   start_date,
        "end date":                     end_date,
        "elapsed seconds":              elapsed,
        "numbers":                      valid_numbers,
        "number of valid numbers":      len(valid_numbers),
        "longest number length":        longest_num_len,
        "sum value":                    sum_value,
        "extra validation passed":      False not in extra_validation_results,
        "was interrupted":              was_interrupted,
        "error occurred":               error_occured
    }   
    json_dump = json.dumps(dump, indent=4)
    
    
    try:
        name_part = f"[F{MIN_DIGITS}_T{MAX_DIGITS}] [U{UEXPL}_L{LEXPL}]"
        name_part += "_I" if was_interrupted else ""
        name_part += "_E" if error_occured else ""
        with open(f"{name_part}_dump.json", 'w') as dump_file:
            dump_file.write(json_dump)
    except Exception as e:
        log(f"Ops! Not dumped. Error: {e}")
    else:
        log(f"Dumped to {getcwd()} -> {dump_file.name}")
        
    input("> Press Enter to exit...")


if __name__ == '__main__':
    main()
