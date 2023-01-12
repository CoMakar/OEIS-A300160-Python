from Common.printer import Printer
from Common.timer import Timer
from Config import direct_config
from DirectSearch.near_power import s_func


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    TARGET_DIGITS = direct_config.TARGET_DIGITS

    timer = Timer()
    timer.tic()

    valid_numbers = []
    sum_value = 0

    print(f"{'START':-^64}")
    try:
        valid_numbers = s_func(TARGET_DIGITS, True)
        sum_value = sum(valid_numbers)
        print(f"{'END':-^64}")
    except KeyboardInterrupt:
        print(f"{'HALTED':-^64}")


    elapsed = timer.toc()

    printer = Printer(6, 12)
    printer.printf(valid_numbers)
    print(f"Sum_value = {sum_value}\n"
        f"Time elapsed: {elapsed:.2f} seconds")
    input(">...")


if __name__ == "__main__":
    main()
