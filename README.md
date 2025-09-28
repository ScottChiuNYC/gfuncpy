# GFuncPy

GFuncPy is a flexible and intuitive library for numerical analysis and plotting — perfect for research, teaching, or just exploring math in a hands-on way. It represents functions in discrete form using $x$ and $y$ values, enabling direct computation and analysis without fuss.

Here's a quick taste of how simple and expressive it can be: 

```python
from gfuncpy import Identity

x = Identity([0, 2])

(x**2 - 2).root()
```

This snippet finds the root of $x^2 - 2$ over the interval $[0, 2]$, yielding $\sqrt{2} \approx 1.4142135\ldots$. Want to see what else it can do? Head to the [documentation page](https://gfuncpy.readthedocs.io/en/latest/index.html) for more examples and walkthroughs.

