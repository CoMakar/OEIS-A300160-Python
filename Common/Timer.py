from time import perf_counter


#---------------------------------------------------------------------------
#                              CLASS
#---------------------------------------------------------------------------
class Timer(object):
    __tic = None
    __toc = None
    
    def __init__(self, name=None):
        self.__name = name

    def __enter__(self):
        self.__start = perf_counter()
        self.__tic = self.__start

    def __exit__(self, type, value, traceback):
        if self.__name:
            print(f"[TIMER: {self.__name}] ", end="")
        print(f"Elapsed: {perf_counter() - self.__start:<010.3f} seconds")
        
    def tic(self):
        self.__tic = perf_counter()
        
    def toc(self):
        self.__toc = perf_counter() - self.__tic
        return self.__toc
        