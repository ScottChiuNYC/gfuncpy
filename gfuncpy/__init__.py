__version__= '0.1.4'

from .grid_function import Identity, GridFunction, max, min, gfunc
import numpy as np


_function_cache = {}

def __getattr__(name):
    """
    Dynamically create a function for the given name if it exists in NumPy, with caching.
    """
    if name in _function_cache:
        return _function_cache[name]

    if hasattr(np, name):
        def wrapper(grid_function):
            if isinstance(grid_function, GridFunction):
                return GridFunction(grid_function.x, getattr(np, name)(grid_function.y))
            raise TypeError(f"Expected a GridFunction instance, got {type(grid_function)}")
        wrapper.__name__ = name
        _function_cache[name] = wrapper
        return wrapper

    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


# No need to manually define sin, cos, etc. explicitly; they will be created dynamically
#
# def sin(fnc):
#     return GridFunction(fnc.x, np.sin(fnc.y))
#
# def cos(fnc):
#     return GridFunction(fnc.x, np.cos(fnc.y))