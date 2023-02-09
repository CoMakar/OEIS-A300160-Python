import os

from Common.Printer import Printer
from Common.Timer import Timer
from Config import direct_config
from DirectSearch.near_power import exhaust_search_withCache


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():      
    TARGET_DIGITS = direct_config.TARGET_DIGITS
    WIDTH         = os.get_terminal_size().columns // 2
    max_number = int("9" * TARGET_DIGITS)


    timer = Timer()
    timer.tic()

    sum_value = 0
    valid_numbers = []
    counter = 1

    print(f"#{'START':-^{WIDTH}}#")
    try:
        for i in range(1, max_number):
            isnp = exhaust_search_withCache(i)
            if isnp:
                sum_value += i
                valid_numbers.append(i)
                print(f"> Found [{counter}] {i}")
                counter += 1
        print(f"#{'END':-^{WIDTH}}#")
    except KeyboardInterrupt:
        print(f"#{'HALTED':-^{WIDTH}}#")

    elapsed = timer.toc()


    printer = Printer(1, 1, False)
    printer.printf(valid_numbers)
    print(f"Sum_value = {sum_value}\n"
        f"Time elapsed: {elapsed:.2f} seconds")
    
    input("> Press Enter to exit...")


if __name__ == "__main__":
    main()
