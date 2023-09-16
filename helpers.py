from functools import reduce


def reduce_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return reduce(lambda x, y: x + y, result, 0.00)

    return wrapper
