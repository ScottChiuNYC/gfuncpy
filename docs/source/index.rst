.. GFuncPy documentation master file, created by
   sphinx-quickstart on Fri Jul 18 21:05:30 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


GFuncPy Documentation
=====================

GFuncPy is a flexible and intuitive library for numerical analysis and plotting — perfect for research, teaching, or just exploring math in a hands-on way. It represents functions in discrete form using :math:`x` and :math:`y` values, enabling direct computation and analysis without fuss.

Here's a quick taste of how simple and expressive it can be:

.. code-block:: python

    from gfuncpy import Identity

    x = Identity([0, 2])

    (x**2 - 2).root()


This snippet finds the root of :math:`x^2 - 2` over the interval :math:`[0, 2]`, yielding :math:`\sqrt{2} \approx 1.4142135\ldots`. Want to see what else it can do? Head to the *Usage* page below for more examples and walkthroughs.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   usage
   developer_guide
