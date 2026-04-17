.. highlight:: shell

============
Installation
============

To install mlconjug3, you have multiple options:

Using pip: 
~~~~~~~~~~

  This is the preferred method to install mlconjug3, as it will always install the most recent stable release.

To install mlconjug3, run this command in your terminal:

.. code-block:: console

  $ pip install mlconjug3


If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.


Using pipx_:
~~~~~~~~~~~~

  Recommended for users who want to avoid conflicts with other Python packages.

.. code-block:: console

  $ pipx install mlconjug3


Using conda:
~~~~~~~~~~~~

You can also install mlconjug3 by using Anaconda_ or Miniconda_ instead of `pip`.
To install Anaconda or Miniconda, please follow the installation instructions on their respective websites.
After having installed Anaconda or Miniconda, run these commands in your terminal:

.. code-block:: console

  $ conda config --add channels conda-forge
  $ conda config --set channel_priority strict
  $ conda install mlconjug3
  
If you already have Anaconda or Miniconda available on your system, just type this in your terminal:

.. code-block:: console

  $ conda install -c conda-forge mlconjug3


You can find detailed instructions for installing mlconjug3 on the Anaconda eco-system here: https://github.com/conda-forge/mlconjug3-feedstock#installing-mlconjug3

.. warning::

  If you intend to install mlconjug3 on a Apple Macbook with an Apple M1 or M2 processor or newer,
  it is advised that you install mlconjug3 by using the conda installation method as all dependencies will be pre-compiled.

.. _pip: https://pip.pypa.io
.. _pipx: https://github.com/pypa/pipx
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Anaconda: https://www.anaconda.com/products/individual
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html



From sources
~~~~~~~~~~~~

The sources for mlconjug3 can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/Ars-Linguistica/mlconjug3

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/Ars-Linguistica/mlconjug3/tarball/master

Once you have a copy of the source, get in the source directory and you can install it with:

.. code-block:: console

    $ python setup.py install

Alternatively, you can use poetry to install the software:

.. code-block:: console

    $ pip install poetry
    
    $ poetry install


.. _Github repo: https://github.com/Ars-Linguistica/mlconjug3
.. _tarball: https://github.com/Ars-Linguistica/mlconjug3/tarball/master

