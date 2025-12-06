from time import perf_counter


def log(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f"{func.__name__}({args}, {kwargs}) -> {ret}")
        return ret

    return wrapper


class Perf:
    def __init__(self):
        self.start = perf_counter()
        self.prev = self.start

    def tick(self, msg):
        now = perf_counter()
        print(f"{now - self.start:.3f} {now - self.prev:.3f} {msg}")
        self.prev = now


def mapl(f, things):
    return list(map(f, things))
