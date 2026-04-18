.. image:: https://raw.githubusercontent.com/Ars-Linguistica/mlconjug3/master/logo/logotype2%20mlconjug.png
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: mlconjug3 PyPi Home Page

----

.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
        :target: https://GitHub.com/Ars-Linguistica/mlconjug3/graphs/commit-activity
        :alt: Package Maintenance Status

.. image:: https://img.shields.io/badge/maintainer-SekouDiaoNlp-blue
        :target: https://GitHub.com/Ars-Linguistica/mlconjug3
        :alt: Package Maintainer

.. image:: https://bestpractices.coreinfrastructure.org/projects/6961/badge
        :target: https://bestpractices.coreinfrastructure.org/projects/6961/
        :alt: OpenSSF Best Practices

.. image:: https://api.securityscorecards.dev/projects/github.com/Ars-Linguistica/mlconjug3/badge
        :target: https://api.securityscorecards.dev/projects/github.com/Ars-Linguistica/mlconjug3/
        :alt: OpenSSF ScoreCard

.. image:: https://github.com/Ars-Linguistica/mlconjug3/actions/workflows/poetry_build_and_test.yml/badge.svg
        :target: https://github.com/Ars-Linguistica/mlconjug3/actions/workflows/poetry_build_and_test.yml
        :alt: CI Status

.. image:: https://img.shields.io/pypi/v/mlconjug3.svg
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: PyPI Version

.. image:: https://static.pepy.tech/badge/mlconjug3
        :target: https://pepy.tech/project/mlconjug3
        :alt: PyPI Downloads

.. image:: https://static.pepy.tech/badge/mlconjug3/month
        :target: https://pepy.tech/project/mlconjug3
        :alt: Monthly Downloads

.. image:: https://anaconda.org/conda-forge/mlconjug3/badges/version.svg
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Conda Version

.. image:: https://codecov.io/gh/Ars-Linguistica/mlconjug3/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/Ars-Linguistica/mlconjug3
        :alt: Code Coverage

----

=======================================
mlconjug3: The multi-lingual conjugator
=======================================

mlconjug3 is a Python library and CLI tool for verb conjugation using machine learning models trained per language.

Supported languages:
- French
- English
- Spanish
- Italian
- Portuguese
- Romanian

----

🧠 Version 4.0.0 Update (Major ML Upgrade)
------------------------------------------

Version 4 introduces a major redesign of the machine learning pipeline:

- Improved feature extraction for verb morphology
- Better handling of Italian and Romanian conjugation patterns
- Updated SGDClassifier (elasticnet regularization)
- Improved generalization for unseen verbs

⚠️ Models trained before v4.0.0 are not compatible with the new pipeline.

----

⚠️ Compatibility Matrix
-----------------------

mlconjug3 is tested across multiple Python versions and operating systems.

+----------------+-------------------+----------------------------+
| Python Version | Status            | Notes                      |
+================+===================+============================+
| 3.9            | ✔ Stable          | Fully supported            |
+----------------+-------------------+----------------------------+
| 3.10           | ✔ Stable          | Fully supported            |
+----------------+-------------------+----------------------------+
| 3.11           | ✔ Stable          | Recommended                |
+----------------+-------------------+----------------------------+
| 3.12           | ✔ Stable          | Current main target        |
+----------------+-------------------+----------------------------+
| 3.13           | ⚠ Experimental    | SciPy/NumPy instability    |
+----------------+-------------------+----------------------------+
| 3.14           | ⚠ Experimental    | Not recommended for prod   |
+----------------+-------------------+----------------------------+

Operating Systems:

+------------+-------------------+------------------------------+
| OS         | Status            | Notes                        |
+============+===================+==============================+
| Linux      | ✔ Stable          | Fully CI tested             |
+------------+-------------------+------------------------------+
| macOS      | ✔ Stable          | Fully CI tested             |
+------------+-------------------+------------------------------+
| Windows    | ✔ Supported       | SciPy edge cases possible    |
+------------+-------------------+------------------------------+

----

Features
--------

- Verb conjugation using ML models
- Generalization to unseen verbs
- Retrainable pipeline (scikit-learn compatible)
- CLI + Python API

----

Installation
------------

.. code-block:: console

  $ pip install mlconjug3

----

From source
------------

.. code-block:: console

  $ git clone https://github.com/Ars-Linguistica/mlconjug3
  $ cd mlconjug3
  $ poetry install
