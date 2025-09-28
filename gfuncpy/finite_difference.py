import numpy as np

# Will review later: 
# 1. Is it a good idea to take grid as input? 
# 2. Is central difference implemented correctly? (see developer guide)
# 3. There are many repetitions, say dx and dy. Should I refactor to avoid that?

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
        # Implement the weighted central difference from the developer guide:
        # delta_x f(x_j) = (Delta_j^- / (Delta_j^+ + Delta_j^-)) * delta^+_x f(x_j)
        #                 + (Delta_j^+ / (Delta_j^+ + Delta_j^-)) * delta^-_x f(x_j)
        # where Delta_j^+ = x[j+1] - x[j], Delta_j^- = x[j] - x[j-1].
        # Vectorize for interior points j = 1..n-2
        dx = np.diff(x)               # length n-1, dx[k] = x[k+1] - x[k]
        if dx.size >= 2:
            dx_plus = dx[1:]         # Delta_j^+ for j=1..n-2
            dx_minus = dx[:-1]       # Delta_j^- for j=1..n-2

            # Forward/backward differences for interior points
            delta_plus = (y[2:] - y[1:-1]) / dx_plus
            delta_minus = (y[1:-1] - y[:-2]) / dx_minus

            denom = dx_plus + dx_minus
            # Avoid division by zero: where denom == 0 set to nan
            with np.errstate(invalid='ignore', divide='ignore'):
                weights_plus = np.where(denom != 0, dx_minus / denom, np.nan)
                weights_minus = np.where(denom != 0, dx_plus / denom, np.nan)

            result[1:-1] = weights_plus * delta_plus + weights_minus * delta_minus
        else:
            # Not enough points to form interior; leave interior as nan
            result[1:-1] = np.nan

        return result