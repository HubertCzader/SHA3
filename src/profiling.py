import time
from collections import defaultdict

profile_results = defaultdict(lambda: [])


def profile(_func=None, name=None):
    """Profiling decorator"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal name
            start_time = time.time()
            result = func(*args, **kwargs)
            if not name:
                name = func.__qualname__
            elapsed_time = time.time() - start_time
            profile_results[name].append(elapsed_time)

        return wrapper

    return decorator(_func) if _func else decorator
