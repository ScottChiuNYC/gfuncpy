import unittest
import numpy as np

from gfuncpy.finite_difference import FiniteDifference
from gfuncpy.grid_function import Grid, GridFunction


class TestFiniteDifference(unittest.TestCase):
    def test_forward_backward_on_uniform(self):
        x = np.linspace(0.0, 1.0, 5)
        g = Grid(x)
        y = x ** 2

        fwd = FiniteDifference.forward(g, y)
        bwd = FiniteDifference.backward(g, y)

        dx = x[1] - x[0]
        # analytical forward/backward for uniform grid
        expected_fwd = np.empty_like(y)
        expected_fwd[:-1] = (y[1:] - y[:-1]) / dx
        expected_fwd[-1] = np.nan

        expected_bwd = np.empty_like(y)
        expected_bwd[0] = np.nan
        expected_bwd[1:] = (y[1:] - y[:-1]) / dx

        np.testing.assert_allclose(fwd[:-1], expected_fwd[:-1])
        np.testing.assert_allclose(bwd[1:], expected_bwd[1:])
        self.assertTrue(np.isnan(fwd[-1]))
        self.assertTrue(np.isnan(bwd[0]))

    def test_central_uniform_matches_analytical(self):
        x = np.linspace(0.0, 2.0, 9)
        g = Grid(x)
        y = x ** 3  # derivative 3 x^2

        cen = FiniteDifference.central(g, y)
        # For a uniform grid the developer-guide weighted formula reduces to
        # (y[i+1] - y[i-1]) / (2*h). Compare to that discrete formula rather
        # than the analytic derivative (centered difference has O(h^2) error).
        h = x[1] - x[0]
        expected_centered = (y[2:] - y[:-2]) / (2 * h)
        np.testing.assert_allclose(cen[1:-1], expected_centered, rtol=1e-12, atol=0)
        self.assertTrue(np.isnan(cen[0]))
        self.assertTrue(np.isnan(cen[-1]))

    def test_central_nonuniform_weighted_formula(self):
        # non-uniform grid
        x = np.array([0.0, 0.1, 0.4, 1.0, 1.5])
        g = Grid(x)
        y = np.sin(x)

        cen = FiniteDifference.central(g, y)

        # compute expected using the weighted formula from the developer guide
        dx = np.diff(x)
        dx_plus = dx[1:]
        dx_minus = dx[:-1]

        delta_plus = (y[2:] - y[1:-1]) / dx_plus
        delta_minus = (y[1:-1] - y[:-2]) / dx_minus
        denom = dx_plus + dx_minus
        expected_interior = (dx_minus / denom) * delta_plus + (dx_plus / denom) * delta_minus

        np.testing.assert_allclose(cen[1:-1], expected_interior)
        self.assertTrue(np.isnan(cen[0]))
        self.assertTrue(np.isnan(cen[-1]))

    def test_small_grid_behavior(self):
        # With only two points, central should be all nans
        x = np.array([0.0, 1.0])
        g = Grid(x)
        y = np.array([0.0, 1.0])

        cen = FiniteDifference.central(g, y)
        self.assertEqual(len(cen), 2)
        self.assertTrue(np.isnan(cen[0]))
        self.assertTrue(np.isnan(cen[1]))

        # forward/backward should behave as implemented (one valid, one nan)
        fwd = FiniteDifference.forward(g, y)
        bwd = FiniteDifference.backward(g, y)
        self.assertTrue(np.isnan(fwd[-1]))
        self.assertTrue(np.isnan(bwd[0]))


if __name__ == '__main__':
    unittest.main()
