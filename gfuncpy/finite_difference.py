import numpy as np

# Have you reviewed. The central difference is not following the math on developer guide. 

# Finite difference differentiation operators for 1D grids
class FiniteDifference:
    @staticmethod
    def forward(grid, y):
        """
        Forward difference: (y[i+1] - y[i]) / (x[i+1] - x[i])
        Returns array of length n (last value is nan)
        """
        x = grid.x
        dy = np.diff(y)
        dx = np.diff(x)
        result = np.empty_like(y)
        result[:-1] = dy / dx
        result[-1] = np.nan
        return result

    @staticmethod
    def backward(grid, y):
        """
        Backward difference: (y[i] - y[i-1]) / (x[i] - x[i-1])
        Returns array of length n (first value is nan)
        """
        x = grid.x
        dy = np.diff(y)
        dx = np.diff(x)
        result = np.empty_like(y)
        result[0] = np.nan
        result[1:] = dy / dx
        return result

    @staticmethod
    def central(grid, y):
        """
        Central difference: (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
        Returns array of length n (first and last values are nan)
        """
        x = grid.x
        result = np.empty_like(y)
        result[0] = np.nan
        result[-1] = np.nan
        result[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
        return result