from gfuncpy import GridFunction, Identity, sin, cos, gfunc
from gfuncpy.finite_difference import FiniteDifference
import gfuncpy
import unittest
import numpy as np
from math import pi

class GridFunctionTestCase(unittest.TestCase):
    def test_maximum_minimum(self):
        x = Identity.uniform_grid(0, 1, 100)
        f1 = x**2
        f2 = x + 2
        # Pointwise maximum/minimum between two grid functions. 
        # Must write gfuncpy.max so that python does not confuse it with the built-in max function.
        max_f = gfuncpy.max(f1, f2)
        min_f = gfuncpy.min(f1, f2)
        self.assertIsInstance(max_f, GridFunction)
        self.assertIsInstance(min_f, GridFunction)
        # Check values at a few points
        self.assertAlmostEqual(max_f(0), max(0**2, 0+2))
        self.assertAlmostEqual(max_f(1), max(1**2, 1+2))
        self.assertAlmostEqual(min_f(0), min(0**2, 0+2))
        self.assertAlmostEqual(min_f(1), min(1**2, 1+2))
        # Pointwise maximum/minimum with a scalar
        max_scalar = gfuncpy.max(f1, 0.5)
        min_scalar = gfuncpy.min(f2, 2.5)
        self.assertIsInstance(max_scalar, GridFunction)
        self.assertIsInstance(min_scalar, GridFunction)
        self.assertAlmostEqual(max_scalar(0), max(0**2, 0.5))
        self.assertAlmostEqual(min_scalar(1), min(1+2, 2.5))

    def test_integrate(self):
        x = Identity.uniform_grid(0, 1, 100)
        f = x**2  

        antideriv = f.integrate()
        self.assertIsInstance(antideriv, GridFunction)
        
        approx = f.integrate(0, 1)
        expected = 1/3  
        self.assertAlmostEqual(approx, expected, places=3)
        
        approx_half = f.integrate(0, 0.5)
        expected_half = (0.5**3)/3
        self.assertAlmostEqual(approx_half, expected_half, places=3)

        with self.assertRaises(ValueError):
            f.integrate(-1, 1)

        with self.assertRaises(ValueError):
            f.integrate(0, 2)

    def test_gfunc_decorator(self):

        @gfunc
        def absolute_value(x):
            if x > 0:
                return x
            else:
                return -x

        x = Identity([-1, 1])
        abs_x = absolute_value(x)
        self.assertIsInstance(abs_x, GridFunction)

        # Check a few values
        self.assertAlmostEqual(abs_x(-1), 1)
        self.assertAlmostEqual(abs_x(0), 0)
        self.assertAlmostEqual(abs_x(1), 1)

    def setUp(self):
        self.x = Identity.uniform_grid(0, 2*pi, 100)

    def test_identity_init_uniform(self):
        # Test with default n
        ident = Identity((0, 1))
        self.assertTrue(np.allclose(ident.x, ident.y))
        self.assertEqual(len(ident.x), int((1-0)*200)+1)

        # Test with explicit n
        ident2 = Identity((0, 2), n=50)
        self.assertTrue(np.allclose(ident2.x, ident2.y))
        self.assertEqual(len(ident2.x), 51)

    def test_identity_init_invalid_nodes(self):
        # Test with non-array-like nodes
        with self.assertRaises(ValueError):
            Identity(0)
        # Test with wrong length nodes
        with self.assertRaises(NotImplementedError):
            Identity((0, 1, 2))
        
    def test_function_operations(self):
        x = self.x

        f1 = sin(x) + cos(x)
        f2 = sin(x) + sin(x) + cos(x)
        f3 = sin(x) + 2
        f4 = 2 + sin(x)
        f5 = sin(x) - 2
        f6 = 2 - sin(x)
        f7 = -sin(x)
        f8 = (sin(x) + cos(x)) / 2
        
        self.assertAlmostEqual(f1(pi/2), np.sin(pi/2) + np.cos(pi/2))
        self.assertAlmostEqual(f2(pi/2), np.sin(pi/2) + np.sin(pi/2) + np.cos(pi/2))
        self.assertAlmostEqual(f3(pi/2), np.sin(pi/2) + 2)
        self.assertAlmostEqual(f4(pi/2), 2 + np.sin(pi/2))
        self.assertAlmostEqual(f5(pi/2), np.sin(pi/2) - 2)
        self.assertAlmostEqual(f6(pi/2), 2 - np.sin(pi/2))
        self.assertAlmostEqual(f7(pi/2), -np.sin(pi/2))
        self.assertAlmostEqual(f8(pi/2), (np.sin(pi/2) + np.cos(pi/2)) / 2)
    
    def test_root(self):
        x = self.x

        self.assertRaises(ArithmeticError, lambda: (3*x + 29).root())
        self.assertAlmostEqual((3*x - 5).root(), 5/3)

    def test_derivative_uniform_behavior(self):
        # derivative should use weighted central for interior and forward/backward at endpoints
        x = np.linspace(0.0, 2.0, 9)
        y = x ** 3
        gf = GridFunction(x, y)

        d = gf.derivative()
        # interior: centered difference
        h = x[1] - x[0]
        expected_center = np.empty_like(y)
        expected_center[1:-1] = (y[2:] - y[:-2]) / (2 * h)

        np.testing.assert_allclose(d.y[1:-1], expected_center[1:-1], rtol=1e-12, atol=0)

        # endpoints: forward/backward differences
        expected_first = (y[1] - y[0]) / (x[1] - x[0])
        expected_last = (y[-1] - y[-2]) / (x[-1] - x[-2])
        self.assertAlmostEqual(d.y[0], expected_first)
        self.assertAlmostEqual(d.y[-1], expected_last)

    def test_derivative_nonuniform_matches_fd(self):
        x = np.array([0.0, 0.1, 0.4, 1.0, 1.5])
        y = np.sin(x)
        gf = GridFunction(x, y)

        d = gf.derivative()
        fd = FiniteDifference.central(gf.grid, gf.y)

        # interior should match FiniteDifference.central
        np.testing.assert_allclose(d.y[1:-1], fd[1:-1])

        # endpoints should equal forward/backward finite differences
        expected_first = (y[1] - y[0]) / (x[1] - x[0])
        expected_last = (y[-1] - y[-2]) / (x[-1] - x[-2])
        self.assertAlmostEqual(d.y[0], expected_first)
        self.assertAlmostEqual(d.y[-1], expected_last)

if __name__ == '__main__':
    unittest.main()
