def log(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f"{func.__name__}({args}, {kwargs}) -> {ret}")
        return ret

    return wrapper


def mapl(f, things):
    return list(map(f, things))
