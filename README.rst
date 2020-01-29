.. image:: https://raw.githubusercontent.com/SekouDiaoNlp/mlconjug/master/logo/logotype2%20mlconjug.png
        :target: https://pypi.python.org/pypi/mlconjug
        :alt: mlconjug PyPi Home Page

=========
mlconjug3
=========


.. image:: https://img.shields.io/pypi/v/mlconjug3.svg
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: Pypi Python Package Index Status

.. image:: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/python-3-shield.svg
     :target: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/
     :alt: Python 3

.. image:: https://img.shields.io/travis/SekouDiaoNlp/mlconjug3.svg
        :target: https://travis-ci.org/SekouDiaoNLP/mlconjug3
        :alt: Linux Continuous Integration Status

.. image:: https://ci.appveyor.com/api/projects/status/6iatj101xxfehbo8/branch/master?svg=true
        :target: https://ci.appveyor.com/project/SekouDiaoNlp/mlconjug3
        :alt: Windows Continuous Integration Status

.. image:: https://readthedocs.org/projects/mlconjug3/badge/?version=latest
        :target: https://mlconjug3.readthedocs.io/en/latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/shield.svg
     :target: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/
     :alt: Dependencies status

.. image:: https://codecov.io/gh/SekouDiaoNlp/mlconjug3/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/SekouDiaoNlp/mlconjug3
        :alt: Code Coverage Status

.. image:: https://snyk.io/test/github/SekouDiaoNlp/mlconjug3/badge.svg?targetFile=requirements.txt
        :target: https://snyk.io/test/github/SekouDiaoNlp/mlconjug3?targetFile=requirements.txt
        :alt: Code Vulnerability Status


| A Python library to conjugate verbs in French, English, Spanish, Italian, Portuguese and Romanian (more soon)
    using Machine Learning techniques.
| Any verb in one of the supported language can be conjugated, as the module contains a Machine Learning model of how the verbs behave.
| Even completely new or made-up verbs can be successfully conjugated in this manner.
| The supplied pre-trained models are composed of:

- a binary feature extractor,
- a feature selector using Linear Support Vector Classification,
- a classifier using Stochastic Gradient Descent.

| MLConjug uses scikit-learn to implement the Machine Learning algorithms.
| Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the models.

| The training data for the french model is based on Verbiste https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html .
| The training data for English, Spanish, Italian, Portuguese and Romanian was generated using unsupervised learning techniques
  using the French model as a model to query during the training.

.. warning::
    MLCONJUG3 now only supports Python 3.x as Python 2.x has been deprecated in 2020.

* Free software: MIT license
* Documentation: https://mlconjug3.readthedocs.io.

Supported Languages
-------------------

- French
- English
- Spanish
- Italian
- Portuguese
- Romanian


Features
--------

- Easy to use API.
- Includes pre-trained models with 99% + accuracy in predicting conjugation class of unknown verbs.
- Easily train new models or add new languages.
- Easily integrate MLConjug in your own projects.
- Can be used as a command line tool.

Credits
-------

This package was created with the help of Verbiste_ and scikit-learn_.

The logo was designed by Zuur_.

.. _Verbiste: https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html
.. _scikit-learn: http://scikit-learn.org/stable/index.html
.. _Zuur: https://github.com/zuuritaly

