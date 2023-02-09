import os

from Common.Printer import Printer
from Common.Timer import Timer
from Config import direct_config
from DirectSearch.near_power import s_func


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    TARGET_DIGITS = direct_config.TARGET_DIGITS
    WIDTH         = os.get_terminal_size().columns // 2


    timer = Timer()
    timer.tic()

    valid_numbers = []
    sum_value = 0

    print(f"#{'START':-^{WIDTH}}#")
    try:
        valid_numbers = s_func(TARGET_DIGITS, True)
        sum_value = sum(valid_numbers)
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
