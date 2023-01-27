.. image:: https://raw.githubusercontent.com/SekouDiaoNlp/mlconjug3/master/logo/logotype2%20mlconjug.png
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: mlconjug3 PyPi Home Page

----

.. image:: https://img.shields.io/badge/maintainer-SekouDiaoNlp-blue
        :target: https://GitHub.com/SekouDiaoNlp/mlconjug3
        :alt: Package Maintener

.. image:: https://img.shields.io/pypi/pyversions/mlconjug3
        :target: https://pypi.python.org/pypi/mlconjug3
        :alt: Compatible Python versions

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

.. image:: https://github.com/SekouDiaoNlp/mlconjug3/workflows/mlconjug3/badge.svg
        :target: https://github.com/SekouDiaoNlp/mlconjug3/actions
        :alt: Build status on Windows, MacOs and Linux

.. image:: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/shield.svg
        :target: https://pyup.io/repos/github/SekouDiaoNlp/mlconjug3/
        :alt: Dependencies status

.. image:: https://readthedocs.org/projects/mlconjug3/badge/?version=latest
        :target: https://mlconjug3.readthedocs.io/en/latest/readme.html
        :alt: Documentation Status

.. image:: https://bestpractices.coreinfrastructure.org/projects/6961/badge
        :target: https://bestpractices.coreinfrastructure.org/projects/6961/
        :alt: OpenSSF Best Practices

.. image:: https://snyk-widget.herokuapp.com/badge/pip/mlconjug3/badge.svg
        :target: https://snyk.io/test/github/SekouDiaoNlp/mlconjug3?targetFile=requirements.txt
        :alt: Code Vulnerability Status

.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
        :target: https://GitHub.com/SekouDiaoNlp/mlconjug3/graphs/commit-activity
        :alt: Package Maintenance Status

.. image:: https://api.securityscorecards.dev/projects/github.com/SekouDiaoNlp/mlconjug3/badge
        :target: https://api.securityscorecards.dev/projects/github.com/SekouDiaoNlp/mlconjug3/
        :alt: OpenSSF ScoreCard

.. image:: https://codecov.io/gh/SekouDiaoNlp/mlconjug3/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/SekouDiaoNlp/mlconjug3
        :alt: Code Coverage Status

.. image:: https://img.shields.io/mastodon/follow/109313632815812004?domain=https%3A%2F%2Ffosstodon.org&style=plastic
        :target: https://fosstodon.org/@SekouDiao
        :alt: Follow me on Mastodon


----

=========
mlconjug3
=========

Welcome to mlconjug3, the ultimate tool for language learners, teachers, developers, researchers, and anyone who wants to master verb conjugation in multiple languages. With mlconjug3, you can easily conjugate any verb in French, English, Spanish, Italian, Portuguese, and Romanian (with more languages coming soon) using advanced Machine Learning techniques.

Our pre-trained models use a binary feature extractor, Linear Support Vector Classification, and Stochastic Gradient Descent to deliver over 99% accuracy in predicting conjugation class for unknown verbs. And, with our easy-to-use API and CLI, you can quickly modify and retrain the models using any compatible classifiers from scikit-learn. Plus, we use caching and multiprocessing for maximum performance, so you can focus on perfecting your language skills.

But that's not all - mlconjug3 also offers a variety of other features, such as:

- Command Line Interface tool for quick and convenient use
- Easy-to-use and intuitive API for integration into your own projects
- Extensive documentation and community support for troubleshooting and expanding capabilities
- Customizable settings to modify the User Interface theme, fine-tune performance and adapt to different use cases
- Regular updates and improvements to ensure optimal performance
- Integration with popular libraries such as scikit-learn and numpy for machine learning tasks
- Support for multiple languages, including English, Spanish, French, and German
- Robust error handling and troubleshooting capabilities

We are honored to have received recognition from the academic community, as mlconjug3 has been cited in a number of publications. It is a testament to the hard work and dedication of our team, and we are humbled by the interest and support of our users.


----

.. image:: https://raw.githubusercontent.com/SekouDiaoNlp/mlconjug3/master/docs/images/D798CD83-9383-432F-9D52-1BB304FC99EB.png
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



Installation
------------

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

    $ git clone git://github.com/SekouDiaoNlp/mlconjug3

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/SekouDiaoNlp/mlconjug3/tarball/master

Once you have a copy of the source, get in the source directory and you can install it with:

.. code-block:: console

    $ python setup.py install

Alternatively, you can use poetry to install the software:

.. code-block:: console

    $ pip install poetry
    
    $ poetry install


.. _Github repo: https://github.com/SekouDiaoNlp/mlconjug3
.. _tarball: https://github.com/SekouDiaoNlp/mlconjug3/tarball/master



Academic publications citing mlconjug3
--------------------------------------

- | Gerard Canal, Senka Krivic ́, Paul Luff, Andrew Coles.
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
     journal={GitHub. Note: https://github.com/SekouDiaoNlp/mlconjug3 Cited by},
     year={2023}
   }


Software projects using mlconjug3
---------------------------------


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


Signing of Releases
-------------------

Starting with version 3.10, all versions of the mlconjug3 package released on PyPi and GitHub will be signed using sigstore. This is to ensure the authenticity and integrity of the package, and to provide an added layer of security for our users.

Signing a software package is a way to ensure that the package has not been tampered with and that it comes from a trusted source. This is important because malicious actors may try to tamper with a package by adding malware or other unwanted code, or by pretending to be the author of the package.

By signing mlconjug3 releases using sigstore, users can verify that the package they are downloading is the one that was created and uploaded by the package's author, Sekou Diao (diao.sekou.nlp@gmail.com), and that it has not been tampered with. This provides an additional layer of security for users and helps to ensure that they can trust the package they are using.

What is sigstore?
~~~~~~~~~~~~~~~~~

Sigstore is an open-source tool that allows developers to easily sign their software releases, making it easy for users to verify the authenticity of the package. The signature is cryptographically verified against the developer's public key, which is stored on a publicly accessible keyserver. This ensures that the package has not been tampered with and that it was indeed released by the developer who claims to have released it.

How to verify the signature of a release?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To verify the package, you can use the instructions provided below, which will show you how to check the package's signature and certificate using the python package sigstore, and also check for claims specific to GitHub Actions.


To verify a mlconjug3 release, the sigstore python module can be used. By default, sigstore verify will attempt to find a <filename>.sig and <filename>.crt in the same directory as the file being verified. For example, to verify the file mlconjug3-3.10.tar.gz, sigstore verify will look for mlconjug3-3.10.tar.gz.sig and mlconjug3-3.10.tar.gz.crt.

To verify the signature, use the following command:

.. code-block:: console
    
    $ python -m sigstore verify identity mlconjug3-3.10.tar.gz \
        --cert-identity 'diao.sekou.nlp@gmail.com' \
        --cert-oidc-issuer 'https://github.com/login/oauth'


Multiple files can be verified at once:

.. code-block:: console

    $ python -m sigstore verify identity mlconjug3-3.10.tar.gz mlconjug3-3.10.0-py3-none-any.whl \
        --cert-identity 'diao.sekou.nlp@gmail.com' \
        --cert-oidc-issuer 'https://github.com/login/oauth'

If the signature and certificate files are at different paths, they can be specified explicitly (but only for one file at a time):

.. code-block:: console

    $ python -m sigstore verify identity mlconjug3-3.10.tar.gz \
        --certificate some/other/path/mlconjug3-3.10.crt \
        --signature some/other/path/mlconjug3-3.10.sig \
        --cert-identity 'diao.sekou.nlp@gmail.com' \
        --cert-oidc-issuer 'https://github.com/login/oauth'

Verifying signatures from GitHub Actions:

.. code-block:: console

    $ python -m sigstore verify github mlconjug3-3.10.tar.gz \
        --certificate mlconjug3-3.10.tar.gz.crt \
        --signature mlconjug3-3.10.tar.gz.sig \
        --cert-identity https://github.com/diao.sekou.nlp/mlconjug3/.github/workflows/sign_and_publish.yml@refs/tags/v3.10.0

GitHub Actions specific claims can also be verified by adding flags such as --trigger, --sha, --name, --repository, and --ref.

Please note that these are examples and the exact file names and paths may vary depending on the version and distribution of mlconjug3 being verified. It is important to ensure that the correct signature and certificate files are being used for verification.


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
