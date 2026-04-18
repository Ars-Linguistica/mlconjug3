.. image:: https://raw.githubusercontent.com/Ars-Linguistica/mlconjug3/master/logo/logotype2%20mlconjug.png
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: mlconjug3 PyPi Home Page

----

.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
        :target: https://GitHub.com/Ars-Linguistica/mlconjug3/graphs/commit-activity
        :alt: Package Maintenance Status

.. image:: https://img.shields.io/badge/maintainer-SekouDiaoNlp-blue
        :target: https://GitHub.com/Ars-Linguistica/mlconjug3
        :alt: Package Maintener

.. image:: https://bestpractices.coreinfrastructure.org/projects/6961/badge
        :target: https://bestpractices.coreinfrastructure.org/projects/6961/
        :alt: OpenSSF Best Practices

.. image:: https://api.securityscorecards.dev/projects/github.com/Ars-Linguistica/mlconjug3/badge
        :target: https://api.securityscorecards.dev/projects/github.com/Ars-Linguistica/mlconjug3/
        :alt: OpenSSF ScoreCard

.. image:: https://img.shields.io/pypi/v/mlconjug3.svg
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: Pypi Python Package Index Status

.. image:: https://anaconda.org/conda-forge/mlconjug3/badges/version.svg
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Anaconda Package Index Status

.. image:: https://img.shields.io/conda/pn/conda-forge/mlconjug3?color=dark%20green&label=Supported%20platforms
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Supported platforms

.. image:: https://img.shields.io/conda/dn/conda-forge/mlconjug?label=Anaconda%20Downloads
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Conda

.. image:: https://codecov.io/gh/Ars-Linguistica/mlconjug3/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/Ars-Linguistica/mlconjug3
        :alt: Code Coverage Status

.. image:: https://snyk-widget.herokuapp.com/badge/pip/mlconjug3/badge.svg
        :target: https://snyk.io/test/github/Ars-Linguistica/mlconjug3?targetFile=requirements.txt
        :alt: Code Vulnerability Status

.. image:: https://img.shields.io/badge/DOI-10.5281%2Fzenodo.194376338-blue.svg
        :target: https://doi.org/10.5281/zenodo.194376338
        :alt: DOI

.. image:: https://img.shields.io/mastodon/follow/109313632815812004?domain=https%3A%2F%2Ffosstodon.org&style=plastic
        :target: https://fosstodon.org/@SekouDiao
        :alt: Follow me on Mastodon

----

=======================================
mlconjug3: The multi-lingual conjugator
=======================================

A Command Line application and Python library to conjugate verbs in French, English, Spanish, Italian, Portuguese, and Romanian (with more languages soon to come) using Machine Learning techniques.

The mlconjug3 project is now a proud member of the ARS Linguistica organization. ARS Linguistica is a community-driven, open source project that aims to develop free and accessible linguistic tools and resources for all. With a focus on advancing linguistic research, documentation, and education, ARS Linguistica is dedicated to preserving and promoting linguistic diversity through the use of open source and open science.

With mlconjug3, you can:

- Conjugate any verb in one of the supported languages, even completely new or made-up verbs, with the help of a pre-trained Machine Learning model.
- Easily modify and retrain the models using any compatible classifiers from scikit-learn.
- Integrate mlconjug3 in your own projects.

----

Compatibility Matrix (v4.0.0)
-----------------------------

+----------------------+----------------------+------------------------------+
| Platform             | Supported            | Notes                        |
+======================+======================+==============================+
| Linux                | ✔ Python 3.9–3.14    | Fully supported              |
+----------------------+----------------------+------------------------------+
| macOS                | ✔ Python 3.9–3.14    | Fully supported              |
+----------------------+----------------------+------------------------------+
| Windows              | ✔ Python 3.9–3.12    | Stable                       |
+----------------------+----------------------+------------------------------+
| Windows (3.13+)      | ~ Experimental       | SciPy / sklearn issues       |
+----------------------+----------------------+------------------------------+
| Python 3.13+         | ~ Experimental       | Native binary instability    |
+----------------------+----------------------+------------------------------+
⚠ IMPORTANT:
Windows + Python 3.13/3.14 may crash due to upstream SciPy binary incompatibilities.
These builds are marked experimental in CI.

----

Release Notes (v4.0.0)
----------------------

This release introduces major internal improvements to the ML pipeline.

Improvements:

- Reworked training pipeline for stability and reproducibility
- Improved feature extraction for Italian and Romanian verb morphology
- Unified sklearn Pipeline architecture for all models
- Updated classifier to SGDClassifier (elasticnet regularization)
- Better handling of unseen verb forms via enhanced feature engineering
- Improved cross-platform consistency (Windows/macOS/Linux)

Behavioral changes:

- Slight variations in prediction outputs due to improved feature representation
- Optional sample weighting added to training pipeline
- Internal API refactoring (public API remains backward compatible)

Migration notes:

- No breaking changes in public API
- Minor variation in predictions expected due to improved model generalization

----

Using mlconjug3 in Academic Research
------------------------------------

mlconjug3 is a valuable tool for linguistic researchers, as it provides accurate and up-to-date conjugation information for a wide range of languages. With its ability to handle completely new or made-up verbs, mlconjug3 is perfect for exploring new linguistic concepts and theories. It can also be used to compare and contrast conjugation patterns across different languages, helping researchers to identify and understand linguistic trends.

Integrating mlconjug3 in Applications
-------------------------------------

In addition to academic research, mlconjug3 can be integrated into a wide range of web and desktop applications. For language learning platforms, mlconjug3 provides an accurate and comprehensive source of conjugation information, helping students to quickly and easily master verb conjugation. For language translation tools, mlconjug3 can help to ensure that translations are grammatically correct, by providing accurate verb conjugation information in real-time.

By using mlconjug3, you are not only getting a powerful and flexible tool for verb conjugation, but you are also supporting the goals and mission of ARS Linguistica. Whether you are a linguistic researcher, language teacher, or simply someone who is passionate about preserving linguistic heritage, your support is crucial to the success of our organization.

Join us in our mission to make linguistic tools and resources accessible to all!

----

.. image:: https://raw.githubusercontent.com/Ars-Linguistica/mlconjug3/master/docs/images/example.gif
        :alt: Conjugation for the verb to be.

----

* Free software: MIT license
* Documentation: https://mlconjug3.readthedocs.io/en/latest/readme.html


Supported Languages
-------------------

- French
- English
- Spanish
- Italian
- Portuguese
- Romanian


Academic publications citing mlconjug3
--------------------------------------

- | Gerard Canal, Senka Krivic, Paul Luff, Andrew Coles.
  | "`PlanVerb: Domain-Independent Verbalization and Summary of Task Plans`_".
  | Thirty-Sixth AAAI Conference on Artificial Intelligence (AAAI-22), 2022.

- | Mike Hongfei Wu.
  | "`Extensions and Applications of Deep Probabilistic Inference for Generative Models`_".
  | A DISSERTATION SUBMITTED TO THE DEPARTMENT OF COMPUTER SCIENCE AND THE COMMITTEE ON GRADUATE STUDIES OF STANFORD UNIVERSITY IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF DOCTOR OF PHILOSOPHY. May 2022.

- | Spencer Ng, Lucy Teaford, Andy Yang, and Isaiah Zwick-Schachter.
  | "`Fluorescing Questions: Effects of Semantic Perturbations on BERT Performance in SQuAD 1.1`_".
  | CMSC 25610: Computational Linguistics University of Chicago, 2021.

- | Ali Malik and Mike Wu and Vrinda Vasavada and Jinpeng Song and John Mitchell and Noah D. Goodman and Chris Piech.
  | "`Generative Grading Neural Approximate Parsing for Automated Student Feedback`_".
  | Proceedings of the 34th AAAI conference on Artificial Intelligence, 2019.


BibTeX
------

If you want to cite mlconjug3 in an academic publication use this citation format:

.. code:: bibtex

   @article{mlconjug3,
     title={mlconjug3},
     author={Sekou Diao},
     journal={GitHub. Note: https://github.com/Ars-Linguistica/mlconjug3 Cited by},
     year={2023}
   }


Software projects using mlconjug3
---------------------------------

- | `EDS-NLP`_
  | EDS-NLP provides a set of spaCy components that are used to extract information from clinical notes written in French.

- | `Machine Translation Service`_
  | Translation flask API for the Helsinki NLP models available in the Huggingface Transformers library.

- | `NLP-Suite`_
  | NLP Suite is a package of tools designed for non-specialists, for scholars with no knowledge or little knowledge of Natural Language Processing.

- | `Runebook`_
  | Runebook translates various references such as programming languages, frameworks, libraries, and APIs that software engineers refer to in development.

- | `Gender Bias Visualization`_
  | This project offers tools to visualize the gender bias in pre-trained language models.

- | `Text Adaptation To Context`_
  | Uses language models to generate adapted text.

- | `verbecc-svc`_
  | Dockerized microservice for conjugation.

- | `nvhtml`_
  | HTML transformation tool.

- | `Tux`_
  | A Tux bot.

- | `twitter-bot`_
  | Tweets French words.

- | `verb-form-helper`_
  | Helps learn verb forms.

- | `NLP Tasks`_
  | NLP utilities.

- | `Facemask Detection`_
  | Detects masks.

- | `Bad Excuses for Zoom Abuses`_
  | Generates excuses.

- | `NLP`_
  | NLP repository.

- | `Virtual Assistant`_
  | Voice assistant.

- | `Bad Advice`_
  | Random advice generator.

- | `Spanish Conjugations Quiz`_
  | Quiz generator.

- | `Silver Rogue DF`_
  | Rogue-like game.

- | `learn-spanish-react`_
  | Spanish learning app.

- | `Learn_vocab`_
  | Vocabulary app.


Installation
------------

You can install mlconjug3 using different methods depending on your workflow.

### 1. Install via pip (recommended)

.. code:: bash

   pip install mlconjug3


### 2. Install from source (GitHub)

.. code:: bash

   git clone https://github.com/Ars-Linguistica/mlconjug3.git
   cd mlconjug3
   pip install .


### 3. Install via conda (conda-forge)

.. code:: bash

   conda install -c conda-forge mlconjug3


----

Signing of Releases
-------------------

Starting with version 3.10, all releases of mlconjug3 published on PyPI and GitHub are signed using Sigstore.

What is Sigstore?
~~~~~~~~~~~~~~~~~

Sigstore is an open-source project that provides simple, transparent, and secure software signing. It allows developers to sign releases without managing long-lived cryptographic keys.

Instead, Sigstore uses short-lived certificates issued through identity providers, making the signing process both secure and easy to verify.

This ensures that mlconjug3 releases on PyPI can be cryptographically verified and have not been tampered with.

How to verify a release?
~~~~~~~~~~~~~~~~~~~~~~~~

You can verify mlconjug3 package signatures using `cosign`, which is part of the Sigstore ecosystem.

Install cosign:

.. code:: bash

   # Linux / macOS
   curl -O -L https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64
   chmod +x cosign-linux-amd64
   sudo mv cosign-linux-amd64 /usr/local/bin/cosign

   # macOS (Homebrew)
   brew install cosign

Verify a release:

.. code:: bash

   cosign verify-blob \
       --certificate-identity https://github.com/Ars-Linguistica/mlconjug3/.github/workflows/upload_wheels_to_pypi.yml \
       --certificate-oidc-issuer https://token.actions.githubusercontent.com \
       mlconjug3-<version>.tar.gz \
       --signature mlconjug3-<version>.tar.gz.sig

This ensures:
- The package was built by the official CI pipeline
- The release was not modified after publication
- The signature matches the GitHub Actions identity

For more details, see:
https://docs.sigstore.dev/

Credits
-------

This package was created with the help of Verbiste_ and scikit-learn_.

The logo was designed by Zuur_.

.. _Verbiste: https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html
.. _scikit-learn: http://scikit-learn.org/stable/index.html
.. _Zuur: https://github.com/zuuritaly
.. _`PlanVerb: Domain-Independent Verbalization and Summary of Task Plans`: https://ojs.aaai.org/index.php/AAAI/article/download/21204/version/19491/20953
.. _`Generative Grading Neural Approximate Parsing for Automated Student Feedback`: https://arxiv.org/abs/1905.09916
.. _`Fluorescing Questions: Effects of Semantic Perturbations on BERT Performance in SQuAD 1.1`: https://github.com/spencerng/squad-sentiment/blob/87b42a41ba7f4f3f8d4e6c478f746d6cdf9f5515/assets/semantic-perturbations-bert-performance.pdf
.. _`Extensions and Applications of Deep Probabilistic Inference for Generative Models`: https://drive.google.com/file/d/10IXi-RleFoG9L6G70TEKbAGd-v29R2Zz/view?usp=sharing
.. _`EDS-NLP`: https://github.com/aphp/edsnlp
.. _`Runebook`: https://github.com/runebookdev/runebook/tree/4391d52588bb5c5c0e7d49a0c31b4bdc1cbffb47
.. _`Gender Bias Visualization`: https://github.com/GesaJo/Gender-Bias-Visualization
.. _`Text Adaptation To Context`: https://github.com/lzontar/Text_Adaptation_To_Context
.. _`Facemask Detection`: https://github.com/samuel-karanja/facemask-derection
.. _`Bad Excuses for Zoom Abuses`: https://github.com/tyxchen/bad-excuses-for-zoom-abuses
.. _NLP: https://github.com/pskshyam/NLP
.. _`Virtual Assistant`: https://github.com/JeanExtreme002/Virtual-Assistant
.. _`Bad Advice`: https://github.com/matthew-cheney/bad-advice
.. _`Spanish Conjugations Quiz`: https://github.com/williammortimer/Spanish-Conjugations-Quiz
.. _`Silver Rogue DF`: https://github.com/FranchuFranchu/silver-rogue-df
.. _`NLP-Suite`: https://github.com/NLP-Suite/NLP-Suite
.. _`twitter-bot`: https://github.com/arthurcouyere/twitter-bot
.. _`verb-form-helper`: https://github.com/gittymutt/verb-form-helper
.. _`NLP Tasks`: https://github.com/ai-systems/poly-nlp
.. _`verbecc-svc`: https://pypi.org/project/verbecc/
.. _`nvhtml`: https://pypi.org/project/nvhtml/
.. _`Machine Translation Service`: https://github.com/pauchai/machine-translation-service
.. _`Tux`: https://github.com/amirkasraa/Tux
.. _`learn-spanish-react`: https://github.com/advay168/learn-spanish-react
.. _`Learn_vocab`: https://github.com/MilaimKas/Learn_vocab
