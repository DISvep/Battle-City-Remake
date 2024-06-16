import functools
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logg = logging.getLogger(__name__)


def logger(func):
    called_before = False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal called_before
        result = func(*args, **kwargs)
        if not called_before:
            logg.info(f"[{func.__module__} {func.__class__.__name__}]: {func.__qualname__}")
            called_before = True
        return result
    return wrapper
