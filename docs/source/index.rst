.. GFuncPy documentation master file, created by
   sphinx-quickstart on Fri Jul 18 21:05:30 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to GFuncPy's documentation!
===================================

**Package Status**

.. raw:: html

    <p>
       <a href="https://gfuncpy.readthedocs.io/en/latest/">
          <img src="https://img.shields.io/readthedocs/gfuncpy.svg" alt="docs"/>
       </a>
       <a href="https://pypi.org/project/gfuncpy/">
          <img src="https://img.shields.io/pypi/v/gfuncpy.svg" alt="pypi"/>
       </a>
       <a href="https://pepy.tech/project/gfuncpy">
          <img src="https://static.pepy.tech/badge/gfuncpy" alt="downloads"/>
       </a>
       <!-- <a href="https://pepy.tech/project/gfuncpy">
          <img src="https://static.pepy.tech/p/d/gfuncpy" alt="downloads/month"/>
       </a> -->
       <a href="https://github.com/ScottChiuNYC/gfuncpy/blob/main/LICENSE">
          <img src="https://img.shields.io/github/license/ScottChiuNYC/gfuncpy.svg" alt="license"/>
       </a>
    </p>

----

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
