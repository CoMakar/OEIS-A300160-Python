import signal


class DontInterrupt():
    def __enter__(self):
        self.s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGINT, self.s)
