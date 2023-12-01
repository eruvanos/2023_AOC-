import sys
from functools import wraps
from time import time, sleep


class Timer:
    def __init__(self, name=None, show_input=False, file=sys.stderr):
        self.name = name
        self.show_input = show_input
        self.file = file

    def __call__(self, func):
        print(f"call {self.name}")
        return self.wrap(func)

    def wrap(self, f):
        @wraps(f)
        def wrapper(*args, **kw):
            ts = time()
            result = f(*args, **kw)
            te = time()

            name = self.name if self.name else f.__name__
            args = f"({args}, {kw})" if self.show_input else ""
            print(f"{name}{args} took: {te - ts:2.4f} sec", file=self.file, flush=True)
            return result

        return wrapper


if __name__ == "__main__":

    @Timer()
    def tesa():
        sleep(0.1)

    @Timer("TEs")
    def tesa2(**kwargs):
        sleep(0.1)

    tesa()
    tesa2(a=dict(a=1, b=2, c=3))
