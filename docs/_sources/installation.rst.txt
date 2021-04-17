.. highlight:: shell

============
Installation
============


Stable release
--------------

To install MLConjug3, run this command in your terminal:

.. code-block:: console

    $ pip install mlconjug3

This is the preferred method to install MLConjug, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.


You can also install mlconjug3 by using Anaconda_ or Miniconda_.
To install Anaconda_ or Miniconda_, please follow the installation instructions on their respective websites.
After having installed Anaconda_ or Miniconda_, run this command in your terminal:

.. code-block:: console

    $ conda config --add channels conda-forge
    $ conda config --set channel_priority strict
    $ conda install mlconjug3

.. warning::
    If you intend to install mlconjug3 on a Apple Macbook with an Apple M1 processor,
    it is advised that you install mlconjug3 by using the conda installation method as all dependencies will be pre-compiled.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Anaconda: https://www.anaconda.com/products/individual
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html


From sources
------------

The sources for MLConjug can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/SekouDiaoNlp/mlconjug3

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/SekouDiaoNlp/mlconjug3/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/SekouDiaoNlp/mlconjug
.. _tarball: https://github.com/SekouDiaoNlp/mlconjug/tarball/master
