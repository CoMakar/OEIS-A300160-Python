from Common.timer import Timer
from Config import direct_config
from DirectSearch.near_prime import exhaust_search_withCache


#------------------------------------------------
#                MAIN
#------------------------------------------------
def main():      
    TARGET_DIGITS = direct_config.TARGET_DIGITS
    max_number = int("9" * TARGET_DIGITS)

    timer = Timer()
    timer.tic()

    sum_value = 0
    counter = 1

    print(f"{'START':-^64}")
    try:
        for i in range(1, max_number):
            isnp = exhaust_search_withCache(i)
            if isnp:
                sum_value += i
                print(f"> Found [{counter}] {i}")
                counter += 1
        print(f"{'END':-^64}")
    except KeyboardInterrupt:
        print(f"{'HALTED':-^64}")

        
    elapsed = timer.toc()


    print(f"Sum_value = {sum_value}\n"
        f"Time elapsed: {elapsed:.2f} seconds")
    input(">...")


if __name__ == "__main__":
    main()
