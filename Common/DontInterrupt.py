import signal


class DontInterrupt():
    """
    Context manager that prevents everything enclosed from being interrupted by Ctrl+C
    """
    def __enter__(self):
        self.s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGINT, self.s)
        

def dont_interrupt(func):
    """
    decorator for functions that should not be interrupted by Ctrl+C
    """
    def wrapper(*args, **kwargs):
        with DontInterrupt():
            return func(*args, **kwargs)
    return wrapper
