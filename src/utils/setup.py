import builtins
import functools


def verbose(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        verbose = kwargs.get('verbose', False)
        def custom_print(*args, **kwargs):
            if verbose:
                print(*args, **kwargs)
        original_print = builtins.print
        builtins.print = custom_print
        try:
            result = func(*args, **kwargs)
        finally:
            builtins.print = original_print
        return result
    return wrapper