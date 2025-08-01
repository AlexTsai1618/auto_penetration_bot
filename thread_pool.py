import threading

class ThreadPool:
    """Simple helper to run multiple tasks concurrently."""

    def __init__(self):
        self.threads = []

    def submit(self, func, *args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()
        self.threads.append(t)
        return t

    def join_all(self):
        for t in self.threads:
            t.join()
        self.threads.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.join_all()
