from Common.timer import Timer
from Config import direct_config
from DirectSearch.near_prime import s_func


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():
    TARGET_DIGITS = direct_config.TARGET_DIGITS

    timer = Timer()
    timer.tic()

    sum_value = 0

    print(f"{'START':-^64}")
    try:
        sum_value = s_func(TARGET_DIGITS, True)
        print(f"{'END':-^64}")
    except KeyboardInterrupt:
        print(f"{'HALTED':-^64}")


    elapsed = timer.toc()

    print(f"Sum_value = {sum_value}\n"
        f"Time elapsed: {elapsed:.2f} seconds")
    input(">...")


if __name__ == "__main__":
    main()
