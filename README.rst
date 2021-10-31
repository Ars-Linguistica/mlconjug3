.. image:: https://raw.githubusercontent.com/SekouDiaoNlp/mlconjug3/master/logo/logotype2%20mlconjug.png
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: mlconjug3 PyPi Home Page

=========
MLCONJUG3
=========


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
        :target: https://GitHub.com/SekouDiaoNlp/mlconjug3/graphs/commit-activity
        :alt: Package Maintenance Status

.. image:: https://img.shields.io/badge/maintainer-SekouDiaoNlp-blue
        :target: https://GitHub.com/SekouDiaoNlp/mlconjug3
        :alt: Package Maintener

.. image:: https://github.com/SekouDiaoNlp/mlconjug3/workflows/mlconjug3/badge.svg
        :target: https://github.com/SekouDiaoNlp/mlconjug3/actions
        :alt: Build status on Windows, MacOs and Linux

.. image:: https://img.shields.io/pypi/v/mlconjug3.svg
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: Pypi Python Package Index Status

.. image:: https://anaconda.org/conda-forge/mlconjug3/badges/version.svg
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Anaconda Package Index Status

.. image:: https://img.shields.io/pypi/pyversions/mlconjug3
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: Compatible Python versions

.. image:: https://img.shields.io/conda/pn/conda-forge/mlconjug3?color=dark%20green&label=Supported%20platforms
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Supported platforms

.. image:: https://readthedocs.org/projects/mlconjug3/badge/?version=latest
        :target: https://mlconjug3.readthedocs.io/en/latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/shield.svg
        :target: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/
        :alt: Dependencies status

.. image:: https://codecov.io/gh/SekouDiaoNlp/mlconjug3/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/SekouDiaoNlp/mlconjug3
        :alt: Code Coverage Status

.. image:: https://snyk-widget.herokuapp.com/badge/pip/mlconjug3/badge.svg
        :target: https://snyk.io/test/github/SekouDiaoNlp/mlconjug3?targetFile=requirements.txt
        :alt: Code Vulnerability Status

.. image:: https://img.shields.io/pypi/dm/mlconjug3?label=PyPi%20Downloads
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: PyPI Downloads

.. image:: https://img.shields.io/conda/dn/conda-forge/mlconjug?label=Anaconda%20Total%20Downloads
        :target: https://anaconda.org/conda-forge/mlconjug3
        :alt: Conda





| A Python library to conjugate verbs in French, English, Spanish, Italian, Portuguese and Romanian (more soon)
    using Machine Learning techniques.
| Any verb in one of the supported language can be conjugated, as the module contains a Machine Learning model of how the verbs behave.
| Even completely new or made-up verbs can be successfully conjugated in this manner.
| The supplied pre-trained models are composed of:

- a binary feature extractor,
- a feature selector using Linear Support Vector Classification,
- a classifier using Stochastic Gradient Descent.

| MLConjug3 uses scikit-learn to implement the Machine Learning algorithms.
| Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the models.

| The training data for the french model is based on Verbiste https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html .
| The training data for English, Spanish, Italian, Portuguese and Romanian was generated using unsupervised learning techniques
  using the French model as a model to query during the training.

.. warning::
    MLCONJUG3 now only supports Python 3.x as Python 2.x has been deprecated in 2020.

* Free software: MIT license
* Documentation: https://mlconjug3.readthedocs.io/en/latest/.


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


Academic publications citing mlconjug
-------------------------------------

- | Ali Malik and Mike Wu and Vrinda Vasavada and Jinpeng Song and John Mitchell and Noah D. Goodman and Chris Piech.
  | "`Generative Grading Neural Approximate Parsing for Automated Student Feedback`_".
  | Proceedings of the 34th AAAI conference on Artificial Intelligence, 2019.

Software projects using mlconjug
--------------------------------


- | `Machine Translation Service`_
  | Translation flask API for the Helsinki NLP models available in the Huggingface Transformers library.
- | `NLP-Suite`_
  | NLP Suite is a package of tools designed for non-specialists, for scholars with no knowledge or little knowledge of Natural Language Processing.
- | `Gender Bias Visualization`_
  | This project offers tools to visualize the gender bias in pre-trained language models to better understand the prejudices in the data.
- | `Text Adaptation To Context`_
  | This project uses language models to generate text that is well suited to the type of publication.
- | `verbecc-svc`_
  | Dockerized microservice with REST API for conjugation of any verb in French and Spanish.
- | `nvhtml`_
  | A tool to Manage and tansform HTML documents.
- | `Tux`_
  | A Tux bot.
- | `twitter-bot`_
  | Tweets the words of the French language. Largely inspired by the @botducul (identical lexicon, but code in Python) and the @botsupervnr.
  | Posts on @botduslip. Stores the position of the last tweeted word in a Redis database.
- | `verb-form-helper`_
  | This project offers a tool to help learn differnt verbal forms.
- | `NLP Tasks`_
  | A collection of common NLP tasks such as dataset parsing and explicit semantic extraction.
- | `Facemask Detection`_
  | This project offers a model which recognizes covid-19 masks.
- | `Bad Excuses for Zoom Abuses`_
  | Need an excuse for why you can't show up in your Zoom lectures? Just generate one here!
- | `NLP`_
  | Repository to store Natural Language Processing models.
- | `Virtual Assistant`_
  | This is a simple virtual assistant. With it, you can search the Internet, access websites, open programs, and more using just your voice.
  | This virtual assistant supports the English and Portuguese languages and has many settings that you can adjust to your liking.
- | `Bad Advice`_
  | This python module responds to yes or no questions. It dishes out its advice at random.
  | Disclaimer: Do not actually act on this advice ;)
- | `Spanish Conjugations Quiz`_
  | Python+Flask web app that uses mlconjug to dynamically generate foreign language conjugation questions.
- | `Silver Rogue DF`_
  | A dwarf-fortress adventure mode-inspired rogue-like Pygame Python3 game.
- | `learn-spanish-react`_
  | A WebApp to learn Spanish.
- | `Learn_vocab`_
  | Application for German-French vocabulary with simple GUI.

BibTeX
------

If you want to cite mlconjug3 in an academic publication use this citation format:

.. code:: bibtex

   @article{mlconjug3,
     title={mlconjug3},
     author={Sekou Diao},
     journal={GitHub. Note: https://github.com/SekouDiaoNlp/mlconjug3 Cited by},
     year={2021}
   }


Credits
-------

This package was created with the help of Verbiste_ and scikit-learn_.

The logo was designed by Zuur_.

.. _Verbiste: https://perso.b2b2c.ca/~sarrazip/dev/verbiste.html
.. _scikit-learn: http://scikit-learn.org/stable/index.html
.. _Zuur: https://github.com/zuuritaly
.. _`Generative Grading Neural Approximate Parsing for Automated Student Feedback`: https://arxiv.org/abs/1905.09916
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
